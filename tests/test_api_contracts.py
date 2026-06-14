import pytest
import httpx
import time

BASE_URL = "https://nba-data-platform-api.onrender.com"
TIMEOUT = 90.0


@pytest.fixture(scope="session")
def client():
    with httpx.Client(base_url=BASE_URL, timeout=TIMEOUT) as c:
        # Warm up - wake API before running tests
        for _ in range(3):
            try:
                c.get("/health")
                break
            except Exception:
                time.sleep(10)
        yield c


class TestHealthEndpoint:
    def test_health_returns_200(self, client):
        r = client.get("/health")
        assert r.status_code == 200

    def test_health_returns_ok_status(self, client):
        r = client.get("/health")
        assert r.json()["status"] == "ok"

    def test_health_response_time_under_3s(self, client):
        start = time.time()
        client.get("/health")
        elapsed = time.time() - start
        assert elapsed < 3.0


class TestRootEndpoint:
    def test_root_returns_200(self, client):
        r = client.get("/")
        assert r.status_code == 200

    def test_root_contains_version(self, client):
        r = client.get("/")
        assert "version" in r.json()

    def test_root_contains_records_count(self, client):
        r = client.get("/")
        assert r.json()["records"] == 11460


class TestSeasonsEndpoint:
    def test_seasons_returns_200(self, client):
        r = client.get("/players/seasons")
        assert r.status_code == 200

    def test_seasons_returns_25_seasons(self, client):
        r = client.get("/players/seasons")
        assert len(r.json()["seasons"]) == 25

    def test_seasons_contains_first_season(self, client):
        r = client.get("/players/seasons")
        assert "Epoca1996-97" in r.json()["seasons"]

    def test_seasons_contains_last_season(self, client):
        r = client.get("/players/seasons")
        assert "Epoca2020-21" in r.json()["seasons"]


class TestTeamsEndpoint:
    def test_teams_returns_200(self, client):
        r = client.get("/players/teams")
        assert r.status_code == 200

    def test_teams_returns_non_empty_list(self, client):
        r = client.get("/players/teams")
        assert len(r.json()["teams"]) > 0

    def test_teams_contains_known_team(self, client):
        r = client.get("/players/teams")
        assert "LAL" in r.json()["teams"]


class TestTopScorersEndpoint:
    def test_top_scorers_returns_200(self, client):
        r = client.get("/players/top-scorers")
        assert r.status_code == 200

    def test_top_scorers_default_limit_10(self, client):
        r = client.get("/players/top-scorers")
        assert r.json()["count"] == 10

    def test_top_scorers_custom_limit(self, client):
        time.sleep(2)
        r = client.get("/players/top-scorers?limit=25")
        assert r.json()["count"] == 25

    def test_top_scorers_max_limit_100(self, client):
        r = client.get("/players/top-scorers?limit=99999")
        assert r.status_code == 422

    def test_top_scorers_season_filter(self, client):
        r = client.get("/players/top-scorers?season=Epoca2020-21&limit=10")
        assert r.status_code == 200
        data = r.json()["data"]
        assert all(p["season"] == "Epoca2020-21" for p in data)

    def test_top_scorers_returns_expected_fields(self, client):
        # FIX BUG-002: field names normalised to English in Sprint 16
        r = client.get("/players/top-scorers?limit=1")
        player = r.json()["data"][0]
        for field in ["player", "team", "season", "points", "assists", "rebounds", "games_played"]:
            assert field in player

    def test_top_scorers_games_played_not_null(self, client):
        # Regression test for BUG-001: games_played was missing from SELECT
        r = client.get("/players/top-scorers?limit=1")
        player = r.json()["data"][0]
        assert player["games_played"] is not None
        assert isinstance(player["games_played"], (int, float))
        assert player["games_played"] > 0

    def test_top_scorers_invalid_season_returns_empty(self, client):
        r = client.get("/players/top-scorers?season=InvalidSeason")
        assert r.status_code == 200
        assert r.json()["count"] == 0


