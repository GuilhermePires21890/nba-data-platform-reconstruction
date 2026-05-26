import pytest
import pandas as pd
from src.transformation.consolidate_seasons import (
    extract_season_from_filename,
    normalize_columns,
)
from src.validation.schema_validator import validate_required_columns


class TestSeasonExtraction:
    def test_extracts_season_from_filename(self):
        assert extract_season_from_filename("1996-97.csv") == "1996-97"

    def test_removes_csv_extension(self):
        result = extract_season_from_filename("2020-21.csv")
        assert ".csv" not in result

    def test_handles_underscore_format(self):
        result = extract_season_from_filename("WebScrapper1996-97.csv")
        assert "csv" not in result


class TestColumnNormalization:
    def test_lowercase_columns(self):
        df = pd.DataFrame(columns=["Player", "Team", "Points"])
        result = normalize_columns(df)
        assert list(result.columns) == ["player", "team", "points"]

    def test_spaces_replaced_with_underscores(self):
        df = pd.DataFrame(columns=["player name", "team name"])
        result = normalize_columns(df)
        assert "player_name" in result.columns
        assert "team_name" in result.columns

    def test_strips_whitespace(self):
        df = pd.DataFrame(columns=[" player ", " team "])
        result = normalize_columns(df)
        assert "player" in result.columns
        assert "team" in result.columns


class TestSchemaValidation:
    def test_valid_schema_passes(self):
        cols = ["player_name", "team", "points", "rebounds", "assists"]
        assert validate_required_columns(cols) is True

    def test_missing_column_raises_error(self):
        cols = ["player_name", "team", "points"]
        with pytest.raises(ValueError) as exc:
            validate_required_columns(cols)
        assert "Missing required columns" in str(exc.value)

    def test_empty_columns_raises_error(self):
        with pytest.raises(ValueError):
            validate_required_columns([])