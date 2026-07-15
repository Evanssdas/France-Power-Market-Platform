# France Power Forecast Scorecard

_Only forecasts marked **pre_auction** and later fully graded are included._

- Logged rows: **3**
- Official pre-auction rows: **0**
- Fully graded official rows: **0**

> **Sample warning:** fewer than 30 graded forecasts are available. The figures below are operational checks, not strong evidence of model skill.

## Model versus persistence

The persistence baseline uses the latest completed daily observation available at the 10:30 D-1 issue time (D-2).

| target | n | model MAE | baseline MAE | improvement | RMSE | bias | model wins |
|---|---:|---:|---:|---:|---:|---:|---:|
| demand (GW) | 0 | — | — | — | — | — | — |
| nuclear (GW) | 0 | — | — | — | — | — | — |
| wind (GW) | 0 | — | — | — | — | — | — |
| solar (GW) | 0 | — | — | — | — | — | — |
| hydro (GW) | 0 | — | — | — | — | — | — |
| residual (GW) | 0 | — | — | — | — | — | — |
| peak price (EUR/MWh) | 0 | — | — | — | — | — | — |

## Price direction

No graded price forecasts yet.

## Illustrative VaR backtest

- Observations with a usable risk record: **0**
- 95% VaR breaches: **0**
- Observed breach rate: **0.0%** (the model benchmark is approximately 5% over a large sample)

## Reading the table

- **Positive improvement:** the model beat persistence.
- **Negative improvement:** persistence was better; this must not be hidden.
- **Bias above zero:** the model tends to predict too high.
- **Bias below zero:** the model tends to predict too low.
- **Model wins:** percentage of individual days when the model absolute error was smaller.