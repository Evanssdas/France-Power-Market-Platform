"""Generate a Colab-friendly notebook that runs the leakage-safe trainer."""
from pathlib import Path

import nbformat as nbf

root = Path(__file__).resolve().parent
notebook = nbf.v4.new_notebook()
notebook["metadata"] = {
    "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
    "language_info": {"name": "python", "version": "3.11"},
}
notebook["cells"] = [
    nbf.v4.new_markdown_cell(
        """# France Power Analytics — model training

This notebook trains six integrated models:

1. French demand
2. Nuclear generation
3. Wind generation
4. Solar generation
5. Hydro generation
6. Daily maximum day-ahead price

The price model uses **out-of-fold component forecasts**, not in-sample component predictions. This prevents optimistic leakage. The validation baseline is the latest completed daily observation available at a 10:30 D-1 forecast issue time (D-2)."""
    ),
    nbf.v4.new_code_cell("!pip -q install -r requirements.txt"),
    nbf.v4.new_markdown_cell(
        """## Train and validate

This downloads about 18 months of Energy-Charts generation/price data and Open-Meteo weather, performs a time holdout, compares every model with persistence, and saves the final LightGBM model files."""
    ),
    nbf.v4.new_code_cell("%run train_models.py"),
    nbf.v4.new_markdown_cell("## Inspect the saved validation metrics"),
    nbf.v4.new_code_cell(
        """import json, pandas as pd
metrics = json.load(open('training_metrics.json'))
rows=[]
for name, block in metrics.items():
    rows.append({
        'model': name,
        'n': block['n'],
        'mae': block['mae'],
        'baseline_mae': block['baseline_mae'],
        'improvement_pct': block['improvement_pct'],
        'bias': block['bias'],
    })
pd.DataFrame(rows)"""
    ),
    nbf.v4.new_markdown_cell(
        """## Important interpretation

A negative improvement is not a failed notebook. It means persistence beat the model on the holdout. That is especially plausible for nuclear generation, which is driven by outage and maintenance information rather than weather alone."""
    ),
]
nbf.write(notebook, root / "FR_Power_Models.ipynb")
print("Wrote FR_Power_Models.ipynb")
