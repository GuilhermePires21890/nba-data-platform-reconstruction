# Data Dictionary

## Objective

This document will centralize the business and technical definition of the NBA historical datasets.

The goal is to improve:

- data understanding
- analytical consistency
- maintainability
- onboarding
- documentation quality

---

# Planned Dataset Structure

## Player Statistics Dataset

| Column | Description | Type | Notes |
|---|---|---|---|
| player_name | NBA player name | TEXT | Standardized naming |
| season | NBA season | TEXT | Example: 2020-2021 |
| team | Team abbreviation | TEXT | Standardized team codes |
| games_played | Total games played | INTEGER | |
| points | Total points | NUMERIC | |
| assists | Total assists | NUMERIC | |
| rebounds | Total rebounds | NUMERIC | |
| steals | Total steals | NUMERIC | |
| blocks | Total blocks | NUMERIC | |
| plus_minus | Plus/minus metric | NUMERIC | |

---

# Future Improvements

- Metadata versioning
- Validation rules
- Data lineage
- Quality metrics
- Dimensional modeling
