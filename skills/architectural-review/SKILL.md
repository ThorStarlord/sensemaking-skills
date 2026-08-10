# Architectural Review Skill

Evaluates proposed architectural responses against principal-engineer judgment: capability abstraction vs. features, bottleneck detection, user experience inversion, architectural risk mapping, and quantifiable success validation.

---

## Workflow

**Input**: 
- Artifact: `repository_sensemaking_brief` (from repo-sensemaker diagnostic)
- Named input: `proposed_direction` (user-supplied architecture proposal)

**Output**:
- Artifact: `architectural_review_recommendation` (decision + risk analysis)

**Invocation**: Only via `--from-session` with pre-written `proposed_direction.md` in session directory.

---

## Boundary Rules

1. **Do not re-diagnose the repository.** Trust `repository_sensemaking_brief` as the authoritative fog classification and evidence base.

2. **Evidence reuse**: When citing evidence from the brief, reference sections directly (e.g., "See brief, section X, evidence Y"). Do not re-cite repository files independently.

3. **Proposed response evaluation**: Evaluate whether the *proposed* response architecturally addresses the identified fog, not whether the fog classification is correct. Leave fog validation to repo-sensemaker.

4. **Insufficient brief handling**: If the brief is incomplete or insufficient, return `investigate_first` and recommend running a more comprehensive fog workflow. Do not supplement the brief independently.

5. **Output decision outcomes**: Every recommendation must result in one of: `pursue`, `pursue_narrowed`, `investigate_first`, `defer`, or `reject`. Decisions must be actionable and justified with specific risks, constraints, or conditions.

6. **Optional Section 15 awareness** (candidate, unratified — see `docs/candidate/architecture-decision.md`, Decision 4). If the brief has a Section 15 `extended_analysis` block, you may use two of its fields; absence of Section 15 changes nothing about this workflow.
   - `consequential_boundary.is_demonstrated_weakness: true` means the weakness **described by `consequential_boundary` itself** is independently, currently demonstrated (not just plausible). Before applying this to your verdict, establish what `consequential_boundary.description` actually names — **do not assume it refers to Section 6's `weakest_boundary` merely because both appear in the same brief.** Section 15 is deliberately allowed to name a different boundary than Section 6 (see the template's own note on this); co-occurrence is not equivalence, and this rule does not require the two sections to agree.
     - If the proposal under review addresses the boundary `consequential_boundary` describes, but only partially: that's narrower than what the evidence supports — pushes toward `pursue_narrowed` rather than `pursue`, because the verdict should say so rather than imply full resolution.
     - If the proposal was never targeting the boundary `consequential_boundary` describes at all — a separate, disclosed, `is_demonstrated_weakness: true` defect that the proposal doesn't touch and isn't a partial cut at — note it explicitly as a separate finding in your risk analysis (the calling agent should know it exists and remains open), but do not let its mere presence narrow the verdict on the proposal's own target. Unaddressed-and-unrelated is not the same failure mode as addressed-but-incomplete.
   - `domain` (a list) names every fog dimension genuinely implicated. If any value in `domain` is outside this review's own competence (e.g. a `product` domain value when you're evaluating pure architectural merit), say so explicitly in the recommendation as an out-of-lens disclosure — do not silently stay quiet about it, and do not expand scope to cover it yourself.
   This does not change Boundary Rule 1 (still do not re-diagnose) or Boundary Rule 4 (still return `investigate_first` for an insufficient brief) — it only adds two optional inputs to the reasoning in Boundary Rules 2-3 above. It does not introduce any requirement that Section 6 and Section 15 agree with each other.

---

## Execution Protocol

1. **Parse inputs**: Load `repository_sensemaking_brief` and `proposed_direction` as separate contexts.

2. **Analyze proposed response**: Map the proposal against the brief's fog classification and evidence:
   - Does it address the identified weaknesses?
   - Does it introduce new risks or bottlenecks?
   - Does it preserve existing authority boundaries?

3. **Risk identification**: Enumerate specific risks, not generic concerns. Examples of sufficient specificity:
   - ❌ "This could become another source of truth" (vague)
   - ✅ "Workspace becomes second orchestration layer, conflicting with identity model authority" (specific, bounded, testable)

4. **Decision reasoning**: Provide explicit reasoning for each decision type:
   - **pursue**: Proposal addresses fog with acceptable risk profile
   - **pursue_narrowed**: Proposal is sound only under specific constraints (list them)
   - **investigate_first**: Propose additional investigation or validation steps needed before proceeding
   - **defer**: Proposal is sound but timing/priority makes it incorrect now (specify conditions for reconsideration)
   - **reject**: Proposal creates unacceptable risks or architectural violations (specify kill conditions)

5. **Success measures**: For any `pursue` decision, define how success will be measured:
   - Metric: What will be measured
   - Baseline: Current state
   - Target: Desired outcome
   - Method: How measurement will be performed

---

## References

- [Artifact Contract](../../workflow-planner/references/artifact-contracts.yaml): `architectural_review_recommendation`
- [Workflow Registry](../../workflow-planner/references/workflow-registry.yaml): `architectural-review-planning-workflow`
- [Skill Registry](../../workflow-planner/references/skill-registry.yaml): `architectural-review`
- [Design Document](../../docs/skill-design-architectural-review.md): Full specification
- [Template](./references/architectural-review-template.md): Artifact template
- [Trigger Policy](./references/architectural-review-trigger-policy.md): When to invoke this skill

---

## Invocation Prerequisite (v1)

This skill requires a pre-written `proposed_direction.md` artifact supplied by the caller in a session directory. The runtime uses `--from-session <path>` to locate this pre-written artifact before invoking the skill.

**In v1, fresh invocations cannot supply `proposed_direction` directly** because the session directory is not knowable until `workflow-runtime.py` starts. The workflow therefore supports only existing-session invocation (Possibility A):

1. Caller creates a session directory with a unique ID
2. Caller writes `00-user-intent.md` (required by all workflows)
3. Caller writes `proposed_direction.md` with the proposal
4. Caller invokes: `python workflow-runtime.py --workflow architectural-review-planning-workflow --from-session <path>`

See `INVOCATION-GUIDE.md` for step-by-step procedures.

---

## Regression Testing

Baseline test: `tests/integration/test_end_to_end_workflows.py` (existing workflows, structural only)

New E2E test: `tests/test_architectural_review_recommendation_runtime.py`
- Covers validator dispatch, input resolution, control flow
- Exercises artifact path scoping and session-directory handling
- Verifies missing-input hard-fail before skill invocation

No changes required to existing workflows. This skill is optional; existing workflows remain unchanged.

---

## References by Role

**For agents**: Read the artifact template and trigger policy to understand when and how to invoke this skill.

**For implementation**: See the full design document in `docs/skill-design-architectural-review.md`.

**For validation**: The specialized validator `validate-architectural-review-recommendation.py` enforces decision consistency and required fields.
