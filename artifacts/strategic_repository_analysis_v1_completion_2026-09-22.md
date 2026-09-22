# Strategic Repository Analysis — Version 1.0 Completion

## 1. Governing Intent and Scope

Owner intent in this episode is to identify the highest-value remaining difference
between the current `sensemaking-skills` product and a finished Version 1.0
product, then continue autonomously through repository-answerable work until a
genuine owner, Level-4, external, or no-further-work boundary.

Target repository: `ThorStarlord/sensemaking-skills`.

Target source identity: `main@a3d83c14de033734d33296ff3f45ebc5f4d8d911`.

Governing product authority remains `docs/product-strategy.md`, ADR 0029, and
the reduced-scope Version 1.0 release contract. This analysis does not grant
merge, publication, PyPI, tag, or final release-owner authority.

### Goal fitness

The stated objective, **finished Version 1.0 product**, is a terminal product/release
outcome. The currently named `1.0.0rc3` freeze is an instrumental release
milestone, not the terminal objective.

A concrete counterexample exists: RC3 could be frozen and qualified while the
final Version 1.0 readiness gate remained structurally unable to return `READY`.
Therefore RC3 qualification alone is not a sufficient proxy for the owner's goal.

## 1A. Strategic Continuity

This analysis **SUPERSEDES for the current decision** the legacy
`artifacts/strategic_repository_analysis.md`, which targeted
`main@81e01c971b1196d24fa63fd071a4a1eb91e954e6` and selected a post-#401
STATUS reconciliation that is already complete.

The prior artifact remains immutable provenance. Its selected PATH-1 is not an
unfinished responsibility for the current source state.

## 2. Current System Model

The reduced-scope Version 1.0 product already has a defined stable CLI/API/Skill
surface, Campaign schema v2, package/lab boundary, exact-source release mechanics,
installed-wheel/sdist qualification, strategic analysis surfaces, and explicit
authority boundaries.

Current source remains `1.0.0rc3.dev0` in `development`, targeting
`1.0.0rc3`. Native-harness compatibility, cross-harness portability, and
semantic usefulness remain deliberately excluded/deferred rather than required
Version 1.0 support claims.

The completion layers are therefore:

- implementation surface: established for the reduced-scope contract;
- integration/reachability: established by current package/CLI/Skill machinery;
- intended reduced-scope behavior/contract: established mechanically, with
  stronger usefulness/native claims explicitly deferred;
- release qualification/finalization: partial;
- release-owner publication authority: reserved.

The decisive repository-local defect is in the finalization layer:
`scripts/validate-release-readiness.py` unconditionally emits
`exact release head CI evidence is not recorded`, so the documented authoritative
final gate cannot return `READY` even if every external prerequisite is actually met.
The same gate also expects release-owner authorization inside the repository
workspace while requiring a clean exact head, without defining a provenance-safe
external/ignored evidence boundary.

## 3. Capability and Limitation Map

| Capability | State | Evidence | Strategic relevance |
| --- | --- | --- | --- |
| reduced-scope stable product surface | ESTABLISHED | `release-v1.0.yaml`, `docs/public-surface-v1.0.md` | The current product boundary is already defined; more architecture is not a prerequisite to final 1.0. |
| exact-head distribution qualification | ESTABLISHED | `.github/workflows/release-candidate.yml`, `docs/PUBLISHING.md` | The repository can build and qualify exact source artifacts. |
| final 1.0 readiness gate | PARTIAL | `scripts/validate-release-readiness.py`, `docs/release-v1.0-checklist.md` | The intended authoritative final gate is structurally unsatisfiable and therefore blocks a genuine final transition. |
| native-harness compatibility evidence | DEFERRED | `release-v1.0.yaml`, `docs/release-v1.0-contract.md` | Explicitly outside the required reduced-scope 1.0 promise; should not be silently promoted into a blocker. |
| semantic usefulness evidence | DEFERRED | `release-v1.0.yaml`, `docs/product-strategy.md` | Important future product evidence but not a current reduced-scope 1.0 release prerequisite. |
| GitHub main protection | BLOCKED | Issue #384 | External hosting governance gap; repository code cannot complete it. |
| final publication authorization | BLOCKED | `docs/PUBLISHING.md`, `docs/release-v1.0-checklist.md` | Correctly owner-reserved and must remain separate from technical readiness. |

