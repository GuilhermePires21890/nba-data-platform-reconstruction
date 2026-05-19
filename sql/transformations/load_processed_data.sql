-- Example PostgreSQL loading strategy

COPY player_stats (
    player_name,
    season,
    team,
    games_played,
    points,
    rebounds,
    assists,
    steals,
    blocks,
    plus_minus
)
FROM '/data/processed/player_stats_consolidated.csv'
DELIMITER ','
CSV HEADER;
