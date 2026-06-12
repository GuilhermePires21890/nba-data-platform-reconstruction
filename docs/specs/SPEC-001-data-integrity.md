# SPEC-001 - Data Integrity and Quality

**Version:** 1.0.0
**Priority:** P0 - Critical
**Area:** Data Layer
**Status:** ✅ Complete
**Last Updated:** June 2026

---

## Overview

This specification defines the data integrity and quality requirements
for the NBA Data Platform historical dataset.

The dataset contains 11,460 player-season records spanning 25 NBA seasons
from 1996-97 to 2020-21, sourced from the original academic web scraping
project and loaded into PostgreSQL via the Python ETL pipeline.

---

## Background

```gherkin
Background:
  Given the NBA Data Platform database is running on PostgreSQL 16
  And the player_stats table has been populated via the ETL pipeline
  And the database is accessible at the configured connection endpoint
```

---

## Feature: Dataset Volume Integrity

```gherkin
Feature: Dataset Volume Integrity
  As a data consumer
  I want to verify the dataset contains the expected volume of records
  So that I can trust the completeness of the historical data

  Background:
    Given the player_stats table exists in the database
    And the ETL pipeline has completed successfully

  Scenario: Total record count matches expected value
    Given the player_stats table has been fully loaded
    When I count all records in player_stats
    Then the total count should be exactly 11460

  Scenario: Exactly 25 distinct seasons are present
    Given the player_stats table has been fully loaded
    When I count distinct values in the season column
    Then the count should be exactly 25

  Scenario: First season is present
    Given the player_stats table has been fully loaded
    When I query for records with season equal to Epoca1996-97
    Then at least one record should be returned

  Scenario: Last season is present
    Given the player_stats table has been fully loaded
    When I query for records with season equal to Epoca2020-21
    Then at least one record should be returned
```

**Test Evidence:**

| Scenario | Result | Executed by |
|---|---|---|
| Total record count equals 11460 | ✅ PASS - COUNT returned 11460 | pytest - test_data_integrity.py |
| Exactly 25 distinct seasons | ✅ PASS - COUNT DISTINCT returned 25 | pytest - test_data_integrity.py |
| First season Epoca1996-97 exists | ✅ PASS - 433 records found | pytest - test_data_integrity.py |
| Last season Epoca2020-21 exists | ✅ PASS - 529 records found | pytest - test_data_integrity.py |

---

## Feature: Data Quality Validation

```gherkin
Feature: Data Quality Validation
  As a data analyst
  I want all statistical values to be within valid ranges
  So that analytics built on this data produce accurate insights

  Background:
    Given the player_stats table is populated with 11460 records

  Scenario: No negative points values exist
    When I query for records where pontos is less than 0
    Then the count should be 0

  Scenario: No negative rebounds values exist
    When I query for records where rebotes is less than 0
    Then the count should be 0

  Scenario: No negative assists values exist
    When I query for records where assistencias is less than 0
    Then the count should be 0

  Scenario: Field goal percentage within valid range
    Given percentages are stored on a 0 to 100 scale
    When I query for records where percentagem_de_meta_de_campo
    is less than 0 or greater than 100
    Then the count should be 0

  Scenario Outline: No null values in critical columns
    When I query for records where <column> is NULL
    Then the count should be 0

    Examples:
      | column     |
      | jogador    |
      | equipa     |
      | season     |
```

**Test Evidence:**

| Scenario | Result | Note |
|---|---|---|
| No negative points | ✅ PASS | 0 records returned |
| No negative rebounds | ✅ PASS | 0 records returned |
| No negative assists | ✅ PASS | 0 records returned |
| FG percentage in range 0-100 | ✅ PASS | Percentages stored as 0-100 scale, not 0-1 |
| No null player names | ✅ PASS | 0 null records |
| No null teams | ✅ PASS | 0 null records |
| No null seasons | ✅ PASS | 0 null records |

**Data Discovery Note:**
During initial test execution, percentages were found to be stored
on a 0-100 scale (e.g. 44.7) rather than a 0-1 scale (e.g. 0.447).
This is consistent with the original academic project format.
Test was updated to reflect this validated behaviour.

