# Reconciliation Report — Domain Alignment Report Run 1

## claims
- **claim**: C1 phantom skill-registry path — CONTEXT.md source-of-truth listed root skill-registry.yaml vs actual skills/workflow-planner/references/skill-registry.yaml
  - **classification**: verified
  - **artifact**: CONTEXT.md:319 (pre-fix) vs skills/workflow-planner/references/skill-registry.yaml:1, src/sensemaking_skills/config.py:32, git diff 5a77885
  - **disposition**: fixed
- **claim**: C2 canonical/package vocabulary drift — 5 gates, 5 artifact_ids, yolo flags differ; validators load package copy
  - **classification**: verified
  - **artifact**: docs/canonical-vocabulary.yaml:150-419,421-661 vs src/sensemaking_skills/defaults/canonical-vocabulary.yaml:360-386 vs src/sensemaking_skills/validation.py:44
  - **disposition**: deferred — ownership ratified (docs/canonical-vocabulary.yaml authored canonical, package mirror generated, semantic-equivalence test; no generator this session; record as deferred, not filed)
- **claim**: C3 ghost/deprecated workflow consumers — 44 entries vs CONTEXT 8 representatives; triage proposed/tdd deprecated but workflows sequence them
  - **classification**: disputed as framed
  - **artifact**: skills/workflow-planner/references/skill-registry.yaml:80-93 (status: proposed/deprecated), CONTEXT.md:126-134 (representative list, not exhaustive), skills/workflow-planner/references/workflow-registry.yaml:665-721 (implementation-workflow et al)
  - **disposition**: deferred — reframe as workflow executability/compatibility-liveness drift; underlying concern verified, contradiction framing disputed; file follow-up issue
- **claim**: C4 yolo_execution compatibility vs default — canonical marks compatibility-only yet runner.py defaults to yolo_execution
  - **classification**: verified as compatibility/default-policy tension
  - **artifact**: docs/canonical-vocabulary.yaml:418-419 vs src/sensemaking_skills/runner.py:72,337 vs workflow-registry.yaml:496,569
  - **disposition**: deferred — UNRESOLVED_COMPATIBILITY_DEFAULT_TENSION per owner decision; no runtime change authorized this session; preserve for consumer analysis
