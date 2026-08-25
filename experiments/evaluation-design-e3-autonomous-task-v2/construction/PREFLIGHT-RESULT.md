# Autonomous Task v2 — Preflight Result (Task 22)

> **SUPERSEDED (historical, frozen at `0ffb564b`).** This is the original
> construction-era preflight result, run at the old freeze
> `0ffb564b67eb7fcac3c1a2c8a1365ed6b2a0e6c5`. The re-frozen pilot instrument
> (current product freeze `a7b957d`) is preflighted separately in
> `AUTONOMOUS-TASK-V2-LOCK-RECORD-RE-FREEZE.md` §4 and `RE-FREEZE-PROVENANCE.md`
> §3. Do not use this old result as the dispatch gate for a `a7b957d` run.

## Setup

A real standalone clone was created at the frozen SHA — not this worktree,
not a `git worktree add` linked checkout:

```
git clone --no-local \
  "H:/GithubRepositories/sensemaking-skills/.claude/worktrees/autonomous-task-v2-candidate-construction" \
  <fresh-parent-dir>/clone
git -C <clone> checkout 0ffb564b67eb7fcac3c1a2c8a1365ed6b2a0e6c5
git -C <clone> remote remove origin
```

`--no-local` performs a real object copy (not a hardlink-sharing clone), and
the `origin` remote — which would otherwise carry a local filesystem path —
was removed immediately after checkout, before the gate ran, so
`clone-remote-has-no-local-path` is exercised meaningfully rather than
trivially passed. The clone's parent directory was created fresh and
contains nothing but the clone itself.

The `AUTONOMOUS-TASK-V2-PREFLIGHT-GATE.sh` script itself was read from the
17-file design package at
`experiments/evaluation-design-e3-autonomous-task-v2/` in this repository's
main checkout — per `00-HANDOFF-VERIFICATION.md` §1, that package is "the
normative input to this phase" and was never committed into this isolated
construction worktree's own git history (it predates and sits outside this
branch). It was invoked, not edited, consistent with the plan's "Modify
(invoke, not edit)" framing for this file.

## Oracle self-test command

