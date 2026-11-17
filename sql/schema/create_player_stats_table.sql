-- ============================================================
-- NBA Data Platform Reconstruction
-- Production schema for the player_stats table
--
-- One row per player and season. Columns follow the consolidated dataset header
-- (player_stats_consolidated.csv). Names are kept in
-- Portuguese, as in the original dataset, because the API, the analytics
-- queries and the data-integrity tests use them. Season labels follow the
-- 'EpocaYYYY-YY' convention (for example 'Epoca2020-21').
-- ============================================================

CREATE TABLE IF NOT EXISTS player_stats (
    jogador                                 TEXT,
    equipa                                  TEXT,
    idade                                   INTEGER,
    jogos_jogados                           INTEGER,
    vitorias                                INTEGER,
    derrotas                                INTEGER,
    minutos_jogador                         NUMERIC,
    pontos                                  NUMERIC,
    metas_de_campo_feitas                   NUMERIC,
    tentativas_de_metas_de_campo            NUMERIC,
    percentagem_de_meta_de_campo            NUMERIC,
    golos_de_campo_de_3_pontos_feitos       NUMERIC,
    tentativa_de_gol_de_campo_de_3_pontos   NUMERIC,
    porcentagem_de_gols_de_campo_de_3_pontos NUMERIC,
    lancamentos_livres_realizados           NUMERIC,
    tentativa_de_lances_livres              NUMERIC,
    percentagem_de_lances_livres            NUMERIC,
    rebotes_ofensivos                       NUMERIC,
    rebotes_defensivos                      NUMERIC,
    rebotes                                 NUMERIC,
    assistencias                            NUMERIC,
    faturamentos                            NUMERIC,
    roubos                                  NUMERIC,
    bloqueio                                NUMERIC,
    faltas_pessoais                         NUMERIC,
    ponto_fantasia                          NUMERIC,
    duplos_duplos                           INTEGER,
    triplos_duplos                          INTEGER,
    mais_ou_menos                           NUMERIC,
    season                                  TEXT
);
