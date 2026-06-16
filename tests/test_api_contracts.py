import pytest
import httpx
import time

BASE_URL = "https://nba-data-platform-api.onrender.com"
TIMEOUT = 90.0


def safe_get(client, url, retries=2, retry_sleep=10):
    """GET with retry on rate limit (HTML response = 429 from Render CDN)."""
    for attempt in range(retries + 1):
        r = client.get(url)
        # If response is HTML, Render rate-limited us - wait and retry
        content_type = r.headers.get("content-type", "")
        if "text/html" in content_type and attempt < retries:
            time.sleep(retry_sleep)
            continue
        return r
    return r


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
    """
    Analytics endpoint tests with rate-limit-aware pacing.
    The CI runs against the live Render free-tier API (30 req/min limit).
    A small sleep between tests prevents 429 responses during sequential runs.
    """

    @pytest.fixture(autouse=True)
    def pace_requests(self):
        """Auto-applied fixture: 3s gap before each test in this class.
        The Render free-tier API has a 30 req/min rate limit (slowapi).
        3s spacing = max 20 req/min, safely under the limit.
        """
        time.sleep(3)
        yield

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
        for field in ["season", "team", "championship_score", "predicted_rank"]:
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
        r = safe_get(client, "/analytics/young-stars")
        assert r.status_code == 200

    def test_young_stars_no_duplicates(self, client):
        # BUG-004 regression: DISTINCT ON (jogador) should prevent duplicate players
        r = safe_get(client, "/analytics/young-stars?limit=50")
        assert r.status_code == 200, f"Expected 200, got {r.status_code} - possible rate limit"
        data = r.json()
        players = [p["player"] for p in data["data"]]
        assert len(players) == len(set(players)), "Duplicate players found in young-stars response"

    def test_young_stars_all_under_25(self, client):
        r = safe_get(client, "/analytics/young-stars?limit=50")
        ages = [p["age"] for p in r.json()["data"]]
        assert all(a <= 25 for a in ages)

    def test_young_stars_fields_present(self, client):
        r = safe_get(client, "/analytics/young-stars?limit=1")
        star = r.json()["data"][0]
        for field in ["player", "team", "season", "age", "points", "assists", "rebounds"]:
            assert field in star

    def test_player_career_returns_200(self, client):
        r = safe_get(client, "/analytics/players/LeBron James/career")
        assert r.status_code == 200

    def test_player_career_returns_player_name(self, client):
        r = safe_get(client, "/analytics/players/LeBron James/career")
        assert r.status_code == 200, f"Rate limited or error: {r.status_code}"
        assert r.json()["player"] == "LeBron James"

    def test_player_career_returns_seasons_played(self, client):
        r = safe_get(client, "/analytics/players/LeBron James/career")
        assert r.status_code == 200, f"Rate limited or error: {r.status_code}"
        assert r.json()["seasons_played"] > 0

    def test_player_career_fields_present(self, client):
        r = safe_get(client, "/analytics/players/LeBron James/career")
        season = r.json()["data"][0]
        for field in ["season", "team", "points", "assists", "rebounds"]:
            assert field in season

    def test_player_career_returns_teams(self, client):
        # BUG-005 regression: career should expose all teams played for
        r = safe_get(client, "/analytics/players/LeBron James/career")
        assert "teams" in r.json()
        assert "/" in r.json()["teams"]  # LeBron played for CLE / MIA / LAL

    def test_player_career_unknown_player_returns_empty(self, client):
        r = safe_get(client, "/analytics/players/Unknown Player XYZ/career")
        assert r.status_code == 200
        assert r.json()["count"] == 0


