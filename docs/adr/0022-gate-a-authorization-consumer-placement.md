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

2. Only `authorize_invocation()` can mint an `AuthorizedInvocation`, and only
   when the decision is `authorized=True`. The class constructor requires a
   private module token, so no caller can forge one.

3. Both model-invoking executors require that object for a controlled Stage 1
   invocation (`controlled_experiment=True`), in three layers:

   - `create_executor` refuses every executor id without it;
   - each executor's `__init__` refuses to be constructed without it;
   - `_invoke_skill_async` **consumes** it as the last statement before
     `query()`.

4. `consume()` raises rather than returning a value, so an intermediate caller
   cannot proceed by discarding a result. It marks the capability spent, which
   is what makes `invocation_limit: 1` real.

### Why `controlled_experiment` is the trigger

`controlled_experiment=True` is the repository's existing, already-enforced
declaration that a run is a controlled experiment (issue #86 made an explicit
`--model` mandatory in that mode). Stage 1 is defined as such a run. Gating on
it means a controlled Stage 1 invocation cannot occur without a capability
through any executor or entrypoint, while ordinary development invocations —
which are not Stage 1 runs, and which Gate A does not claim to govern — are
unchanged. This scoping is stated plainly rather than hidden: it is the honest
boundary, not an omission.

### Why not the rejected alternatives

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

PROPOSED, not Accepted. Promotion condition: an independent adversarial
reviewer confirms (a) the negative zero-invocation proofs genuinely exercise
the real executors, (b) no ungated provider call site remains, and (c) the
preparation-contract status changes are limited to what actually changed.
