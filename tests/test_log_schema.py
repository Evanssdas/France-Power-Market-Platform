from log_schema import LOG_COLUMNS


def test_log_columns_are_unique():
    assert len(LOG_COLUMNS) == len(set(LOG_COLUMNS))


def test_log_contains_core_outputs():
    required = {
        "target_date",
        "pred_demand_gw",
        "actual_demand_gw",
        "pred_nuclear_gw",
        "pred_residual_gw",
        "pred_price_peak_eur_mwh",
        "var95_eur",
        "forecast_status",
        "grade_status",
    }
    assert required.issubset(LOG_COLUMNS)
