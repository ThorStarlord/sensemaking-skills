# Relational Evidence Reconciliation (RELATE)

RELATE is the Steward's responsibility for checking whether a **relationship,
capability, dependency or governing rule** is established by the available
evidence. The `using-sensemaking` controller invokes it when a consequential
conclusion rests on an absence or on a relation the reviewed graph does not
settle. RELATE returns a verdict. The controller decides what the verdict
changes. RELATE never recommends, escalates or selects the next responsibility.

```text
graph miss                 != absence in the product
NOT_ASSESSED               != absent
declared but unexercised   != absent
declared exclusion         != capability gap
```

## 1. When to run it

Run RELATE when the conclusion would change a recommendation, a priority or an
owner escalation, and it rests on one of:

- **absence:** "the product has no X", "nothing depends on Y", "no component
  reads Z", "no defined rule covers W";
- **relation:** "X points to, depends on or is governed by Y", when the answer
  decides the choice;
- **escalation:** "this is an architecture gap", "this needs an ADR", "this needs
  an owner decision".

Skip it for narrow mechanical work, for a fact that one inspected source at the
decisive revision already states, and for a claim about a file you are editing
now. A bounded search that settles the class is enough. Stop there.

## 2. State the claim exactly

Write one line: `subject - relation - object - scope`. The scope names what was
examined: the product, a component, a contract, an artifact family or the indexed
revision. A negative claim without a scope is not a claim. Name its kind:
presence, absence, direction or governance.

## 3. Graph-grounded retrieval

The reviewed graph is one layer. Use the existing semantic query operations.
Retrieval finds reviewed records; it cannot prove that a product lacks something.

1. **Search by names and statements.** `search --term <t>` (repeat `--term` for
   an explicit OR, literal match). Include the likely identifiers: contract,
   component and field names, not only plain-language words.
2. **Explain the neighbourhood.** `explain --subject <claim-id> --depth 1` lists
   the incident relations of a claim. `--expect-kind` assesses expected neighbour
   kinds inside that one-hop neighbourhood only. A neighbour kind that is absent
   beyond one hop is still `NOT_ASSESSED`.
3. **Read file-level records.** `context-for --subject <repository-relative path>`
   gives ownership, rules, linked contracts, decisions and tests for one file.
   `rules-for` gives architecture rules alone.
4. **Read the proposal under review.** Reviewed records in the working tree or in
   the same change set are not in a committed index. Read the authored
   `.sensemaking/knowledge/*.json` directly for them.

Record every retrieval: the query, the indexed revision, `workspace_context`
(`head_matches_indexed_ref`, `uncommitted_changes_not_indexed`) and the outcome.

| Outcome | Meaning |
| --- | --- |
| hit | relevant reviewed records found at the indexed revision |
| miss | no relevant reviewed record at a current indexed revision |
| unavailable | no index, a stale index or uncommitted changes touching the subject |

A **miss** is a fact about the reviewed graph at that revision, nothing more.
An **unavailable** result is `NOT_ASSESSED`, not a miss. In both cases, the
authored records and the original sources are still the fallback.

## 4. Cross-layer source reconciliation

Check the layers below in order. Stop when the question is settled for its
stated scope. Each layer answers a different question, and a miss in one layer
does not settle another.

| Layer | What to look for | What it establishes |
| --- | --- | --- |
| Governing decisions | accepted and proposed ADRs, product scope and status documents that name the subject | intent, scope and ratification status |
| Declared contract | the schema, template or reference that defines the field, interface or artifact | what is declared, and under what condition |
| Validators and tests | the machine check that reads or writes the field | what machinery enforces |
| Implementation and consumers | `grep` over `src/` and `scripts/` for the identifier; readers and writers | what is implemented and exercised |
| Recorded use | receipts, PRs, qualification evidence, example outputs | what has been observed in use |
| Prior syntheses | architectural syntheses, earlier observations and their superseded notes | what earlier reasoning concluded, and whether it is still current |

Rules:

