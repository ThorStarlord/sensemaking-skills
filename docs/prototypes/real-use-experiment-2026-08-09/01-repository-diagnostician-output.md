*(Raw output from a fresh-context subagent invocation of `repository-diagnostician`, preserved verbatim below the separator. Subagent given: the owner's question verbatim, the recovered known_intent from `00-pre-registration.md`, and read/investigation tool access to the real repository. Not given: any of the interaction layer's or this conversation's synthesis, opinions, or expected-answer framing. Investigation duration: ~708s, 57 tool calls, per the Agent tool's own reported usage.)*

*(Correction, written during this same experiment: the first version of this file was a paraphrase with a pointer back to "the parent conversation's tool-result" instead of the actual verbatim text — a real gap this experiment surfaced on its own, before the downstream-consumer step even ran. See `03-downstream-consumer-attempt-1-FAILED.md` for what that gap caused. This file now contains the actual, complete, verbatim brief.)*

---

# Repository Sensemaking Brief (vNext prototype)

**Produced by:** `repository-diagnostician` (PROTOTYPE, `prototype/repo-sensemaker-vnext`), invoked non-interactively, read-only.
**Repository:** `H:\GithubRepositories\sensemaking-skills`, branch `prototype/repo-sensemaker-vnext`, HEAD `abab6c4` (`main` at `e790f30`, PR #163 open/mergeable, PR #164 open/draft — all confirmed during this investigation).
**Owner's question (verbatim):** "Given the current state of Sensemaking Skills, what should I focus on next to create the most product value, and what should I deliberately stop investing in?"

---

## 1. Repository goal

Per `CONTEXT.md:1-13`, this repository is a meta-routing layer for AI agents: it turns project/repository uncertainty ("fog") into problem frames, research paths, and skill recommendations, via a pipeline of Markdown-defined skills (`problem-framer` → `unknowns-mapper` → `repo-sensemaker` → `workflow-planner` → `handoff`) that communicate through durable artifacts rather than conversation memory ("Artifacts as API," `CONTEXT.md:12`). Its own stated production-readiness target (`docs/adr/0021-production-readiness-requirements.md:15-18`) is narrower than the whole system: "externally validated repository-sensemaking briefs" — i.e., the `repo-sensemaker` skill's Stage A output surviving contact with a real, independently-authored external repository.

## 2. Current shape

- `skills/` (4,049 tracked lines across `.md`/`.py`) holds the actual product surface: the five-skill core pipeline plus ecosystem skills (product/PM, UI, docs-aligner) and, on this branch only, the experimental `repository-diagnostician` / `vnext-review-consumer` prototypes.
- `scripts/` holds the validator stack (Level 1-5, `CONTEXT.md:339-355`) plus, as of the last ~3 months, a large execution-governance subsystem: Gate A authorization (`scripts/gate_a_authorization.py`), the exploratory-authorization capability lifecycle, campaign accounting/ledger, and `scripts/execution_infra/` (verifier, provider adapter, governed runner).
- `experiments/` holds two distinct research lines that both matter to this question: (a) the P1-P4 / S1-S2 product/solution-interaction experiments (`experiments/product-interaction-p*-v1/`, `experiments/solution-interaction-s*-v1/`), and (b) the `experiments/campaigns/EXP-0001-*` / `EXP-0002-*` external-validation preparation packages.
- `.github/workflows/validation.yml` (685 lines) runs nine distinct CI jobs: Gate A (Linux/Windows), Phase 2 campaign validation + wheel smoke, Phase 3 exploratory authorization, Phase 4 campaign ledger + Windows path confinement, Phase 5 EXP-0001 preparation, Phase 6 execution boundary, plus the original Level 1-5 "Repository validation" job.
- `docs/adr/` has 21 accepted/proposed ADRs; the newest (0021, 0022, 0023) all govern the execution-governance track specifically.

## 3. Strong signals

- The core validator stack is real and exercised: `scripts/validate-repo.py` passes cleanly on this branch right now (ran during this investigation), and `scripts/test-validators.py` reports 69/69 passing per PR #163's own test plan.
- The interaction-design research line (P1-P4, S1-S2) is genuine, cumulative product research, not busywork: P1 found and correctly deprioritized a hypothesis pending reproduction (`experiments/product-interaction-p1-v1/disposition-v1.md:10-20`), the reproduction (P1-R) confirmed a real distribution defect ("shipped 0.2.1 lacks setup-skills command and all SKILL.md trees" — PR #155 title), and the defect was actually fixed and shipped (PR #156, "wheel ships canonical skill trees... (0.2.2)").
- P4 (external, documentation-light target `renpy_mcp_server`) produced a STRONG_SHARPENING, direction-establishing result the owner explicitly accepted (`experiments/product-interaction-p4-v1/learning-v1.md:8-16, 177-194`).
- S2, even though MIXED, is a well-diagnosed failure with a specific, actionable refinement already written down and owner-reviewed (`experiments/solution-interaction-s2-v1/learning-v1.md:119-152`) — this is exactly the kind of falsifiable, non-hand-wavy research output the repo's own evidence discipline calls for.
- ADR 0021 is unusually self-correcting: its own text flags and reverses an earlier draft's overbroad "already true today" claim about external-repo coverage (`docs/adr/0021-production-readiness-requirements.md:75-84, 96-100`) — a real instance of the repo practicing the honesty discipline `CLAUDE.md` asks for.

## 4. Missing pieces

- No successfully completed external-validation campaign exists anywhere in this repository's history. Every historical attempt at the Stage 1 auteur run failed structurally (see Section 7/9).
- `CONTEXT.md`'s "Known Gaps" section (last touched 2026-05-25, commit `1f7fd67`, `git log -- CONTEXT.md`) still asserts "**No value-production runs exist yet**" (`CONTEXT.md:322`) — a claim now roughly 2.5 months and dozens of experiment/infrastructure commits stale, unrevisited since P1/P4/S2 ran against real (including external) targets.
- README/pyproject version drift is live right now: `README.md:9` and `README.md:77` both say `v0.2.1`; `pyproject.toml:7` says `0.2.2` — confirmed both by direct read and by running this branch's own `scripts/prototype_version_drift_scan.py --repo-root .` (output: `README.md:77: 0.2.1 <-- DRIFT`). This is the same finding S1 recorded as "minor and non-decision-changing" and it has sat unfixed since.
- `README.md:8` claims "Maturity: Production-ready for agent-based use" one line above "Status: Beta" — an internally inconsistent claim not chased further here (see Section 15's discipline note on why).

## 5. Improvement opportunities

- `ISSUE-LIST-SENSEMAKING-INFRASTRUCTURE-FIX.md` (dated 2026-05-29) references `workflow-orchestrator` by its pre-rename name and targets an `artifact-contracts.yaml` location CONTEXT.md's own routing table (`CONTEXT.md:150-156`) has since superseded; it is itself a stale planning artifact, though its one live consequence (INFRA-004) is already correctly xfail-marked (`tests/test_artifact_contracts_pm_engineering.py`: 3 passed, 5 xfailed, run during this investigation), i.e., acknowledged and non-blocking, not silently broken.
- The two-value routing-field alias table in `CONTEXT.md:158-165` is current for `validate-brief.py` (PR #163 fixes exactly this file) but `scripts/workflow-runtime.py`'s own `fog_type_patterns` dict (`scripts/workflow-runtime.py:1269-1274`) still hard-codes only 4 fog types and has no `integration_fog` entry — a second, separate instance of the same registry-drift class PR #163 fixes elsewhere, left for a follow-up.

## 6. Weakest boundary

**The repository's own execution-governance track (Gate A / Two-Lane authorization / Phase 2-6 campaign infrastructure) has substantially overshot the problem it exists to solve, and this is independently, currently demonstrated — not merely a suspicion.**

**Weakness type:** Other

This does not fit any of the seven registered types (`skills/repo-sensemaker/references/weakness-types.md`): nothing claims a false format, no autonomous workflow lacks an approval gate (if anything, the opposite — see Section 9), no documented feature is unimplemented, and no core logic lacks a check. What's demonstrated instead is a **resource-allocation/overinvestment pattern**: a governance apparatus built to safely re-run one failed external-validation experiment now measures ~97 files / ~29,401 lines (`tests/campaign_validation/`, `tests/campaign_accounting/`, `tests/execution_infra_tests/`, `tests/campaign_preparation/`, `tests/test_gate_a_*.py`, `tests/test_exploratory_*.py`, `src/sensemaking_skills/{campaign_validation,campaign_accounting,exploratory_authorization}/`, `scripts/execution_infra/`, `scripts/gate_a_authorization.py` — counted via `git ls-files ... | xargs wc -l` during this investigation) — roughly 40% of the repository's total tracked Python/Markdown/YAML (73,305 lines), against 4,049 lines in `skills/`, the part of the repo that actually produces user-facing value. In exchange, it has produced **zero** completed post-infrastructure campaign executions, required a full rework cycle mid-build (PR #129, "REQUEST_CHANGES" — closed, not merged, superseded by "Phase 6 correction," `f92e977`), and — as of this investigation — is the reason `main`'s CI has failed on every one of its last 6 pushes.

## 6.5. Problem classification (fog type)

**primary_fog_type: product_fog.** The owner's question is fundamentally "what creates product value, what doesn't" — a resourcing/prioritization question, not a code-structure one, even though its evidence is architectural. See `domain` in Section 15 for the fuller, multi-valued picture this single field can't carry.

## 7. Evidence

<!-- mode: investigative -->

`.github/workflows/validation.yml:592-648` defines the "Phase 6 execution boundary" CI job. Running `gh run list --branch main --workflow="Validator Ecosystem" --limit 15` during this investigation shows this job failing on **every push to `main` since 2026-08-09T02:39Z through 2026-08-09T05:01Z** (6 consecutive runs, spanning the P2/P3/P4/S1 experiment merges and PR #161/#162), immediately preceded by 10 consecutive green runs back through 2026-08-06. The failure (`gh run view 31295784963 --log`, captured in full) is `tests/execution_infra_tests/test_runner.py::test_real_campaign_refuses_unpinned_framework_checkout` — `AssertionError: assert 'not the pinned' in 'validity window has not opened: now=2026-08-08T00:00:00+00:00 < not_before=2026-08-08T05:01:21+00:00'`. Reading the test directly (`tests/execution_infra_tests/test_runner.py:172-188`) shows why: it copies the **real, committed** `experiments/campaigns/EXP-0002-*` package and asserts on a specific fail-closed error string, using a fixed simulated clock (`datetime.fromisoformat("2026-08-08T00:00:00+00:00")`) written against that real package's `not_before` value at authoring time. The real package has since been repinned (git history shows a chain of `chore(EXP-0002): repin to ...` commits — `d829a06`, `2d67a0b`, `248b14f`, `cc2b31e`, `72f3b81`, `7a6a2c6`), shifting `not_before` and silently flipping which fail-closed check now fires first. This is a genuine, currently-live defect: an implicit, unpinned dependency of a test on a real, frequently-mutated data file elsewhere in the repo (`experiments/campaigns/EXP-0002-*/campaign-policy.yaml`), undetected across 6 merges.

Separately, `experiments/campaigns/EXP-0001-stage1-auteur-autonomy-pilot/README.md:3` states "STATUS: PREPARATION ONLY. NOT OPERATIVE. NOT APPROVED. NOT EXECUTED," and `README.md:49-53` pins the frozen approval window to `not_before: 2026-08-18T00:00:00+00:00` — meaning even if the owner approved it today, this campaign structurally cannot begin for 9 more days, and the approval itself requires a manual GitHub issue-comment step (`README.md:129-146`) that hasn't happened.

The predecessor Stage 1 run (before this apparatus existed) did execute once and failed: GitHub issue #83's closing comment (`gh issue view 83 --json comments`) reads "Stage 1 authorized run: complete (FAIL)... Failure class: structural quote-fidelity failure... No second Stage 1 run is authorized until both are resolved/merged, a new framework SHA is pinned, an updated execution package exists, and a new explicit owner authorization is granted." The two blocking defects it named (issues #89, #90) are now closed, but no rerun has occurred since — the multi-phase governance apparatus was built instead.

`docs/adr/0021-production-readiness-requirements.md:38-52` confirms the owner ratified the external-validation target (D7/D8) and a *staged* plan (E4) — but explicitly authorized "Stage 1 **planning** only," with execution requiring "a separate, explicit owner instruction issued after the owner reviews the final pinned revisions" — that instruction is not recorded anywhere in this repository as of this investigation.

Logic trace: the CI-red result (observed directly, this investigation) is a symptom of the same track whose file/LOC footprint (derived, this investigation) and zero-completed-campaign history (observed via issue #83, the EXP-0001 package contents, and the campaign-policy validity window) together show sustained, still-growing investment with no realized output — while `CONTEXT.md:259-262`'s own "Harden Only Where Pressured" principle ("System-level hardening... is only permitted when... a real run fails with a specific error [or] the same failure class recurs") was the correct trigger for fixing issues #89/#90 narrowly, not for building a five-phase authorization/ledger/capability-lifecycle framework in response to it — connecting the observed evidence to the weakest-boundary conclusion above.

## 8. Evidence excerpts

```yaml
evidence_excerpts:
  - file: tests/execution_infra_tests/test_runner.py
    lines: L172-188
    quote: "see file/lines"
    supports_claim: "Test asserts on a fail-closed error string that depends on the real, frequently-repinned EXP-0002 campaign package's not_before value, using a fixed historical clock literal that has desynced from it -- the direct cause of main's current CI red state."
  - file: experiments/campaigns/EXP-0001-stage1-auteur-autonomy-pilot/README.md
    lines: L3
    quote: "see file/lines"
    supports_claim: "The prepared external-validation campaign is explicitly not operative, not approved, and not executed."
  - file: experiments/campaigns/EXP-0001-stage1-auteur-autonomy-pilot/README.md
    lines: L49-53
    quote: "see file/lines"
    supports_claim: "The campaign's approval window cannot open before 2026-08-18, so no amount of further engineering makes it executable sooner."
  - file: docs/adr/0021-production-readiness-requirements.md
    lines: L38-52
    quote: "see file/lines"
    supports_claim: "Only Stage 1 planning was ratified; Stage 1 execution requires a separate, explicit owner instruction not yet given."
  - file: README.md
    lines: L9
    quote: "see file/lines"
    supports_claim: "README states the shipped version as v0.2.1."
  - file: pyproject.toml
    lines: L7
    quote: "see file/lines"
    supports_claim: "Canonical package version is declared 0.2.2, contradicting README.md:9/:77."
  - file: CONTEXT.md
    lines: L322
    quote: "see file/lines"
    supports_claim: "CONTEXT.md's Known Gaps section still claims no value-production runs exist, unrevised since 2026-05-25 despite P1/P4/S2 running against real repositories since."
  - file: CONTEXT.md
    lines: L259-262
    quote: "see file/lines"
    supports_claim: "The repo's own governing principle (Harden Only Where Pressured) is the yardstick against which the execution-governance track's scope is measured as an overshoot."
  - file: experiments/solution-interaction-s2-v1/learning-v1.md
    lines: L144-152
    quote: "see file/lines"
    supports_claim: "The interaction-research line's own next step is already scoped and owner-gated: test the state-currency refinement before further construction."
```

## 9. Why this boundary matters

If this pattern continues unexamined, the repository will keep converting engineering hours into audit/authorization machinery for a validation event that (a) cannot occur for at least 9 more days regardless of further code, and (b) has never yet succeeded even once under any framework version — while two comparatively cheap, already-scoped, owner-endorsed product-value tracks (the S-series interaction research, and this very vNext prototype's own recommended next evidence) sit untouched. The concrete, current cost is visible today: `main`'s CI has been red for 6 consecutive pushes in exactly this track, and — because the failing job (Phase 6) is one of nine parallel jobs in a single workflow, several of which are cosmetically unrelated ("Node.js 20 is deprecated" noise, unrelated `git` exit-128 warnings on unrelated jobs) — a real, diagnosable defect is currently sitting inside a wall of green checkmarks that a maintainer would need to read carefully to even notice. This is precisely the failure mode the repo's own "Repeatable Failure Boundary" and "Harden Only Where Pressured" principles (`CONTEXT.md:259-264`) were written to prevent, applied here to the very system that implements them.

## 10. Candidate next steps

1. **Declare a moratorium on new execution-governance scope** (no new Gate A checks, campaign-ledger features, or authorization lanes) until either EXP-0001 actually executes once, or a real, specific, recurring failure (per `CONTEXT.md:259-262`'s own test) demands otherwise. This is a policy decision, not code — zero implementation cost.
2. **Fix the CI-red root cause** (`tests/execution_infra_tests/test_runner.py:172-188`): either pin a synthetic fixture package for this test instead of copying the real, mutable EXP-0002 package, or update the fixed clock literal to track the real package's current `not_before` value. Small, bounded, immediately restores a trustworthy signal.
3. **Resume the interaction-design research line at S3**, testing S2's already-named refinement ("verify documented state is current before sequencing a recommendation") in another authentic use — the cheapest, most-scoped, most owner-endorsed live product-value track in the repository right now.
4. **When (and only when) the EXP-0001 window opens on 2026-08-18**, if external validation is still the priority, post the single required GitHub approval comment (`experiments/campaigns/EXP-0001-stage1-auteur-autonomy-pilot/README.md:129-146`) — no further engineering is needed to reach this point.
5. **Resolve this vNext prototype's own fate** using this investigation as the evidence its assumption ledger says it needs (`docs/prototypes/repo-sensemaker-vnext.md:315-322`: "Keep... Discard or heavily revise before treated as more than one candidate") — which this real-use experiment is already in progress on.

## 11. Recommended next step

**Fix `tests/execution_infra_tests/test_runner.py`'s coupling to the real EXP-0002 package (candidate #2) and adopt the moratorium (candidate #1) in the same pass.** This is the smallest concrete action with the highest leverage: it is cheap (one test file), reversible, requires no owner strategic decision, restores a truthful CI signal repository-wide, and directly enacts — rather than merely recommends — the "stop investing" half of the owner's question for the one track where repository evidence, not owner preference, already settles the answer. It does not require choosing among candidates #3/#4/#5, which genuinely do need owner input (see Section 15).

## 12. Recommended workflow

**`product-strategy-sprint`** (`skills/workflow-planner/references/workflow-registry.yaml:290-332`) — the closest registered fit for turning a resourcing hypothesis ("stop expanding execution-governance infrastructure; prioritize among the interaction-research, external-validation, and vNext-prototype tracks") into `lean-canvas` → `north-star` → `okr` → `roadmap` → `stakeholder-update`. This is a genuine stretch, flagged honestly: no workflow in the registry is built for "confirm an overinvestment finding and pick among three already-scoped alternatives" specifically, and `product-strategy-sprint` expects a validated hypothesis as input rather than producing one — this brief supplies that hypothesis, pre-validated by the evidence above.

## 13. Machine-readable handoff

```yaml
artifact_id: repository_sensemaking_brief
schema_version: 1
source_intent_ref: docs/prototypes/real-use-experiment-2026-08-09/00-pre-registration.md
user_implied_fog_type: product_fog
primary_fog_type: product_fog
diagnosis_conflict: false
escalation_recommended: false
evidence:
  - "tests/execution_infra_tests/test_runner.py (lines L172-188): test couples to the real, frequently-repinned EXP-0002 campaign package via a stale fixed clock, the direct cause of main's current CI red state"
  - ".github/workflows/validation.yml (lines L592-648): Phase 6 execution boundary job definition, currently failing on main"
  - "experiments/campaigns/EXP-0001-stage1-auteur-autonomy-pilot/README.md (lines L3, L49-53): campaign explicitly not operative; approval window cannot open before 2026-08-18"
  - "docs/adr/0021-production-readiness-requirements.md (lines L38-52): only Stage 1 planning ratified, execution requires a separate unrecorded owner instruction"
  - "README.md (lines L9): states shipped version v0.2.1"
  - "pyproject.toml (lines L7): declares canonical version 0.2.2, contradicting README.md"
  - "CONTEXT.md (lines L322): Known Gaps section claims no value-production runs exist, stale since 2026-05-25"
  - "CONTEXT.md (lines L259-262): repo's own Harden Only Where Pressured principle, the yardstick the execution-governance track is measured against"
  - "experiments/solution-interaction-s2-v1/learning-v1.md (lines L144-152): interaction-research line's own scoped, owner-gated next step"
recommended_workflow_id: product-strategy-sprint
recommended_execution_mode: guided_execution
weakest_boundary: "Execution-governance infrastructure (Gate A / Two-Lane / Phase 2-6) has overshot the problem it exists to solve: ~29,401 lines built to safely re-run one external-validation experiment, which has never once succeeded and cannot execute again before 2026-08-18 regardless of further engineering, while the same track's own tests are currently failing on main, undetected across 6 merges."
weakness_type: Other
weakness_type_explanation: "Demonstrated, evidenced overinvestment/resource-allocation pattern -- not a code-format, documentation, safety-gate, dependency, validation-coverage, or example-staleness defect in the sense the seven registered types describe. The concrete symptom cited (a real, currently-failing test) is closest in kind to Implicit Dependencies, but the finding this brief actually rests on is the broader allocation pattern that symptom is evidence for, which the registered taxonomy (explicitly scoped to defect mechanisms in code/artifacts, per this prototype's own assumption ledger A-04) does not cover."
required_inputs:
  - user_intent
  - repository_state
created_at: "2026-08-09T00:00:00Z"
immutable: true
```

## 14. Ready-to-copy prompt

> Using this Repository Sensemaking Brief (`repository_sensemaking_brief`, created 2026-08-09), run `product-strategy-sprint` with hypothesis_statement: "sensemaking-skills' execution-governance infrastructure (Gate A / Two-Lane authorization / Phase 2-6 campaign machinery) has overshot the single external-validation experiment it exists to enable — ~29,401 lines, zero completed campaigns, one PR-129 rework cycle, and a currently-failing test on `main` (`tests/execution_infra_tests/test_runner.py::test_real_campaign_refuses_unpinned_framework_checkout`) — while three cheaper, already-scoped, owner-touched product-value tracks (S-series interaction research, the eventual EXP-0001 run once its 2026-08-18 window opens, and this vNext prototype's own next-evidence need) remain the live candidates for 'what to focus on next.' Use lean-canvas/north-star/okr/roadmap to help the owner rank these three and formally deprioritize further execution-governance scope growth." Before running it, first apply Section 11's recommended next step directly (fix the CI-coupling defect; adopt the moratorium) — that part needs no further sensemaking, only execution.

---

## 15. Analysis vNext (PROTOTYPE — not read by any canonical validator)

```yaml
analysis_vnext:
  schema_version: prototype-1
  domain:
    - product
    - architecture
  discovery_confidence:
    level: high
    why_bounded: >
      Grounded in direct, multi-source, mostly first-hand observation during this
      investigation: a live CI run and its full log (gh run view/list), direct file
      reads (README.md, pyproject.toml, CONTEXT.md, ADR 0021, EXP-0001 README, the
      failing test's source), a real GitHub issue's closing comment (#83), a real
      closed-not-merged PR (#129), and a directly-run file-count/LOC command plus
      this branch's own prototype_version_drift_scan.py tool -- not inference from
      prose alone. Bounded because: (a) I did not independently re-verify that
      issues #89/#90 were actually fixed correctly (only that they are closed);
      (b) I did not read the full raw investigation files for P1-P3 (only their
      disposition/learning summaries), so I cannot rule out nuance those summaries
      omit; (c) I did not run the full pytest suite locally, only the specific
      xfail-marked file and the live CI log, so I cannot rule out other currently-red
      tests outside the one CI job I traced; (d) LOC/file counts are a proxy for
      investment, not a direct measure of value or difficulty, and are presented as
      such, not as a precise ratio.
  consequential_boundary:
    description: >
      Investment allocation has drifted toward self-referential execution-governance
      infrastructure (Gate A / Two-Lane authorization / Phase 2-6 campaign machinery)
      at the expense of demonstrated product-value work. This same finding drives
      Section 6's weakest_boundary above -- this prototype's P4-derived hypothesis
      (that consequential_boundary and weakest_boundary can diverge) was tested here
      and found NOT to require divergence in this case: the boundary that matters
      most for "what should I focus on next" and the boundary that is most currently
      fragile are the same finding, evidenced from two angles (portfolio allocation,
      and a concrete live defect inside that same portfolio).
    rationale: >
      See Section 7/9 for the full evidentiary chain: ~29,401 lines / 97 files
      (~40% of tracked source) built around a single external-validation experiment
      that has never succeeded, cannot execute again before 2026-08-18 regardless of
      further engineering, required a mid-build rework cycle (PR #129), and whose
      own test suite is the reason main's CI has been red for 6 consecutive pushes,
      undetected. Measured against the repository's own explicit "Harden Only Where
      Pressured" principle (CONTEXT.md:259-262), the response to the two specific
      defects (#89, #90) that triggered this track was disproportionate to the
      triggering evidence.
    is_demonstrated_weakness: true
  uncertainty:
    source: owner_intent
    question: >
      Among (a) resuming the interaction-design research line at S3 (testing S2's
      already-named state-currency refinement), (b) waiting for and then executing
      EXP-0001 once its approval window opens on 2026-08-18 (assuming external
      validation remains the priority readiness target it was ratified as in ADR
      0021), and (c) resolving this vNext prototype's own fate (KEEP/REVISE/COLLAPSE)
      using real-use evidence like this investigation -- which does the owner want
      treated as the PRIMARY next product-value investment, and which as
      secondary/deferred? Repository evidence establishes that all three are live,
      legitimate, owner-touched candidates with concrete unblocked next steps, and
      that none of them requires more diagnosis to become actionable -- but it
      cannot establish which one the owner values most right now, and I attempted to
      resolve this before classifying it here: I checked whether ADR 0021's
      ratification settles it (it ratifies external validation as A target, not as
      THE priority over the others), whether EXP-0001 is actually executable now (it
      is not, for 9+ days minimum), and whether the S-series or vNext tracks have an
      unconditional owner green light already (both are gated -- "test... before
      deliberate product construction" for S3; "run one genuine owner-originated
      decision... through the pipeline" for vNext, which this very investigation is
      now doing). None of those checks resolves the ranking; it remains a genuine
      preference/strategic call.
  owner_intent_state:
    known: >
      Sustained, repeated emphasis on returning to real product use over indefinite
      infrastructure/cleanup work, and explicit statements against chasing every
      newly-discovered drift item into another infrastructure campaign. Explicit
      standing epistemic discipline: implemented != validated != owner-ratified !=
      production-ready. A long-running, multi-experiment interaction-design research
      line (P1-P4, S1-S2) that predates this investigation and reflects sustained,
      deliberate owner interest. Explicitly deferred, recorded-not-acted-on items:
      the workflow-runtime.py fog_type alias, further canonical-vocabulary.yaml
      drift, INFRA-004 (already xfail-marked, confirmed non-blocking this
      investigation), and ADR-0021-gated external validation. Heavy, explicitly
      PROTOTYPE-ONLY investment in the repo-sensemaker/repository-diagnostician
      vNext split (PR #164), whose own ledger says it needs real use, not more
      construction, as its next evidence.
    unresolved: >
      Which of the three live candidate tracks (S-series continuation, eventual
      EXP-0001 execution, vNext prototype disposition) the owner wants prioritized
      as THE next product-value focus, versus treated as secondary/parked. Also
      unresolved, lower-stakes: whether the README/pyproject version drift and the
      CONTEXT.md Known-Gaps staleness are worth a combined one-line fix now or are
      genuinely too minor to interrupt anything for (repository evidence says they
      are cheap and safe to fix; whether they're worth the interruption at all is
      still a small owner call).
    status: thin
  evidence_status_notes:
    - file: tests/execution_infra_tests/test_runner.py
      lines: "172-188"
      status: observed
    - file: .github/workflows/validation.yml
      lines: "592-648"
      status: observed
    - file: docs/adr/0021-production-readiness-requirements.md
      lines: "38-52"
      status: observed
    - file: experiments/campaigns/EXP-0001-stage1-auteur-autonomy-pilot/README.md
      lines: "3, 49-53"
      status: observed
    - file: README.md
      lines: "9, 77"
      status: observed
    - file: pyproject.toml
      lines: "7"
      status: observed
    - file: scripts/prototype_version_drift_scan.py
      lines: "n/a (tool output)"
      status: derived
    - file: "(directory-set LOC count: tests/campaign_validation, tests/campaign_accounting, tests/execution_infra_tests, tests/campaign_preparation, tests/test_gate_a_*.py, tests/test_exploratory_*.py, src/sensemaking_skills/{campaign_validation,campaign_accounting,exploratory_authorization}, scripts/execution_infra, scripts/gate_a_authorization.py)"
      lines: "n/a (git ls-files | xargs wc -l)"
      status: derived
    - file: "GitHub Actions run 31295784963 (Validator Ecosystem, main)"
      lines: "n/a (live CI run, not a repo file)"
      status: observed
    - file: "GitHub issue #83 (closing comment)"
      lines: "n/a (issue tracker, not a repo file)"
      status: observed
    - file: CONTEXT.md
      lines: "259-262, 322"
      status: observed
    - file: "CONTEXT.md staleness claim (no value-production runs)"
      lines: "322"
      status: interpretation
  evidence_note: >
    This brief's central claim rests on descriptive evidence (LOC counts, a live
    failing CI run, a real test's source code, real campaign-package contents) that
    agrees with itself across every source checked -- no code-vs-ADR disagreement
    was found requiring the drift-not-rank treatment. The one place citation-trust
    ordering mattered: CONTEXT.md's "no value-production runs" claim (a canonical
    doc) is treated as descriptive-but-stale rather than normative, since nothing
    ratifies it as a current decision -- it is an unrevised observation, correctly
    superseded by more recent, more specific evidence (the P1/P4/S2 run records)
    per the citation-trust hierarchy's own ordering (code/tests and direct run
    evidence over historical status docs).
```
