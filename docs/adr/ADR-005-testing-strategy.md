# ADR-005 - Testing Strategy

## Status
Accepted

---

## Context

The NBA Data Platform is a public-facing platform with:
- A REST API deployed on Render
- A PostgreSQL database hosted on Supabase
- A public frontend dashboard
- A CI/CD pipeline via GitHub Actions

As the platform became publicly available, a structured testing
strategy was required to ensure reliability, data integrity,
and API contract stability.

---

## Decision

Adopt a layered testing strategy covering four distinct areas:
data integrity, API contracts, pipeline transformations,
and performance baselines.

---

## Testing Layers

### Layer 1 - Data Integrity Tests
Validate the dataset loaded in PostgreSQL.

Checks:
- Total record count equals 11,460
- Exactly 25 distinct seasons present
- No negative points or rebounds values
- Percentages within valid range (0 to 1)
- Season format consistent (EpocaYYYY-YY)
- No games played equals zero with stats populated

### Layer 2 - API Contract Tests
Validate FastAPI endpoint behaviour.

Checks:
- GET /health returns 200
- GET /players/seasons returns non-empty list of 25 seasons
- GET /players/top-scorers returns correct number of results
- GET /players/top-scorers?season=X filters correctly
- GET /players/top-scorers?limit=100 respects maximum limit
- GET /players/ with invalid season returns graceful response
- Response time under 3 seconds for standard requests

### Layer 3 - Transformation Tests
Validate Python ETL pipeline logic.

Checks:
- Season extracted correctly from filename
- Column normalisation produces snake_case names
- Consolidation produces no duplicate records
- Schema validator raises error on missing required columns
- Encoding handles special characters in player names

### Layer 4 - Performance Baseline
Establish response time benchmarks.

Checks:
- /health endpoint under 500ms
- /players/seasons under 1000ms
- /players/top-scorers under 2000ms

---

## Tooling

| Tool | Purpose |
|---|---|
| pytest | Test runner |
| httpx | API contract testing |
| psycopg2 | Data integrity testing |
| pytest-cov | Coverage reporting |
| GitHub Actions | CI execution |

---

## Consequences

### Positive
- Regression protection on every push
- Data quality confidence
- API contract stability
- Portfolio demonstration of QA maturity

### Trade-offs
- Test maintenance overhead
- CI execution time increase
- Requires test database or fixtures

---

## Future Evolution
- Load testing with Locust
- Contract testing with Pact
- End-to-end testing with Playwright
- Mutation testing