# Scientific questions — EXP-0001-stage1-auteur-autonomy-pilot

This campaign is NOT asking "can we keep retrying until we get a good
answer?". It is asking: under one frozen configuration, what is the
distribution of outcomes across three independently reserved, authorized,
and recorded attempts?

Every attempt uses the exact same configuration identity
(`bd36c7b68e85c37503daf07aa02a5e05147e052bf5f222731a996a0dcd242fc7`).
Each attempt gets its own attempt ID, its own durable reservation, its own
budget charge, and its own ledger history (Phase 4). The append-only ledger
and the derived campaign summary will enumerate all three attempts — the
system has no successes-only export mode, so no run can be concealed.

## 1. Consistency

Do three runs under one configuration identify the same architectural
boundaries and weaknesses in the Auteur repository at the pinned SHA?

## 2. Output variance

How much do prioritization, terminology, and evidence selection change
between runs of the same `repository_sensemaking_brief` artifact?

## 3. Failure rate

Does the provider reliably produce a schema-valid
`repository_sensemaking_brief` for this target? Provider failures and
validation failures are recorded, budgeted, and preserved exactly like
successes.

## 4. Evidence stability

Do the findings repeatedly point to the same files, components, and
quoted evidence passages?

## 5. Decision usefulness

Does one run produce a materially better recommendation than the others,
or are the three roughly equivalent for downstream planning?

## Non-goals

- This campaign does not retry until success: a failed or invalid attempt
  is never silently repeated under the same attempt ID; a retry is a new
  attempt with a new reservation and a new budget charge (Phase 4).
- This campaign produces exploratory output only
  (`EXPLORATORY_NOT_CANONICAL_EVIDENCE`). Nothing it produces is canonical
  evidence, and nothing it produces is automatically merged or promoted.
