# Autonomous Task v2 — Hardening Pass 1

Status: DRAFT. Narrow hardening pass over the 11 draft artifacts produced in
the initial design pass. Does not redesign the experiment broadly. No
main-study task instances constructed. No pilot agent run. Nothing locked or
hashed. No production source code modified. This pass DID modify repository
state at one place only: it created a temporary, isolated git worktree
outside the tracked repository (under the session scratchpad) to inspect the
frozen SHA directly; that worktree is removed at the end of this pass and
touches no tracked file.

## Method note

A detached git worktree was created at exactly `0ffb564b67eb7fcac3c1a2c8a1365ed6b2a0e6c5`
(`git worktree add --detach`, confirmed `git rev-parse HEAD` matches, confirmed
`git status --porcelain` empty — i.e., genuinely clean and at the frozen
revision, unlike the initial design pass's working-tree inspection, which was
85 commits ahead). All findings below marked "frozen-SHA-verified" were
checked directly against that worktree's file contents, not against the
current `main` tip.

---

## 1. T1 re-verification at the frozen SHA

**Correction to the initial design pass: the `build/` directory does not
exist at the frozen SHA at all.** It is a later, untracked build artifact
that only appears in the current (85-commits-ahead) working tree. The
"3-4 physical copies" claim in the original `AUTONOMOUS-TASK-V2-PROTOCOL-DRAFT.md`
§3 was based on the wrong checkout and is retracted.

**Second correction: `skill-registry.yaml` has exactly one copy at the
frozen SHA** (`skills/workflow-planner/references/skill-registry.yaml`). It
is not duplicated. Any T1 instance built around a "which skill-registry copy
is authoritative" trap would not be admissible at this SHA.

