# France Power Forecast Scorecard

_Only forecasts marked **pre_auction** and later fully graded are included._

- Logged rows: **32**
- Official pre-auction rows: **8**
- Fully graded official rows: **6**

> **Sample warning:** fewer than 30 graded forecasts are available. The figures below are operational checks, not strong evidence of model skill.

## Model versus persistence

The persistence baseline uses the latest completed daily observation available at the 10:30 D-1 issue time (D-2).

| target | n | model MAE | baseline MAE | improvement | RMSE | bias | model wins |
|---|---:|---:|---:|---:|---:|---:|---:|
| demand (GW) | 6 | 1.63 | 3.03 | +46.3% | 2.12 | +1.32 | 83.3% |
| nuclear (GW) | 6 | 2.97 | 1.56 | -90.6% | 3.09 | +2.97 | 33.3% |
| wind (GW) | 6 | 0.95 | 1.38 | +31.1% | 1.13 | +0.26 | 83.3% |
| solar (GW) | 6 | 0.27 | 1.13 | +76.1% | 0.34 | -0.09 | 83.3% |
| hydro (GW) | 6 | 0.52 | 0.26 | -99.8% | 0.56 | +0.52 | 16.7% |
| residual (GW) | 6 | 2.64 | 2.42 | -9.2% | 3.04 | -2.35 | 50.0% |
| peak price (EUR/MWh) | 6 | 88.34 | 85.99 | -2.7% | 133.73 | -88.34 | 50.0% |

## Price direction

Directional accuracy versus the D-2 reference price: **50.0%** across **6** graded forecasts.

## Illustrative VaR backtest

- Observations with a usable risk record: **6**
- 95% VaR breaches: **1**
- Observed breach rate: **16.7%** (the model benchmark is approximately 5% over a large sample)

## Reading the table

- **Positive improvement:** the model beat persistence.
- **Negative improvement:** persistence was better; this must not be hidden.
- **Bias above zero:** the model tends to predict too high.
- **Bias below zero:** the model tends to predict too low.
- **Model wins:** percentage of individual days when the model absolute error was smaller.