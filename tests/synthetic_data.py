"""Deterministic synthetic player-season data for the API contract tests.

Nothing in this module is real NBA data. Player names are placeholders
("Jogador 001") and team codes are placeholders ("T01" to "T06"), so the
contract tests can run in CI without depending on the production database
or on any licensed dataset.

The table layout follows the columns the API queries (Portuguese names used
in the production database). The generator is seeded, so every run produces
the same rows, and the record holders can be recomputed in Python as an oracle.
"""

from __future__ import annotations

import os
import random
from pathlib import Path

import psycopg2

SEASONS = [f"Epoca{year}-{str(year + 1)[-2:]}" for year in range(1996, 2021)]  # 25 seasons
TEAMS = [f"T{i:02d}" for i in range(1, 7)]
PLAYERS = [f"Jogador {i:03d}" for i in range(1, 61)]  # 60 placeholder players

SCHEMA_FILE = Path(__file__).resolve().parents[1] / "sql" / "schema" / "create_player_stats_table.sql"
DDL = "DROP TABLE IF EXISTS player_stats CASCADE;\n" + SCHEMA_FILE.read_text(encoding="utf-8")

LOCAL_HOSTS = frozenset({"localhost", "127.0.0.1", "::1"})
RESET_FLAG = "ALLOW_TEST_DB_RESET"
TEST_DB_SUFFIX = "_test"
# libpq reads these from the environment when they are not passed as arguments, and
# they can point the connection away from POSTGRES_HOST. Any presence refuses the reset.
LIBPQ_OVERRIDE_VARS = ("PGHOSTADDR", "PGSERVICE", "PGSERVICEFILE")


class ResetRefused(RuntimeError):
    """Raised when the guards refuse a destructive reset. No connection was opened."""


def check_reset_allowed() -> None:
    """Refuse any reset of player_stats unless every guard passes.

    Checks run in this order and stop at the first failure, before any connection:
    1. ALLOW_TEST_DB_RESET must be exactly "1".
    2. PGHOSTADDR, PGSERVICE and PGSERVICEFILE must be absent from the environment.
    3. POSTGRES_HOST must be a local host.
    4. POSTGRES_DB must end with "_test".
    Messages name the variable and its value. They never include the password.
    """
    if os.getenv(RESET_FLAG) != "1":
        raise ResetRefused(
            f"{RESET_FLAG} must be exactly '1' to reset player_stats. "
            "Set it only for the command that intends to reset the test database."
        )
    for var in LIBPQ_OVERRIDE_VARS:
        if var in os.environ:
            raise ResetRefused(
                f"{var} is set in the environment and can redirect the connection away from "
                f"POSTGRES_HOST, so the reset is refused. Unset {var} for this command."
            )
    host = os.getenv("POSTGRES_HOST", "localhost")
    if host not in LOCAL_HOSTS:
        raise ResetRefused(
            f"Refusing to reseed a non-local database (POSTGRES_HOST={host!r}). "
            "Contract tests only run against a local test database."
        )
    dbname = os.getenv("POSTGRES_DB", "nba_data_platform")
    if not dbname.endswith(TEST_DB_SUFFIX):
        raise ResetRefused(
            f"Refusing to reseed database {dbname!r}: its name must end with '{TEST_DB_SUFFIX}'. "
            "Use a dedicated test database, for example nba_data_platform_test."
        )


COLUMNS = [
    "jogador", "equipa", "season", "idade", "jogos_jogados", "minutos_jogador",
    "pontos", "assistencias", "rebotes", "roubos", "bloqueio", "ponto_fantasia",
    "triplos_duplos", "mais_ou_menos", "percentagem_de_meta_de_campo",
    "percentagem_de_lances_livres", "golos_de_campo_de_3_pontos_feitos",
    "tentativa_de_gol_de_campo_de_3_pontos",
    "tentativas_de_metas_de_campo", "metas_de_campo_feitas",
    "tentativa_de_lances_livres", "rebotes_ofensivos",
]


# Columns used by the single-season record categories, with the smallest step that
# separates two values. Ties at the top would make the record holder ambiguous.
RECORD_COLUMNS = {
    "pontos": 0.1,
    "rebotes": 0.1,
    "assistencias": 0.1,
    "ponto_fantasia": 0.1,
    "mais_ou_menos": 0.1,
    "percentagem_de_meta_de_campo": 0.1,
    "golos_de_campo_de_3_pontos_feitos": 0.1,
    "triplos_duplos": 1,
}


def _break_top_ties(rows: list[dict]) -> None:
    """Nudge the runner-up upwards until each record column has a single leader."""
    qualified = [r for r in rows if r["jogos_jogados"] >= 50]
    for column, step in RECORD_COLUMNS.items():
        while True:
            ordered = sorted(qualified, key=lambda r: r[column], reverse=True)
            if ordered[0][column] != ordered[1][column]:
                break
            ordered[1][column] = round(ordered[1][column] + step, 3)


