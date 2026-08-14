# France Power Forecast Scorecard

_Only forecasts marked **pre_auction** and later fully graded are included._

- Logged rows: **31**
- Official pre-auction rows: **7**
- Fully graded official rows: **5**

> **Sample warning:** fewer than 30 graded forecasts are available. The figures below are operational checks, not strong evidence of model skill.

## Model versus persistence

The persistence baseline uses the latest completed daily observation available at the 10:30 D-1 issue time (D-2).

| target | n | model MAE | baseline MAE | improvement | RMSE | bias | model wins |
|---|---:|---:|---:|---:|---:|---:|---:|
| demand (GW) | 5 | 1.93 | 3.33 | +41.9% | 2.32 | +1.60 | 80.0% |
| nuclear (GW) | 5 | 2.83 | 1.81 | -56.4% | 2.96 | +2.83 | 40.0% |
| wind (GW) | 5 | 0.89 | 1.30 | +31.3% | 1.11 | +0.07 | 80.0% |
| solar (GW) | 5 | 0.32 | 1.25 | +74.3% | 0.37 | -0.10 | 80.0% |
| hydro (GW) | 5 | 0.57 | 0.22 | -164.8% | 0.60 | +0.57 | 0.0% |
| residual (GW) | 5 | 2.12 | 2.16 | +2.1% | 2.35 | -1.77 | 60.0% |
| peak price (EUR/MWh) | 5 | 86.14 | 66.97 | -28.6% | 139.60 | -86.14 | 40.0% |

## Price direction

Directional accuracy versus the D-2 reference price: **40.0%** across **5** graded forecasts.

## Illustrative VaR backtest

- Observations with a usable risk record: **5**
- 95% VaR breaches: **0**
- Observed breach rate: **0.0%** (the model benchmark is approximately 5% over a large sample)

## Reading the table

- **Positive improvement:** the model beat persistence.
- **Negative improvement:** persistence was better; this must not be hidden.
- **Bias above zero:** the model tends to predict too high.
- **Bias below zero:** the model tends to predict too low.
- **Model wins:** percentage of individual days when the model absolute error was smaller.