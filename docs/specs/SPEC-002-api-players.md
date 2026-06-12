# SPEC-002 - API Players Endpoints

**Version:** 1.0.0
**Priority:** P0 - Critical
**Area:** API Layer
**Status:** ✅ Complete
**Last Updated:** June 2026

---

## Overview

This specification defines the functional behaviour and acceptance criteria
for the Players endpoints of the NBA Data Platform REST API.

The API is built with FastAPI, deployed on Render, and serves data from
PostgreSQL hosted on Supabase.

**Base URL:** https://nba-data-platform-api.onrender.com

---

## Background

```gherkin
Background:
  Given the NBA Data Platform API is deployed and running
  And the API base URL is https://nba-data-platform-api.onrender.com
  And the Supabase PostgreSQL database contains 11460 player records
  And the API responds within 90 seconds including cold start
```

---

## Feature: API Health and Root

```gherkin
Feature: API Health and Root
  As an API consumer
  I want to verify the API is operational before making data requests
  So that I can detect availability issues early

  Scenario: Health endpoint returns OK status
    When I send GET /health
    Then the response status should be 200
    And the response body should contain status equal to ok

  Scenario: Root endpoint returns platform metadata
    When I send GET /
    Then the response status should be 200
    And the response body should contain version
    And the response body should contain records equal to 11460

  Scenario: Health endpoint responds within 3 seconds when warm
    Given the API has already received at least one request
    When I send GET /health
    Then the response time should be less than 3 seconds
```

**Test Evidence:**

| Scenario | Result | Executed by |
|---|---|---|
| Health returns 200 | ✅ PASS | pytest - test_api_contracts.py |
| Health returns ok status | ✅ PASS | pytest - test_api_contracts.py |
| Response time under 3s when warm | ✅ PASS | pytest - test_api_contracts.py |
| Root returns 200 | ✅ PASS | pytest - test_api_contracts.py |
| Root contains version | ✅ PASS | pytest - test_api_contracts.py |
| Root contains records 11460 | ✅ PASS | pytest - test_api_contracts.py |

**Note:** First request to a cold Render free tier instance may take
50-90 seconds due to spin-up. Subsequent requests respond normally.

---

## Feature: Seasons Endpoint

```gherkin
Feature: Seasons Endpoint
  As an API consumer
  I want to retrieve the list of available seasons
  So that I can populate filters and understand dataset coverage

  Scenario: Seasons endpoint returns 200
    When I send GET /players/seasons
    Then the response status should be 200

  Scenario: Seasons endpoint returns exactly 25 seasons
    When I send GET /players/seasons
    Then the response body seasons array should contain exactly 25 items

  Scenario: First season is present in response
    When I send GET /players/seasons
    Then the seasons array should contain Epoca1996-97

  Scenario: Last season is present in response
    When I send GET /players/seasons
    Then the seasons array should contain Epoca2020-21
```

**Test Evidence:**

| Scenario | Result | Executed by |
|---|---|---|
| Seasons returns 200 | ✅ PASS | pytest - test_api_contracts.py |
| Returns exactly 25 seasons | ✅ PASS | pytest - test_api_contracts.py |
| Contains Epoca1996-97 | ✅ PASS | pytest - test_api_contracts.py |
| Contains Epoca2020-21 | ✅ PASS | pytest - test_api_contracts.py |

---

## Feature: Teams Endpoint

```gherkin
Feature: Teams Endpoint
  As an API consumer
  I want to retrieve the list of available teams
  So that I can populate team filters in client applications

  Scenario: Teams endpoint returns 200
    When I send GET /players/teams
    Then the response status should be 200

  Scenario: Teams endpoint returns non-empty list
    When I send GET /players/teams
    Then the teams array should contain at least one item

  Scenario: Known team is present in response
    When I send GET /players/teams
    Then the teams array should contain LAL
```

**Test Evidence:**

| Scenario | Result | Executed by |
|---|---|---|
| Teams returns 200 | ✅ PASS | pytest - test_api_contracts.py |
| Returns non-empty list | ✅ PASS | pytest - test_api_contracts.py |
| Contains LAL | ✅ PASS | pytest - test_api_contracts.py |

---

## Feature: Top Scorers Endpoint