## 4. Strategic Frontier

### FRONTIER-1 — Satisfiable final-release qualification path

The final Version 1.0 gate is intended to be authoritative but currently cannot
reach `READY` because CI evidence is rejected unconditionally and external
authorization/evidence inputs lack a clean exact-head boundary.

This materially affects the repository future because it prevents transition from
the implemented reduced-scope product into a mechanically finalizable Version 1.0
without weakening source-identity guarantees.

### FRONTIER-2 — Stronger empirical/native support claims

Real native-harness compatibility, portability, and semantic usefulness remain
unestablished. Pursuing them would expand the evidence/support promise beyond the
current reduced-scope contract.

This is strategically real but not a prerequisite under current Level-4/release
authority.

## 5. Candidate Construction Paths

### PATH-1 — Make reduced-scope Version 1.0 finalization mechanically satisfiable

- **Future state:** final release readiness can become `READY` only when exact
  final source identity, exact-head Product Validation, exact-head Release
  Candidate Distribution, artifact hashes, clean Git state, and explicit owner
  authorization are all supplied.
- **Why plausible:** all underlying qualification surfaces already exist; the
  missing boundary is the final evidence consumer/contract, not a new product
  runtime.
- **Frontier grounding:** FRONTIER-1.
- **Builds on:** current release contract, release-candidate workflow, release
  authority audit, exact-source identity discipline.
- **Requires:** provenance-safe sidecar evidence inputs and a positive regression
  proving `READY` is reachable.
- **Construction sequence:** define non-source evidence boundary -> validate exact
  head/run/hash/owner evidence -> prove positive and stale/failing cases -> reconcile
  publication docs.
- **Dependencies:** existing reduced-scope contract remains governing.
- **Unlocks:** a real final-1.0 technical readiness transition without changing
  source bytes to record post-build evidence.
- **Risks / tradeoffs:** an evidence sidecar can only validate recorded provenance
  mechanically; it must not pretend to independently query GitHub or make the
  owner decision.
- **Reversibility:** high; bounded release tooling/docs/tests.
- **Evidence gaps:** none that change whether the current gate is unsatisfiable.

### PATH-2 — Expand Version 1.0 to native-harness/usefulness claims before release

- **Future state:** Version 1.0 advertises stronger native-harness, portability,
  or usefulness claims backed by new empirical evidence.
- **Why plausible:** qualification protocols and retained evidence machinery exist,
  and the product strategy recognizes these as unresolved product questions.
- **Frontier grounding:** FRONTIER-2.
- **Builds on:** external qualification verifier and normal-use evidence lanes.
- **Requires:** fresh empirical work, explicit scope/promise reconsideration, and
  potentially Level-4/owner authorization.
- **Construction sequence:** authorize evidence program -> run real harnesses ->
  reconcile results -> decide whether to expand support claims.
- **Dependencies:** owner direction to resume empirical/native qualification for
  stronger claims.
- **Unlocks:** broader Version 1.0 support promise.
- **Risks / tradeoffs:** delays finalization and silently changes the current
  reduced-scope contract if treated as mandatory without owner ratification.
- **Reversibility:** moderate; evidence collection is reversible, public claim
  expansion is more consequential.
- **Evidence gaps:** real native/usefulness evidence is deliberately absent.

## 6. Qualitative Path Comparison

PATH-1 directly serves the current reduced-scope Version 1.0 commitment, removes a
hard mechanical blocker, is repository-answerable, reversible, and preserves all
claim ceilings. Deferral keeps final readiness impossible.

PATH-2 addresses a broader product-value question, but current authority explicitly
marks those claims deferred/non-required. Promoting it now would convert a
deliberately excluded evidence program into an implicit release prerequisite and
would exceed the current bounded completion objective.

## 7. Decision-Changing Uncertainty

The material question was whether the final readiness blocker was merely missing
external evidence or whether the repository-local gate itself was unsatisfiable.

Direct inspection resolves that uncertainty: the script unconditionally reports
missing exact-head CI evidence and defines no satisfiable CI-evidence input path.
No experiment is required.

