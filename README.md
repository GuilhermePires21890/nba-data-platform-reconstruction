# 🏀 NBA Data Platform Reconstruction

> **From academic scraper to professional Data Engineering platform.**  
> A full modernization of a legacy NBA analytics project - preserving its origin, elevating its engineering.

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791?style=flat&logo=postgresql&logoColor=white)](https://postgresql.org)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=flat&logo=docker&logoColor=white)](https://docker.com)
[![Metabase](https://img.shields.io/badge/Metabase-Analytics-509EE3?style=flat&logo=metabase&logoColor=white)](https://metabase.com)
[![Pandas](https://img.shields.io/badge/Pandas-2.2+-150458?style=flat&logo=pandas&logoColor=white)](https://pandas.pydata.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![CI Pipeline](https://github.com/GuilhermePires21890/nba-data-platform-reconstruction/actions/workflows/ci.yml/badge.svg)](https://github.com/GuilhermePires21890/nba-data-platform-reconstruction/actions/workflows/ci.yml)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Supabase](https://img.shields.io/badge/Supabase-Cloud-3ECF8E?style=flat&logo=supabase&logoColor=white)](https://supabase.com)
[![Render](https://img.shields.io/badge/Render-Deploy-46E3B7?style=flat&logo=render&logoColor=white)](https://render.com)

---

## 📖 Project Story

This project started as a **university assignment** in 2021/2022 at Instituto Superior Politécnico Gaya (Porto, Portugal).

The original goal was simple: extract historical NBA player statistics using web scraping.

The result was a working **end-to-end pipeline** built with C#, Selenium, CSV files, SQL Server and R - scraping **25 seasons of NBA data (1996–2021)**, covering **11,460 player records** across **332,340 data fields**.

**This repository is the reconstruction** - taking that academic foundation and rebuilding it as a professional Data Engineering and Analytics platform, demonstrating technical evolution, architectural maturity and modern engineering practices.

---

## 📊 Dataset Coverage

| Metric | Value |
|---|---|
| Seasons covered | 1996–97 to 2020–21 |
| Total seasons | 25 |
| Total player records | 11,460 |
| Total data fields | 332,340 |
| Statistical columns | 30 per record |

---

## 🏗️ Architecture Evolution

### Legacy Architecture (Original Academic Project)

```mermaid
flowchart LR
    A[🌐 NBA Website] --> B[C# + Selenium Scraper]
    B --> C[📄 CSV per Season]
    C --> D[SQL Server Scripts]
    D --> E[R Statistical Analysis]
    E --> F[📈 Insights]
```

**Stack:** C# · Selenium · CSV · SQL Server · R · ggplot2

---

### Modern Architecture (This Reconstruction)

```mermaid
flowchart TD
    A[🌐 NBA Data Source] --> B[Python Ingestion Layer]
    B --> C[📁 Raw Data Layer]
    C --> D[🔍 Validation Layer]
    D --> E[⚙️ Transformation Layer]
    E --> F[📦 Processed Dataset]
    F --> G[(PostgreSQL 16)]
    G --> H[📊 Metabase Dashboards]
    G --> I[📓 Jupyter Notebooks]
    G --> J[🔎 SQL Analytics Layer]
```

**Stack:** Python · Pandas · PostgreSQL · Docker · Metabase · SQL · Jupyter

---

## 🚀 Tech Stack

|| Layer | Technology | Purpose |
|---|---|---|
| Ingestion | Python + Pandas | Data extraction and consolidation |
| Storage | PostgreSQL 16 | Relational analytical database |
| Runtime | Docker Compose | Reproducible local environment |
| BI & Dashboards | Metabase | Interactive analytics and visualization |
| Analytics | SQL | Aggregations, rankings, historical analysis |
| REST API | FastAPI | Public API layer with Swagger docs |
| Cloud DB | Supabase | Managed PostgreSQL cloud hosting |
| Cloud Deploy | Render | Web service + static site hosting |
| CI/CD | GitHub Actions | Automated testing pipeline |
| Frontend | HTML + Chart.js | Public analytics dashboard |
| Documentation | Markdown + Mermaid | Architecture and data dictionary |

---

## 📈 Analytics Dashboards

Built with **Metabase** on top of **PostgreSQL**, covering 25 seasons of NBA history.

### Dashboard Preview

#### NBA Historical Analytics - 1996 to 2021
![NBA Historical Analytics Dashboard](docs/screenshots/NBA%20Historical%20Analytics%20-%201996%20to%202021.png)

#### Top 10 Historical Scorers
![Top 10 Historical Scorers](docs/screenshots/Top%2010%20Historical%20Scorers.png)

#### Top 10 All-Time Assist Leaders
![Top 10 All-Time Assist Leaders](docs/screenshots/Top%2010%20All-Time%20Assist%20Leaders.png)

#### Top 10 All-Time Rebound Leaders
![Top 10 All-Time Rebound Leaders](docs/screenshots/Top%2010%20All-Time%20Rebound%20Leaders.png)

#### Top 10 Fantasy Points Leaders
![Top 10 Fantasy Points Leaders](docs/screenshots/Top%2010%20Fantasy%20Points%20Leaders.png)

### NBA Historical Analytics - 1996 to 2021

| Dashboard | Insight |
|---|---|
| 🏆 Top 10 Historical Scorers | LeBron James leads with 25 seasons of dominance |
| 🎯 Top 10 All-Time Assist Leaders | Chris Paul #1 all-time in accumulated assists |
| 💪 Top 10 All-Time Rebound Leaders | Dwight Howard leads the big men era |
| ⭐ Top 10 Fantasy Points Leaders | LeBron James dominates multi-stat contribution |

> Dashboards available locally via Metabase after environment setup.

---

## 🌐 Live Platform

| Service | URL |
|---|---|
| **🖥️ Live Dashboard** | **https://nba-data-platform.onrender.com** |
| API Root | https://nba-data-platform-api.onrender.com |
| Swagger Docs | https://nba-data-platform-api.onrender.com/docs |
| Top Scorers | https://nba-data-platform-api.onrender.com/players/top-scorers |
| Seasons | https://nba-data-platform-api.onrender.com/players/seasons |
| Teams | https://nba-data-platform-api.onrender.com/players/teams |

> Free tier - cold start may take 30-60 seconds after inactivity.

---

## ⚡ Quick Start

---

### Prerequisites

- Docker Desktop
- Python 3.11+
- Git

### 1. Clone the repository

```bash
git clone https://github.com/GuilhermePires21890/nba-data-platform-reconstruction.git
cd nba-data-platform-reconstruction
```

### 2. Configure environment

```bash
cp .env.example .env
```

### 3. Start the platform

```bash
docker compose up -d
```

### 4. Set up Python environment

```bash
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
```

### 5. Verify the platform

```bash
docker ps
# Expected: nba_postgres (Up) · nba_metabase (Up)
```

### 6. Access Metabase

```
http://localhost:3001
```

---

## 📁 Repository Structure

```
nba-data-platform-reconstruction/
│
├── data/
│   ├── raw/legacy_csv/          # Original scraped CSV files (25 seasons)
│   ├── processed/               # Consolidated analytical dataset
│   └── curated/                 # Analytics-ready outputs
│
├── docs/
│   ├── adr/                     # Architecture Decision Records
│   ├── architecture.md          # System architecture overview
│   ├── data-dictionary.md       # Column definitions and metadata
│   ├── legacy-analysis.md       # Original project analysis
│   └── modernization-strategy.md
│
├── notebooks/
│   └── exploratory_analysis.md  # EDA planning and analysis
│
├── sql/
│   ├── schema/                  # Table definitions
│   ├── analytics/               # Analytical queries
│   ├── transformations/         # Data loading scripts
│   └── views/                   # Reusable analytical views
│
├── src/
│   ├── transformation/          # Dataset consolidation pipeline
│   ├── validation/              # Schema and data quality validation
│   └── utils/                   # Shared configuration and utilities
│
├── tests/                       # Automated test suite
├── docker-compose.yml           # Platform orchestration
├── requirements.txt             # Python dependencies
└── .env.example                 # Environment configuration template
```

---

## 🗺️ Roadmap

| Sprint | Focus | Status |
|---|---|---|
| Sprint 1 | Technical archaeology and baseline | ✅ Completed |
| Sprint 2 | Modern architecture design | ✅ Completed |
| Sprint 3 | Repository setup and legacy asset organization | ✅ Completed |
| Sprint 4 | Dataset consolidation and PostgreSQL ingestion | ✅ Completed |
| Sprint 5 | Metabase analytics dashboards | ✅ Completed |
| Sprint 6 | GitHub polish and professional documentation | ✅ Completed |
| Sprint 7 | Advanced SQL analytics and Championship Predictor | ✅ Completed |
| Sprint 8 | FastAPI REST layer | ✅ Completed |
| Sprint 9 | CI/CD with GitHub Actions | ✅ Completed |
| Sprint 10 | Cloud deployment - Supabase PostgreSQL + Render Web Service | ✅ Completed |
| Sprint 11 | Public frontend - live dashboard at nba-data-platform.onrender.com | ✅ Completed |

---

## 📐 Architecture Decision Records

| ADR | Decision | Status |
|---|---|---|
| [ADR-001](docs/adr/ADR-001-use-postgresql.md) | PostgreSQL as primary database | ✅ Accepted |
| ADR-002 | Python for ingestion and transformation | ✅ Accepted |
| ADR-003 | Docker for reproducible environments | ✅ Accepted |
| ADR-004 | Metabase for BI and dashboards | ✅ Accepted |

---

## 🎓 Academic Origin

> **"Today, sports statistics and analytics are omnipresent and have become a very important factor in decision-making in sports."**  
> - Original academic paper, ISPGaya 2022

**Original project facts:**

- **Institution:** Instituto Superior Politécnico Gaya, Porto, Portugal
- **Year:** 2021/2022
- **Original stack:** C# · Selenium · CSV · SQL Server · R
- **Data scraped:** 25 NBA seasons (1996–2021)
- **Records extracted:** 11,460 player records

The academic project demonstrated genuine end-to-end thinking - from web extraction to statistical analysis. This reconstruction preserves that narrative while elevating the engineering maturity.

---

## 🤝 Contributing

This is a portfolio project under active development.  
Feedback, suggestions and issues are welcome via [GitHub Issues](https://github.com/GuilhermePires21890/nba-data-platform-reconstruction/issues).

---

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

---

<p align="center">
  <strong>Built in Porto, Portugal 🇵🇹</strong><br/>
  Academic origin · Professional reconstruction · Engineering evolution
</p>

