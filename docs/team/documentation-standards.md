# Documentation Standards
 
| Field | Value |
|---|---|
| Owner | Mazen Malas (Operations & Evidence Lead) |
| Backup | Khumonyun (Operations & Evidence Lead) |
| Last updated | 2026-09-18 |
 
These standards keep our repository consistent so anyone can find and trust our documents.
 
## Format and Location
 
- All documents are Markdown (`.md`) and go in the matching `/docs/` folder: `team/`, `requirements/`, `planning/`, `ai/`, or `decisions/`.
- Don't create empty folders or placeholder files.
## File Names
 
- Lowercase with hyphens, no spaces: `risk-register.md`.
- If the course names a file (like `ai-policy.md` or `teamcharter.md`), use that exact name.
## Document Header
 
Every document starts with a title and a small table listing the **Owner**, **Backup**, and **Last updated** date (YYYY-MM-DD).
 
## Writing
 
- Write for someone who wasn't in the meeting: include names, dates, and specifics.
- Use relative links between files, like `[AI Policy](../ai/ai-policy.md)`.
- Mark unfinished work with `TODO:` so gaps are visible, not hidden.

## Changes
 
- Commit messages start with a type and a short description: `docs: add risk register`.
- AI-assisted documents follow the [AI-Use Policy](../ai/ai-policy.md).
 