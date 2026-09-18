# AI Usage Policy
| Field | Value |
|---|---|
| Owner | Mazen Malas (Operations & Evidence Lead) |
| Backup | Khumonyun (Operations & Evidence Lead) |
| Last updated | 2026-09-18 |
 
## 1. Purpose
 
Team 4 allows AI tools in this project. This policy sets the conditions for that use: AI work must be disclosed, reviewed by a person, verified, and owned by a named team member. The goal is that every AI-assisted artifact in this repository can be traced to a person who understands it and is accountable for it.

## 2. Core Principles
 
1. **A human owns everything.** The team member who commits AI-assisted work is its author and is responsible for its correctness. "The AI wrote it" is never an explanation for a defect.
2. **Disclose, don't hide.** AI assistance is normal and allowed. Undisclosed AI assistance is a policy violation.
3. **Verify before trusting.** AI output is treated as an unreviewed draft from an unknown contributor.
4. **Understand what you submit.** A member must be able to explain any AI-assisted work they commit, without the tool.
5. **Protect data and secrets.** Nothing sensitive goes into an AI tool (see Section 6).

## 3. Approved AI Tools
 
- Claude
- ChatGPT
- GitHub Copilot
- Other tools may be added by PR to this list before use.

## 4. Allowed Uses
 
AI tools may be used for:
 
- Brainstorming project ideas, features, and requirements
- Drafting or editing documentation (charters, policies, READMEs, meeting summaries)
- Explaining concepts, errors, libraries, or course material
- Suggesting repository structure, Git commands, or workflow setup
- Generating or refactoring code, once implementation begins
- Drafting test cases and identifying edge cases
- Reviewing code or documents for errors, clarity, or style

## 5. Prohibited Uses

AI tools may **not** be used to:

- Commit output that no team member has read and understood
- Fabricate engineering evidence, such as meeting notes for meetings that didn't happen, invented test results, or backdated decisions
- Replace a required human review (e.g., using AI approval in place of a PR review)


## 6. Data, Privacy, and Security
 
Never paste the following into an AI tool:
 
- API keys, bot tokens (e.g., Telegram bot tokens), passwords, or `.env` contents
- Personal data of real users of our application (names, usernames, chat IDs, food or health logs)
- Other students' private information 
- Instructor materials the course does not permit sharing outside Sakai
- If a secret is accidentally exposed to an AI tool or committed to the repo please notify the team.

## 7. Disclosure Requirements

Any AI use that produces content committed to the repository (documents, code, tests, or configuration) must be disclosed with an AI-Use Log entry and a note in the PR description.

**AI-Use Log.** Entries go in [`/docs/ai/ai-use-log.md`](ai-use-log.md), using the format defined there by the log owner.

**Pull requests.** The PR description states whether AI was used, which tool, and what for. The PR template in `/.github/` includes a checkbox for this.

**Code comments.** When a block of code is mostly AI-generated, mark it with a short comment, for example:
`# AI-assisted (Claude), reviewed by <name>`

## 8. Review and Verification
 
Before AI-assisted work is merged:
 
1. **The author** reads every line, removes anything they cannot explain, and checks facts, links, file paths, and version numbers against real sources.
2. **For code**, the author runs it and runs relevant tests. AI-suggested libraries must be confirmed to exist and be maintained (AI tools sometimes invent package names).
3. **A reviewer other than the author** approves the pull request under the team's normal review rules. Reviewers may ask the author to explain any AI-assisted section.
4. **For documents**, the author confirms the content reflects what the team actually decided or did, not what the AI assumed.

## 9. Ownership and Accountability
 
- The committing member is the author of record for AI-assisted work.
- Reviewers share responsibility for obvious problems they approve.
- If AI-assisted work is later found to be wrong, it is fixed like any other defect: open an issue, correct it, and note it in the AI-Use Log if the error came from AI output.

## 10. Violations
 
If undisclosed or unverified AI work is found:
 
1. The finder raises it privately with the author, or with the Operations & Evidence Leads.
2. The author adds the missing disclosure or verification, or reverts the work.
3. Repeated issues are escalated to the Team Lead and handled under the Working Agreements.

## 11. Policy Changes

Any team member can propose a change to this policy through a pull request. Changes follow the team's normal review process, and the team is notified in the group chat when the policy changes.

## 12. Team Acceptance
 
Each member accepts this policy by filling in their row through a commit or PR approval under their own GitHub account.
 
| Member | Role | Accepted (Y/N) | Date |
|---|---|---|---|
| Victoria | Team Lead | | |
| Bazid | Planning & Process Lead | | |
| Adiya | Architecture & Development Lead | | |
| Sophail | Quality & Review Lead | | |
| Mazen Malas | Operations & Evidence Lead | Yes | 9/18/2026 |
| Khumonyun | Operations & Evidence Lead | | |