# Hardening Review: `repo-sensemaker` Workflow ID Verification

## 1. Executive Summary
This review evaluates whether the `repo-sensemaker` skill should be required to verify `workflow_id` values against `workflow-registry.yaml`. The investigation confirms that current instructions allow for semantic hallucination of routing labels, as seen in the `wave-1-execution` mismatch.

## 2. Review Questions

### 1. Does `repo-sensemaker` currently have authority to recommend `workflow_id` values?
**Yes.** 
- `skills/repo-sensemaker/SKILL.md` (Step 6) explicitly instructs the agent to "Produce a Repository Sensemaking Brief with candidate next steps and recommended workflows."
- `skills/repo-sensemaker/references/repo-analysis-template.md` includes a `recommended_workflow_id` field in the machine-readable handoff section.

### 2. If yes, does its contract require registry verification?
**No.** 
The current `SKILL.md` instructs the agent to "Inspect README, core files, folder structure, and existing documentation" (Step 1), but it does not mandate a lookup in `skills/workflow-orchestrator/references/workflow-registry.yaml` specifically to validate the recommended ID.

### 3. Was the `wave-1-execution` mismatch caused by skill instructions, template ambiguity, missing validator coverage, or generated-artifact error?
**Multi-factor root cause:**
- **Skill Instructions**: Lack of "Registry-First" constraint for ID selection.
- **Template Ambiguity**: Presence of a machine-readable field without an explicit "Must match registry" comment.
- **Generated-Artifact Error**: The agent prioritized task-local context (the "Wave 1" test plan) over repository-global state (the registry).
- **Validator Coverage**: Unconfirmed. `scripts/validate-brief.py` exists, but this review did not inspect whether it validates `recommended_workflow_id` against `workflow-registry.yaml`.

### 4. Should the fix be: skill instruction hardening, template hardening, validator hardening, orchestrator-only containment, or no change?
**Recommended Fix: Layered Hardening.**
1. **Skill Instruction Hardening**: Explicitly require the agent to consult `workflow-registry.yaml` before writing the brief.
2. **Validator Hardening**: If the unconfirmed check in `scripts/validate-brief.py` is absent, update the validation logic to reject briefs containing `workflow_id` values that do not exist in the registry.
3. **Template Hardening**: Add a comment in the YAML block of the template to reinforce the constraint.

### 5. What is the lowest-risk recommended follow-up?
**Authorized maintenance pass, staged as:**
1. Inspect `scripts/validate-brief.py` for registry validation of `recommended_workflow_id`.
2. If missing, add validator hardening.
3. Add instruction/template hardening so `repo-sensemaker` must consult `workflow-registry.yaml` before recommending workflow IDs.
4. Do not add aliases merely to accommodate hallucinated IDs.

## 3. Evidence Mapping

| Artifact | Location | Observation |
| :--- | :--- | :--- |
| `SKILL.md` | Line 16 | Step 6 recommends workflows but lacks lookup rules. |
| `repo-analysis-template.md` | Line 47 | Placeholder `recommended_workflow_id` is blank/unconstrained. |
| `REGISTRY-DRIFT-REVIEW.md` | Section 2.1 | Confirms `wave-1-execution` was a hallucinated label. |

## 4. Conclusion
The `repo-sensemaker` should be required to verify workflow IDs. Relying on "semantic fallback" in the orchestrator is a robust safety net, but "Producer-Side Integrity" is the preferred engineering standard for the sensemaking pipeline.

**Final Recommendation**: Proceed with a staged maintenance pass: Inspect validator behavior -> Harden validator if needed -> Harden skill instructions and template.