T2's guardrail test, run against the unmodified frozen-SHA fixture
(expected to reflect the *unsolved* state — the T2 pilot's task asks for a
change this test doesn't yet reflect):

```
python3 -m pytest "<clone>/tests/test_field_contract_agreement.py" -q 2>/dev/null | sed -E 's/ in [0-9.]+s ?//'
```

The `sed` filter strips pytest's non-deterministic wall-clock duration
suffix (e.g. `in 0.91s`) from the `-q` summary line — without it, the same
command produces a different byte sequence on every invocation and the
gate's hash-match check can never pass. Confirmed deterministic by running
it twice independently and comparing sha256 (both `29d19ead...`) before
using it as the gate's `--oracle-self-test-command`.

## Task bundle

`--task-bundle` / `--task-bundle-sha256` used T2's agent-visible bundle
from Task 21: `pilot/bundles/agent-visible/T2.md`,
sha256 `021fcd90156be5c0e87ead018a22d2353620c123765c728c89a8f9018546f525`.

## Attempt 1 — FAIL (found and fixed)

```
bash AUTONOMOUS-TASK-V2-PREFLIGHT-GATE.sh \
  --clone-dir <clone> --frozen-sha 0ffb564b67eb7fcac3c1a2c8a1365ed6b2a0e6c5 \
  --out-dir <out-dir> --regime-dir <design-package-dir> \
  --run-state-dir <run-state-dir> \
  --task-bundle <agent-visible-bundle-path> \
  --task-bundle-sha256 021fcd90156be5c0e87ead018a22d2353620c123765c728c89a8f9018546f525 \
  --oracle-self-test-command 'python3 -m pytest "<clone>/tests/test_field_contract_agreement.py" -q' \
  --expected-oracle-self-test-sha 98e0b49edede7f52779b488413b5fe5f8e6385d8c4d6d112e8bba3ca3e12b0bd
```

Timestamp: 2026-08-21T01:01:56Z. Exit code: 1. `PASS=16 FAIL=1 UNVERIFIABLE=0`.

```
FAIL           oracle-self-test                         self-test output sha256=8d56ddcc3d6f13b77e37868e3294f0b9d5f288bf8d282f7ddcc4734881be9fa7 expected=98e0b49edede7f52779b488413b5fe5f8e6385d8c4d6d112e8bba3ca3e12b0bd
```

**Root cause**: the `--expected-oracle-self-test-sha` was precomputed from
one run of the raw `pytest -q` command, but that command's stdout includes
a timing suffix (`in 0.91s`) that changes every invocation — the same
command necessarily hashes differently on the gate's own re-run. This is a
real condition (a non-deterministic self-test command cannot pass a
hash-match check by construction), not a gate defect, an environment
issue, or something to waive — per the script's own no-waiver design and
the plan's Step 4 instruction, the actual condition was fixed: the command
was changed to strip the non-deterministic suffix before hashing (see
"Oracle self-test command" above), and the expected hash was recomputed
against the now-deterministic output.

## Attempt 2 — PASS (final, clean)

```
bash AUTONOMOUS-TASK-V2-PREFLIGHT-GATE.sh \
  --clone-dir <clone> --frozen-sha 0ffb564b67eb7fcac3c1a2c8a1365ed6b2a0e6c5 \
  --out-dir <out-dir> --regime-dir <design-package-dir> \
  --run-state-dir <run-state-dir> \
  --task-bundle <agent-visible-bundle-path> \
  --task-bundle-sha256 021fcd90156be5c0e87ead018a22d2353620c123765c728c89a8f9018546f525 \
  --oracle-self-test-command 'python3 -m pytest "<clone>/tests/test_field_contract_agreement.py" -q 2>/dev/null | sed -E '"'"'s/ in [0-9.]+s ?//'"'"'' \
  --expected-oracle-self-test-sha 29d19ead61a379113a2df8c577553f8148e77d835bd0ca67d3cd69e25e09ef82
```

Timestamp: 2026-08-21T01:02:43Z. Exit code: **0**. `PASS=17 FAIL=0 UNVERIFIABLE=0`.

Full output:

```
Autonomous Task v2 preflight — 2026-08-21T01:02:43Z
clone_dir=<clone> frozen_sha=0ffb564b67eb7fcac3c1a2c8a1365ed6b2a0e6c5
---
PASS           clone-is-git-repo                        <clone>
PASS           clone-head-matches-frozen-sha            0ffb564b67eb7fcac3c1a2c8a1365ed6b2a0e6c5
PASS           clone-working-tree-clean                 no tracked modifications
PASS           clone-is-standalone-not-worktree         .git is a real directory
PASS           no-known-sibling-experiment-dirs         none found under <clone>/experiments
PASS           clone-remote-has-no-local-path           no local-filesystem-path remotes configured
PASS           clone-worktree-list-shows-self-only      1 entry
PASS           clone-parent-directory-is-uncrowded      no unapproved entries in <clone parent>
PASS           clone-no-alternate-object-store          no alternates file present
PASS           clone-common-dir-is-self                 <clone>/.git
PASS           regime-file-present:R0-ROBUST            sha256=5cab71b47464ddeb4e3537d26dd58540bd88249b6f44d319f46ca008c0585ea9
PASS           regime-file-present:R1-LEAN              sha256=6a7147cdfb726fc6a2f216dd39fdf3335daad08447a98178b5ae7b2dd24f4861
PASS           regime-file-present:R2-ESCALATION        sha256=ab94cc5480a8e4410bcc9df1f788f36f622625c277b8c917170caf8e568e3714
PASS           telemetry-destination-writable           <out-dir>
PASS           run-state-dir-is-fresh                   <run-state-dir> does not exist yet (fresh)
PASS           oracle-self-test                         self-test output matches expected sha256=29d19ead61a379113a2df8c577553f8148e77d835bd0ca67d3cd69e25e09ef82
PASS           task-bundle-matches-frozen-hash           task bundle sha256 matches expected: 021fcd90156be5c0e87ead018a22d2353620c123765c728c89a8f9018546f525
ENV_LIMIT      ambient-scope-runtime-enforcement          AMBIENT_SCOPE_NOT_TECHNICALLY_ENFORCED — this script cannot verify or enforce that the executing agent's filesystem access is bounded to $CLONE_DIR during the run; verify via the harness/sandbox layer, not this script
---
PASS=17 FAIL=0 UNVERIFIABLE=0
```

`FAIL_COUNT == 0` and `UNVERIFIABLE_COUNT == 0`, exit code `0`, exactly as
the plan's Step 3 expected condition specifies. The `ENV_LIMIT` line on
`ambient-scope-runtime-enforcement` reports
`AMBIENT_SCOPE_NOT_TECHNICALLY_ENFORCED` — per the script's own design this
is a permanent disclosure, not a failure, and is expected on every run.

## Result

**PREFLIGHT: CLEAN.** All 17 checkable conditions PASS, zero FAIL, zero
UNVERIFIABLE. The one genuine failure encountered (attempt 1) traced to a
real condition in the self-test command construction, not a gate defect or
an environment limitation, and was fixed per the script's explicit
no-waiver design before re-running — not bypassed.
