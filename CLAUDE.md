## Agent skills

### Issue tracker

Issues and PRDs live as GitHub issues. See `docs/agents/issue-tracker.md`.

### Triage labels

Five canonical labels using the skill defaults. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context repo — `CONTEXT.md` at root, ADRs in `docs/adr/`. See `docs/agents/domain.md`.

## Verification discipline (artifacts are the API)

This repo's founding principle is *artifacts are the API between skills*. Field names
are part of that API. These rules exist because each was violated and caused a real bug.

- **Field names are part of the contract.** Before writing code that reads a machine
  field from an artifact, confirm the field name is declared in
  `skills/workflow-planner/references/artifact-contracts.yaml` for that artifact.
  Producers and consumers must agree on field names — do not read fields from memory.
  `tests/test_field_contract_agreement.py` enforces this for routing field reads; if you
  add a field-read alias to the runtime, declare it in a contract too.
- **Artifact *paths* are part of the contract, too — not just field names.** One component
  owns path resolution: the runtime, via `OrchestrationRunner._resolve_artifact_path`
  (which session-scopes paths). Any component that *writes* an artifact (e.g. a skill
  executor) must receive the resolved path from the runtime — passed as
  `context["expected_output_path"]` — and write exactly there. Never recompute
  `artifacts/<id>.md` independently. Producers and consumers must agree on *where* an
  artifact lives, not only *what* is in it. A flat-path-vs-session-path mismatch once made
  an executor report success while the runtime saw `ARTIFACT_NOT_FOUND`. See ADR 0010.
- **A validator rule must trace to a real consumer.** Before a validator enforces a
  format or shape, confirm something downstream actually parses it. Enforcing a convention
  nothing consumes produces false failures and fights the producer's natural, valid output
  — an `Lx`-only evidence-line format (read by nothing downstream) repeatedly rejected
  valid bare-number citations until it was relaxed to accept both.
- **"Done" requires running the real path.** Structural checks (YAML parses, workflow
  exists, logic-in-isolation) do not prove a producer→consumer handoff works. Before
  claiming a routing/handoff feature works, exercise it end-to-end against realistic
  artifacts. Never claim "production ready" on structural tests alone.
- **A TODO in an execution path is a blocker, not decoration.** Do not build a feature on
  top of an unfinished primitive without flagging it.
- **Console output is ASCII-only.** This codebase runs on Windows (cp1252); non-ASCII
  characters in `print()`/stdout crash the process. Use ASCII (`->` not `→`).
- **Compare like-for-like when checking for regressions.** Run the same test set the same
  way on both the baseline and your change before attributing a failure to your work.
