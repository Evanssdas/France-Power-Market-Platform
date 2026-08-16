# France Power Forecast Scorecard

_Only forecasts marked **pre_auction** and later fully graded are included._

- Logged rows: **33**
- Official pre-auction rows: **9**
- Fully graded official rows: **7**

> **Sample warning:** fewer than 30 graded forecasts are available. The figures below are operational checks, not strong evidence of model skill.

## Model versus persistence

The persistence baseline uses the latest completed daily observation available at the 10:30 D-1 issue time (D-2).

| target | n | model MAE | baseline MAE | improvement | RMSE | bias | model wins |
|---|---:|---:|---:|---:|---:|---:|---:|
| demand (GW) | 7 | 1.44 | 3.14 | +54.1% | 1.97 | +1.18 | 85.7% |
| nuclear (GW) | 7 | 3.09 | 1.71 | -80.4% | 3.20 | +3.09 | 28.6% |
| wind (GW) | 7 | 0.95 | 1.26 | +24.9% | 1.11 | +0.36 | 71.4% |
| solar (GW) | 7 | 0.30 | 1.19 | +74.7% | 0.36 | -0.14 | 85.7% |
| hydro (GW) | 7 | 0.52 | 0.27 | -95.7% | 0.55 | +0.52 | 14.3% |
| residual (GW) | 7 | 2.90 | 2.09 | -39.2% | 3.28 | -2.65 | 42.9% |
| peak price (EUR/MWh) | 7 | 79.96 | 114.89 | +30.4% | 124.32 | -79.96 | 57.1% |

## Price direction

Directional accuracy versus the D-2 reference price: **57.1%** across **7** graded forecasts.

## Illustrative VaR backtest

- Observations with a usable risk record: **7**
- 95% VaR breaches: **2**
- Observed breach rate: **28.6%** (the model benchmark is approximately 5% over a large sample)

## Reading the table

- **Positive improvement:** the model beat persistence.
- **Negative improvement:** persistence was better; this must not be hidden.
- **Bias above zero:** the model tends to predict too high.
- **Bias below zero:** the model tends to predict too low.
- **Model wins:** percentage of individual days when the model absolute error was smaller.