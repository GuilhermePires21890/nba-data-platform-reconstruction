from fastapi import APIRouter, Query, HTTPException
from src.api.database import get_connection

router = APIRouter(prefix="/players", tags=["Players"])


@router.get("/")
def get_players(
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
    query += f" LIMIT %s OFFSET %s"
    params.extend([limit, offset])

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, params)
            results = cur.fetchall()

    return {"data": results, "count": len(results)}


@router.get("/top-scorers")
def get_top_scorers(
    season: str = Query(None),
    limit: int = Query(10, le=50),
):
    query = """
        SELECT jogador, equipa, season, pontos, assistencias, rebotes, ponto_fantasia
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
def get_seasons():
    query = "SELECT DISTINCT season FROM player_stats ORDER BY season ASC"

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            results = cur.fetchall()

    return {"seasons": [r["season"] for r in results]}


@router.get("/teams")
def get_teams():
    query = "SELECT DISTINCT equipa FROM player_stats ORDER BY equipa ASC"

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            results = cur.fetchall()

    return {"teams": [r["equipa"] for r in results]}