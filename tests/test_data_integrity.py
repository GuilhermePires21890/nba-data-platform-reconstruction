# NOTE: These tests require a live database connection (Supabase).
# Run locally with: pytest tests/test_data_integrity.py -v
# Not included in CI pipeline (no production data in CI environment).
import pytest
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "host":     os.getenv("POSTGRES_HOST", "localhost"),
    "port":     os.getenv("POSTGRES_PORT", "5432"),
    "dbname":   os.getenv("POSTGRES_DB", "nba_data_platform"),
    "user":     os.getenv("POSTGRES_USER", "nba_admin"),
    "password": os.getenv("POSTGRES_PASSWORD", "nba_password"),
}


@pytest.fixture(scope="session")
def db():
    conn = psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)
    yield conn
    conn.close()


def query(db, sql):
    with db.cursor() as cur:
        cur.execute(sql)
        return cur.fetchone()


class TestRecordCounts:
    def test_total_records_equals_11460(self, db):
        result = query(db, "SELECT COUNT(*) AS n FROM player_stats")
        assert result["n"] == 11460

    def test_exactly_25_seasons(self, db):
        result = query(db, "SELECT COUNT(DISTINCT season) AS n FROM player_stats")
        assert result["n"] == 25

    def test_first_season_exists(self, db):
        result = query(db, "SELECT COUNT(*) AS n FROM player_stats WHERE season = 'Epoca1996-97'")
        assert result["n"] > 0

    def test_last_season_exists(self, db):
        result = query(db, "SELECT COUNT(*) AS n FROM player_stats WHERE season = 'Epoca2020-21'")
        assert result["n"] > 0


class TestDataQuality:
    def test_no_negative_points(self, db):
        result = query(db, "SELECT COUNT(*) AS n FROM player_stats WHERE pontos < 0")
        assert result["n"] == 0

    def test_no_negative_rebounds(self, db):
        result = query(db, "SELECT COUNT(*) AS n FROM player_stats WHERE rebotes < 0")
        assert result["n"] == 0

    def test_no_negative_assists(self, db):
        result = query(db, "SELECT COUNT(*) AS n FROM player_stats WHERE assistencias < 0")
        assert result["n"] == 0

    def test_fg_percentage_in_valid_range(self, db):
    # Percentages stored as 0-100 scale (e.g. 44.7, not 0.447)
        result = query(db, """
            SELECT COUNT(*) AS n FROM player_stats
            WHERE percentagem_de_meta_de_campo < 0
            OR percentagem_de_meta_de_campo > 100
        """)
        assert result["n"] == 0

    def test_no_null_player_names(self, db):
        result = query(db, "SELECT COUNT(*) AS n FROM player_stats WHERE jogador IS NULL")
        assert result["n"] == 0

    def test_no_null_teams(self, db):
        result = query(db, "SELECT COUNT(*) AS n FROM player_stats WHERE equipa IS NULL")
        assert result["n"] == 0

    def test_no_null_seasons(self, db):
        result = query(db, "SELECT COUNT(*) AS n FROM player_stats WHERE season IS NULL")
        assert result["n"] == 0


class TestSeasonFormat:
    def test_season_format_consistent(self, db):
        result = query(db, """
            SELECT COUNT(*) AS n FROM player_stats
            WHERE season NOT LIKE 'Epoca____-__'
        """)
        assert result["n"] == 0

    def test_known_players_exist(self, db):
        result = query(db, "SELECT COUNT(*) AS n FROM player_stats WHERE jogador = 'LeBron James'")
        assert result["n"] > 0