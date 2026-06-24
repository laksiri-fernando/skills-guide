# Skills Guide

## How to Write Your Own Skills for Claude Code
Skills are instruction files that teach Claude how to handle specific tasks — like a cheat sheet Claude reads before tackling a job. Here's the full process from scratch.

## What Is a Skill?
A skill is a folder containing a SKILL.md file (and optionally scripts, references, and assets). When you ask Claude to do something, it checks available skills, reads the relevant one, and follows its instructions.

```text
my-skill/
├── SKILL.md          ← required: the brain of the skill
├── scripts/          ← optional: reusable code Claude can run
├── references/       ← optional: docs Claude can look up
└── assets/           ← optional: templates, fonts, etc.
```

### Step 1 — Decide What Your Skill Does

Before writing anything, answer these questions:

What task should this skill help Claude do? (e.g., "generate weekly status reports", "convert CSVs to formatted Excel files")

When should it trigger? What phrases would a user type? (e.g., "write a status update", "make a report")

What should the output look like? A file? A specific format? Plain text?


### Step 2 — Create the Folder and SKILL.md

Make a folder named after your skill (use lowercase with hyphens):

```bash
mkdir my-skill
touch my-skill/SKILL.md
```

Open SKILL.md and start with the required YAML frontmatter at the very top:
```markdown
---
name: my-skill
description: >
  Use this skill when the user wants to [do X]. Triggers when the user
  mentions [keywords], asks for [type of output], or needs [specific context].
  Always use this for [scenario] even if they don't say it explicitly.
---

# My Skill

Brief explanation of what this skill does and why.

## When to use it
[Explain the scenarios]

## Steps
1. Do this first
2. Then do this
3. Output should look like this

## Output format
ALWAYS use this structure:
[describe the format]

## Example
Input: "Make me a weekly report for the dev team"
Output: A markdown report with sections: Summary, Completed, Blockers, Next Steps
Key rule: The description in the frontmatter is what makes Claude decide to use the skill. Make it descriptive and slightly "pushy" — list the keywords and scenarios clearly.
```

### Step 3 — Write Good Instructions Inside the Skill

Think of the body of SKILL.md as instructions you'd give to a smart human assistant. Tips:

Use imperative language — "Always include a summary section", "Never skip the output format"
Give examples — show what good input/output looks like

Explain the why — "Include a summary because stakeholders skim reports"

Keep it under ~500 lines — if it's longer, split content into references/ files and tell Claude when to read them


### Step 4 — Test It

Come up with 2–3 realistic prompts a real user would type, like:

"Write a status update for the backend team"

"Generate a sprint report from these notes"

Try them out and see if Claude reads your skill and follows the instructions correctly. Ask yourself:

Did Claude trigger the skill when it should have?

Did the output match what you described?

Were any steps missed or unclear?


### Step 5 — Iterate and Improve

Based on your tests, refine the skill:

If Claude didn't trigger the skill → improve the description with more keywords and trigger phrases

If Claude followed instructions incorrectly → add clearer steps, examples, or explicit "ALWAYS/NEVER" rules

If the output wasn't quite right → define the format more precisely, maybe with a template

Repeat until you're happy with the results.

### Step 6 — Install the Skill

Skills go in a skills/ directory that Claude Code has access to. The exact path depends on your Claude Code setup, but typically:

```bash
~/.claude/skills/my-skill/SKILL.md
```

Or package it as a .skill file if you want to share it.

Quick Reference: Skill Structure

| Part | Required? | Purpose |
|------|-----------|---------|
| name (frontmatter) |✅ Yes | Identifies the skill |
| description (frontmatter) | ✅ Yes | Tells Claude when to use the skill |
| Body of SKILL.md | ✅ Yes| The actual instructions | 
| scripts/ folder | Optional | Reusable code Claude can execute | 
| references/ folder | Optional | Extra docs Claude loads when needed | 
| assets/ folder | Optional | Templates, fonts, static files |

### A Simple Example — "Daily Standup Skill"
```markdown
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
```

### Deploy skill

```bash

# claude code
gh skill install laksiri-fernando/skills-guide standup-writer --agent claude-code

# opencode
gh skill install laksiri-fernando/skills-guide standup-writer --agent opencode
```