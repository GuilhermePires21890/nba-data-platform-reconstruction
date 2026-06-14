# Changelog

All notable changes to the NBA Data Platform are documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [Sprint 16] - 2026-06-14 - Polish and Hardening

### Fixed
- BUG-001: `games_played` field missing from `/players/top-scorers` response - added to SELECT alongside normalization
- BUG-002: Inconsistent field naming across API - normalized all endpoints to English (`player`, `team`, `points`, `assists`, `rebounds`, `games_played`, `fantasy_points`)
- BUG-003: `/analytics/championship-predictor` without season filter returned only latest season - now returns predicted champion per season across all 25 seasons
- BUG-004: `/analytics/young-stars` returned duplicate players across seasons - implemented `DISTINCT ON (jogador)` to return each player's best season only
- BUG-005: Player Career header showed only first team - backend now returns `teams` field with all franchises (e.g. "CLE / MIA / LAL")
- BUG-006: Era Analysis grid rendered ghost 6th slot - replaced `auto-fill` with `auto-fit` in CSS grid

### Added
- Cold start UX banner - orange notice on page load, auto-hides after first successful API response
- Championship Predictor dynamic mode label - shows context ("Predicted champion per season - 25 seasons" vs "All teams ranked for [season]")

---

## [Sprint 15] - 2026-06-14 - Frontend Analytics Upgrade

### Added
- Era Analysis section with 5 historical era cards (color-coded by era) and grouped bar chart via `/analytics/era-analysis`
- 3-Point Revolution chart upgraded from hardcoded data to live API (`/analytics/3point-revolution`) with dual Y-axis (3PM + League 3P%)
- Championship Predictor section with ranked table, score bars, and season filter via `/analytics/championship-predictor`
- Player Career Search with text input, Enter key support, career summary cards, and 3-dataset line chart via `/analytics/players/{name}/career`
- Young Stars section with grid cards and season filter via `/analytics/young-stars`

### Fixed
- Field name mapping between frontend and all analytics endpoints
- Route paths corrected after openapi.json inspection (`/analytics/players/{name}/career`, `/analytics/young-stars`)

---

## [Sprint 14] - 2026-06-12 - QA Expert Documentation

### Added
- 7 Gherkin/BDD specification files covering all platform features
- 78 scenarios across Championship Predictor, 3-Point Revolution, API rate limiting, data integrity, frontend rendering, analytics endpoints, and security
- Enterprise-grade QA documentation demonstrating SDET-level thinking

---

## [Sprint 13] - 2026-06-12 - API Analytics Endpoints

### Added
- `GET /analytics/championship-predictor` - weighted scoring model using plus/minus, fantasy points, points, assists, rebounds with RANK() window function
- `GET /analytics/era-analysis` - 5 NBA eras aggregated with CASE WHEN grouping
- `GET /analytics/3point-revolution` - season-by-season 3-point trend with league percentage
- `GET /analytics/players/{player_name}/career` - full career trajectory per player ordered by season
- `GET /analytics/young-stars` - top performers aged 25 or under ordered by fantasy points
- CI pipeline timeout extended to 90s with API warm-up step for Render free tier

---

## [Sprint 12] - 2026-06-04 - ADR Cleanup and Deploy Fix

### Added
- ADR-004: Rate Limiting Strategy (slowapi, 30-60 req/min)
- ADR-005: CORS Policy (restricted to known frontend domain)
- ADR-006: Security Headers Middleware

### Fixed
- Render auto-deploy not triggering - resolved by configuring manual GitHub Deploy Hook webhook
- `.coverage` file added to `.gitignore`
- Removed debug test line from README

---

## [Sprint 11] - 2026-06-04 - Public Frontend

### Added
- Dark editorial-style public frontend with Chart.js
- Hero section with animated stats (Bebas Neue + DM Mono + Fraunces typography)
- Platform Overview live data cards
- Scoring Leaders leaderboard with animated bars and filters
- 3-Point Revolution line chart (hardcoded trend data)
- Noise texture overlay, sticky header, responsive layout
- Deployed as Render Static Site at `nba-data-platform.onrender.com`

