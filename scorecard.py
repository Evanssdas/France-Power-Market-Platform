"""Create an honest rolling scorecard from the self-grading daily log."""
from __future__ import annotations

import math

import numpy as np
import pandas as pd

from config import COMPONENTS, LOG_PATH, ROOT

OUTPUT = ROOT / "SCORECARD.md"


def metrics(actual: pd.Series, predicted: pd.Series, baseline: pd.Series) -> dict[str, float | int]:
    frame = pd.DataFrame(
        {"actual": actual, "predicted": predicted, "baseline": baseline}
    ).apply(pd.to_numeric, errors="coerce").dropna()
    if frame.empty:
        return {"n": 0}
    model_error = frame["predicted"] - frame["actual"]
    base_error = frame["baseline"] - frame["actual"]
    mae = float(model_error.abs().mean())
    baseline_mae = float(base_error.abs().mean())
    improvement = 100.0 * (1.0 - mae / baseline_mae) if baseline_mae else math.nan
    return {
        "n": int(len(frame)),
        "mae": mae,
        "baseline_mae": baseline_mae,
        "improvement_pct": improvement,
        "rmse": float(np.sqrt(np.mean(np.square(model_error)))),
        "bias": float(model_error.mean()),
        "model_wins_pct": float((model_error.abs() < base_error.abs()).mean() * 100.0),
    }


def main() -> None:
    if not LOG_PATH.exists() or LOG_PATH.stat().st_size == 0:
        OUTPUT.write_text("# France Power Scorecard\n\nNo forecasts have been logged yet.\n", encoding="utf-8")
        print("No log yet; wrote empty SCORECARD.md")
        return

    log = pd.read_csv(LOG_PATH)
    if "issue_timing" in log.columns:
        official = log[log["issue_timing"].fillna("") == "pre_auction"].copy()
    else:
        official = log.copy()
    graded = official[official.get("grade_status", "").fillna("") == "graded"].copy()

    lines = [
        "# France Power Forecast Scorecard",
        "",
        "_Only forecasts marked **pre_auction** and later fully graded are included._",
        "",
        f"- Logged rows: **{len(log)}**",
        f"- Official pre-auction rows: **{len(official)}**",
        f"- Fully graded official rows: **{len(graded)}**",
        "",
    ]
    if len(graded) < 30:
        lines += [
            "> **Sample warning:** fewer than 30 graded forecasts are available. "
            "The figures below are operational checks, not strong evidence of model skill.",
            "",
        ]

    lines += [
        "## Model versus persistence",
        "",
        "The persistence baseline uses the latest completed daily observation available "
        "at the 10:30 D-1 issue time (D-2).",
        "",
        "| target | n | model MAE | baseline MAE | improvement | RMSE | bias | model wins |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]

    targets = [*COMPONENTS, "residual"]
    for target in targets:
        block = metrics(
            graded.get(f"actual_{target}_gw", pd.Series(dtype=float)),
            graded.get(f"pred_{target}_gw", pd.Series(dtype=float)),
            graded.get(f"baseline_{target}_gw", pd.Series(dtype=float)),
        )
        if block["n"] == 0:
            lines.append(f"| {target} (GW) | 0 | — | — | — | — | — | — |")
        else:
            lines.append(
                f"| {target} (GW) | {block['n']} | {block['mae']:.2f} | "
                f"{block['baseline_mae']:.2f} | {block['improvement_pct']:+.1f}% | "
                f"{block['rmse']:.2f} | {block['bias']:+.2f} | {block['model_wins_pct']:.1f}% |"
            )

    price = metrics(
        graded.get("actual_price_peak_eur_mwh", pd.Series(dtype=float)),
        graded.get("pred_price_peak_eur_mwh", pd.Series(dtype=float)),
        graded.get("baseline_price_peak_eur_mwh", pd.Series(dtype=float)),
    )
    if price["n"] == 0:
        lines.append("| peak price (EUR/MWh) | 0 | — | — | — | — | — | — |")
    else:
        lines.append(
            f"| peak price (EUR/MWh) | {price['n']} | {price['mae']:.2f} | "
            f"{price['baseline_mae']:.2f} | {price['improvement_pct']:+.1f}% | "
            f"{price['rmse']:.2f} | {price['bias']:+.2f} | {price['model_wins_pct']:.1f}% |"
        )

    lines += ["", "## Price direction", ""]
    price_frame = graded[[
        c for c in [
            "pred_price_peak_eur_mwh",
            "baseline_price_peak_eur_mwh",
            "actual_price_peak_eur_mwh",
        ] if c in graded.columns
    ]].apply(pd.to_numeric, errors="coerce").dropna()
    if len(price_frame):
        predicted_direction = np.sign(
            price_frame["pred_price_peak_eur_mwh"]
            - price_frame["baseline_price_peak_eur_mwh"]
        )
        actual_direction = np.sign(
            price_frame["actual_price_peak_eur_mwh"]
            - price_frame["baseline_price_peak_eur_mwh"]
        )
        directional_accuracy = float((predicted_direction == actual_direction).mean() * 100.0)
        lines += [
            f"Directional accuracy versus the D-2 reference price: **{directional_accuracy:.1f}%** "
            f"across **{len(price_frame)}** graded forecasts.",
            "",
        ]
    else:
        lines += ["No graded price forecasts yet.", ""]

    lines += ["## Illustrative VaR backtest", ""]
    if {"var95_breach", "realized_pnl_eur"}.issubset(graded.columns):
        risk = graded.copy()
        risk["var95_breach"] = risk["var95_breach"].astype(str).str.lower().map(
            {"true": True, "false": False}
        )
        risk = risk.dropna(subset=["var95_breach"])
        breaches = int(risk["var95_breach"].sum()) if len(risk) else 0
        rate = 100.0 * breaches / len(risk) if len(risk) else 0.0
        lines += [
            f"- Observations with a usable risk record: **{len(risk)}**",
            f"- 95% VaR breaches: **{breaches}**",
            f"- Observed breach rate: **{rate:.1f}%** (the model benchmark is approximately 5% over a large sample)",
            "",
        ]
    else:
        lines += ["No graded VaR observations yet.", ""]

    lines += [
        "## Reading the table",
        "",
        "- **Positive improvement:** the model beat persistence.",
        "- **Negative improvement:** persistence was better; this must not be hidden.",
        "- **Bias above zero:** the model tends to predict too high.",
        "- **Bias below zero:** the model tends to predict too low.",
        "- **Model wins:** percentage of individual days when the model absolute error was smaller.",
    ]
    OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUTPUT.name}")


if __name__ == "__main__":
    main()
