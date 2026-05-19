# Dataset Consolidation Strategy

## Objective

Define the canonical consolidation strategy for the historical NBA datasets.

The original academic project stored one CSV file per season.

The modernization process aims to consolidate all historical datasets into a unified analytical model.

---

# Strategic Goals

- Create a canonical dataset structure
- Standardize seasons and naming
- Improve analytical consistency
- Support PostgreSQL ingestion
- Enable scalable analytics workflows

---

# Current Legacy Structure

## Legacy Pattern

One CSV file per season:

- 1996_1997.csv
- 1997_1998.csv
- 1998_1999.csv
- etc.

---

# Target Canonical Structure

## Target Dataset

```text
player_stats_consolidated.csv
```

---

# Canonical Schema

| Column | Type | Description |
|---|---|---|
| player_name | TEXT | NBA player name |
| season | TEXT | NBA season |
| team | TEXT | Team abbreviation |
| games_played | INTEGER | Total games played |
| points | NUMERIC | Total points |
| rebounds | NUMERIC | Total rebounds |
| assists | NUMERIC | Total assists |
| steals | NUMERIC | Total steals |
| blocks | NUMERIC | Total blocks |
| plus_minus | NUMERIC | Plus/minus metric |

---

# Normalization Rules

## Season Normalization

Example:

```text
1996_1997.csv
→ 1996-1997
```

## Naming Standards

- lowercase column names
- snake_case naming
- standardized team abbreviations

---

# Validation Rules

## Required Checks

- mandatory season column
- consistent schema
- numeric validation
- duplicate detection
- null checks

---

# Output Strategy

## Processed Output

```text
/data/processed/player_stats_consolidated.csv
```

---

# Future Evolution

Possible future improvements:

- parquet support
- incremental ingestion
- PostgreSQL direct loading
- dimensional modeling
- data lineage tracking
