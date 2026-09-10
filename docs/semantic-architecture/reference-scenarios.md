# Reference Scenarios

**Status:** Canonical semantic-architecture evaluation scenarios, v0  
**Purpose:** Test whether the ontology and reasoning model improve real Sensemaking work.

These scenarios are not unit tests yet. They are semantic acceptance cases. Future executable work should prefer turning stable mechanical portions into fixtures rather than simulating semantic judgment.

## Scenario A — Architecture drift

### Situation

An ADR states:

```text
presentation may depend on application
application may depend on domain
domain must not depend on infrastructure
```

Current source contains:

```text
domain/order.py imports infrastructure/database.py
```

### Required semantic representation

```text
Observation O1:
  domain/order.py imports infrastructure/database.py
  status = OBSERVED
  target = S1

Ratified claim C1:
  domain must not depend on infrastructure
  status = RATIFIED
  source = ADR

Inferred architectural memberships:
  order.py belongsToLayer domain
  database.py belongsToLayer infrastructure

Derived relation:
  dependency crosses domain/infrastructure boundary

Contradiction K1:
  observed dependency conflicts with ratified dependency rule
```

### Decision-changing uncertainty

Is the direct dependency intentional transitional compatibility code, or unintended architecture drift?

### Invalid shortcut

```text
import exists -> automatically repair architecture
```

### Competency coverage

CQ-020, CQ-021, CQ-024, CQ-032, CQ-033, CQ-037, CQ-041.

---

## Scenario B — Missing product capability versus missing implementation

### Situation

README advertises a `campaign export` capability, but no CLI command or runtime implementation is found.

### Required distinction

```text
ProductCapability claim:
  user can export Campaign

Documentation evidence:
  README states export exists

Repository observations:
  no command found in complete CLI registration scope
  no implementation found in declared package scope
```

If the search/probe contract is complete enough, the system may derive a bounded absence claim for those scopes.

### Possible interpretations

- ghost feature: documentation claims a capability not implemented;
- implementation exists through another surface not yet inspected;
- feature was removed but docs are stale;
- worktree/branch mismatch.

### Required behavior

Represent uncertainty rather than immediately choosing one explanation.

### Competency coverage

CQ-017, CQ-026, CQ-035, CQ-036, CQ-067, CQ-068.

---

## Scenario C — Documentation/code contradiction

### Situation

`STATUS.md` says a milestone is blocked, but current code and CI evidence show the implementation was merged after that status update.

### Semantic representation

```text
Documentation claim C1
  applies to time T1

Repository/CI evidence E2
  applies to later target snapshot T2

Result:
  contradiction may be temporal/staleness rather than implementation failure
```

### Required reasoning

The agent should ask which source is current and authoritative for which claim instead of treating either prose or code as globally authoritative.

### Competency coverage

CQ-007, CQ-010, CQ-036, CQ-037, CQ-067, CQ-068, CQ-070.

---

## Scenario D — Failed repair despite changed repository

### Situation

A bug is diagnosed, files are modified, tests execute, but the original reproducer still fails.

### Semantic representation

```text
Change CH1 modifies files A/B
  status = OBSERVED/DERIVED from target diff

Validation V1
  generic unit suite passed

Validation V2
  original reproducer failed

Claim C1:
  repository changed
  status = DERIVED

Claim C2:
  targeted bug repaired
  status = CONTRADICTED / UNRESOLVED
```

### Required invariant

```text
repository changed != repair succeeded
```

### Competency coverage

CQ-054 through CQ-060.

---

## Scenario E — Product enhancement proposal

### Situation

Sensemaking already persists Campaign state. A Resume Capsule is proposed to make fresh-context continuation easier.

### Product ontology representation

```text
ProductCapability:
  durable fresh-context continuation

Existing feature:
  Campaign persistence / handoff

ProductChange:
  Resume Capsule

Structural type:
  enhancement + UX improvement

Value mechanisms:
  deepen + simplify

Value relation:
  complementary / reinforcing
```

### Required invariant

These labels describe the proposal but do not imply it should be prioritized or implemented.

