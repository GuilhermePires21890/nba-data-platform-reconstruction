"""API contract tests.

The API runs in-process against a local PostgreSQL seeded with synthetic data
(see tests/conftest.py and tests/synthetic_data.py). No request leaves the
machine, so these tests do not depend on Render or on the production database.
"""

import time

import pytest

from synthetic_data import SEASONS, TEAMS, record_holders


@pytest.fixture
def client(api_client):
    return api_client


def safe_get(client, url):
    """GET a URL on the local test client."""
    return client.get(url)


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
        # The count is a constant in main.py, not computed from the table.
        r = client.get("/")
        assert isinstance(r.json()["records"], int)


class TestSeasonsEndpoint:
    def test_seasons_returns_200(self, client):
        r = client.get("/players/seasons")
        assert r.status_code == 200

    def test_seasons_returns_25_seasons(self, client):
        r = client.get("/players/seasons")
        assert r.json()["seasons"] == SEASONS

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

    def test_teams_contains_all_seeded_teams(self, client):
        r = client.get("/players/teams")
        assert sorted(r.json()["teams"]) == sorted(TEAMS)


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
    """Analytics endpoints: shape and business rules, checked against synthetic data."""


    def test_era_analysis_returns_200(self, client):
        r = safe_get(client, "/analytics/era-analysis")
        assert r.status_code == 200

    def test_era_analysis_returns_5_eras(self, client):
        r = safe_get(client, "/analytics/era-analysis")
        assert r.json()["count"] == 5

    def test_era_analysis_fields_present(self, client):
        r = safe_get(client, "/analytics/era-analysis")
        era = r.json()["data"][0]
        for field in ["era", "avg_points", "avg_assists", "avg_rebounds", "avg_3pm", "avg_fantasy"]:
            assert field in era

    def test_era_analysis_first_era_is_jordan(self, client):
        r = safe_get(client, "/analytics/era-analysis")
        eras = [e["era"] for e in r.json()["data"]]
        assert "1996-2001 Jordan Era" in eras

    def test_championship_predictor_returns_200(self, client):
        r = safe_get(client, "/analytics/championship-predictor")
        assert r.status_code == 200

    def test_championship_predictor_all_seasons_returns_24(self, client):
        # BUG-003 regression: one prediction per season. The first season has no
        # previous season to forecast from, so 25 seasons give 24 forecasts.
        r = safe_get(client, "/analytics/championship-predictor")
        assert r.json()["count"] == 24

    def test_championship_predictor_fields_present(self, client):
        r = safe_get(client, "/analytics/championship-predictor")
        entry = r.json()["data"][0]
        for field in ["season", "based_on_season", "team", "championship_score", "predicted_rank"]:
            assert field in entry

    def test_championship_predictor_season_filter(self, client):
        r = safe_get(client, "/analytics/championship-predictor?season=Epoca2020-21")
        assert r.status_code == 200
        data = r.json()["data"]
        assert len(data) > 0
        assert all(e["season"] == "Epoca2020-21" for e in data)

    def test_three_point_revolution_returns_200(self, client):
        r = safe_get(client, "/analytics/3point-revolution")
        assert r.status_code == 200

    def test_three_point_revolution_returns_25_seasons(self, client):
        r = safe_get(client, "/analytics/3point-revolution")
        assert r.json()["count"] == 25

    def test_three_point_revolution_fields_present(self, client):
        r = safe_get(client, "/analytics/3point-revolution")
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
        r = safe_get(client, "/analytics/players/Jogador 001/career")
        assert r.status_code == 200

    def test_player_career_returns_player_name(self, client):
        r = safe_get(client, "/analytics/players/Jogador 001/career")
        assert r.status_code == 200, f"Rate limited or error: {r.status_code}"
        assert r.json()["player"] == "Jogador 001"

    def test_player_career_returns_seasons_played(self, client):
        r = safe_get(client, "/analytics/players/Jogador 001/career")
        assert r.status_code == 200, f"Rate limited or error: {r.status_code}"
        assert r.json()["seasons_played"] > 0

    def test_player_career_fields_present(self, client):
        r = safe_get(client, "/analytics/players/Jogador 001/career")
        season = r.json()["data"][0]
        for field in ["season", "team", "points", "assists", "rebounds"]:
            assert field in season

    def test_player_career_returns_teams(self, client):
        # BUG-005 regression: career should expose all teams played for
        r = safe_get(client, "/analytics/players/Jogador 001/career")
        assert "teams" in r.json()
        assert " / " in r.json()["teams"]  # Jogador 001 rotates between teams

    def test_player_career_unknown_player_returns_empty(self, client):
        r = safe_get(client, "/analytics/players/Unknown Player XYZ/career")
        assert r.status_code == 200
        assert r.json()["count"] == 0


