# Possibility Synthesis v1

Use this optional producer when a goal-family inspection yields a genuinely new
recombination or a newly identified gap that the active agent decides is worth
retaining as a candidate possibility. It does not activate for a routine
retrieval or for restating an existing record under a new name.

The active agent owns the synthesis. The producer only validates provenance and
materializes an unreviewed proposal.

## 1. Inspect the existing family

Start from the existing product and possibility consumers:

```bash
sensemaking-skills semantic workspace-query \
  --operation product-outline --include-candidates --json

sensemaking-skills semantic workspace-query \
  --operation possibility-ecology \
  --subject goal:domain-general-cognitive-development --json
```

Inspect the candidate statements, dimensions, realization states, goal links,
relationships and shared links. Identify specifically what the new candidate
combines or what gap it addresses. A new candidate that merely restates an
existing one should not be recorded.

## 2. Author the synthesis episode

Create a tracked UTF-8 JSON episode and stage or commit it first:

```json
{
  "possibility_id": "short-lowercase-slug",
  "actor": "the actual synthesizing agent",
  "source_revision": "40-character Git commit SHA",
  "origin_date": "YYYY-MM-DD",
  "title": "Short candidate title",
  "statement": "The new capability possibility and its intended beneficiary behavior.",
  "goal_refs": ["goal:existing-goal"],
  "source_candidate_refs": ["poss:existing-candidate"],
  "capability_refs": ["cap:existing-capability"],
  "assumption_refs": ["hyp:existing-assumption"],
  "contradicts_refs": ["poss:existing-conflicting-alternative"],
  "dimensions": {
    "alignment": {"value": "ALIGNED", "basis": "why the product purpose supports it"},
    "ambition": {"value": "SUBSTANTIAL", "basis": "what new outcome it would enable"},
    "horizon": {"value": "FORESEEABLE", "basis": "which existing records/capabilities seed it"},
    "realization": {"value": "HYPOTHETICAL", "establishment": "inferred", "basis": "no implementation is claimed"}
  },
  "synthesis_basis": "what existing candidates/capabilities/assumptions are combined and why this is distinct",
  "value_hypothesis": "what would become materially better if it worked",
  "revisit_when": "what later evidence would confirm, narrow or retire it",
  "counterevidence": "opposing evidence or NOT_ASSESSED",
  "claim_ceiling": "what this synthesis cannot establish",
  "evidence_refs": ["file:tracked/evidence/path.md"]
}
```

`source_candidate_refs` must name existing `poss:` opportunities at
`source_revision`; `goal_refs` must name existing goals. Capability,
assumption and contradiction refs are optional but validated when present.
`realization` must be `HYPOTHETICAL` or `NOT_ASSESSED`; the producer refuses an
implementation claim. Evidence paths must be tracked source files.

## 3. Materialize and review

```bash
sensemaking-skills semantic possibility record \
  --repo . --episode path/to/synthesis.json \
  --output .sensemaking/knowledge/possibility-<slug>.json --json

sensemaking-skills semantic knowledge-proposal-check \
  --repo . --proposal .sensemaking/knowledge/possibility-<slug>.json --json
```

The producer creates a hypothetical `opportunity` claim with:

- `candidate_opportunity_for` links to the cited goals;
- `derived_from` links to the source candidates;
- optional `requires_capability`, `assumes` and `contradicts` links.

It never edits existing possibilities, ranks candidates, selects a direction,
commits or grants permissions. The output is an `UNREVIEWED_DRAFT`; ordinary
Git review remains necessary.

When synthesis and review occur in different contexts, keep the hypothetical
proposal outside active knowledge until a compatible reviewer can inspect it:

```bash
sensemaking-skills semantic possibility record \
  --repo . --episode path/to/synthesis.json --draft-only \
  --output .sensemaking/proposals/possibility-<slug>.json --json

sensemaking-skills semantic knowledge-proposal-check \
  --repo . --proposal .sensemaking/proposals/possibility-<slug>.json \
  --destination .sensemaking/knowledge/possibility-<slug>.json --json
```

The same schema and provenance checks apply. The detached preflight is read-only,
binds draft bytes by digest and checks against the current committed packs and
index-tracked evidence; it does not make the draft a queryable opportunity.
Retain only decision-relevant unreviewed drafts; never treat them as knowledge.
After semantic review and explicit knowledge-edit authority, compare checked
bytes, copy to the intended new pack, rerun ordinary preflight, commit and
build at the exact clean revision. Existing pack edits remain in-place checks.
If tooling is unavailable, retain the original synthesis episode or draft
outside knowledge, and report preflight NOT_RUN. No automatic promotion.

## 4. Consumer and limits

After review, the new candidate appears in existing `product-outline` and
`possibility-ecology` results under its cited goal(s), with authored dimensions,
realization, relationships and shared links. When the candidate is inspected as
an opportunity focus, `possibility-ecology` also shows its explicit
`required_capability_routes` to reviewed components, so a later agent can
reconstruct the construction bridge without a separate outline lookup. It
remains a possible future, not a selected strategy, shipped capability or proof
of value.

```text
synthesis support != automatic generation
new candidate      != validated opportunity
reviewed record    != implementation
reviewed record    != selection or authorization
```

A later agent must inspect the original evidence, counterevidence and
conditions. Applying, implementing, ranking or rejecting the candidate remains
the agent's decision. Independent later use and comparative benefit require
separate evidence.