**Third correction, more consequential: the originally-proposed "Skill-tool
vs. `workflow-runtime.py` CLI" ambiguity does not qualify as a T1 trap.**
`CONTEXT.md` (frozen-SHA-verified, ADR 0013 section) states explicitly:
"Skills are platform-agnostic: Same skill works whether called by agent
(Skill tool) or CLI (Python import)." The two invocation surfaces are
*designed* to be equivalent, not merely both-plausible. A task built around
this distinction would have no genuine wrong answer for the oracle to
detect — it would fail item 3 of the required checklist ("the wrong route is
genuinely plausible" implies there must actually be a wrong route). This
candidate is dropped, not merely re-labeled.

**What survives and strengthens, frozen-SHA-verified:** `workflow-registry.yaml`
exists in exactly two locations —
`skills/workflow-planner/references/workflow-registry.yaml` and
`src/sensemaking_skills/defaults/workflow-registry.yaml` — and **the two
copies have already diverged in content at the frozen SHA**: the `skills/`
copy contains a workflow (`architecture-implementation-workflow`, an
83-line block) that the `src/defaults/` copy lacks entirely (verified via
`diff`, frozen-SHA-verified). This is not a hypothetical drift risk; it is
an existing, observable fact about the frozen commit.

Tracing the two consumers (frozen-SHA-verified, by reading the actual
loading code, not inferring from file location alone):
- `scripts/_validator_utils.py:_registry_path()` and
  `scripts/workflow-planner.py:load_workflow_registry()` both hardcode
  `skills/workflow-planner/references/workflow-registry.yaml`. This is the
  path read when operating on this repository directly via its local CLI
  scripts (the "dogfood" path).
- `src/sensemaking_skills/registry.py:WorkflowRegistry._load_package_defaults()`
  reads `src/sensemaking_skills/defaults/workflow-registry.yaml` as
  **package defaults**, then merges in a target repository's own registry as
  an override. Its own docstring: "Provides injectable workflow registry
  system that loads package defaults and allows external repo overrides."
  This is the path exercised when `sensemaking_skills` is installed as a
  library and pointed at a *different*, external target repository.

This satisfies every item on the re-verification checklist:
1. Both routes exist at `0ffb564b` — confirmed by direct file read.
2. Both are discoverable — with a caveat: discoverable by reading the two
   Python modules that load each file (both are short, findable via
   `grep`/`Grep` for "workflow-registry.yaml" or "defaults"), but **not**
   documented in any prose doc — `API.md`, `CONTEXT.md`, and `docs/` contain
   zero mentions of "WorkflowRegistry", "package defaults", or
   "defaults/workflow-registry" (frozen-SHA-verified, `grep -rl` returned no
   matches). An agent must read source, not just documentation, to find the
   second route. Recorded as a real but modest caveat, not a blocker: this
   repository's own R0/R1/R2 regime texts already expect source-level
   investigation, and this is squarely within that expectation.
3. The wrong route is genuinely plausible — both files have the identical
   filename `workflow-registry.yaml`; nothing in the name distinguishes
   them.
4. Semantic difference is externally testable — running
   `scripts/workflow-planner.py` locally vs. instantiating `WorkflowRegistry`
   against a target repo already produces two different available-workflow
   lists at this exact commit, which is directly checkable.
5. Success is not inferable from naming alone — confirmed (item 3).
6. No live-network/credential dependency decides the route — confirmed; the
   distinction is purely about which consumer/mode the task's stated intent
   implies (edit-for-local-dogfood vs. edit-for-installed-package-default),
   never about environment state.
7. Oracle can remain route-independent unless the process contract requires
   a mechanism — yes: a CALIBRATION-ONLY example task ("ensure workflow X is
   available to a freshly-instantiated `WorkflowRegistry` pointed at an
   external target repo" vs. "ensure `scripts/workflow-planner.py` run
   locally lists workflow X") states its intended consumer explicitly in the
   process contract, and the oracle checks only the resulting behavior of
   that stated consumer.
8. Freshness relative to prior Autonomous Task work — this specific
   dual-consumer/already-diverged-registry construct was not part of the
   banked Semantic Tool Routing candidate as described in the supplied
   provenance (that candidate is external and undetailed here); it is newly
   grounded in this pass directly against the frozen SHA.

**T1 conclusion: `T1_ADMISSIBLE`**, with the "which mechanism copy is
authoritative for which consumer" construct as the frozen-SHA-verified
substrate, and the Skill-tool-vs-CLI candidate formally dropped.

---

## 2. T2 hardening at the frozen SHA

Frozen-SHA-verified: `tests/test_field_contract_agreement.py` exists at
`0ffb564b` and its own docstring documents a *real prior incident* this repo
already had: "the auto-invocation routing code read the machine field
`fog_type`... but `fog_type` is declared in NO artifact contract... The
validation silently no-op'd and routing could silently fail." This is
strong evidence the T2 substrate is not just structurally plausible but
tied to a genuine, previously-costly invariant this repository already
polices.

Checked against the required properties:
- **Multiple valid solutions exist**: `artifact-contracts.yaml` (687 lines
  at the frozen SHA) has no declared ordering constraint on keys within a
  block or on comment style; a new field declaration can be inserted at
  different valid positions within a contract block and still satisfy the
  test.
- **Success defined by invariant, not reference text**: the test itself
  checks field-name *membership* (is the field the runtime reads declared
  somewhere?), not textual equality with a specific YAML diff — an oracle
  built on this test is inherently invariant-based.
- **Nontrivial reasoning required**: the task requires identifying *which*
  artifact block a given field logically belongs to and *which* of
  `required_machine_fields` vs. a looser declaration is correct — this is
  not literal substitution.
- **Protected regions independently checkable**: structural YAML diff over
  all blocks except the target one is mechanical.
- **Rejects superficially plausible near-misses**: e.g., declaring the field
  under the wrong artifact's block, or misspelling the field name relative
  to what the runtime actually reads, both pass a shallow "file changed,
  looks contract-like" read but fail the actual test.
- **Distinctness from D/D'**: this repository has no visibility into the
  external D/D' task definitions (they are outside this repo, per supplied
  provenance), so distinctness cannot be mechanically confirmed from this
  side — recorded honestly as an open item for whoever holds the D/D'
  definitions to confirm, not asserted.

**T2 conclusion: `T2_ADMISSIBLE`.** No material weakening found; if
anything, the frozen-SHA check surfaced a stronger justification (a real
historical incident) than the initial pass cited.

---

## 3. T3 admissibility — tested, not rescued

Frozen-SHA-verified findings, from reading `scripts/run-ledger.py` and
`scripts/workflow-runtime.py` directly (not merely confirming the ledger
file's existence, which was the initial pass's weaker evidence):

- `append_ledger_event()` in `run-ledger.py` opens the ledger file in
  append (`"a"`) mode and writes one complete JSON line per call. Combined
  with `workflow-runtime.py`'s `for step in steps:` execution loop (multiple
  independent loop sites, e.g. lines 646, 736, 807 at the frozen SHA), a
  process interrupted between steps leaves a syntactically valid, honestly
  partial ledger — not a corrupted one. This directly answers "can a
  realistic partial state be produced without hand-editing" in the
  affirmative at the mechanism level.
