# ADR-0009: Dependencies and Python Version

| Field | Value |
|-------|-------|
| Owner | Mazen Malas (Operations & Evidence Lead) |
| Backup | Adiya (Architecture & Development Lead) |
| Last updated | 2026-11-09 |

- **Status:** Accepted (2026-11-09, team vote in #56).
- **Decision owner:** Mazen (dependency review, issue #58), with Adiya
- **Related:** [ADR-0005](adr-0005-python-flask-webhook.md); NFR-3, NFR-5; Risk 6; [`requirements.txt`](../../requirements.txt); [`ci.yml`](../../.github/workflows/ci.yml) (issue #57, PR #73)

## Context
`requirements.txt` and `ci.yml` both say new packages and GitHub Actions are reviewed in this ADR, but it was not written during Assignment 4 (listed as Not started in the [Assignment 4 evidence package](../reviews/assignment4-review-package.md)). In her review of PR #73, Adiya also asked that the Python version be settled here: ADR-0005 says "Python 3.10 or later," and Python 3.10 reached end of life in October 2026.

## What We Depend On
Checked on 2026-11-09 against `main` (tag `a4-construction-integration`) and open PR #90.

| Dependency | Version | Used in | Why |
|------------|---------|---------|-----|
| Flask | 3.1.3, pinned in `requirements.txt` | `src/bot/web.py` | Webhook endpoint (ADR-0005, contract C-1) |
| Werkzeug, Jinja2, itsdangerous, click, blinker, MarkupSafe | Installed by Flask, not pinned. Versions checked: 3.1.9, 3.1.6, 2.2.0, 8.5.0, 1.9.0, 3.0.3 | Flask itself | Flask's own requirements |
| Python standard library | Comes with Python | `urllib` (Telegram Adapter), `hmac` (secret check), `zoneinfo` (Chicago day), `sqlite3` (Entry Store, PR #90), `json`, `logging` | Everything else |
| `actions/checkout` | v7.0.1, pinned to commit `3d3c42e` | `ci.yml` | Downloads the code in CI |
| `actions/setup-python` | v7.0.0, pinned to commit `5fda3b9` | `ci.yml` | Installs Python in CI |

There is no Telegram library. ADR-0005 rejected `python-telegram-bot`, and the Telegram Adapter (`src/adapters/telegram.py`) calls the Bot API with `urllib`.

## Decision
1. **Python 3.12 or later.** This replaces item 1 of ADR-0005. CI already runs 3.12. Python 3.12 gets security fixes until October 2028, and PythonAnywhere (ADR-0006) offers it on its current system image.
2. **Flask is the only runtime package.** Adding a package or a GitHub Action needs a pull request that updates this ADR (name, version, why, audit result) along with `requirements.txt` or `ci.yml`.
3. **Pin what we control.** Flask is pinned by version. Actions are pinned to a full commit SHA, so a moved tag cannot change what runs. The CI token is read-only.
4. **Flask's own dependencies stay unpinned for Cycle 1.** Accepted because the audit below found no known vulnerabilities. A lock file with hashes is a Cycle 2 candidate.

## Security Check (2026-11-09)
- `pip-audit` on Flask 3.1.3 and the six dependency versions above: no known vulnerabilities. Flask 3.1.3 and Werkzeug 3.1.9 were the newest releases on PyPI that day.
- Both Action SHAs match their release tags in the `actions/checkout` and `actions/setup-python` repositories. `actions/setup-python` v7.1.0 has since been released; we stay on v7.0.0 and change the SHA and this ADR together if we move.
- Secrets are read only by adapters, from environment variables (NFR-3). The CI secrets check fails a pull request that commits a `.env`, database or key file, or text shaped like a Telegram token. It checks the current files only, not git history (Risk 6).

## Consequences
- **Good:** few moving parts: one package family and two pinned Actions.
- **Cost:** we maintain our own small Telegram adapter (ADR-0005).
- **Gaps:** Flask's dependencies can install at newer versions than the ones checked here. On Windows, `zoneinfo` needs `pip install tzdata`, because Windows has no built-in time zone database; CI and the Linux host are not affected.
- **Follow-up:** `src/README.md` now says Python 3.12 or later (changed in PR #90).
## Change Log
| Date | Change | By |
|------|--------|----|
| 2026-11-09 | Created: dependency review for issue #58; Python 3.12 minimum, from Adiya's review of PR #73 | Mazen |
| 2026-11-09 | Accepted by team vote (#56) | Mazen |