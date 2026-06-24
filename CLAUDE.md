# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

A documentation/tutorial repository that teaches how to author Claude Code Skills. There is no build system, no tests, and no application code — content is plain Markdown.

- [README.md](README.md) — the full guide: the 6-step process for writing a skill, the required folder layout, and the SKILL.md frontmatter contract.
- [standup-writer/SKILL.md](standup-writer/SKILL.md) — a worked example skill referenced by the README.

## The SKILL.md contract (the core domain knowledge here)

A skill is a folder whose only required file is `SKILL.md`. Optional sibling folders: `scripts/` (runnable code), `references/` (docs Claude loads on demand), `assets/` (templates/static files).

`SKILL.md` must open with YAML frontmatter containing exactly two required keys, followed by the instruction body:

```markdown
---
name: my-skill           # lowercase-with-hyphens, matches the folder name
description: >            # what makes Claude decide to invoke the skill
  Use this skill when... Trigger on phrases like "...".
---
```

When editing or creating skills in this repo, keep these conventions (they are the lessons the README is teaching — stay consistent with them):

- `name` is kebab-case and matches the containing folder name.
- `description` is the trigger signal: list concrete keywords/phrases and scenarios, and lean slightly "pushy" so Claude actually invokes it.
- Body uses imperative ALWAYS/NEVER rules, includes at least one input→output example, and explains the *why* behind format rules.
- Keep `SKILL.md` under ~500 lines; overflow goes into `references/` with an explicit instruction telling Claude when to read it.

## Adding a new example skill

Create `skill-name/SKILL.md` mirroring `standup-writer/` — folder name in kebab-case matching the frontmatter `name`. If the README enumerates examples, update it to reference the new skill so the guide and the examples stay in sync.
