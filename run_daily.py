"""Daily France forecast, self-grading and risk snapshot pipeline."""
from __future__ import annotations

import datetime as dt
import json
from pathlib import Path
from zoneinfo import ZoneInfo

import lightgbm as lgb
import numpy as np
import pandas as pd

from config import (
    COMPONENTS,
    COMPONENT_FEATURES,
    LOG_PATH,
    MODEL_FILES,
    MODEL_METADATA_PATH,
    PRICE_FEATURES,
    TARGET_COLUMNS,
    TIMEZONE,
    load_settings,
    var_limit_eur,
)
from fr_common import (
    calendar_weather_features,
    fetch_generation_chunked,
    fetch_price_chunked,
    fetch_weather_forecast,
    inverse_price_transform,
    risk_snapshot,
)
from log_schema import LOG_COLUMNS


def blank_log() -> pd.DataFrame:
    return pd.DataFrame(columns=LOG_COLUMNS)


def read_log() -> pd.DataFrame:
    if not LOG_PATH.exists() or LOG_PATH.stat().st_size == 0:
        return blank_log()
    log = pd.read_csv(LOG_PATH)
    for column in LOG_COLUMNS:
        if column not in log.columns:
            log[column] = np.nan
    log = log[LOG_COLUMNS]
    if "target_date" in log:
        log = log.drop_duplicates(subset=["target_date"], keep="last")
    return log


def numeric(value) -> float | None:
    try:
        parsed = float(value)
        return parsed if np.isfinite(parsed) else None
    except (TypeError, ValueError):
        return None


def predict_booster(path: Path, features: dict[str, float], names: list[str]) -> float:
    if not path.exists():
        raise FileNotFoundError(
            f"Missing {path.name}. Run train_models.py or the training notebook first."
        )
    frame = pd.DataFrame([{name: features[name] for name in names}], columns=names)
    booster = lgb.Booster(model_file=str(path))
    return float(booster.predict(frame)[0])


def upsert_row(log: pd.DataFrame, row: dict) -> pd.DataFrame:
    target = str(row["target_date"])
    mask = log["target_date"].astype(str) == target
    if mask.any():
        idx = log.index[mask][-1]
        for key, value in row.items():
            log.at[idx, key] = value
    else:
        complete = {column: row.get(column, np.nan) for column in LOG_COLUMNS}
        log = pd.concat([log, pd.DataFrame([complete])], ignore_index=True)
    return log


