# ADR-003 - Docker for Reproducible Environments

## Status
Accepted

---

## Context

The original project had no containerisation - it depended on
local SQL Server and R installations, making it impossible to
reproduce without manual environment setup.

The reconstruction required a reproducible, portable development
environment accessible to any contributor.

---

## Decision

Adopt Docker Compose as the standard for local development
environment orchestration.

---

## Rationale

- Eliminates "works on my machine" problems
- PostgreSQL and Metabase run consistently across all environments
- Single command startup: docker compose up -d
- Aligns with cloud-native deployment practices
- Demonstrates infrastructure thinking in portfolio

---

## Services Orchestrated

| Service | Image | Purpose |
|---|---|---|
| nba_postgres | postgres:16 | Primary analytical database |
| nba_metabase | metabase/metabase:latest | BI and dashboard layer |

---

## Consequences

### Positive
- Fully reproducible local environment
- Consistent PostgreSQL version across dev and CI
- Simple onboarding for new contributors
- Foundation for future cloud migration

### Trade-offs
- Docker Desktop required on developer machine
- Memory overhead for local development
- Volume management complexity

---

## Future Evolution
- Docker multi-stage builds for API image
- docker-compose.prod.yml for production configuration
- Container registry for versioned images