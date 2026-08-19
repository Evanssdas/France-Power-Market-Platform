# France Power Forecast Scorecard

_Only forecasts marked **pre_auction** and later fully graded are included._

- Logged rows: **36**
- Official pre-auction rows: **12**
- Fully graded official rows: **10**

> **Sample warning:** fewer than 30 graded forecasts are available. The figures below are operational checks, not strong evidence of model skill.

## Model versus persistence

The persistence baseline uses the latest completed daily observation available at the 10:30 D-1 issue time (D-2).

| target | n | model MAE | baseline MAE | improvement | RMSE | bias | model wins |
|---|---:|---:|---:|---:|---:|---:|---:|
| demand (GW) | 10 | 1.24 | 3.34 | +62.8% | 1.74 | +1.06 | 80.0% |
| nuclear (GW) | 10 | 3.41 | 1.66 | -105.4% | 3.57 | +3.41 | 20.0% |
| wind (GW) | 10 | 0.97 | 1.28 | +23.9% | 1.11 | +0.46 | 60.0% |
| solar (GW) | 10 | 0.43 | 1.08 | +60.2% | 0.55 | -0.21 | 80.0% |
| hydro (GW) | 10 | 0.43 | 0.30 | -45.2% | 0.48 | +0.43 | 30.0% |
| residual (GW) | 10 | 3.21 | 2.13 | -50.5% | 3.63 | -3.03 | 40.0% |
| peak price (EUR/MWh) | 10 | 74.28 | 89.56 | +17.1% | 109.25 | -74.28 | 50.0% |

## Price direction

Directional accuracy versus the D-2 reference price: **60.0%** across **10** graded forecasts.

## Illustrative VaR backtest

- Observations with a usable risk record: **10**
- 95% VaR breaches: **2**
- Observed breach rate: **20.0%** (the model benchmark is approximately 5% over a large sample)

## Reading the table

- **Positive improvement:** the model beat persistence.
- **Negative improvement:** persistence was better; this must not be hidden.
- **Bias above zero:** the model tends to predict too high.
- **Bias below zero:** the model tends to predict too low.
- **Model wins:** percentage of individual days when the model absolute error was smaller.