---
name: standup-writer
description: >
  Use this skill when the user wants to write a daily standup, scrum update,
  or team status message. Trigger on phrases like "write my standup",
  "daily update", "what did I work on", or "team update". Use this even if
  they just say "standup" casually.
---

# Standup Writer

Helps write concise daily standup messages in the standard format.

## Format
ALWAYS use exactly this structure:

**Yesterday:** [What was completed]
**Today:** [What's planned]  
**Blockers:** [Anything blocking progress, or "None"]

## Instructions
1. Ask the user what they worked on if they haven't said
2. Keep each section to 1–3 bullet points
3. Use plain, clear language — no jargon
4. Keep the whole thing under 100 words

## Example
Input: "I fixed the login bug and today I'm working on the dashboard"
Output:
**Yesterday:** Fixed the login authentication bug
**Today:** Working on the dashboard UI
**Blockers:** None