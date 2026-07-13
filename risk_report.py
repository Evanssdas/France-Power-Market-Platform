"""Write the current illustrative France power risk report."""
from __future__ import annotations

import datetime as dt

import pandas as pd

from config import LOG_PATH, ROOT, load_settings, var_limit_eur
from fr_common import fetch_price_chunked, risk_snapshot

OUTPUT = ROOT / "RISK_REPORT.md"


def main() -> None:
    settings = load_settings()
    today = dt.date.today()
    end = today - dt.timedelta(days=1)
    start = end - dt.timedelta(days=105)
    prices = fetch_price_chunked(start, end)
    if prices.empty:
        raise RuntimeError("No French price history available for the risk report")

    position = float(settings["illustrative_position_mwh"])
    side = str(settings["illustrative_position_side"])
    sign = 1.0 if side == "long" else -1.0
    capital = float(settings["illustrative_capital_eur"])
    limit_pct = float(settings["var_limit_percent_of_capital"])
    limit = var_limit_eur(settings)
    snapshot = risk_snapshot(prices["price_peak"], position, limit)
    max_position_limit = float(settings["max_position_mwh"])
    permitted = min(float(snapshot["max_size_mwh"]), max_position_limit)

    latest_forecast = None
    if LOG_PATH.exists() and LOG_PATH.stat().st_size:
        log = pd.read_csv(LOG_PATH)
        okay = log[log.get("forecast_status", "").fillna("") == "ok"]
        if len(okay):
            latest_forecast = okay.sort_values("target_date").iloc[-1]

    lines = [
        "# France Daily Peak Price Risk Report",
        "",
        f"_Generated {today.isoformat()}. Energy-Charts FR day-ahead prices; daily maximum series._",
        "",
        "## What is market data and what is an assumption?",
        "",
        "| item | value | type |",
        "|---|---:|---|",
        f"| Latest observed daily peak price | €{snapshot['spot_eur_mwh']:,.2f}/MWh | market data |",
        f"| 30-day volatility of daily price changes | €{snapshot['vol30_eur_mwh']:,.2f}/MWh | calculated from market data |",
        f"| Paper position | {side} {position:,.0f} MWh | illustrative assumption |",
        f"| Paper capital | €{capital:,.0f} | illustrative assumption |",
        f"| 95% VaR appetite | {limit_pct:.1%} of paper capital = €{limit:,.0f} | illustrative assumption |",
        "",
        "The risk limit is not supplied by Energy-Charts or by the market. It is a transparent paper-trading assumption.",
        "",
        "## Market conditions",
        "",
        "| metric | value |",
        "|---|---:|",
        f"| Latest daily peak | €{snapshot['spot_eur_mwh']:,.2f}/MWh |",
        f"| 30-day standard deviation of daily price changes | €{snapshot['vol30_eur_mwh']:,.2f}/MWh |",
        f"| 90-day standard deviation of daily price changes | €{snapshot['vol90_eur_mwh']:,.2f}/MWh |",
        f"| 90-day daily-peak range | €{snapshot['price_min_eur_mwh']:,.2f} to €{snapshot['price_max_eur_mwh']:,.2f}/MWh |",
        f"| Worst observed daily change in window | €{snapshot['worst_change_eur_mwh']:,.2f}/MWh |",
        f"| Volatility regime | **{snapshot['regime']}** |",
        "",
        "## Value at Risk: one day, parametric",
        "",
        "Because electricity prices can be zero or negative, this report uses absolute daily price changes:",
        "",
        "`VaR = position MWh × standard deviation of daily EUR/MWh changes × z-score`",
        "",
        "| position | VaR 95% | VaR 99% |",
        "|---|---:|---:|",
        f"| {side} {position:,.0f} MWh | €{snapshot['var95_eur']:,.0f} | €{snapshot['var99_eur']:,.0f} |",
        "",
        f"Under the model assumptions, there is approximately a 5% probability that the one-day loss exceeds **€{snapshot['var95_eur']:,.0f}**.",
        "",
        "## Absolute price-shock stress tests",
        "",
        "These scenarios have no assigned probability; they show the financial consequence of a chosen price move.",
        "",
        "| price change | paper P&L |",
        "|---:|---:|",
    ]
    for shock in settings["stress_price_shocks_eur_mwh"]:
        pnl = sign * position * float(shock)
        lines.append(f"| {float(shock):+,.0f} EUR/MWh | €{pnl:+,.0f} |")

    lines += [
        "",
        "## Exposure versus illustrative limits",
        "",
        "| limit | set | current | status |",
        "|---|---:|---:|---|",
        f"| Maximum single position | {max_position_limit:,.0f} MWh | {position:,.0f} MWh | {'OK' if position <= max_position_limit else '**BREACH**'} |",
        f"| Maximum portfolio 95% VaR | €{limit:,.0f} | €{snapshot['var95_eur']:,.0f} | {'OK' if snapshot['var95_eur'] <= limit else '**BREACH**'} |",
        "",
        "## Position sizing",
        "",
        f"The VaR formula permits **{snapshot['max_size_mwh']:,.0f} MWh**; the separate volume limit permits **{max_position_limit:,.0f} MWh**.",
        "",
        f"The binding maximum is therefore **{permitted:,.0f} MWh**.",
        "",
    ]

    if latest_forecast is not None:
        lines += [
            "## Latest model forecast",
            "",
            f"- Target date: **{latest_forecast.get('target_date', '')}**",
            f"- Forecast demand: **{pd.to_numeric(latest_forecast.get('pred_demand_gw'), errors='coerce'):.2f} GW**",
            f"- Forecast nuclear generation: **{pd.to_numeric(latest_forecast.get('pred_nuclear_gw'), errors='coerce'):.2f} GW**",
            f"- Forecast residual demand: **{pd.to_numeric(latest_forecast.get('pred_residual_gw'), errors='coerce'):.2f} GW**",
            f"- Forecast daily peak price: **€{pd.to_numeric(latest_forecast.get('pred_price_peak_eur_mwh'), errors='coerce'):.2f}/MWh**",
            "",
        ]

    lines += [
        "## Limitations",
        "",
        "- Parametric VaR assumes price changes are approximately normally distributed; power markets have spikes and fat tails.",
        "- VaR is a loss threshold, not the maximum possible loss.",
        "- Volatility is backward-looking and does not know tomorrow's outage or system event.",
        "- The price target is the daily maximum day-ahead price, not a baseload or peakload contract settlement.",
        "- The paper capital, position and limits are illustrative and must not be described as real company limits.",
        "- With one position there is no diversification model; a multi-asset portfolio would require covariance or scenario aggregation.",
    ]
    OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUTPUT.name}")


if __name__ == "__main__":
    main()
