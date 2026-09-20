# Strategic Repository Analysis

## 1. Governing Intent and Scope

State owner intent, repository-owned product authority, target repository, exact
source identity when available, and analysis/implementation authority boundary.

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
- **Dependencies:**
- **Unlocks:**
- **Risks / tradeoffs:**
- **Reversibility:**
- **Evidence gaps:**

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
target_repository: owner/repository
target_source_identity: "<commit/tree/ref or documented-unverified>"
governing_intent: "<owner/repository strategy statement>"
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
    dependencies:
      - "<dependency>"
    unlocks:
      - "<what becomes possible>"
    risks:
      - "<material risk/tradeoff>"
    reversibility: "<qualitative explanation>"
    evidence_gaps:
      - "<material assumption/gap>"
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
strategic_disposition: BUILD
selected_path_id: PATH-1
candidate_repository_responsibility: "<bounded responsibility or null>"
smallest_warranted_intervention: "<intervention or null>"
implementation_authority_established_by_artifact: false
semantic_truth_established: false
created_at: "YYYY-MM-DDTHH:MM:SSZ"
immutable: true
```