- **`workflow-runtime.py` already ships a ledger-audit subcommand**,
  `handle_audit_run(args)` (frozen-SHA-verified), whose logic explicitly
  checks for exactly the invariants a recovery task needs: "Multiple
  'run_started' events found," "Duplicate step_started," "'artifact_created'
  ... after step already completed," and more (`[AUDIT FAIL] ...` messages
  read directly from source). This means a T3 hidden oracle does not need to
  be built from scratch — it can reuse this repository's own existing audit
  logic the same way T2 reuses the field-contract-agreement test, which is
  exactly the kind of "route-independent, capable of contradicting the
  agent" check the protocol requires.

This materially de-risks T3 relative to the initial pass's assessment. What
this pass did **not** do: actually execute `workflow-runtime.py`, kill it
mid-run, and confirm the resulting partial state is agent-solvable and
oracle-checkable end to end. That remains real, unproven construction risk —
the mechanism-level evidence is strong, but "the pieces exist and look
compatible" is not the same as "we produced one working partial state and
recovered from it." Per the explicit instruction not to manufacture an
unrealistic crash solely to preserve T3, this pass stopped at mechanism-level
verification rather than attempting a live interrupt-and-resume outside the
scope of a design-only pass (doing so would mean actually running an
orchestration workflow, which edges toward dispatching a task rather than
designing one).

**T3 conclusion: `T3_CONDITIONALLY_ADMISSIBLE`**, upgraded from the initial
pass's "low-medium confidence" to **medium-high confidence** on the strength
of the append-only write pattern and the pre-existing audit subcommand, but
still gated on the pilot actually performing one real interrupt-and-resume
cycle before either T3 held-out task is built. This is not a rescue by
lowering the bar — it is upgraded confidence from new, specific, frozen-SHA
evidence, with the actual execution proof still deferred to the pilot as
originally planned.

---

## 4. Family-fallback rule — frozen now

Per instruction, this is decided now rather than left implicit.

**Selected: a variant of Option B.** If the T3 pilot cell returns
`T3_NOT_ADMISSIBLE` (i.e., a real interrupt-and-resume attempt fails to
produce a solvable, checkable partial state even once), the main study
proceeds as **T1 + T2 only, with each family contributing three instances
instead of two** (e.g., MEDIUM, HIGH, and a second HIGH-shaped instance
constructed via a distinct wrong-route/invariant-set within that family —
not a trivial rerun of the same shape), preserving 6 paired main-study tasks
total (2 families x 3 instances x 3 regimes = 18 runs, matching the
originally planned run count).

Rejected alternatives and why:
- **Option A (4 tasks, 2 families x 2 levels)** is simpler but was rejected
  because it weakens H4 (complexity-dependent break-even) exactly where T1's
  frozen-SHA evidence turned out strong enough to support a real
  within-family MEDIUM/HIGH comparison — throwing away a third instance pair
  per family for the sake of symmetry with the original plan is not
  justified once T1/T2 are this well-grounded.
- **Option C (require three admissible families or declare the whole
  experiment inadmissible)** was rejected as too strict given T1 and T2
  independently clear every admissibility criterion with frozen-SHA
  evidence; the research question survives fine on two well-grounded
  families, and inventing a synthetic third family under deadline pressure
  would risk exactly the construct-validity problem this hardening pass
  exists to prevent.
