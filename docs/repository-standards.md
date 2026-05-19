# Repository Standards

## Objective

Define repository organization and engineering conventions for the NBA Data Platform Reconstruction project.

---

# Engineering Principles

## Documentation-first

All important technical decisions should be documented.

## Modular architecture

Responsibilities should be separated by processing layer.

## Reproducibility

Local environments and execution steps should be reproducible.

## Maintainability

The repository structure should remain scalable and understandable.

---

# Naming Conventions

| Area | Convention |
|---|---|
| Python files | snake_case |
| SQL files | snake_case |
| Markdown docs | kebab-case |
| Branches | feature/ or docs/ |

---

# Git Standards

## Commit Style

Examples:

- feat: add dataset consolidation pipeline
- docs: add architecture overview
- refactor: improve SQL transformation logic
- fix: correct player statistics mapping

---

# Data Standards

- Preserve raw data immutability
- Separate processing stages
- Avoid overwriting curated datasets
- Document schema changes

---

# Documentation Standards

All major modules should include:

- purpose
- responsibilities
- usage guidance
- future evolution notes
