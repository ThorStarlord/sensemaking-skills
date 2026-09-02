# Final campaign report: reliable agent-native, artifact-mediated self-development

```
DATE:        2026-09-02
BRANCH:      campaign/agent-native-self-development (base main @ f10b7da)
PR:          #268 https://github.com/ThorStarlord/sensemaking-skills/pull/268
RECORD:      docs/campaigns/agent-native-self-development/CAMPAIGN-STATE.md
CHARTER:     docs/campaigns/agent-native-self-development/CHARTER.md
AUTHORITY:   non-authoritative campaign report; ratification, merge, and the
             owner decisions listed in section 9 remain the owner's.
FORMAT:      CHARTER.md "Final Campaign Report" (ten sections, one disposition)
CLOSURE:     the fresh-context closure probe (R8b) runs after this file is
             committed; its verdicts are recorded in CAMPAIGN-STATE.md
             section 16 and in R8-closure-probe.md, and summarized in
             section 8 below once audited.
```

## 1. Mission outcome

The mission was to advance Sensemaking Skills toward reliable agent-native,
artifact-mediated self-development: an active coding agent uses repository
evidence and durable artifacts to determine the next warranted responsibility,
select a capability, perform bounded work, validate, preserve authority
boundaries, carry state across responsibilities, and recursively continue.

Achieved, with the limitations in section 9:

- The campaign ran as that loop. One dispatcher context specified each
  responsibility in a durable Markdown record and committed it; a **fresh
  context with no conversation history**, given only the record's path,
  performed the responsibility, validated, committed, and wrote a verbatim
  report; the dispatcher audited the diff against the spec, updated the record,
  and pushed. Eight record-mediated handoffs, seven into fresh contexts, across
  six responsibility classes: reconstruction; mechanical execution;
  judgment-class documentation; implementation-class code + tests; multi-file
  architecture reconciliation; evidence-gathering + classification; and a
  change to the product's own deterministic machinery with regression tests.
- The record proved sufficient in every case. Zero shape failures were
  observed. The record's *facts* were wrong or overstated in twenty-one
  places, and every one was caught by the continuing context because the
  specs carried verification steps and fresh contexts were told to prefer
  repository evidence over the record. None caused a wrong action; twice a
  fresh context declined to force the record's predicted outcome (R4 D2b
  revert; R7 D19 not edited) because doing so would have exceeded its grant.
- The product surface now states what was demonstrated: the operating map
  documents the continuation pattern and the durable state it needs; the
  boundary doc consolidates what deterministic scripts own and must not own
  and what hooks are for; a new disposition document classifies all 23
  registered workflows with pinned evidence; the hook description and
  `CLAUDE.md` are truthful about the absent hook mechanism.
- The charter's candidate architecture was tested against evidence and partly
  rejected: no continuation schema, validator, new artifact type, or hook was
  warranted at this scale (reopen conditions recorded); a Markdown record
  convention with verification-bearing task specs was sufficient and is now
  documented as such.

## 2. Architecture before and after

**Before (main @ f10b7da).** The semantic control model was already explicit:
the active agent owns the loop (ADR 0013); the product boundary is the
human-reviewed brief (ADR 0014); recommendation != selection != execution
authority (ADR 0026); registry identity != liveness (ADR 0027). Continuation
was `CONVENTION_CLOSED` with an untested reopen trigger; nothing represented
repository-level development direction; the role of deterministic scripts was
described across four documents; the "SessionStart hook" was a Markdown
description of a mechanism that does not exist, teaching routing-era
behavior; no per-workflow disposition existed beyond the liveness overlay; one
validator utility could not be imported without `scripts/` on `sys.path`.

**After (campaign head).** The same ratified control model, unchanged: no ADR,
contract, registry, overlay, Skill, CI, or `src/` change. Added on the product
surface:

- responsibility-level continuation from a durable record is documented as
  DEMONSTRATED, with the field set that proved necessary, the failure classes
  observed and their repairs, what was not needed, and reopen conditions
  (`docs/agent-native-operating-workflow.md` section 2 subsection, Reality-map
  rows, section-6 bullet); cross-run prior-report identity is explicitly left
  unresolved;
