# France Power Forecast Scorecard

_Only forecasts marked **pre_auction** and later fully graded are included._

- Logged rows: **35**
- Official pre-auction rows: **11**
- Fully graded official rows: **9**

> **Sample warning:** fewer than 30 graded forecasts are available. The figures below are operational checks, not strong evidence of model skill.

## Model versus persistence

The persistence baseline uses the latest completed daily observation available at the 10:30 D-1 issue time (D-2).

| target | n | model MAE | baseline MAE | improvement | RMSE | bias | model wins |
|---|---:|---:|---:|---:|---:|---:|---:|
| demand (GW) | 9 | 1.31 | 3.26 | +59.8% | 1.82 | +1.10 | 77.8% |
| nuclear (GW) | 9 | 3.39 | 1.57 | -115.9% | 3.56 | +3.39 | 22.2% |
| wind (GW) | 9 | 1.03 | 1.01 | -1.2% | 1.16 | +0.57 | 55.6% |
| solar (GW) | 9 | 0.34 | 1.14 | +70.4% | 0.39 | -0.09 | 88.9% |
| hydro (GW) | 9 | 0.44 | 0.32 | -39.7% | 0.50 | +0.43 | 33.3% |
| residual (GW) | 9 | 3.39 | 2.06 | -64.7% | 3.79 | -3.19 | 33.3% |
| peak price (EUR/MWh) | 9 | 75.37 | 98.83 | +23.7% | 113.14 | -75.37 | 55.6% |

## Price direction

Directional accuracy versus the D-2 reference price: **55.6%** across **9** graded forecasts.

## Illustrative VaR backtest

- Observations with a usable risk record: **9**
- 95% VaR breaches: **2**
- Observed breach rate: **22.2%** (the model benchmark is approximately 5% over a large sample)

## Reading the table

- **Positive improvement:** the model beat persistence.
- **Negative improvement:** persistence was better; this must not be hidden.
- **Bias above zero:** the model tends to predict too high.
- **Bias below zero:** the model tends to predict too low.
- **Model wins:** percentage of individual days when the model absolute error was smaller.