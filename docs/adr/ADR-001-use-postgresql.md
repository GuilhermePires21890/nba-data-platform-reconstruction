# ADR-001 - Use PostgreSQL as the Primary Relational Database

## Status

Accepted

---

# Context

The original academic project relied on local SQL Server-oriented scripts and CSV-based storage.

The reconstruction project requires a modern relational database capable of supporting:

- analytical workloads
- reproducible local development
- containerized environments
- modern SQL practices
- portfolio-friendly architecture

---

# Decision

The reconstruction project will adopt PostgreSQL as the primary relational database.

---

# Rationale

## Open-source ecosystem

PostgreSQL provides a strong open-source ecosystem suitable for personal and portfolio projects.

## Strong analytical capabilities

PostgreSQL supports:

- advanced SQL
- aggregations
- analytical queries
- views
- indexing

## Docker compatibility

PostgreSQL integrates cleanly with Docker-based local environments.

## Industry relevance

PostgreSQL is widely adopted in:

- Data Engineering
- Analytics
- SaaS platforms
- cloud-native architectures

---

# Consequences

## Positive

- Modern SQL environment
- Easier reproducibility
- Better GitHub portfolio positioning
- Improved scalability potential

## Trade-offs

- Migration effort from legacy SQL scripts
- Potential syntax adjustments
- Need for schema redesign

---

# Future Evolution

Possible future additions:

- dbt
- warehouse modeling
- cloud-managed PostgreSQL
- orchestration pipelines
