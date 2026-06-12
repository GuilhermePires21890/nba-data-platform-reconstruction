# SPEC-005 - 3-Point Revolution Trend Analysis

**Version:** 1.0.0
**Priority:** P2 - Medium
**Area:** Analytics - Trend Analysis
**Status:** ✅ Complete
**Last Updated:** June 2026

---

## Overview

This specification defines the behaviour and acceptance criteria for the
3-Point Revolution trend analysis feature of the NBA Data Platform.

The analysis tracks the evolution of 3-point shooting across 25 NBA seasons
(1996-97 to 2020-21), revealing one of the most significant tactical shifts
in professional basketball history - the transition from a post-centric game
to a perimeter-dominated, analytics-driven playing style.

---

## Historical Context

The 3-point revolution is widely attributed to the Golden State Warriors
dynasty and the influence of Steph Curry from approximately 2015 onwards.
The data in this platform provides quantitative evidence of this shift
across the entire dataset period.

**Key data points:**
- 1996-97: avg 3PM per player = 0.56
- 2015-16: avg 3PM per player = 0.75
- 2018-19: avg 3PM per player = 1.01 (first season above 1.0)
- 2020-21: avg 3PM per player = 1.15 (dataset maximum)
- Total increase 1996 to 2021: +105%

---

## Background

```gherkin
Background:
  Given the 3-point revolution endpoint is available at
  /analytics/3point-revolution
  And the analysis includes all players with at least 20 games played
  And data covers 25 consecutive seasons from 1996-97 to 2020-21
  And results are ordered chronologically ascending by season
```

---

## Feature: Trend Data Completeness

```gherkin
Feature: 3-Point Revolution Trend Data Completeness
  As a data analyst
  I want the trend data to cover all 25 seasons completely
  So that the visualisation shows an uninterrupted historical timeline

  Scenario: Endpoint returns 200
    When I send GET /analytics/3point-revolution
    Then the response status should be 200

  Scenario: All 25 seasons are present
    When I send GET /analytics/3point-revolution
    Then the response data array should contain exactly 25 items

  Scenario: Data begins with the first season
    When I send GET /analytics/3point-revolution
    Then the first record should have season equal to Epoca1996-97

  Scenario: Data ends with the last season
    When I send GET /analytics/3point-revolution
    Then the last record should have season equal to Epoca2020-21

  Scenario: All records contain required fields
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
| 25 seasons present | ✅ PASS | count: 25 confirmed |
| Starts with 1996-97 | ✅ PASS | First record: Epoca1996-97 |
| Ends with 2020-21 | ✅ PASS | Last record: Epoca2020-21 |
| All fields present | ✅ PASS | All fields confirmed in response |

---

## Feature: Trend Direction Validation

```gherkin
Feature: 3-Point Revolution Trend Direction
  As a sports analyst
  I want to verify the trend shows a clear upward trajectory
  So that the data confirms the known historical narrative

  Scenario: Modern era average exceeds Jordan era average
    Given the Jordan era spanned seasons 1996-97 to 2000-01
    And the modern era spanned seasons 2016-17 to 2020-21
    When avg_3pm values are compared across eras
    Then the modern era average should be more than double
    the Jordan era average

  Scenario: 2018-19 season exceeds 1.0 average 3PM
    Given this was the first season the league average surpassed 1.0
    When I retrieve the record for season Epoca2018-19
    Then avg_3pm should be greater than or equal to 1.0

  Scenario: 2020-21 represents the dataset maximum
    Given this is the final season in the dataset
    When avg_3pm values are compared across all seasons
    Then Epoca2020-21 should have one of the three highest avg_3pm values
    in the entire dataset

  Scenario: Pre-2012 seasons are all below 0.70 average
    Given the 3-point revolution had not yet begun before 2012
    When I review seasons from Epoca1996-97 to Epoca2011-12
    Then all avg_3pm values should be below 0.70

  Scenario: Acceleration is visible after 2015-16
    Given the Warriors dynasty began winning championships from 2015
    When avg_3pm for Epoca2015-16 is compared to Epoca2019-20
    Then Epoca2019-20 avg_3pm should be at least 30 percent higher
