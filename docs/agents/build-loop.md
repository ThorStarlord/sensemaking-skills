# Build Loop: Sensemaking Skills Local Construction Profile

**Scope:** This page applies the portable
[`using-sensemaking` Skill](../../skills/using-sensemaking/SKILL.md) and its
[bundled construction reference](../../skills/using-sensemaking/references/portable-construction-loop-v1.md)
to **developing this repository**. It is **not** the portable build-loop
implementation and is **not required** in target repositories using the
installed Skill.

[Value-Directed Continuous Construction](../value-directed-continuous-construction.md)
states the product-value-led development philosophy for this repository.
`CLAUDE.md` holds the current owner-directed branch, local verification and
PR-merge instructions. This page connects that philosophy and those local
sources to the portable Architect -> Builder -> Reconcile capability; it
creates no new Skill, runtime, artifact, strategy or authority.

## Local product and strategic grounding

For an actual `sensemaking-skills` increment, read **selectively**:

- `CONTEXT.md` ("Current product definition") and
  `docs/product-strategy.md`: product goals, intended benefit and
  explicit epistemic ceilings.
- Accepted ADR 0029: scope, non-goals and agent-owned semantic control.
  Accepted ADR 0038: the Long-Horizon Adaptive Strategic Development purpose.
  Accepted ADR 0031: the persistent semantic stewardship foundation.
  Other accepted owner decisions and authority-bearing sources when
  relevant. The two sources used by PR #599 are **not** a future
  two-document authority allowlist.
- `docs/persistent-semantic-stewardship-plan.md` sections 12 and 14:
  value criteria and *illustrative* construction trajectory, **not** a
  deterministic backlog.
- `STATUS.md` "Current next step", relevant current Level-3 reconciliation
  and applicable unresolved owner boundaries.
- The current owning code/consumers, Git history, prior relevant PR, and
  task-specific reviewed semantic knowledge or Steward RECALL when it
  could change the decision.

Root `roadmap.md` and `goal.md` are historical, not current
implementation queues. Both authored goal records
`goal:longterm-stewardship` and
`goal:compounding-product-knowledge` remain unchanged by the owner's
2026-10-26 reconciliation. Never silently merge them, assert an additional
relationship, or infer product authority from an indexed record.

## Keep recent receipts from becoming a backlog

A recent session receipt or PR recommendation is history, not a new local
priority. Repeated diagnostics and repairs of one support surface (such as
the receipt reader) warrant checking for selection anchoring, not another
fix by default. When the next responsibility is open, compare the candidate
against current PATH-1 product value, source-grounded gaps and a materially
different credible outcome. If recommending "stop receipt polish; return to
PATH-1", identify a concrete possible capability and its owning source and
consequence, or report that the specific next responsibility remains unknown.
No mandatory candidate count, extra Skill, strategic reopening or approval
gate follows from this check. Clear authorized bounded work remains direct.

## Observed repository-only discovery miss (2026-10-27)

