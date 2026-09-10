# Phase 10 Episode 3 — ViralFactory production-activation pre-mortem

## Context and assumptions

Target: `ThorStarlord/ViralFactory@2cb5d4358b9a2d10b828ceda481de7f43de2d0eb`.

The repository handoff says the three-package factory chain is repository-qualified, but production activation remains unproven until target-environment migrations, configuration, a durable staging smoke, deployed `/factory` verification, and product/platform approval are evidenced. The canonical factory contract separately records that marketplace-specific live adapters and a live LLM provider are not yet canonical/live.

This analysis stress-tests **production activation of the existing qualified factory chain**. It does not authorize live scraping, provider adoption, publishing, migration application, credential changes, or production rollout.

## Tigers

### RISK-1 — Target environment may not satisfy the repository-qualified contracts

**Evidence status:** observed evidence gap.  
**Urgency:** launch-blocking.  
**Impact:** high.  
**Probability:** unknown.

The repository can establish the code/contracts and deterministic qualification, but it cannot establish from GitHub state alone that the target Supabase migrations are applied, service configuration is correct, real MoviePy/FFmpeg rendering persists a valid artifact, or the deployed authenticated `/factory` projection shows the durable lifecycle.

**Mitigation:** execute the existing production-activation runbook in staging and preserve environment evidence before production activation.  
**Owner role:** operator / deployment owner.  
**Success criterion:** all five activation evidence gates in `STATUS.md` have preserved target-environment evidence with no unexplained contract mismatch.  
**Escalation signal:** migration/configuration mismatch, failed durable render/storage path, or deployed dashboard state diverges from persisted lifecycle.

## Paper tigers

### RISK-2 — Repository-wide raw TypeScript errors automatically invalidate the factory activation

**Evidence status:** observed, but bounded by existing qualification evidence.  
**Urgency:** track.  
**Impact:** medium.  
**Probability:** low for the already-qualified factory surface, unknown for unrelated surfaces.

The handoff records pre-existing raw `tsc --noEmit` errors in `CampaignPage`, `CampaignPage.test.tsx`, and `storageMedia.test.ts`, while the Package 3 scoped TypeScript qualification, Vite production build, frontend tests, and factory/dashboard CI passed on the exact candidate. That evidence does not make repository-wide type debt harmless, but it does not support treating those existing errors as a demonstrated factory-activation blocker.

**Mitigation:** keep the debt as a separately bounded package; if target-environment smoke implicates those surfaces, reclassify based on observed failure.  
**Owner role:** frontend engineering.  
**Success criterion:** factory activation evidence remains green without suppressing or misrepresenting the repository-wide debt.  
**Escalation signal:** target smoke or build/runtime evidence links a listed type error to the factory activation path.

## Elephants

### RISK-3 — Expanding to a live marketplace adapter or live model provider before activation evidence obscures the source of failures

**Evidence status:** hypothetical.  
**Urgency:** investigate.  
**Impact:** high.  
**Probability:** unknown.

The current architecture intentionally keeps live source acquisition and live model-provider execution outside the completed repository-qualified slice. Introducing either before proving the existing chain in a target environment could add source/provider variables while the deployment contract itself remains unverified.

**Mitigation:** preserve the current sequencing: production activation/observability first, then one bounded live source adapter, then one bounded live structured critique provider.  
**Owner role:** product + engineering.  
**Success criterion:** existing chain has target-environment evidence before a separately authorized live-integration package begins.  
**Escalation signal:** pressure to add provider/source integration is used as a substitute for resolving missing activation evidence.

## Mitigations and monitoring

1. Apply the three factory migrations to the intended staging environment in documented order.
2. Verify service-side Supabase configuration and render bucket configuration.
3. Run one durable staging Deal -> Critique -> RenderJob -> RenderArtifact execution with the real renderer and Storage persistence.
4. Authenticate into the deployed SaaS and verify `/factory` against persisted success plus at least one non-success state.
5. Preserve activation evidence separately from later live-source/provider qualification.
6. Keep repository-wide TypeScript debt visible but do not silently expand the activation package to repair unrelated files.

## Recommendation

**`insufficient_evidence` for production activation.**

The repository-side factory milestone is qualified; the missing information is target-environment evidence. The next action should be evidence collection through the existing activation runbook, not speculative repository expansion.

This recommendation is analysis only. It grants no authority to modify Supabase, deploy, scrape marketplaces, call a live model provider, or publish content.

## Machine-readable handoff

```yaml
artifact_id: risk_analysis
schema_version: "1"
source_artifact_ref: "ThorStarlord/ViralFactory@2cb5d4358b9a2d10b828ceda481de7f43de2d0eb:STATUS.md"
risks:
  - id: RISK-1
    class: tiger
    statement: "Target environment may not satisfy the repository-qualified factory contracts."
    evidence_status: observed
    evidence_refs:
      - "STATUS.md@2cb5d4358b9a2d10b828ceda481de7f43de2d0eb"
      - "docs/architecture/FACTORY-PIPELINE-CONTRACT.md@2cb5d4358b9a2d10b828ceda481de7f43de2d0eb"
    urgency: launch_blocking
    impact: high
    probability: unknown
    mitigation: "Run the documented staging activation checks and preserve target-environment evidence before production activation."
    owner_role: "operator / deployment owner"
    success_criterion: "All documented activation gates have preserved target-environment evidence with no unexplained contract mismatch."
    escalation_signal: "Migration/configuration mismatch, failed durable render/storage path, or deployed dashboard state diverges from persisted lifecycle."
  - id: RISK-2
    class: paper_tiger
    statement: "Repository-wide raw TypeScript errors automatically invalidate the already-qualified factory surface."
    evidence_status: observed
    evidence_refs:
      - "STATUS.md@2cb5d4358b9a2d10b828ceda481de7f43de2d0eb"
    urgency: track
    impact: medium
    probability: low
    mitigation: "Keep the debt separately bounded and reclassify only if target evidence links it to the factory activation path."
    owner_role: "frontend engineering"
    success_criterion: "Activation evidence remains green without hiding repository-wide type debt."
    escalation_signal: "Target smoke or runtime evidence links the listed type errors to the factory path."
  - id: RISK-3
    class: elephant
    statement: "Adding a live source adapter or live model provider before activation evidence may obscure the source of failures."
    evidence_status: hypothetical
    evidence_refs:
      - "STATUS.md@2cb5d4358b9a2d10b828ceda481de7f43de2d0eb"
      - "docs/architecture/FACTORY-PIPELINE-CONTRACT.md@2cb5d4358b9a2d10b828ceda481de7f43de2d0eb"
    urgency: investigate
    impact: high
    probability: unknown
    mitigation: "Preserve activation-first sequencing before separately authorized live integration work."
    owner_role: "product + engineering"
    success_criterion: "Target-environment activation evidence exists before live integration expansion begins."
    escalation_signal: "Live integration is proposed as a substitute for resolving missing activation evidence."
recommendation: insufficient_evidence
conditions:
  - "Apply and verify factory migrations in the target staging environment."
  - "Complete a durable real-renderer staging smoke with persisted artifact evidence."
  - "Verify the deployed authenticated /factory lifecycle projection."
unresolved_questions:
  - "Are the documented migrations already applied in the intended target environment?"
  - "Does the deployed environment reproduce the repository-qualified durable lifecycle with real renderer and Storage dependencies?"
  - "Does any pre-existing repository-wide TypeScript debt affect the deployed factory path in practice?"
```
