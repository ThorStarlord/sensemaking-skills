# Repository Sensemaking Brief — Sensemaking Skills (fresh repeated-use run 2026-08-14)

## 1. Repository goal

Sensemaking Skills is a pre-implementation intelligence system: fog
classification and repository diagnosis (repo-sensemaker) producing an
evidence-grounded, human-reviewed Repository Sensemaking Brief is the
ratified product core (ADR 0014). Agent-native execution is primary (ADR
0013); deterministic scripts/validators are support machinery. Routing to
downstream implementation workflows is deferred, not ratified (ADR 0014;
ADR 0018 PROPOSED). The active coding agent's end-to-end operating model is
documented in docs/agent-native-operating-workflow.md (Workflow v0).

## 2. Current shape

HEAD: `a6239630` (main). Version 0.2.2 (STATUS.md:3). Working tree carries
pre-existing local contamination (modified src/sensemaking_skills.egg-info/
PKG-INFO + SOURCES.txt, modified .claude/settings.json, untracked auteur
dogfood artifacts + untracked evidence 0016) — committed state is clean of
these. CONTEXT.md was reconciled to the agent-native architecture
(evidence 0021 CLOSED; stale-claim scan empty at a6239630).

## 3. Strong signals

- Ratified core (brief production) is implemented, validated, and stable
  (repo-sensemaker + probe engine + validate-brief.py; ADR 0014).
- Agent-native execution ratified (ADR 0013); the retired runner is gone;
  CLI default plan_only is coherent.
- Workflow v0 (docs/agent-native-operating-workflow.md) is committed and
  was exercised repeatedly on real tasks (evidence 0021, the Auteur
  release-evidence campaign).

## 4. Missing pieces

- Four documentation surfaces deferred by the runner-retirement
  reconciliation were never completed: ROUTING_GUIDE, run-ledger-guide,
  PORTFOLIO_OPERATIONS, PRODUCT-CONTRACT-REVIEW (retirement plan,
  docs/2026-08-programmatic-runner-retirement-plan.md:133-135, "Deferred to
  a follow-up pass ... verify incidental references individually").
- roadmap.md still presents "Current Version: 0.2.1 (Beta)" and "Phase 2.3
  Complete" with a Phase 3 real-world-CLI-testing plan, while STATUS.md
  (2026-08-10) reports 0.2.2 and a completed docs reconciliation.

## 5. Improvement opportunities

- Complete the deferred docs verification (small, bounded).
- Align roadmap.md with STATUS.md version/phase claims.
- Decide (owner) how the retained-but-unratified routing surface maps into
  v1 scope.

## 6. Weakest boundary

**Weakness type:** Vocabulary Drift

The main CONTEXT.md drift is closed (evidence 0021 CLOSED at a6239630), but
the same documentation-currency responsibility remains live on a smaller
surface: roadmap.md claims "Current Version: 0.2.1 (Beta)" and "Phase 2.3
Complete" (roadmap.md:3, roadmap.md current-version line) against STATUS.md
v0.2.2 (STATUS.md:3), and four runner-era documents were explicitly
deferred by the retirement reconciliation and never verified
(docs/2026-08-programmatic-runner-retirement-plan.md:133-135). Separately,
the committed surface (workflow-registry.yaml auto-invoke entries, four
implementation workflows, retained deterministic runtime) is substantially
larger than the ratified core (brief production, ADR 0014), and no
consolidated v1-scope decision records how that surface is resolved.

Logic trace: CONTEXT.md (the agent first-read) was the demonstrated defect
and is repaired; the same drift class persists on the deferred docs and
roadmap (demonstrated currency mismatches), and the ratified-vs-committed
surface gap is a documented architectural fact (ADR 0014 vs
workflow-registry.yaml) that only the owner can scope. Therefore the
consequential boundary is the residual documentation-currency drift on the
deferred subset, with the v1-scope question as the owner-intent dependency.

## 7. Why it matters

The next meaningful Sensemaking decision is the v1 scope call. That decision
needs (a) accurate current-state docs (roadmap/STATUS agree) and (b) a
decision on the deferred + unratified surface. The residual drift is small
and bounded; the scope question is large and owner-owned.

## 8. Evidence

- STATUS.md:3 (version 0.2.2, 2026-08-10).
- roadmap.md:3 ("Phase 2.3 Complete"; current-version claim 0.2.1 Beta).
- docs/2026-08-programmatic-runner-retirement-plan.md:133-135 (deferred:
  ROUTING_GUIDE, run-ledger-guide, PORTFOLIO_OPERATIONS,
  PRODUCT-CONTRACT-REVIEW).
- docs/adr/0014 (ratified core = brief production; routing deferred);
  docs/adr/0018 (PROPOSED).
- skills/workflow-planner/references/workflow-registry.yaml
  (auto_invoke_next_workflow entries; ui/product/docs/implementation-
  workflow ids) — retained unratified surface.
- experiments/evidence/0021 (CONTEXT.md finding CLOSED).

## 9. Recommended next step

Bounded docs reconciliation of the deferred subset + roadmap alignment
(sensemaking-docs-reconciler responsibility), separately from the owner's
v1-scope decision. Not implemented by this campaign.

## 10. Ready-to-copy prompt

Reconcile roadmap.md and the four retirement-deferred docs to current
agent-native state; flag any incidental runner-era claims found.

## 11. Candidate next steps

- Verify the four deferred docs for runner-era claims (retirement plan
  follow-up).
- Align roadmap.md version/phase with STATUS.md.
- Owner: draft the v1 scope decision covering the retained routing surface.

## 12. Evidence rules

- State-currency: all claims from direct reads at a6239630 (2026-08-14);
  no probe re-run this run.

## 13. Machine-readable handoff

```yaml
artifact_id: repository_sensemaking_brief
schema_version: 1
primary_fog_type: docs_fog
weakness_type: Vocabulary Drift
weakness_type_explanation: residual documentation-currency drift on retirement-deferred docs and roadmap; CONTEXT.md itself closed
recommended_workflow_id: docs-contract-reconciliation
recommended_execution_mode: plan_only
escalation_recommended: false
evidence:
  - STATUS.md:3
  - roadmap.md:3
  - docs/2026-08-programmatic-runner-retirement-plan.md:133-135
  - docs/adr/0014; docs/adr/0018 (PROPOSED)
  - skills/workflow-planner/references/workflow-registry.yaml
  - experiments/evidence/0021 (CLOSED)
created_at: 2026-08-14T00:00:00Z
immutable: true
```

## 15. Extended analysis

- uncertainty: source owner_intent, detail "v1 scope of the retained routing surface is owner-owned; deferred-docs currency is repository_evidence"
- owner_intent_state: status thin, known "ADR 0014 ratified core; routing deferred pending external proof"
