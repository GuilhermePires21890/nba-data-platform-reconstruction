"""Shared fixtures for the API contract tests.

The API runs in-process (FastAPI TestClient) against a local PostgreSQL that is
seeded with synthetic data. No request leaves the machine, so the tests do not
depend on Render, on deploy timing, or on the production database.
"""

import pytest


@pytest.fixture(scope="session")
def synthetic_rows():
    from synthetic_data import generate_rows

    return generate_rows()


@pytest.fixture(scope="session")
def seeded_database(synthetic_rows):
    """Replace player_stats in the dedicated test database with synthetic rows.

    The safety guards live in synthetic_data.load_into_database(). If they refuse,
    the whole run stops with exit code 2 before any connection or DDL executes.
    """
    from synthetic_data import ResetRefused, load_into_database

    try:
        load_into_database(synthetic_rows)
    except ResetRefused as exc:
        pytest.exit(str(exc), returncode=2)
    yield


@pytest.fixture(scope="session")
def api_client(seeded_database):
    """In-process client for the FastAPI app, backed by the seeded database."""
    from fastapi.testclient import TestClient

    from src.api.main import app
    from src.api.routers import analytics, players
    from src.api.main import limiter as app_limiter

    # Rate limits protect the public API. They are not what these tests check,
    # and the local client would otherwise hit them during a normal run.
    for limiter in (app_limiter, analytics.limiter, players.limiter):
        limiter.enabled = False

    with TestClient(app) as client:
        yield client
