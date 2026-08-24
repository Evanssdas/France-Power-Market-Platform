# France Power Forecast Scorecard

_Only forecasts marked **pre_auction** and later fully graded are included._

- Logged rows: **41**
- Official pre-auction rows: **17**
- Fully graded official rows: **15**

> **Sample warning:** fewer than 30 graded forecasts are available. The figures below are operational checks, not strong evidence of model skill.

## Model versus persistence

The persistence baseline uses the latest completed daily observation available at the 10:30 D-1 issue time (D-2).

| target | n | model MAE | baseline MAE | improvement | RMSE | bias | model wins |
|---|---:|---:|---:|---:|---:|---:|---:|
| demand (GW) | 15 | 1.20 | 3.22 | +62.8% | 1.59 | +1.07 | 80.0% |
| nuclear (GW) | 15 | 2.76 | 1.84 | -50.1% | 3.07 | +2.35 | 40.0% |
| wind (GW) | 15 | 1.38 | 1.68 | +18.0% | 1.64 | +0.24 | 60.0% |
| solar (GW) | 15 | 0.65 | 1.12 | +41.8% | 0.85 | -0.22 | 66.7% |
| hydro (GW) | 15 | 0.44 | 0.32 | -38.9% | 0.48 | +0.43 | 33.3% |
| residual (GW) | 15 | 2.63 | 2.49 | -5.7% | 3.11 | -1.72 | 53.3% |
| peak price (EUR/MWh) | 15 | 72.58 | 64.92 | -11.8% | 98.27 | -72.58 | 33.3% |

## Price direction

Directional accuracy versus the D-2 reference price: **66.7%** across **15** graded forecasts.

## Illustrative VaR backtest

- Observations with a usable risk record: **15**
- 95% VaR breaches: **2**
- Observed breach rate: **13.3%** (the model benchmark is approximately 5% over a large sample)

## Reading the table

- **Positive improvement:** the model beat persistence.
- **Negative improvement:** persistence was better; this must not be hidden.
- **Bias above zero:** the model tends to predict too high.
- **Bias below zero:** the model tends to predict too low.
- **Model wins:** percentage of individual days when the model absolute error was smaller.