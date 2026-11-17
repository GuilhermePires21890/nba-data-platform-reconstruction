import importlib.util
from pathlib import Path

_path = Path(__file__).resolve().parents[1] / "scripts" / "build_team_seasons.py"
_spec = importlib.util.spec_from_file_location("build_team_seasons", _path)
bts = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(bts)


def game(home, away, hs, vs, postseason=False, date="2021-01-01"):
    return {
        "status_state": "final",
        "postseason": postseason,
        "date": date,
        "home_team": {"abbreviation": home},
        "visitor_team": {"abbreviation": away},
        "home_team_score": hs,
        "visitor_team_score": vs,
    }


def test_team_season_totals_and_diff():
    games = [game("AAA", "BBB", 110, 100), game("BBB", "AAA", 90, 105)]
    rows = {r["team"]: r for r in bts.build_team_seasons(games)}
    assert rows["AAA"]["wins"] == 2 and rows["AAA"]["losses"] == 0
    assert rows["AAA"]["diff_pg"] == 12.5  # (110 + 105 - 100 - 90) / 2
    assert rows["BBB"]["wins"] == 0 and rows["BBB"]["losses"] == 2


def test_playoff_games_are_excluded_from_team_season():
    games = [game("AAA", "BBB", 120, 80, postseason=True)]
    assert bts.build_team_seasons(games) == []


def test_champion_is_winner_of_last_playoff_game():
    games = [
        game("AAA", "BBB", 100, 90, postseason=True, date="2021-06-01"),
        game("BBB", "AAA", 101, 99, postseason=True, date="2021-06-10"),
    ]
    champ = bts.find_champion(games)
    assert champ["champion"] == "BBB" and champ["runner_up"] == "AAA"


def test_no_playoffs_returns_none():
    assert bts.find_champion([game("AAA", "BBB", 100, 90)]) is None


def test_empty_rebuild_removes_stale_csv(tmp_path):
    stale = tmp_path / "team_seasons.csv"
    stale.write_text("season,team\n2020,OLD\n", encoding="utf-8")
    bts.write_csv(stale, [])
    assert not stale.exists()
