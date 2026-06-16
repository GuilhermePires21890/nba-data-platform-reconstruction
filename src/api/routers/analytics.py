from fastapi import APIRouter, Query, Request
from src.api.database import get_connection
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/championship-predictor")
@limiter.limit("30/minute")
def get_championship_predictor(
    request: Request,
    season: str = Query(None, description="Filter by season (e.g. Epoca2020-21)"),
    limit: int = Query(30, le=30),
):
    query = """
        WITH roster_stats AS (
            SELECT
                season,
                equipa,
                COUNT(*)                            AS roster_size,
                ROUND(AVG(mais_ou_menos), 3)        AS avg_plus_minus,
                ROUND(AVG(ponto_fantasia), 3)       AS avg_fantasy,
                ROUND(AVG(pontos), 3)               AS avg_points,
                ROUND(AVG(assistencias), 3)         AS avg_assists,
                ROUND(AVG(rebotes), 3)              AS avg_rebounds
            FROM player_stats
            WHERE jogos_jogados >= 20
            GROUP BY season, equipa
        ),
        scored AS (
            SELECT *,
                ROUND(
                    (avg_plus_minus * 0.35) +
                    (avg_fantasy    * 0.25) +
                    (avg_points     * 0.20) +
                    (avg_assists    * 0.10) +
                    (avg_rebounds   * 0.10)
                , 3) AS championship_score,
                RANK() OVER (
                    PARTITION BY season
                    ORDER BY
                        (avg_plus_minus * 0.35) +
                        (avg_fantasy    * 0.25) +
                        (avg_points     * 0.20) +
                        (avg_assists    * 0.10) +
                        (avg_rebounds   * 0.10) DESC
                ) AS predicted_rank
            FROM roster_stats
        )
        SELECT season, equipa AS team, championship_score,
               avg_plus_minus, avg_fantasy, avg_points,
               avg_assists, avg_rebounds, predicted_rank
        FROM scored
        WHERE 1=1
    """
    params = []

    if season:
        query += " AND season = %s"
        params.append(season)
        query += " ORDER BY predicted_rank ASC LIMIT %s"
        params.append(limit)
    else:
        query += " AND predicted_rank = 1"
        query += " ORDER BY season DESC LIMIT %s"
        params.append(limit)

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, params)
            results = cur.fetchall()

    return {"data": results, "count": len(results)}


@router.get("/era-analysis")
@limiter.limit("30/minute")
def get_era_analysis(request: Request):
    query = """
        SELECT
            CASE
                WHEN season IN ('Epoca1996-97','Epoca1997-98','Epoca1998-99','Epoca1999-00','Epoca2000-01')
                    THEN '1996-2001 Jordan Era'
                WHEN season IN ('Epoca2001-02','Epoca2002-03','Epoca2003-04','Epoca2004-05','Epoca2005-06')
                    THEN '2001-2006 Post-Jordan'
                WHEN season IN ('Epoca2006-07','Epoca2007-08','Epoca2008-09','Epoca2009-10','Epoca2010-11')
                    THEN '2006-2011 LeBron Rise'
                WHEN season IN ('Epoca2011-12','Epoca2012-13','Epoca2013-14','Epoca2014-15','Epoca2015-16')
                    THEN '2011-2016 Heat and Warriors'
                WHEN season IN ('Epoca2016-17','Epoca2017-18','Epoca2018-19','Epoca2019-20','Epoca2020-21')
                    THEN '2016-2021 Modern Era'
            END                                         AS era,
            COUNT(*)                                    AS total_player_seasons,
            ROUND(AVG(pontos), 2)                       AS avg_points,
            ROUND(AVG(assistencias), 2)                 AS avg_assists,
            ROUND(AVG(rebotes), 2)                      AS avg_rebounds,
            ROUND(AVG(golos_de_campo_de_3_pontos_feitos), 2) AS avg_3pm,
            ROUND(AVG(ponto_fantasia), 2)               AS avg_fantasy,
            SUM(triplos_duplos)                         AS total_triple_doubles
        FROM player_stats
        WHERE jogos_jogados >= 20
        GROUP BY era
        ORDER BY MIN(season) ASC
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            results = cur.fetchall()

    return {"data": results, "count": len(results)}


@router.get("/3point-revolution")
@limiter.limit("30/minute")
def get_3point_revolution(request: Request):
    query = """
        SELECT
            season,
            ROUND(AVG(golos_de_campo_de_3_pontos_feitos), 2)        AS avg_3pm,
            ROUND(AVG(tentativa_de_gol_de_campo_de_3_pontos), 2)    AS avg_3pa,
            ROUND(
                SUM(golos_de_campo_de_3_pontos_feitos) /
                NULLIF(SUM(tentativa_de_gol_de_campo_de_3_pontos), 0) * 100
            , 1)                                                     AS league_3p_pct,
            COUNT(*)                                                 AS total_players
        FROM player_stats
        WHERE jogos_jogados >= 20
        GROUP BY season
        ORDER BY season ASC
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            results = cur.fetchall()

    return {"data": results, "count": len(results)}


