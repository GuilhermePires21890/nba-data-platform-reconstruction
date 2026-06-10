# Security Audit

## Scope

This document records the security baseline and the implementation status of mitigations for the public NBA Data Platform API.

The platform serves public, read-only sports analytics data and does not process authentication data, payment data or personally identifiable information.

---

## Baseline Test Results

### TEST-001 - SQL Injection

**Vector:** Query parameter injection via season filter  
**Test:**

```bash
curl "https://nba-data-platform-api.onrender.com/players/?season='; DROP TABLE player_stats;--"
```

**Baseline result:** PASS  
**HTTP response:** 403 Forbidden  
**Notes:** Blocked by Cloudflare before reaching the application layer. Parameterized `psycopg2` queries provide application-level defence-in-depth.

---

### TEST-002 - Rate Limiting

**Vector:** High-volume requests from a single client  
**Baseline test:**

```bash
for i in {1..20}; do curl -s -o /dev/null -w "%{http_code} " \
https://nba-data-platform-api.onrender.com/health; done
```

**Baseline result:** FAIL  
**Baseline response:** 200 on all 20 consecutive requests  
**Mitigation implemented:** `slowapi` middleware with default and endpoint-specific limits of 30-60 requests per minute.  
**Current status:** Implemented - pending repeatable post-deployment regression evidence

---

### TEST-003 - Security Headers

**Vector:** Missing HTTP security headers  
**Baseline test:**

```bash
curl -I https://nba-data-platform-api.onrender.com/
```

**Baseline result:** PARTIAL  
**Baseline observation:** Application-level security headers were missing.  
**Mitigation implemented:** FastAPI middleware now adds:

- `X-Content-Type-Options`
- `X-Frame-Options`
- `X-XSS-Protection`
- `Strict-Transport-Security`
- `Referrer-Policy`
- `Permissions-Policy`

**Current status:** Implemented - pending repeatable post-deployment regression evidence

---

### TEST-004 - CORS Policy

**Vector:** Cross-origin request from an unauthorized domain  
**Baseline test:**

```bash
curl -H "Origin: https://malicious-site.com" \
     -I https://nba-data-platform-api.onrender.com/players/seasons
```

**Baseline result:** FAIL  
**Baseline response:** `access-control-allow-origin: *`  
**Mitigation implemented:** CORS restricted to the public frontend and approved local development origins. Allowed methods are restricted to `GET`.  
**Current status:** Implemented - pending repeatable post-deployment regression evidence

---

### TEST-005 - Oversized Request

**Vector:** Abnormal limit parameter  
**Test:**

```bash
curl "https://nba-data-platform-api.onrender.com/players/?limit=99999"
```

**Result:** PASS  
**HTTP response:** 422 Unprocessable Entity  
**Notes:** FastAPI/Pydantic validation rejects values above the endpoint maximum.

---

### TEST-006 - Path Traversal

**Vector:** Malformed endpoint paths  
**Test:**

```bash
curl "https://nba-data-platform-api.onrender.com/../../etc/passwd"
```

**Result:** PASS  
**HTTP response:** 404 Not Found  
**Notes:** Invalid routes are rejected and no filesystem operations are exposed by the API.

---

## Risk Register - Current Status

| Risk ID | Description | Severity | Control | Status |
|---|---|---|---|---|
| RISK-001 | Unrestricted request volume | Medium | `slowapi` rate limiting | Implemented |
| RISK-002 | Permissive CORS | Medium | Known origins and GET-only methods | Implemented |
| RISK-003 | Supabase RLS posture not formally validated | Medium | Validate exposure and apply read-only RLS where applicable | Open |
| RISK-004 | Missing application security headers | Low | FastAPI security-header middleware | Implemented |
| RISK-005 | SQL injection surface | Low | Cloudflare, Pydantic and parameterized queries | Mitigated |
| RISK-006 | Path traversal | Low | FastAPI route isolation | Mitigated |
| RISK-007 | Oversized requests | Low | Pydantic query limits | Mitigated |

---

## Audit Summary

| Category | Status |
|---|---|
| Baseline tests executed | 6 |
| Critical vulnerabilities | 0 |
| Application mitigations implemented | Rate limiting, restricted CORS and security headers |
| Remaining open risk | Supabase RLS posture validation |
| Regression evidence | Post-deployment retest recommended |

**Overall assessment:** The platform is suitable for public read-only portfolio use. No critical vulnerabilities were identified. The main baseline gaps were addressed in application code. A repeatable post-deployment security regression run should be added to provide evidence that the controls remain active in the deployed environment.

---

## Recommended Regression Commands

```bash
# Security headers
curl -I https://nba-data-platform-api.onrender.com/

# Unauthorized origin
curl -H "Origin: https://malicious-site.com" \
     -I https://nba-data-platform-api.onrender.com/players/seasons

# Rate limiting
for i in {1..70}; do
  curl -s -o /dev/null -w "%{http_code} " \
  https://nba-data-platform-api.onrender.com/players/seasons
done
```

Expected outcomes:

- Security headers are present in the API response
- Unauthorized origins do not receive an `Access-Control-Allow-Origin` response for their domain
- Requests above the configured threshold begin returning HTTP 429