- **Replacing T3 with an independently justified new family** was
  considered and rejected for this pass specifically: no candidate was
  found during this pass's inspection that clears the admissibility bar as
  cleanly as the T1/T2 substrates did, and inventing one now would not have
  the frozen-SHA verification rigor applied to T1/T2 above.

Consequences, stated explicitly:
- H1, H2, H5 (efficacy preservation, efficiency improvement, no concealed
  quality loss): unaffected in kind, still testable within either 3-family
  or 2-family-with-3-instances shape, since these are computed per paired
  task instance regardless of family count.
- H3 (escalation efficiency): unaffected.
- H4 (complexity-dependent break-even): under the fallback, tested with 3
  instances per family (MEDIUM Rank 1, HIGH Rank 1, HIGH Rank 2 — per the
  explicit fallback rank mapping frozen in Lock-Readiness Response 2 §1C;
  **correction, per that same response's smaller-issues item 3**: this is
  two complexity *levels* — MEDIUM and HIGH — with one additional HIGH-
  shaped replication, not three distinct complexity levels/points) instead
  of 3 families x 2 levels — this changes what "complexity-dependent" can
  mean (now within-family granularity across MEDIUM and a replicated HIGH,
  instead of a cross-family MEDIUM/HIGH comparison in 3 families) and must
  be reported as a narrower claim if the fallback triggers, not silently
  treated as equivalent to the
  original design.
- Task-family imbalance: the fallback removes one whole failure-mode
  category (`TASK_FAMILY_IMBALANCE` cannot manifest across 3 families if
  only 2 remain) but does not eliminate imbalance risk between T1 and T2
  themselves — that check still applies with 2 categories instead of 3.
- Paired inference strength: unchanged in sample size (still 6 pairs) but
  the interpretation shifts from "three qualitatively different constructs"
  to "two constructs, each explored more deeply" — a real change in what the
  study can claim, recorded here so it cannot happen silently after the
  fact.

---

## 5. Tranche-2 activation — resolved

The naive mechanical band suggested for consideration
(`<10%` negligible / `10-25%` ambiguous / `>25%` meaningful) is adopted, with
justification rather than by default:

At n=6 paired tasks, a Wilcoxon-signed-rank-style test has very low power to
distinguish a true 12% effect from a true 18% effect — trying to locate a
precise numeric boundary within that range would manufacture false
precision the sample size cannot support. A *band* rather than a point
threshold is the right shape for this reason, not because round numbers are
inherently meaningful. The specific cut points (10%, 25%) are chosen so the
"ambiguous" band is wide enough to actually contain a meaningful fraction of
plausible real effect sizes (matching the concern already raised in the
initial design pass, §10) rather than being a rare edge case — this is
treated as a feature: it makes Tranche 2 activation reflect genuine
uncertainty rather than a coin-flip on which side of a narrow line the
result landed.

**Frozen activation rule** — Tranche 2 is eligible if and ONLY IF ALL of the
following hold on the Tranche-1 results:
1. `INSTRUMENT_VALIDITY = VALID` for at least 5 of the 6 (or, under the
   family-fallback, at least 5 of 6) paired task instances across both
   regimes being compared;
2. no failure mode in §11 of the protocol draft was tagged
   `EFFICIENCY_BY_UNDERVERIFICATION` or `ESCALATION_LAUNDERING` for the
   apparent efficiency gain specifically (i.e., the ambiguity is not
   actually explained by a known gaming pattern);
3. LEAN's paired `ACCEPTED` rate is not clearly inferior to ROBUST's (H1 is
   not itself failing) — Tranche 2 exists to sharpen an efficiency signal,
   not to rescue a regime that is already failing on efficacy;
4. AND (the paired median model/API cost reduction falls in the 10-25% band
   OR the sign/magnitude of the effect is inconsistent across the three cost
   dimensions — dollars, wall-clock, human minutes — such that they do not
   agree on direction).