class TestAnalyticsEndpoints:
    def test_era_analysis_returns_200(self, client):
        r = client.get("/analytics/era-analysis")
        assert r.status_code == 200

    def test_era_analysis_returns_5_eras(self, client):
        r = client.get("/analytics/era-analysis")
        assert r.json()["count"] == 5

    def test_era_analysis_fields_present(self, client):
        r = client.get("/analytics/era-analysis")
        era = r.json()["data"][0]
        for field in ["era", "avg_points", "avg_assists", "avg_rebounds", "avg_3pm", "avg_fantasy"]:
            assert field in era

    def test_era_analysis_first_era_is_jordan(self, client):
        r = client.get("/analytics/era-analysis")
        eras = [e["era"] for e in r.json()["data"]]
        assert "1996-2001 Jordan Era" in eras

    def test_championship_predictor_returns_200(self, client):
        r = client.get("/analytics/championship-predictor")
        assert r.status_code == 200

    def test_championship_predictor_all_seasons_returns_25(self, client):
        # BUG-003 regression: without season filter should return 1 per season = 25
        r = client.get("/analytics/championship-predictor")
        assert r.json()["count"] == 25

    def test_championship_predictor_fields_present(self, client):
        r = client.get("/analytics/championship-predictor")
        entry = r.json()["data"][0]
        for field in ["season", "equipa", "championship_score", "predicted_rank"]:
            assert field in entry

    def test_championship_predictor_season_filter(self, client):
        r = client.get("/analytics/championship-predictor?season=Epoca2020-21")
        assert r.status_code == 200
        data = r.json()["data"]
        assert len(data) > 0
        assert all(e["season"] == "Epoca2020-21" for e in data)

    def test_three_point_revolution_returns_200(self, client):
        r = client.get("/analytics/3point-revolution")
        assert r.status_code == 200

    def test_three_point_revolution_returns_25_seasons(self, client):
        r = client.get("/analytics/3point-revolution")
        assert r.json()["count"] == 25

    def test_three_point_revolution_fields_present(self, client):
        r = client.get("/analytics/3point-revolution")
        row = r.json()["data"][0]
        for field in ["season", "avg_3pm", "avg_3pa", "league_3p_pct"]:
            assert field in row

    def test_young_stars_returns_200(self, client):
        r = client.get("/analytics/young-stars")
        assert r.status_code == 200

    def test_young_stars_no_duplicates(self, client):
        # BUG-004 regression: DISTINCT ON (jogador) should prevent duplicate players
        r = client.get("/analytics/young-stars?limit=50")
        players = [p["jogador"] for p in r.json()["data"]]
        assert len(players) == len(set(players)), "Duplicate players found in young-stars response"

    def test_young_stars_all_under_25(self, client):
        r = client.get("/analytics/young-stars?limit=50")
        ages = [p["idade"] for p in r.json()["data"]]
        assert all(a <= 25 for a in ages)

    def test_young_stars_fields_present(self, client):
        r = client.get("/analytics/young-stars?limit=1")
        star = r.json()["data"][0]
        for field in ["jogador", "equipa", "season", "idade", "points", "assists", "rebounds"]:
            assert field in star

    def test_player_career_returns_200(self, client):
        r = client.get("/analytics/players/LeBron James/career")
        assert r.status_code == 200

    def test_player_career_returns_player_name(self, client):
        r = client.get("/analytics/players/LeBron James/career")
        assert r.json()["player"] == "LeBron James"

    def test_player_career_returns_seasons_played(self, client):
        r = client.get("/analytics/players/LeBron James/career")
        assert r.json()["seasons_played"] > 0

    def test_player_career_fields_present(self, client):
        r = client.get("/analytics/players/LeBron James/career")
        season = r.json()["data"][0]
        for field in ["season", "equipa", "points", "assists", "rebounds"]:
            assert field in season

    def test_player_career_returns_teams(self, client):
        # BUG-005 regression: career should expose all teams played for
        r = client.get("/analytics/players/LeBron James/career")
        assert "teams" in r.json()
        assert "/" in r.json()["teams"]  # LeBron played for CLE / MIA / LAL

    def test_player_career_unknown_player_returns_empty(self, client):
        r = client.get("/analytics/players/Unknown Player XYZ/career")
        assert r.status_code == 200
        assert r.json()["count"] == 0