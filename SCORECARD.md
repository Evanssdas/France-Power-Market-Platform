# France Power Forecast Scorecard

_Only forecasts marked **pre_auction** and later fully graded are included._

- Logged rows: **38**
- Official pre-auction rows: **14**
- Fully graded official rows: **12**

> **Sample warning:** fewer than 30 graded forecasts are available. The figures below are operational checks, not strong evidence of model skill.

## Model versus persistence

The persistence baseline uses the latest completed daily observation available at the 10:30 D-1 issue time (D-2).

| target | n | model MAE | baseline MAE | improvement | RMSE | bias | model wins |
|---|---:|---:|---:|---:|---:|---:|---:|
| demand (GW) | 12 | 1.20 | 2.90 | +58.6% | 1.65 | +1.05 | 75.0% |
| nuclear (GW) | 12 | 3.19 | 1.87 | -70.8% | 3.39 | +3.19 | 33.3% |
| wind (GW) | 12 | 1.20 | 1.36 | +11.7% | 1.40 | -0.00 | 58.3% |
| solar (GW) | 12 | 0.63 | 1.14 | +45.0% | 0.84 | -0.24 | 75.0% |
| hydro (GW) | 12 | 0.46 | 0.31 | -47.1% | 0.51 | +0.46 | 25.0% |
| residual (GW) | 12 | 2.85 | 2.39 | -18.9% | 3.35 | -2.35 | 50.0% |
| peak price (EUR/MWh) | 12 | 71.35 | 75.41 | +5.4% | 102.45 | -71.35 | 41.7% |

## Price direction

Directional accuracy versus the D-2 reference price: **58.3%** across **12** graded forecasts.

## Illustrative VaR backtest

- Observations with a usable risk record: **12**
- 95% VaR breaches: **2**
- Observed breach rate: **16.7%** (the model benchmark is approximately 5% over a large sample)

## Reading the table

- **Positive improvement:** the model beat persistence.
- **Negative improvement:** persistence was better; this must not be hidden.
- **Bias above zero:** the model tends to predict too high.
- **Bias below zero:** the model tends to predict too low.
- **Model wins:** percentage of individual days when the model absolute error was smaller.