def generate_rows(seed: int = 20260101) -> list[dict]:
    """Return one dict per player-season, deterministic for a given seed."""
    rng = random.Random(seed)
    rows = []
    for season_index, season in enumerate(SEASONS):
        for player_index, player in enumerate(PLAYERS):
            # Players rotate between teams over the seasons, so careers span several teams.
            team = TEAMS[(player_index + season_index) % len(TEAMS)]
            games = rng.randint(30, 82)
            points = round(rng.uniform(6.0, 30.0), 1)
            rebounds = round(rng.uniform(2.0, 12.0), 1)
            assists = round(rng.uniform(1.0, 9.0), 1)
            fantasy = round(points + rebounds * 1.2 + assists * 1.5, 1)
            threes_attempted = round(rng.uniform(1.0, 10.0), 1)
            threes_made = round(threes_attempted * rng.uniform(0.25, 0.42), 1)
            rows.append({
                "jogador": player,
                "equipa": team,
                "season": season,
                "idade": 19 + (player_index % 16),
                "jogos_jogados": games,
                "pontos": points,
                "assistencias": assists,
                "rebotes": rebounds,
                "ponto_fantasia": fantasy,
                "triplos_duplos": rng.randint(0, 3),
                "mais_ou_menos": round(rng.uniform(-10.0, 10.0), 1),
                "percentagem_de_meta_de_campo": round(rng.uniform(38.0, 58.0), 1),
                "golos_de_campo_de_3_pontos_feitos": threes_made,
                "tentativa_de_gol_de_campo_de_3_pontos": threes_attempted,
                "minutos_jogador": round(games * rng.uniform(18.0, 36.0), 1),
                "roubos": round(rng.uniform(0.3, 2.5), 1),
                "bloqueio": round(rng.uniform(0.1, 2.0), 1),
                "percentagem_de_lances_livres": round(rng.uniform(60.0, 92.0), 1),
            })
    _break_top_ties(rows)
    # Shooting volume and offensive rebounds come from a separate generator so the
    # values above stay exactly as before. Makes are derived from the attempts and the
    # field-goal percentage, so makes <= attempts and offensive rebounds <= rebounds.
    rng2 = random.Random(seed + 1)
    for row in rows:
        attempts = round(rng2.uniform(3.0, 25.0), 1)
        row["tentativas_de_metas_de_campo"] = attempts
        row["metas_de_campo_feitas"] = round(attempts * row["percentagem_de_meta_de_campo"] / 100, 1)
        row["tentativa_de_lances_livres"] = round(rng2.uniform(1.0, 10.0), 1)
        row["rebotes_ofensivos"] = round(row["rebotes"] * rng2.uniform(0.2, 0.4), 1)
    return rows


def record_holders(rows: list[dict]) -> dict[str, dict]:
    """Oracle for /analytics/all-time-records, computed in Python from the same rows.

    Mirrors the SQL: only player-seasons with at least 50 games qualify, and each
    category takes the single highest value. Ties would make the API's answer
    arbitrary, so the generator must not produce them; this function fails if it does.
    """
    qualified = [r for r in rows if r["jogos_jogados"] >= 50]
    categories = {
        "highest_scoring_season": "pontos",
        "most_rebounds_season": "rebotes",
        "most_assists_season": "assistencias",
        "highest_fantasy_season": "ponto_fantasia",
        "best_plus_minus_season": "mais_ou_menos",
        "best_fg_pct_season": "percentagem_de_meta_de_campo",
        "most_3pm_season": "golos_de_campo_de_3_pontos_feitos",
        "most_triple_doubles_season": "triplos_duplos",
    }
    holders = {}
    for name, column in categories.items():
        ordered = sorted(qualified, key=lambda r: r[column], reverse=True)
        if len(ordered) > 1 and ordered[0][column] == ordered[1][column]:
            raise AssertionError(f"Tie for {column}: the oracle would be ambiguous")
        best = ordered[0]
        holders[name] = {
            "player": best["jogador"],
            "team": best["equipa"],
            "season": best["season"].replace("Epoca", ""),
            "value": best[column],
        }
    return holders


def load_into_database(rows: list[dict]) -> None:
    """Drop and recreate player_stats in the configured test database, then insert rows.

    Destructive. The guards in check_reset_allowed() run first, before any connection.
    """
    check_reset_allowed()
    conn = psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=os.getenv("POSTGRES_PORT", "5432"),
        dbname=os.getenv("POSTGRES_DB", "nba_data_platform"),
        user=os.getenv("POSTGRES_USER", "nba_admin"),
        password=os.getenv("POSTGRES_PASSWORD", "nba_password"),
    )
    try:
        with conn, conn.cursor() as cur:
            cur.execute(DDL)
            placeholders = ", ".join(["%s"] * len(COLUMNS))
            cur.executemany(
                f"INSERT INTO player_stats ({', '.join(COLUMNS)}) VALUES ({placeholders})",
                [tuple(r[c] for c in COLUMNS) for r in rows],
            )
    finally:
        conn.close()
