## SessionStart hook

At session start, the **using-sensemaking** bootstrap skill is available to agents.

This skill teaches agents:
- Fog classification (4 types)
- When repository sensemaking is warranted
- How to read artifact outputs
- How to interpret validator errors (JSON format)
- How to select responsibility before Skill
- Bounded retry logic and escalation
- When validation, reconciliation, repair verification, continuation, or stopping is warranted

**Agents invoke this skill** via the Skill tool: `/skill using-sensemaking`

**The hook does NOT**:
- Inspect your repository
- Classify fog type
- Invoke workflows
- Validate artifacts

Those are agent responsibilities, taught by the skill and the agent-native operating workflow.

See `.claude/hooks/sessionstart.md` for full hook documentation and testing guide.

No executable hook is configured (`.claude/settings.json` is `{}`); the bootstrap
reaches agents through this file plus the installed `using-sensemaking` skill.
Disposition of deterministic scripts and hooks:
`docs/decision-orchestration-boundary.md`, section "Deterministic machinery and hooks".

---

## Agent skills

### Issue tracker

Issues and PRDs live as GitHub issues. See `docs/agents/issue-tracker.md`.

### Triage labels

Five canonical labels using the skill defaults. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context repo — `CONTEXT.md` at root, ADRs in `docs/adr/`. See `docs/agents/domain.md`.

## Current operating discipline

The active coding agent owns the top-level control loop (ADR 0013). Use
`docs/agent-native-operating-workflow.md` as the current operating map.

- **Choose responsibility before Skill.** Resolve the nearest unresolved
  decision-changing uncertainty before committing to an eventual solution.
- **Decision is not orchestration.** Sensemaking selects the responsibility
  warranted by current evidence. Execution/orchestration coordinates how the
  selected responsibility is performed. Do not restore automatic downstream
  routing merely because a runtime path exists.
- **Validation is not closure.** Mechanical PASS makes an artifact eligible
  for semantic use; it does not prove the conclusion, work claim, or original
  finding is resolved.
- **Finding is not authorization.** Diagnosis, recommendation, implementation,
  validation, owner decision, publication, and canonical closure are distinct
  lifecycle states.
- **Research hypotheses are not architecture.** Domain-general Sensemaking,
  domain-specific packs, and formalized decision-theory machinery remain
  research questions unless separately ratified.

See `docs/decision-orchestration-boundary.md` for the control-ownership boundary
and `docs/research/control-model-research-agenda.md` for explicitly non-ratified
research paths.

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
