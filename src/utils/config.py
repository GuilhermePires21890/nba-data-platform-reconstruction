from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

RAW_DATA_PATH = BASE_DIR / 'data' / 'raw' / 'legacy_csv'
PROCESSED_DATA_PATH = BASE_DIR / 'data' / 'processed'
CURATED_DATA_PATH = BASE_DIR / 'data' / 'curated'

CONSOLIDATED_DATASET_NAME = 'player_stats_consolidated.csv'
