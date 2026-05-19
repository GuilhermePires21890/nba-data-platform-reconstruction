# Architecture Overview

## Objective

This document defines the target architecture for the modern reconstruction of the original NBA academic project.

The new platform aims to evolve the legacy scraping and analytics solution into a modular, scalable and portfolio-grade Data Engineering platform.

---

# Legacy Architecture

```mermaid
flowchart TD
    A[NBA Website] --> B[C# Selenium Scraper]
    B --> C[CSV Files]
    C --> D[SQL Processing]
    D --> E[R Analysis]
```

## Characteristics

- Monolithic execution flow
- Manual data ingestion
- Local processing
- Separate CSV files per season
- SQL scripts with repetitive transformations
- Statistical analysis executed independently

---

# Modern Target Architecture

```mermaid
flowchart TD
    A[NBA Data Source] --> B[Python Ingestion Layer]
    B --> C[Raw Data Layer]
    C --> D[Validation Layer]
    D --> E[Transformation Layer]
    E --> F[Processed Data]
    F --> G[PostgreSQL]
    G --> H[Analytics SQL]
    H --> I[Power BI]
    H --> J[Jupyter Notebooks]
```

---

# Architectural Principles

## 1. Modularity

Each processing layer should have isolated responsibilities.

## 2. Reproducibility

The entire platform should be reproducible using Docker and version-controlled scripts.

## 3. Documentation-first

Technical decisions must be documented.

## 4. Portfolio-oriented engineering

The repository should demonstrate:

- Data Engineering practices
- Architecture thinking
- Data modeling
- Analytics
- Documentation quality
- Technical evolution

---

# Future Evolution Possibilities

- API ingestion
- Incremental loads
- Cloud deployment
- Data warehouse modeling
- Automated testing
- CI/CD pipelines
- dbt transformations
- Observability and logging