```

**Test Evidence:**

| Scenario | Result | Evidence |
|---|---|---|
| Modern era double Jordan era | ✅ PASS | Modern avg ~1.0 vs Jordan avg ~0.46 - 117% increase |
| 2018-19 exceeds 1.0 | ✅ PASS | Epoca2018-19 avg_3pm: 1.01 |
| 2020-21 is dataset maximum | ✅ PASS | Epoca2020-21: 1.15 - highest value |
| Pre-2012 below 0.70 | ✅ PASS | Maximum pre-2012 was 0.65 in 2012-13 |
| Post-2015 acceleration | ✅ PASS | 2015-16: 0.75 vs 2019-20: 1.11 - 48% increase |

---

## Feature: Shooting Efficiency Analysis

```gherkin
Feature: 3-Point Shooting Efficiency Tracking
  As a basketball analyst
  I want to track not just volume but efficiency of 3-point shooting
  So that I can understand if more attempts led to better or worse accuracy

  Scenario: League 3-point percentage is tracked per season
    When I send GET /analytics/3point-revolution
    Then each record should contain league_3p_pct
    And all values should be between 25 and 50

  Scenario: Attempts increased proportionally with makes
    Given more makes logically requires more attempts
    When avg_3pm and avg_3pa values are compared
    Then avg_3pa should always be greater than avg_3pm
    for every season in the dataset

  Scenario: 1996-97 shooting percentage is available
    When I retrieve the record for season Epoca1996-97
    Then league_3p_pct should be 35.6

  Scenario: Total players per season is tracked
    When I send GET /analytics/3point-revolution
    Then each record should contain total_players
    And all values should be greater than 300
```

**Test Evidence:**

| Scenario | Result | Evidence |
|---|---|---|
| 3P% between 25 and 50 | ✅ PASS | All values in range 33-40% |
| Attempts exceed makes | ✅ PASS | All seasons: avg_3pa > avg_3pm |
| 1996-97 percentage 35.6 | ✅ PASS | Confirmed in response |
| Total players above 300 | ✅ PASS | All seasons above 300 players |

---

## Full Dataset Reference

| Season | avg_3pm | avg_3pa | league_3p_pct |
|---|---|---|---|
| Epoca1996-97 | 0.56 | 1.57 | 35.6 |
| Epoca1997-98 | 0.41 | 1.18 | 34.5 |
| Epoca1998-99 | 0.43 | 1.27 | 33.9 |
| Epoca1999-00 | 0.44 | 1.25 | 35.1 |
| Epoca2000-01 | 0.44 | 1.26 | 34.9 |
| Epoca2001-02 | 0.47 | 1.37 | 34.3 |
| Epoca2002-03 | 0.47 | 1.38 | 34.1 |
| Epoca2003-04 | 0.49 | 1.44 | 34.0 |
| Epoca2004-05 | 0.52 | 1.52 | 34.2 |
| Epoca2005-06 | 0.51 | 1.50 | 34.0 |
| Epoca2006-07 | 0.56 | 1.63 | 34.4 |
| Epoca2007-08 | 0.59 | 1.74 | 33.9 |
| Epoca2008-09 | 0.62 | 1.83 | 33.9 |
| Epoca2009-10 | 0.60 | 1.77 | 33.9 |
| Epoca2010-11 | 0.59 | 1.75 | 33.7 |
| Epoca2011-12 | 0.59 | 1.76 | 33.6 |
| Epoca2012-13 | 0.65 | 1.93 | 33.7 |
| Epoca2013-14 | 0.68 | 2.01 | 33.8 |
| Epoca2014-15 | 0.72 | 2.11 | 34.1 |
| Epoca2015-16 | 0.75 | 2.18 | 34.4 |
| Epoca2016-17 | 0.86 | 2.48 | 34.7 |
| Epoca2017-18 | 0.95 | 2.73 | 34.8 |
| Epoca2018-19 | 1.01 | 2.89 | 35.0 |
| Epoca2019-20 | 1.11 | 3.13 | 35.5 |
| Epoca2020-21 | 1.15 | 3.25 | 35.4 |

---

## Known Limitations

| Limitation | Impact | Mitigation |
|---|---|---|
| Per-player averages not per-game | Players with few games included if above 20 threshold | Minimum games filter applied |
| No positional breakdown | Guards vs forwards 3PT not separated | Future enhancement |
| League expansion not normalised | More teams in later seasons affects totals | Per-player metric used instead of totals |
| No individual star impact analysis | Steph Curry specific contribution not isolated | Era analysis provides proxy |