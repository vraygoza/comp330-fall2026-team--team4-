# Quality Plan

Project: Calorie Counter Telegram Bot
Team: Team 4 (COMP 330, Fall 2026)
Owner: Sohail (Quality & Review Lead)

## 1. What Quality Means for This Project
For Cycle 1, our main goals are making sure the bot doesn't crash, gives accurate numbers, and feels smooth for our 10-15 trial users. Since the bot is pretty simple right now (log food -> get calories -> show running daily total), we are focusing on four core things:

- Accurate math and day reset: Calorie counts should add up correctly, and the running total needs to reset at midnight without weird timezone bugs.
- Clear error messages: If someone types gibberish or the calorie lookup fails, the bot shouldn't freeze or go silent. It needs to tell the user what went wrong.
- Privacy and secrets: No bot tokens or real user food logs get committed to GitHub or used in public test files. We keep tokens in a local .env file and use synthetic sample meals for testing.
- Working code on main: Nothing gets merged into main without another team member testing it and reviewing the pull request.

## 2. Quality Checks Before Merging
Before any code or docs get merged, they need to pass through these basic steps:

1. Self-check: The person writing the code runs it locally, checks for clean formatting, and makes sure edge cases (like weird inputs or negative numbers) don't break it.
2. Peer Review: A second team member reviews the PR using our checklist (review-checklist.md).
3. No secrets or personal data: Double-check that no API keys, tokens, or personal logs slipped into the commit.
4. Merge to main: Once approved, the branch is merged and the corresponding GitHub issue is updated.

## 3. Testing Approach

### Unit Tests
We will write unit tests for the parts of the code that don't need a live internet connection:
- Parsing user messages (grabbing "2 slices of pizza" and separating the quantity from the food item).
- Adding up calories and resetting daily totals.
- Handling invalid inputs (blank messages, zero or negative amounts, random non-food text).
- Mocking external API responses so tests run fast without calling the live Telegram or food database APIs.

### Manual and Acceptance Testing
Before we hand the bot over to our classmates and friends to test, we will run through these basic checks manually:
- Send /start and make sure onboarding works.
- Log a basic meal (like "1 apple") and verify the calorie lookup and updated daily total.
- Test bad lookups (typing a made-up food name) to verify the bot asks the user to try again cleanly.

## 4. Definition of Done
A feature or task isn't considered done just because the code is written. It is done when:
1. It meets the requirements described in the issue.
2. It includes basic tests or clear manual steps showing it worked.
3. The PR is reviewed and approved by another team member.
4. Any relevant docs or requirements are updated.