---

## Feature: Season Format Consistency

```gherkin
Feature: Season Format Consistency
  As a developer integrating with the API
  I want season identifiers to follow a consistent format
  So that filtering and display logic works predictably

  Background:
    Given the player_stats table contains 25 seasons of data

  Scenario: All seasons follow the Epoca pattern
    When I query for records where season does NOT match
    the pattern Epoca followed by 4 digits, hyphen, 2 digits
    Then the count should be 0

  Scenario: Known player exists across multiple seasons
    Given LeBron James played in the NBA from 2003 onwards
    When I query for records where jogador equals LeBron James
    Then at least 10 records should be returned
```

**Test Evidence:**

| Scenario | Result | Note |
|---|---|---|
| Season format consistent | ✅ PASS | 0 non-conforming records |
| LeBron James records exist | ✅ PASS | 18 season records found |

---

## Feature: ETL Pipeline Transformation

```gherkin
Feature: ETL Pipeline Transformation
  As a data engineer
  I want the ETL pipeline to correctly transform source CSV files
  So that data loaded into PostgreSQL is clean and consistent

  Background:
    Given the Python ETL pipeline is configured
    And source CSV files are present in data/raw/legacy_csv

  Scenario: Season extracted correctly from filename
    Given a CSV file named 1996-97.csv
    When extract_season_from_filename is called
    Then the result should be 1996-97
    And the result should not contain .csv

  Scenario: Column names are normalised to lowercase
    Given a DataFrame with columns Player, Team, Points
    When normalize_columns is called
    Then all column names should be lowercase
    And column names should be player, team, points

  Scenario: Column names with spaces become underscores
    Given a DataFrame with columns player name, team name
    When normalize_columns is called
    Then column names should be player_name and team_name

  Scenario: Whitespace is stripped from column names
    Given a DataFrame with columns " player " and " team "
    When normalize_columns is called
    Then column names should be player and team

  Scenario: Schema validation passes for valid columns
    Given the required columns are
    player_name, team, points, rebounds, assists
    When validate_required_columns is called
    Then the result should be True

  Scenario: Schema validation raises error for missing columns
    Given only player_name, team, points are provided
    When validate_required_columns is called
    Then a ValueError should be raised
    And the message should contain Missing required columns

  Scenario: Schema validation raises error for empty column list
    Given an empty list of columns is provided
    When validate_required_columns is called
    Then a ValueError should be raised
```

**Test Evidence:**

| Scenario | Result | Executed by |
|---|---|---|
| Season extraction from filename | ✅ PASS | pytest - test_transformation.py |
| CSV extension removed | ✅ PASS | pytest - test_transformation.py |
| Underscore format handled | ✅ PASS | pytest - test_transformation.py |
| Columns lowercased | ✅ PASS | pytest - test_transformation.py |
| Spaces replaced with underscores | ✅ PASS | pytest - test_transformation.py |
| Whitespace stripped | ✅ PASS | pytest - test_transformation.py |
| Valid schema passes | ✅ PASS | pytest - test_transformation.py |
| Missing columns raises error | ✅ PASS | pytest - test_transformation.py |
| Empty columns raises error | ✅ PASS | pytest - test_transformation.py |

---

## Automated Test Coverage

File: tests/test_data_integrity.py
Scenarios covered: 13
Pass rate: 13/13 (100%)
Execution time: ~1s (local Supabase connection)
Note: Requires live database connection - not run in CI

File: tests/test_transformation.py
Scenarios covered: 9
Pass rate: 9/9 (100%)
Execution time: ~5s
Note: Runs in CI on every push to main

---

## Known Limitations

| Limitation | Impact | Mitigation |
|---|---|---|
| Data integrity tests require live DB | Cannot run in CI without credentials | Tests run locally against Supabase |
| Percentages stored as 0-100 not 0-1 | Potential confusion for API consumers | Documented in data dictionary |
| No unique constraint on player+season | Theoretical duplicates possible | ETL pipeline validates on load |