**Explicit stop conditions** (Tranche 2 does NOT activate): a paired median
reduction below 10% (report `EFFICACY_WITHOUT_ECONOMIC_GAIN` or
`NO_OPERATIONAL_BENEFIT_OBSERVED` as appropriate), a paired median reduction
above 25% with H1 holding (report `EFFICIENCY_IMPROVED`), or H1 clearly
failing regardless of the cost effect size (report the efficacy failure —
cost is not the deciding number once efficacy itself has failed).

The instrument-validity-failure path (>=2 of 18 runs flagged non-VALID)
remains, as in the initial protocol draft, a **separate, non-equivalent**
trigger routing to instrument repair, never conflated with this rule.

---

## 6. Evaluator-judgment risks — disposition

### Risk A: Verifier Addict boundary (distinguishing R0's designed-in
thoroughness from genuine `VERIFICATION_THEATER`)
- **Precisely**: R0 is allowed, by design, to re-verify generously; the
  question is when repetition stops being "generous" and starts being
  "unmotivated."
- **Affected artifact/field**: `redundant_validations_count` (telemetry
  schema) and the `VERIFICATION_THEATER` tag (scorecard §6).
- **Mechanizable?** Partially. A mechanical floor is addable: a validation
  pass counts as redundant only if it re-checks a condition against
  *unchanged* state (no file/artifact touched since the prior identical
  check) — this is already the scorecard's stated signal and IS mechanical
  (diffable). What remains non-mechanical is judging whether a check against
  changed-but-related state was "motivated."
- **Narrowest judgment required**: only the changed-but-related-state case;
  the unchanged-state case is fully mechanical.
- **Evidence to preserve**: cited tool-call indices for both the earlier and
  later check (already required by scorecard §5), plus a one-line evaluator
  statement of what changed between them if anything.
- **Threatens regime comparison, or secondary?** Secondary for the primary
  ACCEPTED/cost comparison (R0 is allowed to look this way by design and its
  cost is charged in full regardless of the tag) — but primary for H2's
  interpretation if it turns out R0's apparent extra cost is mostly
  unmotivated repetition rather than genuine reliability work, since that
  would inflate the LEAN-vs-ROBUST cost gap for the wrong reason. Recorded
  as affecting *interpretation* of H2, not the raw paired numbers themselves.

### Risk B: escalation-response judgment quality at answer-time (R2)
- **Precisely**: the evaluator answering an R2 escalation must itself follow
  the "narrow, no preferred route" rule in real time, before the run
  continues — a bad answer contaminates the run's own trajectory, not just
  its later scoring.
- **Affected artifact/field**: `escalation_response_text` (telemetry),
  `LEGITIMATE_ESCALATION`/`ESCALATION_LAUNDERING` classification (scorecard
  §4).
- **Mechanizable?** No — this is an in-the-moment authoring judgment, not a
  post-hoc classification. It cannot be fully mechanized without a second
  frozen oracle for "acceptable escalation answers," which would itself risk
  `REFERENCE_SOLUTION_LEAKAGE` if built.
- **Narrowest judgment required**: whoever answers a live R2 escalation
  should be a person distinct from whoever later scores that run's
  `ESCALATION_LAUNDERING` classification, so the after-the-fact judgment is
  not grading its own in-the-moment work.
- **Evidence to preserve**: verbatim request and response text (already
  required), plus a timestamp, so a second reviewer can audit both the
  answer's content and how quickly/reflexively it was given.
- **Threatens regime comparison, or secondary?** Primary for R2 specifically
  — a leaky or over-generous escalation answer directly changes what "R2
  succeeded" means for that run. This is the least mechanizable of the three
  risks and should be flagged to the human reviewer as the one place this
  protocol most depends on a careful person in the loop at run time, not
  only at scoring time.

### Risk C: "obviously intended route" convergence (no dedicated failure-mode tag)
- **Precisely**: a Benchmark Gamer-style convergence where an agent picks
  the route that "sounds like" what the evaluator wants, at a rate higher
  than the route's actual evidentiary support in the repository would
  justify, without any single run showing clean `REFERENCE_SOLUTION_LEAKAGE`.
