-- Migration 001: bring an existing player_stats table up to the full 30-column schema.
--
-- Use this when player_stats already exists in a database created with an earlier
-- version of sql/schema/create_player_stats_table.sql. CREATE TABLE IF NOT EXISTS does
-- not add columns to an existing table, so this script adds the missing ones.
--
-- Safe to run more than once (every statement uses IF NOT EXISTS). Existing columns
-- and their data are not changed. Column types match the schema file.
-- Runs in one transaction.

BEGIN;

ALTER TABLE player_stats ADD COLUMN IF NOT EXISTS jogador TEXT;
ALTER TABLE player_stats ADD COLUMN IF NOT EXISTS equipa TEXT;
ALTER TABLE player_stats ADD COLUMN IF NOT EXISTS idade INTEGER;
ALTER TABLE player_stats ADD COLUMN IF NOT EXISTS jogos_jogados INTEGER;
ALTER TABLE player_stats ADD COLUMN IF NOT EXISTS vitorias INTEGER;
ALTER TABLE player_stats ADD COLUMN IF NOT EXISTS derrotas INTEGER;
ALTER TABLE player_stats ADD COLUMN IF NOT EXISTS minutos_jogador NUMERIC;
ALTER TABLE player_stats ADD COLUMN IF NOT EXISTS pontos NUMERIC;
ALTER TABLE player_stats ADD COLUMN IF NOT EXISTS metas_de_campo_feitas NUMERIC;
ALTER TABLE player_stats ADD COLUMN IF NOT EXISTS tentativas_de_metas_de_campo NUMERIC;
ALTER TABLE player_stats ADD COLUMN IF NOT EXISTS percentagem_de_meta_de_campo NUMERIC;
ALTER TABLE player_stats ADD COLUMN IF NOT EXISTS golos_de_campo_de_3_pontos_feitos NUMERIC;
ALTER TABLE player_stats ADD COLUMN IF NOT EXISTS tentativa_de_gol_de_campo_de_3_pontos NUMERIC;
ALTER TABLE player_stats ADD COLUMN IF NOT EXISTS porcentagem_de_gols_de_campo_de_3_pontos NUMERIC;
ALTER TABLE player_stats ADD COLUMN IF NOT EXISTS lancamentos_livres_realizados NUMERIC;
ALTER TABLE player_stats ADD COLUMN IF NOT EXISTS tentativa_de_lances_livres NUMERIC;
ALTER TABLE player_stats ADD COLUMN IF NOT EXISTS percentagem_de_lances_livres NUMERIC;
ALTER TABLE player_stats ADD COLUMN IF NOT EXISTS rebotes_ofensivos NUMERIC;
ALTER TABLE player_stats ADD COLUMN IF NOT EXISTS rebotes_defensivos NUMERIC;
ALTER TABLE player_stats ADD COLUMN IF NOT EXISTS rebotes NUMERIC;
ALTER TABLE player_stats ADD COLUMN IF NOT EXISTS assistencias NUMERIC;
ALTER TABLE player_stats ADD COLUMN IF NOT EXISTS faturamentos NUMERIC;
ALTER TABLE player_stats ADD COLUMN IF NOT EXISTS roubos NUMERIC;
ALTER TABLE player_stats ADD COLUMN IF NOT EXISTS bloqueio NUMERIC;
ALTER TABLE player_stats ADD COLUMN IF NOT EXISTS faltas_pessoais NUMERIC;
ALTER TABLE player_stats ADD COLUMN IF NOT EXISTS ponto_fantasia NUMERIC;
ALTER TABLE player_stats ADD COLUMN IF NOT EXISTS duplos_duplos INTEGER;
ALTER TABLE player_stats ADD COLUMN IF NOT EXISTS triplos_duplos INTEGER;
ALTER TABLE player_stats ADD COLUMN IF NOT EXISTS mais_ou_menos NUMERIC;
ALTER TABLE player_stats ADD COLUMN IF NOT EXISTS season TEXT;

COMMIT;
