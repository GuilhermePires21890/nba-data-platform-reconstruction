-- Per-game averages for each player-season, built on the production schema.
-- Output aliases follow the English names used by sql/analytics/top_scorers.sql.
CREATE OR REPLACE VIEW player_performance_view AS
SELECT
    jogador                                             AS player_name,
    season,
    equipa                                              AS team,
    jogos_jogados                                       AS games_played,
    pontos                                              AS points,
    rebotes                                             AS rebounds,
    assistencias                                        AS assists,
    roubos                                              AS steals,
    bloqueio                                            AS blocks,
    mais_ou_menos                                       AS plus_minus,
    ROUND(pontos / NULLIF(jogos_jogados, 0), 2)         AS avg_points_per_game,
    ROUND(rebotes / NULLIF(jogos_jogados, 0), 2)        AS avg_rebounds_per_game,
    ROUND(assistencias / NULLIF(jogos_jogados, 0), 2)   AS avg_assists_per_game
FROM player_stats;