```gherkin
Feature: Top Scorers Endpoint
  As an API consumer
  I want to retrieve the top scoring players
  So that I can display historical scoring leaders in client applications

  Background:
    Given the top-scorers endpoint filters players with
    at least 50 games played

  Scenario: Top scorers returns 200
    When I send GET /players/top-scorers
    Then the response status should be 200

  Scenario: Default limit returns 10 players
    When I send GET /players/top-scorers with no parameters
    Then the response count should be 10

  Scenario: Custom limit is respected
    When I send GET /players/top-scorers?limit=25
    Then the response count should be 25

  Scenario: Maximum limit is enforced at 50
    When I send GET /players/top-scorers?limit=99999
    Then the response status should be 422
    And the response should indicate the limit must be
    less than or equal to 50

  Scenario: Season filter returns only matching records
    When I send GET /players/top-scorers?season=Epoca2020-21
    Then all records in the response should have
    season equal to Epoca2020-21

  Scenario: Response contains expected statistical fields
    When I send GET /players/top-scorers?limit=1
    Then the response data should contain jogador
    And the response data should contain equipa
    And the response data should contain season
    And the response data should contain pontos
    And the response data should contain assistencias
    And the response data should contain rebotes

  Scenario: Invalid season returns empty result gracefully
    When I send GET /players/top-scorers?season=InvalidSeason
    Then the response status should be 200
    And the response count should be 0
```

**Test Evidence:**

| Scenario | Result | Executed by |
|---|---|---|
| Returns 200 | ✅ PASS | pytest - test_api_contracts.py |
| Default limit 10 | ✅ PASS | pytest - test_api_contracts.py |
| Custom limit 25 | ✅ PASS | pytest - test_api_contracts.py |
| Max limit 422 for 99999 | ✅ PASS | pytest - test_api_contracts.py |
| Season filter correct | ✅ PASS | pytest - test_api_contracts.py |
| Expected fields present | ✅ PASS | pytest - test_api_contracts.py |
| Invalid season returns empty | ✅ PASS | pytest - test_api_contracts.py |

---

## Feature: Players List Endpoint

```gherkin
Feature: Players List Endpoint
  As an API consumer
  I want to retrieve a paginated list of players
  So that I can browse the full dataset with filtering options

  Scenario: Players endpoint returns 200
    When I send GET /players/
    Then the response status should be 200

  Scenario: Default limit is 20 records
    When I send GET /players/ with no parameters
    Then the response count should be 20

  Scenario: Maximum limit is enforced at 100
    When I send GET /players/?limit=99999
    Then the response status should be 422

  Scenario: Season filter is applied correctly
    When I send GET /players/?season=Epoca2020-21
    Then all returned records should have
    season equal to Epoca2020-21

  Scenario: Team filter is applied correctly
    When I send GET /players/?team=LAL
    Then all returned records should have equipa equal to LAL

  Scenario: Offset pagination works correctly
    Given GET /players/?limit=10 returns players A through J
    When I send GET /players/?limit=10&offset=10
    Then the response should not contain players A through J
```

**Test Evidence:**

| Scenario | Result | Note |
|---|---|---|
| Returns 200 | ✅ PASS | Manual validation |
| Default limit 20 | ✅ PASS | Manual validation |
| Max limit 422 | ✅ PASS | Pydantic validation |
| Season filter | ✅ PASS | Manual validation |
| Team filter | ✅ PASS | Manual validation |
| Offset pagination | ✅ PASS | Manual validation |

---

## API Contract Reference

| Endpoint | Method | Auth | Rate Limit |
|---|---|---|---|
| /health | GET | None | 60/min |
| / | GET | None | 60/min |
| /players/ | GET | None | 60/min |
| /players/seasons | GET | None | 30/min |
| /players/teams | GET | None | 30/min |
| /players/top-scorers | GET | None | 30/min |

---

## Known Limitations

| Limitation | Impact | Mitigation |
|---|---|---|
| Free tier cold start 50-90s | First request may timeout | CI warm-up step implemented |
| No authentication | Any client can query | Read-only data - acceptable for public platform |
| Rate limiting may affect CI | Test failures on rapid sequential requests | time.sleep(2) added between tests |