- **claim**: C5 MODEL_WARRANT not wired — implementation only in reasoning/, registry/runner never consult warrant
  - **classification**: disputed
  - **artifact**: scripts/workflow-runtime.py _run_seam_warrant() post-Brief invocation (contrary evidence), src/sensemaking_skills/reasoning/warrant_gate.py:76-89 vs incomplete search src/sensemaking_skills/*.py excluding scripts/, tests/test_*warrant*
  - **disposition**: deferred — correct to "warrant seam exists but opt-in (warrant_enabled false by default)"; add negative-evidence regression fixture; no repair this session
- **claim**: C6 workflow plan REQUIRED vs provisional — artifact-contracts requires fields contradicting ADR 0025 provisional lifecycle
  - **classification**: disputed
  - **artifact**: docs/adr/0025-workflow-orchestration-plan-lifecycle.md:86-113 (Accepted two-stage lifecycle), skills/workflow-planner/references/artifact-contracts.yaml:484-514 note provisional may omit, scripts/workflow-runtime.py:2564-2568 provisional generation
  - **disposition**: deferred — previously adjudicated intentional lifecycle (Issue #232 closed); remove from contradiction count; use as positive authority regression fixture
- **claim**: F1-F5 fuzzy language sharpening — 5 clusters need qualified canonical terms
  - **classification**: verified with revision
  - **artifact**: CONTEXT.md:142-144,223-242,328-336 vs docs-aligner report §3
  - **disposition**: deferred — F1 qualified usage guidance not new ontology; F2 largely already canonical; F3 revise to preserve capability as distinct (Skill capability write_files); F4 prefer Probe/Observation/Evidence; F5 split terminology vs real default-mode contradiction (promote to §2 if confirmed)
- **claim**: U1-U6 undocumented concepts — 6 concepts missing from CONTEXT glossary
  - **classification**: disputed as "undocumented"
  - **artifact**: CONTEXT.md:165-177 (MODEL_WARRANT addendum already documents), skills/repo-sensemaker/references/weakness-types.md, docs/canonical-vocabulary.yaml:149-419, artifact-contracts.yaml:150-157
  - **disposition**: deferred — recharacterize as CONTEXT glossary gaps (concepts documented elsewhere, absent from glossary subsection); preserve original report as evidence

## findings
- **concept**: vocabulary drift — canonical vs packaged
  - **finding_type**: claim_verified
  - **observations**:
    - source: docs/canonical-vocabulary.yaml
      location: docs/canonical-vocabulary.yaml:418-419
      value: yolo_execution compatibility_only:true + status_note
      evidence: missing in src/sensemaking_skills/defaults/canonical-vocabulary.yaml:360-386
    - source: src/sensemaking_skills/validation.py
      location: src/sensemaking_skills/validation.py:44
      value: loads package defaults
      evidence: package consumers reason over stale semantics
  - **confidence**: high
  - **requires_semantic_review**: true
  - **notes**: Load-bearing drift — runtime validates different semantic world than canonical docs. Ownership now ratified: docs/canonical-vocabulary.yaml authored source, package mirror generated, semantic-equivalence test. Implementation deferred.
- **concept**: phantom path
  - **finding_type**: claim_verified
  - **observations**:
    - source: CONTEXT.md
      location: CONTEXT.md:319
      value: skill-registry.yaml
      evidence: Test-Path skill-registry.yaml => False; actual at skills/workflow-planner/references/skill-registry.yaml:1
  - **confidence**: high
  - **requires_semantic_review**: false
  - **notes**: Fixed in 5a77885. Guard already exists (path-drift tests); extend rather than new CI concept per Harden Only Where Pressured.
- **concept**: ghost Skills framing
  - **finding_type**: claim_disputed
  - **observations**:
    - source: skills/workflow-planner/references/skill-registry.yaml
      location: skill-registry.yaml:80-93
      value: triage status:proposed, tdd status:deprecated
      evidence: CONTEXT.md lists representative Skills, not exhaustive claim
    - source: skills/workflow-planner/references/workflow-registry.yaml
      location: workflow-registry.yaml:665-721
      value: implementation-workflow sequences triage->tdd
      evidence: workflows appear executable but Steps not executable
  - **confidence**: high
  - **requires_semantic_review**: true
  - **notes**: Real issue is workflow executability/compatibility-liveness, not CONTEXT taxonomy defect. Reframe and file follow-up.
- **concept**: yolo_execution default tension
  - **finding_type**: claim_verified
  - **observations**:
    - source: docs/canonical-vocabulary.yaml
      location: docs/canonical-vocabulary.yaml:418-419
      value: compatibility_only:true
      evidence: runner.py:72 defaults to yolo_execution
  - **confidence**: high
  - **requires_semantic_review**: true
  - **notes**: Compatibility presence != ratified policy (ADR 0026 pattern). Tension is legacy API default, not mere existence. Leave UNRESOLVED, requires consumer analysis before changing default.
- **concept**: MODEL_WARRANT absence assertion
  - **finding_type**: claim_contradicted
  - **observations**:
    - source: scripts/workflow-runtime.py
      location: scripts/workflow-runtime.py:_run_seam_warrant
      value: warrant seam invoked post-Brief
      evidence: runtime does consult warrant; report searched only src/sensemaking_skills/*.py
    - source: artifacts/domain_alignment_report.md
      location: report.md:41
      value: grep src/sensemaking_skills/*.py excluding reasoning/
      evidence: search scope did not cover scripts/workflow-runtime.py named in claim
  - **confidence**: high
  - **requires_semantic_review**: false
  - **notes**: Incomplete absence search. Correct to opt-in status (warrant_enabled false by default). Use as negative-evidence regression.
- **concept**: workflow plan lifecycle
  - **finding_type**: claim_contradicted
  - **observations**:
    - source: docs/adr/0025-workflow-orchestration-plan-lifecycle.md
      location: ADR 0025:86-113
      value: Accepted two-stage lifecycle provisional vs finalized
      evidence: Issue #232 closed as completed
    - source: skills/workflow-planner/references/artifact-contracts.yaml
      location: artifact-contracts.yaml:514
      value: note provisional may omit primary_fog_type/workflow_steps/created_at
      evidence: exception documented beside apparent requirement
  - **confidence**: high
  - **requires_semantic_review**: false
  - **notes**: Previously adjudicated intentional distinction, not contradiction. Report proposed weakening would violate prior owner decision. Use as positive authority regression.
- **concept**: docs-aligner authority handling
  - **finding_type**: claim_omitted
  - **observations**:
    - source: skills/docs-aligner/SKILL.md
      location: SKILL.md:10
      value: gate:none only when downstream review_alignment_report gate present
      evidence: autonomous CONTEXT.md mutation performed without mechanical downstream gate in this run
    - source: skills/docs-aligner/SKILL.md
      location: SKILL.md:6
      value: generic docs-aligner vs sensemaking-docs-reconciler
      evidence: report treated compatibility/historical/proposed status as contradictions without currentness check
  - **confidence**: medium
  - **requires_semantic_review**: true
  - **notes**: Skill lacked authority/currentness/prior-adjudication classification. Harden with narrow pre-classification (Hybrid C): confirmed_contradiction / intentional_divergence / previously_adjudicated / needs_adjudication + negative-evidence rule. Keep deep adjudication in sensemaking-docs-reconciler.

## recommendations
- **issue**: Ratify and enforce canonical vocabulary ownership — docs/canonical-vocabulary.yaml authored source, src/.../defaults mirror generated via deterministic command, CI semantic-equivalence test (not hand-edited mirror)
  - **target**: docs/canonical-vocabulary.yaml + src/sensemaking_skills/defaults/ + CI
- **issue**: Reframe and file workflow executability drift — audit workflow-registry workflows referencing proposed/deprecated Skills (triage->tdd) as compatibility-liveness, not CONTEXT taxonomy defect
  - **target**: skills/workflow-planner/references/workflow-registry.yaml + skill-registry.yaml
- **issue**: Harden docs-aligner with authority/currentness pre-classification + negative-evidence rule and add regression fixtures (C5 incomplete-search, C6 prior-adjudication); preserve Run 1 as evidence, rerun after hardening for comparison
  - **target**: skills/docs-aligner/SKILL.md + tests/
- **issue**: Preserve yolo_execution compatibility/default tension as unresolved — conduct bounded consumer analysis (who calls run_workflow without mode, breaking change, migration path) before changing default
  - **target**: src/sensemaking_skills/runner.py + workflow-registry.yaml
- **issue**: Fix docs-aligner report Markdown table escaping (pipe in NO | PARTIAL | INCONCLUSIVE splits table rows)
  - **target**: artifacts/domain_alignment_report.md §6 + validator Markdown table check

## machine-readable handoff
```yaml
artifact_id: reconciliation_report
schema_version: 1
source_claim_ref: artifacts/work_claim.md
claims:
  - claim: C1 phantom skill-registry path
    classification: verified
    artifact: CONTEXT.md:319 and skills/workflow-planner/references/skill-registry.yaml:1
    disposition: fixed
  - claim: C2 canonical/package vocabulary drift
    classification: verified
    artifact: docs/canonical-vocabulary.yaml vs src/sensemaking_skills/defaults/canonical-vocabulary.yaml
    disposition: deferred
  - claim: C3 ghost/deprecated workflow consumers
    classification: disputed
    artifact: skill-registry.yaml:80-93 vs workflow-registry.yaml:665-721
    disposition: filed
  - claim: C4 yolo_execution compatibility vs default
    classification: verified
    artifact: docs/canonical-vocabulary.yaml:418-419 vs runner.py:72
    disposition: deferred
  - claim: C5 MODEL_WARRANT not wired
    classification: disputed
    artifact: scripts/workflow-runtime.py _run_seam_warrant vs incomplete search
    disposition: deferred
  - claim: C6 workflow plan REQUIRED vs provisional
    classification: disputed
    artifact: ADR 0025 vs artifact-contracts.yaml:514
    disposition: deferred
  - claim: F1-F5 fuzzy language sharpening
    classification: verified
    artifact: CONTEXT.md domain language vs report §3
    disposition: deferred
  - claim: U1-U6 undocumented concepts
    classification: disputed
    artifact: CONTEXT.md:165-177 and repo-sensemaker docs vs glossary subsection
    disposition: deferred
findings:
  - concept: vocabulary drift
    finding_type: claim_verified
    observations:
      - source: docs/canonical-vocabulary.yaml
        location: docs/canonical-vocabulary.yaml:418-419
        value: canonical yolo compatibility flag
        evidence: absent in package mirror
    confidence: high
    requires_semantic_review: true
    notes: ownership ratified, implementation deferred
  - concept: workflow plan lifecycle
    finding_type: claim_contradicted
    observations:
      - source: docs/adr/0025-workflow-orchestration-plan-lifecycle.md
        location: ADR 0025:86-113
        value: provisional vs finalized intentional
        evidence: previously adjudicated Issue #232
    confidence: high
    requires_semantic_review: false
    notes: use as positive regression
recommendations:
  - issue: enforce canonical vocabulary ownership and generated mirror
    target: docs/canonical-vocabulary.yaml
  - issue: harden docs-aligner authority classification + fixtures
    target: skills/docs-aligner
  - issue: preserve yolo default tension as unresolved
    target: src/sensemaking_skills/runner.py
created_at: 2026-09-01T00:00:00Z
immutable: true
```
