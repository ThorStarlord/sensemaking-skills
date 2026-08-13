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
