# France Power Forecast Scorecard

_Only forecasts marked **pre_auction** and later fully graded are included._

- Logged rows: **43**
- Official pre-auction rows: **19**
- Fully graded official rows: **17**

> **Sample warning:** fewer than 30 graded forecasts are available. The figures below are operational checks, not strong evidence of model skill.

## Model versus persistence

The persistence baseline uses the latest completed daily observation available at the 10:30 D-1 issue time (D-2).

| target | n | model MAE | baseline MAE | improvement | RMSE | bias | model wins |
|---|---:|---:|---:|---:|---:|---:|---:|
| demand (GW) | 17 | 1.24 | 3.44 | +64.1% | 1.58 | +1.13 | 82.4% |
| nuclear (GW) | 17 | 2.64 | 1.88 | -39.9% | 2.95 | +2.27 | 47.1% |
| wind (GW) | 17 | 1.51 | 2.01 | +25.0% | 1.90 | -0.04 | 64.7% |
| solar (GW) | 17 | 0.60 | 1.03 | +42.1% | 0.80 | -0.22 | 70.6% |
| hydro (GW) | 17 | 0.47 | 0.34 | -37.9% | 0.53 | +0.47 | 35.3% |
| residual (GW) | 17 | 2.69 | 2.75 | +2.3% | 3.14 | -1.36 | 52.9% |
| peak price (EUR/MWh) | 17 | 72.03 | 61.04 | -18.0% | 95.20 | -72.03 | 29.4% |

## Price direction

Directional accuracy versus the D-2 reference price: **58.8%** across **17** graded forecasts.

## Illustrative VaR backtest

- Observations with a usable risk record: **17**
- 95% VaR breaches: **2**
- Observed breach rate: **11.8%** (the model benchmark is approximately 5% over a large sample)

## Reading the table

- **Positive improvement:** the model beat persistence.
- **Negative improvement:** persistence was better; this must not be hidden.
- **Bias above zero:** the model tends to predict too high.
- **Bias below zero:** the model tends to predict too low.
- **Model wins:** percentage of individual days when the model absolute error was smaller.