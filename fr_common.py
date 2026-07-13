"""Shared data, feature and risk helpers for the France pipeline."""
from __future__ import annotations

import datetime as dt
import math
from typing import Iterable

import holidays
import numpy as np
import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from config import (
    BASE_ENERGY_CHARTS,
    PRICE_TRANSFORM_SCALE,
    TIMEZONE,
    WX_FEATURES,
    Z_95,
    Z_99,
)

TIMEOUT = 90
SERIES = {
    "load": "Load",
    "nuclear": "Nuclear",
    "wind_on": "Wind onshore",
    "wind_off": "Wind offshore",
    "solar": "Solar",
    "hydro_ror": "Hydro Run-of-River",
    "hydro_res": "Hydro water reservoir",
    "gas": "Fossil gas",
}


def _session() -> requests.Session:
    retry = Retry(
        total=4,
        connect=4,
        read=4,
        backoff_factor=1.5,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=frozenset({"GET"}),
    )
    s = requests.Session()
    s.mount("https://", HTTPAdapter(max_retries=retry))
    s.headers.update({"User-Agent": "france-power-analytics/1.0"})
    return s


SESSION = _session()


def _get_json(url: str) -> dict:
    response = SESSION.get(url, timeout=TIMEOUT)
    response.raise_for_status()
    payload = response.json()
    if not isinstance(payload, dict):
        raise TypeError(f"Expected JSON object from {url}")
    return payload


def _aligned_series(values: Iterable, expected: int, name: str) -> pd.Series:
    s = pd.to_numeric(pd.Series(list(values)), errors="coerce")
    if len(s) != expected:
        raise ValueError(f"{name}: expected {expected} points, received {len(s)}")
    return s


def fetch_generation(start: dt.date, end: dt.date) -> pd.DataFrame:
    """Return daily mean French load/generation series in GW."""
    if start > end:
        raise ValueError("start must not be after end")
    url = f"{BASE_ENERGY_CHARTS}/public_power?country=fr&start={start}&end={end}"
    payload = _get_json(url)

    unix_seconds = payload.get("unix_seconds", [])
    production_types = payload.get("production_types", [])
    if not unix_seconds or not production_types:
        raise RuntimeError(f"No French generation data returned for {start} to {end}")

    ts = pd.to_datetime(pd.Series(unix_seconds), unit="s", utc=True).dt.tz_convert(TIMEZONE)
    out = pd.DataFrame({"ts": ts})
    by_name = {
        item.get("name"): item.get("data", [])
        for item in production_types
        if isinstance(item, dict)
    }
    for key, api_name in SERIES.items():
        if api_name in by_name:
            out[key] = _aligned_series(by_name[api_name], len(out), api_name) / 1000.0

    mandatory = {"load", "nuclear", "wind_on", "solar", "hydro_ror", "hydro_res"}
    missing = sorted(mandatory - set(out.columns))
    if missing:
        raise KeyError(f"Missing mandatory generation series: {missing}")

    out["date"] = out["ts"].dt.date
    daily = out.groupby("date").mean(numeric_only=True).sort_index()
    daily["wind"] = daily.get("wind_on", 0.0) + daily.get("wind_off", 0.0)
    daily["hydro"] = daily.get("hydro_ror", 0.0) + daily.get("hydro_res", 0.0)
    daily["residual"] = (
        daily["load"]
        - daily["nuclear"]
        - daily["wind"]
        - daily["solar"]
        - daily["hydro"]
    )
    return daily


def fetch_generation_chunked(start: dt.date, end: dt.date, chunk_days: int = 59) -> pd.DataFrame:
    frames: list[pd.DataFrame] = []
    cursor = start
    while cursor <= end:
        chunk_end = min(cursor + dt.timedelta(days=chunk_days), end)
        frames.append(fetch_generation(cursor, chunk_end))
        cursor = chunk_end + dt.timedelta(days=1)
    if not frames:
        return pd.DataFrame()
    result = pd.concat(frames).sort_index()
    return result[~result.index.duplicated(keep="last")]


def fetch_price(start: dt.date, end: dt.date) -> pd.DataFrame:
    """Return daily mean and maximum French day-ahead prices in EUR/MWh."""
    if start > end:
        raise ValueError("start must not be after end")
    url = f"{BASE_ENERGY_CHARTS}/price?bzn=FR&start={start}&end={end}"
    payload = _get_json(url)
    unix_seconds = payload.get("unix_seconds", [])
    prices = payload.get("price", [])
    if not unix_seconds or not prices:
        raise RuntimeError(f"No French price data returned for {start} to {end}")

    ts = pd.to_datetime(pd.Series(unix_seconds), unit="s", utc=True).dt.tz_convert(TIMEZONE)
    price = _aligned_series(prices, len(ts), "price")
    df = pd.DataFrame({"ts": ts, "price": price})
    df["date"] = df["ts"].dt.date
    grouped = df.groupby("date")["price"]
    return pd.DataFrame(
        {"price_mean": grouped.mean(), "price_peak": grouped.max()}
    ).sort_index()


def fetch_price_chunked(start: dt.date, end: dt.date, chunk_days: int = 59) -> pd.DataFrame:
    frames: list[pd.DataFrame] = []
    cursor = start
    while cursor <= end:
        chunk_end = min(cursor + dt.timedelta(days=chunk_days), end)
        frames.append(fetch_price(cursor, chunk_end))
        cursor = chunk_end + dt.timedelta(days=1)
    if not frames:
        return pd.DataFrame()
    result = pd.concat(frames).sort_index()
    return result[~result.index.duplicated(keep="last")]