- **Read the artifact's own contract.** If the artifact being written or reviewed
  has a field for the relation, the field's contract is in scope. A reasoning
  step that writes `campaign_ref: null` while concluding that no pointer exists
  has not read the contract it is filling in.
- **Name the search scope.** "No `src/` reader at `<sha>`, searched with
  `grep` over `src/` and `scripts/`" is a bounded statement. "No reader" is not.
- **Declared is not exercised, and exercised is not declared.** Keep both
  observations. An unexercised declaration does not become absence, and a
  working code path with no governing declaration is an implementation fact that
  still needs its status stated.

## 5. Classify the claim

Use one class in the verdict. The classes map onto the receipt's existing
`epistemic_status` values, so the session receipt schema does not change.

| Class | Meaning | Receipt `epistemic_status` |
| --- | --- | --- |
| `DECLARED` | a governing or contract source states the relation or capability | `RATIFIED` if in an accepted decision, else `OBSERVED` |
| `IMPLEMENTED` | code implements the relation or capability | `OBSERVED` |
| `EXERCISED` | recorded use or a runtime consumer shows it | `OBSERVED` |
| `DECLARED_EXCLUSION` | a governing source excludes or defers it, with a stated condition | `RATIFIED` if in an accepted decision, else `OBSERVED` |
| `ABSENT_FROM_GRAPH` | retrieval missed at a current indexed revision; sources not yet checked | `UNRESOLVED` |
| `NOT_ASSESSED` | the decisive layer was not inspected, or retrieval was unavailable or stale | `UNRESOLVED` |
| `UNSUPPORTED_IN_SCOPE` | every named layer within the stated scope was inspected and none supports the claim | `OBSERVED`, with the scope in the statement |
| `CONTRADICTED` | an existing source says otherwise | `CONTRADICTED` |
| `UNRESOLVED` | sources conflict, or the remaining question is a choice among governed alternatives | `UNRESOLVED` |

Rules for the classes:

- `ABSENT_FROM_GRAPH` and `NOT_ASSESSED` never support a product-level "no".
  Recommendations may say only "not recorded in the reviewed graph at `<sha>`"
  or "not assessed in `<layer>`".
- `UNSUPPORTED_IN_SCOPE` is always scoped: "unsupported in `src/` and the
  session-receipt contract at `<sha>`", never "unsupported".
- A support surface declared narrower than the implementation is a boundary
  finding, not a missing capability. Report both sides.
- Escalate only when the verdict is `UNRESOLVED` because a choice between
  governed alternatives remains. A verdict of `ABSENT_FROM_GRAPH`,
  `NOT_ASSESSED`, or a declaration that is merely unexercised is not an owner
  question.

## 6. Relationship reconstruction and reviewed knowledge

For each relation the layers establish:

1. Check whether the reviewed graph at the indexed revision records it. If not,
   state that plainly.
2. Decide whether reviewed knowledge should change. Reconcile when a later agent
   asking the same question would receive an incorrect, incomplete or
   mislabelled answer. Otherwise return `NO_MODEL_CHANGE` with the reason.
3. Preserve epistemic status and source identity. Use the existing predicate
   vocabulary from [knowledge contract](knowledge-contract.md). Put the source
   that establishes the relation itself in `evidence_refs`.
4. Do not turn an ADR's silence into a relation, and do not turn a graph miss into
   a claim of absence.
5. Proposed records go through `semantic knowledge-proposal-check` and the normal
   reviewed Git change. A proposal is a draft until it is reviewed.

## 7. Verdict returned to the controller

Return one block, in the report or as a receipt finding. No new artifact type is
needed.

```text
RELATIONAL_VERDICT
claim:     <subject - relation - object - scope>
class:     <one class from section 5>
retrieval: <queries run; hit | miss | unavailable; indexed revision; workspace context>
layers:    <layers inspected, with paths and revision; layers not inspected>
affects:   <the recommendation, priority or escalation this verdict changes>
knowledge: <reconcile (which records) | NO_MODEL_CHANGE (reason)>
limits:    <what remains NOT_ASSESSED or UNRESOLVED>
```

