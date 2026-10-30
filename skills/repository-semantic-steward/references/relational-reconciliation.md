# Relational Evidence Reconciliation (RELATE)

RELATE tests whether a relationship, capability, dependency, governing rule or
runtime behavior is established by the available evidence. It tests claims in
both directions: an absence the sources do not support, and a positive relation
or behavior that a record states more strongly than its sources show. The
`using-sensemaking` controller invokes RELATE before a recommendation, a
knowledge correction or an owner escalation rests on such a claim. RELATE
returns a verdict. The controller decides what the verdict changes. RELATE
never recommends, escalates or selects the next responsibility.

```text
graph miss                 != absence in the product
NOT_ASSESSED               != absent
declared, not exercised    != gap by itself
recorded relation          != established relation until its source supports it
constrains a support claim != constrains the implementation
```

## 1. When to run it

Run RELATE when the conclusion would change a recommendation, a priority, a
knowledge correction or an owner escalation, and it rests on one of:

- **absence:** "the product has no X", "nothing depends on Y", "no component
  reads Z";
- **positive relation or behavior:** "X is constrained by Y", "X reads Z at
  session start", "X depends on Y", "X has cardinality N:M", where the answer
  changes the choice or the record;
- **escalation:** "this is an architecture gap", "this needs an ADR", "this needs
  an owner decision".

Skip it for narrow mechanical work, for a fact that one inspected source at the
decisive revision already states, and for a claim about a file you are editing
now. A bounded search that settles the question is enough.

## 2. State the claim exactly

Write one line: `subject - relation - object - scope`. The scope names what was
examined: the product, a component, a contract, an artifact family or the
indexed revision. A claim without a scope is not a claim. Name its direction
(absence or positive) and, for a positive claim, the thing it says is constrained,
performed or consumed. That thing must be the subject, not the broad topic.

## 3. Graph-grounded retrieval

The reviewed graph is one layer. Use the existing semantic query operations.
Retrieval finds reviewed records. It cannot prove that a product lacks something,
and a hit is a record, not a source.

1. **Search by names and statements.** `search --term <t>` (repeat `--term` for an
   explicit OR, literal match). Include identifier variants as well as plain
   words: a literal search for "native harness" misses `native_harnesses`.
2. **Explain the neighbourhood.** `explain --subject <claim-id> --depth 1` lists
   the incident relations of a claim. `--expect-kind` assesses expected neighbour
   kinds inside that one-hop neighbourhood only. A neighbour kind absent beyond
   one hop is still `NOT_ASSESSED`.
3. **Read file-level records.** `context-for --subject <repository-relative path>`
   gives ownership, rules, linked contracts, decisions and tests for one file.
   `rules-for` gives architecture rules alone.
4. **Read the proposal under review.** Records in the working tree or in the same
   change set are not in a committed index. Read the authored
   `.sensemaking/knowledge/*.json` directly for them.

Record every retrieval: the query, the indexed revision, `workspace_context`
(`head_matches_indexed_ref`, `uncommitted_changes_not_indexed`) and the outcome.

| Outcome | Meaning |
| --- | --- |
| hit | relevant reviewed records found at the indexed revision |
| miss | no relevant reviewed record at a current indexed revision |
| unavailable | no index, a stale index, or uncommitted changes touching the subject |

A **miss** is a fact about the reviewed graph at that revision, nothing more. An
**unavailable** result is `NOT_ASSESSED`, not a miss. In both cases the authored
records and the original sources are the fallback.

## 4. Cross-layer source reconciliation

Check the layers below in order. Stop when the question is settled for its stated
scope. Each layer answers a different question, and a miss in one layer does not
settle another.

| Layer | What to look for | What it establishes |
| --- | --- | --- |
| Governing decisions | accepted and proposed ADRs, product scope and status documents that name the subject | intent, scope and ratification status |
| Declared contract | the schema, template, release file or reference that defines the field, interface, promise or boundary | what is declared, under what condition, and what kind of promise it is (section 5) |
| Validators and tests | the machine check that reads or writes the field | what machinery enforces |
| Implementation and consumers | `grep` over `src/` and `scripts/` for the identifier; the code path that performs the behavior, including its trigger | what is implemented, and whether a runtime consumer exists |
| Recorded use | receipts, PRs, qualification evidence, example outputs | what has been observed in use |
| Prior syntheses | architectural syntheses, earlier observations and their superseded notes | what earlier reasoning concluded, and whether it is still current |

Rules:

- **Read the artifact's own contract.** If the artifact being written or reviewed
  has a field for the relation, that field's contract is in scope. A step that
  writes `campaign_ref: null` while concluding that no pointer exists has not read
  the contract it is filling in.
