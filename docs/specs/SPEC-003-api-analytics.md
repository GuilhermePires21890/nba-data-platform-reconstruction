# SPEC-003 - API Analytics Endpoints

**Version:** 1.0.0
**Priority:** P1 - High
**Area:** API Layer - Analytics
**Status:** ✅ Complete
**Last Updated:** June 2026

---

## Overview

This specification defines the functional behaviour and acceptance criteria
for the Analytics endpoints of the NBA Data Platform REST API.

Analytics endpoints expose pre-computed insights derived from advanced SQL
queries against the historical dataset. These endpoints power the public
frontend dashboard and demonstrate analytical thinking beyond basic CRUD.

**Base URL:** https://nba-data-platform-api.onrender.com/analytics

---

## Background

```gherkin
Background:
  Given the NBA Data Platform API is deployed and running
  And the analytics router is registered at /analytics prefix
  And all endpoints require minimum 20 games played for statistical validity
  And rate limiting is set to 30 requests per minute per client
```

---

## Feature: Era Analysis Endpoint

```gherkin
Feature: Era Analysis Endpoint
  As a sports data analyst
  I want to retrieve aggregated statistics grouped by historical era
  So that I can understand how the NBA game evolved over 25 seasons

  Scenario: Era analysis returns 200
    When I send GET /analytics/era-analysis
    Then the response status should be 200

  Scenario: Era analysis returns exactly 5 eras
    When I send GET /analytics/era-analysis
    Then the response data array should contain exactly 5 items

  Scenario: All expected eras are present
    When I send GET /analytics/era-analysis
    Then the data should contain era 1996-2001 Jordan Era
    And the data should contain era 2001-2006 Post-Jordan
    And the data should contain era 2006-2011 LeBron Rise
    And the data should contain era 2011-2016 Heat and Warriors
    And the data should contain era 2016-2021 Modern Era

  Scenario: Modern era shows highest 3-point average
    Given the 3-point revolution accelerated after 2016
    When I send GET /analytics/era-analysis
    Then the 2016-2021 Modern Era avg_3pm should be greater than
    the 1996-2001 Jordan Era avg_3pm

  Scenario: Response contains required analytical fields
    When I send GET /analytics/era-analysis
    Then each era record should contain era
    And each era record should contain total_player_seasons
    And each era record should contain avg_points
    And each era record should contain avg_assists
    And each era record should contain avg_rebounds
    And each era record should contain avg_3pm
    And each era record should contain avg_fantasy
    And each era record should contain total_triple_doubles
```

**Test Evidence:**

| Scenario | Result | Evidence |
|---|---|---|
| Returns 200 | ✅ PASS | curl response HTTP 200 |
| Returns 5 eras | ✅ PASS | count: 5 in response |
| All 5 eras present | ✅ PASS | All era names confirmed in response |
| Modern era highest 3PM | ✅ PASS | Modern Era avg_3pm: 1.02 vs Jordan Era: 0.46 |
| Required fields present | ✅ PASS | All fields confirmed in response |

**Data Insight:** The Modern Era (2016-2021) shows avg_3pm of 1.02 compared
to 0.46 in the Jordan Era - a 121% increase confirming the 3-point revolution.

---

## Feature: 3-Point Revolution Endpoint

```gherkin
Feature: 3-Point Revolution Trend Endpoint
  As a sports historian
  I want to retrieve season-by-season 3-point shooting trends
  So that I can visualise the evolution of the 3-point game over 25 seasons

  Scenario: 3-point revolution returns 200
    When I send GET /analytics/3point-revolution
    Then the response status should be 200

  Scenario: Returns data for all 25 seasons
    When I send GET /analytics/3point-revolution
    Then the response data array should contain exactly 25 items

  Scenario: Data is ordered chronologically
    When I send GET /analytics/3point-revolution
    Then the first record should have season Epoca1996-97
    And the last record should have season Epoca2020-21

  Scenario: Post-2018 seasons exceed 1.0 average 3PM
    Given Steph Curry and the Warriors changed 3-point culture after 2015
    When I send GET /analytics/3point-revolution
    Then seasons from Epoca2018-19 onwards should have avg_3pm
    greater than or equal to 1.0

  Scenario: Response contains shooting efficiency fields
    When I send GET /analytics/3point-revolution
    Then each record should contain season
    And each record should contain avg_3pm
    And each record should contain avg_3pa
    And each record should contain league_3p_pct
    And each record should contain total_players
```

**Test Evidence:**

| Scenario | Result | Evidence |
|---|---|---|
| Returns 200 | ✅ PASS | curl response HTTP 200 |
| 25 seasons returned | ✅ PASS | count: 25 confirmed |
| Chronological order | ✅ PASS | First: Epoca1996-97, Last: Epoca2020-21 |
| Post-2018 above 1.0 | ✅ PASS | 2018-19: 1.01, 2019-20: 1.11, 2020-21: 1.15 |
| All fields present | ✅ PASS | All fields confirmed in response |

---

## Feature: Young Stars Endpoint

```gherkin
Feature: Young Stars Endpoint
  As a talent scout analyst
  I want to retrieve the best performing players aged 25 or under
  So that I can identify historically exceptional young seasons

  Background:
    Given the young-stars endpoint filters players with
    age less than or equal to 25 and at least 50 games played

  Scenario: Young stars returns 200
    When I send GET /analytics/young-stars
    Then the response status should be 200

  Scenario: Default limit returns 25 players
    When I send GET /analytics/young-stars
    Then the response count should be 25

  Scenario: All returned players are aged 25 or under
    When I send GET /analytics/young-stars
    Then all records should have idade less than or equal to 25

  Scenario: Results ordered by fantasy points descending
    When I send GET /analytics/young-stars
    Then the first record should have a higher fantasy_points
    than the last record

  Scenario: Giannis Antetokounmpo appears in top results
    Given Giannis had exceptional young seasons with Milwaukee
    When I send GET /analytics/young-stars?limit=5
    Then the top 5 should include Giannis Antetokounmpo

  Scenario: Season filter returns only matching records
    When I send GET /analytics/young-stars?season=Epoca2020-21
    Then all records should have season equal to Epoca2020-21
```