The controller reads the verdict, decides what changed and then continues,
stops or escalates. A verdict is evidence for that decision, not the decision.

## 8. Worked cases

These cases come from the `sensemaking-skills` repository. They show the
procedure, not a reusable answer.

### Case A: receipt-to-Campaign pointer

- **Claim:** session receipts have no defined relation to Campaign state.
  Scope: the product. Kind: absence. The completion receipt of 2026-10-30
  recorded it as an owner question (Q-1: decide the relation in an ADR).
- **Retrieval:** at the indexed revision before the correction (`db821c25`), the
  reviewed graph had no relation between the receipt contract and the Campaign
  core. This is `ABSENT_FROM_GRAPH`, which is true and also insufficient.
- **Layers:**
  - Declared contract: `session-receipt-v1.md` defines `continuity.campaign_ref`
    as an optional repository-relative path, and section 7 says to point to
    Campaign state with it rather than duplicate it. `DECLARED`.
  - Governing decisions: ADR 0029 places optional durable Campaign state within
    current product scope. ADR 0032 (PROPOSED) says the receipt points to a
    Campaign when continuation complexity warrants one. `DECLARED`, with status
    `PROPOSED` for ADR 0032.
  - Validator: `validate-receipt.py` checks the pointer's shape and, with
    `--target-repo`, its existence. Validation.
  - Implementation: no `src/` module reads or writes `campaign_ref`. Every
    committed session receipt holds `null`. The pointer is `DECLARED` but not
    `EXERCISED`.
- **Verdict:** the relation is declared and unexercised. The graph miss was a
  knowledge gap. The product question was already answered by the contract, so
  the owner escalation was unnecessary.
- **Knowledge:** reconcile. The reviewed relation between the receipt contract
  and the Campaign core existed only after the correction. Its evidence should
  name the governing contract (the pointer field and section 7) and ADR 0032, and
  record the pointer field and the unexercised status.

### Case B: native-harness support

- **Claim:** the product has no native harness relationship. Scope: the release
  support surface and the installer. Kind: absence.
- **Retrieval:** the reviewed graph held an observation that the release declares
  an empty `native_harnesses` list, and a `distribution-setup` component that
  describes the installer's explicit host-to-root mapping. No relation linked the
  two. A literal search for "native harness" returned nothing, because the graph
  writes the identifier as `native_harnesses`. Search for identifier variants too.
- **Layers:**
  - Declared exclusion: `release-v1.0.yaml` declares `native_harnesses: []` and
    excludes native harness discovery and invocation from the 1.0 support promise
    "until real harness evidence exists". `DECLARED_EXCLUSION`.
  - Governing decisions: ADR 0028 assigns installation, discovery and native
    invocation evidence to adapters. `DECLARED`.
  - Implementation: `harness_adapters.py` maps explicit targets (`claude`,
    `codex`, `opencode`, `generic`) to user and project discovery roots, and
    performs no runtime detection. `IMPLEMENTED` as install destinations, not
    `EXERCISED` as native loading.
- **Verdict:** the claim "no native harness" is wrong as stated. The accurate
  class is a declared exclusion over implemented install roots, with no runtime
  evidence. It is not a capability gap that needs an owner decision. Changing the
  1.0 promise would be an owner decision, and the release names the condition
  under which it could change.
- **Knowledge:** reconcile. Record the exclusion's condition on its observation,
  and link the installer component to it with `constrained_by`. A later agent
  asking "does Sensemaking support Claude Code?" then gets the precise answer:
  install destinations exist, and native support is excluded until evidence exists.
## 9. Method notes

- RELATE is proportionate. Two or three layers often settle a claim. Most
  verdicts need the declared contract, the decisive implementation search and one
  retrieval.
- A helper script is not required for this procedure. The retrieval and search
  operations already exist. A new mechanical check for "absence" would invite the
  reading this procedure forbids: a scripted search over one layer would sound
  like a product-wide claim.
