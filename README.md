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

### New Skill with Assets, References and Scripts

Meeting Notes Formatter

#### Folder structure
```text
~/.claude/skills/meeting-notes/
├── SKILL.md              ← main instructions
├── scripts/
│   └── extract_action_items.py   ← script Claude can run
├── references/
│   └── formatting-guide.md       ← detailed rules Claude reads when needed
└── assets/
    └── template.md               ← output template Claude fills in
```

#### The files

`SKILL.md`

```markdown
---
name: meeting-notes
description: Format raw meeting notes into a structured summary. Use when
  the user pastes meeting notes, says "format my notes", "clean up these
  notes", or "summarize this meeting". Extracts action items, decisions,
  and attendees automatically.
allowed-tools: Bash(python3 *)
---

# Meeting Notes Formatter

Turns raw, messy meeting notes into a clean structured summary.

## Steps

1. Read the raw notes the user provides
2. Use the template in [assets/template.md](assets/template.md) as your output structure
3. Follow the style rules in [references/formatting-guide.md](references/formatting-guide.md)
4. Run the action item extractor script for accuracy:

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/extract_action_items.py "$ARGUMENTS"
```

5. Fill in the template with your analysis + the script's extracted action items
6. Output the completed template as a markdown block

## Notes
- If attendees aren't listed, write "Not specified"
- If no decisions were made, write "No decisions recorded"
- Keep the summary under 5 bullet points
```
```

`scripts/extract_action_items.py`

```py
#!/usr/bin/env python3
"""
Scans raw meeting notes and extracts action items as "WHO will WHAT".

Splits the text into sentences (notes are often one long line), then for each
sentence pulls out the actor and the action. Handles:
  - "@alice to update the docs"        -> "Alice will update the docs"
  - "John will send the report by Fri" -> "John will send the report by Fri"
  - "Bob to schedule a call"           -> "Bob will schedule a call"

Decision statements ("Decided to ...", "Agreed to ...") are NOT action items
and are skipped.
"""

import sys
import re

# Verbs that introduce a decision, not an assignment. Used as the leading word
# these would otherwise look like "<who> to <action>", so we exclude them.
DECISION_WORDS = {
    "decided", "agreed", "approved", "rejected", "deferred", "discussed",
    "resolved", "concluded",
}

# Sentence-level patterns. Each captures (who, action).
PATTERNS = [
    # "ACTION: John will send report"
    (re.compile(r"ACTION[:\s]+(?P<who>\w+)\s+(?:will|to|should)\s+(?P<action>.+)", re.IGNORECASE), None),
    # "@alice will/to/should update the docs"
    (re.compile(r"@(?P<who>\w+)\s+(?:will|to|should)\s+(?P<action>.+)", re.IGNORECASE), None),
    # "John will/to/should send the report by Friday"
    (re.compile(r"\b(?P<who>\w+)\s+(?:will|to|should)\s+(?P<action>.+)", re.IGNORECASE), None),
]


def split_sentences(text: str) -> list[str]:
    # Split on sentence terminators and newlines; keep non-empty fragments.
    parts = re.split(r"[.\n!?]+", text)
    return [p.strip() for p in parts if p.strip()]


def extract_action_items(text: str) -> list[str]:
    items = []
    seen = set()
    for sentence in split_sentences(text):
        for pattern, _ in PATTERNS:
            match = pattern.search(sentence)
            if not match:
                continue
            who = match.group("who")
            if who.lower() in DECISION_WORDS:
                break  # a decision, not an action item
            action = match.group("action").strip().rstrip(".")
            who = who.capitalize()
            item = f"{who} will {action}"
            if item.lower() not in seen:
                seen.add(item.lower())
                items.append(f"- {item}")
            break  # first matching pattern wins for this sentence

    return items if items else ["- No action items detected"]


if __name__ == "__main__":
    if len(sys.argv) > 1:
        raw_text = " ".join(sys.argv[1:])
    else:
        raw_text = sys.stdin.read()

    print("## Extracted Action Items\n")
    for item in extract_action_items(raw_text):
        print(item)
```

`references/formatting-guide.md`

```markdown
# Meeting Notes Formatting Guide

Load this file when you need to apply consistent formatting rules.

## Tone
- Use past tense for what was discussed ("The team decided...")
- Use future tense for action items ("Alice will send...")
- Be concise — one idea per bullet

## Dates & Times
- Always write dates as: 24 Jun 2026
- Use 24-hour format for times: 14:30, not 2:30 PM

## People
- Use first names only unless two people share a first name
- If a role is mentioned, add it in brackets: Alice [PM]

## Action Items
- Must include: WHO + WILL DO WHAT + BY WHEN (if stated)
- Example: "Alice will share the Q3 report by Friday"
- If no deadline is given, write: "Alice will share the Q3 report (no deadline set)"

## Decisions
- Start each decision with a strong verb: "Approved", "Rejected", "Agreed", "Deferred"
- Example: "Approved the new onboarding flow design"
```

`assets/template.md`

```markdown
# Meeting Summary

**Date:** {{DATE}}
**Attendees:** {{ATTENDEES}}

---

## Summary
{{SUMMARY_BULLETS}}

## Decisions Made
{{DECISIONS}}

## Action Items
{{ACTION_ITEMS}}

## Next Meeting
{{NEXT_MEETING}}
```

#### Try it
Once installed at `~/.claude/skills/meeting-notes/`, paste some raw notes and say:

```text
Format my meeting notes: "Discussed Q3 launch. John will send the report 
by Friday. @alice to update the docs. Decided to delay the beta by 2 weeks."
```

### Deploy

```bash
# claude code
gh skill install laksiri-fernando/skills-guide meeting-notes --agent claude-code

# opencode
gh skill install laksiri-fernando/skills-guide meeting-notes --agent opencode
```