-- ============================================================
-- NBA Data Platform Reconstruction
-- Advanced Analytics SQL Layer
-- Sprint 7 - SQL Analytics
-- ============================================================


-- ============================================================
-- QUERY 1 - Offensive Efficiency Index
-- Players with best scoring efficiency (points per minute)
-- Minimum 50 games and 10 minutes per game filter
-- ============================================================

SELECT
    jogador,
    equipa,
    season,
    jogos_jogados,
    ROUND(pontos, 1)                                                        AS total_points,
    ROUND(minutos_jogador, 1)                                               AS total_minutes,
    ROUND(pontos / NULLIF(minutos_jogador, 0), 4)                          AS points_per_minute,
    ROUND(percentagem_de_meta_de_campo * 100, 1)                           AS fg_percentage,
    ROUND(percentagem_de_lances_livres * 100, 1)                           AS ft_percentage
FROM player_stats
WHERE jogos_jogados >= 50
  AND minutos_jogador > 0
  AND ROUND(minutos_jogador / NULLIF(jogos_jogados, 0), 1) >= 10
ORDER BY points_per_minute DESC
LIMIT 25;


-- ============================================================
-- QUERY 2 - Triple-Double Dominance by Era
-- Which era produced the most triple-doubles?
-- Groups seasons into historical eras
-- ============================================================

SELECT
    CASE
        WHEN season IN ('Epoca1996-97','Epoca1997-98','Epoca1998-99','Epoca1999-00','Epoca2000-01') THEN '1996–2001 Jordan Era'
        WHEN season IN ('Epoca2001-02','Epoca2002-03','Epoca2003-04','Epoca2004-05','Epoca2005-06') THEN '2001–2006 Post-Jordan'
        WHEN season IN ('Epoca2006-07','Epoca2007-08','Epoca2008-09','Epoca2009-10','Epoca2010-11') THEN '2006–2011 LeBron Rise'
        WHEN season IN ('Epoca2011-12','Epoca2012-13','Epoca2013-14','Epoca2014-15','Epoca2015-16') THEN '2011–2016 Heat & Warriors'
        WHEN season IN ('Epoca2016-17','Epoca2017-18','Epoca2018-19','Epoca2019-20','Epoca2020-21') THEN '2016–2021 Modern Era'
    END                                     AS era,
    COUNT(*)                                AS total_player_seasons,
    SUM(triplos_duplos)                     AS total_triple_doubles,
    ROUND(AVG(triplos_duplos), 2)           AS avg_triple_doubles_per_player,
    MAX(triplos_duplos)                     AS max_triple_doubles_single_season
FROM player_stats
WHERE jogos_jogados >= 50
GROUP BY era
ORDER BY total_triple_doubles DESC;


-- ============================================================
-- QUERY 3 - All-Time Player Consistency Score
-- Players who maintained high performance across multiple seasons
-- Consistency = seasons above their own career average
-- ============================================================

WITH career_stats AS (
    SELECT
        jogador,
        COUNT(*)                            AS total_seasons,
        ROUND(AVG(pontos), 2)               AS career_avg_points,
        ROUND(AVG(assistencias), 2)         AS career_avg_assists,
        ROUND(AVG(rebotes), 2)              AS career_avg_rebounds,
        ROUND(AVG(ponto_fantasia), 2)       AS career_avg_fantasy,
        ROUND(MAX(pontos), 2)               AS best_scoring_season,
        ROUND(MIN(pontos), 2)               AS worst_scoring_season
    FROM player_stats
    WHERE jogos_jogados >= 50
    GROUP BY jogador
    HAVING COUNT(*) >= 8
)
SELECT
    jogador,
    total_seasons,
    career_avg_points,
    career_avg_assists,
    career_avg_rebounds,
    career_avg_fantasy,
    best_scoring_season,
    worst_scoring_season,
    ROUND(best_scoring_season - worst_scoring_season, 2) AS scoring_variance
FROM career_stats
ORDER BY career_avg_fantasy DESC
LIMIT 20;


-- ============================================================
-- QUERY 4 - 3-Point Revolution Analysis
-- Evolution of 3-point shooting across 25 seasons
-- Shows the shift in NBA playing style over time
-- ============================================================

SELECT
    season,
    COUNT(*)                                                                    AS total_players,
    ROUND(SUM(golos_de_campo_de_3_pontos_feitos), 0)                           AS total_3pm_season,
    ROUND(AVG(golos_de_campo_de_3_pontos_feitos), 2)                           AS avg_3pm_per_player,
    ROUND(AVG(tentativa_de_gol_de_campo_de_3_pontos), 2)                       AS avg_3pa_per_player,
    ROUND(
        SUM(golos_de_campo_de_3_pontos_feitos) /
        NULLIF(SUM(tentativa_de_gol_de_campo_de_3_pontos), 0) * 100
    , 1)                                                                        AS league_3p_percentage
FROM player_stats
WHERE jogos_jogados >= 20
GROUP BY season
ORDER BY season ASC;


-- ============================================================
-- QUERY 5 - Win Correlation Analysis
-- Which individual stats correlate most with team wins?
-- Aggregates player contributions by team and season
-- ============================================================

SELECT
    equipa,
    season,
    MAX(vitorias)                                   AS team_wins,
    MAX(derrotas)                                   AS team_losses,
    ROUND(AVG(pontos), 2)                           AS avg_points_roster,
    ROUND(AVG(assistencias), 2)                     AS avg_assists_roster,
    ROUND(AVG(rebotes), 2)                          AS avg_rebounds_roster,
    ROUND(AVG(roubos), 2)                           AS avg_steals_roster,
    ROUND(AVG(bloqueio), 2)                         AS avg_blocks_roster,
    ROUND(AVG(mais_ou_menos), 2)                    AS avg_plus_minus_roster,
    ROUND(AVG(ponto_fantasia), 2)                   AS avg_fantasy_roster
FROM player_stats
WHERE jogos_jogados >= 20
GROUP BY equipa, season
ORDER BY team_wins DESC
LIMIT 30;


-- ============================================================
-- QUERY 6 - Young Stars Identification
-- Best performing players under 25 years old
-- Identifies breakout seasons by young talent
-- ============================================================

SELECT
    jogador,
    equipa,
    season,
    idade,
    jogos_jogados,
    ROUND(pontos, 1)                                AS points,
    ROUND(assistencias, 1)                          AS assists,
    ROUND(rebotes, 1)                               AS rebounds,
    ROUND(ponto_fantasia, 1)                        AS fantasy_points,
    ROUND(percentagem_de_meta_de_campo * 100, 1)   AS fg_pct,
    triplos_duplos
FROM player_stats
WHERE idade <= 25
  AND jogos_jogados >= 50
ORDER BY ponto_fantasia DESC
LIMIT 25;
