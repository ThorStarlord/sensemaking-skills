# Strategic Repository Analysis

## 1. Governing Intent and Scope

State owner intent, repository-owned product authority, target repository, exact
source identity when available, and analysis/implementation authority boundary.
When mechanically addressable governing authority files materially condition the
analysis, list them explicitly in `governing_authority_refs`. This is provenance
for currentness inspection, not a semantic claim that file change invalidates strategy.

## 1A. Strategic Continuity (when continuing prior analysis)

When a materially relevant prior strategic analysis exists, identify its stable
reference, declare the continuity disposition (`REAFFIRM | CONTINUE | REVISE |
SUPERSEDE | CLOSE`), identify the prior selected path when applicable, and state
why the relationship holds. Use `NEW` when explicitly creating a new analysis
lineage.

## 2. Current System Model

Describe the current repository/product as a system: purpose, major capabilities,
architecture/control surfaces, current qualification/release posture when
material, constraints, and claim ceilings.

## 3. Capability and Limitation Map

| Capability | State | Evidence | Strategic relevance |
| --- | --- | --- | --- |
| ... | ESTABLISHED / PARTIAL / MISSING / DEFERRED / BLOCKED / CLAIMED_UNVERIFIED / OUT_OF_SCOPE | ... | ... |

## 4. Strategic Frontier

List only current decision-relevant repository/product boundaries.

## 5. Candidate Construction Paths

For each path include:

### PATH-1 — <name>

- **Future state:**
- **Why plausible:**
- **Builds on:**
- **Requires:**
- **Construction sequence:**
- **Path transitions (optional):** stable conceptual transition references such as
  `PATH-1/T1` when later work would otherwise be difficult to reconstruct. A
  transition is strategic provenance, not a roadmap task.
- **Dependencies:**
- **Unlocks:**
- **Risks / tradeoffs:**
- **Reversibility:**
- **Evidence gaps:**
- **Assumptions:** decision-relevant premises this path depends on, when useful.
- **Reassessment triggers:** concrete changes that should cause the path judgment
  to be reconsidered.

Repeat for each materially distinct path.

If no coherent construction path is currently warranted/representable, explicitly state
that and use `construction_paths: []` plus `path_comparison: []` in the machine
summary. Do not invent a placeholder path. A `BUILD` disposition still requires a
selected real path.

## 6. Qualitative Path Comparison

Compare paths using:

- mission relevance;
- decision value;
- blocking power;
- evidence sufficiency / resolvability;
- consequence of error;
- deferral cost;
- reversibility;
- authority availability;
- dependency;
- smallest warranted intervention.

Do not use numeric scores or weighted ranking.

## 7. Decision-Changing Uncertainty

State the uncertainty that could materially change the strategic judgment, what
it could change, whether inquiry is warranted, the smallest sufficient evidence,
and the correct evidence source.

## 7A. Decision Assumptions and Reassessment Triggers

Record only premises whose failure could materially change the strategic judgment.
Each assumption should have a stable identifier, evidence references, and one or
more reassessment triggers. Do not use confidence scores or probability fields.

## 8. Strategic Synthesis

Explain the semantic judgment across the candidate paths and why the disposition
follows from current evidence.

## 9. Warranted Direction

Declare one semantic disposition:

`BUILD | INVESTIGATE | DEFER | NO_CHANGE | OWNER_DECISION | THESIS_REVIEW`

If BUILD, identify the selected path and candidate bounded repository
responsibility.

If INVESTIGATE, identify the bounded evidence-producing responsibility.

## 10. Authority and Claim Boundaries

Explicitly state implementation authority, protected owner/external decisions,
and the claim ceiling.

## 11. Evidence

List decision-changing evidence with relative repository references and stable
line/range or identifier where available.

## 12. Machine-Readable Summary

```yaml
artifact_id: strategic_repository_analysis
analysis_ref: "SRA-<stable-reference>"
continuity:
  prior_analysis_ref: null
  disposition: NEW
  prior_selected_path_id: null
  reason: "No prior analysis is being continued."
target_repository: owner/repository
target_source_identity: "<commit/tree/ref or documented-unverified>"
governing_intent: "<owner/repository strategy statement>"
governing_authority_refs:
  - docs/product-strategy.md
capability_states:
  - capability_id: example-capability
    state: ESTABLISHED
    evidence_refs:
      - path/to/file.md:L10-L20
strategic_frontier:
  - frontier_id: FRONTIER-1
    statement: "<decision-relevant boundary>"
construction_paths:
  - path_id: PATH-1
    name: "<path name>"
    future_state: "<coherent future state>"
    builds_on:
      - "<existing capability>"
    required_capabilities:
      - "<needed capability>"
    construction_sequence:
      - "<coarse step>"
    path_transitions:
      - transition_ref: PATH-1/T1
        transition: "<conceptual capability-state transition>"
    dependencies:
      - "<dependency>"
    unlocks:
      - "<what becomes possible>"
    risks:
      - "<material risk/tradeoff>"
    reversibility: "<qualitative explanation>"
    evidence_gaps:
      - "<material assumption/gap>"
    assumptions:
      - "<decision-relevant premise>"
    reassessment_triggers:
      - "<observable condition that should trigger reconsideration>"
path_comparison:
  - path_id: PATH-1
    lenses:
      mission_relevance: "<qualitative judgment>"
      decision_value: "<qualitative judgment>"
      blocking_power: "<qualitative judgment>"
      evidence_sufficiency: "<qualitative judgment>"
      consequence_of_error: "<qualitative judgment>"
      deferral_cost: "<qualitative judgment>"
      reversibility: "<qualitative judgment>"
      authority_availability: "<qualitative judgment>"
      dependency: "<qualitative judgment>"
      smallest_warranted_intervention: "<qualitative judgment>"
decision_changing_uncertainty:
  statement: "<uncertainty or none>"
  could_change: "<which strategic judgment>"
  inquiry_warranted: false
  evidence_needed: "<smallest sufficient evidence or none>"
  source: repository_evidence
decision_assumptions:
  - assumption_id: ASSUMPTION-1
    statement: "<premise that could change the judgment if false>"
    evidence_refs:
      - path/to/file.md:L10-L20
    reassessment_triggers:
      - "<condition that should trigger strategic reconsideration>"
strategic_disposition: BUILD
selected_path_id: PATH-1
candidate_repository_responsibility: "<bounded responsibility or null>"
candidate_path_transition_ref: PATH-1/T1
smallest_warranted_intervention: "<intervention or null>"
implementation_authority_established_by_artifact: false
semantic_truth_established: false
created_at: "YYYY-MM-DDTHH:MM:SSZ"
immutable: true
```

## Path-transition boundary

Path transition identity is optional and exists only to make a selected strategic
trajectory reconstructible across later responsibilities and reconciliations.

```text
path transition != roadmap item
path transition != backlog item
path transition != authorized responsibility
transition established != next transition selected
```

Do not add scheduling/project-management fields such as priority, deadline, estimate,
percent complete, assignee, start/due date, blocked-by, or automatic next-transition
selection.
