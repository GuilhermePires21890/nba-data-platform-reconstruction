-- Team-level results per season (one row per team and season).
--
-- Source: team_seasons.csv (balldontlie, 2000-2025). Team wins and losses live here,
-- not in player_stats: player-level vitorias/derrotas are per player, not per team.
-- season uses the same 'EpocaYYYY-YY' label as player_stats, so the two join directly.

CREATE TABLE IF NOT EXISTS team_seasons (
    season          TEXT        NOT NULL,
    team            TEXT        NOT NULL,
    wins            INTEGER     NOT NULL,
    losses          INTEGER     NOT NULL,
    games           INTEGER     NOT NULL,
    pts_for_pg      NUMERIC,
    pts_against_pg  NUMERIC,
    diff_pg         NUMERIC,
    PRIMARY KEY (season, team)
);
