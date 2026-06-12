# SPEC-007 - Public Frontend Dashboard

**Version:** 1.0.0
**Priority:** P2 - Medium
**Area:** Frontend
**Status:** ✅ Complete
**Last Updated:** June 2026

---

## Overview

This specification defines the functional behaviour and acceptance criteria
for the NBA Data Platform public frontend dashboard.

The frontend is a single-page HTML application served as a static site
on Render, consuming data from the FastAPI REST layer. It provides
public access to the key analytical insights of the platform without
requiring any local installation or authentication.

**URL:** https://nba-data-platform.onrender.com

---

## Technical Architecture

| Component | Technology | Notes |
|---|---|---|
| Hosting | Render Static Site | Global CDN - no cold start |
| Framework | Vanilla HTML + CSS + JavaScript | No build step required |
| Charts | Chart.js 4.4.1 | Line and bar charts |
| Typography | Google Fonts - Bebas Neue, Fraunces, DM Mono | Editorial design |
| Data source | NBA Data Platform REST API | Live data via fetch() |
| Design direction | Dark editorial sports analytics | ESPN meets Vercel aesthetic |

---

## Background

```gherkin
Background:
  Given the NBA Data Platform frontend is deployed at
  https://nba-data-platform.onrender.com
  And the frontend consumes data from the REST API at
  https://nba-data-platform-api.onrender.com
  And the page is accessible without authentication
  And all data is loaded asynchronously on page load
```

---

## Feature: Page Availability and Loading

```gherkin
Feature: Frontend Page Availability
  As a public user
  I want to access the NBA Data Platform dashboard from any browser
  So that I can explore historical NBA analytics without installation

  Scenario: Dashboard loads successfully
    When I navigate to https://nba-data-platform.onrender.com
    Then the response status should be 200
    And the page title should contain NBA Data Platform

  Scenario: Page renders in dark theme
    When the dashboard loads
    Then the background should be dark
    And the accent colour should be orange
    And the typography should use Bebas Neue for headings

  Scenario: Header is visible on page load
    When the dashboard loads
    Then the header should display NBA DATA PLATFORM
    And the header should show API LIVE indicator
    And the header should show API DOCS link

  Scenario: All main sections are present
    When the dashboard loads
    Then the page should contain a hero section with platform statistics
    And the page should contain a Platform Overview section
    And the page should contain a Scoring Leaders section
    And the page should contain a 3-Point Revolution section
    And the page should contain a footer with stack information
```

**Test Evidence:**

| Scenario | Result | Evidence |
|---|---|---|
| Dashboard loads 200 | ✅ PASS | Browser navigation confirmed |
| Dark theme renders | ✅ PASS | Visual inspection - dark background #080a0f |
| Header visible | ✅ PASS | Logo, API LIVE dot, API DOCS button confirmed |
| All sections present | ✅ PASS | Visual inspection of all sections |

---

## Feature: Hero Section

```gherkin
Feature: Hero Section Statistics Display
  As a first-time visitor
  I want to immediately see the scale of the dataset
  So that I understand the depth of the platform

  Scenario: Hero displays correct record count
    When the dashboard loads
    Then the hero section should display 11,460 as player records

  Scenario: Hero displays correct season count
    When the dashboard loads
    Then the hero section should display 25 as the number of seasons

  Scenario: Hero displays correct data fields count
    When the dashboard loads
    Then the hero section should display 332K as total data fields

  Scenario: Hero statistics are animated on load
    When the dashboard loads
    Then the hero statistics should fade in with upward animation
    And the animation delay should stagger across the four statistics
```

**Test Evidence:**

| Scenario | Result | Evidence |
|---|---|---|
| 11,460 records displayed | ✅ PASS | Visual inspection confirmed |
| 25 seasons displayed | ✅ PASS | Visual inspection confirmed |
| 332K fields displayed | ✅ PASS | Visual inspection confirmed |
| Animation on load | ✅ PASS | fadeUp CSS animation confirmed in code |

---

## Feature: Platform Overview Cards

