"""Shared fixtures for the API contract tests.

The API runs in-process (FastAPI TestClient) against a local PostgreSQL that is
seeded with synthetic data. No request leaves the machine, so the tests do not
depend on Render, on deploy timing, or on the production database.
"""

import os

import pytest

LOCAL_HOSTS = {"localhost", "127.0.0.1", "::1"}


@pytest.fixture(scope="session")
def synthetic_rows():
    from synthetic_data import generate_rows

    return generate_rows()


@pytest.fixture(scope="session")
def seeded_database(synthetic_rows):
    """Replace player_stats in the test database with synthetic rows.

    The table is dropped and recreated, so this must never point at a real
    database. Refuse to run unless the host is local.
    """
    host = os.getenv("POSTGRES_HOST", "localhost")
    if host not in LOCAL_HOSTS:
        pytest.exit(
            f"Refusing to reseed a non-local database (POSTGRES_HOST={host!r}). "
            "Contract tests only run against a local test database.",
            returncode=2,
        )

    from synthetic_data import load_into_database

    load_into_database(synthetic_rows)
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
