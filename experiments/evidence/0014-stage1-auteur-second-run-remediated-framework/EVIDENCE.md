# Evidence 0014 — Second Controlled Stage 1 Auteur Run (Remediated Framework)

## Summary

```text
Final classification: STAGE 1 FAIL
Invocation count: 1
Structural validation: FAIL
Substantive review: NOT REACHED (gated on structural PASS)
Usefulness review: NOT REACHED (gated on structural PASS)
Target mutation: none
Completed target writes: 0
```

## Pins

```text
Framework repository: ThorStarlord/sensemaking-skills
Framework SHA: 1098acfd614e497bdf551040d3b1dee30afb9834
Target repository: local auteur clone (H:\GithubRepositories\auteur origin)
Target SHA: b40db654e0df9e90074f7ad85b40d7362378e07d
Model requested: claude-sonnet-5
Model reported: claude-sonnet-5 (uniform, single distinct value)
model_match: true
Fallback: none configured, none used
Retry: none
```

## Authorization

See `AUTHORIZATION.md`. Owner authorization given in chat 2026-07-27, after
independent verification of PR #95's merge status, the framework/target SHA
pins, and the ancestor chain of PR #91/#92/#94 in the framework pin.

## Preflight results

```text
PR #95 merged: YES (mergedAt 2026-07-27T15:18:46Z, merge commit 1885dff0482cf2e43cbbbaec75fb47d33f506a51)
Framework SHA exists and is on origin/main: YES
PR #91 merge commit (e65da78b) ancestor of framework SHA: YES
PR #92 merge commit (f8c40fd6) ancestor of framework SHA: YES
PR #94 == framework SHA: YES (1098acfd614e497bdf551040d3b1dee30afb9834)
Target SHA (b40db654) exists in local auteur repo: YES
Historical evidence commit a328c80 (PR #78) reachable from
  evidence/auteur-campaign-final-rerun: YES
PR #78 status: OPEN, unmerged (untouched by this run)
Evidence 0013 status: unmodified by this run
Fresh disposable clones used: YES
  H:\scratch\stage1-auteur-rerun-2\framework
  H:\scratch\stage1-auteur-rerun-2\target-auteur
Clones outside .claude/worktrees/: YES
Framework working tree clean pre-run: YES
Target working tree clean pre-run: YES
Framework HEAD == authorized framework SHA: YES
Target HEAD == authorized target SHA: YES
validate-repo.py: PASSED
test-validators.py: PASSED (all fixtures pass)
Model enforcement code path present (PR #87): YES (confirmed via
  requested_model/reported_models/model_match fields in tool-call-trace.jsonl)
Deterministic evidence-quote extraction present (PR #91): YES (present in
  framework pin; not exercised because structural validation failed before
  reaching quote-grounding checks)
weakness_type safeguard integrated (PR #92/#94): YES (present in framework
  pin; not exercised for the same reason)
No retry/fallback wrapper present: YES
Exactly one invocation authorized: YES
```

No preflight hard stop occurred. Execution proceeded.

## Note on target-repository source

The merged execution package's own §6 command plan leaves the target clone
source as a literal placeholder (`<auteur-repo-source>`), unresolved by the
package itself. This run resolved that gap by cloning from the local
`auteur` working copy at `H:\GithubRepositories\auteur` (which was
independently confirmed to contain the exact authorized target SHA,
`b40db654e0df9e90074f7ad85b40d7362378e07d`, at a clean working tree) rather
than a GitHub URL. This is disclosed here as a deviation from the package's
literal (incomplete) text, not as a silent assumption.

## Exact invocation

```text
python scripts/workflow-runtime.py \
  "Analyze this external repository, identify the weakest architectural boundary affecting reliable development or operation, and produce an evidence-grounded repository sensemaking brief. Do not modify the target repository." \
  --workflow architectural-review-planning-workflow \
  --mode guided_execution \
  --executor claude-code \
  --controlled-experiment \
  --model claude-sonnet-5 \
  --gate-decision auto-approve \
  --repo-root "H:/scratch/stage1-auteur-rerun-2/framework" \
  --target-repo "H:/scratch/stage1-auteur-rerun-2/target-auteur" \
  --log-dir "H:/scratch/stage1-auteur-rerun-2/logs"
```

