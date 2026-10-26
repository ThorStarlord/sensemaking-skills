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
  Accepted ADR 0031: the Persistent Semantic Stewardship destination.
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
