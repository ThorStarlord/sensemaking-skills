# Semantic Reasoning Profile

**Status:** Phase 9 pilot instrument  
**Authority:** Comparative reasoning evidence only; not a semantic truth engine  
**Purpose:** Make the canonical Reasoning Model observable across contrasting Skills without forcing every Skill into one domain artifact schema.

## Why this exists

Phase 9 tests whether the shared semantic architecture improves real Skill reasoning. The profile is a companion record: it does not replace a Skill's canonical artifact and it does not become Campaign state automatically.

The profile makes hidden reasoning boundaries visible:

```text
Target/currentness
-> Observations
-> Claims + epistemic status
-> Contradictions / uncertainty
-> Responsibility
-> Capability + authority
-> Result
-> Mechanical validation
-> Semantic evaluation
-> Decision
-> Explicit limits
```

Not every stage must be populated in every pilot. The required comparison core is intentionally smaller: target/currentness, observations, material claims, uncertainty, and explicit limits.

## Review template

### 1. Target and currentness

Record the exact repository/snapshot or inherited artifact state used by the Skill. Do not write `current` unless the access method actually establishes currentness.

Questions:

- What target was analyzed?
- What exact ref/snapshot bounded the analysis?
- Was currentness directly measured, pinned, inherited from an upstream artifact, or unverified?
- Which evidence establishes that boundary?

### 2. Observations

List direct or mechanically derived observations before interpretation.

Examples:

```text
OBSERVATION O1
statement: package A imports package B
method: direct_read
source: src/a.py
```

Do not encode `bad architecture`, `wrong component`, `successful repair`, or similar semantic judgments as observations.

### 3. Material claims

For every decision-changing claim, record:

```text
claim id
statement
scope
epistemic status
evidence refs
limits / non-claims
```

Canonical pilot statuses:

```text
OBSERVED
DERIVED
INFERRED
HYPOTHESIZED
RATIFIED
CONTRADICTED
SUPERSEDED
UNRESOLVED
```

A status describes how the claim is warranted, not a probability that the claim is true.

### 4. Contradictions

Record material conflicts between claims, evidence, ratified intent, or current repository state. A contradiction is not automatically a defect: the agent must still determine scope, authority, and which interpretation is warranted.

### 5. Uncertainties

Record unresolved questions that could change scope, next action, authority path, or stop/continue decision.

For each uncertainty record:

- the question;
- why it is decision-relevant;
- what evidence could change the answer;
- whether it remains active, resolved, or deferred.

### 6. Consequential uncertainty

When the Skill owns this decision, identify which unresolved question currently governs the next action. When the Skill does not own this decision, say that explicitly rather than selecting one on behalf of its caller.

### 7. Responsibility

When applicable, record the bounded responsibility warranted by the evidence and which decision it unblocks. Do not substitute capability availability for responsibility warrant.

### 8. Capability and authority

When applicable, preserve:

```text
warranted responsibility
!= available capability
!= authorized capability
```

The profile may record what capability was used and what authority applied. It must not infer that an available capability was semantically correct merely because it existed.

### 9. Result

Record what the Skill/tool/work actually produced:

```text
artifact
repository change
observation set
validation evidence
no-result / blocker evidence
```

`execution completed` is not equivalent to `responsibility satisfied`.

### 10. Mechanical validation

State exactly what a validator/probe established and what it did not establish.

Example:

```text
Established: artifact satisfies the required structural contract.
Not established: the architectural recommendation is semantically correct.
```

### 11. Semantic evaluation

The active agent evaluates what the evidence now warrants. Keep this separate from mechanical PASS/FAIL.

### 12. Decision

When the workflow reaches a decision boundary, record the agent-authored disposition and supporting evidence. In Campaign context this may correspond to `advance`, `defer`, or `close`.

### 13. Explicit limits

Every profile must preserve important non-claims, blind spots, inherited assumptions, and unavailable evidence. This is mandatory because a compact semantic summary otherwise tends to overstate what was established.

## Machine-comparable pilot core

Phase 9 pilot profiles use the following experimental shape:

```yaml
artifact_id: semantic_reasoning_profile
schema_version: 1
pilot_id: pilot-a-repo-sensemaker
source_skill: repo-sensemaker
target:
  repository: ThorStarlord/example
  ref: <exact commit, snapshot id, or inherited artifact ref>
  access_mode: github_exact_sha | local_snapshot | inherited_artifact
currentness:
  status: pinned_snapshot | verified_current | inherited_currentness | unverified
  evidence_refs:
    - <source establishing the currentness boundary>
observations:
  - id: O1
    statement: <direct/mechanical observation>
    method: direct_read | probe | git_metadata | validator_output | artifact_read | owner_statement | other
    evidence_refs:
      - <source>
claims:
  - id: C1
    statement: <material claim>
    epistemic_status: OBSERVED | DERIVED | INFERRED | HYPOTHESIZED | RATIFIED | CONTRADICTED | SUPERSEDED | UNRESOLVED
    evidence_refs:
      - <source>
    scope: <bounded scope>
    limits:
      - <what this claim does not establish>
uncertainties:
  - id: U1
    question: <decision-relevant question>
    decision_relevance: <how the answer could change action/scope/authority/stop decision>
    evidence_needed:
      - <bounded evidence that could resolve it>
    status: active | resolved | deferred
explicit_limits:
  - <important non-claim or blind spot>
```

Optional stage-specific fields may be recorded in prose pilot reports. They are deliberately not part of the first common executable core.

## Pilot metrics

Each pilot report should record:

```text
competency questions exercised
ambiguous terms encountered
cross-Skill concept mismatches
unsupported inference jumps found/prevented
claims missing evidence/currentness before alignment
new concepts requested
ontology concepts unused
coordination overhead introduced
candidate Level-3 fields
```

## Promotion rule

This profile begins as a Phase 9 comparison instrument. A field becomes a common Level-3 semantic contract only if contrasting pilots demonstrate stable reuse and a deterministic validator can check its representation without judging semantic truth.
