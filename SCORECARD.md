# France Power Forecast Scorecard

_Only forecasts marked **pre_auction** and later fully graded are included._

- Logged rows: **28**
- Official pre-auction rows: **4**
- Fully graded official rows: **2**

> **Sample warning:** fewer than 30 graded forecasts are available. The figures below are operational checks, not strong evidence of model skill.

## Model versus persistence

The persistence baseline uses the latest completed daily observation available at the 10:30 D-1 issue time (D-2).

| target | n | model MAE | baseline MAE | improvement | RMSE | bias | model wins |
|---|---:|---:|---:|---:|---:|---:|---:|
| demand (GW) | 2 | 1.18 | 3.68 | +67.8% | 1.24 | +0.36 | 100.0% |
| nuclear (GW) | 2 | 1.99 | 3.85 | +48.1% | 2.00 | +1.99 | 100.0% |
| wind (GW) | 2 | 1.29 | 0.92 | -40.4% | 1.43 | +0.61 | 50.0% |
| solar (GW) | 2 | 0.29 | 1.82 | +84.1% | 0.39 | +0.26 | 100.0% |
| hydro (GW) | 2 | 0.47 | 0.24 | -95.0% | 0.49 | +0.47 | 0.0% |
| residual (GW) | 2 | 2.97 | 3.15 | +5.7% | 2.98 | -2.97 | 50.0% |
| peak price (EUR/MWh) | 2 | 43.52 | 1.46 | -2870.6% | 47.45 | -43.52 | 0.0% |

## Price direction

Directional accuracy versus the D-2 reference price: **0.0%** across **2** graded forecasts.

## Illustrative VaR backtest

- Observations with a usable risk record: **2**
- 95% VaR breaches: **0**
- Observed breach rate: **0.0%** (the model benchmark is approximately 5% over a large sample)

## Reading the table

- **Positive improvement:** the model beat persistence.
- **Negative improvement:** persistence was better; this must not be hidden.
- **Bias above zero:** the model tends to predict too high.
- **Bias below zero:** the model tends to predict too low.
- **Model wins:** percentage of individual days when the model absolute error was smaller.