from fastapi import APIRouter, Query, Request
from src.api.database import get_connection
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

router = APIRouter(prefix="/players", tags=["Players"])


@router.get("/")
@limiter.limit("60/minute")
def get_players(
    request: Request,
    season: str = Query(None, description="Filter by season (e.g. Epoca2020-21)"),
    team: str = Query(None, description="Filter by team (e.g. LAL)"),
    limit: int = Query(20, le=100),
    offset: int = Query(0),
):
    query = "SELECT * FROM player_stats WHERE 1=1"
    params = []

    if season:
        query += " AND season = %s"
        params.append(season)

    if team:
        query += " AND equipa = %s"
        params.append(team)

    query += " ORDER BY pontos DESC"
    query += " LIMIT %s OFFSET %s"
    params.extend([limit, offset])

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, params)
            results = cur.fetchall()

    return {"data": results, "count": len(results)}


@router.get("/top-scorers")
@limiter.limit("30/minute")
def get_top_scorers(
    request: Request,
    season: str = Query(None),
    limit: int = Query(10, le=50),
):
    # FIX BUG-001: added games_played to SELECT
    # FIX BUG-002: normalised field names to English
    query = """
        SELECT
            jogador                         AS player,
            equipa                          AS team,
            season,
            jogos_jogados                   AS games_played,
            ROUND(pontos, 1)                AS points,
            ROUND(assistencias, 1)          AS assists,
            ROUND(rebotes, 1)               AS rebounds,
            ROUND(ponto_fantasia, 1)        AS fantasy_points
        FROM player_stats
        WHERE jogos_jogados >= 50
    """
    params = []

    if season:
        query += " AND season = %s"
        params.append(season)

    query += " ORDER BY pontos DESC LIMIT %s"
    params.append(limit)

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, params)
            results = cur.fetchall()

    return {"data": results, "count": len(results)}


@router.get("/seasons")
@limiter.limit("30/minute")
def get_seasons(request: Request):
    query = "SELECT DISTINCT season FROM player_stats ORDER BY season ASC"

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            results = cur.fetchall()

    return {"seasons": [r["season"] for r in results]}


@router.get("/teams")
@limiter.limit("30/minute")
def get_teams(request: Request):
    query = "SELECT DISTINCT equipa FROM player_stats ORDER BY equipa ASC"

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            results = cur.fetchall()

    return {"teams": [r["equipa"] for r in results]}