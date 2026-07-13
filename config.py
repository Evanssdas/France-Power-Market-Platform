"""Configuration shared by the France power analytics pipeline."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
SETTINGS_PATH = ROOT / "settings.json"
LOG_PATH = ROOT / "fr_predictions_log.csv"
MODEL_METADATA_PATH = ROOT / "model_metadata.json"
TRAINING_METRICS_PATH = ROOT / "training_metrics.json"

TIMEZONE = "Europe/Paris"
BASE_ENERGY_CHARTS = "https://api.energy-charts.info"

COMPONENTS = ("demand", "nuclear", "wind", "solar", "hydro")
TARGET_COLUMNS = {
    "demand": "load",
    "nuclear": "nuclear",
    "wind": "wind",
    "solar": "solar",
    "hydro": "hydro",
}

WX_FEATURES = [
    "t_mean",
    "t_max",
    "t_min",
    "wind_max",
    "solar_rad",
    "HDD",
    "CDD",
    "dow",
    "is_we",
    "month",
    "doy",
    "is_hol",
]
COMPONENT_FEATURES = WX_FEATURES + ["lag2", "lag7"]
PRICE_FEATURES = [
    "f_residual",
    *WX_FEATURES,
    "price_lag2",
    "price_lag7",
]

MODEL_FILES = {
    "demand": ROOT / "model_fr_demand.txt",
    "nuclear": ROOT / "model_fr_nuclear.txt",
    "wind": ROOT / "model_fr_wind.txt",
    "solar": ROOT / "model_fr_solar.txt",
    "hydro": ROOT / "model_fr_hydro.txt",
    "price": ROOT / "model_fr_price.txt",
}

PRICE_TRANSFORM_SCALE = 50.0
Z_95 = 1.6448536269514722
Z_99 = 2.3263478740408408


def load_settings() -> dict[str, Any]:
    """Load user-editable paper-trading settings."""
    with SETTINGS_PATH.open("r", encoding="utf-8") as fh:
        settings = json.load(fh)

    required = {
        "weather_lat",
        "weather_lon",
        "illustrative_position_mwh",
        "illustrative_capital_eur",
        "var_limit_percent_of_capital",
        "max_position_mwh",
    }
    missing = sorted(required - set(settings))
    if missing:
        raise KeyError(f"Missing settings: {missing}")
    return settings


def var_limit_eur(settings: dict[str, Any]) -> float:
    """Derive the illustrative VaR limit from capital and risk appetite."""
    return float(settings["illustrative_capital_eur"]) * float(
        settings["var_limit_percent_of_capital"]
    )