class TestAllTimeRecordsEndpoint:
    """
    Tests for the Sprint 18 /analytics/all-time-records endpoint.
    Returns 8 single-season record holders across all 25 seasons (1996-2021).
    """


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

    def test_all_time_records_highest_scoring_matches_oracle(self, client, synthetic_rows):
        r = client.get("/analytics/all-time-records")
        record = r.json()["records"]["highest_scoring_season"]
        expected = record_holders(synthetic_rows)["highest_scoring_season"]
        assert record["player"] == expected["player"]
        assert record["season"] == expected["season"]
        assert record["value"] == pytest.approx(expected["value"], abs=0.05)

    def test_all_time_records_most_rebounds_matches_oracle(self, client, synthetic_rows):
        r = client.get("/analytics/all-time-records")
        record = r.json()["records"]["most_rebounds_season"]
        expected = record_holders(synthetic_rows)["most_rebounds_season"]
        assert record["player"] == expected["player"]
        assert record["value"] == pytest.approx(expected["value"], abs=0.05)

    def test_all_time_records_seasons_covered_is_25(self, client):
        r = safe_get(client, "/analytics/all-time-records")
        assert r.json()["seasons_covered"] == 25

    def test_all_time_records_total_records_is_8(self, client):
        r = safe_get(client, "/analytics/all-time-records")
        assert r.json()["total_records"] == 8


