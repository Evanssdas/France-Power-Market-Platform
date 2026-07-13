"""Train and honestly validate the six France power models.

The price model is trained on out-of-fold component forecasts rather than
in-sample component predictions. This prevents optimistic validation leakage.
"""
from __future__ import annotations

import datetime as dt
import json
from pathlib import Path

import lightgbm as lgb
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import TimeSeriesSplit

from config import (
    COMPONENTS,
    COMPONENT_FEATURES,
    MODEL_FILES,
    MODEL_METADATA_PATH,
    PRICE_FEATURES,
    TARGET_COLUMNS,
    TRAINING_METRICS_PATH,
    WX_FEATURES,
    load_settings,
)
from fr_common import (
    calendar_weather_features,
    fetch_generation_chunked,
    fetch_price_chunked,
    fetch_weather_history,
    inverse_price_transform,
    price_transform,
)

HISTORY_DAYS = 540
ARCHIVE_LAG_DAYS = 6
RANDOM_STATE = 42


def make_component_model() -> lgb.LGBMRegressor:
    return lgb.LGBMRegressor(
        objective="mae",
        n_estimators=500,
        learning_rate=0.03,
        num_leaves=31,
        min_child_samples=20,
        subsample=0.8,
        subsample_freq=1,
        colsample_bytree=0.8,
        reg_lambda=0.1,
        random_state=RANDOM_STATE,
        verbose=-1,
    )


def make_price_model() -> lgb.LGBMRegressor:
    return lgb.LGBMRegressor(
        objective="mae",
        n_estimators=600,
        learning_rate=0.03,
        num_leaves=31,
        min_child_samples=20,
        subsample=0.8,
        subsample_freq=1,
        colsample_bytree=0.8,
        reg_lambda=0.1,
        random_state=RANDOM_STATE,
        verbose=-1,
    )


def prepare_dataset() -> pd.DataFrame:
    settings = load_settings()
    end = dt.date.today() - dt.timedelta(days=2)
    start = end - dt.timedelta(days=HISTORY_DAYS)
    print(f"Downloading Energy-Charts history: {start} to {end}")
    generation = fetch_generation_chunked(start, end)
    price = fetch_price_chunked(start, end)

    weather_end = min(end, dt.date.today() - dt.timedelta(days=ARCHIVE_LAG_DAYS))
    print(f"Downloading Open-Meteo history: {start} to {weather_end}")
    weather = fetch_weather_history(
        start,
        weather_end,
        lat=float(settings["weather_lat"]),
        lon=float(settings["weather_lon"]),
    )

    frame = generation.join(price, how="inner").join(weather, how="inner")
    frame.index = pd.to_datetime(frame.index)
    frame = frame.sort_index()

    # Calendar and temperature-derived features.
    feature_rows = []
    for stamp, row in frame.iterrows():
        weather_row = {
            "t_mean": float(row["t_mean"]),
            "t_max": float(row["t_max"]),
            "t_min": float(row["t_min"]),
            "wind_max": float(row["wind_max"]),
            "solar_rad": float(row["solar_rad"]),
        }
        feature_rows.append(calendar_weather_features(stamp.date(), weather_row))
    features = pd.DataFrame(feature_rows, index=frame.index)
    for col in features.columns:
        frame[col] = features[col]

    # A 10:30 D-1 forecast cannot know the completed D-1 daily mean. Therefore
    # lag2 and lag7 are used: the most recent completed day and the comparable
    # day one week earlier, matching live information availability.
    for component, target in TARGET_COLUMNS.items():
        frame[f"{component}_lag2"] = frame[target].shift(2)
        frame[f"{component}_lag7"] = frame[target].shift(7)
    frame["price_lag2"] = frame["price_peak"].shift(2)
    frame["price_lag7"] = frame["price_peak"].shift(7)

    frame = frame.replace([np.inf, -np.inf], np.nan)
    print(f"Joined usable calendar span: {frame.index.min().date()} to {frame.index.max().date()}")
    print(f"Rows before per-model cleaning: {len(frame)}")
    return frame


def component_dataset(frame: pd.DataFrame, component: str) -> pd.DataFrame:
    target = TARGET_COLUMNS[component]
    needed = [target, *WX_FEATURES, f"{component}_lag2", f"{component}_lag7"]
    data = frame.dropna(subset=needed).copy()
    data["lag2"] = data[f"{component}_lag2"]
    data["lag7"] = data[f"{component}_lag7"]
    return data


def metric_block(actual: pd.Series, pred: np.ndarray, baseline: pd.Series) -> dict[str, float | int]:
    actual_np = np.asarray(actual, dtype=float)
    pred_np = np.asarray(pred, dtype=float)
    base_np = np.asarray(baseline, dtype=float)
    mae = float(mean_absolute_error(actual_np, pred_np))
    base_mae = float(mean_absolute_error(actual_np, base_np))
    rmse = float(np.sqrt(mean_squared_error(actual_np, pred_np)))
    bias = float(np.mean(pred_np - actual_np))
    improvement = float(100.0 * (1.0 - mae / base_mae)) if base_mae else float("nan")
    return {
        "n": int(len(actual_np)),
        "mae": mae,
        "rmse": rmse,
        "bias": bias,
        "baseline_mae": base_mae,
        "improvement_pct": improvement,
    }


