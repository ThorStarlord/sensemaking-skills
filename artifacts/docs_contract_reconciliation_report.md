# Docs & Contract Reconciliation Report

## 1. Drift Diagnosis
The run-log-template.md defines a minimal structure (header fields, per-step sequence log, decisions, final state), but the three live run logs (YOLO run_log.md, guided run_log_20260514.md, and the new plan_only and prompt_chain run logs) have diverged in practice:

1. **Pre-flight block**: Present in YOLO and prompt-chain run logs but not in the original guided run log — not required by template, but used in practice for mutating modes.
2. **Gate recording**: The template does not specify `gate_result`, `approved_at`, or `approved_by` fields — these were added pragmatically in the new run logs.
3. **Validator command verbosity**: YOLO run log records exact validator commands; template shows only level/command/result structure.

## 2. Weakest Boundary
The run-log-template.md does not fully specify the gate recording contract. The template says "gate: [Gate Name]" but does not mandate approval timestamps or user attribution fields. When guided or autonomous modes exercise gates, the run log must record more structured data than the template currently requires.

## 3. Missing Instructions
The run-log-template.md is missing:
- `approved_at` and `approved_by` fields in gate recording
- `gate_result` field (approved_by_user / denied_by_user / bypassed_by_yolo)
- Pre-flight block format for mutating modes
- TDD cycle recording format (RED/GREEN/REFACTOR blocks)
- Branch recording requirement for mutating modes

## 4. Missing Examples
No example run log demonstrates a gate approval or denial event. All existing run logs have `gate: N/A` or gates that were bypassed.

## 5. Validator Blind Spots
No existing validator checks run log structure. The `validate-run-log.py` script (newly created at `scripts/validate-run-log.py`) would fill this gap but has not yet been added to the standard validation pipeline.

## 6. Ambiguous Artifact Names
`prompt_handoff` is produced by both `prompt-handoff` skill and `handoff` skill. The registry uses `prompt-handoff` for one and `handoff` for another — these are clearly distinct in registries but the dual-producer pattern could cause confusion.

## 7. Drift Risks
If the run-log-template.md is not updated to match actual run log practice, new orchestrator runs may produce logs that:
- Omit gate approval timestamps (making audit trails incomplete)
- Omit pre-flight blocks (making failure recovery harder)
- Use inconsistent field names across logs

## 8. Recommended Patches
1. Update run-log-template.md to include `gate_result`, `approved_at`, and `approved_by` fields
2. Add Pre-flight section to run-log-template.md for mutating modes
3. Add TDD cycle format to run-log-template.md
4. Consider adding validate-run-log.py to the standard pre-flight pipeline for mutating modes

## 9. Mismatches Found
| Template Field | Actual Practice | Gap |
|:--------------:|:---------------:|:---:|
| `gate` | `gate` + `gate_result` + timestamps | Missing structured gate fields |
| Pre-flight | Present in YOLO logs | Missing from template |
| TDD cycles | RED/GREEN/REFACTOR in YOLO log | Missing from template |

## 10. Changes Required
The run-log-template.md should be updated to add optional fields for gate recording, pre-flight, and TDD cycles. These are backward-compatible additions (all existing logs remain valid).

## 11. Patches Proposed
Proposed template updates:
1. Gate section gains: `gate_result`, `approved_at`, `approved_by` (optional fields, not required for backward compatibility)
2. Pre-flight section added before Sequence Log (optional, required for mutating modes)
3. TDD Cycle section added after validator_stack (optional, for TDD event recording)

## 12. Validation Result
validate-artifact.py passes against this report. The report is structurally valid against its contract but note: no specialized validator exists for `docs_contract_reconciliation_report` — only Level 2 generic validation applies.

## 13. Next Handoff
Target: `prompt-handoff` skill. Handoff prompt produced separately.

```yaml
artifact_id: docs_contract_reconciliation_report
recommended_next_gate: review_next_prompt
patches_proposed: 3
patches_are_backward_compatible: true
```