class TestEnrichedAnalytics:
    """Efficiency, career totals, age curve, roster profile and style evolution.

    Each business rule is checked twice: the response must have the right shape,
    and the value must match a plain Python calculation over the synthetic rows.
    """

    @staticmethod
    def _ts(row):
        attempts = row["tentativas_de_metas_de_campo"] + 0.44 * row["tentativa_de_lances_livres"]
        return row["pontos"] / (2 * attempts) * 100

    # --- True Shooting ---------------------------------------------------

    def test_true_shooting_returns_200_with_five_eras(self, client):
        r = safe_get(client, "/analytics/true-shooting")
        assert r.status_code == 200
        body = r.json()
        assert len(body["by_era"]) == 5
        for field in ["era", "league_ts_pct", "player_seasons"]:
            assert field in body["by_era"][0]

    def test_true_shooting_respects_min_games(self, client):
        r = safe_get(client, "/analytics/true-shooting?min_games=60&limit=20")
        assert r.status_code == 200
        leaders = r.json()["leaders"]
        assert leaders, "expected at least one leader with 60+ games"
        assert all(row["games"] >= 60 for row in leaders)

    def test_true_shooting_top_leaders_match_oracle(self, client, synthetic_rows):
        r = safe_get(client, "/analytics/true-shooting?min_games=50&min_fga=15&limit=3")
        leaders = r.json()["leaders"]
        eligible = [row for row in synthetic_rows
                    if row["jogos_jogados"] >= 50 and row["tentativas_de_metas_de_campo"] >= 15]
        expected = sorted((self._ts(row) for row in eligible), reverse=True)[:3]
        assert len(leaders) == 3
        for leader, value in zip(leaders, expected):
            assert abs(leader["ts_pct"] - value) <= 0.05

    def test_true_shooting_min_fga_filters_low_volume_players(self, client, synthetic_rows):
        r = safe_get(client, "/analytics/true-shooting?min_games=1&min_fga=20&limit=50")
        assert r.status_code == 200
        eligible = [row for row in synthetic_rows if row["tentativas_de_metas_de_campo"] >= 20]
        assert r.json()["count"] == min(50, len(eligible))

    def test_true_shooting_limit_is_enforced(self, client):
        r = safe_get(client, "/analytics/true-shooting?limit=3")
        assert len(r.json()["leaders"]) == 3

    # --- Career totals ---------------------------------------------------

    def test_player_totals_match_oracle(self, client, synthetic_rows):
        r = safe_get(client, "/analytics/players/Jogador 001/totals")
        assert r.status_code == 200
        totals = r.json()["totals"]
        rows = [row for row in synthetic_rows if row["jogador"] == "Jogador 001"]
        assert totals["seasons"] == len(rows)
        assert totals["games"] == sum(row["jogos_jogados"] for row in rows)
        expected_points = sum(row["pontos"] * row["jogos_jogados"] for row in rows)
        assert abs(float(totals["points"]) - expected_points) <= 1

    def test_player_totals_peak_season_is_highest_scoring(self, client, synthetic_rows):
        r = safe_get(client, "/analytics/players/Jogador 001/totals")
        peak = r.json()["peak_season"]
        eligible = [row for row in synthetic_rows
                    if row["jogador"] == "Jogador 001" and row["jogos_jogados"] >= 20]
        best = max(row["pontos"] for row in eligible)
        assert peak is not None
        assert abs(peak["points"] - best) <= 0.05

    def test_player_totals_unknown_player_returns_null(self, client):
        r = safe_get(client, "/analytics/players/Unknown Player XYZ/totals")
        assert r.status_code == 200
        assert r.json()["totals"] is None

    # --- Age curve -------------------------------------------------------

    def test_age_curve_covers_ages_19_to_34_only(self, client):
        r = safe_get(client, "/analytics/age-curve")
        assert r.status_code == 200
        ages = [row["age"] for row in r.json()["data"]]
        assert ages == sorted(ages)
        assert min(ages) >= 19 and max(ages) <= 34

    def test_age_curve_points_match_oracle(self, client, synthetic_rows):
        r = safe_get(client, "/analytics/age-curve")
        for row in r.json()["data"]:
            sample = [s for s in synthetic_rows
                      if s["idade"] == row["age"] and s["jogos_jogados"] >= 20]
            expected = sum(s["pontos"] for s in sample) / len(sample)
            assert abs(float(row["avg_points"]) - expected) <= 0.06

    # --- Roster profile --------------------------------------------------

    def test_roster_profile_returns_200_for_season(self, client):
        r = safe_get(client, "/analytics/roster-profile?season=2010-11")
        assert r.status_code == 200
        body = r.json()
        assert body["season"] == "2010-11"
        assert body["count"] == len(body["data"]) > 0
        for field in ["team", "players", "avg_age", "top_scorers"]:
            assert field in body["data"][0]

    def test_roster_profile_player_counts_match_oracle(self, client, synthetic_rows):
        r = safe_get(client, "/analytics/roster-profile?season=2010-11")
        for team_row in r.json()["data"]:
            roster = [s for s in synthetic_rows
                      if s["season"] == "Epoca2010-11" and s["equipa"] == team_row["team"]
                      and s["jogos_jogados"] >= 20]
            assert team_row["players"] == len(roster)

    def test_roster_profile_top_scorers_match_oracle(self, client, synthetic_rows):
        r = safe_get(client, "/analytics/roster-profile?season=2010-11")
        for team_row in r.json()["data"]:
            roster = [s for s in synthetic_rows
                      if s["season"] == "Epoca2010-11" and s["equipa"] == team_row["team"]
                      and s["jogos_jogados"] >= 20]
            expected = [s["jogador"] for s in sorted(roster, key=lambda s: (-s["pontos"], s["jogador"]))[:3]]
            assert team_row["top_scorers"] == expected

    def test_roster_profile_rejects_malformed_season(self, client):
        r = safe_get(client, "/analytics/roster-profile?season=2010")
        assert r.status_code == 422

    # --- Style evolution -------------------------------------------------

    def test_style_evolution_returns_five_eras_with_valid_shares(self, client):
        r = safe_get(client, "/analytics/style-evolution")
        assert r.status_code == 200
        data = r.json()["data"]
        assert len(data) == 5
        for era in data:
            assert 0 < era["three_point_attempt_share_pct"] < 100
            assert 0 < era["offensive_rebound_share_pct"] < 100


class TestPlayersEndpoint:
    """Tests for the GET /players/ endpoint with various filters."""

    def test_players_returns_200(self, client):
        r = client.get("/players/")
        assert r.status_code == 200

    def test_players_default_limit_20(self, client):
        r = client.get("/players/")
        data = r.json()
        assert len(data["data"]) <= 20

    def test_players_season_filter(self, client):
        r = client.get("/players/?season=Epoca2020-21")
        assert r.status_code == 200
        data = r.json()["data"]
        assert len(data) > 0
        assert all(p["season"] == "Epoca2020-21" for p in data)

    def test_players_team_filter(self, client):
        r = client.get("/players/?team=T01")
        assert r.status_code == 200
        data = r.json()["data"]
        assert len(data) > 0
        # /players/ uses SELECT * - returns raw DB column names (equipa, not team)
        assert all(p["equipa"] == "T01" for p in data)


class TestInputValidation:
    """Query parameters must be validated by FastAPI (422), never reach the database."""

    @pytest.mark.parametrize("url", [
        "/players/?limit=-1",
        "/players/?limit=0",
        "/players/?offset=-1",
        "/players/top-scorers?limit=0",
        "/analytics/young-stars?limit=-1",
        "/analytics/championship-predictor?limit=0",
    ])
    def test_invalid_numeric_params_return_422(self, client, url):
        r = safe_get(client, url)
        assert r.status_code == 422, f"{url} returned {r.status_code}"
