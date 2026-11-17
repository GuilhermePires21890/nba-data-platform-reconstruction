-- Load the consolidated player-season dataset into player_stats.
--
-- The CSV uses porcentagem_ for two percentage columns, while the schema and the
-- rest of the project use percentagem_. A staging table keeps the CSV names so the
-- COPY matches the file header exactly, and the INSERT maps them to the schema names.
-- The whole load runs in one transaction, so a bad file leaves player_stats unchanged.
--
-- Usage: replace the FROM path with the real file path on the database server, or
-- use psql's \copy from a client machine with the same column list.

BEGIN;

CREATE TEMP TABLE player_stats_staging (LIKE player_stats INCLUDING DEFAULTS) ON COMMIT DROP;
ALTER TABLE player_stats_staging RENAME COLUMN percentagem_de_meta_de_campo TO porcentagem_de_meta_de_campo;
ALTER TABLE player_stats_staging RENAME COLUMN percentagem_de_lances_livres TO porcentagem_de_lances_livres;

COPY player_stats_staging (
    jogador, equipa, idade, jogos_jogados, vitorias, derrotas,
    minutos_jogador, pontos, metas_de_campo_feitas, tentativas_de_metas_de_campo,
    porcentagem_de_meta_de_campo, golos_de_campo_de_3_pontos_feitos,
    tentativa_de_gol_de_campo_de_3_pontos, porcentagem_de_gols_de_campo_de_3_pontos,
    lancamentos_livres_realizados, tentativa_de_lances_livres, porcentagem_de_lances_livres,
    rebotes_ofensivos, rebotes_defensivos, rebotes, assistencias, faturamentos,
    roubos, bloqueio, faltas_pessoais, ponto_fantasia, duplos_duplos, triplos_duplos,
    mais_ou_menos, season
)
FROM '/path/to/player_stats_consolidated.csv'
WITH (FORMAT csv, HEADER true, DELIMITER ',');

-- Positional mapping: staging columns are in the same order as the schema.
INSERT INTO player_stats (
    jogador, equipa, idade, jogos_jogados, vitorias, derrotas,
    minutos_jogador, pontos, metas_de_campo_feitas, tentativas_de_metas_de_campo,
    percentagem_de_meta_de_campo, golos_de_campo_de_3_pontos_feitos,
    tentativa_de_gol_de_campo_de_3_pontos, porcentagem_de_gols_de_campo_de_3_pontos,
    lancamentos_livres_realizados, tentativa_de_lances_livres, percentagem_de_lances_livres,
    rebotes_ofensivos, rebotes_defensivos, rebotes, assistencias, faturamentos,
    roubos, bloqueio, faltas_pessoais, ponto_fantasia, duplos_duplos, triplos_duplos,
    mais_ou_menos, season
)
SELECT
    jogador, equipa, idade, jogos_jogados, vitorias, derrotas,
    minutos_jogador, pontos, metas_de_campo_feitas, tentativas_de_metas_de_campo,
    porcentagem_de_meta_de_campo, golos_de_campo_de_3_pontos_feitos,
    tentativa_de_gol_de_campo_de_3_pontos, porcentagem_de_gols_de_campo_de_3_pontos,
    lancamentos_livres_realizados, tentativa_de_lances_livres, porcentagem_de_lances_livres,
    rebotes_ofensivos, rebotes_defensivos, rebotes, assistencias, faturamentos,
    roubos, bloqueio, faltas_pessoais, ponto_fantasia, duplos_duplos, triplos_duplos,
    mais_ou_menos, season
FROM player_stats_staging;

COMMIT;
