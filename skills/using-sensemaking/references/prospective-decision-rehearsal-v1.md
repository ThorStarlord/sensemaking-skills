# Prospective Decision Rehearsal v1

**Status:** optional agent-facing reasoning procedure. It tests whether a
candidate possibility or construction path would change a real beneficiary
decision before the agent selects or builds it. It is not a new record type,
planner, ranker or mandatory stage.

## When to use

Use it when:

- a candidate possibility is coherent but its beneficiary value is unclear;
- two materially different possibilities or paths compete;
- a local improvement looks easy to justify but its effect on a real
  decision is uncertain;
- a retained `revisit_when` condition may have become consequential.

Skip it for a narrow, already-grounded task whose correct execution needs no
consequential value judgment. Do not rehearse every idea.

```text
coherent candidate != valuable candidate
feature difference != beneficiary decision delta
predicted delta  != observed benefit
NO_DELTA         != failed rehearsal
```

## Procedure

### 1. Recover the candidate as authored

Inspect the candidate's original source, not only a summary. For a retained
possibility, use the existing product context and ecology:

```bash
sensemaking-skills semantic workspace-query --operation product-outline \
  --include-candidates --json
sensemaking-skills semantic workspace-query --operation possibility-ecology \
  --subject <goal-or-possibility-id> --json
```

Read the authored dimensions, `value_hypothesis`, assumptions, related
capabilities, evidence, counterevidence and `revisit_when`. A missing field is
`NOT_ASSESSED`, not permission to invent one.

### 2. Check whether the candidate's trigger can fire

Identify the existing consumer or data shape the candidate says it would use or
extend. Run that consumer on a real revision pair or authored record set before
imagining the future behavior. For example:

```bash
sensemaking-skills semantic workspace-changes --repo . \
  --base-ref BASE --ref HEAD --json
sensemaking-skills semantic workspace-query --operation possibility-ecology \
  --subject <goal-or-possibility-id> --json
```

Check whether the fields the candidate depends on are populated and matchable.
A `revisit_when` sentence is not a typed claim/source reference. A changed
supporting-file fingerprint is not a semantic consequence. An unpopulated or
unmatchable trigger cannot fire.

If the trigger cannot fire, stop with `NO_DELTA` or `DEFER` and label the result
as a **data/shape limitation**. Do not treat it as evidence that the idea is
valueless; it may become testable when the required fields are authored. A
candidate whose trigger is unrepresented is not yet a buildable capability.

### 3. Recover a real beneficiary episode and current decision

Name a real person, agent, session or observed workflow and the decision it
actually faces now. A prior receipt, normal-use record or concrete current
decision can be the episode. Do not substitute a synthetic persona or an
imagined user for missing evidence; if no real episode exists, stop with
`NO_EPISODE` or investigate.

State the **current decision** in behavioral terms: what the beneficiary
actually does or chooses without the candidate.

### 4. Consult relevant experience when it could change the rehearsal

Use the existing consumers only when the candidate turns on an intellectual
procedure or a prior precedent:

```bash
sensemaking-skills semantic method context --question "<current decision>" \
  --repo . --ref HEAD --json
```

`method context` returns authored lessons, not applicability. If a precedent is
consulted, name the lesson or source, its source revision, the conditions it
states, contrary evidence, and whether you applied, adapted, combined, rejected
or ignored it. A miss is `NOT_ASSESSED`; there is no obligation to find a
lesson. For a prior episode or decision, read the relevant committed receipt or
normal-use record directly, or use the optional `summarize-receipts.py` reader
as a pointer; do not treat a receipt summary as the precedent. Record this in
the existing decision note or rehearsal note, not in a new schema field.

### 5. State the candidate decision and the delta

State the **candidate decision**: what the beneficiary would do differently
with the candidate. Then state the delta for that beneficiary in observable
terms.

If the current and candidate decisions are the same, or the difference is only
a new view, label, explanation or internal representation with no changed
beneficiary action, record `NO_DELTA` and stop. A `NO_DELTA` is a successful
outcome; it prevents low-value construction.

### 6. State the expected observation and failure condition

Name what would be observed, by whom, and how: a command, artifact, user
action, review decision or other bounded observation. State what would count
against the candidate and what cost or risk the rehearsal itself adds.

If no observation could distinguish the candidate from the current state, mark
`UNOBSERVABLE`; do not promote a prediction into evidence.

### 7. Decide and retain only what is useful

Choose one:

- **BUILD / SELECT** — the delta is plausible and the candidate is warranted;
- **DEFER** — the delta may matter but current evidence or timing is
  insufficient;
- **REJECT** — the candidate does not change a real decision or its cost
  exceeds the plausible value;
- **INVESTIGATE** — a bounded fact or episode could make the rehearsal
  discriminating.

If a commitment is warranted, use the existing `hypothesis`, `experiment-design`
or `method trial` capability. Do not create a parallel planning artifact. A
concise rehearsal note in the existing normal-use record or PR decision note is
enough when the decision or its `NO_DELTA` should survive.

## Worked shape

| Field | Example |
| --- | --- |
| Candidate | A new retrieval view over prior notes. |
| Beneficiary episode | A current agent choosing whether to build the view. |
| Current decision | Inspect the prior notes/ask an explorer. |
| Candidate decision | Query the view and choose from its candidates. |
| Expected delta | The view surfaces a prior precedent that changes the choice. |
| Failure condition | The same precedent was already available; the view only adds another surface. |
| Data check | The existing consumer's trigger fields are populated and matchable. |
| Disposition | `NO_DELTA` / `DEFER` / `BUILD`. |

The example is a shape, not a recommendation.

## Failure modes

- **Rehearsal theater:** a polished narrative with no real beneficiary or
  observable delta.
- **Convenient episode:** choosing an episode that makes the candidate look
  good rather than one that could falsify it.
- **Feature-to-benefit leap:** treating a new command, field or view as a
  changed decision.
- **Unfalsifiable delta:** "the agent will understand better" with no
  observation.
- **Precedent citation ritual:** naming a lesson without checking its source,
  conditions or contrary evidence.
- **Unpopulated trigger read as rejection:** treating a free-text or missing
  field as evidence that the candidate is worthless, rather than as a
  data/shape limitation.
- **Retrofit:** writing the rehearsal after the build and presenting it as the
  original decision.
- **Mandatory ceremony:** requiring a rehearsal for narrow or clear work.

## Evidence ceiling

A rehearsal establishes that an agent authored a candidate, a real beneficiary
episode, a current and candidate decision, and an expected observation. It does
not establish that the candidate will work, that the delta will occur, that the
method caused an outcome, or that another agent would benefit. Those remain
separate claims and, where comparative, separate qualification.
