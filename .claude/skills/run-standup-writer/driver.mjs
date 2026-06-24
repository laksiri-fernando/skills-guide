#!/usr/bin/env node
// Driver for the standup-writer skill.
//
// The "app" being driven here is Claude Code itself reading the skill.
// There is no server or binary — so we drive the skill the only way it
// is ever exercised: feed a standup prompt to `claude -p` and assert the
// output comes back in the skill's required format.
//
// Two modes:
//   node driver.mjs --lint            structural check of SKILL.md (fast, no LLM, no cost)
//   node driver.mjs                    lint + live invocation via `claude -p` (network + cost)
//   node driver.mjs "yesterday X, today Y"   live invocation with a custom standup input
//
// Run from the repo root. Paths below are resolved relative to this file,
// so the cwd does not matter.

import { readFileSync, existsSync } from "node:fs";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import { dirname, resolve } from "node:path";

const here = dirname(fileURLToPath(import.meta.url));
const repoRoot = resolve(here, "../../.."); // .claude/skills/run-standup-writer -> repo root
const SKILL = resolve(repoRoot, ".claude/skills/standup-writer/SKILL.md");

const REQUIRED_MARKERS = ["**Yesterday:**", "**Today:**", "**Blockers:**"];

function fail(msg) {
  console.error(`FAIL: ${msg}`);
  process.exit(1);
}

// ---- structural lint -------------------------------------------------------
function lint() {
  if (!existsSync(SKILL)) fail(`SKILL.md not found at ${SKILL}`);
  const src = readFileSync(SKILL, "utf8");

  const fm = src.match(/^---\n([\s\S]*?)\n---/);
  if (!fm) fail("no YAML frontmatter block (--- ... ---) at top of SKILL.md");
  const front = fm[1];

  const name = front.match(/^name:\s*(\S+)/m);
  if (!name) fail("frontmatter missing `name:`");
  if (name[1] !== "standup-writer")
    fail(`frontmatter name is "${name[1]}", expected "standup-writer" (must match folder)`);

  if (!/^description:/m.test(front)) fail("frontmatter missing `description:`");

  for (const m of REQUIRED_MARKERS)
    if (!src.includes(m)) fail(`SKILL.md body does not document the "${m}" format marker`);

  const lines = src.split("\n").length;
  if (lines > 500) fail(`SKILL.md is ${lines} lines (>500; split into references/)`);

  console.log(`lint OK — standup-writer, ${lines} lines, all format markers present`);
}

// ---- live drive ------------------------------------------------------------
function drive(input) {
  const prompt =
    `Use the standup-writer skill. ${input} Write my standup.`;
  console.log(`> claude -p (cwd=${repoRoot})`);
  const r = spawnSync("claude", ["-p", prompt], {
    cwd: repoRoot,
    encoding: "utf8",
    timeout: 180_000,
  });
  if (r.error) fail(`could not run claude: ${r.error.message}`);
  if (r.status !== 0) fail(`claude exited ${r.status}\n${r.stderr || r.stdout}`);

  const out = (r.stdout || "").trim();
  console.log("---- output ----");
  console.log(out);
  console.log("----------------");

  const missing = REQUIRED_MARKERS.filter((m) => !out.includes(m));
  if (missing.length) fail(`output missing required markers: ${missing.join(", ")}`);
  console.log("drive OK — output matched the standup format");
}

// ---- main ------------------------------------------------------------------
const args = process.argv.slice(2);
lint();
if (args.includes("--lint")) process.exit(0);

const custom = args.filter((a) => !a.startsWith("--")).join(" ");
const input =
  custom || "Yesterday I built the login screen, today I'm doing the login service.";
drive(input);