```gherkin
Feature: Platform Overview Cards
  As a data consumer
  I want to see live platform statistics loaded from the API
  So that I can verify the platform is operational with real data

  Background:
    Given the API is available and responding
    And the frontend has made successful calls to /players/seasons
    and /players/teams

  Scenario: Overview cards load from live API data
    When the API responds successfully
    Then the Total Seasons card should display 25
    And the Total Teams card should display the correct team count
    And the Player Records card should display 11,460
    And the Data Fields card should display 332K

  Scenario: API Status card shows LIVE when API is responding
    When the API health endpoint returns 200
    Then the API Status card should display LIVE in green

  Scenario: Championship Model card shows accuracy
    When the overview section loads
    Then the Championship Model card should display 16%
    And the subtitle should mention 16x better than random

  Scenario: Error state is shown when API is unavailable
    Given the API is in cold start or unavailable
    When the frontend attempts to load overview data
    Then an error message should be displayed
    And the message should suggest waiting 30 seconds and retrying
```

**Test Evidence:**

| Scenario | Result | Evidence |
|---|---|---|
| Cards load from API | ✅ PASS | 25 seasons and teams loaded from live API |
| API LIVE shows green | ✅ PASS | Green dot and LIVE text confirmed |
| Championship model 16% | ✅ PASS | Card displays 16% with correct subtitle |
| Error state shown | ✅ PASS | Error message displayed during cold start |

---

## Feature: Scoring Leaders Leaderboard

```gherkin
Feature: Scoring Leaders Interactive Leaderboard
  As a sports fan
  I want to explore top scoring players with interactive filters
  So that I can find the best performers for any season or team

  Background:
    Given the leaderboard is populated from /players/top-scorers

  Scenario: Leaderboard loads top 10 by default
    When the dashboard loads
    Then the leaderboard should display 10 player rows
    And the first row should show the highest scoring player

  Scenario: Season filter updates the leaderboard
    Given the season dropdown contains all 25 seasons
    When I select Epoca2020-21 and click APPLY
    Then the leaderboard should refresh
    And all displayed players should be from season Epoca2020-21

  Scenario: Team filter narrows results
    Given the team dropdown contains all available teams
    When I select a specific team and click APPLY
    Then only players from that team should be displayed

  Scenario: Show filter changes result count
    When I select Top 25 from the show dropdown and click APPLY
    Then the leaderboard should display 25 player rows

  Scenario: Progress bars show relative scoring
    When the leaderboard is populated
    Then each player row should have an orange progress bar
    And the top scorer should have the longest bar at full width
    And all other bars should be proportionally shorter

  Scenario: Rank 1 is highlighted in gold
    When the leaderboard is populated
    Then the rank number for position 1 should be gold coloured
    And rank 2 should be silver
    And rank 3 should be bronze

  Scenario: Player rows animate on load
    When the leaderboard data is received from the API
    Then each row should slide in from the left
    And rows should animate with staggered delay
```

**Test Evidence:**

| Scenario | Result | Evidence |
|---|---|---|
| Default 10 rows | ✅ PASS | 10 player records displayed on load |
| Season filter works | ✅ PASS | Filter applied and results refresh |
| Team filter works | ✅ PASS | Team filter narrows results correctly |
| Show filter works | ✅ PASS | Top 25 displays 25 rows |
| Progress bars present | ✅ PASS | Orange gradient bars visible per row |
| Gold rank 1 | ✅ PASS | CSS class top1 applies gold colour |
| Row animations | ✅ PASS | slideIn animation confirmed in CSS |

---

## Feature: 3-Point Revolution Chart

```gherkin
Feature: 3-Point Revolution Line Chart
  As a sports analyst
  I want to see the 3-point trend visualised as a line chart
  So that the revolution is immediately visible as a compelling visual story

  Background:
    Given the chart uses hardcoded data from the SQL analysis
    And Chart.js 4.4.1 renders the line chart

  Scenario: Chart renders on page load
    When the dashboard loads and scrolls to the chart section
    Then a line chart should be visible
    And the X-axis should show season labels from 1996-97 to 2020-21

  Scenario: Chart shows clear upward trend
    When the chart is rendered
    Then the line should start low on the left
    And end high on the right
    And show acceleration from approximately 2015 onwards

  Scenario: Post-Curry era points are highlighted in gold
    Given seasons from 2018-19 onwards exceeded 1.0 avg 3PM
    When the chart renders
    Then data points for these seasons should be gold coloured
    And all other data points should be orange

  Scenario: Chart tooltip shows season details on hover
    When a user hovers over a data point
    Then a tooltip should appear
    And the tooltip should show the avg 3PM value for that season

  Scenario: Chart subtitle references the Steph Curry era
    When the chart section is visible
    Then the subtitle should mention the Steph Curry era is visible
```

