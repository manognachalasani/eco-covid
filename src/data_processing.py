"""Data loading and cleaning entry points.

Dataset integration is intentionally left as a placeholder for this mock-dashboard phase.
Keep raw files in data/raw/ and write cleaned, documented files to data/processed/.
"""

from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
PROCESSED_DIR = ROOT / "data" / "processed"

def load_processed_data(filename="economic_indicators.csv"):
    """Load a future processed dataset, once the team selects real sources."""
    path = PROCESSED_DIR / filename
    if not path.exists():
        raise FileNotFoundError(
            f"{path} does not exist yet. Add a cleaned dataset when data collection begins."
        )
    return pd.read_csv(path)

def clean_economic_data(df):
    """TODO: add project-specific cleaning after choosing actual source schemas."""
    # Do not silently impute or harmonize values before source definitions are reviewed.
    return df.copy()
