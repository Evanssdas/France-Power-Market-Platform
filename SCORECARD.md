# France Power Forecast Scorecard

_Only forecasts marked **pre_auction** and later fully graded are included._

- Logged rows: **50**
- Official pre-auction rows: **19**
- Fully graded official rows: **19**

> **Sample warning:** fewer than 30 graded forecasts are available. The figures below are operational checks, not strong evidence of model skill.

## Model versus persistence

The persistence baseline uses the latest completed daily observation available at the 10:30 D-1 issue time (D-2).

| target | n | model MAE | baseline MAE | improvement | RMSE | bias | model wins |
|---|---:|---:|---:|---:|---:|---:|---:|
| demand (GW) | 19 | 1.20 | 3.38 | +64.4% | 1.53 | +1.04 | 84.2% |
| nuclear (GW) | 19 | 2.83 | 1.99 | -42.2% | 3.17 | +2.51 | 42.1% |
| wind (GW) | 19 | 1.39 | 2.17 | +36.2% | 1.81 | -0.07 | 68.4% |
| solar (GW) | 19 | 0.61 | 0.93 | +34.6% | 0.80 | -0.24 | 63.2% |
| hydro (GW) | 19 | 0.45 | 0.36 | -23.9% | 0.51 | +0.45 | 42.1% |
| residual (GW) | 19 | 2.79 | 3.28 | +14.9% | 3.24 | -1.60 | 57.9% |
| peak price (EUR/MWh) | 19 | 71.33 | 56.15 | -27.0% | 92.55 | -71.33 | 26.3% |

## Price direction

Directional accuracy versus the D-2 reference price: **52.6%** across **19** graded forecasts.

## Illustrative VaR backtest

- Observations with a usable risk record: **19**
- 95% VaR breaches: **2**
- Observed breach rate: **10.5%** (the model benchmark is approximately 5% over a large sample)

## Reading the table

- **Positive improvement:** the model beat persistence.
- **Negative improvement:** persistence was better; this must not be hidden.
- **Bias above zero:** the model tends to predict too high.
- **Bias below zero:** the model tends to predict too low.
- **Model wins:** percentage of individual days when the model absolute error was smaller.