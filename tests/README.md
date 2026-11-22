# Testing Strategy

This directory contains automated tests for the NBA Data Platform Reconstruction project.

## Destructive contract-test seed

`tests/test_api_contracts.py` replaces the `player_stats` table with synthetic rows. The reset runs only through `synthetic_data.load_into_database()`, which checks these guards in order before opening a connection:

1. `ALLOW_TEST_DB_RESET` must be exactly `1`.
2. `PGHOSTADDR`, `PGSERVICE` and `PGSERVICEFILE` must be absent from the environment, even if empty. libpq reads them and they can redirect the connection.
3. `POSTGRES_HOST` must be `localhost`, `127.0.0.1` or `::1`.
4. `POSTGRES_DB` must end with `_test`.

If any guard fails, the run stops with exit code 2 and no table is changed. In CI, only the API contract step sets the flag, and it uses the dedicated `nba_data_platform_test` database.

The reset opt-in must be supplied explicitly on the command line for each run. Do not put `ALLOW_TEST_DB_RESET` in `.env`, `.env.example`, a shell profile, or any other persistent configuration, because that would enable destructive resets for every run.

## Planned Areas

- Data quality validation
- Schema validation
- Transformation validation
- Pipeline execution checks
- Regression testing

## Objectives

- Improve reliability
- Reduce transformation errors
- Validate datasets
- Support maintainable engineering practices