## 7A. Decision Assumptions and Reassessment Triggers

- **ASSUMPTION-1:** the reduced-scope Version 1.0 contract remains the governing
  release promise.
  - Reassess if the owner explicitly promotes native-harness, portability, or
    semantic-usefulness claims into required Version 1.0 support.
- **ASSUMPTION-2:** final release evidence may be supplied as provenance-bound
  runtime/sidecar evidence rather than committed source truth.
  - Reassess if repository policy requires all final evidence to be committed
    before qualification, because that would reintroduce an exact-head
    self-reference problem.

## 8. Strategic Synthesis

The highest-value remaining difference is **not another semantic-control subsystem
and not RC3 freeze by itself**. Under the current reduced-scope product contract,
the product surface is substantially complete; the decisive repository-local gap
is that final Version 1.0 technical readiness is not mechanically reachable.

Repairing the gate is the smallest intervention that turns finalization from an
aspiration into a satisfiable transition while preserving owner/release authority.

## 9. Warranted Direction

**Disposition: BUILD**

Selected path: `PATH-1`.

Candidate bounded repository responsibility:

> Repair the final Version 1.0 readiness gate so exact-head CI evidence, artifact
> digests, and owner authorization can be supplied through provenance-safe
> non-source inputs; add positive/negative regression coverage and reconcile the
> publishing/checklist documentation without freezing, tagging, publishing, or
> changing the current release claim.

## 10. Authority and Claim Boundaries

This analysis does not authorize:

- changing the final release target to `1.0.0`;
- changing release status to `ready`;
- freezing RC3;
- tagging or publishing;
- creating owner authorization on the owner's behalf;
- claiming native-harness compatibility, portability, or semantic usefulness;
- closing external Issue #384.

## 11. Evidence

- `release-v1.0.yaml` — reduced-scope 1.0 support contract; native/usefulness
  claims deferred and non-required.
- `docs/release-v1.0-checklist.md` — authoritative final publication gate must
  return `READY`.
- `scripts/validate-release-readiness.py` — unconditional exact-head CI blocker
  and in-workspace owner/digest evidence assumptions.
- `.github/workflows/release-candidate.yml` — exact-head distribution workflow
  already produces build/install/digest evidence.
- `docs/PUBLISHING.md` — publication and final 1.0 remain owner-controlled.
- `.gitignore` — `dist/` is ignored, but no final release evidence sidecar
  boundary is currently defined.
- Issue #384 — separate external GitHub-admin governance gap.

## 12. Machine-Readable Summary