---

## [Sprint 10] - 2026-06-04 - Cloud Deployment

### Added
- Supabase cloud PostgreSQL migration with full dataset (11,460 records)
- Render Web Service deployment for FastAPI (`nba-data-platform-api.onrender.com`)
- IPv4 pooler configuration for Supabase compatibility (`aws-0-eu-west-3.pooler.supabase.com:6543`)
- ADR-003: Cloud Infrastructure Decision (Supabase + Render over AWS RDS + EC2)

---

## [Sprint 9] - 2026-06-04 - CI/CD Pipeline

### Added
- GitHub Actions workflow (`nba-ci.yml`) with 3 job stages: transformation tests, API contract tests, API startup validation
- Pytest integration across all test layers in CI
- Docker Compose service orchestration for test environment
- ADR-002: CI/CD Tool Selection (GitHub Actions over Jenkins/CircleCI)

---

## [Sprint 8] - 2026-06-04 - FastAPI REST Layer

### Added
- FastAPI application with Swagger UI (`/docs`) and ReDoc (`/redoc`)
- `GET /players/` with season, team, limit, offset filters
- `GET /players/top-scorers` with season and limit filters
- `GET /players/seasons` and `GET /players/teams` for filter population
- slowapi rate limiting (30-60 req/min per endpoint)
- Restricted CORS policy
- Security headers middleware (X-Content-Type-Options, X-Frame-Options, X-XSS-Protection)
- Security audit: SQL injection, rate limiting, CORS, oversized request, path traversal - all passed
- ADR-001: FastAPI over Django REST Framework

---

## [Sprint 7] - 2026-06-04 - Championship Predictor Model

### Added
- SQL-based Championship Predictor backtested across 25 seasons (1996-2021)
- 16% exact accuracy - 16x better than random baseline (1/30 = 3.3%)
- Weighted scoring: wins (40%), points (25%), plus/minus (20%), fantasy (15%)
- Historical validation query with actual vs predicted champion comparison

---

## [Sprint 6] - 2026-06-04 - Metabase Dashboards

### Added
- 6 Metabase dashboards: Top Scorers, Assists Leaders, Rebounds Leaders, Fantasy Points, 3-Point Revolution, Young Stars U25
- Docker-based Metabase deployment connecting to local PostgreSQL
- Enterprise-grade README with badges, Mermaid architecture diagrams, screenshot embeds

---

## [Sprint 5] - 2026-06-04 - Data Pipeline and Database

### Added
- Python ETL pipeline replacing original R scripts
- Consolidated PostgreSQL schema (`player_stats` unified table replacing 25 separate season tables)
- pandas transformation layer with data quality checks
- pytest test suite: `test_transformation.py`, `test_data_integrity.py`, `test_dataset_schema.py`, `test_api_contracts.py`
- 43 tests across transformation, data integrity, and API contract layers
- Docker Compose local development environment

---

## [Sprint 1-4] - 2022 / 2026 - Academic Origin and Reconstruction Planning

### Origin (2022)
- Academic project at Instituto Superior Politécnico Gaya (Porto, Portugal)
- C# + Selenium web scraper targeting NBA.com traditional player statistics
- 25 seasons scraped (1996-97 to 2020-21): 11,460 player records, 332,340 data fields
- 25 separate SQL Server tables (one per season), R scripts for exploratory analysis
- Manual, monolithic, no automation, no tests, no unified schema

### Reconstruction Planning (2026)
- Decision to modernize into a professional Data Engineering portfolio project
- Architecture decision: Python + FastAPI + PostgreSQL + Supabase + Render + GitHub Actions
- Narrative framing: "From academic scraper to professional data platform"
- Sprint roadmap defined across 16+ iterations