**Test Evidence:**

| Scenario | Result | Evidence |
|---|---|---|
| Returns 200 | ✅ PASS | curl response HTTP 200 |
| Default limit 25 | ✅ PASS | count: 25 confirmed |
| All players aged 25 or under | ✅ PASS | All records validated manually |
| Ordered by fantasy DESC | ✅ PASS | Giannis 56.6 > LeBron 55.8 > ... |
| Giannis in top 5 | ✅ PASS | Giannis #1 (56.6) and #2 (56.2) |
| Season filter works | ✅ PASS | Manual validation confirmed |

---

## Feature: Championship Predictor Endpoint

```gherkin
Feature: Championship Predictor Endpoint
  As a sports analyst
  I want to retrieve team championship scores for any season
  So that I can evaluate which teams the model predicts as contenders

  Background:
    Given the championship score is calculated as a weighted composite:
    35% plus-minus + 25% fantasy + 20% points + 10% assists + 10% rebounds

  Scenario: Championship predictor returns 200
    When I send GET /analytics/championship-predictor
    Then the response status should be 200

  Scenario: Season filter returns teams for that season only
    When I send GET /analytics/championship-predictor?season=Epoca2020-21
    Then all records should have season equal to Epoca2020-21

  Scenario: Results are ordered by predicted rank ascending
    When I send GET /analytics/championship-predictor?season=Epoca2020-21
    Then the first record should have predicted_rank equal to 1

  Scenario: Response contains scoring methodology fields
    When I send GET /analytics/championship-predictor?season=Epoca2020-21
    Then each record should contain championship_score
    And each record should contain predicted_rank
    And each record should contain avg_plus_minus
    And each record should contain avg_fantasy

  Scenario: Predicted rank 1 has highest championship score
    When I send GET /analytics/championship-predictor?season=Epoca2020-21
    Then the record with predicted_rank 1 should have the
    highest championship_score in the response
```

**Test Evidence:**

| Scenario | Result | Evidence |
|---|---|---|
| Returns 200 | ✅ PASS | curl response HTTP 200 |
| Season filter works | ✅ PASS | All 2020-21 records returned |
| Ordered by rank ASC | ✅ PASS | BKN rank 1, POR rank 2, LAC rank 3 |
| Required fields present | ✅ PASS | All fields confirmed |
| Rank 1 has highest score | ✅ PASS | BKN score 9.644 is highest |

---

## Feature: Player Career Endpoint

```gherkin
Feature: Player Career Endpoint
  As a sports data consumer
  I want to retrieve the complete career statistics for a named player
  So that I can analyse their performance evolution across seasons

  Scenario: Career endpoint returns 200 for known player
    When I send GET /analytics/players/LeBron James/career
    Then the response status should be 200

  Scenario: Career data includes player name in response
    When I send GET /analytics/players/LeBron James/career
    Then the response should contain player equal to LeBron James

  Scenario: Career data includes seasons played count
    When I send GET /analytics/players/LeBron James/career
    Then the response should contain seasons_played
    And seasons_played should be greater than 0

  Scenario: LeBron James has 18 seasons in dataset
    Given LeBron James entered the NBA in 2003
    And the dataset covers seasons up to 2020-21
    When I send GET /analytics/players/LeBron James/career
    Then seasons_played should be 18

  Scenario: Career data is ordered chronologically
    When I send GET /analytics/players/LeBron James/career
    Then the first record should have season Epoca2003-04
    And the last record should have season Epoca2020-21

  Scenario: Unknown player returns empty result gracefully
    When I send GET /analytics/players/Unknown Player XYZ/career
    Then the response status should be 200
    And the response count should be 0
    And the response data array should be empty
```

**Test Evidence:**

| Scenario | Result | Evidence |
|---|---|---|
| Returns 200 for LeBron | ✅ PASS | curl response HTTP 200 |
| Player name in response | ✅ PASS | player: LeBron James confirmed |
| seasons_played present | ✅ PASS | seasons_played: 18 |
| LeBron has 18 seasons | ✅ PASS | 18 records returned |
| Chronological order | ✅ PASS | First: Epoca2003-04 confirmed |
| Unknown player graceful | ✅ PASS | Returns empty data array |

---

## API Contract Reference

| Endpoint | Method | Parameters | Rate Limit |
|---|---|---|---|
| /analytics/era-analysis | GET | none | 30/min |
| /analytics/3point-revolution | GET | none | 30/min |
| /analytics/young-stars | GET | season, limit (max 50) | 30/min |
| /analytics/championship-predictor | GET | season, limit (max 30) | 30/min |
| /analytics/players/{name}/career | GET | player_name (path) | 30/min |

---

## Known Limitations

| Limitation | Impact | Mitigation |
|---|---|---|
| Player names are case-sensitive | LeBron James vs lebron james | Document in API docs |
| Spaces in player names require URL encoding | LeBron%20James | Handled by httpx and browsers |
| Championship model uses regular season data only | Playoffs not reflected | Documented in SPEC-004 |
| Young stars limited to players with 50+ games | Part-season injuries excluded | Documented threshold |