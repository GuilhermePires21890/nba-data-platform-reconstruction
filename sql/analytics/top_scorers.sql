SELECT
    player_name,
    season,
    team,
    points,
    avg_points_per_game
FROM player_performance_view
ORDER BY points DESC
LIMIT 25;