def fetch_weather_forecast(
    day: dt.date,
    lat: float = 48.86,
    lon: float = 2.35,
) -> dict[str, float]:
    """Return daily weather forecast features for a French proxy location."""
    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        "&daily=temperature_2m_mean,temperature_2m_max,temperature_2m_min,"
        "wind_speed_10m_max,shortwave_radiation_sum"
        f"&timezone={TIMEZONE.replace('/', '%2F')}&forecast_days=4"
    )
    daily = _get_json(url).get("daily", {})
    frame = pd.DataFrame(daily)
    if frame.empty or "time" not in frame:
        raise RuntimeError("Open-Meteo returned no daily forecast")
    frame["time"] = pd.to_datetime(frame["time"])
    match = frame.loc[frame["time"].dt.date == day]
    if match.empty:
        raise KeyError(f"Weather forecast does not contain {day}")
    row = match.iloc[0]
    return {
        "t_mean": float(row["temperature_2m_mean"]),
        "t_max": float(row["temperature_2m_max"]),
        "t_min": float(row["temperature_2m_min"]),
        "wind_max": float(row["wind_speed_10m_max"]),
        "solar_rad": float(row["shortwave_radiation_sum"]),
    }


def fetch_weather_history(
    start: dt.date,
    end: dt.date,
    lat: float = 48.86,
    lon: float = 2.35,
) -> pd.DataFrame:
    """Return daily historical weather for model training."""
    url = (
        "https://archive-api.open-meteo.com/v1/archive"
        f"?latitude={lat}&longitude={lon}&start_date={start}&end_date={end}"
        "&daily=temperature_2m_mean,temperature_2m_max,temperature_2m_min,"
        "wind_speed_10m_max,shortwave_radiation_sum"
        f"&timezone={TIMEZONE.replace('/', '%2F')}"
    )
    daily = _get_json(url).get("daily", {})
    frame = pd.DataFrame(daily)
    if frame.empty or "time" not in frame:
        raise RuntimeError("Open-Meteo returned no historical weather")
    frame["time"] = pd.to_datetime(frame["time"])
    frame = frame.set_index(frame["time"].dt.date).drop(columns=["time"])
    frame.columns = ["t_mean", "t_max", "t_min", "wind_max", "solar_rad"]
    return frame.apply(pd.to_numeric, errors="coerce")


def calendar_weather_features(day: dt.date, weather: dict[str, float]) -> dict[str, float]:
    """Combine weather, heating/cooling and French calendar features."""
    stamp = pd.Timestamp(day)
    fr_holidays = holidays.country_holidays("FR")
    result: dict[str, float] = {
        **weather,
        "HDD": max(0.0, 15.5 - float(weather["t_mean"])),
        "CDD": max(0.0, float(weather["t_mean"]) - 22.0),
        "dow": float(stamp.dayofweek),
        "is_we": float(stamp.dayofweek >= 5),
        "month": float(stamp.month),
        "doy": float(stamp.dayofyear),
        "is_hol": float(day in fr_holidays),
    }
    missing = [name for name in WX_FEATURES if name not in result]
    if missing:
        raise KeyError(f"Missing features: {missing}")
    return result


def price_transform(values: pd.Series | np.ndarray) -> np.ndarray:
    """Signed, invertible transform that remains valid for negative prices."""
    return np.arcsinh(np.asarray(values, dtype=float) / PRICE_TRANSFORM_SCALE)


def inverse_price_transform(values: pd.Series | np.ndarray) -> np.ndarray:
    return np.sinh(np.asarray(values, dtype=float)) * PRICE_TRANSFORM_SCALE


def risk_snapshot(
    price_history: pd.Series,
    position_mwh: float,
    var_limit: float,
) -> dict[str, float | str]:
    """Calculate fixed-volume VaR from absolute daily price changes.

    Absolute EUR/MWh changes are used instead of percentage returns because
    European electricity prices can be zero or negative.
    """
    clean = pd.to_numeric(price_history, errors="coerce").dropna().sort_index()
    changes = clean.diff().dropna()
    if len(changes) < 30:
        raise RuntimeError("At least 31 daily prices are required for the risk snapshot")

    sigma30 = float(changes.tail(30).std(ddof=1))
    sigma90 = float(changes.tail(90).std(ddof=1)) if len(changes) >= 90 else float(changes.std(ddof=1))
    if not math.isfinite(sigma30) or sigma30 <= 0:
        raise RuntimeError("Invalid 30-day price-change volatility")

    regime = (
        "ELEVATED"
        if sigma30 > sigma90 * 1.15
        else "CALM"
        if sigma30 < sigma90 * 0.85
        else "NORMAL"
    )
    var95 = abs(float(position_mwh)) * sigma30 * Z_95
    var99 = abs(float(position_mwh)) * sigma30 * Z_99
    max_size = float(var_limit) / (sigma30 * Z_95)
    return {
        "spot_eur_mwh": float(clean.iloc[-1]),
        "vol30_eur_mwh": sigma30,
        "vol90_eur_mwh": sigma90,
        "var95_eur": var95,
        "var99_eur": var99,
        "max_size_mwh": max_size,
        "regime": regime,
        "price_min_eur_mwh": float(clean.tail(90).min()),
        "price_max_eur_mwh": float(clean.tail(90).max()),
        "worst_change_eur_mwh": float(changes.tail(90).min()),
    }
