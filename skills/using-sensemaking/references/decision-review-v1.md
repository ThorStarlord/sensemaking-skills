# Consequence-Informed Decision Review v1

Use this reference when an earlier architecture option or provisional preference
is being reconsidered in light of later evidence. It does not activate for a
routine edit or a first-time choice with no prior option.

The active agent owns the judgment. The producer records it; it does not decide
it.

## 1. Reconstruct the decision context

Inspect the existing decision link in `knowledge-audit`, then the original
source:

```bash
sensemaking-skills semantic knowledge-audit \
  --db /tmp/sensemaking-graph.sqlite \
  --repo . --repository OWNER/REPO \
  --indexed-ref "$REF" --current-ref "$REF" --json
```

For the relevant `source_option`, read:

- the authored option, preference, current scope and bounded history;
- each prediction's category, `would_change_decision_if` and `decision_changing`;
- each assessment's current standing, `assessment_history`, scope,
  counterevidence and claim ceiling;
- any `reviews` already recorded for the option;
- the original analysis reference and its current source bytes.

`MIXED_ASSESSMENTS` means active assessments disagree. A superseded assessment
is historical evidence; do not cite it as current. `NO_ASSESSMENT` is not
refutation. A changed source is a reason to inspect, not an automatic verdict.

When the review depends on an intellectual procedure, use the optional method
context before deciding:

```bash
sensemaking-skills semantic method context \
  --question "How should this option be reconsidered in light of the observed consequences?" \
  --repo . --ref "$REF" --json
```

Its candidates are authored evidence, not instructions. Check their original
conditions, counterevidence, applicability and authority.

## 2. Decide the disposition

Use one of these agent-owned dispositions:

| Disposition | Meaning |
| --- | --- |
| `reaffirm` | The prior judgment still holds under the current conditions. |
| `revise` | Change the preference, scope or conditions while preserving the original option. |
| `reopen` | The alternatives or assumptions need a new comparison. |
| `investigate` | One specific uncertainty must be resolved before a disposition is stable. |
| `retain_with_limitation` | Keep the option only within the stated scope, with the limitation explicit. |
| `reject` | The evidence no longer supports the option. |
| `no_change` | The review itself warrants no durable change. |

Do not infer a disposition from a status label, a single positive observation or
an unchanged source. State the basis, the conditions that still apply, the
counterevidence and the claim ceiling.

## 3. Record the review

Author a source-attributed episode JSON. Stage or commit it first.

```json
{
  "review_id": "YYYY-MM-DD-short-review-slug",
  "actor": "the actual reviewing agent",
  "source_revision": "40-character Git commit SHA assessed by the review",
  "source_option": "arch:existing-option-id",
  "disposition": "reaffirm | revise | reopen | investigate | retain_with_limitation | reject | no_change",
  "basis": "why this disposition follows from the cited evidence",
  "conditions": "where the disposition applies",
  "counterevidence": "opposing observations or NOT_ASSESSED",
  "claim_ceiling": "what the review does not establish",
  "evidence_refs": ["file:tracked/evidence/path.md"],
  "consequence_refs": ["conseq:existing-prediction"],
  "assessment_refs": ["observation:existing-active-assessment"],
  "method_ref": "lesson:existing-method-precedent"
}
```

`source_option` must be an authored `arch:` alternative with an authored
preference. Every `consequence_ref` must belong to that option. Every
`assessment_ref` must resolve one of those consequences and must not be
`SUPERSEDED`. `method_ref` is optional and must name an authored lesson with a
method. `evidence_refs` must identify tracked source files.

```bash
sensemaking-skills semantic decision record \
  --repo . \
  --episode path/to/review-episode.json \
  --output .sensemaking/knowledge/decision-review-YYYY-MM-DD.json --json
sensemaking-skills semantic knowledge-proposal-check \
  --repo . --proposal .sensemaking/knowledge/decision-review-YYYY-MM-DD.json --json
```

The command creates an **unreviewed** `decision` claim and relations to the
option, cited predictions, assessments and method. It never overwrites the
option or its preference, commits, merges, changes standing or grants
permission. Ordinary Git review remains necessary.

## 4. Verify the consumer

After the proposal is reviewed and committed, `knowledge-audit` should show the
review under the decision link's `reviews`, and `knowledge-query explain` on the
option should return the decision claim and its evidence. The original option,
preference and assessments remain unchanged.

```text
review record       != automatic preference change
review record       != promotion or acceptance
review record       != causal benefit
review record       != independent-agent use
```

A later agent can inspect the review, the original evidence and any intervening
changes. It may reaffirm, revise, reopen, investigate, retain with limitation or
reject in turn; each review is a new attributed decision.
