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

A security audit was conducted to identify risks and define mitigations appropriate for a portfolio-grade public platform serving read-only sports analytics data.

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

### RISK-001 - Unrestricted Request Volume

**Severity:** Medium  
**Risk:** Abuse, resource exhaustion or denial of service through unlimited requests.  
**Mitigation:** `slowapi` rate limiting middleware with default and endpoint-specific thresholds.  
**Status:** Implemented

### RISK-002 - Permissive CORS Policy

**Severity:** Medium  
**Risk:** Any external domain could consume the API directly from a browser.  
**Mitigation:** CORS restricted to the public frontend and approved local development origins. HTTP methods restricted to `GET`.  
**Status:** Implemented

### RISK-003 - Supabase RLS Disabled

**Severity:** Medium  
**Risk:** Direct Supabase API access could bypass the FastAPI layer if public database APIs are exposed.  
**Mitigation:** Validate Supabase exposure and enable an explicit read-only RLS policy where applicable.  
**Status:** Planned

### RISK-004 - Missing Security Headers

**Severity:** Low  
**Risk:** Clickjacking, MIME sniffing and unnecessary browser capability exposure.  
**Mitigation:** FastAPI middleware adds content-type protection, frame protection, HSTS, referrer policy and permissions policy.  
**Status:** Implemented

### RISK-005 - SQL Injection Surface

**Severity:** Low  
**Risk:** Malformed query parameters reaching database queries.  
**Mitigation:** Parameterized queries through `psycopg2`, input validation through FastAPI/Pydantic and edge filtering through Cloudflare.  
**Status:** Verified - Mitigated

### RISK-006 - Path Traversal

**Severity:** Low  
**Risk:** Malformed routes attempting to access local filesystem paths.  
**Mitigation:** FastAPI routing rejects invalid paths and the service does not expose filesystem operations.  
**Status:** Verified - Mitigated

### RISK-007 - Oversized Query Requests

**Severity:** Low  
**Risk:** Abnormally high result limits causing unnecessary database or API load.  
**Mitigation:** Pydantic validation enforces endpoint limits.  
**Status:** Verified - Mitigated

---

## Security Principles Adopted

1. Read-only public API with no write endpoints exposed
2. No authentication data stored or processed
3. No personally identifiable information in the dataset
4. Secrets managed through Render environment variables
5. No secrets committed to version control
6. Least-privilege exposure between frontend, API and database
7. Layered controls across edge, application and database access

---

## Implemented Application Controls

| Control | Implementation |
|---|---|
| Rate limiting | `slowapi`, 30-60 requests per minute depending on endpoint |
| CORS | Restricted origins and `GET`-only methods |
| Query safety | Parameterized `psycopg2` queries |
| Request validation | FastAPI and Pydantic limits |
| Security headers | Custom FastAPI middleware |
| Secret management | Render environment variables |
| Edge protection | Cloudflare and Render infrastructure |

---

## Consequences

### Positive

- Reduced API abuse surface
- Documented security ownership and risk awareness
- Defence-in-depth across edge and application layers
- Stronger portfolio evidence of production engineering maturity

### Trade-offs

- Rate limiting introduces state and operational considerations
- Restricted CORS requires explicit origin management
- Security controls and dependencies require maintenance
- Supabase RLS posture still requires explicit validation

---

## Future Evolution

- Validate and document Supabase RLS configuration
- Add dependency vulnerability scanning with Dependabot
- Add automated SAST and dependency checks to CI
- Run repeatable post-deployment security regression tests
- Evaluate API key authentication if higher-tier or write capabilities are introduced
- Perform an OWASP API Security Top 10 assessment
