# France Daily Peak Price Risk Report

_Generated 2026-10-06. Energy-Charts FR day-ahead prices; daily maximum series._

## What is market data and what is an assumption?

| item | value | type |
|---|---:|---|
| Latest observed daily peak price | €271.93/MWh | market data |
| 30-day volatility of daily price changes | €59.31/MWh | calculated from market data |
| Paper position | long 100 MWh | illustrative assumption |
| Paper capital | €500,000 | illustrative assumption |
| 95% VaR appetite | 2.0% of paper capital = €10,000 | illustrative assumption |

The risk limit is not supplied by Energy-Charts or by the market. It is a transparent paper-trading assumption.

## Market conditions

| metric | value |
|---|---:|
| Latest daily peak | €271.93/MWh |
| 30-day standard deviation of daily price changes | €59.31/MWh |
| 90-day standard deviation of daily price changes | €53.30/MWh |
| 90-day daily-peak range | €147.98 to €487.38/MWh |
| Worst observed daily change in window | €-207.30/MWh |
| Volatility regime | **NORMAL** |

## Value at Risk: one day, parametric

Because electricity prices can be zero or negative, this report uses absolute daily price changes:

`VaR = position MWh × standard deviation of daily EUR/MWh changes × z-score`

| position | VaR 95% | VaR 99% |
|---|---:|---:|
| long 100 MWh | €9,756 | €13,798 |

Under the model assumptions, there is approximately a 5% probability that the one-day loss exceeds **€9,756**.

## Absolute price-shock stress tests

These scenarios have no assigned probability; they show the financial consequence of a chosen price move.

| price change | paper P&L |
|---:|---:|
| -100 EUR/MWh | €-10,000 |
| -50 EUR/MWh | €-5,000 |
| -25 EUR/MWh | €-2,500 |
| +25 EUR/MWh | €+2,500 |
| +50 EUR/MWh | €+5,000 |
| +100 EUR/MWh | €+10,000 |

## Exposure versus illustrative limits

| limit | set | current | status |
|---|---:|---:|---|
| Maximum single position | 2,000 MWh | 100 MWh | OK |
| Maximum portfolio 95% VaR | €10,000 | €9,756 | OK |

## Position sizing

The VaR formula permits **103 MWh**; the separate volume limit permits **2,000 MWh**.

The binding maximum is therefore **103 MWh**.

## Latest model forecast

- Target date: **2026-10-07**
- Forecast demand: **44.47 GW**
- Forecast nuclear generation: **40.37 GW**
- Forecast residual demand: **-10.33 GW**
- Forecast daily peak price: **€116.60/MWh**

## Limitations

- Parametric VaR assumes price changes are approximately normally distributed; power markets have spikes and fat tails.
- VaR is a loss threshold, not the maximum possible loss.
- Volatility is backward-looking and does not know tomorrow's outage or system event.
- The price target is the daily maximum day-ahead price, not a baseload or peakload contract settlement.
- The paper capital, position and limits are illustrative and must not be described as real company limits.
- With one position there is no diversification model; a multi-asset portfolio would require covariance or scenario aggregation.