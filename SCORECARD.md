# France Power Forecast Scorecard

_Only forecasts marked **pre_auction** and later fully graded are included._

- Logged rows: **30**
- Official pre-auction rows: **6**
- Fully graded official rows: **4**

> **Sample warning:** fewer than 30 graded forecasts are available. The figures below are operational checks, not strong evidence of model skill.

## Model versus persistence

The persistence baseline uses the latest completed daily observation available at the 10:30 D-1 issue time (D-2).

| target | n | model MAE | baseline MAE | improvement | RMSE | bias | model wins |
|---|---:|---:|---:|---:|---:|---:|---:|
| demand (GW) | 4 | 2.26 | 3.64 | +38.1% | 2.58 | +1.85 | 75.0% |
| nuclear (GW) | 4 | 2.76 | 2.12 | -30.2% | 2.92 | +2.76 | 50.0% |
| wind (GW) | 4 | 1.02 | 1.09 | +6.1% | 1.22 | -0.01 | 75.0% |
| solar (GW) | 4 | 0.29 | 1.45 | +80.0% | 0.35 | -0.02 | 100.0% |
| hydro (GW) | 4 | 0.61 | 0.22 | -176.4% | 0.64 | +0.61 | 0.0% |
| residual (GW) | 4 | 1.93 | 1.95 | +1.0% | 2.20 | -1.50 | 50.0% |
| peak price (EUR/MWh) | 4 | 31.84 | 14.22 | -124.0% | 36.80 | -31.84 | 50.0% |

## Price direction

Directional accuracy versus the D-2 reference price: **50.0%** across **4** graded forecasts.

## Illustrative VaR backtest

- Observations with a usable risk record: **4**
- 95% VaR breaches: **0**
- Observed breach rate: **0.0%** (the model benchmark is approximately 5% over a large sample)

## Reading the table

- **Positive improvement:** the model beat persistence.
- **Negative improvement:** persistence was better; this must not be hidden.
- **Bias above zero:** the model tends to predict too high.
- **Bias below zero:** the model tends to predict too low.
- **Model wins:** percentage of individual days when the model absolute error was smaller.