# ADR-0001: No AI Behavior in the Running Bot

| Field | Value |
|-------|-------|
| Owner | Mazen Malas (Operations & Evidence Lead) |
| Backup | Adiya (Architecture & Development Lead) |
| Last updated | 2026-10-15 |

- **Status:** Proposed (P-1 in [INV-01](../architecture/investigations/inv-01-lookup-storage.md)). TODO: change to Accepted, with the date, once the team accepts it at the architecture review.
- **Decision owner:** Whole team
- **Closes:** Assignment 3 Section 6 (AI boundary questions)
- **Related:** FR-2, FR-3, FR-6; Risks 6 and 13

## Context
Assignment 3 asks whether the product includes AI behavior. If it does not, the team must record that decision and apply the boundary questions to its other services. An AI model could read free-form meals, but our [AI Use Policy](../ai/ai-policy.md), Section 6, forbids sending real users' food logs to AI tools, and AC-6.2 forbids saving a guessed calorie value.

## Decision
The Cycle 1 bot uses no AI model. Messages are parsed and matched by fixed rules ([ADR-0002](adr-0002-food-data-source-and-matching.md), [ADR-0004](adr-0004-accepted-input-forms.md)), so every reply can be traced to a rule and an FDC record. AI is used only by team members during development, under the AI Use Policy, and is disclosed in the [AI Use Log](../ai/ai-use-log.md).

## Alternatives Considered
| Option | Why not chosen |
|--------|----------------|
| An AI model reads free-form meals ("a bowl of oatmeal with berries") | Sends tester messages to a third party, which our AI Use Policy forbids; costs money (NFR-5); can return a confident wrong answer (AC-6.2) |
| An AI model estimates calories when FDC has no match | A guessed value, which AC-6.2 and [TR-2](tradeoff-records.md) rule out |

## Consequences
- **Good:** results are repeatable and testable; no tester data leaves our system except the food words sent to FDC; no AI cost.
- **Cost:** testers must use the accepted message forms ([ADR-0004](adr-0004-accepted-input-forms.md)).
- **Revisit when:** several foods per message (DF-2) or photo input (DF-5) are scheduled. Adding AI would need a new ADR, an AI Use Policy update, and a new tester notice.

## Evidence and Checks
- The eight boundary questions are applied to FDC and Telegram in [Architecture](../architecture/architecture.md), Section 6. Data-level answers (Read, Infer, Log, Recover) are in [Data and Context](../architecture/data-context.md).
- Code review at merge (checkpoint G-1) confirms the bot has no AI service dependency.

## Change Log
| Date | Change | By |
|------|--------|----|
| 2026-10-15 | Created from P-1 in INV-01 | Mazen |