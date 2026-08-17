# France Power Forecast Scorecard

_Only forecasts marked **pre_auction** and later fully graded are included._

- Logged rows: **34**
- Official pre-auction rows: **10**
- Fully graded official rows: **8**

> **Sample warning:** fewer than 30 graded forecasts are available. The figures below are operational checks, not strong evidence of model skill.

## Model versus persistence

The persistence baseline uses the latest completed daily observation available at the 10:30 D-1 issue time (D-2).

| target | n | model MAE | baseline MAE | improvement | RMSE | bias | model wins |
|---|---:|---:|---:|---:|---:|---:|---:|
| demand (GW) | 8 | 1.27 | 3.51 | +63.9% | 1.84 | +1.03 | 87.5% |
| nuclear (GW) | 8 | 3.10 | 1.69 | -82.7% | 3.19 | +3.10 | 25.0% |
| wind (GW) | 8 | 0.95 | 1.13 | +15.9% | 1.09 | +0.43 | 62.5% |
| solar (GW) | 8 | 0.31 | 1.18 | +74.1% | 0.36 | -0.17 | 87.5% |
| hydro (GW) | 8 | 0.49 | 0.28 | -78.2% | 0.53 | +0.49 | 25.0% |
| residual (GW) | 8 | 3.04 | 2.22 | -36.9% | 3.37 | -2.82 | 37.5% |
| peak price (EUR/MWh) | 8 | 77.38 | 108.66 | +28.8% | 118.16 | -77.38 | 62.5% |

## Price direction

Directional accuracy versus the D-2 reference price: **62.5%** across **8** graded forecasts.

## Illustrative VaR backtest

- Observations with a usable risk record: **8**
- 95% VaR breaches: **2**
- Observed breach rate: **25.0%** (the model benchmark is approximately 5% over a large sample)

## Reading the table

- **Positive improvement:** the model beat persistence.
- **Negative improvement:** persistence was better; this must not be hidden.
- **Bias above zero:** the model tends to predict too high.
- **Bias below zero:** the model tends to predict too low.
- **Model wins:** percentage of individual days when the model absolute error was smaller.