def backfill_actuals(log: pd.DataFrame, today: dt.date, settings: dict) -> pd.DataFrame:
    if log.empty:
        return log
    targets = pd.to_datetime(log["target_date"], errors="coerce").dt.date
    grade_status = log["grade_status"].fillna("").astype(str)
    due_mask = targets.notna() & (targets < today) & (grade_status != "graded")
    due = log.loc[due_mask]
    if due.empty:
        print("No past-due rows need grading")
        return log

    start = pd.to_datetime(due["target_date"]).min().date()
    end = pd.to_datetime(due["target_date"]).max().date()
    print(f"Backfilling actuals for {start} to {end}")
    generation = fetch_generation_chunked(start, end)
    prices = fetch_price_chunked(start, end)
    side_sign = 1.0 if settings["illustrative_position_side"] == "long" else -1.0
    position_mwh = float(settings["illustrative_position_mwh"])

    for idx, old in due.iterrows():
        target = pd.to_datetime(old["target_date"]).date()
        if target not in generation.index or target not in prices.index:
            log.at[idx, "grade_status"] = "waiting_for_actuals"
            continue

        complete = True
        for component in COMPONENTS:
            source = TARGET_COLUMNS[component]
            actual = numeric(generation.at[target, source])
            predicted = numeric(old[f"pred_{component}_gw"])
            baseline = numeric(old[f"baseline_{component}_gw"])
            log.at[idx, f"actual_{component}_gw"] = actual
            if actual is None:
                complete = False
            if predicted is not None and actual is not None:
                log.at[idx, f"error_{component}_gw"] = predicted - actual
            if baseline is not None and actual is not None:
                log.at[idx, f"baseline_error_{component}_gw"] = baseline - actual

        actual_residual = numeric(generation.at[target, "residual"])
        pred_residual = numeric(old["pred_residual_gw"])
        baseline_residual = numeric(old["baseline_residual_gw"])
        log.at[idx, "actual_residual_gw"] = actual_residual
        if pred_residual is not None and actual_residual is not None:
            log.at[idx, "error_residual_gw"] = pred_residual - actual_residual
        if baseline_residual is not None and actual_residual is not None:
            log.at[idx, "baseline_error_residual_gw"] = baseline_residual - actual_residual

        actual_peak = numeric(prices.at[target, "price_peak"])
        actual_mean = numeric(prices.at[target, "price_mean"])
        predicted_price = numeric(old["pred_price_peak_eur_mwh"])
        baseline_price = numeric(old["baseline_price_peak_eur_mwh"])
        log.at[idx, "actual_price_peak_eur_mwh"] = actual_peak
        log.at[idx, "actual_price_mean_eur_mwh"] = actual_mean
        if actual_peak is None:
            complete = False
        if predicted_price is not None and actual_peak is not None:
            log.at[idx, "price_error_eur_mwh"] = predicted_price - actual_peak
        if baseline_price is not None and actual_peak is not None:
            log.at[idx, "baseline_price_error_eur_mwh"] = baseline_price - actual_peak
            pnl = side_sign * position_mwh * (actual_peak - baseline_price)
            log.at[idx, "realized_pnl_eur"] = pnl
            var95 = numeric(old["var95_eur"])
            if var95 is not None:
                loss = max(0.0, -pnl)
                log.at[idx, "var95_breach"] = bool(loss > var95)

        log.at[idx, "grade_status"] = "graded" if complete else "partial_actuals"
        if complete:
            print(f"Graded {target}")
    return log


def make_forecast_row(
    today: dt.date,
    target: dt.date,
    local_now: dt.datetime,
    settings: dict,
) -> dict:
    metadata = json.loads(MODEL_METADATA_PATH.read_text(encoding="utf-8"))
    lag2_date = target - dt.timedelta(days=2)
    lag7_date = target - dt.timedelta(days=7)

    # Fetch enough history both for model lags and for the risk window.
    history_start = target - dt.timedelta(days=105)
    history_end = lag2_date
    generation = fetch_generation_chunked(history_start, history_end)
    prices = fetch_price_chunked(history_start, history_end)
    for required_date in (lag2_date, lag7_date):
        if required_date not in generation.index:
            raise KeyError(f"Generation history is missing required date {required_date}")
        if required_date not in prices.index:
            raise KeyError(f"Price history is missing required date {required_date}")

    weather = fetch_weather_forecast(
        target,
        lat=float(settings["weather_lat"]),
        lon=float(settings["weather_lon"]),
    )
    common = calendar_weather_features(target, weather)

    predictions: dict[str, float] = {}
    baselines: dict[str, float] = {}
    for component in COMPONENTS:
        source = TARGET_COLUMNS[component]
        features = {
            **common,
            "lag2": float(generation.at[lag2_date, source]),
            "lag7": float(generation.at[lag7_date, source]),
        }
        predictions[component] = predict_booster(
            MODEL_FILES[component], features, COMPONENT_FEATURES
        )
        baselines[component] = features["lag2"]

    pred_residual = (
        predictions["demand"]
        - predictions["nuclear"]
        - predictions["wind"]
        - predictions["solar"]
        - predictions["hydro"]
    )
    baseline_residual = float(generation.at[lag2_date, "residual"])
    price_features = {
        **common,
        "f_residual": pred_residual,
        "price_lag2": float(prices.at[lag2_date, "price_peak"]),
        "price_lag7": float(prices.at[lag7_date, "price_peak"]),
    }
    transformed_price = predict_booster(MODEL_FILES["price"], price_features, PRICE_FEATURES)
    pred_price = float(inverse_price_transform([transformed_price])[0])

    limit = var_limit_eur(settings)
    risk = risk_snapshot(
        prices["price_peak"],
        position_mwh=float(settings["illustrative_position_mwh"]),
        var_limit=limit,
    )

    row: dict = {
        "run_timestamp_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "date_made": today.isoformat(),
        "target_date": target.isoformat(),
        "issue_timing": "pre_auction" if local_now.time() < dt.time(12, 0) else "post_auction_manual",
        "lag2_date": lag2_date.isoformat(),
        "lag7_date": lag7_date.isoformat(),
        "weather_proxy": settings.get("weather_label", "Paris proxy"),
        "model_trained_at_utc": metadata.get("trained_at_utc", ""),
        **weather,
        "pred_residual_gw": pred_residual,
        "baseline_residual_gw": baseline_residual,
        "pred_price_peak_eur_mwh": pred_price,
        "baseline_price_peak_eur_mwh": price_features["price_lag2"],
        "risk_position_side": settings["illustrative_position_side"],
        "risk_position_mwh": float(settings["illustrative_position_mwh"]),
        "illustrative_capital_eur": float(settings["illustrative_capital_eur"]),
        "var_limit_eur": limit,
        "vol30_eur_mwh": risk["vol30_eur_mwh"],
        "vol90_eur_mwh": risk["vol90_eur_mwh"],
        "var95_eur": risk["var95_eur"],
        "var99_eur": risk["var99_eur"],
        "max_size_mwh": min(float(risk["max_size_mwh"]), float(settings["max_position_mwh"])),
        "risk_regime": risk["regime"],
        "forecast_status": "ok",
        "grade_status": "awaiting_actuals",
    }
    for component in COMPONENTS:
        row[f"pred_{component}_gw"] = predictions[component]
        row[f"baseline_{component}_gw"] = baselines[component]
    return row


