# Legacy Assets Inventory

## Objective

This document inventories the original academic project assets preserved during the reconstruction process.

The goal is to:

- preserve historical context
- support technical archaeology
- document modernization opportunities
- separate legacy and modern assets

---

# Legacy Assets Identified

## Historical NBA CSV Datasets

| Asset Type | Description |
|---|---|
| CSV datasets | Historical NBA player statistics by season |
| Seasons covered | 1996/1997 to 2020/2021 |
| Structure | One CSV file per season |

### Observations

- Consistent column structure across seasons
- Good candidate for dataset consolidation
- Strong potential for historical analytics

---

# SQL Assets

| Asset Type | Description |
|---|---|
| SQL scripts | Data transformations and analytics queries |
| SQL style | Legacy SQL Server oriented |
| Main operations | ALTER COLUMN, aggregations, rankings |

### Observations

- Significant repetition detected
- Opportunity for modular SQL redesign
- Potential PostgreSQL migration candidate

---

# Statistical Analysis Assets

| Asset Type | Description |
|---|---|
| R scripts | Statistical analysis and visualizations |
| Libraries | ggplot2 and base R |

### Observations

- Demonstrates analytical mindset
- Useful historical analytical reference
- Candidate for notebook migration

---

# Documentation Assets

| Asset Type | Description |
|---|---|
| Academic report | Original project explanation |
| Screenshots | Evidence of execution and outputs |

### Observations

- Valuable for reconstruction context
- Important for portfolio storytelling

---

# Modernization Opportunities

| Legacy Area | Modernization Direction |
|---|---|
| CSV per season | Consolidated canonical dataset |
| SQL repetition | Modular SQL layer |
| R scripts | Python notebooks |
| Local execution | Dockerized environment |
| Monolithic flow | Layered architecture |