**Test Evidence:**

| Scenario | Result | Evidence |
|---|---|---|
| Chart renders | ✅ PASS | Line chart visible in browser |
| Upward trend visible | ✅ PASS | Visual inspection confirmed hockey stick shape |
| Gold points post-2018 | ✅ PASS | pointBackgroundColor logic confirmed in JS |
| Tooltip on hover | ✅ PASS | Chart.js tooltip configured and working |
| Curry era subtitle | ✅ PASS | Text confirmed in HTML |

---

## Feature: Footer and Navigation

```gherkin
Feature: Footer Information and External Links
  As a developer or recruiter
  I want to access the GitHub repository and API documentation
  So that I can explore the technical implementation in depth

  Scenario: Footer displays project narrative
    When I scroll to the footer
    Then the footer should mention ISPGaya Porto 2022 as the origin
    And should mention professional Data Engineering platform

  Scenario: API Documentation link is present and correct
    When I look at the footer links section
    Then there should be a link to the Swagger documentation
    And the link URL should contain /docs

  Scenario: GitHub repository link is present
    When I look at the footer links section
    Then there should be a link to the GitHub repository
    And the link should point to GuilhermePires21890

  Scenario: Tech stack badges are displayed
    When I scroll to the footer
    Then I should see badges for Python, FastAPI, PostgreSQL
    And badges for Supabase, Render, Docker, Metabase
    And badges for GitHub Actions

  Scenario: Footer credits reference Porto Portugal
    When I scroll to the footer bottom bar
    Then the text should mention Porto Portugal
    And should mention the date range 2022 to 2026
```

**Test Evidence:**

| Scenario | Result | Evidence |
|---|---|---|
| Project narrative present | ✅ PASS | ISPGaya Porto 2022 text confirmed |
| API docs link present | ✅ PASS | Link to /docs confirmed in HTML |
| GitHub link present | ✅ PASS | GuilhermePires21890 link confirmed |
| Tech badges displayed | ✅ PASS | All 8 tech badges visible |
| Porto Portugal credit | ✅ PASS | Footer bottom text confirmed |

---

## Responsive Design

```gherkin
Feature: Responsive Layout
  As a mobile user
  I want the dashboard to be usable on smaller screens
  So that I can access analytics from any device

  Scenario: Hero title scales on mobile
    Given a viewport width of 375px
    When the dashboard loads
    Then the hero title font size should scale down via clamp()
    And all content should remain readable

  Scenario: Leaderboard hides less critical columns on mobile
    Given a viewport width below 768px
    When the leaderboard is displayed
    Then columns beyond the 4th should be hidden
    And player name and points should always be visible

  Scenario: Footer switches to single column on mobile
    Given a viewport width below 768px
    When the footer is rendered
    Then the three-column grid should collapse to single column
```

**Test Evidence:**

| Scenario | Result | Evidence |
|---|---|---|
| Hero scales on mobile | ✅ PASS | clamp() font-size confirmed in CSS |
| Leaderboard columns hidden | ✅ PASS | nth-child(n+5) display:none in media query |
| Footer single column | ✅ PASS | grid-template-columns: 1fr in media query |

---

## Known Limitations

| Limitation | Impact | Mitigation |
|---|---|---|
| API cold start causes loading errors | User sees error on first visit | Error message guides user to retry after 30s |
| No loading skeleton | Layout shift during data fetch | Spinner shown during load |
| Chart data is hardcoded | 3-point revolution does not auto-update | Data is historical - no update needed |
| No offline support | Page requires internet connection | Acceptable for analytics platform |
| No accessibility audit | Screen reader support not validated | Future enhancement - WCAG 2.1 target |