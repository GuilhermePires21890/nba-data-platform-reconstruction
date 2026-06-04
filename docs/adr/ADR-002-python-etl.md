# ADR-002 - Python for Ingestion and Transformation

## Status
Accepted

---

## Context

The original academic project used C# for web scraping and R for
statistical analysis. The reconstruction required a modern language
capable of handling both data ingestion and transformation within
a single, maintainable codebase.

---

## Decision

Adopt Python as the primary language for all ingestion and
transformation layers.

---

## Rationale

- Industry standard for Data Engineering pipelines
- Pandas provides powerful DataFrame-based transformations
- Strong ecosystem: psycopg2, SQLAlchemy, FastAPI, pytest
- Unified language across pipeline, API and tests
- Portfolio relevance for Data Engineering roles

---

## Consequences

### Positive
- Single language across all layers
- Rich library ecosystem
- Easier onboarding and maintenance
- Strong CI/CD integration

### Trade-offs
- Migration effort from original C# codebase
- Performance ceiling vs compiled languages for large scale

---

## Future Evolution
- dbt for transformation layer
- Apache Airflow or Prefect for orchestration
- Polars as Pandas replacement at scale