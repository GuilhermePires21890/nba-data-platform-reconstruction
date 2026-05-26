# ADR-006 - Security Strategy

## Status
Accepted

---

## Context

The NBA Data Platform is publicly accessible via:
- REST API at nba-data-platform-api.onrender.com
- Frontend at nba-data-platform.onrender.com
- PostgreSQL database at Supabase (cloud-managed)
- Source code at GitHub (public repository)

A security audit was conducted to identify risks and
define mitigations appropriate for a portfolio-grade
public platform serving read-only sports analytics data.

---

## Threat Model

| Asset | Exposure | Risk Level |
|---|---|---|
| REST API | Public internet | Medium |
| PostgreSQL DB | Supabase cloud | Medium |
| Frontend | Public static site | Low |
| Source code | Public GitHub | Low |
| Environment variables | Render secrets | Low |

---

## Identified Risks and Mitigations

### RISK-001 - No Rate Limiting
**Severity:** Medium
**Description:** API accepts unlimited requests per client.
**Risk:** Abuse, resource exhaustion, denial of service.
**Mitigation:** Implement slowapi rate limiting middleware.
**Status:** Planned

### RISK-002 - Permissive CORS Policy
**Severity:** Medium
**Description:** CORS configured with allow_origins=["*"].
**Risk:** Any domain can consume the API.
**Mitigation:** Restrict to nba-data-platform.onrender.com.
**Status:** Planned

### RISK-003 - Supabase RLS Disabled
**Severity:** Medium
**Description:** Row Level Security not enabled on player_stats.
**Risk:** Direct Supabase API access bypasses FastAPI layer.
**Mitigation:** Enable read-only RLS policy on player_stats table.
**Status:** Planned

### RISK-004 - Missing Security Headers
**Severity:** Low
**Description:** API responses lack security headers.
**Risk:** Clickjacking, MIME sniffing, information disclosure.
**Mitigation:** Add security headers middleware to FastAPI.
**Status:** Planned

### RISK-005 - SQL Injection Surface
**Severity:** Low
**Description:** Query parameters passed to SQL queries.
**Risk:** Potential SQL injection via malformed parameters.
**Mitigation:** psycopg2 parameterised queries already in use.
Verified via penetration testing.
**Status:** Verified - Mitigated

---

## Security Principles Adopted

1. Read-only API - no write endpoints exposed
2. No authentication data stored or processed
3. No PII in dataset - only public sports statistics
4. Secrets managed via Render environment variables
5. No secrets in version control

---

## Consequences

### Positive
- Documented risk awareness
- Structured mitigation roadmap
- Portfolio demonstration of security thinking

### Trade-offs
- Rate limiting adds latency overhead
- Restricted CORS requires frontend URL management

---

## Future Evolution
- OWASP Top 10 assessment
- Dependency vulnerability scanning (Dependabot)
- API key authentication for higher-tier access
- Automated security scanning in CI pipeline