@router.get("/young-stars")
@limiter.limit("30/minute")
def get_young_stars(
    request: Request,
    season: str = Query(None),
    limit: int = Query(25, le=50),
):
    if season:
        query = """
            SELECT
                jogador AS player, equipa AS team, season, idade AS age, jogos_jogados,
                ROUND(pontos, 1)            AS points,
                ROUND(assistencias, 1)      AS assists,
                ROUND(rebotes, 1)           AS rebounds,
                ROUND(ponto_fantasia, 1)    AS fantasy_points,
                triplos_duplos
            FROM player_stats
            WHERE idade <= 25
              AND jogos_jogados >= 50
              AND season = %s
            ORDER BY ponto_fantasia DESC
            LIMIT %s
        """
        params = [season, limit]
    else:
        query = """
            WITH best_season AS (
                SELECT DISTINCT ON (jogador)
                    jogador AS player, equipa AS team, season, idade AS age, jogos_jogados,
                    ROUND(pontos, 1)            AS points,
                    ROUND(assistencias, 1)      AS assists,
                    ROUND(rebotes, 1)           AS rebounds,
                    ROUND(ponto_fantasia, 1)    AS fantasy_points,
                    triplos_duplos
                FROM player_stats
                WHERE idade <= 25
                  AND jogos_jogados >= 50
                ORDER BY jogador, ponto_fantasia DESC
            )
            SELECT * FROM best_season
            ORDER BY fantasy_points DESC
            LIMIT %s
        """
        params = [limit]

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, params)
            results = cur.fetchall()

    return {"data": results, "count": len(results)}


