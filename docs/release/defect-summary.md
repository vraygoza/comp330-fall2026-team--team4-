# Cycle 1 Defect & Issue Summary

| Field | Detail |
|---|---|
| Author | Sohail Shaik (Quality & Review Lead) |
| Date | 2026-11-09 |
| Baseline Tag | `a5-cycle1-release` |
| Target Cycle | Assignment 5 / Cycle 1 Release Baseline |
| Governing Requirements | C-1 through C-8, ADR-0001 through ADR-0008, Scope Decision D3 |

---

## 1. Classification & Status Definitions

- Severity Levels:
  - High: Blocks the core end-to-end food-logging path, compromises multi-user SQLite isolation, or risks runtime data corruption.
  - Medium: Incorrect timezone boundary handling, unhandled edge-case inputs, or governance/documentation mismatches that obscure project truth.
  - Low: Non-blocking formatting discrepancies, minor logging inconsistencies, or localized CLI output anomalies.
- Disposition States:
  - Fixed: Remediated, independently reviewed, and verified by passing automated tests on `main`.
  - Mitigated: Defensive fallbacks implemented; residual operational risk is controlled and acceptable for Cycle 1 release.
  - Deferred: Explicitly scoped out and scheduled for implementation during Cycle 2 construction.
  - Accepted: Intentional architectural deviation bounded by scope decision D3 (e.g., offline synthetic food data).

---

## 2. Comprehensive Defect Matrix

| Defect ID | Description | Severity | Disposition | Root Cause & Remediation Details | Verification Evidence | Owner |
|---|---|---|---|---|---|---|
| DEF-01 | Unintegrated End-to-End Log Path: Core pipeline returned `NOT_READY` at A4 baseline; Telegram message parsing was decoupled from SQLite storage and running totals. | High | Fixed | Core router lacked integration handlers linking parser output to database insertion and total computation. Resolved via PR #90 end-to-end integration. | `tests/test_integration.py` passing on `main` | Adiya / Team |
| DEF-02 | ADR Status Governance Mismatch: Architectural review documented ADRs as accepted while individual records (`ADR-0001` to `ADR-0008`) retained `Proposed` status. | Medium | Fixed | Decision files were not updated immediately after review consensus. Addressed via Issue #56; all ADR headers reconciled to authoritative state. | `docs/architecture/architecture.md`, Issue #56 | Adiya / Sohail |
| DEF-03 | Unknown Food Negative Path: Unmatched food queries risked raising unhandled exceptions (`KeyError`) or writing zero-calorie phantom rows. | High | Fixed | Lookup logic lacked explicit empty-result propagation. Added explicit `FOOD_NOT_FOUND` refusal response asserting zero database inserts on failure. | TC-05 test case; `tests/test_lookup.py` | Khumoyun |
| DEF-04 | Chicago Timezone Midnight Rollover: Late-evening meals logged between 7:00 PM and 11:59 PM CST risked attribution to the next UTC day. | Medium | Fixed | Timestamps defaulted to server UTC. Implemented centralized timezone normalization utility converting epoch timestamps to `America/Chicago`. | Daylight saving & midnight boundary tests | Bazid |
| DEF-05 | Offline Synthetic Food Data Boundary: Food resolution relies on offline dictionary; live USDA FoodData Central (FDC) API calls deferred. | Medium | Accepted | External REST calls and network error handling were bounded under ADR-0002 and D3 to guarantee reliable offline demonstration. | ADR-0002, Scope Decision D3 | Adiya |
| DEF-06 | Single Food Item Parsing Constraint: Natural language meal strings with multiple comma-separated items fail parsing. | Low | Deferred | Parser grammar limited to `<quantity> <food_item>`. System returns clean refusal prompting single-item entries. Multi-item parsing deferred to Cycle 2. | Cycle 2 Roadmap; Known Limitations log | Khumoyun |
| DEF-07 | Two-User SQLite Concurrency & Leakage: Initial unit tests only asserted single-tenant isolation, leaving cross-user data leakage unverified. | High | Fixed | Multi-tenant assertions were absent from CI suite. Added two-user test in PR #90 asserting User B totals remain 0 kcal when User A logs entries. | TC-08 test case; PR #90 CI run | Adiya |
| DEF-08 | Environment Secrets Fallback: Telegram bot skeleton risked unhandled network exceptions if `BOT_TOKEN` was unset. | Medium | Fixed | Startup entry point lacked fail-fast guard. Implemented immediate non-zero exit with explicit standard-error logging when configuration is missing. | PR #69 verification check | Adiya |