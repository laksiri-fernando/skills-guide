---
name: run-standup-writer
description: >
  Run, drive, test, or smoke-check the standup-writer skill in this repo.
  Use when asked to run the standup-writer skill, verify it works, check it
  triggers and returns the right format, lint its SKILL.md, or screenshot/
  demo its output. Triggers on "run standup-writer", "test the skill",
  "does the standup skill work", "validate the skill".
---

# Run: standup-writer

This repo has **no application** — it is a tutorial on authoring Claude Code
skills, plus one example skill, `standup-writer`. So the thing to "run" is the
skill itself, and the only system that runs a skill is **Claude Code reading
it**. The driver therefore exercises the skill end-to-end by feeding a standup
prompt to `claude -p` and asserting the output comes back in the skill's
required `**Yesterday:** / **Today:** / **Blockers:**` format.

Paths below are relative to the repo root (`skills-guide/`).

## Prerequisites

Already present in this environment; no `apt-get` needed.

- `node` (v22 here) — runs the driver.
- `claude` CLI (v2.1.118 here) — the runtime that loads and follows the skill.
  Must be authenticated. The driver shells out to it.

## Run (agent path) — the driver

The driver is [.claude/skills/run-standup-writer/driver.mjs](driver.mjs). Run
it from the repo root.

Fast structural lint only (no LLM, no network, no cost) — checks the
frontmatter has `name`/`description`, that `name` matches the folder, that the
three format markers are documented, and that the file is under 500 lines:

```bash
node .claude/skills/run-standup-writer/driver.mjs --lint
```

Full live drive — lints, then invokes the skill via `claude -p` and asserts the
output contains all three format markers:

```bash
node .claude/skills/run-standup-writer/driver.mjs
```

Drive with your own standup input:

```bash
node .claude/skills/run-standup-writer/driver.mjs "Yesterday I fixed the payment webhook, today I'm writing integration tests."
```

Exit code `0` = pass, `1` = `FAIL: <reason>`. Expected output of a passing
live run:

```text
lint OK — standup-writer, 32 lines, all format markers present
> claude -p (cwd=/home/laksiri/my/lessions/agent-skills/skills-guide)
---- output ----
**Yesterday:** Built the login screen
**Today:** Implementing the login service
**Blockers:** None
----------------
drive OK — output matched the standup format
```

## Run (manual path)

To exercise the skill by hand without the driver, run from the repo root so
`claude` discovers `.claude/skills/standup-writer/`:

```bash
claude -p "Use the standup-writer skill. Yesterday I built the login screen, today I'm doing the login service. Write my standup."
```

It prints the standup directly. In an interactive session, `/standup-writer`
also invokes it.

## Gotchas

- **Three copies of the skill, and they drift.** The skill exists at
  `standup-writer/SKILL.md`, `.claude/skills/standup-writer/SKILL.md`, and
  `.agents/skills/standup-writer/SKILL.md`. As of this writing the first two
  are byte-identical but the `.agents/` copy differs (`md5sum` them to confirm).
  `claude` loads the `.claude/skills/` copy — that's the one the driver lints
  and the only one that affects behavior. Editing only `standup-writer/` at the
  repo root changes nothing about how the skill runs.
- **No screenshot — there is no GUI.** "Driving" this skill means asserting on
  the text `claude -p` returns. The captured output block above is the
  equivalent artifact.
- **The live run is non-deterministic and costs tokens.** The wording varies
  run to run ("doing" vs "Implementing"); only the three bold markers are
  asserted, never exact prose. Use `--lint` in tight loops and CI; reserve the
  full drive for confirming the skill still triggers and formats correctly.

## Troubleshooting

- `FAIL: output missing required markers` — the skill didn't trigger or changed
  format. Re-run; if it persists, check that `.claude/skills/standup-writer/SKILL.md`
  still documents `**Yesterday:**`/`**Today:**`/`**Blockers:**`.
- `could not run claude` / non-zero claude exit — the `claude` CLI isn't on
  `PATH` or isn't authenticated. Run `claude --version`, then `node driver.mjs --lint`
  (which needs neither) to confirm the rest of the driver is fine.
