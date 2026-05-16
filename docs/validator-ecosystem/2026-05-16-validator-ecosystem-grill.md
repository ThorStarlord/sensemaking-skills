# Validator Ecosystem: Grill Session Output

**Date:** 2026-05-16
**Method:** grill-with-docs
**Repo:** sensemaking-skills

---

## Current Landscape

### The Three-Level Validator Hierarchy

As defined in `skills/workflow-orchestrator/references/validator-stack-policy.md`:

| Level | Type | Scope | Scripts |
|-------|------|-------|---------|
| **Level 1** | Structural | Repository integrity, registries, branch safety | `validate-repo.py` |
| **Level 2** | Generic | Artifact contract compliance (sections, machine fields, paths) | `validate-artifact.py` |
| **Level 3** | Specialized | Semantic fidelity, evidence grounding, domain-specific logic | `validate-brief.py`, `validate-plan.py`, `validate-skill-improvement-plan.py`, `validate-usage-research-report.py` |

### Artifact Coverage

`artifact-contracts.yaml` registers **22 artifact types**. Coverage breakdown:

- **4 have specialized (Level 3) validators**: `repository_sensemaking_brief`, `workflow_orchestration_plan`, `skill_improvement_plan`, `usage_research_report`
- **18 have only generic (Level 2) validation**: section presence, `file:///` ban, YAML field checks
- **All pass through Level 2**: `validate-artifact.py` handles any `artifact_id` against its contract

### Workflow Registry

11 registered workflows, all producing or consuming artifacts from the contract registry. The most common terminal artifact is `prompt_handoff` (used by 10 of 11 workflows), consumed by `external_agent`.

---

## Inconsistencies Discovered

### CLI Interface Fragmentation

| Dimension | validate-repo | validate-artifact | validate-brief | validate-plan | validate-skill-imp-plan | validate-usage-research |
|---|---|---|---|---|---|---|
| `--repo-root` | ❌ (no args) | ✅ | ✅ | ✅ | ✅ | ❌ |
| Positional arg | N/A | `artifact_id` + `artifact_path` | `artifact_path` | `plan_path` | `plan_path` | `report_path` |
| Stable error codes | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ |
| `main(argv)` entry | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ |
| Machine output | ❌ | ❌ | `ERROR CODE: msg` | ❌ | ❌ | ❌ |
| `--list-codes` | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ |
| Test suite coverage | excluded | ✅ | ✅ | ✅ | ✅ | ✅ |

### Registry Loading Redundancy

Every validator that needs registry data loads and parses YAML files independently. No shared utility exists.

- `validate-brief.py`: loads `workflow-registry.yaml`, `weakness-types.md`
- `validate-plan.py`: loads all 3 registries (workflow, artifact-contracts, skill-registry)
- `validate-artifact.py`: loads `artifact-contracts.yaml`
- `validate-repo.py`: loads 10+ YAML files inline

### Entry Point Patterns

Only `validate-brief.py` has a proper `main(argv=None) -> int` entry point. The others parse args and exit directly in `if __name__ == "__main__":`.

### Output Formats

`validate-brief.py` outputs `ERROR CODE: descriptive message`. All others output ` - message` with no code prefix. The test-validators.py harness checks for substring matches in output, so either format works, but the hybrid prevents uniform machine parsing.

---

## Decisions and Rationale

### Scope: Standardize + One Addition (Reject Full Coverage)

**Decision:** Focus on standardizing the existing 6 validators. Add one new specialized validator for `prompt_handoff`. Do not add validators for the other 17 artifact types.

**Rationale:**
- Specialized validators add value only for artifacts with external registry cross-references, domain-specific semantics, or internal structural constraints beyond section presence
- Most product artifacts (persona_definition, okr_list, roadmap, story_list, etc.) are adequately served by generic section checks
- The cost of maintaining a validator (fixtures, regression tests, documentation) is non-trivial per validator

### prompt_handoff: Highest-Value Gap

**Decision:** Add a specialized validator for `prompt_handoff`.

**Rationale:**
- Terminal artifact in 10 of 11 workflows — broken handoffs break entire pipelines
- Consumed by `external_agent` — no human review before execution
- Checkable: `target_skill` exists in registry, `stop_condition` has real content, no hallucinated skill IDs
- `prompt-handoff` and `handoff` both produce it — single validator covers both paths