def main() -> None:
    settings = load_settings()
    paris = ZoneInfo(TIMEZONE)
    local_now = dt.datetime.now(paris)
    today = local_now.date()
    target = today + dt.timedelta(days=1)

    log = read_log()
    try:
        log = backfill_actuals(log, today, settings)
    except Exception as exc:  # Preserve forecasts even if the data provider is temporarily unavailable.
        print(f"Backfill failed: {type(exc).__name__}: {exc}")

    existing = log[log["target_date"].astype(str) == target.isoformat()]
    existing_ok = (
        not existing.empty
        and existing.iloc[-1]["forecast_status"] == "ok"
    )
    if existing_ok:
        print(f"Forecast already exists for {target}; not overwriting the issued record")
    else:
        try:
            row = make_forecast_row(today, target, local_now, settings)
            log = upsert_row(log, row)
            print(
                f"Forecast {target}: demand {row['pred_demand_gw']:.2f} GW | "
                f"nuclear {row['pred_nuclear_gw']:.2f} GW | "
                f"residual {row['pred_residual_gw']:.2f} GW | "
                f"peak price €{row['pred_price_peak_eur_mwh']:.2f}/MWh"
            )
        except Exception as exc:
            failure = {
                "run_timestamp_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
                "date_made": today.isoformat(),
                "target_date": target.isoformat(),
                "issue_timing": "pre_auction" if local_now.time() < dt.time(12, 0) else "post_auction_manual",
                "forecast_status": f"failed: {type(exc).__name__}: {exc}",
                "grade_status": "not_forecast",
            }
            log = upsert_row(log, failure)
            print(f"Forecast failed: {type(exc).__name__}: {exc}")

    log = log[LOG_COLUMNS].drop_duplicates(subset=["target_date"], keep="last")
    log = log.sort_values("target_date", na_position="last")
    log.to_csv(LOG_PATH, index=False)
    print(f"Wrote {LOG_PATH.name} with {len(log)} rows")


if __name__ == "__main__":
    main()
