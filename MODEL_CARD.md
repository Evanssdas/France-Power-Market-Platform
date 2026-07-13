# France Power Model Card

_Trained 2026-07-13T13:38:52.380392+00:00._

## Design

- Forecast issue time: 10:30 Europe/Paris on the day before delivery.
- Component lags: D-2 and D-7, because D-1 daily means are incomplete at issue time.
- Price stacking: out-of-fold component predictions; no in-sample residual-demand leakage.
- Weather: Paris is currently an explicit national proxy and a known limitation.
- Holdout weather uses realised archive values, while live serving uses forecast weather; live accuracy may therefore be worse.
- Generation targets: daily mean GW.
- Price target: daily maximum France day-ahead price in EUR/MWh.

## Holdout results

| model | n | MAE | baseline MAE | improvement |
|---|---:|---:|---:|---:|
| demand (GW) | 178 | 1.49 | 3.67 | +59.3% |
| nuclear (GW) | 178 | 2.12 | 2.44 | +12.8% |
| wind (GW) | 178 | 1.44 | 3.06 | +52.9% |
| solar (GW) | 178 | 0.68 | 0.80 | +15.0% |
| hydro (GW) | 178 | 0.70 | 0.65 | -8.4% |
| price (EUR/MWh) | 178 | 32.65 | 41.60 | +21.5% |

A negative improvement means the model lost to the persistence baseline. That result must be reported honestly rather than hidden.