### problem_frame / unknowns_map: Skip

**Decision:** Do not add specialized validators.

**Rationale:**
- Only 7 and 6 sections respectively
- No cross-registry references to validate
- Generic validator already checks section presence and machine fields
- Adding validators for these would be building "just because we can"

### Shared Library: Single Module

**Decision:** `scripts/_validator_utils.py` — a single module, not a package.

**Rationale:**
- Lower friction than a package (no `__init__.py`, no import restructuring)
- 5 of 6 validators duplicate registry-loading code — one shared module eliminates this
- The leading underscore signals "internal, not a validator itself"
- test-validators.py auto-discovers by `startswith("validate-")`, so `_validator_utils.py` is naturally excluded

### validate-repo: Structural Exception

**Decision:** Keep `validate-repo.py` structurally different. It can use shared utilities for registry loading where convenient, but don't force the standard CLI pattern on it. Remain excluded from the fixture-based test suite.

**Rationale:**
- Takes no artifact input — validates entire repository state
- Cannot be fixture-tested (no single input file)
- Its purpose (cross-cutting integrity) is fundamentally different from artifact validators

### Standard CLI Contract

**Decision for all Level 2 and Level 3 validators:**

```
python scripts/validate-{name}.py <artifact_path> [--repo-root PATH] [--list-codes]
```

- Exit code 0 = pass, 1 = any error found
- `artifact_path` positional (nargs="?" to allow `--list-codes` without it)
- `--repo-root` defaults to `"."`
- `--list-codes` prints stable error codes and exits 0

### Standard Output Format

**Decision for all Level 3 validators:**

```
ERROR {CODE}: {descriptive message}
```

- Machine-parseable by prefix (`ERROR `) and code field
- Human-readable after the colon
- Compatible with test-validators.py substring matching
- Level 2 (validate-artifact.py) can optionally adopt this for its own error codes

### Stable Error Codes: All Level 3

**Decision:** Every Level 3 validator defines module-level error code constants and exposes them via `--list-codes`.

**Rationale:**
- Enables regression testing against specific error codes (not fuzzy substring matching)
- `validate-brief.py` already does this — proven pattern
- Allows the test suite to assert "failed for the right reason"
- Enables downstream tooling to handle errors by code

### Add --repo-root to validate-usage-research-report.py

**Decision:** Add `--repo-root` flag for interface uniformity. No behavioral change initially.

**Rationale:**
- Removes the hardcoded script-name check in `test-validators.py` line 35-36
- Enables future use (e.g., registry-aware role boundary checks)
- Zero cost: the flag exists but doesn't change current behavior

---

## Terminology

| Term | Definition |
|------|------------|
| **Validator Ecosystem** | The complete set of validator scripts, their shared utilities, fixture-based test suite, and the contract registry that maps artifacts to validators |
| **Level 1 (Structural)** | Validates cross-cutting repository integrity. Single script: `validate-repo.py`. Not fixture-testable |
| **Level 2 (Generic)** | Validates any artifact against its contract. Single script: `validate-artifact.py`. Takes `artifact_id` + `artifact_path` |
| **Level 3 (Specialized)** | Domain-specific semantic validation for a single artifact type. One script per artifact type |
| **Stable Error Code** | A named string constant (e.g., `HALLUCINATED_WORKFLOW_ID`) that is guaranteed not to change between versions. Used for regression testing and machine parsing |
| **Fixture Coverage** | Every validator (except Level 1) must have `tests/fixtures/{validator-name}/valid/` and `tests/fixtures/{validator-name}/invalid/` directories with at least one fixture each |
| **Negative Fixture** | A deliberately invalid artifact that the validator must reject with a specific error code |
| **Validator Verification Suite** | `scripts/test-validators.py` — runs every validator against its fixtures and reports pass/fail |
| **Contract Mapping** | The `artifact-contracts.yaml` file that maps each `artifact_id` to its `generic_validator` and `specialized_validators` |
| **Artifact-Driven Validation** | Validation is organized around artifacts, not skills. A validator checks the output artifact contract, not the producing skill's behavior |
