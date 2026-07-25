# Hypotheses

## Run 0002 — live golden-path proof

**Hypothesis under test:** the `architectural-review-planning-workflow`
(steps: repo-sensemaker -> architectural-review) can be executed live, with
the `claude-code` executor, in `guided_execution` mode, against a disposable
target repository, producing a validated brief and a validated recommendation
that are both preserved in the framework repo as durable artifacts — and that
the same runtime enforces the `proposed_direction` input contract by failing
explicitly (not silently) when it is missing.

**Falsification conditions:**
- the executor is unavailable or the run cannot complete a real skill
  invocation (-> EXECUTOR BLOCKER, not proof)
- the target repository is mutated by the run (-> CONFINEMENT FAILURE)
- generated artifacts fail validation (-> VALIDATOR BLOCKER)
- the negative-path run does not fail explicitly at input resolution, or
  produces a recommendation anyway (-> negative-path not proven)
