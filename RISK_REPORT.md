# France Daily Peak Price Risk Report

_Generated 2026-09-03. Energy-Charts FR day-ahead prices; daily maximum series._

## What is market data and what is an assumption?

| item | value | type |
|---|---:|---|
| Latest observed daily peak price | €247.27/MWh | market data |
| 30-day volatility of daily price changes | €65.30/MWh | calculated from market data |
| Paper position | long 100 MWh | illustrative assumption |
| Paper capital | €500,000 | illustrative assumption |
| 95% VaR appetite | 2.0% of paper capital = €10,000 | illustrative assumption |

The risk limit is not supplied by Energy-Charts or by the market. It is a transparent paper-trading assumption.

## Market conditions

| metric | value |
|---|---:|
| Latest daily peak | €247.27/MWh |
| 30-day standard deviation of daily price changes | €65.30/MWh |
| 90-day standard deviation of daily price changes | €52.70/MWh |
| 90-day daily-peak range | €62.44 to €487.38/MWh |
| Worst observed daily change in window | €-207.30/MWh |
| Volatility regime | **ELEVATED** |

## Value at Risk: one day, parametric

Because electricity prices can be zero or negative, this report uses absolute daily price changes:

`VaR = position MWh × standard deviation of daily EUR/MWh changes × z-score`

| position | VaR 95% | VaR 99% |
|---|---:|---:|
| long 100 MWh | €10,741 | €15,190 |

Under the model assumptions, there is approximately a 5% probability that the one-day loss exceeds **€10,741**.

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
| Maximum portfolio 95% VaR | €10,000 | €10,741 | **BREACH** |

## Position sizing

The VaR formula permits **93 MWh**; the separate volume limit permits **2,000 MWh**.

The binding maximum is therefore **93 MWh**.

## Latest model forecast

- Target date: **2026-09-04**
- Forecast demand: **45.45 GW**
- Forecast nuclear generation: **37.52 GW**
- Forecast residual demand: **-6.06 GW**
- Forecast daily peak price: **€137.93/MWh**

## Limitations

- Parametric VaR assumes price changes are approximately normally distributed; power markets have spikes and fat tails.
- VaR is a loss threshold, not the maximum possible loss.
- Volatility is backward-looking and does not know tomorrow's outage or system event.
- The price target is the daily maximum day-ahead price, not a baseload or peakload contract settlement.
- The paper capital, position and limits are illustrative and must not be described as real company limits.
- With one position there is no diversification model; a multi-asset portfolio would require covariance or scenario aggregation.