# France Power Forecast Scorecard

_Only forecasts marked **pre_auction** and later fully graded are included._

- Logged rows: **39**
- Official pre-auction rows: **15**
- Fully graded official rows: **13**

> **Sample warning:** fewer than 30 graded forecasts are available. The figures below are operational checks, not strong evidence of model skill.

## Model versus persistence

The persistence baseline uses the latest completed daily observation available at the 10:30 D-1 issue time (D-2).

| target | n | model MAE | baseline MAE | improvement | RMSE | bias | model wins |
|---|---:|---:|---:|---:|---:|---:|---:|
| demand (GW) | 13 | 1.26 | 2.87 | +56.1% | 1.67 | +1.12 | 76.9% |
| nuclear (GW) | 13 | 3.03 | 1.92 | -57.4% | 3.27 | +2.86 | 38.5% |
| wind (GW) | 13 | 1.39 | 1.50 | +7.1% | 1.69 | +0.28 | 53.8% |
| solar (GW) | 13 | 0.62 | 1.17 | +46.6% | 0.83 | -0.18 | 76.9% |
| hydro (GW) | 13 | 0.44 | 0.32 | -40.1% | 0.49 | +0.44 | 30.8% |
| residual (GW) | 13 | 2.74 | 2.26 | -20.9% | 3.24 | -2.28 | 46.2% |
| peak price (EUR/MWh) | 13 | 73.43 | 70.37 | -4.4% | 102.15 | -73.43 | 38.5% |

## Price direction

Directional accuracy versus the D-2 reference price: **61.5%** across **13** graded forecasts.

## Illustrative VaR backtest

- Observations with a usable risk record: **13**
- 95% VaR breaches: **2**
- Observed breach rate: **15.4%** (the model benchmark is approximately 5% over a large sample)

## Reading the table

- **Positive improvement:** the model beat persistence.
- **Negative improvement:** persistence was better; this must not be hidden.
- **Bias above zero:** the model tends to predict too high.
- **Bias below zero:** the model tends to predict too low.
- **Model wins:** percentage of individual days when the model absolute error was smaller.