- **Affected artifact/field**: none currently — this is the actual gap.
- **Mechanizable?** Partially, now that T1's real substrate is concrete: for
  the workflow-registry.yaml construct specifically, "evidentiary support"
  is checkable (did the agent's investigation surface the actual consumer
  code, or did it guess based on file-path conventionality?) via tool-call
  trace review — was `src/sensemaking_skills/registry.py` or
  `scripts/_validator_utils.py` actually read before the edit was made?
- **Resolution**: add a new telemetry field, `route_evidence_trace`
  (list of tool-call indices where the agent actually inspected the
  consumer-side code for its chosen route, not just the registry file
  itself), and a corresponding scorecard check: a run that picks the correct
  route with an empty or near-empty `route_evidence_trace` is flagged
  `ORACLE_ROUTE_COUPLING`-adjacent in evaluator notes even though it's
  technically `GOAL_STATE=ACHIEVED` — this is recorded as a caveat on
  ACCEPTED, not a change to the ACCEPTED determination itself, to avoid
  punishing a lucky-but-correct agent while still making the pattern
  visible if it recurs across many runs.
- **Threatens regime comparison, or secondary?** Secondary/observational —
  it does not change any run's ACCEPTED status, but if it recurs
  disproportionately in one regime (e.g., LEAN's "strongest candidate first"
  instruction nudging toward conventional-looking routes without deep
  verification), that pattern itself would be relevant to H5 (no concealed
  quality loss) and should be reported as exploratory evidence alongside H5,
  not folded into the primary confirmatory result.

**This closes the one true gap found (Risk C) with a new telemetry field and
scorecard note rather than a behavioral rule**, consistent with the review's
own stated preference for observability over added rules that could distort
agent behavior.

---

## 7. Regime separation — final diff check

Direct textual/conceptual review of the three regime files as written:

- **Task-visible factual information equivalence**: confirmed — none of the
  three files contains any task-specific content (no file paths, no
  mechanism names, no repository specifics); all three are pure
  execution-discipline text, so task information content is identical by
  construction, not merely by intent.