```yaml
schema_version: 2
artifact_id: strategic_repository_analysis
analysis_ref: "SRA-2026-09-22-V1-COMPLETION"
continuity:
  prior_analysis_ref: "artifacts/strategic_repository_analysis.md@81e01c971b1196d24fa63fd071a4a1eb91e954e6"
  disposition: SUPERSEDE
  prior_selected_path_id: PATH-1
  reason: "The prior post-#401 currentness responsibility is complete; the owner now asks the materially broader final-Version-1.0 completion question."
target_repository: ThorStarlord/sensemaking-skills
target_source_identity: "main@a3d83c14de033734d33296ff3f45ebc5f4d8d911"
governing_intent: "Finish Version 1.0 under the current product strategy and reduced-scope support contract, continuing autonomously through repository-answerable work while preserving owner/external boundaries."
governing_authority_refs:
  - docs/product-strategy.md
  - docs/adr/0029-current-product-boundary.md
  - release-v1.0.yaml
  - docs/release-v1.0-contract.md
capability_states:
  - capability_id: reduced-scope-stable-surface
    state: ESTABLISHED
    evidence_refs:
      - release-v1.0.yaml
      - docs/public-surface-v1.0.md
  - capability_id: exact-head-distribution-qualification
    state: ESTABLISHED
    evidence_refs:
      - .github/workflows/release-candidate.yml
      - docs/PUBLISHING.md
  - capability_id: final-release-readiness-gate
    state: PARTIAL
    evidence_refs:
      - scripts/validate-release-readiness.py
      - docs/release-v1.0-checklist.md
  - capability_id: native-harness-evidence
    state: DEFERRED
    evidence_refs:
      - release-v1.0.yaml
      - docs/release-v1.0-contract.md
  - capability_id: semantic-usefulness-evidence
    state: DEFERRED
    evidence_refs:
      - release-v1.0.yaml
      - docs/product-strategy.md
  - capability_id: github-main-protection
    state: BLOCKED
    evidence_refs:
      - https://github.com/ThorStarlord/sensemaking-skills/issues/384
  - capability_id: final-publication-authorization
    state: BLOCKED
    evidence_refs:
      - docs/PUBLISHING.md
      - docs/release-v1.0-checklist.md
strategic_frontier:
  - frontier_id: FRONTIER-1
    statement: "The authoritative final Version 1.0 readiness gate is structurally unable to reach READY while preserving exact-head provenance."
    evidence_refs:
      - scripts/validate-release-readiness.py
      - docs/release-v1.0-checklist.md
      - .gitignore
    affected_capability_ids:
      - final-release-readiness-gate
      - exact-head-distribution-qualification
    strategic_consequence: "Without a satisfiable final gate, the implemented reduced-scope product cannot complete the Version 1.0 technical readiness transition."
  - frontier_id: FRONTIER-2
    statement: "Stronger native-harness, portability, and semantic-usefulness claims remain empirically unqualified but are explicitly deferred from the reduced-scope Version 1.0 promise."
    evidence_refs:
      - release-v1.0.yaml
      - docs/release-v1.0-contract.md
      - docs/product-strategy.md
    affected_capability_ids:
      - native-harness-evidence
      - semantic-usefulness-evidence
    strategic_consequence: "Promoting these claims would broaden the Version 1.0 support promise and require fresh empirical/owner authority rather than ordinary release completion."
construction_paths:
  - path_id: PATH-1
    name: "Satisfiable reduced-scope Version 1.0 finalization"
    future_state: "Final technical readiness becomes reachable from an exact clean source head using provenance-bound CI, digest, and owner-authorization evidence without mutating source identity."
    frontier_refs:
      - FRONTIER-1
    why_plausible: "The required qualification workflows already exist; the missing capability is a correct evidence-consumption boundary in the final readiness gate."
    builds_on_capability_ids:
      - reduced-scope-stable-surface
      - exact-head-distribution-qualification
    required_capability_ids:
      - final-release-readiness-gate
    construction_sequence:
      - "define ignored/out-of-tree final release evidence inputs"
      - "bind CI and owner evidence to exact source identity"
      - "validate artifact digest coverage"
      - "prove READY is reachable and stale/failed evidence is rejected"
      - "reconcile publishing and checklist documentation"
    dependencies:
      - "reduced-scope Version 1.0 contract remains governing"
    unlocks:
      - "mechanically satisfiable final Version 1.0 readiness decision"
    risks:
      - "recorded sidecar evidence could be mistaken for independent live GitHub verification unless claim ceilings stay explicit"
    reversibility: "High; bounded release tooling, tests, and documentation."
    evidence_gaps:
      - "No decision-changing evidence gap remains for whether the current gate needs repair."
    assumptions:
      - "Final CI/owner evidence can be supplied as provenance-bound runtime sidecars rather than committed source bytes."
    reassessment_triggers:
      - "Repository policy requires all final evidence to be committed before exact-head qualification."
  - path_id: PATH-2
    name: "Broaden Version 1.0 support claims before finalization"
    future_state: "Version 1.0 includes native-harness/portability/usefulness support claims backed by fresh empirical evidence."
    frontier_refs:
      - FRONTIER-2
    why_plausible: "Existing qualification protocols and product hypotheses provide a basis for stronger claims if the owner chooses to expand the release promise."
    builds_on_capability_ids:
      - reduced-scope-stable-surface
      - native-harness-evidence
      - semantic-usefulness-evidence
    required_capability_ids:
      - native-harness-evidence
      - semantic-usefulness-evidence
    construction_sequence:
      - "obtain explicit owner authorization for stronger evidence program"
      - "run real native-harness and usefulness qualification"
      - "reconcile claim ceilings and support contract"
    dependencies:
      - "owner/Level-4 decision to broaden the current reduced-scope Version 1.0 promise"
    unlocks:
      - "broader supported Version 1.0 claim set"
    risks:
      - "silently converts deferred research/product questions into release blockers and delays finalization"
    reversibility: "Empirical inquiry is reversible; published claim expansion is more consequential."
    evidence_gaps:
      - "Real native-harness, portability, and usefulness evidence is currently absent."
    assumptions:
      - "The owner may prefer a broader Version 1.0 promise than the current reduced-scope contract."
    reassessment_triggers:
      - "Owner explicitly promotes one or more deferred claims into required Version 1.0 support."
path_comparison:
  - path_id: PATH-1
    lenses:
      mission_relevance: "Directly completes the current bounded Version 1.0 promise without inventing new product scope."
      decision_value: "Resolves a hard technical blocker to a real final-readiness decision."
      blocking_power: "The current gate can never return READY, so this boundary blocks every finalization path."
      evidence_sufficiency: "Direct source inspection establishes the defect and the existing workflows establish the available evidence producers."
      consequence_of_error: "Low to moderate; the repair is bounded and must retain explicit claim ceilings around recorded evidence."
      deferral_cost: "Final Version 1.0 remains mechanically unreachable regardless of otherwise green qualification."
      reversibility: "High; release tooling/tests/docs can be reverted without changing product runtime semantics."
      authority_availability: "Repository-local repair is within the delegated scope; final release remains owner-reserved."
      dependency: "Depends only on the existing reduced-scope contract and current release workflow."
  - path_id: PATH-2
    lenses:
      mission_relevance: "Could strengthen the public product promise, but exceeds what the current reduced-scope Version 1.0 contract requires."
      decision_value: "Potentially high for broader product confidence, but not needed to answer the current finalization decision."
      blocking_power: "Low under current authority because these claims are explicitly deferred/non-required."
      evidence_sufficiency: "Fresh external empirical evidence is absent and would require a separately authorized program."
      consequence_of_error: "High if promoted implicitly because it changes the release promise and could manufacture an unnecessary release blocker."
      deferral_cost: "Acceptable under the current claim ceiling; the product can honestly ship without these claims."
      reversibility: "Inquiry is reversible, but public support-claim expansion is authority-sensitive."
      authority_availability: "Not currently established for making these claims mandatory."
      dependency: "Depends on explicit owner/Level-4 scope expansion plus external evidence."
decision_changing_uncertainty:
  statement: "Is final Version 1.0 blocked only by missing external evidence, or is the repository-local final readiness gate itself unsatisfiable?"
  could_change: "Whether the next responsibility is release-gate repair versus simply gathering final external evidence."
  inquiry_warranted: false
  evidence_needed: "None; direct source inspection shows an unconditional CI-evidence blocker and no satisfiable exact-head evidence input path."
  source: repository_evidence
decision_assumptions:
  - assumption_id: ASSUMPTION-1
    statement: "The reduced-scope Version 1.0 contract remains governing."
    evidence_refs:
      - release-v1.0.yaml
      - docs/release-v1.0-contract.md
    reassessment_triggers:
      - "Owner explicitly expands required Version 1.0 support claims."
  - assumption_id: ASSUMPTION-2
    statement: "Final release evidence may be supplied as provenance-bound sidecar/runtime evidence rather than committed source truth."
    evidence_refs:
      - .github/workflows/release-candidate.yml
      - docs/PUBLISHING.md
    reassessment_triggers:
      - "Repository policy requires final CI/authorization evidence to be committed before qualification."
strategic_disposition: BUILD
selected_path_id: PATH-1
candidate_repository_responsibility: "Repair the final Version 1.0 readiness gate so exact-head CI evidence, artifact digests, and owner authorization can be supplied through provenance-safe non-source inputs; add positive/negative regressions and reconcile release documentation."
smallest_warranted_intervention: "Bounded release-readiness script, tests, ignored evidence boundary, and publishing/checklist documentation; no product runtime/schema change and no release transition."
implementation_authority_established_by_artifact: false
semantic_truth_established: false
created_at: "2026-09-22T05:30:00Z"
immutable: true
```
