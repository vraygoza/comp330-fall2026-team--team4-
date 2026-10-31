# Team 4: Calorie Counter Telegram Bot

| Field | Value |
|-------|-------|
| Owner | Adiya (Architecture & Development Lead) |
| Backup | Khumoyun |
| Last updated | 2026-10-30 |

COMP 330 Software Engineering, Fall 2026, Loyola University Chicago.

## What We Are Building
A Telegram bot that tracks calories. A user texts the bot what they ate, the bot looks up the calories, saves the entry, and replies with the user's running total for the day. About 10 to 15 friends and classmates will test it. Macro tracking (protein, carbs, fats, fiber) is planned for a later cycle.

The project was chosen at the 2026-09-16 team meeting. See [D1 in the Decision Log](docs/decisions/decision-log.md).

## Current Status
   Cycle 1 construction (Assignment 4). The bot's core code and automated tests are merged; see the Assignment 4 section below for how to run and test them.

   | Phase gate | Git tag | Status |
   |------------|---------|--------|
   | Assignment 1: Project Launch | `a1-project-launch` | Submitted |
   | Assignment 2: Cycle 1 Planning and Estimation | `a2-planning-estimate` | Submitted |
   | Assignment 3: Architecture and Review Package | `a3-architecture-review` | Submitted |
   | Assignment 4: Construction, Integration and AI Code Review | `a4-construction-integration` | In progress |

## Where to Find Things
| Area | Location | Contents |
|------|----------|----------|
| Team | [`/docs/team/`](docs/team/), [`team-charter.md`](docs/team-charter.md), [`roles.md`](docs/roles.md) | Charter, roles, documentation standards |
| Requirements | [`/docs/requirements/`](docs/requirements/) | Requirements, acceptance criteria, assumptions, open questions |
| Planning | [`/docs/planning/`](docs/planning/README.md) | Scope, task plan, estimates, schedule, risks, commitments |
   | Source code | [`/src/`](src/) | Bot logic and adapters (PR #69) |
   | Tests | [`/tests/`](tests/) | Automated tests (PR #70) |


Task tracking lives in GitHub Issues and the GitHub Projects board, not in repository folders.

## How We Work
1. Every task is a GitHub Issue with one owner.
2. Work happens on a branch and merges through a pull request reviewed by someone other than the author.
3. All work is pushed 48 hours before the official deadline so the team can review it.
4. AI assistance is allowed and must be logged. See the [AI Use Policy](docs/ai/ai-policy.md).

## Team
| Member | Role |
|--------|------|
| Victoria Raygoza | Team Lead |
| Bazid | Planning & Process Lead |
| Adiya | Architecture & Development Lead |
| Sohail | Quality & Review Lead |
| Mazen Malas | Operations & Evidence Lead |
| Khumoyun | Operations & Evidence Co-Lead |



## Assignment 3: Architecture and Review Package
The Cycle 1 architecture evidence is indexed in [docs/architecture/README.md](docs/architecture/README.md).
Planning records are in [docs/planning/](docs/planning/), requirements in [docs/requirements/](docs/requirements/), decisions in [docs/decisions/](docs/decisions/), and AI use in [docs/ai/ai-use-log.md](docs/ai/ai-use-log.md).

The Cycle 1 architecture evidence is indexed in [docs/architecture/README.md](docs/architecture/README.md). Planning records are in [docs/planning/](docs/planning/), requirements in [docs/requirements/](docs/requirements/), decisions in [docs/decisions/](docs/decisions/), and AI use in [docs/ai/ai-use-log.md](docs/ai/ai-use-log.md).



## Assignment 4: Construction and Review Evidence

Status: construction is in progress. This section is updated as pull requests merge.

### How to run
Full details are in [src/README.md](src/README.md). In short, from the repository root:

1. Create your own test bot with @BotFather in Telegram and copy its token. Do not use the shared tester bot.
2. Set up and configure:

```
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env             # Windows: copy .env.example .env
```

3. Open `.env` and paste the token after `TELEGRAM_BOT_TOKEN=`. Never commit `.env`.
4. Start the bot: `python -m src.bot.poll`
5. In Telegram, send `/start` to your test bot. Press Ctrl+C to stop.

`poll.py` is for local development only. The production entry point is the webhook (ADR-0005), deployed only after the host checks pass.

### How to test
From the repository root:

```
python -m unittest discover -s tests -t .
```

Tests use Python's built-in `unittest`, so they need nothing beyond `requirements.txt`. The planned test cases will be in `docs/testing/test-strategy.md` (pending; it is not on `main` yet).

### Evidence map
| Evidence | Location | Status |
|---|---|---|
| Pull request template | `.github/pull_request_template.md` | PR open |
| CI workflow | `.github/workflows/ci.yml` | In progress |
| Source code | [`/src/`](src/) | Merged (#69) |
| Tests | [`/tests/`](tests/) | Merged (#70) |
| Traceability | [docs/planning/traceability.md](docs/planning/traceability.md) | Updating |
| Decisions and ADRs | [docs/decisions/](docs/decisions/) | Exists |
| Architecture | [docs/architecture/](docs/architecture/) | Exists |
| AI-use log | [docs/ai/ai-use-log.md](docs/ai/ai-use-log.md) | Updating |
| Review package (index of all evidence) | `docs/reviews/assignment4-review-package.md` | PR open |



