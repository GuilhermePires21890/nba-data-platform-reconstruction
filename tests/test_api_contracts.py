import pytest
import httpx
import time

BASE_URL = "https://nba-data-platform-api.onrender.com"
TIMEOUT = 30.0


@pytest.fixture(scope="session")
def client():
    with httpx.Client(base_url=BASE_URL, timeout=TIMEOUT) as c:
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
        r = client.get("/players/top-scorers?limit=1")
        player = r.json()["data"][0]
        for field in ["jogador", "equipa", "season", "pontos", "assistencias", "rebotes"]:
            assert field in player

    def test_top_scorers_invalid_season_returns_empty(self, client):
        r = client.get("/players/top-scorers?season=InvalidSeason")
        assert r.status_code == 200
        assert r.json()["count"] == 0