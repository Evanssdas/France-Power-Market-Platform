# France Power Forecast Scorecard

_Only forecasts marked **pre_auction** and later fully graded are included._

- Logged rows: **27**
- Official pre-auction rows: **3**
- Fully graded official rows: **1**

> **Sample warning:** fewer than 30 graded forecasts are available. The figures below are operational checks, not strong evidence of model skill.

## Model versus persistence

The persistence baseline uses the latest completed daily observation available at the 10:30 D-1 issue time (D-2).

| target | n | model MAE | baseline MAE | improvement | RMSE | bias | model wins |
|---|---:|---:|---:|---:|---:|---:|---:|
| demand (GW) | 1 | 0.82 | 3.64 | +77.4% | 0.82 | -0.82 | 100.0% |
| nuclear (GW) | 1 | 2.19 | 2.70 | +18.7% | 2.19 | +2.19 | 100.0% |
| wind (GW) | 1 | 0.69 | 0.96 | +28.6% | 0.69 | -0.69 | 100.0% |
| solar (GW) | 1 | 0.55 | 1.28 | +57.1% | 0.55 | +0.55 | 100.0% |
| hydro (GW) | 1 | 0.35 | 0.11 | -215.5% | 0.35 | +0.35 | 0.0% |
| residual (GW) | 1 | 3.23 | 1.40 | -130.2% | 3.23 | -3.23 | 0.0% |
| peak price (EUR/MWh) | 1 | 62.43 | 2.25 | -2674.6% | 62.43 | -62.43 | 0.0% |

## Price direction

Directional accuracy versus the D-2 reference price: **0.0%** across **1** graded forecasts.

## Illustrative VaR backtest

- Observations with a usable risk record: **1**
- 95% VaR breaches: **0**
- Observed breach rate: **0.0%** (the model benchmark is approximately 5% over a large sample)

## Reading the table

- **Positive improvement:** the model beat persistence.
- **Negative improvement:** persistence was better; this must not be hidden.
- **Bias above zero:** the model tends to predict too high.
- **Bias below zero:** the model tends to predict too low.
- **Model wins:** percentage of individual days when the model absolute error was smaller.