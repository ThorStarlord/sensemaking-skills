# Validator Ecosystem Architecture

**Status:** Living document — describes the target architecture for the artifact validation system in `sensemaking-skills`.
**See also:** [validator-stack-policy.md](../skills/workflow-orchestrator/references/validator-stack-policy.md) (execution order and enforcement), [artifact-contracts.yaml](../skills/workflow-orchestrator/references/artifact-contracts.yaml) (artifact-to-validator mapping).

---

## 1. Introduction

The validator ecosystem is a **three-level hierarchy** of Python scripts that enforce artifact integrity throughout the sensemaking pipeline. Every artifact produced by a skill passes through at least one validator before it is consumed by the next skill.

The ecosystem ensures:

- **Structural integrity** — the repository itself is consistent (registries, contracts, templates)
- **Contract compliance** — every artifact has its required sections, machine fields, and no absolute paths
- **Semantic fidelity** — cross-references to registries are valid, classifications are recognized, evidence is grounded

---

## 2. System Context

```
Skill produces                    Validator checks               Next skill or
artifact (markdown)  ───────>     artifact against      ───────> external agent
                                 its contract
                                       │
                                       ▼
                              Error report (stderr)
                              Exit code 0 = pass
                              Exit code 1 = fail
```

Validators are **stateless** scripts. They take an artifact file path, optionally a repo root for registry lookups, and return error lines and an exit code. They do not modify files.

---

## 3. The Three-Level Hierarchy

| Level | Type | Scope | Script | Input |
|-------|------|-------|--------|-------|
| **1** | Structural | Repository integrity, registries, branch safety | `scripts/validate-repo.py` | No artifact — validates full repo state |
| **2** | Generic | Artifact contract compliance (sections, machine fields, paths) | `scripts/validate-artifact.py` | `artifact_id` + `artifact_path` |
| **3** | Specialized | Semantic fidelity, evidence grounding, domain-specific logic | One per artifact type (see below) | `artifact_path` |

### Level 1 — Structural (`validate-repo.py`)

Validates the repository itself: every required file exists, YAML files parse, skill registries are consistent, workflow steps don't reference themselves, YOLO safety policies are in place, template section headers match expected numbering.

**Not fixture-testable** — operates on the entire repo state, not a single input file. Excluded from the Validator Verification Suite.

### Level 2 — Generic (`validate-artifact.py`)

The universal validator. Given any `artifact_id` (matching a contract in `artifact-contracts.yaml`) and an artifact path, it checks:

- File exists
- No `file:///` absolute links anywhere in the content
- All required sections (from the contract) are present as `## Section Name` headings
- A YAML block containing all required machine fields exists
- For `repository_sensemaking_brief` specifically: `evidence_excerpts` YAML block is well-formed

This validator **always runs first** for any artifact. If it fails, Level 3 validators for that artifact should not run.

### Level 3 — Specialized (one per artifact type)

Domain-specific validators that understand the semantics of a particular artifact. They check things the generic validator cannot: registry cross-references, recognized classification terms, role boundaries, file-level evidence grounding.

---

## 4. Validator Contract

Every Level 2 and Level 3 validator must conform to this contract.

### 4.1 CLI Interface

```
python scripts/validate-{name}.py <artifact_path> [--repo-root PATH] [--list-codes]
```

| Argument | Required | Description |
|----------|----------|-------------|
| `artifact_path` | Yes* | Path to the artifact markdown file. May be omitted when `--list-codes` is used |
| `--repo-root` | No | Root of the repository for registry lookups. Default: `"."` |
| `--list-codes` | No | Print all stable error codes and exit 0 |

\*`artifact_path` uses `nargs="?"` so `--list-codes` can be called without it.

`validate-artifact.py` is the exception: it takes two positional arguments:

```
python scripts/validate-artifact.py <artifact_id> <artifact_path> [--repo-root PATH] [--list-codes]
```

`validate-repo.py` is the exception: it takes no positional arguments and has no `--list-codes`.

### 4.2 Output Format

All errors follow this format:

```
ERROR {CODE}: {descriptive message}
```

- Prefix `ERROR ` (with trailing space)
- CODE is a stable error code constant (e.g., `HALLUCINATED_WORKFLOW_ID`)
- Colon and space, then a human-readable message
- One error per line
- Multiple errors for the same artifact are all reported (no early exit on first error)