An owner-shared coding-agent transcript at `e11a44f` exposed a failure of
**task grounding during actual Skill use**, despite the existing
method-versus-target and repository-only discovery instructions (PRs #619 and
#620). The owner intended `using-sensemaking` as the method applied to the
whole `sensemaking-skills` repository. The agent instead declared the Skill
component its explicit target, investigated prior Skill-only receipts, and
closed with "no further Skill edit warranted". It acknowledged the wrong
scope only after the owner challenged the conclusion; the intended
repository-wide discovery was not shown to complete.

The reported working-tree-only receipt,
`.sensemaking/receipts/2026-10-27-use-sensemaking-skill-target.session.yaml`,
listed `target_repository: ThorStarlord/sensemaking-skills`, but its actual
responsibility was "Diagnose the using-sensemaking Skill as the explicit
target" and its stop disposition was `NO_FURTHER_WARRANT` for that component.
A matching repository identity field **does not establish semantic coverage**.
The transcript's `Get-Content STATUS.md -TotalCount 220` also could not read
the later "Current next step" section; it did not demonstrate a full current
product-capability comparison. This is owner-supplied episode evidence, not a
Git-committed receipt or an independent agent-success/failure rate.

**Leading hypothesis, not proven cause:** premature component-level task
framing, reinforced by related historical receipts, displaced product-level
discovery. Incomplete context delivery or other instruction-application
failures have not been ruled out. The real gap is between *knowledge present
in the Skill* and *knowledge used to select and close a responsibility*.

**Decision-relevant follow-up:** investigate where the original target was
lost in a real invocation and whether the current lightweight entry/closure
judgment can prevent premature `NO_FURTHER_WARRANT`. At entry, distinguish
invoked method, requested target, intended outcome and authority. Before
closure, compare the owner's requested scope with the source areas actually
examined, selected responsibility, final claim **and** receipt; if one
component was assessed, do not infer repository-wide completion. Continue the
authorized discovery after a scope correction. Use ordinary source and
session evidence to decide whether any further implementation is needed;
do not default to another receipt feature, large Skill rewrite, mechanical
validator or synthetic evaluation. This is a candidate engineering
investigation, **not** a ratified automatic PATH-1 backlog item or evidence
that the documented safeguard already works.

## Outcome-Responsibility Drift (ORD): Method Adaptation construction case (2026-11-19)

**Definition (descriptive, not a new policy):** Outcome-Responsibility Drift occurs
when the agent selects or closes a local responsibility that is relevant to,
but materially narrower than, the governing owner outcome, without recognizing
that the larger outcome remains unmet. A locally correct patch, source review
or receipt does not by itself satisfy a broader capability goal. **Premature
local closure** is one observable manifestation. **Defensive minimalism** (a
preference for easy-to-defend small actions) and **constraint inversion**
(treating a means-limiting heuristic as the primary objective) are possible
explanations, **not demonstrated causes**.

**Source-grounded sequence:**

- [PR #930](https://github.com/ThorStarlord/sensemaking-skills/pull/930)
  concluded `NO_CODE_CHANGE / NO_FURTHER_WARRANT` after using the
  [#909 receiving-agent record](../normal-use/2026-11-18-receiving-agent-adaptation-909.md)
  as its existing method-adaptation precedent. That record shows a technical
  hypothesis correction and a two-line output repair, not attributable
  development of a reusable reasoning procedure.
- [PR #931](https://github.com/ThorStarlord/sensemaking-skills/pull/931)
  correctly narrowed the earlier completion inference and retained a
  conditional method-claim checking candidate. The correction was useful but
  did not itself deliver the requested agent-facing method lifecycle.
- [PR #932](https://github.com/ThorStarlord/sensemaking-skills/pull/932)
  then delivered optional `semantic method context` and `semantic method
  record` interfaces. Hosted read-side re-entry succeeded; authentic
  write-side use and independent cognitive benefit were not established.
  Its later success does **not** establish why the earlier selections differed.

This resembles the [2026-10-27 task-grounding miss](#observed-repository-only-discovery-miss-2026-10-27),
but the episodes are not matched comparisons. Plausible alternative
explanations include differing owner prompts and explicit scope grants,
reliance on earlier receipts, uneven exposure to guidance, a remote-only
execution environment favoring documentary changes, or an agent-level
selection tendency. Do not infer an intrinsic bias or a general failure rate
from these few episodes.

**Observe during valuable work, without a mandatory procedure:** when a
consequential responsibility is selected or closed, compare the actual owner
outcome, the responsibility selected, the user-visible capability delivered,
and the outcome that remains open. If a material, credible alternative could
deliver much more value within authority, reconsider before declaring
`GOAL_SATISFIED` or `NO_FURTHER_WARRANT`. Preserve only original,
source-attributed task/decision evidence already useful to the work; a
post-hoc report is not a contemporaneous decision trace. A small patch can
be exactly right, and a `NO_CODE_CHANGE` decision can be justified.

**Historical continuation (2026-11-19):** the
[Method Adaptation v0 construction-and-observation plan](../superpowers/plans/2026-11-19-method-adaptation-v0-continuation-ord-observation.md) sets the earlier construction-first context.
ORD is a secondary observation lens, not a new controller, obligatory
reflection checkpoint, qualification study, or reason to postpone construction.

**Later reconciliation (2026-11-27):** the [historical cognitive-failure
review](../normal-use/2026-11-27-adaptive-cognitive-failure-review.md) preserves
#935's useful implementation while disputing the warrant for its
`SCOPE_EXHAUSTED` stop under the broader delegation. The broader gap was
acknowledged, so classical ORD under the narrow definition above is not
conclusively established. The portable AMS safeguards and terminal prompt
now support recognizing and correcting this kind of scope mismatch before a
consequential selection or stop. This is not evidence that the guidance has
already changed a later agent's cognition.

## Continue after a spike or merged increment

**Remember:** `GOAL -> SPIKE? -> BUILD -> INTEGRATE -> CONTINUE`.
The optional spike settles an uncertainty, not the whole capability. After
any spike or merged PR, compare the actual source/behavior with the authorized
end-to-end goal. If a necessary vertical layer remains and another increment
is warranted and authorized, build it instead of defaulting to more unit or
integration tests, a new evaluation harness or external field validation.
Perform the verification demanded by the actual change and this repository's
current policy; known consequential defects still need repair, and hosted CI
and release boundaries remain intact. For an explicitly delegated terminal
mission, continue through subsequent bounded responsibilities until the
terminal goal or a genuine stop boundary. A bounded request does not expand
into an unlimited mission. See [the local continuation rule](../../CLAUDE.md)
and [the existing construction guide](../value-directed-continuous-construction.md);
this is a reminder of their policy, not a new process or approval gate.

## Local PR and verification conventions

Use the **portable Skill** for proportional architect selection, real
implementation, in-scope redesign, review, decision-relevant reconciliation,
and the boundary between one increment and a multi-increment strategic
mission. The following details are **local overrides/choices**, not
portable defaults:

1. **Every construction PR** has a short source-grounded decision note in
   the description. Two sentences suffice for a clear local repair;
   consequential selection records real alternatives, the intended useful
   slice, affected contracts and review/verification limits. Do not
   generate fixed candidate counts, numeric priorities or a separate
   handoff artifact for an obvious change.
2. Use a separate `claude/<topic>` branch for each PR, per `CLAUDE.md`.
3. In the current owner-declared CONSTRUCTION phase, **do not add or
   manually run local unit/synthetic evidence tests**. Inspect the source
   and diff, perform proportionate non-test mechanical checks where
   appropriate and report `NOT_RUN` accurately. This phase-specific
   exception does **not** apply to other repositories or release
   qualification.
4. Under the owner's explicit local policy, **merge authorized PRs
   promptly after a clean source/diff review without waiting for hosted
   CI**. Preserve actual GitHub protections, hosted CI and release gates;
   do not knowingly merge consequential dangerous failures or invent
   check results. A material post-merge failure becomes a warranted
   repair responsibility.
5. Keep routine decisions and evidence in PR/Git history. Update
   `STATUS.md` only when strategy, actual capability, meaningful
   limitations or next responsibility changes materially. Reconcile
   reviewed knowledge only if source-grounded, durable learning will
   improve later decisions.
6. When an in-scope Builder discovery changes the design, update the
   same PR note and continue. Reassess responsibility or ask for owner
   input if outcome, product authority or protected scope changes.

## Boundary and interpretation

This repository's operating instructions help its maintainers. They
must **never** be treated as an install-time dependency, an instruction
that `using-sensemaking` must be invoked through `CLAUDE.md`, or a
blanket merge/test policy in `auteur`, `React_incremental_game_prototype`,
or any other target. Another coding agent can use the bundled portable
loop **after loading the Skill**, grounded in whatever authentic sources
that target has. Discovery still depends on its host/Skill installation;
missing documentation neither guarantees auto-loading nor prevents the
Skill from functioning when loaded.
