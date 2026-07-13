import numpy as np
import pandas as pd

from fr_common import inverse_price_transform, price_transform, risk_snapshot


def test_price_transform_round_trip_handles_negative_prices():
    values = np.array([-100.0, -5.0, 0.0, 25.0, 300.0])
    restored = inverse_price_transform(price_transform(values))
    assert np.allclose(values, restored)


def test_risk_snapshot_uses_absolute_price_changes():
    prices = pd.Series([50.0 + i + (5.0 if i % 3 == 0 else 0.0) for i in range(100)])
    snapshot = risk_snapshot(prices, position_mwh=100.0, var_limit=10_000.0)
    assert snapshot["vol30_eur_mwh"] > 0
    assert snapshot["var95_eur"] > 0
    assert snapshot["var99_eur"] > snapshot["var95_eur"]
    assert snapshot["max_size_mwh"] > 0