The success message is free text — the exit code is the authoritative signal:

| Exit code | Meaning |
|-----------|---------|
| 0 | No errors — artifact is valid |
| 1 | One or more errors — artifact is invalid |

### 4.3 Stable Error Codes

Every Level 3 validator defines error code constants at module level:

```python
HALLUCINATED_WORKFLOW_ID = "HALLUCINATED_WORKFLOW_ID"
NO_LOGIC_TRACE = "NO_LOGIC_TRACE"
```

These constants are:

- **Exposed via `--list-codes`** — printed one per line for documentation and tooling
- **Used in error output** — every error message uses `ERROR {CODE}: {message}`
- **Used in negative fixtures** — `expected_error_contains` frontmatter references the code
- **Guaranteed stable** — codes do not change between versions. A code may be deprecated but never removed without a major version bump

### 4.4 Entry Point Pattern

```python
def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(...)
    args = parser.parse_args(argv)
    if args.list_codes:
        for code in ALL_CODES:
            print(code)
        return 0
    errors = validate(args.artifact_path, args.repo_root)
    for e in errors:
        print(f"ERROR {e}")
    return 1 if errors else 0

if __name__ == "__main__":
    sys.exit(main())
```

This enables programmatic use: other scripts can `import` the module and call `main([...])` instead of subprocessing.

### 4.5 Shared Utility Module

`scripts/_validator_utils.py` provides shared functions that validators import for common operations:

| Function | Purpose |
|----------|---------|
| `load_yaml(path)` | Safe YAML load with error wrapping |
| `load_workflow_registry(repo_root)` | Load `workflow-registry.yaml` |
| `load_artifact_contracts(repo_root)` | Load `artifact-contracts.yaml` |
| `load_skill_registry(repo_root)` | Load `skill-registry.yaml` |
| `load_weakness_types(repo_root)` | Parse `weakness-types.md` |
| `format_error(code, message)` | Return `"{code}: {message}"` |
| `resolve_repo_root(given, script_dir)` | Resolve relative repo root path |

---

## 5. Registration and Discovery

### 5.1 Artifact-to-Validator Mapping

`skills/workflow-orchestrator/references/artifact-contracts.yaml` is the canonical registry. Each artifact entry specifies:

```yaml
- id: repository_sensemaking_brief
  produced_by: repo-sensemaker
  consumed_by: [workflow-orchestrator, prompt-handoff]
  verification:
    generic_validator: "python scripts/validate-artifact.py repository_sensemaking_brief {artifact_path}"
    specialized_validators:
      - "python scripts/validate-brief.py {artifact_path}"
    required_for_modes: [guided_execution, autonomous_execution, yolo_execution]
```

- `generic_validator` — always `validate-artifact.py` with the `artifact_id`
- `specialized_validators` — zero or more Level 3 validators for this artifact type
- `required_for_modes` — which execution modes enforce this validation

### 5.2 Auto-Discovery by the Test Suite

`scripts/test-validators.py` discovers validators by scanning `scripts/` for files matching `validate-*.py`. For each discovered script, it expects a fixture directory at `tests/fixtures/{script-name}/` containing `valid/` and `invalid/` subdirectories.

