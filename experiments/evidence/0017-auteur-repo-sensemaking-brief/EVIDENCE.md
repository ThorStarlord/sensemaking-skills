# Evidence 0017 — Auteur repo-sensemaking brief (direct-invoked run)

## Purpose

Dogfood evidence for the **sensemaking-skills** repository: the `repo-sensemaker`
skill was executed end-to-end against a real external target repository (Auteur)
and produced a validated `repository_sensemaking_brief.md`. This folder records
that run so it can be analyzed later as evidence that the skill works on a real,
non-trivial target.

## Target repository (the object of the brief)

- Repository: `H:\GithubRepositories\auteur` (auteur, v0.37.1)
- Branch/head at analysis time: `main` @ `3acf8a1`
- Analysis date: 2026-08-13

## How the run was performed

- Skill: `repo-sensemaker` (per the sensemaking-skills canonical SKILL.md).
- Invocation mode: **direct invocation** — NOT runtime-invoked, so there is no
  `run-ledger.jsonl`, no `tool-call-trace.jsonl`, and no runtime skeleton. The
  skill's "Output Format" rule made the brief the response; it was then written
  into the target repo's runtime scratch area (`artifacts/09-orchestration-run/`)
  and promoted here as evidence.
- Probe engine: `scripts/probe-repo.py` was run against the target; the raw
  output is `probe-report.yaml` in this folder (generated 2026-08-13T01:22:08Z).
- The `00-user-intent.md` artifact follows the auteur runtime's artifact shape
  (`created_by: orchestration-runner`) and was produced for this run to match the
  target repo's convention — even though this run itself was direct-invoked.
- Validation: both validators exit 0 —
  - target repo's own `scripts/validate-brief.py` (auteur):
    "Brief verification passed! Evidence and workflow ID are valid." (see `validator-output.txt`)
  - canonical `scripts/validate-brief.py` (sensemaking-skills):
    "Brief verification passed! All required fields are present and valid."

## Folder contents

| File | Purpose |
| --- | --- |
| `repository_sensemaking_brief.md` | The validated brief (docs_fog diagnosis, weakness type Vocabulary Drift) |
| `probe-report.yaml` | Raw probe measurements of the target repo (verified current state) |
| `00-user-intent.md` | The run's user-intent artifact |
| `validator-output.txt` | stdout of the target repo's `validate-brief.py` (exit 0) |
| `EVIDENCE.md` | This run record |

## Provenance

- Target repository: Auteur (`H:\GithubRepositories\auteur`, v0.37.1)
- Target repository SHA analyzed: `3acf8a1` (auteur `main` at analysis time;
  reverified from `probe-report.yaml` `git_state.head_sha`)
- Sensemaking generator repository SHA (sensemaking-skills `main` at run time):
  `63350d47f251a6753662e9aeab92098f76c15d61` — recorded as the repository state
  at run time, **not** as a formal product/version identifier
- Loaded skill source (verified): the `repo-sensemaker` SKILL.md executed was
  loaded from the installed skill root
  (`C:\Users\Admin\.agents\skills\repo-sensemaker\SKILL.md`); its content does
  NOT byte-match `skills/repo-sensemaker/SKILL.md` at the SHA above
  (SHA-256 `7879fb8f44809debfb73abb3f44982e9bcd0910a317b50366ca45d55954d0d4b`
  installed vs `b223b7808f210bd4b8021b898285261565b90ec77bca2eb50f023ced406dae7e`
  at `63350d4`), so the SHA alone does not identify the loaded skill revision
- Probe engine + validators: sensemaking-skills `scripts/probe-repo.py` /
  `validate-brief.py` from the sensemaking-skills checkout at the SHA above
- Execution mode: direct-invoked (no orchestration runtime)
- Review verdict: ship as-is (forced review)
- Promotion date: 2026-08-13
- `run-ledger.jsonl` / `tool-call-trace.jsonl`: **not produced** — this was not a
  full orchestration-runtime run; their absence is evidence of the execution
  mode, not a gap (no fabricated telemetry)

## Dogfood findings (observations for sensemaking-skills)

1. **Probe engine timeout masks context entropy.** On a target with ~10k ignored
   files (Auteur's root reasoning-report JSONs), the probe's `git status
   --ignored` subprocess hit the 30s cap in `repo_probes._git`, so
   `context_entropy.ce` was reported as `0.0` (a false "clean" reading) instead
   of the true high-entropy state. (The timeout itself is inferred from
   `repo_probes._git`'s 30s cap and empty return on failure — `probe-report.yaml`
   records no exit code/stderr for git calls.) Recommendation: distinguish
   "timed out" from "clean", or raise the timeout / stream ignored files.
2. **Validator-generation drift on excerpt `lines` format.** The canonical skill
   (evidence-rules.md) accepts bare numbers or `Lx`/`Lx-Ly`; auteur's vendored
   `validate-brief.py` rejects bare numbers (`INVALID_LINE_FORMAT`). A brief that
   passes one validator can fail the other. Producers cannot satisfy both without
   knowing the consumer's generation.
3. **Duplicate ADR identifiers are not flagged.** The target has two files both
   numbered `013`; the ADR probe catalogs both (`relationships.adr.catalog`) but
   emits no finding for the duplicate id. A duplicate-id check would have caught
   the target's sharpest defect mechanically.
4. **Root-level handoff docs escape the `file:///` check.** The target's
   `validate-repo.py` only scans `examples/` for absolute `file:///` paths, so a
   stale root `HANDOFF.md` with machine-specific links passes all checks.

## Outcome

The brief's diagnosis (duplicate ADR 013, stale HANDOFF.md, reasoning-report
artifact sprawl; `docs_fog` / Vocabulary Drift) was independently verified by a
forced review (verdict: ship as-is). The same brief was promoted to the target
repo's tracked evidence location (`docs/reviews/2026-08-13-auteur-repo-sensemaking-brief.md`)
as target-repo evidence; this folder is the sensemaking-skills dogfood record.

### Durability-completion pass (2026-08-13)

The initial promotion copied the brief into tracked locations but its durable
references still pointed at the gitignored runtime directory
(`artifacts/09-orchestration-run/`). A corrective pass normalized every such
reference so it resolves to the tracked companion artifacts inside this folder:

- `artifacts/09-orchestration-run/probe-report.yaml`
  → `experiments/evidence/0017-auteur-repo-sensemaking-brief/probe-report.yaml`
  (5 occurrences: Sections 3.1, 3.3, 7, 11, 13 `evidence` list)
- `artifacts/09-orchestration-run/00-user-intent.md`
  → `experiments/evidence/0017-auteur-repo-sensemaking-brief/00-user-intent.md`
  (1 occurrence: Section 13 `source_intent_ref`)

Only path/reference syntax changed; the diagnosis, claims, recommendations,
evidence meaning, fog/boundary classification, and quoted evidence are
unchanged. The corrected brief re-passes the canonical validator (exit 0).

