# Phase 10 Episode 3 — ViralFactory / Product Management pre-mortem

**Source capability:** `pre-mortem`  
**Target:** `ThorStarlord/ViralFactory@2cb5d4358b9a2d10b828ceda481de7f43de2d0eb`  
**Canonical episode artifact:** `episode-3-viralfactory-risk-analysis.md`  
**Companion profile:** `episode-3-viralfactory-profile.yaml`

## Episode result

This episode deliberately compares the common semantic profile against a mature domain artifact rather than against handoff prose alone.

The PM `risk_analysis` contract already represents:

- risk evidence status;
- evidence references;
- observed versus hypothetical concerns;
- urgency and impact/probability uncertainty;
- mitigations and escalation signals;
- an analysis-only recommendation;
- unresolved questions.

Applied to ViralFactory, the pre-mortem found one observed launch-blocking evidence gap: repository qualification does not establish that the target environment has the required migrations/configuration or that the real durable render/storage/dashboard lifecycle works there. It also kept live-source/provider expansion risk explicitly hypothetical rather than inventing a failure.

## What the companion profile added

The profile adds some useful cross-domain structure:

- exact target/currentness identity is first-class;
- observations and material claims are separated from the risk taxonomy itself;
- claim-level scope and non-claims are easy to reconstruct without interpreting `tiger | paper_tiger | elephant`;
- the distinction `repository qualified != target environment activated` becomes visible outside the PM-specific risk schema.

## What it duplicated

Duplication is high in this episode.

The `risk_analysis` artifact already carries evidence status, evidence refs, uncertainty, mitigation, recommendation boundaries, and unresolved questions. Re-expressing every risk as generic observations/claims/uncertainties would create a second representation with little additional domain value.

This is direct evidence **against embedding the whole common envelope into PM risk artifacts**.

## Embedding assessment

No shared field is missing strongly enough from `risk_analysis` to justify a canonical contract change. The only clearly additive common fields are the compact target/currentness header and generic explicit-limit summary; even those can remain companion-level because the source artifact and episode context already identify the target.

**Episode signal:** favors **Outcome A — keep companion**, but with **low marginal value inside a strong domain artifact** and high duplication if embedded.

## Measured/observed experiment notes

- Material omission caught by companion profile: **no**; the PM artifact itself already preserved the consequential evidence gap and uncertainty.
- Fresh-context utility: **moderate-high** because generic claims/limits can be read without knowing the PM risk taxonomy.
- Domain-semantic duplication: **high**.
- Validator overreach observed: **none**; both validators remain representation-only.
- Local-only Probe Engine metrics: **unmeasured on connector surface**.
- Exact token overhead: **not instrumented**; this episode demonstrates enough duplicate representation that mandatory embedding would be hard to justify without stronger evidence.

## Non-claim

The `insufficient_evidence` recommendation is not a deployment decision. It records that the inspected Git evidence cannot establish target-environment activation and that the missing evidence should be collected through the existing runbook.
