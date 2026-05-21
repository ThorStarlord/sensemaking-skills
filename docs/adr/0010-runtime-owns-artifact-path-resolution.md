# ADR 0010: Runtime Owns Artifact Path Resolution

**Status**: Accepted

**Context**: Artifacts are session-scoped: a run writes them under
`artifacts/<NN-run-name>/<id>.md`, and the runtime resolves that location through
`OrchestrationRunner._resolve_artifact_path` (contract path + `_scope_to_session_dir`).
The skill executors (`ClaudeAgentSdkSkillExecutor`, `ApiSkillExecutor`) independently
computed a *flat* output path, `artifacts/<id>.md`, both to instruct the skill where to
write and to check whether the artifact was produced. The two computations disagreed
whenever a session directory was active. A real `guided_execution` run of
`full-local-sensemaking` exposed this: the executor wrote `artifacts/problem_frame.md`,
saw it on disk, and returned `EXECUTED`; the runtime then looked in
`artifacts/100-orchestration-run/problem_frame.md`, did not find it, and failed the step
with `ARTIFACT_NOT_FOUND` ("Executor reported success but artifact not found"). The
failure occurred at step 1 and masked every downstream step.

**Decision**: The runtime is the **single owner** of artifact path resolution. When it
invokes a skill it passes the resolved, session-scoped absolute path to the executor as
`context["expected_output_path"]`. Executors MUST write to and verify that exact path via
the shared helper `skill_executor.resolve_output_path(repo_root, artifact_id, context)`,
which returns the provided path and falls back to the flat `artifacts/<id>.md` only when
no path is supplied (standalone executor use outside the runtime).

**Rationale**: This is the same principle the repo already enforces for machine **field
names** (artifacts are the API; producer and consumer must agree), extended to artifact
**location**. Path resolution involves contracts and session scoping that the runtime
already implements; duplicating that logic in each executor guarantees drift. Making the
runtime the sole authority means a new executor cannot reintroduce the mismatch — it
receives a path rather than guessing one.

**Alternatives considered**: (1) Pass only the session directory and let executors join
the filename — rejected; executors would still encode the naming/contract convention and
could drift. (2) Have the runtime check both the flat and session paths — rejected; it
hides the disagreement instead of removing it and leaves stray flat-path artifacts.

**Consequences**: Positive: producer and consumer agree on artifact location by
construction; the bug class cannot recur silently; `tests/test_executor_path_handoff.py`
exercises the real runtime↔executor handoff (not logic-in-isolation). Negative: every
real executor must accept `expected_output_path` from context; an executor that ignores it
will write to the wrong place. The fallback flat path is retained only for standalone use
and should not be relied on inside a workflow run.
