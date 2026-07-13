"""Canonical one-row-per-target-date prediction log schema."""
from __future__ import annotations

from config import COMPONENTS

BASE_COLUMNS = [
    "run_timestamp_utc",
    "date_made",
    "target_date",
    "issue_timing",
    "lag2_date",
    "lag7_date",
    "weather_proxy",
    "model_trained_at_utc",
    "t_mean",
    "t_max",
    "t_min",
    "wind_max",
    "solar_rad",
]

COMPONENT_COLUMNS: list[str] = []
for component in COMPONENTS:
    COMPONENT_COLUMNS += [
        f"pred_{component}_gw",
        f"baseline_{component}_gw",
        f"actual_{component}_gw",
        f"error_{component}_gw",
        f"baseline_error_{component}_gw",
    ]

RESIDUAL_COLUMNS = [
    "pred_residual_gw",
    "baseline_residual_gw",
    "actual_residual_gw",
    "error_residual_gw",
    "baseline_error_residual_gw",
]

PRICE_COLUMNS = [
    "pred_price_peak_eur_mwh",
    "baseline_price_peak_eur_mwh",
    "actual_price_peak_eur_mwh",
    "actual_price_mean_eur_mwh",
    "price_error_eur_mwh",
    "baseline_price_error_eur_mwh",
]

RISK_COLUMNS = [
    "risk_position_side",
    "risk_position_mwh",
    "illustrative_capital_eur",
    "var_limit_eur",
    "vol30_eur_mwh",
    "vol90_eur_mwh",
    "var95_eur",
    "var99_eur",
    "max_size_mwh",
    "risk_regime",
    "realized_pnl_eur",
    "var95_breach",
]

STATUS_COLUMNS = ["forecast_status", "grade_status"]

LOG_COLUMNS = (
    BASE_COLUMNS
    + COMPONENT_COLUMNS
    + RESIDUAL_COLUMNS
    + PRICE_COLUMNS
    + RISK_COLUMNS
    + STATUS_COLUMNS
)
