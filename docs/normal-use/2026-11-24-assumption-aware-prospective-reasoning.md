# Assumption-aware prospective reasoning (2026-11-24)

**Status:** intellectual-capability increment and one authentic use.
**Source baseline:** `9ca3100bddad1972d4eef6d5fd7e9eb9158a4b98`.
**Contrast implementation:** `13bc8a2f9cdcac759778cc429dfdde1ef564ef9c`.
**Retained candidate:** `6fd3d765ef831fb7e08ac066e8ed0c5f7dff2086`.

This record covers the ability to reason about how alternative assumptions
change an authored possibility landscape. It does not claim that the tool
found a true assumption, selected a direction or improved a decision.

## 1. Authentic task

The governing question was:

> How should Sensemaking support assumption-aware prospective reasoning for
> its domain-general cognitive-development objective, without building another
> opportunity generator, ranker or infrastructure surface?

The task mattered independently because it is the owner's preferred next
intellectual capability and because the existing possibility landscape had not
been examined for assumption coverage.

## 2. Current behavior and limitation

The existing `possibility-ecology` operation already exposes one-hop candidate
relationships, including authored `references` with `conceptual_relation`
`assumes` or `sharesAssumptionWith`. The agent could inspect those relations,
but had no way to:

- project a whole goal's candidate set under an alternative assumption;
- distinguish candidates that depend on a negated assumption from those that
  do not;
- see which candidates have no authored assumptions at all;
- see shared assumptions that lack a direct relation between candidates;
- separate complete from partial relationship coverage.

A real contrast at `9ca3100b` showed:

- `goal:compounding-product-knowledge`: 5 candidates, 3 assumptions;
- `goal:domain-general-cognitive-development`: 9 inherited candidates, only
  3 assumptions, and 5 candidates with no visible assumption relation;
- `poss:assumption-aware-opportunity-ecology`, the candidate specifically about
  assumption-aware ecology, had **no authored assumptions** in the visible
  relation set;
- `hyp:cross-episode-synthesis-recurs` was shared by three candidates but two
  pairs had no direct relation;
- two candidates had truncated one-hop relationship coverage.

This is not proof that the underlying capabilities are absent. It is evidence
that the authored option set did not make its assumptions inspectable enough
for a scenario-conditioned comparison.

## 3. Desired behavior

An agent should be able to:

1. retrieve a goal or opportunity ecology;
2. identify the authored assumptions and their visible users;
3. author a small set of held/negated scenarios;
4. project affected, unaffected and unassessed candidates;
5. see shared assumptions and unrepresented pairs as questions;
6. use the contrast to discover or evaluate a materially different direction;
7. retain a new candidate only as a hypothesis if warranted.

The agent still owns scenario authorship, source inspection, applicability,
evaluation and selection.

## 4. Delivered capability

### `semantic possibility contrast`

A read-only operation over one committed ecology:

```bash
sensemaking-skills semantic possibility contrast --repo . --ref HEAD \
  --subject goal:compounding-product-knowledge \
  --scenarios scenarios.json --json
```

It validates a small scenario document, marks each visible candidate
`AFFECTED`, `UNAFFECTED` or `NOT_ASSESSED`, lists shared assumptions and
pairs without a direct relation, and discloses partial relationship coverage.
It does not infer assumptions, generate candidates, rank scenarios, select a
direction or authorize construction.

### Assumption-aware prospective reasoning reference

`skills/using-sensemaking/references/assumption-aware-prospective-reasoning-v1.md`
provides the procedure, scenario schema, interpretation rules and failure
modes. `using-sensemaking` conditionally points to it when a consequential
choice may be bounded by assumptions; it is not a mandatory stage.

### Hosted mechanical check

The semantic-context re-entry workflow runs a base and negated-assumption
scenario against `goal:compounding-product-knowledge`, asserts the bridge and
cross-episode candidate are affected, and asserts that no selection or
recommendation is performed. This proves the projection mechanics, not the
decision quality.