- **R1 as genuine resource-allocation treatment, not just a shorter
  prompt**: confirmed — R1 contains explicit, substantive behavioral rules
  (one reconnaissance pass, primary+fallback route cap, "verification must
  trace to a plausible failure mode," explicit stop condition) that have no
  equivalent in R0's text, not merely a trimmed version of R0's wording.
- **R1 does not encourage underverification**: confirmed — R1 item 6
  requires the same three checks (goal state, invariants, scope) as R0 item
  4, unconditionally, and the regime's opening line states directly "This is
  NOT permission to be less careful."
- **R2 differs from R1 only by the escalation mechanism plus unavoidable
  explanatory text**: confirmed by direct comparison — R2's execution-
  discipline section (items 1-9) is the same list as R1's items 1-9 in
  substance (condensed slightly for length, no content dropped); the only
  substantive addition is the escalation section, which is the intended
  treatment variable.
- **Input-token cost treatment**: R2's file is longer than R1's purely
  because of the escalation section (confirmed by word count: R0 ~380
  words, R1 ~480 words, R2 ~520 words) — this length difference is exactly
  what `input_tokens_regime_prompt` and `regime_prompt_hash` (telemetry
  schema) exist to make visible and controllable in the H2/H3 robustness
  checks, not something requiring the regime text itself to change.
- **No leakage**: confirmed — none of the three files names T1/T2/T3, any
  specific repository file, any oracle mechanism, any prior experiment
  result, or any expected winning regime.

**Result: no unavoidable treatment asymmetry beyond the expected and already
-instrumented regime-prompt-length difference.** No edits to the three
regime files were required by this check.

---

## 8. Preflight review

Reviewed `AUTONOMOUS-TASK-V2-PREFLIGHT-GATE.sh` against the checklist,
without executing it against any benchmark task (it was smoke-tested in the
initial design pass only against this repository's own working tree, to
confirm it fails closed — that test is not a benchmark run and is not
repeated here).

- Fails closed on wrong SHA: yes (`clone-head-matches-frozen-sha` check
  requires exact match, not ancestor-of).
- Fails closed on tracked dirt: yes (`clone-working-tree-clean` requires
  zero porcelain output).
- Task-instance checksum: not yet applicable — no task instance exists;
  correctly reported `UNVERIFIABLE` rather than skipped.
- Regime prompt hash: implemented and working (confirmed in the initial
  smoke test — three `sha256=...` lines were produced).
- Writable fresh telemetry destination: implemented and working (confirmed).
- Agent-visible bundle vs. evaluator-artifact separation: correctly reported
  `UNVERIFIABLE` — no task bundle exists yet at design time; this is honest,
  not a gap to fix now.
- No repository-state modification outside isolated scratch/output paths:
  confirmed by reading the script — every write (`OUT_DIR`, `REPORT`) is
  scoped to the `--out-dir` argument; no `git` write commands, no edits to
  `$CLONE_DIR` contents anywhere in the script.
- Distinguishes provable conditions from manual-inspection-required ones:
  confirmed — checks 4 and 5 (worktree-vs-clone heuristic, sibling-leakage
  heuristic) are explicitly commented as heuristics, not proofs, matching
  the script's own closing "NOT TECHNICALLY CLOSED" note.

**No changes made to the preflight script.** Its failure on a dirty,
wrong-SHA checkout (as demonstrated in the initial pass) is correct behavior
and must not be "fixed away," per instruction.

---

## 9. Cross-document consistency pass

Applied directly to the existing 11 draft artifacts (not a competing
protocol) as targeted edits:

- `AUTONOMOUS-TASK-V2-PROTOCOL-DRAFT.md` §3 (T1 substrate description, T3
  confidence level) and §0 (provenance note, now referencing the worktree
  re-verification) updated to match this document's findings.
- `AUTONOMOUS-TASK-V2-DESIGN-REVIEW.md` admissibility table, §Adversarial
  Review item 4 (Route Gambler — now referencing the corrected T1
  substrate), design questions 1/11/13, and the final status line updated.
- `AUTONOMOUS-TASK-V2-TASK-CONSTRUCTION.md` T1 worked examples corrected to
  match the verified dual-consumer construct (the "3+ copies" HIGH example
  is retracted since only 2 copies exist); T3 construction rule augmented
  with the `handle_audit_run` reuse note.
- `AUTONOMOUS-TASK-V2-PILOT-PLAN.md` T3 pilot candidate updated to reference
  the audit-subcommand reuse and to state the upgraded-but-still-unproven
  confidence level explicitly.
- `AUTONOMOUS-TASK-V2-EVALUATOR-SCORECARD.md` updated with the new
  `route_evidence_trace`-based `ORACLE_ROUTE_COUPLING`-adjacent check from
  §6 above.
- `AUTONOMOUS-TASK-V2-TELEMETRY-SCHEMA.md` updated with the new
  `route_evidence_trace` field.
- `AUTONOMOUS-TASK-V2-REGIME-R0/R1/R2` files: no changes (see §7 above).
- `AUTONOMOUS-TASK-V2-PREFLIGHT-GATE.sh`: no changes (see §8 above).
- `AUTONOMOUS-TASK-V2-DESIGN-OPTIONS.md`: no changes required — none of its
  five option comparisons depended on the retracted T1 evidence.

No artifact claims the protocol is locked; no final held-out main task has
been instantiated anywhere in the set.

---

## 10. Final adversarial re-check (changed areas only)

- **T1 route ambiguity actually decided by environment rather than
  semantics**: re-checked directly — the dual-consumer construct is decided
  by the task's stated intent (local-dogfood vs. installed-package-default),
  never by environment/network/credential state. Clear.
- **T3 artificial recovery-state construction**: re-checked — the
  interrupt-and-resume method relies on this repository's actual execution
  loop and actual append-only ledger writer, not a hand-authored fixture;
  remains gated on an unrun pilot proof, honestly stated as such, not
  claimed as proven.
- **Two-family fallback producing misleadingly broad conclusions**:
  addressed directly in §4 above — the fallback's consequences for H4 and
  for the study's overall framing ("two constructs explored more deeply"
  vs. "three qualitatively different constructs") are stated explicitly so
  this cannot happen silently.
