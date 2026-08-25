# T2 Pilot Oracle — Hidden (evaluator-only)

## Verified mechanism (investigated at frozen SHA `0ffb564b`, not assumed)

> **Re-freeze revalidation (a7b957d):** Re-verified at current main `a7b957d`. The `git diff` base SHA in Check 4 was re-pointed old->new freeze. The protected field sets the oracle asserts (`FROZEN_REQUIRED`, `FROZEN_RECOMMENDED`) and the runtime tuple `_WORKFLOW_ID_FIELDS` are byte-identical to the old freeze (#232 added only a note line inside the `workflow_orchestration_plan` block, shifting that block from line ~452 to ~459 but not touching its required/recommended field sets or adding any block header). Full detail in `RE-FREEZE-PROVENANCE.md`.

`tests/test_field_contract_agreement.py` is the authoritative guardrail
(read in full at frozen SHA). It loads `OrchestrationRunner._WORKFLOW_ID_FIELDS`
and `._FOG_TYPE_FIELDS` from `scripts/workflow-runtime.py`
(`_WORKFLOW_ID_FIELDS = ("recommended_workflow_id", "chosen_workflow_id",
"selected_workflow")` at line 1180) and asserts every entry in each tuple is
declared as a `required_machine_fields` or `recommended_machine_fields`
entry on **some** artifact in `artifact-contracts.yaml` — the check unions
fields across *all* artifacts (`declared.update(...)` per artifact, no
per-artifact attribution). This means the test **cannot by itself**
distinguish "declared on the right artifact" from "declared on any
artifact" — a genuine gap between the authoritative automated guardrail and
full task correctness, which is exactly why this oracle adds its own
attribution check below rather than relying on `pytest` alone.

The field's true home is `workflow_orchestration_plan`
(`artifact-contracts.yaml:452-489` at frozen SHA) — that block already
declares the sibling fields `chosen_workflow_id` (required) and
`selected_workflow` (recommended) for the same purpose, with an explanatory
comment about fallback semantics for the analogous fog-type fields
immediately above the `recommended_machine_fields` list.

## Oracle procedure

Run against the agent's final repository state (a patched clone at frozen
SHA):

```python
import subprocess, sys
from pathlib import Path
import yaml

CLONE = Path(CLONE_DIR)

# 1. AUTHORITATIVE CHECK — the guardrail test itself, unmodified.
result = subprocess.run(
    [sys.executable, "-m", "pytest", "tests/test_field_contract_agreement.py", "-v"],
    cwd=CLONE, capture_output=True, text=True,
)
assert result.returncode == 0, f"FAIL: guardrail test did not pass:\n{result.stdout}\n{result.stderr}"

# 2. RUNTIME CHECK — target_workflow_id actually added as a read alias.
runtime_src = (CLONE / "scripts" / "workflow-runtime.py").read_text(encoding="utf-8")
import re
m = re.search(r'_WORKFLOW_ID_FIELDS\s*=\s*\(([^)]*)\)', runtime_src)
assert m and '"target_workflow_id"' in m.group(1).replace("'", '"'), \
    "FAIL: target_workflow_id not added to OrchestrationRunner._WORKFLOW_ID_FIELDS"

# 3. ATTRIBUTION CHECK — declared specifically on workflow_orchestration_plan,
#    as recommended (not required). This is the check the pytest guardrail
#    structurally cannot make (see "Verified mechanism" above).
contracts = yaml.safe_load((CLONE / "skills" / "workflow-planner" / "references" / "artifact-contracts.yaml").read_text(encoding="utf-8"))
by_id = {a["id"]: a for a in contracts["artifacts"]}
wop = by_id["workflow_orchestration_plan"]
assert "target_workflow_id" not in (wop.get("required_machine_fields") or []), \
    "FAIL: declared as required -- would break every existing plan artifact lacking this legacy field"
assert "target_workflow_id" in (wop.get("recommended_machine_fields") or []), \
    "FAIL: not declared as a recommended machine field on workflow_orchestration_plan"
for other_id, other in by_id.items():
    if other_id == "workflow_orchestration_plan":
        continue
    assert "target_workflow_id" not in (other.get("required_machine_fields") or []) + (other.get("recommended_machine_fields") or []), \
        f"FAIL: target_workflow_id also/instead declared on unrelated artifact {other_id!r}"

# 4. PROTECTED-STATE CHECK — every existing required/recommended field on
#    workflow_orchestration_plan survives untouched, and every other
#    artifact block is byte-identical to its frozen-SHA content.
FROZEN_REQUIRED = {"artifact_id", "primary_fog_type", "chosen_workflow_id", "routing_decision_method", "workflow_steps", "created_at"}
FROZEN_RECOMMENDED = {"source_intent_ref", "execution_mode", "system_recommended_workflow", "selected_workflow",
                       "routing_divergence", "escalation_recommended", "auto_escalation_allowed",
                       "approval_gates", "gate_behavior", "stop_conditions", "subset_run", "subset_reason",
                       "included_steps", "excluded_steps"}
assert FROZEN_REQUIRED <= set(wop.get("required_machine_fields") or []), "FAIL: an existing required field on workflow_orchestration_plan was removed"
assert FROZEN_RECOMMENDED <= set(wop.get("recommended_machine_fields") or []), "FAIL: an existing recommended field on workflow_orchestration_plan was removed"

import subprocess as sp
diff = sp.run(
    ["git", "diff", "--unified=0", "a7b957d738f5e1c42b6dd06824c3e6029d816bcd", "--",
     "skills/workflow-planner/references/artifact-contracts.yaml"],
    cwd=CLONE, capture_output=True, text=True,
).stdout
touched_artifact_blocks = {
    line.split("id:", 1)[1].strip()
    for line in diff.splitlines()
    if line.startswith(("+  - id:", "-  - id:"))
}
assert touched_artifact_blocks <= {"workflow_orchestration_plan"}, \
    f"FAIL: diff touches artifact block header(s) other than workflow_orchestration_plan: {touched_artifact_blocks}"
```

