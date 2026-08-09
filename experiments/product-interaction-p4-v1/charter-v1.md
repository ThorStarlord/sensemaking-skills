# Task P4 — Documentation-Light Transfer Probe (charter, frozen)

experiment_type: product_interaction
record: charter-v1
recorded_at: 2026-08-08 04:15:49 -03:00 (before any target-specific investigation)
status: FROZEN
owner: ThorStarlord (repository owner)
scope: experiments/product-interaction-p4-v1/

## Purpose

Test whether the decision-sharpening value observed in P1-P3 survives in a
real repository where explicit narrative documentation is substantially
weaker than in Sensemaking Skills and Auteur.

This is a lightweight product-discovery experiment. Do not implement anything.

Core hypothesis:

> "When explicit repository narrative is sparse, repo-sensemaker can still use
> code, tests, configuration, history, and runtime/product surfaces to identify
> a consequential engineering decision boundary and recommend a bounded next
> action."

P4 does not attempt to establish general product validity.

## Target

- Target repository: **renpy_mcp_server** (H:\GithubRepositories\renpy_mcp_server)
- Owner decision: **generic shape** — "What engineering work would create the
  most value next?" (owner selected the generic question; no more specific real
  owner decision was stated)
- The target repository must not be modified as part of P4.
- Experimental variable: DOCUMENTATION RICHNESS. The target has ~8.5k code
  files, ~30 markdown files, no ADR directory at freeze time — substantially
  weaker explicit narrative than Sensemaking Skills and Auteur. Owner
  relationship and work are real; this is not combined with a different-owner
  experiment.

## Phase 0 — Freeze identities (recorded before investigation)

- Target repository: renpy_mcp_server @ SHA `a1d6f55af5716a50a8674302466b385711ef513f`
  (working tree clean at freeze time: 0 modified/untracked entries).
- Canonical Sensemaking Skills repository: SHA
  `27aa2442e5395f8793023882d5ed5e94861755e4` (worktree has an unrelated
  modified `src/sensemaking_skills.egg-info/PKG-INFO` and untracked `.reasonix/`).
- Canonical repo-sensemaker SKILL.md: `skills/repo-sensemaker/SKILL.md`,
  git blob SHA `a5cb5dd71fd75adeb879780b9dc47020cecd5ab3` (identical to the
  canonical identity frozen in P3).
- Exact owner question: "What engineering work would create the most value next?"
- Execution mode: agent-native, one-shot, read-only canonical repo-sensemaker
  interaction (agent performs the analysis per SKILL.md as a local procedure).
- Timestamp: 2026-08-08.

Only the current canonical repo-sensemaker is used, exactly once. Not used:
hardening candidates, stale installed copies, modified prompts, or repair
branches.

## Phase 1 — Assisted baseline

Capture: real owner situation; real owner question; prior inclination only if
legitimately supported; existing reasoning if available; apparent
decision-changing uncertainty. If none exists, write exactly
`NO CLEAR PRE INCLINATION`. Clearly state this is an ASSISTED_BASELINE and
cannot support a clean PRE->POST claim. Freeze before investigation.

## Phase 2 — One investigation

Run exactly ONE read-only canonical repo-sensemaker investigation against the
target. Do not implement or modify the target repository. Investigate available
evidence including code, tests, configuration, dependency/runtime boundaries,
git history, package/release state, documentation where available, and
generated/runtime artifacts where relevant. For important claims, identify the
dominant evidence source using lightweight labels where useful: CODE / TEST /
CONFIG / HISTORY / DOC / RUNTIME/ARTIFACT / INFERENCE. These labels are
descriptive only — no schema or validator.

The investigation must:
- distinguish observations from inference;
- identify the most consequential apparent decision boundary;
- compare materially different alternatives, including defer/do-nothing where
  credible;
- explain why the recommended boundary matters more than other visible issues;
- bound uncertainty when product intent cannot be inferred from repository
  evidence;
- prefer the smallest justified next action.

Do not turn generic code-quality observations into product priority without
evidence.

## Phase 3 — Synthesis

Produce a compact owner-facing synthesis:

1. Recommended action.
2. Why this matters now.
3. Strongest evidence.
4. Strongest credible alternative.
5. Most important uncertainty.
6. Cheapest credible next move.
7. Confidence and why bounded.
8. What repository evidence cannot establish without owner/product context.

If one targeted owner question would materially improve the decision, say so
explicitly rather than inventing the missing intent. Do not ask that question
or rerun the experiment unless separately authorized; record it as
product-learning evidence.

Keep the synthesis substantially shorter than the investigation artifact.

## Phase 4 — Validation

Canonical standalone validation is part of normal repo-sensemaker execution.
Run it exactly once and preserve the result (`validation-result-v1.json`).
If it fails: record the failure as evidence; do not repair the brief; do not
repair the validator; do not rerun repo-sensemaker; do not rerun validation.
Validation success/failure does not substitute for the product-value question.

## Phase 5 — Owner POST

Ask:
1. Is the recommendation useful?
2. Did it establish, change, narrow, sequence, or better justify what you would
   do?
3. What specifically was decision-changing or useful, if anything?
4. Did the recommendation feel grounded in repository evidence, or did it rely
   too heavily on speculation?

Record answers faithfully.

## Phase 6 — Learning

Assign one descriptive disposition:

```
STRONG_SHARPENING
USEFUL_CONFIRMATION
WEAK_SHARPENING
NO_SHARPENING
MISLEADING
```

Then answer: "What did P4 change about our confidence that repo-sensemaker's
decision-sharpening value survives documentation-light repositories?" Use one
of: STRENGTHENED / WEAKENED / AMBIGUOUS / UNCHANGED. Explain in prose.

Also record whether P4 suggests the preferred product interaction should be:
- autonomous investigation -> recommendation;
- investigation -> one targeted owner question -> recommendation;
- another interaction shape;
- unresolved.

Do not implement the interaction.

## Artifacts

- charter-v1.md
- assisted-baseline-v1.md
- repo-sensemaker-investigation-v1.md
- owner-synthesis-v1.md
- owner-post-v1.md
- learning-v1.md
- validation-result-v1.json (canonical validation runs for this skill)

No scoring infrastructure. No aggregate evaluator. No campaign machinery.
No new schemas.

## Hard stop

P4 does not authorize implementation. Do NOT: modify the target repository;
modify repo-sensemaker; fix validator behavior; start hardening; implement a
recommended action; prototype the discovered interaction; start another P
experiment automatically. If the investigation identifies a promising
engineering action or follow-up probe, record it and stop.
