# ADR 0022: Gate A Authorization Consumer Placement and Invocation Binding

**Status**: PROPOSED — awaiting independent adversarial review. Merging this
ADR and its implementation **does not authorize Stage 1**.
**Date**: 2026-07-30
**Proposes resolution for**: the Gate A authorization-consumer requirement
ratified by PR #107 (`docs/experiments/STAGE-1-AUTEUR-POST-REMEDIATION-PREPARATION.md`,
section 2j; hard stop 24 `GATE_A_AUTHORIZATION_CONSUMER_NOT_IMPLEMENTED`).

---

## Context

PR #107 ratified a complete authorization contract for a single controlled
Stage 1 run against the remediated `auteur` repository, and was explicit that
the contract was **specified but unenforced**: no runtime component loaded the
authorization record, recomputed its digest, validated the owner approval, or
blocked a model invocation on authorization state. Hard stop 24 existed to say
so, first-evaluated and non-waivable.

Section 2j, criterion 25 is the load-bearing constraint:

> A consumer that passes unit tests in isolation but is never called by the
> real Stage 1 path enforces nothing.

So the decision is not "write a validator". It is **where to put the gate, and
what binds it to the invocation**.

## The real call graph (verified, not assumed)

The preparation prose names `scripts/workflow-runtime.py` as
`stage1_entrypoint`. That is the CLI entrypoint, but it is **not** where a
model call happens. Reading the actual code, there are exactly two production
paths that reach a provider SDK, both in `scripts/skill_executor.py`:

```text
scripts/workflow-runtime.py  (CLI / workflow plan execution)
  -> OrchestrationRunner.__init__
     -> skill_executor.create_executor(executor_id, ..., controlled_experiment)
        -> ClaudeAgentSdkSkillExecutor.invoke_skill
             -> _invoke_skill_async
                  -> claude_agent_sdk.query(ClaudeAgentOptions(model=...))   [PATH 1]
        -> ApiSkillExecutor.invoke_skill
             -> anthropic.Anthropic().messages.create(model=...)             [PATH 2]
```

`DryRunSkillExecutor` and `PromptChainSkillExecutor` never reach a provider.

Two findings mattered:

1. **Path 2 is a real second production provider path.** Gating only the Agent
   SDK executor would have left a genuine bypass. It also hardcodes a model
   that is *not* the contractually authorized Stage 1 model.
2. **The invocation count becomes nonzero inside `_invoke_skill_async`**, not
   in the runtime and not in `invoke_skill`. A gate placed only in the CLI
   would be a gate an intermediate caller could route around.

Placing the gate from the prose alone would have produced enforcement in the
wrong component.

## Decision

**Gate at the provider boundary, bind by typed single-use capability.**

1. `scripts/gate_a_authorization.py` is the consumer. It is pure and read-only:
   it validates and returns a typed `AuthorizationDecision`. It never invokes a
   model, never writes either repository, and never repairs an invalid record.

2. Only `authorize_invocation()` can obtain an `AuthorizedInvocation`, and only
   when the decision is `authorized=True`. The capability is *issued by the
   registry*; the returned object is an opaque handle to one live issuance.
   Possessing the object is not authorization -- being live in the registry is.

3. Both model-invoking executors require that object whenever the derived
   `ExecutionMode` requires Gate A, in three layers:

   - `create_executor` refuses every executor id without it;
   - each executor's `__init__` refuses to be constructed without it;
   - `_invoke_skill_async` **consumes** it as the last statement before
     `query()`.

4. `consume()` raises rather than returning a value, so an intermediate caller
   cannot proceed by discarding a result. It retires the registry issuance
   atomically, which is what makes `invocation_limit: 1` real.

### Superseded: why `controlled_experiment` was the trigger, and why it is not

**The original design in this ADR was wrong, and an independent adversarial
review reproduced three working authorization bypasses against it.** That
history is recorded here rather than quietly edited out.

