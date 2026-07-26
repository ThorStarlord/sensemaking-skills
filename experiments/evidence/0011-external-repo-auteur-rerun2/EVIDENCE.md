# Evidence: External-repo validation rerun #2 (post both infrastructure fixes)

This experiment reruns the `architectural-review-planning-workflow` external
validation against `auteur` at a pinned commit, now that BOTH previously
discovered blocking bugs are fixed and merged:

- issue #68 / PR #69 (merged) — `validate-brief.py` resolves citations
  against `target_repo`, not just `repo_root`.
- issue #71 / PR #72 (merged) — the live repo-sensemaker prompt explains the
  required `quote`/`supports_claim` evidence-excerpt fields and the
  logic-trace requirement.

## Relationship to prior attempts

- **PR #67** (pre-fix): failed on citation resolution — validator looked in
  `repo_root` instead of `target_repo`. Left untouched, historical evidence.
- **PR #70** (post-first-fix only): citation bug fixed, but failed on missing
  `quote`/`supports_claim` evidence-excerpt fields and missing logic-trace
  paragraph. Left untouched, historical evidence.
- **This run (rerun #2)**: both fixes present. Investigates whether the
  underlying workflow now produces a *substantively* sound brief, not just a
  structurally valid one.

## Commits under test

- Framework (source clone): `H:\GithubRepositories\sensemaking-skills` @
  `ce840263ad8cbada3e7bf71203b424c253a5cccd` (main, includes PR
  #57/#59/#60/#62/#64/#65/#66/#69/#72)
- Target: `auteur` @ `b40db654e0df9e90074f7ad85b40d7362378e07d` (pinned,
  same commit as the failed PR #67 attempt; auteur's HEAD has since moved on)

## Fresh, disposable clones used (distinct from all prior attempts)

- Framework: `H:\scratch\sensemaking-external-exp3-framework`
  (own `.git`, independent of primary repo; absent from
  `git worktree list` of the primary checkout; HEAD =
  `ce840263ad8cbada3e7bf71203b424c253a5cccd`; clean before run)
- Target: `H:\scratch\auteur-target-readonly-3`
  (checked out to `b40db654e0df9e90074f7ad85b40d7362378e07d`; clean before
  and after the run)

Sentinels verified present in the fresh framework clone before running:
`skills/`, `scripts/workflow-runtime.py`, `scripts/skill_executor.py`,
`docs/mode-coverage.yaml`, `.git/`.

`scripts/skill_executor.py` `allowed_tools` for the executor subagent:
`["Read", "Write", "Glob", "Grep"]` — no Bash/PowerShell available to the
model, confirmed by direct read of the fresh clone's source (not memory).

## Stage A — external live Step 1

Command:
```
python scripts/workflow-runtime.py "Analyze this external repository, identify the weakest architectural boundary affecting reliable development or operation, and produce an evidence-grounded repository sensemaking brief. Do not modify the target repository." \
  --workflow architectural-review-planning-workflow \
  --mode guided_execution \
  --executor claude-code \
  --gate-decision auto-approve \
  --target-repo H:/scratch/auteur-target-readonly-3 \
  --repo-root H:/scratch/sensemaking-external-exp3-framework \
  --log-dir H:/scratch/sensemaking-external-exp3-framework/exp3-logs-stageA
```
PID 16791, launched from the fresh framework clone. Runtime: ~4m03s
(started 08:47:46, process exited by t=243s in the polling loop). Exit
observed via direct PID liveness polling (`ps -p 16791`), not delegated.

Session ID: `orchestration-20260726-084748-e26480bc`.

### Result

- Step 1 (`repo-sensemaker`) executed exactly once, produced
  `artifacts/05-orchestration-run/repository_sensemaking_brief.md`.
- The real, unmodified `validate-and-report.py` validator (target-repo-aware
  per PR #69, evidence-field/logic-trace-aware per PR #72) **passed on the
  first model-produced artifact**, no manual repair. (`[OK] Validation
  passed (0.7s)`)
- Gate `review_diagnosis` auto-approved.
- Step 2 (`architectural-review`) correctly halted with
  `ARTIFACT_NOT_FOUND: ... requires 'proposed_direction' ...` — this is the
  expected, by-design precondition for Stage B (a hand-authored
  `proposed_direction.md` must be supplied before Step 2 can run). This is
  NOT a Stage A failure; it is Stage A behaving exactly as designed.
- Target repo (`auteur-target-readonly-3`) confirmed unchanged throughout:
  `git status --short` empty and HEAD unchanged at every poll tick (ticks
  1-9, ~30s apart) and at final check.
- Framework clone integrity: `git status --short` shows only
  `docs/mode-coverage.yaml` (expected bookkeeping — session id, run log
  path, gate counts) modified, plus new untracked `artifacts/05-...` and
  `exp3-logs-stageA/` directories. No tracked file outside
  `docs/mode-coverage.yaml` changed. See `mode-coverage.diff`.
- **Denied-write near-miss (PR #67 concern) did not recur** in this run: no
  PreToolUse event was observed targeting a path inside the target clone at
  all (the allowed_tools set for the executor subagent is Read/Write/Glob/Grep,
  and the only Write activity landed inside the framework session directory,
  consistent with `expected_output_path` confinement). No mutation occurred
  in the target clone at any point.

**Stage A classification: EXTERNAL LIVE STEP 1 PROVEN** (structurally —
see evidence-quality audit below for the substantive caveat that stops the
campaign before Stage B).

## Evidence-quality audit (mandatory, independent re-check of this run's brief)

The brief's central "weakest boundary" claim: layers 8 (Modulation) and 9
(Theme/Resonance) of the 9-Layer Structural Engine are "declared" (via enum
and `_LAYER_ORDER` display list) but have "no active diagnostic rules" and
are never generated by `run_all_diagnostics()` — classified as a
"Ghost Features" weakness.

| Claim | Citation | Exists | Supports claim | Contradiction found | Notes |
|---|---|---|---|---|---|
| `state_check()` displays all 9 layers via `_LAYER_ORDER` | `src/auteur/structure/state.py` L185-195 | Yes, verbatim match | Yes | No | Accurate citation. |
| `run_all_diagnostics()` only calls `analyze_structure()` (docstring says "Layers 1-5"), `audit_bible_locations()` (L6), `audit_outline_carriers()` (L7) | `src/auteur/structure/analyzer.py` L21-63 | Yes, verbatim match | **No — misleading** | **Yes** | `run_all_diagnostics()` does call exactly those three (plus optional cross-layer) functions, but the docstring's claim that `analyze_structure()` only covers "Layers 1-5" is **stale relative to the function's actual body**. `analyze_structure()` (same file, lines 66-1140) itself emits `DiagnosticLayer.THEME` diagnostics at line 336 (`theme.thesis_unrepresented`) and `DiagnosticLayer.MODULATION` diagnostics at line 1115 (`modulation.pov_underutilized`), and calls `_add_layer9_resonance_diagnostics()` internally (line 1099, function defined at line 1407) which adds further THEME diagnostics. These are real, reachable diagnostic rules for layers 8 and 9, invoked unconditionally from within `analyze_structure()`, which IS called by `run_all_diagnostics()`, which IS called by `state_check()`. |
| Docstring "Currently runs: Layers 1-5... Layer 6... Layer 7" confirms layers 8/9 are "not currently validated" | `src/auteur/structure/analyzer.py` L29-35 | Yes, verbatim match | **No** | **Yes** | The model treated a stale docstring comment as authoritative over the actual function body it summarizes. The docstring itself is arguably inaccurate/out of date (it undersells `analyze_structure()`), but that is a *documentation* discrepancy, not proof that layers 8/9 lack validators — the code contradicts the comment. |

**Stronger evidence not cited by the model, found during this audit:**
- `src/auteur/structure/analyzer.py:336` — `DiagnosticLayer.THEME`,
  rule `theme.thesis_unrepresented`.
- `src/auteur/structure/analyzer.py:1099-1115` — calls
  `_add_layer9_resonance_diagnostics(...)` and directly appends a
  `DiagnosticLayer.MODULATION` diagnostic (`modulation.pov_underutilized`).
- `src/auteur/structure/analyzer.py:1407` — `_add_layer9_resonance_diagnostics`
  function definition, which itself appends multiple `DiagnosticLayer.THEME`
  diagnostics (verified at lines 1442, 1468, 1503, 1536, 1575).
- `src/auteur/structure/cartographer_audit.py:234` — another
  `DiagnosticLayer.THEME` diagnostic in the cross-layer path.

None of these are dead code or commented out; they execute unconditionally
(THEME checks) or under simple guard conditions (`if engine is not None`)
inside `analyze_structure()`, which is on the hot path for every
`state check` invocation.

### Usefulness assessment

The brief is well-formed, specific to real file/line citations, and the
mechanical requirements (quote/supports_claim fields, logic-trace paragraph,
`Logic trace:` marker) are all satisfied — this is a genuine improvement over
PR #70's failure mode. However, its **central factual claim is false**: layers
8/9 are not "ghost features" with zero implementation — they have multiple
active diagnostic rules already wired into the code path the model itself
cited. A maintainer reading this brief would be misled into "implementing"
diagnostics that substantially already exist, wasting effort and likely
producing duplicate/conflicting rules. The model's error was trusting a
stale docstring comment over reading the full ~1140-line function body it
was citing — exactly the "stale docs override current code" failure mode
this campaign's audit protocol was designed to catch.

**Evidence-audit classification: STRUCTURALLY VALID, SUBSTANTIVELY
UNSUPPORTED.**

Per protocol, the campaign STOPS here. Stage B (hand-written
`proposed_direction.md`, Step 2 resume) was **not attempted** — proceeding
to plan an implementation response on top of a factually incorrect weakest-
boundary claim would produce an artifact whose validity this audit has
already disproven, and the protocol explicitly requires stopping in this
case rather than manually repairing or reinterpreting the brief.

## Denied-write near-miss

No write attempt targeting the target clone was observed in this run at
all (not even a denied one) — the near-miss noted in PR #67 did not recur.

## Target and framework integrity

- Target (`auteur-target-readonly-3`): unchanged throughout. HEAD
  `b40db654e0df9e90074f7ad85b40d7362378e07d` before, during (checked at
  ~30s polling intervals), and after the run. `git status --short` empty
  at every check.
- Framework clone: intact. Only `docs/mode-coverage.yaml` (expected
  bookkeeping) modified among tracked files; new artifacts confined to
  `artifacts/05-orchestration-run/` and `exp3-logs-stageA/`, both expected
  session/log paths.

## What is (and is not) known after this rerun

Known, narrowly: at commit `b40db654e0df9e90074f7ad85b40d7362378e07d`,
`architectural-review-planning-workflow`'s Step 1 (repo-sensemaker),
running against this one external repository with both infrastructure bugs
fixed, produces a brief that is **structurally valid** (passes the real,
unweakened validator; correct fields; correct file paths; correct citation
resolution against `target_repo`) but is **not substantively trustworthy**
in this instance — its central architectural claim is contradicted by code
in the very file it cites, at line ranges outside the ones quoted.

This is NOT the same finding as "the original implementation transferred
unchanged" (PR #67) or "the evidence-field mechanics are broken" (PR #70).
Both of those infrastructure bugs are confirmed fixed by this run. What
remains open is a *model reasoning/thoroughness* gap — insufficiently
reading a large function body before asserting what it does — that is
orthogonal to both previously fixed bugs and is not modified as part of
this campaign per instructions (report only).

Nothing here generalizes beyond auteur@b40db65 with this one workflow.
Production readiness, cross-repo generality, and other agents/platforms
remain unproven.
