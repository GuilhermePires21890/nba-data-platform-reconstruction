"""Build team-season tables and champions from the raw balldontlie game files.

Reads data/raw/balldontlie/season_<year>/page_*.json (written by
ingest_balldontlie_games.py) and writes two CSV files to
data/processed/balldontlie/ (ignored by Git):

- team_seasons.csv: one row per team and season, from regular-season games only
  (wins, losses, points for and against per game, point differential per game).
- champions.csv: one row per season, the winner of the last playoff game.

The champion rule is the last final playoff game of the season. It was checked
manually against published results for the seasons 2020-21 to 2024-25. The
2025-26 result must still be confirmed on the official NBA site before publication.
"""

from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path

RAW_DIR = Path("data/raw/balldontlie")
OUT_DIR = Path("data/processed/balldontlie")


def load_games(season_dir: Path) -> list[dict]:
    games: list[dict] = []
    for page in sorted(season_dir.glob("page_*.json")):
        games.extend(json.loads(page.read_text(encoding="utf-8")).get("data", []))
    return [g for g in games if g.get("status_state") == "final"]


def build_team_seasons(games: list[dict]) -> list[dict]:
    """Aggregate regular-season games into one row per team."""
    stats: dict[str, dict] = defaultdict(lambda: {"wins": 0, "losses": 0, "pts_for": 0, "pts_against": 0})
    for game in games:
        if game["postseason"]:
            continue
        home, away = game["home_team"]["abbreviation"], game["visitor_team"]["abbreviation"]
        hs, vs = game["home_team_score"], game["visitor_team_score"]
        for team, scored, allowed in ((home, hs, vs), (away, vs, hs)):
            row = stats[team]
            row["pts_for"] += scored
            row["pts_against"] += allowed
            row["wins" if scored > allowed else "losses"] += 1

    rows = []
    for team, s in sorted(stats.items()):
        played = s["wins"] + s["losses"]
        rows.append({
            "team": team,
            "wins": s["wins"],
            "losses": s["losses"],
            "games": played,
            "pts_for_pg": round(s["pts_for"] / played, 2),
            "pts_against_pg": round(s["pts_against"] / played, 2),
            "diff_pg": round((s["pts_for"] - s["pts_against"]) / played, 2),
        })
    return rows


def find_champion(games: list[dict]) -> dict | None:
    """Return the winner of the last playoff game, or None if there are no playoff games."""
    playoff = [g for g in games if g["postseason"]]
    if not playoff:
        return None
    last = max(playoff, key=lambda g: g["date"])
    if last["home_team_score"] > last["visitor_team_score"]:
        champ, runner_up = last["home_team"], last["visitor_team"]
    else:
        champ, runner_up = last["visitor_team"], last["home_team"]
    return {"champion": champ["abbreviation"], "runner_up": runner_up["abbreviation"], "final_game_date": last["date"]}


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    team_rows: list[dict] = []
    champ_rows: list[dict] = []

    for season_dir in sorted(RAW_DIR.glob("season_*")):
        season = int(season_dir.name.split("_")[1])
        games = load_games(season_dir)
        for row in build_team_seasons(games):
            team_rows.append({"season": season, **row})
        champ = find_champion(games)
        if champ:
            champ_rows.append({"season": season, **champ})
        print(f"Season {season}: {len(games)} final games, champion {champ['champion'] if champ else 'n/a'}")

    write_csv(OUT_DIR / "team_seasons.csv", team_rows)
    write_csv(OUT_DIR / "champions.csv", champ_rows)
    print(f"Wrote {len(team_rows)} team-season rows and {len(champ_rows)} champions to {OUT_DIR}.")


if __name__ == "__main__":
    main()