The rejected reasoning was: `controlled_experiment=True` is the repository's
existing declaration that a run is a controlled experiment, so gate on it. The
defect is that a *declaration* is not a *fact*. The flag was a caller-supplied
boolean defaulting to `False`, and `require_authorization_capability()` opened
with `if not controlled_experiment: return`. Three consequences were
reproduced against the real code, with fake provider spies:

1. **Caller-controlled opt-out.** Omitting one CLI flag reached the real Stage 1
   provider call with zero authorization. Worse, constructing a gated executor
   with a valid capability and then assigning `.controlled_experiment = False`
   reached the provider *and left the capability unconsumed and reusable*.
2. **Capability cloning.** `AuthorizedInvocation` defined no `__copy__`,
   `__deepcopy__`, `__reduce__`, or `__slots__`. `copy.copy`, `copy.deepcopy`,
   and every pickle protocol each produced a fully usable duplicate. One
   authorization yielded nine successful consumptions.
3. **Concurrency race.** `consume()` was check-then-set: it read
   `self._consumed`, performed expensive revalidation (five file hashes, two
   git HEAD reads), and only then set `self._consumed = True`. Eight threads
   racing one single-use capability produced eight successes and a
   `remaining_invocations` of `-7`.

### The replacement decision

**The caller does not decide whether authorization is required, and the
capability object does not itself constitute authorization.**

1. **Controlled Stage 1 is recognized structurally, from immutable invocation
   identity.** `InvocationIdentity` is a frozen record of what is actually being
   invoked: workflow id and stage, artifact type, evidence number and slug,
   output path, framework and target roots, target repository and SHA, the
   exact requested model, executor id, and invocation limit.
   `classify_invocation()` maps it to a typed `ExecutionMode`. The structural
   signals that mean controlled Stage 1 are: the artifact type is
   `repository_sensemaking_brief`; the workflow stage is Stage 1 repository
   sensemaking; the evidence number or slug is the campaign's; the output lands
   under `experiments/evidence/` or `experiments/run-control/`; the target
   repository is the campaign pin; the requested model is the campaign model.

2. **Ambiguity fails closed.** `ExecutionMode.AMBIGUOUS` is gated exactly like
   `CONTROLLED_STAGE1`. A partial match, a missing identity, or a declared mode
   that disagrees with structure all produce
   `GATE_A_INVOCATION_CLASSIFICATION_AMBIGUOUS`, never ordinary execution. A
   declared `False` can never override a structural signal.

3. **`controlled_experiment` is demoted to informational metadata.** It is a
   read-only property with no setter, it is excluded from the identity digest,
   and it appears in the security decision only as a signal that can *raise*
   the requirement, never lower it. The security-relevant executor attributes
   reject reassignment, and -- more importantly -- the classification is
   re-derived from the call arguments at every provider boundary, so even a raw
   `__dict__` poke cannot downgrade what Gate A believes is happening.

4. **Capability uniqueness is issuer-backed, not based on Python privacy.**
   The earlier claim that a module-private construction token made the
   capability "unforgeable" was wrong: Python attribute privacy is a
   convention, not a security boundary. Authorization now lives in a
   process-local `_CapabilityRegistry` keyed by a 256-bit random capability ID.
   `AuthorizedInvocation` carries only that ID (`__slots__`, immutable, not
   subclassable). Every question is answered by the registry, live, under a
   lock. A forged ID is absent (`GATE_A_CAPABILITY_NOT_LIVE`); a reconstructed
   object carrying a *real* ID competes for the same single entry, so at most
   one consumption can ever succeed.

5. **Copying and serialization are prohibited outright.** `__copy__`,
   `__deepcopy__`, `__reduce__`, `__reduce_ex__`, `__getstate__`, and
   `__setstate__` all raise, as does subclassing. This is defense in depth on
   top of (4), not a substitute for it.

6. **Consumption is atomic.** The transition is taken under the registry lock
   *before* revalidation, so the race window is a dict lookup rather than seven
   IO operations:

   ```
   lock: verify state == ISSUED -> set CONSUMING -> unlock
   identity comparison + byte/revision revalidation
   on any failure (including cancellation): lock -> set FAILED -> unlock, raise
   on success:                              lock -> set CONSUMED -> unlock
   call provider
   ```

