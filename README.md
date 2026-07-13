# France Power Analytics Pipeline

An integrated, self-grading French power-market project that forecasts:

- Daily mean electricity demand
- Daily mean nuclear generation
- Daily mean wind generation
- Daily mean solar generation
- Daily mean hydro generation
- Residual demand
- Daily maximum French day-ahead electricity price
- An illustrative fixed-volume VaR and stress report

The repository writes **one permanent row per target date** to `fr_predictions_log.csv`, later fills the actual values, and publishes `SCORECARD.md` and `RISK_REPORT.md`.

## Why this version is designed this way

### 1. The forecast runs before the auction

The daily workflow is scheduled for **10:30 Europe/Paris on D-1**. The French day-ahead order book normally closes at 12:00 CET, so the intended forecast is issued before the price is known.

### 2. The lags match information available at forecast time

At 10:30 on D-1, the completed daily average for D-1 does not exist yet. Therefore the models use:

- `lag2`: D-2, the latest fully completed day
- `lag7`: D-7, the comparable completed day one week earlier

This avoids pretending that incomplete future information was available.

### 3. The price validation avoids stacking leakage

The price model uses forecast residual demand. During training, these component forecasts are generated out-of-fold with an expanding time split. The price model is not allowed to train on component predictions created by models that already saw the same answers.

### 4. Negative prices are supported

The price target uses an invertible `asinh` transform instead of `log(price)`, because French day-ahead electricity prices can be zero or negative.

### 5. VaR uses absolute price changes

The risk calculation uses daily changes in EUR/MWh:

```text
VaR = position MWh × standard deviation of daily EUR/MWh changes × z-score
```

This is more robust for power prices than percentage returns, which can become unstable around zero and negative prices.

## Data sources

### Energy-Charts generation and load

```text
https://api.energy-charts.info/public_power?country=fr&start=YYYY-MM-DD&end=YYYY-MM-DD
```

Used series:

- Load
- Nuclear
- Wind onshore
- Wind offshore
- Solar
- Hydro Run-of-River
- Hydro water reservoir

The API returns high-frequency values in MW. The pipeline converts to GW and calculates daily means.

### Energy-Charts French day-ahead price

```text
https://api.energy-charts.info/price?bzn=FR&start=YYYY-MM-DD&end=YYYY-MM-DD
```

The model target is the **maximum price observed within each delivery date**, in EUR/MWh. This is not a baseload or peakload contract settlement.

### Open-Meteo weather

Forecast:

```text
https://api.open-meteo.com/v1/forecast
```

Historical archive:

```text
https://archive-api.open-meteo.com/v1/archive
```

The current model uses Paris as an explicit national weather proxy. This is a known limitation, not hidden national coverage.

## Repository structure

```text
.
├── .github/workflows/
│   ├── daily-france.yml       # forecast, grade, report and commit daily
│   └── train-models.yml       # manual model retraining
├── tests/
│   ├── test_core.py
│   └── test_log_schema.py
├── config.py                  # model features and file paths
├── settings.json              # easy-to-edit paper risk assumptions
├── fr_common.py               # APIs, weather, transforms and risk helpers
├── log_schema.py              # one-row-per-day CSV schema
├── train_models.py            # leakage-safe model training and validation
├── run_daily.py               # forecast and backfill actuals
├── scorecard.py               # rolling model-vs-baseline performance
├── risk_report.py             # current illustrative VaR report
├── FR_Power_Models.ipynb      # notebook wrapper for model training
├── fr_predictions_log.csv     # permanent self-grading record
└── requirements.txt
```

## First setup

### Option A — easiest: train through GitHub Actions

1. Create a new GitHub repository.
2. Upload every file and folder from this project.
3. Open **Actions**.
4. Select **Retrain France models**.
5. Click **Run workflow**.
6. Wait for the workflow to create and commit:
   - `model_fr_demand.txt`
   - `model_fr_nuclear.txt`
   - `model_fr_wind.txt`
   - `model_fr_solar.txt`
   - `model_fr_hydro.txt`
   - `model_fr_price.txt`
   - `model_metadata.json`
   - `training_metrics.json`
   - `MODEL_CARD.md`
7. Run **France power daily pipeline** manually once.
8. Confirm that `fr_predictions_log.csv`, `SCORECARD.md` and `RISK_REPORT.md` update.

### Option B — train locally

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python train_models.py
pytest -q
python run_daily.py
python scorecard.py
python risk_report.py
```

### Option C — use the notebook

Open `FR_Power_Models.ipynb` in an environment where the rest of the repository files are present, then run all cells.

## What the daily log contains

For demand, nuclear, wind, solar, hydro, residual demand and peak price, the log records:

- Model forecast
- Persistence baseline
- Actual result
- Model error
- Baseline error

It also records:

- Forecast issue timing (`pre_auction` or `post_auction_manual`)
- Weather used
- Model training timestamp
- 30-day and 90-day price-change volatility
- 95% and 99% illustrative VaR
- Maximum position allowed by the illustrative VaR limit
- Illustrative realised long/short P&L
- VaR breach flag
- Forecast and grading status

## How self-grading works

On each run, `run_daily.py` first checks older target dates whose actual values are missing. It downloads the realised generation and price data, fills the actual columns and calculates:

```text
model error = prediction - actual
baseline error = persistence prediction - actual
```

The original forecast is never overwritten after a successful issue.

## How to read the scorecard

`SCORECARD.md` includes only forecasts that were:

1. Marked `pre_auction`
2. Later fully graded

A positive improvement means the model beat persistence. A negative improvement means persistence was better. The scorecard deliberately reports both outcomes.

Do not make strong CV claims until at least **30 graded forecasts** exist; 60–90 is more credible.

## Risk assumptions

The following values in `settings.json` are illustrative, not market data:

- Paper position
- Paper capital
- VaR appetite as a percentage of capital
- Maximum position limit
- Stress shocks

The current defaults are:

```text
Paper position: long 100 MWh
Paper capital: €500,000
95% one-day VaR appetite: 2% = €10,000
```

Change them only with a documented reason. Do not describe them as a real company’s limits.

## Important limitations

- Paris weather is only a proxy for national French conditions.
- Training and holdout use realised Open-Meteo archive weather, while live predictions use forecast weather; holdout performance can therefore be optimistic.
- Nuclear availability is driven heavily by maintenance and outage information, which this weather/calendar model does not include.
- Hydro output is affected by reservoir and hydrological conditions not represented by Paris weather.
- Daily maximum price is a difficult and noisy target.
- The generation values are daily means, so intraday ramps and scarcity periods are compressed.
- Parametric VaR is not a maximum possible loss and will understate some power-price tail events.
- Energy-Charts is a convenient aggregation source; production deployment should include formal data licensing and source-governance review.

## Best future upgrades

1. Add RTE nuclear outage and availability data.
2. Replace the Paris proxy with population-weighted multi-region weather.
3. Train with archived D-1 weather forecasts (or exact historical model runs) rather than realised weather.
4. Add reservoir, precipitation and snowmelt features for hydro.
5. Forecast the full 96-quarter-hour price curve rather than only the daily maximum.
6. Add probabilistic forecasts and prediction intervals.
7. Add model-drift monitoring and scheduled retraining rules.
