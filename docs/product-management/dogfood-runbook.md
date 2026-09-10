# Product Management dogfood and portability runbook

## Purpose

Qualify the Customer Discovery vertical slice with evidence from real coding-agent harnesses. Repository tests prove contracts and adapter representation only; they cannot manufacture native harness evidence.

## Gate A — functional real-harness run

Use a supported coding-agent harness on a real product repository and real PM question. The run should:

1. initialize or resume a Campaign;
2. identify the warranted PM responsibility explicitly;
3. inspect current capability candidates;
4. invoke the canonical PM Skill through the harness's native discovery mechanism;
5. produce and validate the PM artifact;
6. admit the exact artifact bytes;
7. author the Campaign decision and lineage;
8. continue inside the authorized Customer Discovery envelope while warranted;
9. create a durable handoff;
10. stop.

A claimed PASS may not depend on manually repairing PM artifact/validator output or on hidden prior-chat state.

## Gate B — fresh-context reconstruction

Start a fresh agent context with the repository and durable Campaign/handoff state but no prior conversation. Record whether it reconstructs the mission, established facts, assumptions, evidence, completed responsibilities, current responsibility, authority, open uncertainty, and warranted next action.

## Gate C — second-harness portability

Run an equivalent bounded responsibility through a second supported harness. Compare invariants rather than prose:

- canonical capability identity;
- responsibility type;
- required artifact type;
- evidence rules;
- validator identity;
- Campaign representation;
- authority boundary;
- stop semantics.

Different natural-language output is expected. Semantic-contract divergence is not.

## Evidence record

For every attempt preserve:

```text
harness
adapter / native discovery root
canonical capability version or repository SHA
native setup evidence
native invocation evidence
PM artifact and validator result
Campaign admission refs
transitions / lineage / handoff
validation failures
manual repairs, if any
evidence gaps
owner questions
authority/scope stops
fresh-context outcome
conversation-memory dependency
cross-harness divergence
operator ceremony/problems
```

## Outcome taxonomy

- `FUNCTIONAL_PASS_PORTABILITY_PASS` — both functional and portability claims have real evidence.
- `FUNCTIONAL_PASS_PORTABILITY_PENDING` — one real harness works; second-harness evidence is still absent.
- `FUNCTIONAL_PASS_PORTABILITY_FAIL` — functional flow works but a material harness portability defect is observed.
- `FUNCTIONAL_FAIL` — the PM flow itself fails on real use.
- `INVALID` — the attempt does not actually test the promised boundary, for example because prior chat or manual repair substituted for durable state.

Preserve FAIL and INVALID attempts. Do not rewrite them into PASS artifacts.

## Current environment note

Repository-local CI can prove packaging, deterministic validation, Campaign admission, and structural adapter parity. A real Claude Code/Codex/OpenCode native invocation requires that actual external harness and must be recorded separately; repository CI is not a substitute.
