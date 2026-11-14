"""Walk-forward backtest for champion prediction, using only earlier seasons.

Reads data/processed/balldontlie/team_seasons.csv and champions.csv (written by
build_team_seasons.py) and, for each test season, predicts the champion using
only information from the previous season. Same-season statistics are never used,
because they describe the season itself and would leak the outcome.

Strategies compared:
- previous_best_record: team with the most wins in the previous season.
- previous_best_diff: team with the highest point differential per game in the
  previous season.
- same_season_diff (reference only, leaks the outcome): highest point differential
  in the season being predicted. Shown to make the leakage visible.
- random: 1 / number of teams, the chance baseline.
"""

from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path

PROCESSED = Path("data/processed/balldontlie")


def read_csv(name: str) -> list[dict]:
    with (PROCESSED / name).open(encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def top_team(rows: list[dict], key: str) -> str:
    return max(rows, key=lambda r: float(r[key]))["team"]


def main() -> None:
    teams_by_season: dict[int, list[dict]] = defaultdict(list)
    for row in read_csv("team_seasons.csv"):
        teams_by_season[int(row["season"])].append(row)
    champions = {int(r["season"]): r["champion"] for r in read_csv("champions.csv")}

    seasons = sorted(s for s in champions if s in teams_by_season and (s - 1) in teams_by_season)
    if not seasons:
        raise SystemExit("Need at least two consecutive seasons in the processed data.")

    results = {name: [] for name in ("previous_best_record", "previous_best_diff", "same_season_diff")}
    print(f"{'season':<8}{'champion':<10}{'prev_record':<14}{'prev_diff':<13}{'same_season_diff':<18}")
    for season in seasons:
        actual = champions[season]
        prev = teams_by_season[season - 1]
        same = teams_by_season[season]
        picks = {
            "previous_best_record": top_team(prev, "wins"),
            "previous_best_diff": top_team(prev, "diff_pg"),
            "same_season_diff": top_team(same, "diff_pg"),
        }
        for name, pick in picks.items():
            results[name].append(pick == actual)
        print(f"{season:<8}{actual:<10}{picks['previous_best_record']:<14}"
              f"{picks['previous_best_diff']:<13}{picks['same_season_diff']:<18}")

    n_teams = sum(len(teams_by_season[s]) for s in seasons) / len(seasons)
    print(f"\nTest seasons: {len(seasons)}  (average teams per season: {n_teams:.0f})")
    for name, hits in results.items():
        print(f"{name:<22} exact hits: {sum(hits)}/{len(hits)}  ({sum(hits) / len(hits):.0%})")
    print(f"{'random (chance)':<22} expected: {1 / n_teams:.1%} per season")


if __name__ == "__main__":
    main()
