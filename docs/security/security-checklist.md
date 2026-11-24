# Assignment 6 Security Verification Checklist

Repository: comp330-fall2026-team--team4-
Baseline Commit: 9dbc917 (main, 107 passing tests: 93 in tests/, 14 in spikes/inv-01-lookup-storage/)
Owner: Sohail Shaik (Quality & Review Lead)
Reviewer: Mazen Malas
Last Updated: 2026-11-23

---

## 1. Secrets & Credential Hygiene
- [x] No Hardcoded Secrets: Verified zero tokens or API keys in tracked files. .env.example uses placeholder values only (123456:REPLACE_ME).
- [x] CI Secret Scanning: Secret scanning and dependency checks run in .github/workflows/ci.yml on PRs and pushes to main.
- [x] Local Exclusion: Runtime SQLite files and .env files are excluded via .gitignore.

## 2. Input Validation & Data Isolation
- [x] Per-User SQLite Isolation: src/adapters/store.py scopes entries and totals by user_id (verified in tests/test_log_food.py and tests/test_store.py).
- [x] Parameterized SQL: src/adapters/store.py uses parameterized SQL bindings to prevent SQL injection.
- [x] Normalization & Safe Errors: src/core/food_lookup.py normalizes whitespace/case (tests/test_food_lookup.py, tests/test_parser.py); router.py, poll.py, and web.py return safe messages without logging PII (tests/test_router.py).
- [ ] Duplicate Update Protection (T-30 / PR #104): TODO: Not merged on main at 9dbc917 (pending PR #104). Tracked in docs/release/known-limitations.md and docs/quality/defect-summary.md.

## 3. Dependency & Network Boundary
- [x] Bounded Offline Execution: Lookups use local src/core/sample_foods.json with zero external network calls.
- [ ] External USDA FDC API Controls: TODO: Deferred to Cycle 2 per ADR-0002 (live FDC API out of scope for offline baseline).
