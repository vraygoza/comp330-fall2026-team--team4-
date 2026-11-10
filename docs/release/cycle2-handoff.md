# Cycle 2 Handoff & Technical Roadmap

| Field | Detail |
|---|---|
| Author | Sohail Shaik (Quality & Review Lead) |
| Date | 2026-11-09 |
| Release Baseline | Tag a5-cycle1-release |
| Governing Requirements | C-1 through C-8, ADR-0001 through ADR-0009 |
| Target Audience | Cycle 2 Development & Verification Team |

---

## 1. Executive Summary & Cycle 1 Baseline

Cycle 1 establishes a verified, end-to-end vertical slice for single-user and multi-user calorie logging:
- Single food phrase parsing with standard portion scaling defaults.
- Deterministic nutritional resolution against a synthetic sample database (ADR-0002).
- Tenant-isolated SQLite persistence strictly partitioned by telegram_user_id (TC-08).
- Centralized date boundary normalization anchored to America/Chicago (CST/CDT).
- Graceful refusal responses for missing tokens or unmapped food items without phantom row creation.

This document identifies unmerged scope, residual operational risks, weak empirical evidence areas, and architectural handoff questions required to initiate Cycle 2 construction safely.

---

## 2. Deferred Scope & Known Boundaries

The following functional capabilities were intentionally deferred during Cycle 1 under scope boundary D3 and ADR governance:

1. Live USDA FoodData Central (FDC) Integration:
   - Current State: Lookup resolves against a static dictionary of common foods.
   - Cycle 2 Requirement: Connect live REST endpoints (https://api.nal.usda.gov/fdc/v1/foods/search), complete with API key management, rate-limiting guards, and network timeout retries.
2. Multi-Item Meal Parsing:
   - Current State: Parser accepts single items per message (e.g., 2 eggs or banana).
   - Cycle 2 Requirement: Natural language parsing for compound meal entries (e.g., 2 eggs, 1 toast, and black coffee) returning itemized breakdowns.
3. Macronutrient Tracking (Protein, Carbohydrates, Fat):
   - Current State: SQLite schema and Telegram replies track aggregate calories exclusively.
   - Cycle 2 Requirement: Extend database schema and reporting payloads to calculate and present macro grams alongside total energy.
4. Rich Telegram Interaction:
   - Current State: Standard text commands and plain-text logging.
   - Cycle 2 Requirement: Inline keyboard confirmation buttons, meal deletion/undo workflows, and historical daily summary views.

---

## 3. Residual Risks & Technical Debt

| Risk ID | Category | Description | Severity | Recommended Cycle 2 Mitigation |
|---|---|---|---|---|
| RSK-01 | External Latency | Live USDA API calls introduce unpredictable external network latency into the Telegram webhook cycle. | High | Implement an asynchronous worker queue or an in-memory/SQLite cache layer for frequently queried foods to keep response times sub-second. |
| RSK-02 | Concurrency Under Load | SQLite file locking risks contention if concurrent write traffic scales across multiple active chat threads. | Medium | Enable SQLite Write-Ahead Logging (WAL mode) or evaluate migration to a client-server relational database (PostgreSQL) if traffic warrants. |
| RSK-03 | Natural Language Ambiguity | Generic food queries (e.g., "milk") match dozens of variations (whole, skim, almond, oat) with wide caloric divergence. | Medium | Establish a ranking heuristic that defaults to the most common standard serving while prompting the user with disambiguation options. |
| RSK-04 | API Quota Exhaustion | Shared USDA demo API keys impose strict hourly request caps (30 requests/hour/IP). | High | Provision dedicated environment keys, implement caching, and add synthetic fallback lookup when rate limits are encountered. |

---

## 4. Weak Evidence Areas Requiring Empirical Hardening

1. Daylight Saving Transition Verification:
   - Observation: While unit tests validate standard midnight rollovers, synthetic tests simulating the 1-hour spring-forward gap and autumn 1-hour overlap require automated clock-mocking assertions.
2. Live Telegram Network Faults:
   - Observation: Cycle 1 testing executed via synthetic payload fixtures and local polling. Network dropouts, duplicate webhook delivery, and Telegram server 5xx errors have not been stressed under live network conditions.
3. Boundary Query Inputs:
   - Observation: Parser test cases emphasize standard metric and imperial descriptors. Non-standard volumetric descriptions ("handful", "splash", "bowl") currently hit the generic refusal path and need expanded fuzz testing.

---

## 5. Architectural Handoff Questions for Cycle 2

1. Caching Architecture: Should nutritional query caching reside inside the primary SQLite application database, or within a dedicated transient key-value store?
2. User Target Configuration: How should user onboarding capture personalized caloric goals, and where will goal-evaluation business logic live in relation to the Chicago day calculator?
3. Schema Evolution: What migration tooling (e.g., Alembic) will govern schema updates when adding macronutrient columns to ensure existing Cycle 1 SQLite records remain backward-compatible?