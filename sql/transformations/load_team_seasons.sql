-- Load team_seasons.csv into team_seasons.
--
-- The CSV labels seasons by starting year (2000 = 2000-01). The table uses the same
-- 'EpocaYYYY-YY' label as player_stats, so the year is converted in the INSERT.
-- Runs in one transaction. Run it with psql -f from your machine: \copy reads the CSV
-- on the client, so it also works on Supabase, where server-side COPY is not allowed.
-- Replace /path/to/team_seasons.csv with the local path before running.

BEGIN;

CREATE TEMP TABLE team_seasons_staging (
    season_year     INTEGER,
    team            TEXT,
    wins            INTEGER,
    losses          INTEGER,
    games           INTEGER,
    pts_for_pg      NUMERIC,
    pts_against_pg  NUMERIC,
    diff_pg         NUMERIC
) ON COMMIT DROP;

\copy team_seasons_staging (season_year, team, wins, losses, games, pts_for_pg, pts_against_pg, diff_pg) FROM '/path/to/team_seasons.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',')

INSERT INTO team_seasons (season, team, wins, losses, games, pts_for_pg, pts_against_pg, diff_pg)
SELECT
    'Epoca' || season_year || '-' || LPAD(MOD(season_year + 1, 100)::text, 2, '0'),
    team, wins, losses, games, pts_for_pg, pts_against_pg, diff_pg
FROM team_seasons_staging;

COMMIT;