- **Name the search scope.** "No `src/` reader at `<sha>`, searched with `grep`
  over `src/` and `scripts/`" is bounded. "No reader" is not.
- **Declared is not exercised, and exercised is not declared.** Keep both
  observations separately.
- **Check the trigger, not only the verb.** A runtime behavior needs its trigger as
  well as its action. "Reads at session start" is implemented only if something
  executes at session start.

## 5. Profile and assessment

A verdict is a **profile** over four cells, not a single class. Each cell carries
its evidence reference. A mixed profile is a normal result, not a conflict.

| Cell | Values |
| --- | --- |
| **declared** | the promise kind (below) and its source status (ratified, observed, proposed); or `none in scope`; or `not assessed` |
| **implemented** | `yes` (the behavior and its trigger, at the revision); `partial` (some of the promise); `no` (the inspected scope has no such path); `not assessed` |
| **exercised** | `yes` (a runtime consumer or recorded use performs it); `none in scope`; `not assessed` |
| **graph** | `recorded`, `miss` or `unavailable`, at the indexed revision |

**Promise kinds.** The declared cell says what kind of statement the source makes.
The kind decides which gap test applies.

| Promise kind | What the source states | Gap test |
| --- | --- | --- |
| `runtime_behavior` | the system does X when Y happens | promised behavior absent from the inspected implementation is an `IMPLEMENTATION_GAP` candidate |
| `support_boundary` | what the product may claim as supported, or excludes until evidence exists | not a gap. It limits claims. Implementation beyond it is a `BOUNDARY` finding |
| `optional_affordance` | a field, option or pointer the contract allows | not a gap when unused; `exercised: none` is expected |
| `definition` | what a term, field or artifact means | checks consistency only; no runtime test |
| `guidance` | what an agent should do (Skill text, process instruction) | governs agent behavior, not product runtime; missing execution is not an implementation gap |

**Assessment.** One label for the claim as stated, derived from the profile:

| Assessment | When the profile shows | Receipt `epistemic_status` |
| --- | --- | --- |
| `HOLDS` | the claim, as stated, matches the cells its promise kind requires | `RATIFIED` if the source is an accepted decision, else `OBSERVED` |
| `OVERSTATED` | the claim asserts more than the profile supports. Positive direction: a relation or behavior with no source or implementation to match. Negative direction: an absence that a declared source or implementation contradicts | `CONTRADICTED`, naming the source |
| `ABSENT_IN_SCOPE` | an absence holds in every named layer of the stated scope, and the graph miss is not the only evidence | `OBSERVED`, with the scope in the statement |
| `BOUNDARY` | a support boundary limits what may be claimed; implementation may exceed it | `RATIFIED` or `OBSERVED` by source status |
| `IMPLEMENTATION_GAP` | a `runtime_behavior` promise is in scope and the implemented cell is `no` or `partial` at the inspected revision | `OBSERVED`, scoped; a candidate until the residue check (section 7) |
| `UNRESOLVED` | a relevant cell is `not assessed`, or sources conflict | `UNRESOLVED` |

Rules:

- A graph miss is a retrieval outcome. It never yields `ABSENT_IN_SCOPE` alone.
- An absence assessment always carries its scope: "absent in `src/` and the
  session-receipt contract at `<sha>`", never "absent".
- `OVERSTATED` is a finding about a claim or record. The fix is a source or
  knowledge correction, not a product gap.
- `IMPLEMENTATION_GAP` is a candidate about the product, scoped to its revision.
  It still needs the residue check before anyone acts on it.
- A `declared` runtime promise never yields `HOLDS` without the implemented and
  exercised cells that the promise requires.
- A `guidance` promise never yields `IMPLEMENTATION_GAP`.

## 6. Relation review: predicate and direction

Apply this section whenever a verdict depends on a relation, or whenever a
relation would be recorded or corrected. It applies the existing vocabulary in
[knowledge contract](knowledge-contract.md) and ADR 0033.

1. **The subject is the thing constrained, performed or consumed.** A relation
   about a broad topic (the installer, the whole product) does not inherit a
   constraint that applies to one of its claims.
2. **`constrained_by` binds the subject's own claims or behavior** to a
   `constraint` or `invariant` claim. Reviewed records use it with those object
   kinds. A support boundary constrains the claims the product may make. It does
   not constrain code that goes beyond the boundary, so that code is related by
   `references`, not `constrained_by`.
3. **`implemented_by` links a capability to the component that realizes it.**
   An implementation that touches a declared boundary without being bound by it
   is a `references` relation with `attributes.conceptual_relation` (for example
   `implementation_outside_declared_support`).
4. **`relates_to` expresses domain-concept cardinality.** ADR 0033 defines it
   with a required `cardinality`, and the product possibility ontology says it was
   introduced for domain-concept cardinality, not for other relations. A
   contract's field pointer to a component is a one-way reference. Record it as
   `references` with `conceptual_relation` and the field name. Do not record a
   `cardinality` the source does not state.