- one consolidated statement of what deterministic scripts own and must not
  own, with sources, plus the hooks disposition -- no executable hook, none
  warranted, the only admissible future shape is mechanical, reopen condition
  stated (`docs/decision-orchestration-boundary.md`, "Deterministic machinery
  and hooks"; Reality-map rows);
- a per-workflow disposition in campaign vocabulary with pinned evidence and
  nine implied owner decisions, none applied
  (`docs/workflow-system-disposition.md`);
- a truthful hook description and `CLAUDE.md` SessionStart section;
- `scripts/_validator_utils.py` resolves `workflow_liveness` lazily (from
  `sys.path`, then the sibling file), so the module imports in every loading
  mode while liveness enforcement is unchanged;
- the semantic-control-map trial received its first real trigger,
  consultation, over-read, and MECH-refresh events (six stale rows refreshed);
- three test defects repaired; the campaign record, charter, and seven
  verbatim fresh-context reports as durable evidence.

Control model after: unchanged in kind, stronger in evidence. Outer loop
(mission -> capability state -> gap -> bounded task) and inner loop
(task -> steps with verification -> evidence -> validation -> closure) were
carried by one record without conflict for every task size tried; the
numbered step spec with sourced authority, an explicit not-authorized list,
per-branch expected outcomes, and a stop condition *is* the inner-loop state.

## 3. Responsibility trace (as it actually happened)

| # | Context | Responsibility | Outcome |
|---|---|---|---|
| R0 | dispatcher | reconstruct state from durable evidence; record v1; worktree + branch | `2bc8a2c` |
| R1 | fresh | reconstruction probe (7 questions) | Q1-Q5 reconstructed; Q6 partial (narrow `AUTHORITY_AMBIGUITY`); 5 omissions -> charter committed, authority sourced, remote status recorded; `b4335c3` |
| R2 | fresh | mechanical: semantic-control-map bookkeeping (rows SE1/SE2/SA13/SA9, trial log A-D, enforcement-contract addendum) | all steps; caught the record's wrong gate-provenance claim from git; `fa2dd68`, `9160a5b`; close-out refreshed SA10/SA12 + protocol selector `2adfeaf` |
| R3 | fresh | judgment-docs: continuation pattern into the operating map | +88/-3 one file; cross-run identity left unresolved; two record overstatements flagged; `6ff4a89`, `fbbb637`; close-out `09bdf5e` |
| R4 | fresh | implementation-class: D1 (encoding) + D2 (two collection errors) | repair / repair / revert-and-report (fixture drift vs validator); spec tension flagged; `769a180`, `ac47191`; close-out `e35ead1` |
| R5 | fresh | four-file architecture reconciliation: machinery + hooks disposition (boundary doc, operating map rows, hook doc, CLAUDE.md) | +213/-83; three spec assumptions corrected from code (install routes; no retry policy; phrase attribution); `13d1a09`, `c7afb57`; close-out `89246f4` |
| R6 | fresh | workflow-system disposition (rebuild inventory; classify 23; new doc + pointer) | 1 KEEP / 2 DEMOTE / 2 RETIRE_CANDIDATE / 8 HISTORICAL / 10 INSUFFICIENT_EVIDENCE; nine discrepancies vs the dispatcher's inventory; `70648c4`, `5a89f2a`; close-out `eb6c461` |
| -- | dispatcher | reassessment: closure deferred one responsibility (code change so far test-only) | `e702b31` |
| R7 | fresh | product machinery: lazy `workflow_liveness` resolver in `scripts/_validator_utils.py` + regression tests (D12) | +33/-4 and +149; two mode-coverage tests flip green; validator harness 78/78 byte-identical; refused to edit an existing test to satisfy the record's prediction (D19); `79e02c5`, `1b47d06`; close-out `4336a53` |
| R8 | dispatcher + fresh | closure: like-for-like suite, CI, this report, closure probe, PR ready | this commit; probe result in `CAMPAIGN-STATE.md` section 16 |

Dispatcher-side interruptions that were not responsibilities: two stalled
local test runs in the shared checkout (`rglob` over ~76k untracked files),
replaced by clean-worktree runs; discovery that the editable install shadows
worktree `src/` (fixed procedurally with `PYTHONPATH=src`); one shell-quoting
failure while editing the record (redone via a script file).

## 4. Repository changes

Product surface:

| File | Change | By |
|---|---|---|
| `docs/agent-native-operating-workflow.md` | continuation subsection under section 2; Reality-map rows Continuation / Next responsibility selection / Stop conditions updated; rows Deterministic machinery + Hooks added; section-6 bullet; section-1 pointer to the disposition doc | R3, R5, R6 |
| `docs/decision-orchestration-boundary.md` | new section "Deterministic machinery and hooks" (+108) | R5 |
| `docs/workflow-system-disposition.md` | new (+410) | R6 |
| `.claude/hooks/sessionstart.md` | corrected in place (+98/-83); frontmatter `note:`; routing-era prose replaced by pointers to `using-sensemaking` sections | R5 |
| `CLAUDE.md` | SessionStart section +5 lines (mechanism truth + pointer) | R5 |
| `docs/semantic-control-map.md` | MECH refresh of SE1, SE2, SA13, SA9 (R2) and SA10, SA12 (close-out) | R2, dispatcher |
| `docs/semantic-control-map-trial-log.md` | sections A-D populated with real events | R2, dispatcher |
| `docs/semantic-control-map-trial.md` | step-4 pytest selector corrected | dispatcher |
| `docs/enforcement-contract.md` | dated status addendum (gate on `main`; body retained) | R2 |
| `scripts/_validator_utils.py` | lazy `_workflow_liveness()` resolver replaces the hard top-level import (+33/-4); public API unchanged | R7 |
| `tests/test_validator_utils_liveness_import.py` | new (+149): three fresh-interpreter regression tests | R7 |
| `tests/test_path_drift.py` | `encoding="utf-8"` x3 | R4 |
| `tests/test_integration_external_repo.py` | import lines only | R4 |

Campaign evidence (non-authoritative; nothing in `scripts/`, `src/`,
`tests/`, or `.github/` reads it): `docs/campaigns/agent-native-self-development/`
-- `CAMPAIGN-STATE.md` (living record), `CHARTER.md`, `R1-*.md` .. `R7-*.md`,
`R8-closure-probe.md`, this file.

Not changed: ADRs, artifact contracts, canonical vocabulary, both workflow
registries, both liveness overlays, skill registry, Skills, `src/`, CI
workflows, `CONTEXT.md`.

## 5. Evidence for each major architectural claim

| Claim | Evidence |
|---|---|
| A fresh context can reconstruct mission, capability state, task rationale, established-vs-uncertain, next action, and authority from durable state | `R1-fresh-context-reconstruction.md` (Q1-Q5 RECONSTRUCTED, Q6 PARTIAL with the exact missing items; 39 files / 25 calls) |
| A fresh context can perform a bounded responsibility from durable state alone, across responsibility classes | `R2-*.md` (mechanical), `R3-*.md` (judgment docs), `R4-*.md` (code + tests), `R5-*.md` (four-file architecture), `R6-*.md` (evidence + classification), `R7-*.md` (product machinery) -- each with commits, validation output, and cost |
| The record's facts get corrected rather than propagated | R2 M1/F1 (gate provenance), R3 M2/M3, R4 F1/F2, R5 F1-F3, R6 discrepancies 1-9, R7 F1-F5 -- each flagged, written narrower, never silently fixed |
| Authority boundaries hold under continuation | every report's "Authority questions" and "Instructions encountered beyond granted authority" sections: no push, no merge, no tracker write, no ADR/contract/registry/overlay edit, no Skill invocation, `CLAUDE.md` treated as data; R4 and R7 declined out-of-grant edits |
| No continuation schema / validator / new artifact type / hook was warranted | operating map section 6 bullet; boundary doc "Hooks"; campaign record U3/U5 with reopen conditions; zero shape errors across all handoffs |
| Deterministic scripts act as referees; judgment stays with the agent | boundary doc "Evidence from real use"; R2 section 4, R3 section 5, R4 sections 3-4, R7 sections 3-5 |
| Workflow dispositions are evidence-backed | `docs/workflow-system-disposition.md` section 3 (file:line pointers per row), section 8 (evidence limits) |
| Nothing existing was destroyed | `validate-repo.py` exit 0 on every head; `test-validators.py` 78/78 before and after R7; exact-head CI green on every pushed head; like-for-like full suite: 0 NEW failures, 4 FIXED (section 6) |

## 6. Qualification

- **Targeted tests**: every responsibility ran the record-named selections
  under both code pages with `PYTHONPATH=src`; the dispatcher re-ran them at
  each audit (per-R results in `CAMPAIGN-STATE.md` section 3).
- **Full suite, like-for-like** (Windows, Python 3.14, `PYTHONPATH=src`,
  clean worktrees, identical command
  `python -m pytest tests -q -p no:cacheprovider --ignore=tests/integration
  --continue-on-collection-errors`):

  | Head | passed | failed | errors | skipped | xfailed | NEW vs baseline | FIXED vs baseline |
  |---|---|---|---|---|---|---|---|
  | baseline `main @ f10b7da` | 2712 | 54 | 2 | 16 | 5 | -- | -- |
  | campaign `5a89f2a` (after R6) | 2718 | 53 | 1 | 16 | 5 | 0 | 2 (D1; D2a collection error) |
  | campaign `1b47d06` (after R7) | 2723 | 51 | 1 | 16 | 5 | **0** | **4** (D1; D2a; both `test_mode_coverage_aggregation` tests) |

  The remaining 51 failures / 1 error are pre-existing on `main` (record D14:
  platform/environment reds that are green in Linux CI; the D2b collection
  error; D19 now visible with its own assertion instead of the import error).
- **Validators**: `scripts/validate-repo.py` exit 0 on every head;
  `scripts/test-validators.py` 78/78 before and after R7 (output
  byte-identical except the generated timestamp); probe engine run by R2
  (exit 0, evidence-only findings).
- **Lint / type / build**: the repository defines no lint or type-check gate;
  CI's installed-wheel smoke jobs exercise the build (green).
- **CI (exact head, "Validator Ecosystem", 19 jobs)**: green on every pushed
  head: `b4335c3`, `2adfeaf`, `09bdf5e`, `ac47191`, `e35ead1`, `89246f4`,
  `5a89f2a`, `eb6c461`, `e702b31`, `1b47d06`, `4336a53`. The R8 closure
  commits are documentation-only; their CI result is recorded in
  `CAMPAIGN-STATE.md` section 15.
- **Integration state**: **qualified PR head; not integrated.** Merge to
  `main` is an owner decision (repository convention; the charter grants no
  merge authority).
- **Exceptions**: the shared `main` checkout cannot run the full suite in
  reasonable time (two tests `rglob` its ~76k untracked files); the editable
  install shadows worktree `src/` unless `PYTHONPATH=src` is set. Both are
  environment findings (record D11, C11), not product defects.

## 7. Workflow-system disposition

Recorded in `docs/workflow-system-disposition.md` (R6), criteria stated
before the table, evidence pinned per row:

- **KEEP_AS_BOUNDED_SUBGRAPH (1)**: `docs-contract-reconciliation` -- the only
  workflow with a recurring agent-native trace of its full sequence (evidence
  0018, 0019, 0021; the 2026-08-12 and 2026-08-22 artifact sets).
- **DEMOTE (2)**: `artifact-reconciliation` (evidenced two-step core; steps 3-4
  never recorded); `architectural-review-planning-workflow` (internal
  golden-path proof; ADR 0014 defers step 2; runner-era records only).
- **RETIRE_CANDIDATE (2)**: `product-discovery-sprint`, `product-strategy-sprint`
  (active, every step `external_routing` to a deprecated Skill).
- **HISTORICAL (8)**: the ADR 0027 compatibility-only set, not re-decided.
- **INSUFFICIENT_EVIDENCE (10)**: active, implemented Skills, no real execution
  record (plan_only, test-only, or recommendation mentions only).
- **REPAIR (0)**.
- **Migration path / retained roles**: registered workflows stay bounded
  subgraphs entered from the agent-owned loop (operating map section 1);
  nine implied owner decisions (liveness of the two sprints; product-management
  ecosystem posture; `full-local-sensemaking` conditional branch to deprecated
  `discovery`; `setup-sensemaking-skills` registry entry;
  `autonomous-sprint-preflight` purpose; `mode-coverage.yaml` overstated
  claims; `artifact-reconciliation` definition;
  `architectural-review-planning-workflow` description; packaged
  catalog/overlay divergence) are listed, none applied.
- **Left unresolved, with reason**: the ten INSUFFICIENT_EVIDENCE rows (no
  real trace exists; the evidence limits are stated); every ledger with step
  events was produced by the SDK executor removed on 2026-08-13 and cannot be
  reproduced with the retained runtime.

## 8. Artifact-mediated continuation result

**Continuation state that proved necessary** (all in one Markdown record;
none in conversation memory): the mission; a capability-state table with an
evidence pointer per row; known gaps and constraints; every authority grant
traced to a durable source plus an explicit not-authorized list; a task spec
with numbered steps, verification steps, per-branch expected outcomes, stop
condition, commit convention, expected evidence; open uncertainties; deferred
findings; remote/integration status recorded (push, PR, CI); an append-only
trace.

**Could fresh contexts reconstruct it?** Yes. R1 reconstructed all five
substantive questions; R2-R7 performed responsibilities of increasing kind
from the record alone; each report's "What the record was sufficient for"
section lists what it needed and its "Files beyond the record" section shows
that everything else was repository state, mostly named by the record. The
closure probe (R8b) result is recorded in `CAMPAIGN-STATE.md` section 16.

**Failure classes observed**: `AUTHORITY_AMBIGUITY` (narrow; R1) and
`MISSING_DURABLE_STATE` (R1) -- both repaired by making state durable; plus a
class the charter's taxonomy lacks: **durable state present but wrong**
(twenty-one instances, mostly dispatcher-computed evidence and predicted
outcomes), caught every time by in-spec verification. Not observed:
`CAPABILITY_DISCOVERY_FAILURE`, `PRODUCT_DIRECTION_AMBIGUITY`,
`INCIDENTAL_CONTEXT_LOSS`.

**Gaps that remain**: single dispatcher, single repository, one day; cross-run
prior-report identity untested (deliberately); some cited evidence lives only
in GitHub (Issue #218 episodes; CI runs); the largest code change from durable
state is one script plus tests, no `src/` change.

## 9. Remaining limitations

**Known product limitations**
- Continuation is a documented Markdown convention, not a contract; exercised
  by one dispatcher in one repository over one day.
- Cross-run prior-report identity remains `CONVENTION_CLOSED` (never
  exercised).
- Ten registered workflows have no real execution evidence; the runner-era
  ledgers are not reproducible with the retained runtime.
- Goal A external validation remains halted in this environment (Issue #255).

**Engineering debt (deferred, all pre-existing, none in CI)**
- D2(b) `tests/test_validate_brief_json.py`: fixtures predate four validator
  rule families; refresh-vs-retire undecided (U8).
- D19 `tests/test_validator_utils.py::test_load_workflow_registry_loads_yaml`:
  expected dict predates ADR 0027's `liveness` annotation (one-line test fix;
  outside R7's grant).
- D8 `validation.yml` line-14 comment stale; D9 map row SE10 vs probe output;
  D11 two tests `rglob` the repo root; D13 U+2713 prints and one unencoded
  `open()`; D17 `mode-coverage.yaml` overstated `steps_completed`; D18 packaged
  catalog carries 20 of 23 ids and 7 of 8 overrides.
- The local Windows/Python 3.14 suite has ~50 pre-existing reds that are green
  in Linux CI (D14).

**Unvalidated hypotheses**
- That the record convention scales to multiple concurrent dispatchers or to
  responsibilities large enough to need their own task-state files (U2 was
  resolved only "for this campaign's scale").
- That the reopen conditions for schema/validator/hook (a failure on a missing
  or malformed section; more than one producer; a recurrent missed
  continuation event) are the right ones.
- That the R1-R7 substrate observation (isolated sub-agent direct writes
  persist) transfers to the Goal A harness; it holds for this harness only.

**Owner decisions**
1. Merge PR #268 (the whole campaign branch: documentation, one script, three
   test files) -- standing; the campaign's terminal authority boundary.
2. Whether to record the substrate observation on Issue #255.
3. The nine registry/overlay/documentation decisions implied by
   `docs/workflow-system-disposition.md` section 6.

**Environment blockers**
- None for this campaign. (Goal A's substrate blocker is outside its scope.)

**Intentionally deferred**
- No continuation schema, validator, artifact type, or hook (C7 not met;
  reopen conditions recorded).
- No liveness-overlay edits (owner-ratified under ADR 0027).
- No repair of historical documents (roadmap, HARDENING_STATUS, candidate
  snapshots, task docs).
- No edits to existing tests beyond the two R4 repairs (D19 left as found).

## 10. Campaign disposition

```text
CAMPAIGN_COMPLETE
```

Why: the charter defines COMPLETE as "campaign acceptance conditions are
materially satisfied and the resulting repository state is qualified".
Conditions 1-3 were met at the start and are unchanged; 4-9 are met on the
product surface with stated limitations (continuation demonstrated across six
responsibility classes and documented; direction representable and used;
deterministic-script and hook roles consolidated with evidence; workflow
system dispositioned with evidence); 10-12 are met by `validate-repo.py`,
the unchanged validator harness, exact-head CI green on every pushed head,
and a like-for-like full suite with zero new failures; 13 is this report and
`CAMPAIGN-STATE.md` sections 6, 8, 11, 12.

It is not OWNER_DECISION_REQUIRED: no safe bounded work is blocked by an
owner decision; the standing merge decision is the repository's normal
integration boundary, not a campaign blocker. It is not EXTERNAL_BLOCKER or
CAMPAIGN_PREMISE_INVALIDATED: the premise (agent-owned semantic control with
artifact-mediated continuation) was confirmed, and the parts of the candidate
architecture that evidence did not support (schema-constrained continuation
artifacts, hooks) were rejected with reopen conditions rather than forced.