def oof_predictions(data: pd.DataFrame, target: str) -> pd.Series:
    """Expanding-window out-of-fold predictions for leakage-safe stacking."""
    result = pd.Series(np.nan, index=data.index, dtype=float)
    splits = min(5, max(2, len(data) // 80))
    splitter = TimeSeriesSplit(n_splits=splits)
    for train_idx, validation_idx in splitter.split(data):
        train = data.iloc[train_idx]
        validation = data.iloc[validation_idx]
        if len(train) < 80:
            continue
        model = make_component_model()
        model.fit(train[COMPONENT_FEATURES], train[target])
        result.iloc[validation_idx] = model.predict(validation[COMPONENT_FEATURES])
    return result


def build_forecast_residual(
    base: pd.DataFrame,
    predictions: dict[str, pd.Series],
) -> pd.DataFrame:
    output = base.copy()
    for component, series in predictions.items():
        output[f"f_{component}"] = series.reindex(output.index)
    output["f_residual"] = (
        output["f_demand"]
        - output["f_nuclear"]
        - output["f_wind"]
        - output["f_solar"]
        - output["f_hydro"]
    )
    return output


def save_model(model: lgb.LGBMRegressor, path: Path) -> None:
    model.booster_.save_model(str(path))
    print(f"Saved {path.name}")


def main() -> None:
    frame = prepare_dataset()
    complete_dates = frame.dropna(subset=["price_peak"]).index
    if len(complete_dates) < 300:
        raise RuntimeError(f"Only {len(complete_dates)} usable days; at least 300 are required")

    holdout_days = min(180, max(90, len(complete_dates) // 3))
    split_date = complete_dates[-holdout_days]
    train_end = split_date - pd.Timedelta(days=1)
    print(f"Time holdout begins {split_date.date()} ({holdout_days} calendar rows targeted)")

    metrics: dict[str, dict] = {}
    train_component_models: dict[str, lgb.LGBMRegressor] = {}
    final_component_models: dict[str, lgb.LGBMRegressor] = {}
    train_oof: dict[str, pd.Series] = {}
    test_component_predictions: dict[str, pd.Series] = {}
    full_oof: dict[str, pd.Series] = {}

    print("\nComponent validation (baseline = latest completed day, lag2)")
    print("model       n     MAE   baseline   improvement")
    print("-" * 56)

    for component in COMPONENTS:
        target = TARGET_COLUMNS[component]
        data = component_dataset(frame, component)
        train = data.loc[data.index <= train_end]
        test = data.loc[data.index >= split_date]
        if len(train) < 150 or len(test) < 30:
            raise RuntimeError(f"Insufficient {component} train/test rows")

        model = make_component_model()
        model.fit(train[COMPONENT_FEATURES], train[target])
        prediction = model.predict(test[COMPONENT_FEATURES])
        block = metric_block(test[target], prediction, test["lag2"])
        metrics[component] = block
        verdict = "WINS" if block["mae"] < block["baseline_mae"] else "loses"
        print(
            f"{component:<10} {block['n']:>3} {block['mae']:7.2f} "
            f"{block['baseline_mae']:10.2f} {verdict:>6} ({block['improvement_pct']:+6.1f}%)"
        )
        train_component_models[component] = model
        train_oof[component] = oof_predictions(train, target)
        test_component_predictions[component] = pd.Series(prediction, index=test.index)

        final_model = make_component_model()
        final_model.fit(data[COMPONENT_FEATURES], data[target])
        final_component_models[component] = final_model
        full_oof[component] = oof_predictions(data, target)
        save_model(final_model, MODEL_FILES[component])

    # Honest price validation: price training uses OOF component forecasts;
    # price holdout uses component models trained only before the holdout.
    price_base_cols = ["price_peak", *WX_FEATURES, "price_lag2", "price_lag7"]
    price_train_base = frame.loc[frame.index <= train_end].dropna(subset=price_base_cols)
    price_test_base = frame.loc[frame.index >= split_date].dropna(subset=price_base_cols)

    price_train = build_forecast_residual(price_train_base, train_oof)
    price_test = build_forecast_residual(price_test_base, test_component_predictions)
    price_train = price_train.dropna(subset=PRICE_FEATURES + ["price_peak"])
    price_test = price_test.dropna(subset=PRICE_FEATURES + ["price_peak"])
    if len(price_train) < 150 or len(price_test) < 30:
        raise RuntimeError("Insufficient leakage-safe rows for the price model")

    price_model = make_price_model()
    price_model.fit(price_train[PRICE_FEATURES], price_transform(price_train["price_peak"]))
    price_prediction = inverse_price_transform(price_model.predict(price_test[PRICE_FEATURES]))
    price_metrics = metric_block(price_test["price_peak"], price_prediction, price_test["price_lag2"])

    result = price_test.copy()
    result["prediction"] = price_prediction
    result["abs_error"] = (result["price_peak"] - result["prediction"]).abs()
    result["baseline_abs_error"] = (result["price_peak"] - result["price_lag2"]).abs()
    spike_threshold = float(result["price_peak"].quantile(0.85))
    segment_metrics = {}
    for label, mask in {
        "normal": result["price_peak"] < spike_threshold,
        "spike": result["price_peak"] >= spike_threshold,
    }.items():
        segment = result.loc[mask]
        segment_metrics[label] = {
            "n": int(len(segment)),
            "model_mae": float(segment["abs_error"].mean()),
            "baseline_mae": float(segment["baseline_abs_error"].mean()),
        }
    price_metrics["spike_threshold_eur_mwh"] = spike_threshold
    price_metrics["segments"] = segment_metrics
    metrics["price"] = price_metrics
    verdict = "WINS" if price_metrics["mae"] < price_metrics["baseline_mae"] else "loses"
    print("\nPrice validation (leakage-safe forecast residual)")
    print(
        f"price      {price_metrics['n']:>3} {price_metrics['mae']:7.2f} "
        f"{price_metrics['baseline_mae']:10.2f} {verdict:>6} "
        f"({price_metrics['improvement_pct']:+6.1f}%)"
    )
    for label, segment in segment_metrics.items():
        seg_verdict = "WINS" if segment["model_mae"] < segment["baseline_mae"] else "loses"
        print(
            f"  {label:<7} {segment['n']:>3}d | model {segment['model_mae']:7.2f} | "
            f"baseline {segment['baseline_mae']:7.2f} | {seg_verdict}"
        )

    # Final price model: OOF component forecasts across the full history.
    price_full_base = frame.dropna(subset=price_base_cols)
    price_full = build_forecast_residual(price_full_base, full_oof)
    price_full = price_full.dropna(subset=PRICE_FEATURES + ["price_peak"])
    final_price_model = make_price_model()
    final_price_model.fit(
        price_full[PRICE_FEATURES],
        price_transform(price_full["price_peak"]),
    )
    save_model(final_price_model, MODEL_FILES["price"])

    metadata = {
        "trained_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "training_start": frame.index.min().date().isoformat(),
        "training_end": frame.index.max().date().isoformat(),
        "holdout_start": split_date.date().isoformat(),
        "forecast_issue_design": "10:30 Europe/Paris on D-1",
        "information_lags": {
            "lag2": "D-2, latest completed daily observation at issue time",
            "lag7": "D-7, comparable completed observation one week earlier",
        },
        "weather_proxy": load_settings().get("weather_label", "Paris proxy"),
        "weather_training_source": "Open-Meteo archive (realised historical weather)",
        "weather_serving_source": "Open-Meteo live forecast",
        "component_features": COMPONENT_FEATURES,
        "price_features": PRICE_FEATURES,
        "price_transform": "asinh(price / 50); inverse = sinh(prediction) * 50",
        "price_target": "daily maximum French day-ahead price (EUR/MWh)",
        "generation_targets": "daily mean GW",
        "price_stacking": "out-of-fold component forecasts",
    }
    MODEL_METADATA_PATH.write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    TRAINING_METRICS_PATH.write_text(json.dumps(metrics, indent=2), encoding="utf-8")

    lines = [
        "# France Power Model Card",
        "",
        f"_Trained {metadata['trained_at_utc']}._",
        "",
        "## Design",
        "",
        "- Forecast issue time: 10:30 Europe/Paris on the day before delivery.",
        "- Component lags: D-2 and D-7, because D-1 daily means are incomplete at issue time.",
        "- Price stacking: out-of-fold component predictions; no in-sample residual-demand leakage.",
        "- Weather: Paris is currently an explicit national proxy and a known limitation.",
        "- Holdout weather uses realised archive values, while live serving uses forecast weather; live accuracy may therefore be worse.",
        "- Generation targets: daily mean GW.",
        "- Price target: daily maximum France day-ahead price in EUR/MWh.",
        "",
        "## Holdout results",
        "",
        "| model | n | MAE | baseline MAE | improvement |",
        "|---|---:|---:|---:|---:|",
    ]
    for name in [*COMPONENTS, "price"]:
        block = metrics[name]
        unit = "EUR/MWh" if name == "price" else "GW"
        lines.append(
            f"| {name} ({unit}) | {block['n']} | {block['mae']:.2f} | "
            f"{block['baseline_mae']:.2f} | {block['improvement_pct']:+.1f}% |"
        )
    lines += [
        "",
        "A negative improvement means the model lost to the persistence baseline. "
        "That result must be reported honestly rather than hidden.",
    ]
    (Path(__file__).resolve().parent / "MODEL_CARD.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )
    print("\nWrote model_metadata.json, training_metrics.json and MODEL_CARD.md")


if __name__ == "__main__":
    main()
