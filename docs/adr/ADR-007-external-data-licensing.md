# ADR-007 - External Data Licensing and Publication Hold

## Status
Accepted (18 Nov 2026)

---

## Context

The platform started from a 2022 academic dataset built by scraping NBA statistics. In November 2026
the project added data from the balldontlie API (free plan) to extend the history to 2000-2025: game
results, team results per season, champions per season and a walk-forward backtest of a championship
predictor.

The balldontlie free plan documentation states that NBA data requires a separate paid subscription.
Whether public, non-commercial use of the free tier is covered by the terms is not confirmed in writing.

---

## Decision

1. Data derived from the balldontlie API (raw responses, aggregated tables, champion labels for 2000-2025,
   team results per season and backtest results) is **not published** until written confirmation is received.
   Publication means the public website, the public API, README content or any file in the public repository.
2. Raw API responses are never committed to the repository. The local ingestion output stays in
   `data/` and is excluded from version control.
3. The `team_seasons` table may exist in the production database, but no public endpoint exposes it
   until the publication hold is lifted.
4. The original academic dataset is unchanged by this decision. Its source is documented in
   `docs/legacy-analysis.md`.
5. The question has been sent to balldontlie with two points: whether derived aggregates may be published
   on the free plan, and which licence applies to NBA game data accessed through the free plan.

---

## Consequences

- Public features that depend on the balldontlie data (backtest results, champion history beyond the
  original dataset, team records per season) are delayed.
- Internal work continues: validation, analysis and loaders are tested locally.
- If the answer requires a paid plan or a written agreement, the publication scope is reviewed again
  and this ADR is updated.

---

## Open items

- Written reply from balldontlie (sent 17 Nov 2026). Follow-up planned for 25 Nov 2026 if no reply.
- Confirm whether the original academic dataset (collected from NBA statistics in 2022) needs a
  licence review. This is out of scope for the balldontlie question but should be documented.