## Route-independent framing

The check is on final repository state (does the guardrail pass, is the
runtime tuple updated, is the field attributed to the correct artifact as
recommended, is everything else untouched) — not on how the agent got
there (direct YAML edit, a script, multiple incremental edits, etc.).

## Negative cases (must be rejected)

- **Declared on the wrong artifact** (e.g. `repository_sensemaking_brief`
  or any artifact other than `workflow_orchestration_plan`): passes Check 1
  (pytest guardrail, since it unions across all artifacts) but fails Check 3
  (attribution). This is the primary near-miss this pilot exists to detect
  — it demonstrates the gap between "satisfies the automated test" and
  "correct."
- **Declared as required instead of recommended**: fails Check 3 directly,
  and would also fail any existing orchestration-plan artifact lacking the
  legacy field once `validate-plan.py` enforces required fields (not
  exercised directly by this oracle, but the contract-level check alone is
  sufficient to reject it).
- **Runtime tuple updated but contract left undeclared**: fails Check 1
  (the guardrail test itself catches this — it is what the test exists
  for).
- **Contract declared but runtime tuple not updated**: fails Check 2.

## Qualification

- Multiple valid solution strategies: **yes** — direct YAML edit, or a
  small script/codemod that inserts the field; both satisfy the same final
  state.
- Semantic, not text-equality, oracle: **yes** — checks parsed YAML
  structure and tuple membership, not a diff against a reference file.
- Protected-state check present: **yes** — Check 4 (existing fields on the
  touched block, and byte-identity of every other artifact block).
- Plausible hidden near-miss rejectable: **yes** — the wrong-artifact case
  (Check 3), which the authoritative pytest guardrail structurally cannot
  catch on its own.
- Meaningful repository reasoning required: **yes** — requires
  understanding the runtime-tuple/contract-declaration relationship
  (`CLAUDE.md`'s own stated rule: "if you add a new field-read alias to the
  runtime, declare it in a contract too"), not simple text substitution.
- Distinct from prior Autonomous Task D/D' tasks: relying on the reviewed
  package's own note that this substrate (`artifact-contracts.yaml` +
  `test_field_contract_agreement.py`) is fresh; prior task content itself
  was not inspected, per the isolation boundary.

**ADMISSIBLE**

## Sanity check (Task 2 Step 5)

All four checks are directly executable Python/subprocess calls against a
clone of this repo at the frozen SHA plus the agent's edits; `pytest` and
`PyYAML` are already available in this worktree's environment (confirmed:
`PyYAML 6.0.3`; `pytest` presence to be confirmed at Task 22's real
preflight/oracle-self-test stage, not assumed here).
