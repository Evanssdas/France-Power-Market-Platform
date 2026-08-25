# France Power Forecast Scorecard

_Only forecasts marked **pre_auction** and later fully graded are included._

- Logged rows: **42**
- Official pre-auction rows: **18**
- Fully graded official rows: **16**

> **Sample warning:** fewer than 30 graded forecasts are available. The figures below are operational checks, not strong evidence of model skill.

## Model versus persistence

The persistence baseline uses the latest completed daily observation available at the 10:30 D-1 issue time (D-2).

| target | n | model MAE | baseline MAE | improvement | RMSE | bias | model wins |
|---|---:|---:|---:|---:|---:|---:|---:|
| demand (GW) | 16 | 1.24 | 3.23 | +61.8% | 1.60 | +1.12 | 81.2% |
| nuclear (GW) | 16 | 2.65 | 1.83 | -45.1% | 2.98 | +2.27 | 43.8% |
| wind (GW) | 16 | 1.58 | 1.99 | +20.5% | 1.96 | -0.06 | 62.5% |
| solar (GW) | 16 | 0.63 | 1.07 | +41.2% | 0.82 | -0.23 | 68.8% |
| hydro (GW) | 16 | 0.48 | 0.33 | -44.5% | 0.54 | +0.48 | 31.2% |
| residual (GW) | 16 | 2.75 | 2.58 | -6.6% | 3.21 | -1.33 | 50.0% |
| peak price (EUR/MWh) | 16 | 72.16 | 61.51 | -17.3% | 96.56 | -72.16 | 31.2% |

## Price direction

Directional accuracy versus the D-2 reference price: **62.5%** across **16** graded forecasts.

## Illustrative VaR backtest

- Observations with a usable risk record: **16**
- 95% VaR breaches: **2**
- Observed breach rate: **12.5%** (the model benchmark is approximately 5% over a large sample)

## Reading the table

- **Positive improvement:** the model beat persistence.
- **Negative improvement:** persistence was better; this must not be hidden.
- **Bias above zero:** the model tends to predict too high.
- **Bias below zero:** the model tends to predict too low.
- **Model wins:** percentage of individual days when the model absolute error was smaller.