from pathlib import Path
import pandas as pd

RAW_DATA_PATH = Path('data/raw/legacy_csv')
OUTPUT_PATH = Path('data/processed/player_stats_consolidated.csv')


def extract_season_from_filename(filename: str) -> str:
    season = filename.replace('.csv', '')
    season = season.replace('_', '-')
    return season


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = [
        column.strip().lower().replace(' ', '_')
        for column in df.columns
    ]

    return df


def consolidate_datasets() -> pd.DataFrame:
    csv_files = list(RAW_DATA_PATH.glob('*.csv'))

    consolidated_dataframes = []

    for csv_file in csv_files:
        df = pd.read_csv(csv_file, sep=';')

        df = normalize_columns(df)

        df['season'] = extract_season_from_filename(csv_file.name)

        consolidated_dataframes.append(df)

    final_dataframe = pd.concat(
        consolidated_dataframes,
        ignore_index=True
    )

    return final_dataframe


def export_consolidated_dataset(df: pd.DataFrame):
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(OUTPUT_PATH, index=False)


def main():
    consolidated_df = consolidate_datasets()

    export_consolidated_dataset(consolidated_df)

    print('Dataset consolidation completed successfully.')


if __name__ == '__main__':
    main()