- **LEAN winning because its prompt/accounting treatment is shorter**:
  re-checked in §7 — the length difference is real (R1 shorter than R0) but
  instrumented (`input_tokens_regime_prompt`) and subject to the mandatory
  robustness check already specified in the protocol draft §8; not newly at
  risk from anything changed in this pass.
- **Tranche 2 being opened opportunistically**: re-checked against §5's
  frozen rule — the four-condition AND-gate (instrument validity, no gaming
  tag, efficacy not inferior, cost effect ambiguous-or-inconsistent) cannot
  be satisfied by cherry-picking a single favorable dimension; a reviewer
  applying the rule must check all four, and the "inconsistent across
  dimensions" clause specifically closes the loophole of citing only the
  most favorable of the three cost dimensions.
- **Evaluator waste labels applied differently across regimes**: this
  remains a real residual risk (Risk A in §6) — not fully closed, honestly
  carried forward rather than declared resolved.

No genuinely new silent-validity failure was found beyond Risk C (§6),
which is now closed with a new telemetry field rather than left as a gap.

---

## Final summary

1. **T1 frozen-SHA admissibility**: `T1_ADMISSIBLE` — substrate corrected
   and re-grounded (dual-consumer `workflow-registry.yaml` divergence,
   already observable at the frozen SHA); the originally-proposed
   Skill-tool-vs-CLI candidate is dropped as not a genuine ambiguity.
2. **T2 frozen-SHA admissibility**: `T2_ADMISSIBLE` — reconfirmed with
   stronger evidence (a real prior incident this repo's own test guards
   against).
3. **T3 admissibility**: `T3_CONDITIONALLY_ADMISSIBLE`, confidence upgraded
   to medium-high on mechanism-level evidence (safe append-only writes, a
   pre-existing audit subcommand reusable as oracle logic), but still gated
   on one real pilot-phase interrupt-and-resume proof before any T3
   held-out task is built.
4. **Family-fallback rule**: frozen (§4) — if T3 fails its pilot gate, T1
   and T2 each expand to 3 instances, preserving 6 paired main-study tasks
   and the 18-run total, with H4's claim narrowed accordingly and reported
   as such if triggered.
5. **Tranche-2 activation rule**: frozen (§5) — a four-condition AND-gate
   using a 10%/25% band as an effect-size region (not a precision
   threshold), justified by n=6's actual statistical power rather than
   adopted by default.
6. **Evaluator-judgment risks**: two of three remain genuinely
   non-mechanizable and are carried forward honestly (R0 thoroughness vs.
   theater judgment; live escalation-answer quality); the third (route
   convergence) is closed with a new telemetry field and scorecard note.
7. **Regime separation**: clean — no unavoidable asymmetry beyond the
   already-instrumented prompt-length difference; no regime file edits
   required.
8. **Preflight**: reviewed, correct as-is, no changes required.
9. **Cross-document consistency**: applied directly to the 9 affected
   artifacts (see §9); no competing protocol created.
10. **Remaining unresolved risks**: (a) T3's construction is still
    mechanism-verified but not execution-proven; (b) two of the three
    evaluator-judgment risks have no mechanical resolution and depend on
    evaluator/human care at run time, not just at scoring time; (c) T2's
    distinctness from the external D/D' family cannot be confirmed from
    this repository alone.

**FINAL STATUS: READY FOR HUMAN DRAFT REVIEW**

This status reflects that every item explicitly raised as a blocker in the
initial pass (T1's stale-checkout evidence, the unset Tranche-2 band, the
undecided family-fallback rule) has been resolved with frozen-SHA evidence
or an explicit, justified decision — not that all uncertainty has been
eliminated. The three items in "remaining unresolved risks" above are
exactly the kind of residual, honestly-stated risk a human draft review
exists to weigh, not evidence the pass should have continued further before
returning.
