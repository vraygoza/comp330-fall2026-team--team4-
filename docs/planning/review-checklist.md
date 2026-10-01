# Peer Review Checklist

Project: Calorie Counter Telegram Bot  
Team: Team 4 (COMP 330, Fall 2026)  
Owner: Sohail (Quality & Review Lead)  

## 1. Review Policy and Rules
To keep our codebase and documentation consistent, every pull request must be reviewed before it is merged into main.

- Rule: No self-merging. The author of a pull request cannot approve or merge their own work.
- Trigger: Opening any pull request triggers an independent review.
- Reviewer Assignment: The author assigns one primary reviewer when opening the PR.
- Backup / Exception Route: If the assigned reviewer does not respond within 24 hours, the author must tag Sohail (Quality Lead) or Victoria (Team Lead) in the group chat to step in as backup reviewer. In emergency deadline situations, the Team Lead can approve the PR with an explanatory comment on GitHub.
- 48-Hour Target: All PRs should be submitted for review at least 48 hours before the official Sakai deadline so the team has time to review without rushing.

## 2. PR Review Checklist
Reviewers should copy this checklist into their PR review comment on GitHub:

### Review Verification
- [ ] Addresses the assigned issue (linked with Closes # or Refs #).
- [ ] No extraneous changes outside the issue scope.
- [ ] Code follows project conventions and formatting.
- [ ] No hardcoded secrets, bot tokens, or personal food logs (.env used).
- [ ] Basic tests or verification steps are included and pass.
- [ ] Error messages for bad inputs or lookup failures are clear.
- [ ] Any related documentation or AI use log entries are updated.

Reviewer verdict: [Approved / Changes Requested]
Notes: