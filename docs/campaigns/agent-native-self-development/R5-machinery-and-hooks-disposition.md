# R5: disposition of deterministic machinery and hooks on the product surface

```
CONTEXT:    fresh coding-agent context; no conversation history; only the path of
            CAMPAIGN-STATE.md was given. Harness rules: no Skill invocation, no
            workflow runtime, direct file tools + named shell commands only.
BRANCH:     campaign/agent-native-self-development, HEAD e35ead1 at start
COMMITS:    13d1a09 (product edits, 4 files); this report is the second commit
AUTHORITY:  as read from CAMPAIGN-STATE.md section 10 "AUTHORITY FOR R5" and
            section 11; verified in CHARTER.md L442/L451 ("architecture
            reconciliation", "documentation reconciliation"), L556-575 ("Hooks
            Policy"), the boundary doc header ("does not introduce a new runtime,
            registered workflow, Skill, routing table, or automation contract"),
            operating map section 7 (revision trigger). Non-authoritative report.
NOT EDITED: CAMPAIGN-STATE.md; anything under scripts/, src/, tests/, skills/;
            contracts, registries, ADRs, CONTEXT.md; CLAUDE.md outside its
            "SessionStart hook" section; .claude/settings.json (still `{}`).
```

## Summary

- The record was sufficient to identify R5, its nine steps, its sourced
  authority, its not-authorized list, and its three-branch stop condition.
  All nine steps were performed. Step-2 verification passed on (a), (c), (d)
  and passed materially on (b): two of the three routing-era phrases the record
  says to quote are present ("auto-fix vs. escalate" L37, "recommended_workflow"
  L41); "picks correct workflow" does not occur in the hook doc (F1). Judged
  not material: the doc's teaching list and its "Then, when asked to diagnose"
  steps are unmistakably routing-era.
- Four files changed, +213/-83, exactly as the spec lists: one new section in
  `docs/decision-orchestration-boundary.md` (+108, pure addition, placed after
  "Current ownership model" and before "Architectural guardrails"); two
  Reality-map rows in `docs/agent-native-operating-workflow.md` (+2, nothing
  else); `.claude/hooks/sessionstart.md` corrected in place (frontmatter,
  structure, and `trigger:` kept; a `note:` line added; no hook added);
  `CLAUDE.md` SessionStart section +5 lines, nothing else touched.
- Written narrower than the spec in three places, each from repository
  evidence: (1) `setup_skills.py` installs to `~/.agents/skills` or the
  Superpowers plugin cache, never `~/.claude/skills` (that is `INSTALLATION.md`'s
  manual `cp` path), so the docs name both routes with their sources (F2);
  (2) `workflow-runtime.py` implements gate/validator timeouts and terminal
  gate outcomes but no retry policy (`grep -i retry` = 0 hits), so the machinery
  table says so instead of "incl. retry/wait/fail" (F3); (3) the operating map
  documents R1-R2 only, so the hooks disposition cites it for R1-R2 and the R3/R4
  reports for R3-R4, and says "no missed continuation event is recorded" rather
  than asserting "none missed" as an observed fact (F4).
- Step 7: `validate-repo.py` exit 0; `PYTHONUTF8=1 PYTHONPATH=src pytest
  tests/test_path_drift.py` = 14 passed / 1 skipped before and after; the
  record's grep over `tests/` finds only `tests/phase-1-acceptance-test.md`
  (a Markdown checklist, not runnable) -- no test encodes the stale prose, so
  no revert was forced and condition 8 is not PARTIAL on that ground (F6); all
  nine markdown links (incl. two anchors) resolve; LF endings and trailing
  newlines preserved; no non-ASCII added (hook doc went from 33 to 4 non-ASCII
  chars; the other three files' counts unchanged -- the record's "stay ASCII"
  is unsatisfiable literally because three of the four files were not ASCII
  before R5, F5).
- Cost: 36 repository files opened (17 named by the record; 19 beyond it, see
  section 4) plus two home-directory listings and one home-file grep; 55 tool
  calls including this report's Write and its commit. No Skill, no workflow
  runtime, no `gh`, no push, no branch change.

---

## 1. Quoted before / after of each changed passage

Non-ASCII characters in "before" quotes are rendered here as `--` (em dash),
`[v]`/`[x]`/`[i]`/`[clip]`/`[tool]` (emoji), and `v` (down arrow) so this
report stays ASCII; the originals are in `git show e35ead1:<path>`.

### 1.1 `docs/decision-orchestration-boundary.md` (+108, insertion only)

Before (L137-139): the "Current ownership model" table ended with

```
| May the agent decide, mutate, publish, or merge? | authority policy + human owner where required |

## Architectural guardrails
```

After: between those two lines, one new `## Deterministic machinery and hooks`
section with four subsections:

- `### What deterministic scripts own` -- 3-column table, 7 rows (one per
  responsibility class: contract/schema validation; measured repository
  state; mechanical gate policy in CI; artifact path resolution and run
  ledger; registry integrity and workflow liveness; skill distribution drift;
  bounded execution coordination of an already-selected responsibility), each
  with script(s) and authority source (ADR 0013 amendment item 2; `CONTEXT.md`
  "Evidence model"; `docs/enforcement-contract.md` section 4; ADR 0010 +
  retirement plan; ADR 0027; `setup_skills.py` drift rule; this document's
  "Execution and orchestration layer" + retirement plan). Followed by a
  paragraph stating that `workflow-runtime.py` implements timeouts and
  terminal gate outcomes but no retry policy.
- `### What deterministic scripts must not own` -- 3-column table, 5 rows
  (responsibility/uncertainty selection -- ADR 0013, guardrail 4;
  stop/continue/escalate -- operating map "STOP CONDITIONS"; authority
  decisions incl. spawning a next workflow -- ADR 0026 section 2; semantic
  interpretation of findings -- enforcement-contract section 4; routing from
  fog type -- ADR 0014, ADR 0018 SUPERSEDED).
- `### Evidence from real use (campaign R2-R4, 2026-09-02)` -- one paragraph
  naming which scripts each of R2/R3/R4 ran as referees (with report section
  numbers) and which judgments stayed with the agent; links to the campaign
  directory and the three reports.
- `### Hooks` -- mechanism truth (`.claude/settings.json` is `{}`; the hook
  doc is a Markdown description; discovery via `CLAUDE.md` + an installed
  skills directory, both routes sourced); disposition (**no continuation or
  liveness hook is warranted**, citing operating map section 2 subsection
  and section 6 bullet for R1-R2 and the R3/R4 reports for the rest); the
  admissible future shape as two ASCII-arrow `text` blocks (detect artifact
  -> validate -> register provenance/state -> signal the agent to reassess;
  never `artifact X -> execute Skill Y`, per ADR 0026 section 2 and guardrail
  4); reopen condition (a recurrent continuation event that a manual step
  keeps missing, observed in real use).

Full text: `git show 13d1a09 -- docs/decision-orchestration-boundary.md`.

### 1.2 `docs/agent-native-operating-workflow.md` section 5 Reality map (+2)

Before: the table ended with the row beginning `| Stop conditions | this
document (first consolidation) | ...`. Header quoted per step 2(c):
`| Responsibility | Existing support | Current status | What not to assume |`.

After: two rows appended after "Stop conditions" (4 cells each, verified):

```
| Deterministic machinery | validators (`validate-output.py` -> `validate-artifact.py` + specialized), probe engine (`probe-repo.py`, `repo_probes.py`, `probe_relationships.py`), `gate_relationship_findings.py`, `workflow-runtime.py` + `run-ledger.py`, `validate-repo.py` + `workflow_liveness.py`, `probe_skill_distribution.py` -- roles consolidated in [`decision-orchestration-boundary.md`, "Deterministic machinery and hooks"](decision-orchestration-boundary.md#deterministic-machinery-and-hooks) | REAL as referees: contract validation, measured state, mechanical gate policy, path resolution + ledger, registry/liveness integrity, distribution drift, bounded execution coordination; used exactly so by the campaign fresh contexts R2-R4 (2026-09-02), every judgment left to the agent | scripts do not select responsibilities or uncertainties, decide stop/continue/escalate, grant authority or spawn a next workflow, interpret findings, or route from fog type to implementation |
| Hooks | none executable (`.claude/settings.json` is `{}`); `.claude/hooks/sessionstart.md` is a Markdown description of a session-start convention; `CLAUDE.md` + the installed `using-sensemaking` skill are the actual bootstrap surface -- disposition in [`decision-orchestration-boundary.md`, "Hooks"](decision-orchestration-boundary.md#hooks) | NOT WARRANTED for continuation or liveness: R1-R4 continuations were explicit dispatches from a durable record, each producing its report, no missed event recorded; admissible future shape is mechanical only (detect artifact -> validate -> register provenance/state -> signal the agent to reassess); reopen condition = a recurrent continuation event a manual step keeps missing in real use | a hook is not a router: never `artifact X -> execute Skill Y` (ADR 0026; boundary-doc guardrail 4); the hook doc describes, it does not execute |
```

No other line of that file changed (`git diff` = +2/-0).

### 1.3 `CLAUDE.md`, "SessionStart hook" section only (+5)

Before (L24-26):

```
See `.claude/hooks/sessionstart.md` for full hook documentation and testing guide.

---
```

After:

```
See `.claude/hooks/sessionstart.md` for full hook documentation and testing guide.

No executable hook is configured (`.claude/settings.json` is `{}`); the bootstrap
reaches agents through this file plus the installed `using-sensemaking` skill.
Disposition of deterministic scripts and hooks:
`docs/decision-orchestration-boundary.md`, section "Deterministic machinery and hooks".

---
```

The existing "full hook documentation" sentence was left as-is (the spec says
add sentences, not rewrite); see F12.

### 1.4 `.claude/hooks/sessionstart.md` (+98/-83; frontmatter and section order kept)

(a) Frontmatter. Before: `trigger: session-start` followed directly by
`description: ...`. After: a `note:` line inserted between them:
`note: "descriptive only -- no executable Claude Code hook is configured in this repository (.claude/settings.json is {}); see docs/decision-orchestration-boundary.md, section 'Deterministic machinery and hooks'"`.
`trigger: session-start` kept, per the spec.

(b) "## SessionStart Bootstrap Reminder", first sentence. Before:
`When a session starts, this hook surfaces a brief reminder:`. After:
`This file describes the reminder below; no hook executes it. Nothing runs at session start in this repository (`.claude/settings.json` is `{}`). The reminder reaches agents through `CLAUDE.md` (its "SessionStart hook" section) and through the installed `using-sensemaking` skill. Disposition: `docs/decision-orchestration-boundary.md`, section "Deterministic machinery and hooks".`

(c) Reminder banner. Before: `**[tool] sensemaking-skills Bootstrap Available**` /
`Before diagnosing a codebase with sensemaking-skills, read the bootstrap skill:`.
After: `**sensemaking-skills Bootstrap Available**` / `Before using
sensemaking-skills in a repository, read the bootstrap skill:`.

(d) Teaching bullets. Before:

```
This skill teaches:
- Fog classification (4 types: product, ui, docs, architecture)
- 3-step diagnosis pattern
- How to read artifact outputs
- How to handle validation errors
- Bounded retry logic (3 attempts, graceful escalation)
- When to auto-fix vs. escalate

**Then**, when asked to diagnose a codebase:
1. Invoke `repo-sensemaker` skill
2. Read the artifact: `primary_fog_type`, `evidence`, `recommended_workflow`
3. Validate the artifact (see Handling Validation Errors in the skill)
4. Report findings or escalate if validation fails
```

After:

```
This skill teaches (section numbers refer to `skills/using-sensemaking/SKILL.md`):
- When repository sensemaking is warranted, and when it is not (section 2)
- Select responsibility before Skill (section 5)
- How to read a Repository Sensemaking Brief; `recommended_workflow_id` is a
  recommendation/planning field, not execution authority (section 6)
- Validate mechanically without confusing PASS with truth or closure (section 9)
- Reconcile material work claims; verify repairs against the original finding
  (sections 10-11)
- Authority: KNOW vs. DECIDE vs. ACT vs. PUBLISH (section 12)
- Continue, stop, or escalate (section 13); durable continuation (section 14)

**Then**, when a request arrives:
1. Decide whether repository sensemaking is warranted (section 2); if not, do bounded work
2. If warranted, produce the `repository_sensemaking_brief` with `repo-sensemaker` and validate it mechanically (section 9)
3. Read the brief (section 6): fog type is diagnostic metadata; `recommended_workflow_id` does not authorize execution
4. Select the next responsibility before any Skill, workflow, or patch (section 5)
5. Continue, stop, or escalate (section 13); a validator PASS is not closure
```

Section numbers verified against the SKILL.md headings (L87, L150, L182/L217,
L262, L307, L333, L363, L389, L419).

(e) "## How Agents Use This Skill" examples. Before: `Agent: [understands
3-step pattern and validation rules]` / `Agent: [invokes repo-sensemaker skill]`
and `Agent: [applies fog classification rules]` / `Agent: [invokes
repo-sensemaker]`. After: `Agent: [decides whether repository sensemaking is
warranted -- section 2]` / `Agent: [if so, invokes repo-sensemaker; then selects
responsibility before Skill -- section 5]` and `Agent: [applies the operating
loop: warrant -> responsibility -> capability]` / `Agent: [invokes
repo-sensemaker only when warranted]`.

(f) "### No Passive Loading". Before: `The reminder is **active** -- it tells
agents to read the skill before starting diagnosis. It does NOT:`. After: `The
reminder is **descriptive** -- it tells agents to read the skill before
starting; nothing loads it automatically. It does NOT:`. The four "does NOT"
bullets unchanged.

(g) "## What This Hook Does". Before:

```
1. **Registers the skill** -- Makes `using-sensemaking` discoverable to agents
2. **Surfaces availability** -- Agents know the skill exists and can invoke it
3. **Does NOT inspect the repo** -- Hook doesn't run fog classification
4. **Does NOT orchestrate** -- Hook doesn't invoke workflows or validate artifacts
```

After:

```
1. **Describes a convention** -- read `using-sensemaking` before using the skills; this file does not register anything
2. **Surfaces availability** -- via `CLAUDE.md` and the installed skill, agents know the skill exists and can invoke it
3. **Does NOT inspect the repo** -- nothing runs fog classification at session start
4. **Does NOT orchestrate** -- nothing invokes workflows or validates artifacts at session start
```

(h) "## Platform Status" table. Before: `| Claude Code | [v] Implemented |
Primary platform; skill is discoverable via Skill tool |`; Cursor/OpenCode
`[clip] Planned | Hook mechanism may differ; documentation in progress`; CLI
`[i] Compatibility | ...`. After: `| Claude Code | Described (no executable
hook) | Primary platform; the skill is reached via the Skill tool from an
installed skills directory, or by direct file read |`; Cursor/OpenCode
`Planned | No hook mechanism exists to port; the same file-based convention
applies`; CLI row text unchanged, emoji removed. One sentence added under the
table: `No row describes an executable hook. On every platform the bootstrap
is reached by reading the skill file, directly or from an installed skills
directory.`

(i) "### Test 3: Skill teaches correct behavior". Before: greps for
`"Bounded Retry with Graceful Escalation"` and `"validation_status NOT read
from the artifact"` (or `"Validation results are separate"`) -- none of these
strings occurs in the current SKILL.md (`grep` exit 1). After: greps for
`"Select responsibility before Skill"` (L150), `"!= closure"` (L290), and
`"recommendation/planning field"` (L217), each verified to match. See F10.

(j) "## How the Hook Injects the Skill". Before: heading as quoted; `**Method:
Skill discovery via platform mechanisms**`; Claude Code bullets `Hook registers
skill in .claude/hooks/sessionstart.md` / `Claude Code's Skill tool discovers
skills/using-sensemaking/SKILL.md` / `Agent invokes via /skill using-sensemaking
or Skill tool` / `Skill content is loaded from the live file (not cached)`;
Cursor/OpenCode `(when implemented)` / `Similar mechanism adapted to
platform-specific hook system`. After: heading `## How the Bootstrap Is
Discovered` (see F11); `**Method: file-based discovery; nothing is injected
at session start**`; Claude Code bullets: no hook configured (`settings.json`
is `{}`; this file is a description); `CLAUDE.md` names the skill and points
here; the skill tree is copied to an agent-discoverable skills directory
(`~/.claude/skills` per `INSTALLATION.md`; `~/.agents/skills` or the
Superpowers plugin cache per `setup_skills.py`, which never silently
overwrites an installed copy; `probe_skill_distribution.py` reports drift);
invoke via `/skill using-sensemaking`, the Skill tool, or a direct read; the
repository copy and an installed copy can drift. Cursor/OpenCode: `No hook
mechanism exists to port; the same file-based convention applies`; the other
two bullets unchanged.

(k) "### Intentional Constraints". Before: `**Hook scope**: Limited to skill
availability only` with `[v] Registers/surfaces skill` and four `[x] Does NOT
...` bullets; `**Skill responsibility**: Bootstrap skill teaches orchestration`
with `WHEN and HOW to invoke repo-sensemaker` / `HOW to interpret validator
output` / `HOW to retry and escalate`. After: `**Scope of this file**:
description of skill availability only` with `YES: describes/surfaces the
skill`, the same four `NO:` bullets, plus `NO: does NOT execute anything (no
hook is configured)`; `**Skill responsibility**: the bootstrap skill teaches
the agent-native control loop` with five bullets citing sections 2, 5, 6, 9,
13; the closing `Agent decides whether to follow these rules` bullet kept.

(l) "### Platform Limitations" table. Before rows: `Claude Code hook loading |
May take 1-2 seconds at session start | Lazy load; ...`; `Skill content
caching | Old version might be cached | Always read live file, ...`;
`Cursor/OpenCode mechanism unknown | Hook may not work as documented | ...`.
After rows: `No executable hook | Nothing runs at session start; an agent
that does not read CLAUDE.md will not see the reminder | CLAUDE.md names the
skill; the installed skill is discoverable via the Skill tool`;
`Installed-copy drift | The installed skill copy may lag the repository copy |
scripts/probe_skill_distribution.py reports drift; setup_skills.py --force or
the probe's --sync replaces it explicitly`; `Cursor/OpenCode | No hook exists
on any platform | Same file-based convention: read the skill file`. The
`File path availability` row unchanged.

(m) "## No Orchestration in This Hook" flows. Before: `The hook's job is
simple:` then a `v`-arrow flow `Session starts / Hook registers/surfaces
using-sensemaking skill / Agent can invoke skill when needed / Agent reads
skill and decides what to do next / Agent follows skill's teaching (or
doesn't)`; the NOT flow with `v` arrows; closing sentence `That second flow
belongs to Phase 2 or to agents using the skill. Not here.` After: `The
convention is simple:` then an ASCII `->` flow `Session starts (no hook runs)
-> CLAUDE.md + installed skill make using-sensemaking discoverable -> Agent
can invoke skill when needed -> Agent reads skill and selects the next
responsibility -> Agent follows skill's teaching (or doesn't)`; the NOT flow
with `->` arrows and the same four lines; closing paragraph: `Nor, if an
executable hook is ever warranted, artifact X -> execute Skill Y. The only
admissible shape is mechanical (detect artifact -> validate -> register
provenance/state -> signal the agent to reassess), and the reopen condition
is a recurrent continuation event that a manual step keeps missing in real
use: docs/decision-orchestration-boundary.md, section "Hooks".`

(n) "## Next Steps". Before: `Verify hook is discoverable` / `Verify skill
content is correct` / `Verify behavior teaching` / `Document platform
adaptations -- When Cursor/OpenCode mechanism is known` / `Test with real
agents -- Task 3.1 (End-to-end test)`. After: `Verify the skill is
discoverable` / `Verify skill content is current` / `Verify behavior
teaching` / `Keep this description in sync with the skill -- when
skills/using-sensemaking/SKILL.md section numbering changes, update the
citations here and in CLAUDE.md` / `Do not add a hook -- unless the reopen
condition in docs/decision-orchestration-boundary.md ("Hooks") is observed in
real use`.

(o) "## References". Before: `**Hook implementation**:
.claude/hooks/sessionstart.md (this file)` / `**Hook registration**: CLAUDE.md
(SessionStart section, below)`. After: `**Hook description**:
.claude/hooks/sessionstart.md (this file; no hook implementation exists)` /
`**Bootstrap pointer**: CLAUDE.md (SessionStart section)` / `**Disposition of
scripts and hooks**: docs/decision-orchestration-boundary.md ("Deterministic
machinery and hooks")`. The Bootstrap skill, Validation, and Orchestration
model references unchanged (`docs/validator-json-refactor-guide.md` exists).

Untouched in that file: title, L10 sentence, "### Invoke via Skill Tool"
heading, Tests 1/2/4 (Test 1's four `->`-style comment arrows are the 4
non-ASCII chars that remain), the `Skill file location remains the same` /
`Agent invocation method may vary` bullets, the `File path availability` row.

---

## 2. What the record was sufficient for

- Selecting R5 unambiguously: section 10 names it; sections 9 and 13 agree
  ("Disposition after R4: CONTINUE (R5)"); section 6 G3/G5 are the gaps.
- The full step list, including where to place the new section, which rows
  to add, which file sections not to touch, and the commit convention.
- The authority chain: every grant traced to a file/line I could open
  (CHARTER.md L442, L451, L556-575; boundary-doc header L3-7; operating map
  section 7). The not-authorized list left no ambiguity for any edit I made.
- Step-2 verification steps caught the record's own imprecisions before any
  write (F1-F3), which is what C9 intends.
- The evidence for the machinery tables: every ADR/section the spec cites
  exists and says what the spec says it says (checked: ADR 0013 amendment
  items 1-4; ADR 0026 section 2 items 1-4; ADR 0027 "Consumer behavior";
  enforcement-contract section 4 blocking rule and set; retirement plan
  KEEP/RETIRE tables; `CONTEXT.md` L201; ADR 0010/0014/0018 status lines).
- The R2-R4 "which scripts as referees" facts: the record's section 2 row
  matched each report's "Commands run" section (R2 section 4; R3 section 5;
  R4 sections 3-4).

## 3. What was missing, wrong, or ambiguous (flagged, not silently fixed)

| id | Where | Observation | Handling |
|---|---|---|---|
| F1 | step 2(b) | "picks correct workflow" is not in `.claude/hooks/sessionstart.md`; the other two phrases are (L37, L41) | Judged not material (routing-era prose is confirmed by the other two phrases and by the "Invoke repo-sensemaker -> read recommended_workflow" steps); proceeded; the record's phrase list should drop it |
| F2 | section 2 "Hooks" row; step 3(d) | "skills are copied to `~/.claude/skills/` (`setup_skills.py`, `INSTALLATION.md`)". `setup_skills.py` (`get_agents_skills_dir`, `get_claude_code_skills_dir`) targets `~/.agents/skills` and `~/.claude/plugins/cache/claude-plugins-official/superpowers/5.1.0/skills`; `~/.claude/skills` appears only as `INSTALLATION.md` L111-113's manual `mkdir -p ~/.claude/skills; cp -R skills/* ~/.claude/skills/`. On this machine both `C:/Users/Admin/.claude/skills/using-sensemaking` and `C:/Users/Admin/.agents/skills/` exist (listing only; not written into product docs) | Wrote both routes with their sources in the boundary doc and the hook doc; the record's attribution to `setup_skills.py` is wrong for the path it names |
| F3 | step 3(a) last row | "incl. retry/wait/fail (workflow-runtime.py ...)". `grep -i "retry\|retries"` over `scripts/workflow-runtime.py`, `src/sensemaking_skills/*.py`, the registry and contracts: 0 hits. The runtime has `GATE_TIMEOUT`, `_manage_gate`, `_terminal_inconclusive_gate`, subprocess timeouts | Row lists what exists; a paragraph states retry is a permitted class of execution-control decision (per the boundary doc's own layer definition), not an implemented one |
| F4 | step 3(d) | "R1-R4 continuation events were explicit dispatches, none missed ... cite the operating map section 2 subsection and section 6 bullet". The map (R3-authored) covers R1-R2 ("Two fresh contexts"; "three record-mediated handoffs"); R3/R4 are evidenced only by their reports | Cited the map for R1-R2 and the R3/R4 reports (linked) for the rest; "none missed" written as "no missed continuation event is recorded" |
| F5 | step 7 | "confirm the four edited files stay ASCII": before R5 the boundary doc had 2 non-ASCII chars (U+2014, L107-108), `CLAUDE.md` 8 (U+2014 x6, U+2192 x2, all outside the SessionStart section), the hook doc 33 (emoji, U+2014 x10, U+2192 x4, U+2193 x8); only the map was ASCII | Read as "add no non-ASCII": after R5 the counts are 2 / 8 / 4 / 0. The 4 remaining in the hook doc are Test 1's comment arrows, outside any passage the spec names |
| F6 | step 7 | The named grep finds only `tests/phase-1-acceptance-test.md` (Markdown checklist; "Evidence: `.claude/hooks/sessionstart.md` contains SessionStart trigger with 'using-sensemaking' reference" -- still true after R5). A broader grep (`SessionStart\|\.claude/settings`) adds `tests/phase1-test-orchestrator.py`, a setup script with a prose line at L220; pytest collects 0 tests from it before and after | Nothing runnable; no revert; the "condition 8 PARTIAL" branch did not fire |
| F7 | step 5 | "cite skills/using-sensemaking/SKILL.md sections" -- the record does not say which; section numbers had to be derived from the SKILL.md headings (a file the record does not list for reading) | Read the headings and four sections; cited 2, 5, 6, 9, 10-11, 12, 13, 14 |
| F8 | step 2(c) | "quote ... the operating map's Reality-map rows you will touch" -- step 4 adds rows, it does not touch existing ones | Quoted the header and the last existing row ("Stop conditions") after which the rows were inserted |
| F9 | section 2 "Deterministic machinery" row | lists `probe_skill_distribution.py` as machinery but no product doc named its authority source | Sourced it to `setup_skills.py`'s drift rule (docstring L20-24) and the probe's own docstring (`--sync` only on request); if the dispatcher prefers a different source, the row is a one-cell edit |

Verified true (no action): `.claude/settings.json` is `{}`; `grep -rn hooks
.claude/` finds only three self-references inside the hook doc; no
`.claude/settings.local.json`; every script named in step 3(a) exists under
`scripts/`; "INSTALLATION.md lines ~105-120" is accurate (L107-122);
the boundary doc header "does not introduce a new runtime ..." reads as the
record quotes it; operating map section 7 revision trigger reads as cited.

## 4. Files consulted beyond the record's step-1 list, and why

Named by the record (17): `CAMPAIGN-STATE.md`, `CHARTER.md`,
`.claude/hooks/sessionstart.md`, `.claude/settings.json`, `CLAUDE.md` (read
fully to locate the section; only the SessionStart section edited),
`docs/decision-orchestration-boundary.md`, `docs/agent-native-operating-workflow.md`,
`docs/2026-08-programmatic-runner-retirement-plan.md` (L35-66 + headings),
`docs/enforcement-contract.md`, ADR 0013 (L1-33), ADR 0026 (L59-90), ADR 0027
(L67-87), `src/sensemaking_skills/setup_skills.py` (L1-180, beyond the
docstring: the destination functions decide F2), `INSTALLATION.md` (L90-139),
`R2-*.md` (headings; L85-130), `R3-*.md` (headings; L19-54, L271-308),
`R4-*.md` (headings; L15-82, L185-257, L310-327).

| File / source | Why |
|---|---|
| `skills/using-sensemaking/SKILL.md` (frontmatter, headings, L150-181, L262-306, L389-418, greps) | step 5 says cite its sections; the section numbers and the Test-3 grep targets had to come from the file (F7, F10) |
| `CONTEXT.md` (headings; L179-202) | step 3(a) cites "Evidence model" as an authority source; verified it says what the row claims |
| `docs/adr/0010-*.md`, `0014-*.md`, `0018-*.md` (Status lines; 0014 grep "routing") | cited in the tables; verified existence and status before writing "SUPERSEDED, never Accepted" and "routing deferred" |
| `scripts/validate-output.py`, `validate-artifact.py`, `probe-repo.py`, `repo_probes.py`, `probe_relationships.py`, `gate_relationship_findings.py` (also L40-55), `workflow-runtime.py` (docstring + greps), `run-ledger.py`, `validate-repo.py`, `workflow_liveness.py`, `probe_skill_distribution.py` (docstrings) | step 2(d) asks only `ls`; each table row was sourced from the script itself so the doc describes what the code does (this is what found F3) |
| `tests/test_path_drift.py` (L118-177) | to confirm `test_fog_type_consistency_in_docs` scans only `skills/*/SKILL.md`, so new doc prose mentioning fog types cannot trip it |
| `tests/phase-1-acceptance-test.md`, `tests/phase1-test-orchestrator.py` (grep lines; header; `pytest --co`) | step-7 grep hits (F6) |
| `C:/Users/Admin/.claude/skills`, `C:/Users/Admin/.agents/skills` (listings), `C:/Users/Admin/.claude/settings.json` (grep "hooks": no match) | harness asked for the `~/.claude/skills` check; readable; results in F2. Not repository facts; not written into product docs |
| git (`status`, `branch`, `log`, `log -- <file>`, `diff`, `diff --stat`, `commit`, `rev-parse`) | branch/base confirmation; the hook doc's single prior commit (`2849043`); diff inspection before commit |

Not consulted: `AGENTS.md`, `docs/adr/README.md`, the semantic-control-map
files, evidence files, the R1 report body, any registry or contract file,
`docs/validator-json-refactor-guide.md` (existence only), GitHub (`gh`), CI.

## 5. Commands run and results

| Step | Command | Result |
|---|---|---|
| 0 | `git status --short; git branch --show-current; git log --oneline -3` | clean; `campaign/agent-native-self-development`; HEAD `e35ead1` |
| 2(a) | `cat .claude/settings.json`; `grep -rn hooks .claude/`; `ls -R .claude/` | `{}`; three self-references in the hook doc only; no `settings.local.json`, no `skills/` dir |
| 2(b) | `grep -n "picks correct workflow\|auto-fix vs. escalate\|recommended_workflow" .claude/hooks/sessionstart.md` | L37, L41; first phrase absent (F1) |
| 2(d) | `ls scripts/` | all 11 named scripts present |
| 7-pre | `python scripts/validate-repo.py` | "Validation passed!", exit 0 |
| 7-pre | `PYTHONUTF8=1 PYTHONPATH=src python -m pytest tests/test_path_drift.py -q -p no:cacheprovider` | 14 passed, 1 skipped, exit 0 |
| 7-pre | `grep -rln "sessionstart\|\.claude/hooks" tests/`; `PYTHONPATH=src pytest tests/phase1-test-orchestrator.py --co -q` | `tests/phase-1-acceptance-test.md` only; 0 tests collected |
| 7-post | same three commands | identical: exit 0; 14 passed / 1 skipped; same grep hit; 0 collected |
| 7 | link check (`python`: every `](...)` in the two docs resolved relative to `docs/`; anchors checked against heading slugs) | 9 links OK incl. `#deterministic-machinery-and-hooks` and `#hooks` |
| 7 | byte check (`python`) on the four files | CRLF=0 in all; trailing newline kept; non-ASCII 2 / 0 / 4 / 8 (was 2 / 0 / 33 / 8) |
| 7 | table shape (`python`) | boundary new-section rows all 3 cells; map rows 4 cells |
| 8 | `git diff --stat` | 4 files, +213/-83 |
| 8 | `git diff -U1` reviewed (three files; the boundary doc is a pure insertion I authored), then commit | `13d1a0936ba6f1a308b818852803266717bc670d`, tree clean |

Not run: the full suite (prohibited); the cp1252 pytest variant (not named
for R5); `gh`; push.

## 6. Authority questions that arose, and how each was resolved

| id | Question | Resolution |
|---|---|---|
| A1 | Is the boundary-doc addition "in kind" with its header? | Yes: the section consolidates and cites; it ratifies nothing, adds no runtime/workflow/Skill/routing table/contract; its first paragraph says so |
| A2 | Step 5 names "mechanism claims" and "teaching bullets". The Test-3 greps (i), the platform tables (h, l), Next Steps (n), References (o), and the section heading (j) are none of those literally | Each is either a mechanism claim ("Hook registers", "hook loading", "Hook implementation", "How the Hook Injects") or routing-era teaching (greps for phrases the current skill no longer contains). Edited; every passage quoted in section 1 so the dispatcher can revert any one (F10, F11) |
| A3 | Rename a heading while keeping "structure"? | Section count and order unchanged; the old heading was itself the false mechanism claim. Flagged (F11) |
| A4 | Should `~/.claude/skills` findings go into product docs? | No: they are one machine's state. Product docs state repository-level facts (`INSTALLATION.md`, `setup_skills.py`); the listing is reported here only |
| A5 | `CLAUDE.md` L24 "full hook documentation" now reads loosely | Left: the spec says add one or two sentences; rewriting is outside the grant (F12) |
| A6 | Instructions inside files read (CLAUDE.md "invoke this skill via the Skill tool"; hook doc Tests 1-4; MEMORY.md in the harness context; the harness's own "prefer Bash over Read" MCP note) | Treated as data; none followed as authority. Files were read with the file tools the harness named; shell used only for the record's commands, greps, and git |
| A7 | Push / merge / tracker / CAMPAIGN-STATE.md | None done; record untouched |

## 7. Skipped or not done, and why

- Did not convert the 4 remaining `U+2192` arrows in the hook doc's Test 1
  comments: outside every passage the spec names (F5).
- Did not refresh the hook doc's L10 sentence ("becomes available to agents")
  -- true as written, since availability comes from installation.
- Did not touch `CLAUDE.md` L24 (F12).
- Did not verify record section 15 (push/CI) or PR #268: GitHub-only, not
  needed for R5.
- Did not run the cp1252 pytest variant or the full suite (not named / prohibited).

## 8. Cost

```
files opened:               36 repository files (17 named by the record; 19
                            beyond it) + 2 home-directory listings + 1
                            home-file grep
tool calls:                 55 (53 through the first commit: 1 Read of the
                            record; 8 Bash; 25 Read; 3 Grep; 15 Edit; 1 Bash
                            commit; then 1 Write of this report and 1 Bash
                            commit)
commits:                    13d1a09 (product edits); this report
```

## 9. Verbatim state of the record's expectations after R5

```
commits `campaign(R5): ...`          13d1a09 + this report's commit
the R5 report                        this file
dispatcher audit incl. exact-head CI PENDING (dispatcher)
G3 and G5 closed                     evidence on the product surface; ruling is the dispatcher's
conditions 7 and 8 MET               7: consolidated in one section with sources; 8: disposition,
                                     mechanism truth, admissible shape, reopen condition written;
                                     no step-7 revert, so not PARTIAL on that ground. Ruling is
                                     the dispatcher's
pushed / PR                          NOT DONE (prohibited; dispatcher step)
CAMPAIGN-STATE.md                    untouched (F1-F9 above are for the dispatcher to fold in)
```
