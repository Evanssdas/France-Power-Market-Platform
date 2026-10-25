# France Daily Peak Price Risk Report

_Generated 2026-10-25. Energy-Charts FR day-ahead prices; daily maximum series._

## What is market data and what is an assumption?

| item | value | type |
|---|---:|---|
| Latest observed daily peak price | €124.16/MWh | market data |
| 30-day volatility of daily price changes | €66.84/MWh | calculated from market data |
| Paper position | long 100 MWh | illustrative assumption |
| Paper capital | €500,000 | illustrative assumption |
| 95% VaR appetite | 2.0% of paper capital = €10,000 | illustrative assumption |

The risk limit is not supplied by Energy-Charts or by the market. It is a transparent paper-trading assumption.

## Market conditions

| metric | value |
|---|---:|
| Latest daily peak | €124.16/MWh |
| 30-day standard deviation of daily price changes | €66.84/MWh |
| 90-day standard deviation of daily price changes | €58.20/MWh |
| 90-day daily-peak range | €124.16 to €487.38/MWh |
| Worst observed daily change in window | €-207.30/MWh |
| Volatility regime | **NORMAL** |

## Value at Risk: one day, parametric

Because electricity prices can be zero or negative, this report uses absolute daily price changes:

`VaR = position MWh × standard deviation of daily EUR/MWh changes × z-score`

| position | VaR 95% | VaR 99% |
|---|---:|---:|
| long 100 MWh | €10,994 | €15,549 |

Under the model assumptions, there is approximately a 5% probability that the one-day loss exceeds **€10,994**.

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
| Maximum portfolio 95% VaR | €10,000 | €10,994 | **BREACH** |

## Position sizing

The VaR formula permits **91 MWh**; the separate volume limit permits **2,000 MWh**.

The binding maximum is therefore **91 MWh**.

## Latest model forecast

- Target date: **2026-10-26**
- Forecast demand: **49.17 GW**
- Forecast nuclear generation: **41.68 GW**
- Forecast residual demand: **-5.52 GW**
- Forecast daily peak price: **€140.18/MWh**

## Limitations

- Parametric VaR assumes price changes are approximately normally distributed; power markets have spikes and fat tails.
- VaR is a loss threshold, not the maximum possible loss.
- Volatility is backward-looking and does not know tomorrow's outage or system event.
- The price target is the daily maximum day-ahead price, not a baseload or peakload contract settlement.
- The paper capital, position and limits are illustrative and must not be described as real company limits.
- With one position there is no diversification model; a multi-asset portfolio would require covariance or scenario aggregation.