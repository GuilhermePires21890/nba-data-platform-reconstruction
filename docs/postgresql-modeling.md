# PostgreSQL Modeling Strategy

## Objective

Define the relational modeling strategy for the modern NBA Data Platform Reconstruction project.

The goal is to transform the consolidated historical NBA dataset into a scalable analytical relational structure.

---

# Modeling Principles

## Simplicity First

The initial modeling phase prioritizes:

- readability
- maintainability
- analytics readiness
- reproducibility

## Incremental Evolution

The project will evolve incrementally from:

- flat consolidated dataset
- canonical relational table
- analytical views
- future dimensional modeling

---

# Initial Canonical Table

## player_stats

The first analytical table will centralize historical player performance statistics.

| Column | Type |
|---|---|
| player_name | TEXT |
| season | TEXT |
| team | TEXT |
| games_played | INTEGER |
| points | NUMERIC |
| rebounds | NUMERIC |
| assists | NUMERIC |
| steals | NUMERIC |
| blocks | NUMERIC |
| plus_minus | NUMERIC |

---

# Modeling Goals

- support historical analytics
- simplify Power BI integration
- improve SQL maintainability
- support analytical queries
- create reusable analytical layers

---

# Future Evolution

Possible future improvements:

- dimensional modeling
- fact and dimension tables
- advanced metrics tables
- dbt transformations
- warehouse architecture
