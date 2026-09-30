# Control arm 002 — Pydantic (no skill, read-only)

Clean control for `strategic-sensemaking-trial-002.md`. Fresh agent context;
the prompt explicitly forbade reading or using any skill/SKILL.md/sensemaking
material. Same objective, same read-only authority. Recorded for artifact-level
comparison, not self-report.

```text
Repository / domain: a2-target-pydantic (Pydantic)
Date: 2026-09-29
Loaded Skill identity: NONE (control arm — skill deliberately excluded)
Chosen responsibility / next action: Establish a verifiable baseline before any code change — the checkout is clean main but not importable/testable (pydantic requires pydantic-core 2.48.0, machine has 2.46.4; no project venv). Then request the authoritative work queue.
First concrete step: with owner authorization, `uv sync` + smoke test `uv run pytest tests/test_main.py -q`.
Scope avoided / refused: editing source or relaxing the dependency pin to mask the mismatch; TODO/FIXME sweep (61 hits, mostly v3/PEP 747/deliberate); vendored pydantic-core Rust; any commit/branch/PR.
Alternatives rejected: hunt-and-fix a code bug (AST-parsed all modules, 0 failures; no test run possible); pick an in-flight work branch (needs backlog/owner intent); docs/example improvement; dependency bump (already current).
Confidence: moderate (high on diagnosis; moderate on "restore verifiability" being THE single responsibility).
Blocking question: authoritative work queue + owner intent; is the environment intentionally frozen?
Read-only slip: an incidental `uv run --no-sync` probe created a `.venv`; self-detected, confirmed gitignored, removed. `git status` clean.
```

## Comparison (skill arm vs control arm)

- Responsibility chosen: skill = ownership/scope sensemaking → ESCALATE on
  owner-intent/authority; control = restore verifiability + request the queue.
  Different, but both refuse to invent scope.
- Scope avoided: both refuse the TODO sweep and source edits. The control
  additionally breached read-only (created a `.venv`) before self-correcting;
  the skill arm did not mutate.
- Verdict on this task: **mixed / near-tie.** The skill's predicted baseline
  failure (start editing the first visible improvement) did not materialize in
  the control; the control chose a legitimate verify-first responsibility.
  Weak skill-favorable signal only on authority discipline.