### Competency coverage

CQ-061 through CQ-066.

---

## Scenario F — Fresh-context continuation

### Situation

Agent A ends after performing an architectural review. Agent B starts without access to Agent A's conversation.

### Durable state available

- mission;
- TargetSnapshot;
- active Responsibility;
- active Uncertainty;
- evidence artifacts;
- architectural claims and their status;
- contradiction still unresolved;
- authority;
- recent TransitionRecords.

### Required behavior

Agent B should reconstruct:

```text
what is known
what is inferred
what is contradicted
what remains uncertain
what responsibility is active
why it is active
what authority applies
```

without recreating already completed investigation merely because prior chat is unavailable.

### Invalid shortcut

A deterministic handoff generator must not invent the next semantic action.

### Competency coverage

CQ-073 through CQ-078.

---

## Scenario G — Passing test with insufficient claim coverage

### Situation

A unit test verifies that a serializer emits a field. A Skill concludes that the full public API compatibility contract is satisfied.

### Required representation

```text
Observation:
  test T passed

Evidence claim:
  serializer field behavior covered

Overstated claim:
  public API compatibility fully satisfied
```

The ontology should make the coverage mismatch visible.

### Required invariant

```text
passing test != every broader behavior claim proven
```

### Competency coverage

CQ-027, CQ-028, CQ-029, CQ-032, CQ-038.

---

## Scenario H — Capability available but unauthorized

### Situation

The agent determines that a migration is warranted. A repository-mutating capability exists, but current authority is read-only.

### Representation

```text
Responsibility R1 = migration planning / execution boundary
Capability C1 available = true
Capability C1 mutates repository = true
Authority = owner authorization required
```

### Correct outcome

The system may report the capability as available while refusing to treat execution as authorized.

### Required invariant

```text
warranted responsibility != available capability != authorized capability
```

### Competency coverage

CQ-004, CQ-005, CQ-047 through CQ-053.

---

## Scenario I — Absence claim from incomplete search

### Situation

A text search for `FooService` returns no matches. The agent concludes there is no implementation of the Foo capability.

### Required response

Represent the search as evidence but reject the stronger absence inference unless the search/probe contract establishes complete coverage of all relevant representations.

Potential hidden implementations include:

- alternate naming;
- generated code;
- configuration-based registration;
- dynamic import;
- external service;
- different branch/state.

### Competency coverage

CQ-015, CQ-017, CQ-035, CQ-036.

---

## Scenario J — Vocabulary drift across Skills

### Situation

One Skill uses `capability` to mean target-software behavior. Another uses it to mean available agent tool/Skill. A third means product value.

### Required resolution

Normalize to:

```text
SoftwareCapability
SensemakingCapability
ProductCapability
```

and preserve legacy names only as historical provenance where needed.

### Competency coverage

CQ-069, CQ-070, CQ-071, CQ-072.

---

## Scenario K — Multi-source contradiction without premature resolution

### Situation

Static code suggests path A, runtime logs demonstrate path B, and documentation describes path C.

### Required reasoning

The model should preserve three source-scoped claims, inspect temporal/environmental scope, and identify the consequential uncertainty. It should not normalize all evidence to whichever source the current Skill prefers.

### Competency coverage

CQ-030, CQ-034, CQ-037, CQ-040, CQ-041.

---

## Scenario L — Enabler mistaken for customer-facing feature

### Situation

A Skill Contract Manifest is proposed and described as a "new user feature."

### Required product reasoning

Classify the change primarily as:

```text
ProductChange
structural type = enabler/platform capability
value mechanism = enable + harden
primary target = future development / capability contract consistency
```

Then separately identify what downstream user capabilities it is expected to improve or enable.

### Competency coverage

CQ-061 through CQ-066.

## Evaluation rule

The semantic architecture should be considered stronger when these scenarios can be described **with fewer ambiguous terms, clearer evidence lineage, and fewer hidden inference jumps**.

A scenario does not pass merely because the ontology can name every object. It passes when the model improves the quality and reconstructibility of the decision.