# Verification scenario synthesis (2026-11-25)

**Status:** generative product capability, exercised on a real symbol and used
to close two verification gaps.
**Source baseline:** `3a6d54bf28d44e5b313d2d665f921eafae5a85fd`.
**Implementation:** `844f73096c23cdf169ce2ec985f73d212411c7e5`.

The capability turns direct `raise`/`assert` guards in a selected Python
symbol into bounded verification scenario candidates. It does not generate
executable tests, prove reachability or establish coverage.

## 1. Observed limitation

The existing symbol context reported a source-level behavioral surface:
signature, decorators, docstring hash, direct raises/asserts and a source-body
hash. It did **not** show the conditions behind each guard or suggest boundary
inputs.

For `src/sensemaking_skills/semantic_architecture/source_relationships.py`,
`build_source_relationships` had five direct `ValueError` guards. The hosted
consumer exercised only one of them (malformed `--symbol`). The non-Python-path
and untracked-path guards had no direct test candidate and were not checked.
An agent had to read the function and design those scenarios manually.

## 2. Delivered capability

`context-for --include-source-relationships --symbol NAME` now adds
`symbol_context.verification_scenarios`:

- direct `raise` and `assert` guards;
- condition text, including enclosing `if` conditions;
- expected exception or `AssertionError`;
- heuristic boundary input hints from literal comparisons and module integer
  constants;
- count, coverage status, truncation and explicit limits.

The output is a scenario candidate list for the agent to inspect and turn into
tests or probes. It is not a test generator and does not claim that a scenario
is reachable, necessary or correct.

## 3. Selection rehearsal and authentic use

The candidate was rehearsed with [Prospective Decision Rehearsal v1](../../skills/using-sensemaking/references/prospective-decision-rehearsal-v1.md)
before the final implementation decision:

| Field | Observation |
| --- | --- |
| Beneficiary episode | An agent preparing a change to `build_source_relationships`; the current symbol context exposed five guards but only one hosted check. |
| Current decision | Inspect the raises manually and retain the existing malformed-symbol check. |
| Candidate decision | Request the symbol context, read the generated guard scenarios and add negative checks for the non-Python and untracked-path guards. |
| Mechanism-to-data check | The baseline symbol context had raises/asserts but no scenario candidates; the guards and literal comparisons are present, so the new field can fire. |
| Expected observation | The scenarios include the `.py` and tracked-path conditions, and both new hosted negative checks fail closed. |
| Disposition | **BUILD** — a reversible, useful realization with a concrete verification delta. |

Observed after implementation on `build_source_relationships`:

- `guards: 5`, `scenarios: 5`, `with_input_hints: 1`;
- the `limit` guard produced `limit=0`, `limit=1`, `limit=2`, `limit=249`,
  `limit=250`, `limit=251`;
- the non-Python, untracked-path, unreadable-target and malformed-symbol
  conditions were visible with `ValueError` expectations;
- the hosted consumer now rejects `README.md` and an untracked `.py` path for
  this source-context operation.

The capability changed a real verification decision: two previously unchecked
guards are now covered by the hosted consumer.

## 4. Product versus model

**Product:** exact-revision AST extraction, guard/condition mapping, module
constant resolution, heuristic boundary hints, counts, truncation and explicit
limits.

**Model:** selected the symbol and change question, read the generated
scenarios, judged which were consequential, and added the negative checks. The
product did not decide that the implementation was correct or covered.

No intrinsic cognitive improvement or comparative benefit is claimed.

## 5. Claim ceiling

| Level | Status |
| --- | --- |
| Direct guard scenario extraction | Observed on real symbols |
| Boundary hints and condition text | Observed |
| Hosted negative checks for two guards | Observed |
| Executable test generation | NOT IMPLEMENTED |
| Reachability, coverage or pass status | NOT ASSESSED |
| Semantic correctness or change safety | NOT ESTABLISHED |
| Independent later-agent reuse or comparative benefit | NOT ESTABLISHED |

## 6. Continuation

The next warranted use is an independent agent applying the scenarios to a real
signature or guard change and recording whether they changed its verification
set. Extending to helper validation, exception paths, parameterized fixtures or
generated test code requires evidence from that use; it is not assumed here.