5. **Record the direction the source states.** A pointer runs from the
   contract that defines it to the state it names.
6. **Change a predicate only when the current one asserts a constraint, dependency
   or cardinality the source does not state.** Stylistic preference is not a
   reason.

## 7. Residue authority and escalation

After the profile and assessment, what remains unresolved has one authority kind.
Assign it before anyone asks the owner. The categories map onto the controller's
Escalate routing.

| Residue authority | Controller routing | Meaning |
| --- | --- | --- |
| `none` | correct the premise | the profile settles the proposition; any `OVERSTATED` record needs correction |
| `source_inspection` | inspect; do not ask | a bounded check would settle it: a code path, a consumer, a contract |
| `ratification` | draft for the ADR or owner-decision path | the outcome would create a commitment: a boundary, rule, contract or hook |
| `owner_intent` | `owner-decision-capsule` | several governed alternatives remain, and only the owner can choose |
| `authority_boundary` | stop at the boundary | the next step is a protected action: publish, merge, release, external |

RELATE prevents unnecessary escalation when a verdict is `OVERSTATED`,
`ABSENT_IN_SCOPE` or `HOLDS`, or when the residue is `source_inspection`. It does
not prevent necessary escalation: `owner_intent` and `ratification` residue stay
with their owners even when the graph is silent.

Examples from this repository, as checked in this refinement:

- *Does a session-start hook read receipts?* Residue `none`. Nothing executes at
  session start, so the claim is `OVERSTATED`. Correct the record.
- *Is `summarize-receipts.py` run automatically?* Residue `source_inspection`.
  Searching `scripts/`, `.claude/` and the repository's other tooling finds no
  automatic caller. It is optional and agent-invoked. Settled without asking.
- *Should a session-start hook be added?* Residue `ratification`. An executable
  hook would change the orchestration boundary, which the repository's current
  boundary documents do not allow. Draft it for the ADR or owner-decision path.
- *Should the 1.0 promise include native harness discovery?* Residue
  `owner_intent`. The release records the condition for change. Escalate only
  if the owner wants to change the promise.
- *Should receipts be mandatory under the proposed ADR 0032?* Residue
  `ratification`. ADR 0032 is `PROPOSED`, and its ratification is owner-reserved.

## 8. Knowledge reconciliation

1. Check whether the reviewed graph at the indexed revision records the relation.
   If not, state that plainly. If it does, check whether the record states more
   than its governing and implementing sources show.
2. Decide whether reviewed knowledge should change. Reconcile when a later agent
   asking the same question would receive an incorrect, incomplete or overstated
   answer. Otherwise return `NO_MODEL_CHANGE` with the reason.
3. A correction names what it changes: the predicate, the object, the
   attributes, or the statement. The earlier revision stays in Git history.
4. Preserve epistemic status and source identity. Put the source that establishes
   the relation in `evidence_refs`.
5. Do not turn an ADR's silence into a relation, and do not turn a graph miss into
   a claim of absence.
6. Proposed records go through `semantic knowledge-proposal-check` and the normal
   reviewed Git change. A proposal is a draft until it is reviewed.

## 9. Verdict returned to the controller

Return one block in the report or as a receipt finding. No new artifact type is
needed.

```text
RELATIONAL_VERDICT
claim:      <subject - relation - object - scope; direction: absence | positive>
profile:
  declared:    <promise kind; source status; references | none in scope | not assessed>
  implemented: <yes | partial | no | not assessed; code references; revision>
  exercised:   <yes | none in scope | not assessed; consumer or recorded use>
  graph:       <recorded | miss | unavailable; indexed revision; workspace context>
assessment: <HOLDS | OVERSTATED | ABSENT_IN_SCOPE | BOUNDARY | IMPLEMENTATION_GAP | UNRESOLVED>
residue:    <what remains; authority: none | source_inspection | ratification | owner_intent | authority_boundary>
affects:    <the recommendation, correction or escalation this changes>
knowledge:  <reconcile (which records, what change) | NO_MODEL_CHANGE (reason)>
limits:     <what remains NOT_ASSESSED or UNRESOLVED>
```

The verdict is evidence for the controller. The controller decides.

## 10. Worked cases

These cases come from the `sensemaking-skills` repository. They show the
procedure, not a reusable answer.

### Case A: receipt-to-Campaign pointer (absence, overstated)

- **Claim:** session receipts have no defined relation to Campaign state. Scope:
  the product. Direction: absence. The completion receipt recorded it as an owner
  question.