@router.get("/players/{player_name}/career")
@limiter.limit("30/minute")
def get_player_career(request: Request, player_name: str):
    query = """
        SELECT
            season, equipa AS team, idade AS age, jogos_jogados,
            ROUND(pontos, 1)                                    AS points,
            ROUND(assistencias, 1)                              AS assists,
            ROUND(rebotes, 1)                                   AS rebounds,
            ROUND(ponto_fantasia, 1)                            AS fantasy_points,
            ROUND(percentagem_de_meta_de_campo, 1)              AS fg_pct,
            ROUND(golos_de_campo_de_3_pontos_feitos, 1)         AS threes_made,
            mais_ou_menos                                       AS plus_minus,
            triplos_duplos
        FROM player_stats
        WHERE jogador = %s
        ORDER BY season ASC
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, [player_name])
            results = cur.fetchall()

    if not results:
        return {"data": [], "count": 0, "player": player_name, "seasons_played": 0}

    teams = list(dict.fromkeys(r["team"] for r in results))
    teams_display = " / ".join(teams) if len(teams) <= 3 else f"{teams[0]} / {teams[1]} / +{len(teams)-2} more"

    return {
        "player": player_name,
        "teams": teams_display,
        "seasons_played": len(results),
        "data": results,
        "count": len(results),
    }


@router.get("/all-time-records")
@limiter.limit("30/minute")
def get_all_time_records(request: Request):
    """
    Sprint 18 - All-Time Records endpoint.
    Returns single-season record holders for 8 statistical categories
    across all 25 seasons (1996-2021), with full player/team/season context.
    Uses simple subqueries for maximum PostgreSQL compatibility.
    """

    RECORD_QUERIES = {
        "highest_scoring_season": {
            "label": "Highest PPG Season",
            "query": """
                SELECT jogador AS player, equipa AS team,
                       REPLACE(season, 'Epoca', '') AS season,
                       ROUND(pontos, 1) AS value
                FROM player_stats
                WHERE jogos_jogados >= 50
                ORDER BY pontos DESC LIMIT 1
            """
        },
        "most_rebounds_season": {
            "label": "Most Rebounds Per Game",
            "query": """
                SELECT jogador AS player, equipa AS team,
                       REPLACE(season, 'Epoca', '') AS season,
                       ROUND(rebotes, 1) AS value
                FROM player_stats
                WHERE jogos_jogados >= 50
                ORDER BY rebotes DESC LIMIT 1
            """
        },
        "most_assists_season": {
            "label": "Most Assists Per Game",
            "query": """
                SELECT jogador AS player, equipa AS team,
                       REPLACE(season, 'Epoca', '') AS season,
                       ROUND(assistencias, 1) AS value
                FROM player_stats
                WHERE jogos_jogados >= 50
                ORDER BY assistencias DESC LIMIT 1
            """
        },
        "highest_fantasy_season": {
            "label": "Highest Fantasy Season",
            "query": """
                SELECT jogador AS player, equipa AS team,
                       REPLACE(season, 'Epoca', '') AS season,
                       ROUND(ponto_fantasia, 1) AS value
                FROM player_stats
                WHERE jogos_jogados >= 50
                ORDER BY ponto_fantasia DESC LIMIT 1
            """
        },
        "best_plus_minus_season": {
            "label": "Best Plus/Minus Season",
            "query": """
                SELECT jogador AS player, equipa AS team,
                       REPLACE(season, 'Epoca', '') AS season,
                       ROUND(mais_ou_menos, 1) AS value
                FROM player_stats
                WHERE jogos_jogados >= 50
                ORDER BY mais_ou_menos DESC LIMIT 1
            """
        },
        "best_fg_pct_season": {
            "label": "Best FG% Season (min 50 GP)",
            "query": """
                SELECT jogador AS player, equipa AS team,
                       REPLACE(season, 'Epoca', '') AS season,
                       ROUND(percentagem_de_meta_de_campo, 1) AS value
                FROM player_stats
                WHERE jogos_jogados >= 50
                  AND percentagem_de_meta_de_campo IS NOT NULL
                  AND percentagem_de_meta_de_campo > 0
                ORDER BY percentagem_de_meta_de_campo DESC LIMIT 1
            """
        },
        "most_3pm_season": {
            "label": "Most 3-Pointers Made Per Game",
            "query": """
                SELECT jogador AS player, equipa AS team,
                       REPLACE(season, 'Epoca', '') AS season,
                       ROUND(golos_de_campo_de_3_pontos_feitos, 1) AS value
                FROM player_stats
                WHERE jogos_jogados >= 50
                ORDER BY golos_de_campo_de_3_pontos_feitos DESC LIMIT 1
            """
        },
        "most_triple_doubles_season": {
            "label": "Most Triple-Doubles in a Season",
            "query": """
                SELECT jogador AS player, equipa AS team,
                       REPLACE(season, 'Epoca', '') AS season,
                       triplos_duplos AS value
                FROM player_stats
                WHERE jogos_jogados >= 50
                ORDER BY triplos_duplos DESC LIMIT 1
            """
        },
    }

    records = {}
    with get_connection() as conn:
        with conn.cursor() as cur:
            for record_key, config in RECORD_QUERIES.items():
                cur.execute(config["query"])
                row = cur.fetchone()
                if row:
                    records[record_key] = {
                        "player": row["player"],
                        "team": row["team"],
                        "season": row["season"],
                        "value": float(row["value"]) if row["value"] is not None else None,
                        "label": config["label"]
                    }

    return {
        "records": records,
        "total_records": len(records),
        "seasons_covered": 25,
        "description": "Single-season record holders across all 25 NBA seasons (1996-2021)"
    }