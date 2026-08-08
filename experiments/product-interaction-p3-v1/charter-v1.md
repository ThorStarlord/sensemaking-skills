# Task P3 — Cross-Repository Decision-Sharpening Probe (charter, frozen)

experiment_type: product_interaction
record: charter-v1
recorded_at: 2026-08-08 (before any target-specific investigation)
status: FROZEN
owner: ThorStarlord (repository owner)
scope: experiments/product-interaction-p3-v1/

## Purpose

Test whether the product-value signal observed in Tasks P1 and P2 transfers to
a real repository outside Sensemaking Skills.

This is a lightweight product-discovery / product-value experiment.

Core hypothesis:

> "When an owner is uncertain about consequential engineering work,
> repo-sensemaker can investigate the repository and leave the owner in a
> materially better position to decide what should happen next."

P3 does NOT attempt to prove this hypothesis generally. Its specific question is:

> "Does that decision-sharpening value appear in a materially different
> repository context?"

## Target

- Target repository: **auteur** (H:\GithubRepositories\auteur)
- Owner decision: **generic shape** — "What engineering work would create the
  most value next?" (owner selected the generic question; no more specific real
  owner decision was stated)
- The target repository must not be modified as part of P3.

## Evidence claim

P3 uses an ASSISTED_BASELINE, not an independently captured OWNER_PRE.
Therefore no clean PRE->POST decision delta is claimed.

P3 may support a claim of the form:

> "Given a real owner decision and the legitimate context available before
> investigation, repo-sensemaker produced a recommendation that the owner judged
> useful, decision-relevant, or action-sharpening."

## Phase 0 — Freeze identities (recorded before investigation)

- Target repository: auteur @ SHA `374abb48fb1f39d1ddb140df9b43b34cf53f4beb`
  (working tree had local modifications at freeze time: tracked file
  `docs/reviews/2026-07-28-cartographer-profile-emotional-target-evaluation.md`
  +6 lines uncommitted; untracked agent/runtime directories and root-level
  report artifacts present; all untracked paths are gitignored except several
  agent scratch directories; the frozen identity is the committed SHA).
- Canonical Sensemaking Skills repository: SHA
  `d980bcdbf49209a10fa1f9ac00d888dda800ba52` (worktree has an unrelated
  modified `src/sensemaking_skills.egg-info/PKG-INFO`).
- Canonical repo-sensemaker SKILL.md: `skills/repo-sensemaker/SKILL.md`,
  git blob SHA `a5cb5dd71fd75adeb879780b9dc47020cecd5ab3`.
- Exact owner question: "What engineering work would create the most value next?"
- Execution mode: agent-native, one-shot, read-only canonical repo-sensemaker
  interaction (agent performs the analysis per SKILL.md as a local procedure).
- Timestamp: 2026-08-08.

Only the current canonical repo-sensemaker is used. Not used: frozen hardening
candidates, stale installed copies, experimental repair branches, or prompts
modified for P3.

## Phase 1 — Assisted baseline

Summarize only legitimate existing owner context. Record: decision being made;
owner context already available; apparent inclination only if genuinely
supported; already-known reasoning; most important apparent uncertainty.
If no clear owner inclination exists, write exactly `NO CLEAR PRE INCLINATION`.
Label the artifact ASSISTED_BASELINE, never OWNER_PRE. State explicitly that it
is reconstructed context and cannot support a clean PRE->POST delta claim.
Freeze before investigation.

## Phase 2 — One canonical repo-sensemaker interaction

Run exactly ONE read-only canonical repo-sensemaker investigation against the
target repository. Do not implement anything. The investigation should:

- distinguish observed evidence from inference;
- identify the apparent problem and challenge whether it is framed correctly;
- identify materially different alternatives, including defer/do-nothing where
  credible;
- identify evidence supporting and challenging the apparent owner direction;
- identify the most decision-changing uncertainty;
- recommend the smallest action justified by the evidence;
- avoid converting an unfinished technical state directly into product priority
  without justification;
- preserve prior owner decisions unless repository evidence gives a reason to
  challenge them.

Do not optimize for agreement with the owner.

## Phase 3 — Owner-facing synthesis

Produce a compact synthesis containing:

1. Recommended action.
2. Why it matters now.
3. Strongest supporting evidence.
4. Strongest credible alternative.
5. Most important remaining uncertainty.
6. Cheapest credible next action/probe.
7. Confidence and why it is bounded.
8. Prior owner decision preserved or challenged — explain which and why.

Keep it substantially shorter than the investigation artifact.

## Phase 4 — Validation

Canonical standalone validation is part of normal repo-sensemaker execution.
Run it exactly once and preserve the result (`validation-result-v1.json`).
If it fails: record the failure as evidence; do not repair the brief; do not
repair the validator; do not rerun repo-sensemaker; do not rerun validation.
Validation success/failure does not substitute for the product-value question.

## Phase 5 — Lightweight owner POST

Ask only:

1. Is this recommendation useful?
2. Did it change, narrow, sequence, or better justify what you would do?
3. What specifically was decision-changing or decision-sharpening, if anything?

Record the owner's response faithfully. Do not ask the owner to reconstruct an
independent PRE.

## Phase 6 — Learning

Use one descriptive disposition:

```
STRONG_SHARPENING
USEFUL_CONFIRMATION
WEAK_SHARPENING
NO_SHARPENING
MISLEADING
```

Do not create a scorer. Answer: "Did this interaction leave the owner
materially better positioned to decide what engineering work should happen
next?" Then answer the cross-repository learning question: "What did P3 change
about our confidence that repo-sensemaker's decision-sharpening value transfers
beyond Sensemaking Skills?" Use one of: STRENGTHENED / WEAKENED / UNCHANGED /
AMBIGUOUS. Explain in prose.

## Artifacts

- charter-v1.md
- assisted-baseline-v1.md
- repo-sensemaker-investigation-v1.md
- owner-synthesis-v1.md
- owner-post-v1.md
- learning-v1.md
- validation-result-v1.json (canonical validation runs for this skill)

No additional schemas, scoring infrastructure, campaign machinery, or
automation for P3.

## Hard stop

P3 does not authorize implementation. Do NOT: modify the target repository;
modify repo-sensemaker; fix the standalone validation surface; start a
hardening cycle; implement evaluation changes; begin installation/distribution
construction; start P4 automatically; implement any recommendation produced by
P3. If the investigation identifies a promising engineering action or
follow-up probe, record it and stop.
