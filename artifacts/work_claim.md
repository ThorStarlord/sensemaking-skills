# Work Claim — Domain Alignment Report Run 1

## source
- **source**: `artifacts/domain_alignment_report.md` (commit `5a77885`, 186 lines, produced by `docs-aligner` gate:none)
- **producer**: docs-aligner autonomous run 2026-09-01
- **consumer**: reconciliation lane (this work_claim is the audited artifact for output-reconciler)
- **baseline**: `main` at `dc7ebe3` (pre-run) → `5a77885` (post-run) with `CONTEXT.md` mutations

## claims
1. **C1**: `CONTEXT.md` source-of-truth table contained phantom `skill-registry.yaml` path contradicting repository reality at `skills/workflow-planner/references/skill-registry.yaml`
2. **C2**: `docs/canonical-vocabulary.yaml` and `src/sensemaking_skills/defaults/canonical-vocabulary.yaml` are load-bearing drift (5 gates, 5 artifact_ids, yolo compatibility flags) with package runtime loading stale copy
3. **C3**: 44 skill-registry entries include `triage` (proposed) and `tdd` (deprecated) yet 7 workflows sequence `triage->tdd` while `CONTEXT.md` lists 8 representative operational Skills
4. **C4**: `docs/canonical-vocabulary.yaml:418-419` marks `yolo_execution` compatibility-only yet `src/sensemaking_skills/runner.py:72,337` defaults to `yolo_execution` and workflows allow it
5. **C5**: `MODEL_WARRANT` / `representation_sufficiency` not consulted outside `src/sensemaking_skills/reasoning/`; `registry.py:131-169` and `runner.py:208-289` never consult warrant
6. **C6**: `artifact-contracts.yaml:484-490` requires `primary_fog_type`/`workflow_steps`/`created_at` contradicting ADR 0025 provisional skeleton that may omit them and `workflow-runtime.py:2564-2568` pre-brief path
7. **F1-F5**: 5 fuzzy-language clusters (workflow, validation/reconciliation/verification, responsibility/Skill/workflow/capability, probe/evidence, gate/approval/mode) require sharpening
8. **U1-U6**: 6 undocumented concepts (MODEL_WARRANT, Representation Sufficiency, NO_REPOSITORY_CHANGE_WARRANTED, State-Currency Probe, Gate/Execution Mode, Weakness Type) missing from CONTEXT glossary
9. **Summary**: 6 contradictions, 5 fuzzy terms sharpened, 6 undocumented concepts, 0 ADRs, 7 glossary entries added +5 updated +1 path fix; artifact validates PASS via `validate-artifact.py`

## machine-readable handoff
```yaml
artifact_id: work_claim
source: artifacts/domain_alignment_report.md
claims:
  - "C1 phantom skill-registry path"
  - "C2 canonical/package vocabulary drift"
  - "C3 ghost/deprecated workflow consumers"
  - "C4 yolo_execution compatibility vs default"
  - "C5 MODEL_WARRANT not wired"
  - "C6 workflow plan REQUIRED vs provisional"
  - "F1-F5 fuzzy language sharpening"
  - "U1-U6 undocumented concepts"
  - "Summary counts and PASS"
created_at: 2026-09-01T00:00:00Z
immutable: true
```
