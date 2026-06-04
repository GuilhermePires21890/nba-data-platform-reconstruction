# ADR-004 - Metabase for BI and Dashboards

## Status
Accepted

---

## Context

The original project used R and ggplot2 for statistical
visualisation - isolated scripts with no interactive capability
and no shareable dashboards.

The reconstruction required a BI layer capable of providing
interactive analytics on top of the PostgreSQL database,
without requiring custom frontend development at this stage.

---

## Decision

Adopt Metabase as the BI and dashboard layer, running as a
Docker service connected to the PostgreSQL database.

---

## Rationale

- Open-source with strong free tier
- Direct PostgreSQL integration
- No-code dashboard creation for rapid analytics delivery
- SQL question support for advanced queries
- Docker-compatible deployment
- Portfolio-friendly visual output (screenshots for README)

---

## Dashboards Delivered

| Dashboard | Insight |
|---|---|
| Top 10 Historical Scorers | LeBron James leads 25-season aggregate |
| Top 10 All-Time Assist Leaders | Chris Paul #1 all-time |
| Top 10 All-Time Rebound Leaders | Dwight Howard leads big men era |
| Top 10 Fantasy Points Leaders | LeBron dominates multi-stat |
| 3-Point Revolution | Trend analysis 1996-2021 |
| Young Stars U25 | Best under-25 seasons all-time |
| Championship Predictor | Model accuracy backtested 25 seasons |

---

## Consequences

### Positive
- Rapid dashboard delivery without frontend development
- Live data from PostgreSQL
- Exportable screenshots for portfolio
- SQL question layer demonstrates analytical thinking

### Trade-offs
- Local only - not publicly accessible without cloud deployment
- Replaced by public frontend (Sprint 11) for public visibility
- Sleep limitations on free cloud hosting

---

## Relationship to Sprint 11

Metabase serves as the internal analytics layer.
The public frontend (Sprint 11) exposes key insights
via the FastAPI layer to any user without login.

---

## Future Evolution
- Metabase Cloud for public dashboard sharing
- Embedded analytics in frontend
- Additional dashboards: era comparison, team evolution