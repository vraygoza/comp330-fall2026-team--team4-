# Cycle 2 Maturity Summary

| Field | Value |
|-------|-------|
| Owner | Mazen Malas (Operations & Evidence Lead) |
| Backup | Khumoyun (Operations & Evidence Co-Lead) |
| Last updated | 2026-11-23 |
| Baseline | Cycle 1 release tag `A5Cycle1Release` (commit `8eca1b5`) |

Why each Cycle 2 maturity target was picked, what evidence would prove it, who owns it, and how it ended. Every target traces to Cycle 1 evidence in the [Cycle 1 Postmortem](../operations/postmortem-cycle1.md) or the [Risk Register](../planning/risk-register.md).

**How Cycle 2 was planned.** No Cycle 2 task list was written into the repository after the Cycle 1 tag, and no pull request merged to `main` from 11/09 to 11/23 (postmortem F-7). The targets below were set by the Team Lead's Assignment 6 plan on 2026-11-23: no new features, finish and clean up what exists, one owner and one reviewer per item. They are recorded here as the team's actual Cycle 2 scope, not as a plan made in advance.

## Maturity Targets

Dispositions were checked on 2026-11-23 at 6:40 PM. "In review" means a pull request is open; "Merged" is used only once it is on `main`.

| ID | Target | Cycle 1 evidence that justified it | Expected proof | Owner / Backup | Disposition | Risk reduced? |
|----|--------|-----------------------------------|----------------|----------------|-------------|---------------|
| MT-1 | Stop a Telegram resend from saving a meal twice (T-30) | Risk 23; `TODO(T-30)` in `src/bot/web.py`; unowned for 39 days (postmortem F-2) | Repeat-message tests pass in CI; merged to `main` | Adiya / Khumoyun | In review: #104. 18 new tests, 111 in total, CI #82 passed | Partly: proven in unit tests only. A real Telegram retry needs a deployed bot (V-2 to V-4) |
| MT-2 | Record what went wrong in Cycle 1 and why | Release tagged while its own documents were unmerged (F-6); decisions left open 25 days (F-4) | Postmortem with root causes, owned actions and dates | Bazid / Victoria | In review: #105 | Yes, once merged: seven actions (A-1 to A-7) now have owners and dates |
| MT-3 | Evidence files agree with each other and with `main` | Risk register listed Risks 10 to 22 twice and had two Risk 23s (F-8, action A-3); final test evidence said 88 tests when the tag has 93 | De-duplicated register; test and CI evidence re-checked against `main` | Mazen / Bazid | In review: this pull request | Yes: one row per risk; test counts and CI runs through CI #91 checked on 2026-11-23 |
| MT-4 | Tell the truth about what is missing | `known-limitations.md` merged and was reverted the same day (#97, `265a906`); no release notes at the Cycle 1 tag (F-6) | Known limitations and final release notes on `main` | Khumoyun / Mazen | TODO: not opened at 6:40 PM; assigned in the A6 plan | No, until merged |
| MT-5 | Someone outside the team can run and recover the bot | The bot has run end to end once, on one laptop (F-1); a Mac certificate error blocked the first run (PR #90) | Runbook with setup, failure symptoms and recovery | Khumoyun / Mazen | TODO: not opened at 6:40 PM; assigned in the A6 plan | No, until merged |
| MT-6 | Show security, governance and defect status in one place | Commits reached `main` with no review because nothing enforces G-1 (F-7); the defect summary was never merged (F-6, #94) | Security and governance checklist; defect summary | Sohail / Bazid | TODO: not opened at 6:40 PM; assigned in the A6 plan | No, until merged |
| MT-7 | The demo matches the final baseline | The A5 demo script cited 88 tests and a run on a PR commit | Demo script and presentation index re-checked on `main` | Victoria / Adiya | In review: #106. CI #85 to #91 passed; 93 tests re-run on `main` | Yes, once merged: every demo reply matches the code and a named test |
| MT-8 | Process fixes from the postmortem | F-5 (two AI logs, no stated authority), F-3 (two re-estimation files), F-2 (two owner lists), F-7 (no branch protection) | Postmortem actions A-2, A-4, A-6 and A-7 done | Khumoyun (A-2), Bazid (A-4, A-6), Victoria (A-7) | TODO: not in the A6 plan; due 2026-11-24 in the postmortem | No |

## Deliberately Cut From Cycle 2

These were cut because the Assignment 6 plan allows no new features, and because each one depends on deployment, which has not happened. They stay open in the [Risk Register](../planning/risk-register.md) with owners.

| Work | Why it was not done | Risk |
|------|---------------------|------|
| Deploy the webhook: host checks V-2 to V-4, smoke test T-34, practice deploy | Needs T-30 merged first; no host checks scheduled (F-1) | 14, 18, 21 |
| Real food data: V-1, FDC adapter, hand check T-13, food cache T-31 | New feature work; the bot keeps the eight made-up foods | 4, 19 |
| `/today` (AC-5.1, AC-5.2) | New feature | 3 |
| Tester notice T-25, invite check and `/privacy` T-29 | Only needed once outside testers can reach the bot | 15 |
| Deletion script T-33 and nightly backup T-35 | No tester data exists until deployment | 22 |

## Result

Cycle 2 was a cleanup cycle by choice. Every target came from a specific Cycle 1 finding, and none adds a feature. MT-1 is the only code change. At 6:40 PM, four targets were in review, three were assigned but not opened, and one was not in the plan. The final state of each pull request at the `a6-final-release` tag is recorded in the Assignment 6 release package. The biggest risk is unchanged: the bot is still not deployed, so nothing has been tested by an outside tester (Risks 14 and 15).

## Change Log
| Date | Change | By |
|------|--------|----|
| 2026-11-23 | Created for Assignment 6 from the Cycle 1 postmortem, the risk register, the open pull requests and the Team Lead's A6 plan | Mazen |