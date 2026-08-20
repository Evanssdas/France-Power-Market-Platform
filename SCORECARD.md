# France Power Forecast Scorecard

_Only forecasts marked **pre_auction** and later fully graded are included._

- Logged rows: **37**
- Official pre-auction rows: **13**
- Fully graded official rows: **11**

> **Sample warning:** fewer than 30 graded forecasts are available. The figures below are operational checks, not strong evidence of model skill.

## Model versus persistence

The persistence baseline uses the latest completed daily observation available at the 10:30 D-1 issue time (D-2).

| target | n | model MAE | baseline MAE | improvement | RMSE | bias | model wins |
|---|---:|---:|---:|---:|---:|---:|---:|
| demand (GW) | 11 | 1.20 | 3.13 | +61.8% | 1.67 | +1.03 | 81.8% |
| nuclear (GW) | 11 | 3.38 | 1.81 | -86.8% | 3.53 | +3.38 | 27.3% |
| wind (GW) | 11 | 1.12 | 1.46 | +23.5% | 1.32 | +0.18 | 63.6% |
| solar (GW) | 11 | 0.58 | 1.08 | +46.8% | 0.81 | -0.37 | 72.7% |
| hydro (GW) | 11 | 0.46 | 0.32 | -40.8% | 0.51 | +0.45 | 27.3% |
| residual (GW) | 11 | 3.06 | 2.50 | -22.4% | 3.50 | -2.61 | 45.5% |
| peak price (EUR/MWh) | 11 | 73.46 | 81.64 | +10.0% | 106.01 | -73.46 | 45.5% |

## Price direction

Directional accuracy versus the D-2 reference price: **54.5%** across **11** graded forecasts.

## Illustrative VaR backtest

- Observations with a usable risk record: **11**
- 95% VaR breaches: **2**
- Observed breach rate: **18.2%** (the model benchmark is approximately 5% over a large sample)

## Reading the table

- **Positive improvement:** the model beat persistence.
- **Negative improvement:** persistence was better; this must not be hidden.
- **Bias above zero:** the model tends to predict too high.
- **Bias below zero:** the model tends to predict too low.
- **Model wins:** percentage of individual days when the model absolute error was smaller.