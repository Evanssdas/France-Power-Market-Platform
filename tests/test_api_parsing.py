import datetime as dt

import numpy as np

import fr_common


def test_generation_payload_is_aggregated_and_converted_to_gw(monkeypatch):
    # Four 15-minute-style observations across two UTC/Paris dates.
    payload = {
        "unix_seconds": [
            1767225600, 1767226500,  # 2026-01-01
            1767312000, 1767312900,  # 2026-01-02
        ],
        "production_types": [
            {"name": "Load", "data": [40000, 42000, 44000, 46000]},
            {"name": "Nuclear", "data": [30000, 30000, 31000, 31000]},
            {"name": "Wind onshore", "data": [3000, 5000, 4000, 6000]},
            {"name": "Wind offshore", "data": [1000, 1000, 1000, 1000]},
            {"name": "Solar", "data": [0, 2000, 0, 3000]},
            {"name": "Hydro Run-of-River", "data": [2000, 2000, 2500, 2500]},
            {"name": "Hydro water reservoir", "data": [1000, 1000, 1500, 1500]},
        ],
    }
    monkeypatch.setattr(fr_common, "_get_json", lambda _: payload)
    result = fr_common.fetch_generation(dt.date(2026, 1, 1), dt.date(2026, 1, 2))

    assert len(result) == 2
    first = result.iloc[0]
    assert np.isclose(first["load"], 41.0)
    assert np.isclose(first["nuclear"], 30.0)
    assert np.isclose(first["wind"], 5.0)
    assert np.isclose(first["solar"], 1.0)
    assert np.isclose(first["hydro"], 3.0)
    assert np.isclose(first["residual"], 2.0)


def test_price_payload_produces_daily_mean_and_peak(monkeypatch):
    payload = {
        "unix_seconds": [1767225600, 1767226500, 1767312000, 1767312900],
        "price": [20.0, 80.0, -10.0, 30.0],
    }
    monkeypatch.setattr(fr_common, "_get_json", lambda _: payload)
    result = fr_common.fetch_price(dt.date(2026, 1, 1), dt.date(2026, 1, 2))

    assert len(result) == 2
    assert np.isclose(result.iloc[0]["price_mean"], 50.0)
    assert np.isclose(result.iloc[0]["price_peak"], 80.0)
    assert np.isclose(result.iloc[1]["price_mean"], 10.0)
    assert np.isclose(result.iloc[1]["price_peak"], 30.0)