Invoked exactly once. Exit code 0 (runtime completed and reported a FAILED
workflow status; the process itself did not crash). `raw/stdout.log` and
`raw/stderr.log` were not preserved in this evidence package; the invocation,
model-enforcement, target-safety, and validator-result claims in this
document are independently corroborated by `raw/tool-call-trace.jsonl`,
`raw/run-ledger.jsonl`, `raw/workflow_summary.json`, and
`raw/validator-output-authoritative.json` instead.

## Runtime enforcement result

```text
requested model = claude-sonnet-5
all reported models = ['claude-sonnet-5']
model_match = true
distinct reported model count = 1
fallback = none
retry = none
```

Source: `raw/tool-call-trace.jsonl` (`requested_model`, `reported_models`,
`reported_model`, `model_match` fields).

## Target safety result

```text
Target HEAD before: b40db654e0df9e90074f7ad85b40d7362378e07d
Target HEAD after:  b40db654e0df9e90074f7ad85b40d7362378e07d
git status --porcelain (before): empty
git status --porcelain (after):  empty
git diff --exit-code (after): exit 0, no output
git diff --cached --exit-code (after): exit 0, no output
target-manifest-pre.txt vs target-manifest-post.txt: no diff (1044 files, identical)
Write-tool attempts observed against target-auteur in trace: 0
  (2 tool_name="Write" entries in trace overall, both targeting the
  framework artifact path (artifacts/05-orchestration-run/
  repository_sensemaking_brief.md under the framework clone), none
  targeting target-auteur; 17 Read "completed" + 18 Read "observed"
  entries reference target-auteur paths -- read-only access only)
Target mutation = none
Completed target writes = 0
```

Raw manifests: `raw/target-manifest-pre.txt`, `raw/target-manifest-post.txt`.

## Structural validation result

The in-run orchestrator's own Phase 1 unified validator step and a separate,
manually-invoked authoritative check (per package §6 step 6, with both
`--repo-root` and `--target-repo` set, to avoid repeating Evidence 0013's
missing-`--target-repo` mistake) agree:

```json
{
  "valid": false,
  "artifact_id": "unknown",
  "validator": "validate-and-report.py",
  "errors": [
    {
      "error_id": "unknown.artifact_id.missing_field",
      "error_type": "missing_field",
      "field": "artifact_id",
      "message": "Cannot determine artifact_id from file. Generic validator requires artifact_id to be present in YAML block."
    }
  ]
}
```

Full output: `raw/validator-output-authoritative.json`.

This is a **new** failure mode, distinct from Evidence 0013's three
`EVIDENCE_QUOTE_NOT_FOUND` errors — the PR #91 deterministic quote-extraction
fix and the PR #92/#94 `weakness_type` safeguard were never exercised,
because validation halted earlier, on a missing `artifact_id` field in the
generated brief's machine-readable YAML block. The remediation this package
shipped (issues #89/#90/#93) addressed the three specific mechanisms Evidence
0013 exposed; it did not address (and was never claimed to address) artifact
metadata completeness, which is a separate gap.

Per the package's §9 structural-result rules: since validator exit was
non-zero and a blocking error was present, **structural result = FAIL**.

## Substantive review

Not reached. Per package §10/§12, substantive review is gated on structural
PASS, which did not occur.

## Usefulness review

Not reached. Per package §11/§12, usefulness review is gated on structural
and substantive PASS.

## Final classification

```text
STAGE 1 FAIL
```

No repair of the artifact was attempted. No rerun occurred or is authorized
by this evidence package. Historical Evidence 0013 and PR #78 are untouched
by this run.

## Files preserved

- `AUTHORIZATION.md`
- `EVIDENCE.md` (this file)
- `raw/run_log.md`, `raw/implementation_report.md`, `raw/workflow_summary.json`
- `raw/repository_sensemaking_brief.md` (raw generated artifact, unedited)
- `raw/tool-call-trace.jsonl`, `raw/run-ledger.jsonl`
- `raw/target-manifest-pre.txt`, `raw/target-manifest-post.txt`
- `raw/validator-output-authoritative.json`

Not preserved in this evidence package: `raw/stdout.log`, `raw/stderr.log`,
`raw/validator-stderr.log`. Their absence does not affect the conclusions
above, which are independently corroborated by the files that are
preserved (see "Exact invocation" above).

## Explicit no-rerun statement

This run's single authorized invocation has been consumed. No automatic or
manual retry, repair, or rerun was performed or is authorized by this
evidence package. A further attempt would require a new, separate owner
authorization.
