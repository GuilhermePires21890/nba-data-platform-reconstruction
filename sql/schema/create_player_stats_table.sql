-- ============================================================
-- NBA Data Platform Reconstruction
-- Production schema for the player_stats table
--
-- One row per player and season. Column names are kept in Portuguese,
-- as in the original dataset, because the API, the analytics queries and
-- the data-integrity tests all use them. Season labels follow the
-- 'EpocaYYYY-YY' convention (for example 'Epoca2020-21').
-- ============================================================

CREATE TABLE IF NOT EXISTS player_stats (
    jogador                                 TEXT,
    equipa                                  TEXT,
    season                                  TEXT,
    idade                                   INTEGER,
    jogos_jogados                           INTEGER,
    minutos_jogador                         NUMERIC,
    pontos                                  NUMERIC,
    assistencias                            NUMERIC,
    rebotes                                 NUMERIC,
    roubos                                  NUMERIC,
    bloqueio                                NUMERIC,
    ponto_fantasia                          NUMERIC,
    triplos_duplos                          INTEGER,
    mais_ou_menos                           NUMERIC,
    percentagem_de_meta_de_campo            NUMERIC,
    percentagem_de_lances_livres            NUMERIC,
    golos_de_campo_de_3_pontos_feitos       NUMERIC,
    tentativa_de_gol_de_campo_de_3_pontos   NUMERIC
);
