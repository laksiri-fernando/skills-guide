# AGENTS.md

Plain Markdown documentation repo — no build, test, lint, typecheck, or dev server.

## Structure

```
README.md                           ← the full skill-authoring guide
standup-writer/SKILL.md             ← source copy of example skill
.claude/skills/standup-writer/      ← installed copy (mirrors source)
```

## Key facts

- **No app code, no manifests, no config** — only `.md` files. Editing works in any text editor.
- Two copies of `standup-writer` exist: one at repo root (source), one under `.claude/skills/` (installed). When editing the example skill, update both.
- Adding a new skill: create `skill-name/SKILL.md` matching `name` in frontmatter to folder name, then update `README.md` if the README references the list of examples.
- Deploy command: `gh skill install laksiri-fernando/skills-guide <skill-name> --agent claude-code`

## SKILL.md contract (from README)

- YAML frontmatter with exactly two keys: `name` (kebab-case, matches folder) and `description` (trigger signal — list keywords, be pushy).
- Body uses ALWAYS/NEVER rules, includes input→output example, under ~500 lines.
- Overflow goes into `references/` with explicit instruction telling Claude when to read it.