## 5. Authentic use and discovery

The agent ran four scenarios against the domain-general goal:

| Scenario | Affected candidates |
| --- | --- |
| `base` | none |
| `no-cross-episode` (negate `hyp:cross-episode-synthesis-recurs`) | 4, including the bridge and cross-episode synthesis |
| `no-agent-control` (negate `con:agent-owns-semantic-control`) | 2, including the bridge |
| `no-later-consult` (negate `hyp:later-sessions-consult-knowledge`) | 2 |

After retaining the new candidate, the contrast reported 10 visible
candidates, 3 assumptions, 5 unassessed candidates, and the new candidate
affected by both `no-cross-episode` and `no-agent-control`.

The consequential discovery was:

- the existing assumption-aware candidate had no authored assumptions;
- the domain-general goal had no **direct** candidate, only inherited
  repository-centric candidates;
- many candidates were unassessed for assumptions;
- shared assumptions existed without direct relations.

The agent selected a **focused scenario-contrast operation plus a portable
procedure**, not a full opportunity generator, ranker or new schema. It
retained `poss:assumption-contrast-inquiry` as a **hypothetical** candidate
serving `goal:domain-general-cognitive-development` and
`goal:compounding-product-knowledge`. It is the first direct candidate under
the domain-general goal. The producer marked it hypothetical; no realization or
selection authority is claimed.

## 6. What the agent rejected

- A broad opportunity generator: the contrast exposes authored assumptions; it
  does not manufacture candidates.
- A deterministic ranker or planner: the scenarios and interpretation are
  agent-owned.
- A new knowledge schema or Campaign extension: existing claims, relations and
  ecology projections were sufficient.
- Treating shared assumptions as recommended combinations: the output reports
  unrepresented pairs as questions.
- Treating a negated assumption as evidence that it is false: a scenario is
  hypothetical.

## 7. Claim ceiling

| Level | Status |
| --- | --- |
| Authored assumption relations projected under scenarios | Observed through the real CLI |
| Affected/unaffected/unassessed distinction | Observed |
| Shared-assumption groups and partial coverage disclosed | Observed |
| New candidate retained as hypothetical | Observed; first direct candidate for the domain-general goal |
| New candidate realization or value | NOT ESTABLISHED |
| Improved decision quality or reduced missed alternatives | NOT ESTABLISHED |
| Independent later-agent use | NOT ESTABLISHED |
| Comparative or longitudinal benefit | NOT ESTABLISHED |

The operation checks projection, not semantic truth. `NOT_ASSESSED` is not
absence. A scenario is not evidence. The new candidate remains hypothetical.

## 8. Continuation

The next useful evidence is an independent later agent using the contrast in a
real consequential decision and recording whether it changed or confirmed the
chosen direction, or whether the contrast was ignored as unhelpful. No further
projection, ranker, generator or schema is warranted without that evidence.

The candidate will be reconciled to a realization state only after source-
grounded use, not because the operation exists.

## Addendum: fresh evaluation and narrowing

A fresh agent evaluated the retained candidate at `6fd3d765` and
`bafa004b`. It judged `poss:assumption-contrast-inquiry` a **too-narrow
variant** of `poss:assumption-aware-opportunity-ecology`, not a distinct
substantial direction. It also found a real omission-disclosure defect when
`--limit` reduced the candidate set, which was fixed in `bafa004b`.

The parent accepted the judgment: the candidate was narrowed to `INCREMENTAL`
ambition, its non-load-bearing `hyp:cross-episode-synthesis-recurs` assumption
was removed, and a `NARROWED` disposition was recorded. The contrast operation
and portable procedure remain because they are real bounded support, but the
candidate is not claimed as a new product direction. See
[`2026-11-24-assumption-contrast-fresh-use.md`](2026-11-24-assumption-contrast-fresh-use.md).
