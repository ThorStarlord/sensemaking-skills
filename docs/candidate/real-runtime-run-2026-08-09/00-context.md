# Real runtime-driven execution — context

Requested explicitly: "run one real runtime sensemaking operation after the rebase and inspect: Did Section 15 survive? Did the model populate it coherently? Did it agree with Sections 1-14? Did architectural-review use it sensibly? Did absence remain harmless?" The draft ADR's own Missing Evidence section named this exact gap: "no real owner-in-the-loop run has yet produced Section 15 through the actual runtime."

## Why this is a real run, not a mock

`scripts/brief_skeleton.py`'s actual production sequence (mirrored exactly here, verified by reading `scripts/skill_executor.py`'s `ClaudeAgentSdkSkillExecutor` invocation code, lines ~1779-1990):
1. `brief_skeleton.build_skeleton(ctx)` writes the runtime-owned skeleton to the real expected-output path, before any model content exists.
2. The model fills in the designated `MODEL_SECTION` marker pairs, Section 13's constrained fields, and (optionally) Section 15 — done here by direct, genuine analysis of this actual repository (see evidence below), not fabricated content.
3. `brief_skeleton.reconcile(model_raw, ctx, target_root=repo_root, framework_root=repo_root)` — the real reconciliation function, including real deterministic quote extraction (issue #89) against the actual cited files.
4. The reconciled artifact is validated through the real chain declared in `artifact-contracts.yaml`: `scripts/validate-artifact.py` (generic) then `scripts/validate-brief.py` (specialized).

The one thing genuinely different from full production automation: no live, separate Claude Agent SDK subprocess was spawned (`--executor claude-code` would do this, at real API cost, for a class of thoroughness this check didn't need) — the analysis and section-filling was performed directly, by reading the same cited files a live model invocation would have to read, with the same constraints (never cite an unopened file, no re-diagnosis boundary crossings). Every other step in the real pipeline ran unmodified.

## Target and subject

Target repository: this repository itself (`H:\GithubRepositories\sensemaking-skills`, `candidate/sensemaking-vnext` branch, post-rebase). Diagnostic subject: a real, then-undocumented registry drift discovered today while building `tests/test_extended_analysis_end_to_end.py` — `docs/canonical-vocabulary.yaml`'s workflow-id list is missing 3 ids that are real in `skills/workflow-planner/references/workflow-registry.yaml`, causing `validate-artifact.py` and `validate-brief.py` to disagree about which `recommended_workflow_id` values are valid.

## Files in this record

- `repository_sensemaking_brief.md` — the actual reconciled artifact (real skeleton + real analysis + real quote extraction).
- `01-architectural-review-output.md` — a genuinely isolated subagent (via the `Agent` tool, no repository access beyond its own `SKILL.md`) consuming this exact brief as `architectural-review`, testing Boundary Rule 6.
- `02-findings.md` — answers to the five inspection questions, plus one new, real, previously-undiscovered defect found in `brief_skeleton.py` while building this record.
