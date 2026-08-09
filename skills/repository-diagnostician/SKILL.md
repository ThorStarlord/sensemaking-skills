---
name: repository-diagnostician
description: "PROTOTYPE (prototype/repo-sensemaker-vnext, not canonical): non-interactive repository diagnostic core. Given repository state and already-known intent, investigates and produces a Repository Sensemaking Brief (vNext). Does not talk to the owner."
---

# repository-diagnostician (PROTOTYPE)

**Status: experimental, not canonical.** This skill is a candidate answer to one
packaging question: *should repository investigation be a separate,
non-interactive skill from owner interaction?* It is Option A from
`docs/prototypes/repo-sensemaker-vnext.md`. Nothing about its existence
implies the question is settled.

This skill has exactly one responsibility: given a repository and whatever
intent is already known (recovered by the caller, not by this skill), gather
evidence, model the repository, and produce a **Repository Sensemaking Brief
(vNext)**. It never asks the owner anything. If the input intent is
insufficient to proceed, it says so in the brief's `owner_intent_state`
field (see `references/brief-vnext-template.md`) rather than pausing to ask.

## Division of responsibility (prototype)

- **Owner interaction** (recovering intent, deciding whether to ask a
  clarifying question, synthesizing a final recommendation) belongs to the
  caller — in this prototype, `repo-sensemaker`'s EXPERIMENTAL interaction
  layer (see its SKILL.md). This skill does not do that.
- **Repository investigation and evidence-grounded diagnosis** belongs here.

## Inputs

- `repository_state`: the repository to analyze (read-only).
- `known_intent` (optional): whatever the caller has already established
  about what the owner wants — may be empty, partial, or absent. This skill
  must not treat an absent or thin `known_intent` as license to guess; it
  should proceed with what repository evidence can establish and mark the
  rest as unresolved (see `owner_intent_state` below), not invent a
  preference.

## Workflow

1. **Analyze**: inspect README, core files, folder structure, existing
   documentation, git history, and configuration — same evidence discipline
   as the canonical `repo-sensemaker` skill's Standard Workflow steps 1-2.
2. **Evidence gathering**: cite specific file paths and line ranges. Follow
   [Evidence Rules](../repo-sensemaker/references/evidence-rules.md) — this
   prototype does not fork that reference; there is exactly one evidence-rules
   authority.
3. **Consequential boundary identification (vNext)**: identify the boundary
   where the next important decision sits. Then, and only then, ask whether
   it represents a demonstrated/suspected weakness or a legitimate unresolved
   choice:
   - Demonstrated weakness → classify with one of the seven [Weakness
     Types](../repo-sensemaker/references/weakness-types.md) (unchanged from
     canonical — this prototype does not redefine that taxonomy).
   - Legitimate unresolved choice (e.g. two viable directions, repository
     evidence cannot pick between them) → do **not** force a weakness label,
     and do **not** invent a `none`/sentinel value for it either (rejected
     in the assumption ledger, A-04 — it would contaminate the 7-item
     defect-mechanism taxonomy). Set `is_demonstrated_weakness: false`,
     describe the choice fully in `consequential_boundary`, and leave
     Section 13's canonical `weakness_type` absent — its non-blocking
     warning (D2) is the correct, already-existing behavior for this case.
4. **Uncertainty classification (vNext)**: for whatever about the
   consequential boundary remains unresolved, classify *why* it's
   unresolved, not just that it is:
   - `repository_evidence` — investigation is incomplete; more digging in
     this repository could resolve it.
   - `empirical` — repository evidence can describe the question but not
     answer it; only running/observing something would.
   - `owner_intent` — the repository can describe the options but choosing
     among them is a preference or strategic call only the owner can make.
   - `external_environment` — the answer depends on something outside this
     repository (a third-party service, a platform constraint).

   This field only has behavioral value because it's *derived from actual
   investigation*, not asserted from a template. If you have not tried to
   resolve something before classifying it as `owner_intent`, you have not
   done this step. (Evidence: S1's PROMISING disposition rested on exactly
   this distinction being made post-investigation, not a priori.)
5. **Fog classification**: unchanged from canonical — see
   [Canonical Vocabulary Registry](../../docs/canonical-vocabulary.yaml).
6. **Synthesis**: produce the brief per
   [Repository Sensemaking Brief vNext template](references/brief-vnext-template.md).
   The template is additive over the canonical brief — every canonical
   Section 13 field is unchanged and still validated by
   `scripts/validate-brief.py`; the vNext fields live in a separate,
   clearly-marked `analysis_vnext:` block that no canonical validator reads
   or enforces.

## Boundary rules (unchanged from canonical repo-sensemaker)

1. **No implementation.** This skill produces a diagnostic artifact only.
2. **Registry grounding.** Any `recommended_workflow_id` must be verified
   against the real `workflow-registry.yaml`. This prototype adds no new
   routes and makes no routing-coverage claims.
3. **No owner contact.** If this skill cannot proceed without owner input,
   it stops and reports `owner_intent_state: blocking_unknown` rather than
   fabricating an answer or attempting to ask anyone.

## What this skill deliberately does not do

- Does not talk to the owner.
- Does not decide whether to escalate for a clarifying question — that's
  the interaction layer's call, made with this brief as input.
- Does not modify canonical `artifact-contracts.yaml`, `weakness-types.md`,
  or `canonical-vocabulary.yaml`. Every canonical reference above is a
  relative link to the one real copy, not a duplicate.
- Is not registered in `skills/workflow-planner/references/skill-registry.yaml`
  or any workflow. It is invoked directly by name during evaluation of this
  prototype, not through the canonical orchestration path.

## References

- [Repository Sensemaking Brief vNext template](references/brief-vnext-template.md)
- [Evidence Rules](../repo-sensemaker/references/evidence-rules.md) (canonical, not forked)
- [Weakness Types](../repo-sensemaker/references/weakness-types.md) (canonical, not forked)
- [Canonical Vocabulary Registry](../../docs/canonical-vocabulary.yaml) (canonical, not forked)
- [Prototype assumption ledger](../../docs/prototypes/repo-sensemaker-vnext.md)
