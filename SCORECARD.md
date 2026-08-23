# France Power Forecast Scorecard

_Only forecasts marked **pre_auction** and later fully graded are included._

- Logged rows: **40**
- Official pre-auction rows: **16**
- Fully graded official rows: **14**

> **Sample warning:** fewer than 30 graded forecasts are available. The figures below are operational checks, not strong evidence of model skill.

## Model versus persistence

The persistence baseline uses the latest completed daily observation available at the 10:30 D-1 issue time (D-2).

| target | n | model MAE | baseline MAE | improvement | RMSE | bias | model wins |
|---|---:|---:|---:|---:|---:|---:|---:|
| demand (GW) | 14 | 1.21 | 3.08 | +60.8% | 1.62 | +1.07 | 78.6% |
| nuclear (GW) | 14 | 2.90 | 1.79 | -62.1% | 3.17 | +2.57 | 35.7% |
| wind (GW) | 14 | 1.38 | 1.63 | +15.3% | 1.66 | +0.35 | 57.1% |
| solar (GW) | 14 | 0.67 | 1.18 | +42.6% | 0.87 | -0.26 | 71.4% |
| hydro (GW) | 14 | 0.44 | 0.29 | -48.4% | 0.48 | +0.43 | 28.6% |
| residual (GW) | 14 | 2.64 | 2.36 | -11.8% | 3.15 | -2.02 | 50.0% |
| peak price (EUR/MWh) | 14 | 73.74 | 66.35 | -11.1% | 100.60 | -73.74 | 35.7% |

## Price direction

Directional accuracy versus the D-2 reference price: **64.3%** across **14** graded forecasts.

## Illustrative VaR backtest

- Observations with a usable risk record: **14**
- 95% VaR breaches: **2**
- Observed breach rate: **14.3%** (the model benchmark is approximately 5% over a large sample)

## Reading the table

- **Positive improvement:** the model beat persistence.
- **Negative improvement:** persistence was better; this must not be hidden.
- **Bias above zero:** the model tends to predict too high.
- **Bias below zero:** the model tends to predict too low.
- **Model wins:** percentage of individual days when the model absolute error was smaller.