`validate-repo.py` is excluded from auto-discovery (it has no fixture directory). The underscore-prefixed `_validator_utils.py` is naturally excluded (doesn't match `validate-*.py`).

---

## 6. Verification Model

### 6.1 Fixture-Based Testing

Every validator (except Level 1) must have:

```
tests/fixtures/{validator-name}/
├── valid/
│   └── {name}.md          # A valid artifact that should pass
└── invalid/
    ├── {name}.md           # An invalid artifact that should fail
    └── ...                 # One fixture per error condition
```

Each fixture file has YAML frontmatter:

```yaml
---
validator_case: negative        # "positive" or "negative"
expected_error_contains: CODE    # For negative: the stable error code expected
validator_args: []               # Optional extra CLI args
---
```

### 6.2 Validator Verification Suite

`scripts/test-validators.py`:

1. Auto-discovers all `validate-*.py` scripts
2. For each, finds its fixture directories
3. Runs each positive fixture — expects exit 0
4. Runs each negative fixture — expects exit 1 and output containing `expected_error_contains`
5. Checks `tests/fixtures/REGRESSIONS.yaml` for required regression cases
6. Enforces coverage: every non-excluded validator must have a fixture directory
7. Generates a report with pass/fail per case

### 6.3 Regression Cases

`tests/fixtures/REGRESSIONS.yaml` lists required regression tests that must run every time:

```yaml
required_cases:
  - id: repo-sensemaker-workflow-id-hallucination
    validator: validate-brief
    fixture: tests/fixtures/validate-brief/invalid/repo-sensemaker-id-hallucination.md
    reason: Prevent regression of hallucinated workflow IDs such as wave-1-execution.

excluded_validators:
  - validator: validate-repo
    reason: Repository-level meta-validator; not fixture-tested by the Validator Verification Suite.
```

---

## 7. Coverage Map

| Artifact ID | Level 2 | Level 3 | Status |
|-------------|---------|---------|--------|
| `problem_frame` | ✅ validate-artifact.py | ❌ | Generic only |
| `unknowns_map` | ✅ validate-artifact.py | ❌ | Generic only |
| `repository_sensemaking_brief` | ✅ validate-artifact.py | ✅ validate-brief.py | Full |
| `workflow_orchestration_plan` | ✅ validate-artifact.py | ✅ validate-plan.py | Full |
| `skill_improvement_plan` | ✅ validate-artifact.py | ✅ validate-skill-improvement-plan.py | Full |
| `usage_research_report` | ✅ validate-artifact.py | ✅ validate-usage-research-report.py | Full |
| `prompt_handoff` | ✅ validate-artifact.py | ❌ (planned) | Specialized planned |
| All other artifact types (15) | ✅ validate-artifact.py | ❌ | Generic only |

**Design principle:** A Level 3 validator is added only when the artifact has external registry cross-references to validate, domain-specific semantics beyond section presence, or a high blast radius if broken (e.g., consumed by external agents with no human review).

---

## 8. How to Add a New Validator

1. **Decide if it needs Level 3.** If the generic contract check (sections, paths, machine fields) is sufficient, stop.

2. **Create the validator script.** Follow the contract in section 4:
   - `scripts/validate-{name}.py`
   - Stable error code constants
   - Standard CLI (`artifact_path`, `--repo-root`, `--list-codes`)
   - `ERROR {CODE}: {message}` output
   - `main(argv) -> int` entry point
   - Use `_validator_utils.py` for registry loading

3. **Register in `artifact-contracts.yaml`.** Add to the artifact's `verification.specialized_validators` list.

4. **Create fixtures.** At minimum one valid and one invalid:
   - `tests/fixtures/validate-{name}/valid/{name}.md`
   - `tests/fixtures/validate-{name}/invalid/{condition}.md` (one per error code)

5. **Add a regression case** to `tests/fixtures/REGRESSIONS.yaml` for the most critical error condition.

6. **Verify:**
   ```bash
   python scripts/test-validators.py
   python scripts/validate-repo.py   # Ensure Level 1 still passes
   ```

---

## 9. File Reference

| File | Purpose |
|------|---------|
| `scripts/validate-repo.py` | Level 1 — structural repo integrity |
| `scripts/validate-artifact.py` | Level 2 — generic artifact contract checks |
| `scripts/validate-brief.py` | Level 3 — repository sensemaking brief specialist |
| `scripts/validate-plan.py` | Level 3 — orchestration plan specialist |
| `scripts/validate-skill-improvement-plan.py` | Level 3 — skill improvement plan specialist |
| `scripts/validate-usage-research-report.py` | Level 3 — usage research report specialist |
| `scripts/_validator_utils.py` | Shared utility functions for registry loading and error formatting |
| `scripts/test-validators.py` | Validator Verification Suite (fixture runner) |
| `tests/fixtures/REGRESSIONS.yaml` | Required regression test cases and excluded validators |
| `tests/fixtures/{validator-name}/` | Fixture directories per validator |
| `skills/workflow-orchestrator/references/artifact-contracts.yaml` | Canonical artifact-to-validator mapping |
| `skills/workflow-orchestrator/references/validator-stack-policy.md` | Execution order and enforcement rules |