- **Profile:**
  - declared: `session-receipt-v1.md` defines `continuity.campaign_ref`, an
    `optional_affordance` (section 3 field; section 7 says to point to Campaign
    state with it). ADR 0029 places optional Campaign persistence in scope. ADR
    0032 (`PROPOSED`) says the receipt points to a Campaign.
  - implemented: the validator checks its shape and, with `--target-repo`, its
    existence. No `src/` module reads or writes it.
  - exercised: `none in scope`. Every committed session receipt holds `null`.
  - graph: `miss` at `db821c25`, before the correction.
- **Assessment:** `OVERSTATED`, negative direction. The declared contract contradicts
  the absence. The graph miss was real but insufficient.
- **Residue:** `none`. The owner question was unnecessary and is withdrawn.
- **Knowledge:** reconcile the pointer relation (done in this refinement; see the
  receipt).

### Case B: native-harness support (absence, boundary)

- **Claim:** the product has no native harness relationship. Scope: the release
  support surface and the installer. Direction: absence.
- **Profile:**
  - declared: `release-v1.0.yaml` states a `support_boundary`. Native harness
    discovery and invocation are excluded from the 1.0 support promise until real
    harness evidence exists. ADR 0028 assigns installation and discovery to
    adapters.
  - implemented: `harness_adapters.py` maps the `claude`, `codex`, `opencode` and
    `generic` targets to discovery roots, with no runtime detection. The
    installer's `distribution-setup` component describes that mapping.
  - exercised: `none in scope` for native loading.
  - graph: `recorded` for the release observation and the installer component.
    The link between them was missing until the earlier reconciliation.
- **Assessment:** the absence claim is `OVERSTATED`. The accurate statement is
  `BOUNDARY`: a declared exclusion over implemented install destinations, with no
  runtime evidence.
- **Residue:** `owner_intent` only if the owner wants to change the 1.0 promise.
  Nothing in the current support question needs an owner decision.
- **Knowledge:** reconcile. The exclusion constrains supported claims. It does not
  constrain the installer's behavior, so the link is a `references` relation, not
  `constrained_by` (see Case D).

### Case C: session-start receipt reading (positive, overstated)

- **Claim:** `component:receipt-validator` "reads [receipts] at session start".
  Scope: the validator and the repository's session-start machinery. Direction:
  positive.
- **Profile:**
  - declared: the controller's Skill text, a `guidance` promise. It tells an
    agent to read relevant receipts when resuming work, using an optional script.
  - implemented: the validator does not read receipts at session start. Its code
    checks a file it is given. `.claude/settings.json` is `{}`, and
    `.claude/hooks/sessionstart.md` says nothing runs at session start.
  - exercised: `none in scope` for an automatic session-start read.
- **Assessment:** `OVERSTATED`, positive direction. The record attributes a
  runtime trigger that the sources contradict. Because the promise kind is
  `guidance`, this is not an implementation gap.
- **Residue:** `none`. Correct the record.
- **Knowledge:** reconcile. The statement now says what executes (nothing at
  session start) and what the Skill directs.

### Case D: `constrained_by` on the installer (positive, direction error)

- **Claim:** `component:distribution-setup` is `constrained_by`
  `observation:release-declares-no-native-harness`. Direction: positive.
- **Profile:**
  - declared: the release excludes native discovery and invocation from the
    support promise. Its scope is supported claims.
  - implemented: the installer writes to the `claude`, `codex` and `opencode`
    roots. The release does not forbid this. It only fails to promise it.
- **Assessment:** `OVERSTATED`, positive direction. The constraint binds claims
  about support, not the installer's behavior. The predicate asserts a
  constraint the source does not state.
- **Residue:** `none`. Correct the predicate.
- **Knowledge:** reconcile. The relation becomes `references` with
  `conceptual_relation: implementation_outside_declared_support`. The exclusion
  records that it `constrains` supported claims.

### Case E: pointer cardinality (positive, overstated)

- **Claim:** the receipt contract `relates_to` the Campaign core with `N:M`
  cardinality.
- **Profile:** the contract defines one optional pointer per receipt. It does
  not state a many-to-many cardinality. ADR 0033 scopes `relates_to` to
  domain-concept cardinality.
- **Assessment:** `OVERSTATED`, positive direction (cardinality and predicate).
- **Knowledge:** reconcile. The relation becomes `references` with the pointer
  field and direction, with no cardinality.

## 11. Method notes

- RELATE is proportionate. Two or three layers often settle a claim. Most
  verdicts need the declared contract, the decisive implementation search and
  one retrieval.
- Positive claims are cheap to test. Read the verb in the cited source, check its
  trigger, and check the subject. Cases C and D were settled this way.
- A helper script is not required. The retrieval and search operations exist. A
  scripted absence check over one layer would sound like a product-wide claim,
  which is the reading this procedure forbids.
