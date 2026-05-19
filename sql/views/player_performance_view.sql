CREATE OR REPLACE VIEW player_performance_view AS
SELECT
    player_name,
    season,
    team,
    games_played,
    points,
    rebounds,
    assists,
    steals,
    blocks,
    plus_minus,
    ROUND(points / NULLIF(games_played, 0), 2) AS avg_points_per_game,
    ROUND(rebounds / NULLIF(games_played, 0), 2) AS avg_rebounds_per_game,
    ROUND(assists / NULLIF(games_played, 0), 2) AS avg_assists_per_game
FROM player_stats;