class TestAllTimeRecordsEndpoint:
    """
    Tests for the Sprint 18 /analytics/all-time-records endpoint.
    Returns 8 single-season record holders across all 25 seasons (1996-2021).
    Uses the same pace_requests fixture as TestAnalyticsEndpoints.
    """

    @pytest.fixture(autouse=True)
    def pace_requests(self):
        """3s gap before each test - Render free tier rate limit (30 req/min)."""
        time.sleep(3)
        yield

    def test_all_time_records_returns_200(self, client):
        r = safe_get(client, "/analytics/all-time-records")
        assert r.status_code == 200

    def test_all_time_records_returns_records_key(self, client):
        r = safe_get(client, "/analytics/all-time-records")
        assert "records" in r.json()

    def test_all_time_records_returns_8_records(self, client):
        r = safe_get(client, "/analytics/all-time-records")
        assert r.json()["total_records"] == 8

    def test_all_time_records_highest_scoring_season_present(self, client):
        r = safe_get(client, "/analytics/all-time-records")
        assert "highest_scoring_season" in r.json()["records"]

    def test_all_time_records_most_rebounds_present(self, client):
        r = safe_get(client, "/analytics/all-time-records")
        assert "most_rebounds_season" in r.json()["records"]

    def test_all_time_records_most_assists_present(self, client):
        r = safe_get(client, "/analytics/all-time-records")
        assert "most_assists_season" in r.json()["records"]

    def test_all_time_records_highest_fantasy_present(self, client):
        r = safe_get(client, "/analytics/all-time-records")
        assert "highest_fantasy_season" in r.json()["records"]

    def test_all_time_records_best_plus_minus_present(self, client):
        r = safe_get(client, "/analytics/all-time-records")
        assert "best_plus_minus_season" in r.json()["records"]

    def test_all_time_records_best_fg_pct_present(self, client):
        r = safe_get(client, "/analytics/all-time-records")
        assert "best_fg_pct_season" in r.json()["records"]

    def test_all_time_records_most_3pm_present(self, client):
        r = safe_get(client, "/analytics/all-time-records")
        assert "most_3pm_season" in r.json()["records"]

    def test_all_time_records_most_triple_doubles_present(self, client):
        r = safe_get(client, "/analytics/all-time-records")
        assert "most_triple_doubles_season" in r.json()["records"]

    def test_all_time_records_each_record_has_player_field(self, client):
        r = safe_get(client, "/analytics/all-time-records")
        for record in r.json()["records"].values():
            assert "player" in record

    def test_all_time_records_each_record_has_team_field(self, client):
        r = safe_get(client, "/analytics/all-time-records")
        for record in r.json()["records"].values():
            assert "team" in record

    def test_all_time_records_each_record_has_season_field(self, client):
        r = safe_get(client, "/analytics/all-time-records")
        for record in r.json()["records"].values():
            assert "season" in record

    def test_all_time_records_each_record_has_value_field(self, client):
        r = safe_get(client, "/analytics/all-time-records")
        for record in r.json()["records"].values():
            assert "value" in record

    def test_all_time_records_each_record_has_label_field(self, client):
        r = safe_get(client, "/analytics/all-time-records")
        for record in r.json()["records"].values():
            assert "label" in record

    def test_all_time_records_harden_is_top_scorer(self, client):
        r = safe_get(client, "/analytics/all-time-records")
        record = r.json()["records"]["highest_scoring_season"]
        assert record["player"] == "James Harden"
        assert record["value"] == 36.1

    def test_all_time_records_rodman_is_top_rebounder(self, client):
        r = safe_get(client, "/analytics/all-time-records")
        record = r.json()["records"]["most_rebounds_season"]
        assert record["player"] == "Dennis Rodman"
        assert record["value"] == 16.1

    def test_all_time_records_seasons_covered_is_25(self, client):
        r = safe_get(client, "/analytics/all-time-records")
        assert r.json()["seasons_covered"] == 25

    def test_all_time_records_total_records_is_8(self, client):
        r = safe_get(client, "/analytics/all-time-records")
        assert r.json()["total_records"] == 8


class TestPlayersEndpoint:
    """Tests for the GET /players/ endpoint with various filters."""

    def test_players_returns_200(self, client):
        r = client.get("/players/")
        assert r.status_code == 200

    def test_players_default_limit_20(self, client):
        time.sleep(2)
        r = client.get("/players/")
        data = r.json()
        assert len(data["data"]) <= 20

    def test_players_season_filter(self, client):
        time.sleep(2)
        r = client.get("/players/?season=Epoca2020-21")
        assert r.status_code == 200
        data = r.json()["data"]
        assert len(data) > 0
        assert all(p["season"] == "Epoca2020-21" for p in data)

    def test_players_team_filter(self, client):
        time.sleep(2)
        r = client.get("/players/?team=LAL")
        assert r.status_code == 200
        data = r.json()["data"]
        assert len(data) > 0
        assert all(p["team"] == "LAL" for p in data)