7. **Any consumption attempt burns the issuance.** A failed, cancelled, or
   interrupted attempt moves to `FAILED` and never returns to `ISSUED`. This is
   a deliberate tightening: it means a wrong-model attempt, a TOCTOU failure, or
   an interrupted run cannot become an unauthorized retry. This campaign permits
   no retry. Consumption also completes *before* the provider call, so a
   provider error cannot hand back a reusable authorization.

8. **Both provider paths remain gated whenever classification requires Gate A.**
   The Claude Agent SDK path requires and atomically consumes the capability.
   The Anthropic API path requires it too and then still refuses on model
   mismatch, because it hardcodes a model that is not the authorized one.

### The ordinary-development boundary, stated exactly

An invocation is ungated only when it is structurally distinguishable from the
campaign: its output is outside every controlled evidence namespace, it does
not name the campaign evidence number or slug, it does not target the pinned
campaign repository, it does not request the exact campaign model, and it does
not declare controlled mode. Running `repo-sensemaker` locally into
`artifacts/` therefore stays ungated; running the same skill into
`experiments/evidence/` never does. This is a narrow, testable line, and it is
asserted in both directions: positive tests prove ordinary work still runs
without Gate A, and negative tests prove relabelling controlled Stage 1 as
ordinary does not work.

### Why not the rejected alternatives

- **A caller-supplied boolean (`controlled_experiment`)** -- the original
  design. Rejected after three reproduced bypasses; see above.
- **Trusting the capability object's own `_consumed` field** -- the object is
  not the authority. State read from an object an attacker can rebuild is not
  a security check.
- **A global boolean / module flag** — mutable from anywhere, provable by
  nothing, and indistinguishable at the call site from an unset default.
- **An environment variable (`AUTHORIZED=true`)** — an attacker-supplied and
  operator-supplied value with no binding to *which* record was approved. A
  test asserts no such variable exists in either module.
- **Validating early and discarding the result** — this is exactly the defect
  criterion 25 names. It is why the capability is consumed at the provider
  boundary rather than checked in the runtime.
- **Gating only the CLI entrypoint** — leaves the imported-function path, the
  second executor, and any future caller ungated.

## TOCTOU boundary

Preflight-time validity is deliberately **not** sufficient. The capability
stores a `_ValidatedSnapshot` of the record, digest file, approval, package and
checklist digests plus both repository HEADs. `consume()` re-reads all of them
and compares before releasing the invocation, so a change made between
preflight and the provider call fails closed with
`GATE_A_REVALIDATION_FAILED`. Chosen boundary: **capability binding to
validated digests and revisions, plus revalidation at the invocation site.**

## Consequences

- Hard stop 24 is **retired by satisfaction, not waived**. It remains among the
  24 conditions and remains non-waivable, so deleting or unwiring the consumer
  makes it fire again.
- The package stays `PREPARED_NOT_RUN`, `NOT_AUTHORIZED`,
  `package_runnable: false`, Evidence 0016 unused, readiness
  `Externally exercised`.
- With no record, no digest, and no approval on disk, the consumer denies every
  request and mints nothing. **An enforcement mechanism with nothing to enforce
  authorizes nothing.**
- The execution framework SHA is **not** finalized here; it must be the
  canonical `main` SHA *after* this consumer merges and is independently
  verified. Setting it to this branch head would be a self-referential pin.

## Status rationale

PROPOSED, not Accepted. The first submission was reviewed adversarially and
returned REQUEST_CHANGES with three reproduced bypasses; this revision is the
remediation, not a patch to the failing test cases.

Promotion condition: a **second** independent adversarial reviewer confirms
(a) the negative zero-invocation proofs genuinely exercise the real executors,
(b) no ungated provider call site remains, (c) the preparation-contract status
changes are limited to what actually changed, (d) the structural
controlled-Stage-1 classification cannot be defeated by any caller-supplied
value, and (e) no clone, reconstruction, or concurrent caller can obtain a
second consumption from one issuance.
