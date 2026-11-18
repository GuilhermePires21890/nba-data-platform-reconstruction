# Runbook - Production Data Load

Operational steps to bring the production PostgreSQL database (Supabase) in line with the
consolidated dataset and the team-season table. Written for a manual run from a developer
machine. No credentials are stored in this repository.

---

## Scope

| Table | Source | Loader | Idempotent |
|---|---|---|---|
| `player_stats` | `player_stats_consolidated.csv` | `sql/transformations/load_processed_data.sql` | No (plain `INSERT`) |
| `team_seasons` | `team_seasons.csv` | `sql/transformations/load_team_seasons.sql` | Yes (upsert on `season, team`) |

Schema files: `sql/schema/create_player_stats_table.sql` and `sql/schema/create_team_seasons_table.sql`.
Migration for databases created with an earlier schema: `sql/migrations/001_player_stats_full_schema.sql`.

---

## Prerequisites

- `psql` (PostgreSQL 16 client) installed locally.
- Repository checked out on the branch that contains the loaders (or `main`, once merged).
- Session pooler connection details from the Supabase dashboard (Connect > Session pooler).
- The database password, stored in a password manager. Do not paste it into chat, terminal history or files.

---

## Step 1 - Export connection variables (per terminal session)

```bash
read -s "PGPASSWORD?Password: "; echo
export PGPASSWORD
export PGHOST=<session-pooler-host>
export PGPORT=5432
export PGUSER=postgres.<project-ref>
export PGDATABASE=postgres
export PGSSLMODE=require
```

Variables live only in the terminal session where they were exported. Clear them when done:

```bash
unset PGPASSWORD
```

---

## Step 2 - Read-only checks

```bash
psql -Atc "SELECT count(*) FROM player_stats;"
psql -Atc "SELECT count(*) FROM information_schema.tables WHERE table_name='team_seasons';"
psql -Atc "SELECT count(*) FROM information_schema.columns WHERE table_name='player_stats';"
```

Stop and review before continuing if:
- `player_stats` already has rows and a reload is planned. The player loader is a plain `INSERT`, so a reload duplicates rows.
- The column count is not 30. Run the migration first.

---

## Step 3 - Backup

```bash
pg_dump --table=player_stats -f ~/backup_player_stats_<YYYY-MM-DD>.sql
```

Confirm the file is not empty before any change.

---

## Step 4 - Schema changes (only when needed)

Apply the migration only if Step 2 shows fewer than 30 columns:

```bash
psql -v ON_ERROR_STOP=1 -f sql/migrations/001_player_stats_full_schema.sql
```

Create `team_seasons` if it does not exist:

```bash
psql -v ON_ERROR_STOP=1 -f sql/schema/create_team_seasons_table.sql
```

---

## Step 5 - Loads

The loaders use `\copy`, which reads the CSV from the client machine, so they also work on Supabase.
Replace the placeholder path with the local path before running.

```bash
sed "s#/path/to/team_seasons.csv#<LOCAL_PATH>/team_seasons.csv#" sql/transformations/load_team_seasons.sql > /tmp/run_team.sql
psql -v ON_ERROR_STOP=1 -f /tmp/run_team.sql
```

Player data is loaded only into an empty `player_stats` table (see Step 2):

```bash
sed "s#/path/to/player_stats_consolidated.csv#<LOCAL_PATH>/player_stats_consolidated.csv#" sql/transformations/load_processed_data.sql > /tmp/run_player.sql
psql -v ON_ERROR_STOP=1 -f /tmp/run_player.sql
```

Each loader runs in one transaction. An error rolls back the whole load.

---

## Step 6 - Verification

| Check | Expected |
|---|---|
| `SELECT count(*) FROM player_stats;` | 11,460 (rows in the consolidated dataset) |
| `SELECT count(*) FROM team_seasons;` | 776 |
| `SELECT season, team, wins, losses FROM team_seasons WHERE season='Epoca2025-26' AND team='NYK';` | `54 / 29` |
| `SELECT count(*) FROM player_stats WHERE percentagem_de_meta_de_campo > 100 OR percentagem_de_meta_de_campo < 0;` | 0 |
| `SELECT count(DISTINCT season) FROM player_stats;` | 25 |

Then check the public API:

- `GET /health` returns `{"status":"ok"}`.
- `GET /players/seasons` returns the list of 25 seasons. This endpoint also exercises the database connection.

---

## Step 7 - Cleanup

```bash
rm -f /tmp/run_team.sql /tmp/run_player.sql
unset PGPASSWORD
```

---

## Rollback

- Failed loads roll back automatically.
- For a completed load that must be undone, restore from the backup in Step 3 with `psql -f`, or delete the affected rows with a documented query.

---

## Known limitations

- `player_stats` has no primary key. Loading it twice duplicates rows. A future change should add a
  unique key on `(jogador, equipa, season)` after confirming that combination is unique in the source.
- `team_seasons` season labels follow the `EpocaYYYY-YY` convention, converted from the start year in the CSV.
