# France Power Forecast Scorecard

_Only forecasts marked **pre_auction** and later fully graded are included._

- Logged rows: **44**
- Official pre-auction rows: **19**
- Fully graded official rows: **18**

> **Sample warning:** fewer than 30 graded forecasts are available. The figures below are operational checks, not strong evidence of model skill.

## Model versus persistence

The persistence baseline uses the latest completed daily observation available at the 10:30 D-1 issue time (D-2).

| target | n | model MAE | baseline MAE | improvement | RMSE | bias | model wins |
|---|---:|---:|---:|---:|---:|---:|---:|
| demand (GW) | 18 | 1.24 | 3.44 | +64.0% | 1.57 | +1.13 | 83.3% |
| nuclear (GW) | 18 | 2.67 | 1.87 | -42.8% | 2.97 | +2.33 | 44.4% |
| wind (GW) | 18 | 1.46 | 2.24 | +34.7% | 1.86 | -0.07 | 66.7% |
| solar (GW) | 18 | 0.58 | 0.97 | +40.6% | 0.78 | -0.19 | 66.7% |
| hydro (GW) | 18 | 0.47 | 0.37 | -26.1% | 0.52 | +0.46 | 38.9% |
| residual (GW) | 18 | 2.65 | 3.17 | +16.2% | 3.10 | -1.40 | 55.6% |
| peak price (EUR/MWh) | 18 | 71.24 | 59.23 | -20.3% | 93.52 | -71.24 | 27.8% |

## Price direction

Directional accuracy versus the D-2 reference price: **55.6%** across **18** graded forecasts.

## Illustrative VaR backtest

- Observations with a usable risk record: **18**
- 95% VaR breaches: **2**
- Observed breach rate: **11.1%** (the model benchmark is approximately 5% over a large sample)

## Reading the table

- **Positive improvement:** the model beat persistence.
- **Negative improvement:** persistence was better; this must not be hidden.
- **Bias above zero:** the model tends to predict too high.
- **Bias below zero:** the model tends to predict too low.
- **Model wins:** percentage of individual days when the model absolute error was smaller.