# External Golden-Path Qualification Verifier

**Status:** optional empirical qualification / dogfood  
**Protocol:** `v0.3-external-golden-path-dogfood-v1`

This lane makes real-harness dogfood reproducible without turning Sensemaking Skills into a harness launcher or semantic router.

```text
real coding-agent harness run
        ↓
freeze exact attempt + evidence package
        ↓
deterministic package verifier
        ↓
QUALIFIED / NOT QUALIFIED
```

The verifier checks representation, exact byte identity, lifecycle coverage, no-repair boundaries, native Skill-invocation evidence, and fresh-context reconstruction evidence. It does **not** prove that submitted evidence is semantically truthful merely because it is well formed.

```text
valid evidence package
!= semantic truth
!= universal harness support
!= universal repository support
```

## Bounded claim

A passing attempt supports only:

> One exact Sensemaking Skills distribution completed the canonical Campaign golden path on one frozen external repository through one real supported coding-agent harness, with deterministic evidence reconstruction, no manual Campaign/artifact/validator-output repair, native `repo-sensemaker` invocation evidence distinct from Skill setup evidence, and fresh-context resume without prior chat supplied.

It does not prove universal repository support, universal harness support, correct Skill selection in every case, semantic truth, or execution authority.

## Why the harness run remains external

The GitHub qualification workflow does not launch Claude Code, Codex, OpenCode, or another coding-agent harness. Runtime invocation is the empirical event being qualified. The repository-owned lane starts after that run:

1. Freeze the exact Sensemaking distribution and external target identity.
2. Preserve harness-native evidence that `repo-sensemaker` was invoked.
3. Preserve Campaign lifecycle, handoff, and fresh-context evidence.
4. Compute SHA-256 for every cited evidence file.
5. Freeze the attempt without rewriting failed attempts into passes.
6. Run the deterministic verifier locally or through the manual GitHub Actions lane.

This preserves the P10 distinction:

```text
Skill copied to discovery root
!= harness observed Skill
!= Skill invoked
!= execution authorized
```

## Attempt package

```text
<attempt-dir>/
├── attempt.yaml
└── evidence/
    ├── setup.yaml
    ├── native-invocation.yaml
    ├── lifecycle.*
    ├── handoff.yaml
    └── resume.yaml
```

Evidence filenames may differ. `attempt.yaml` binds exact relative paths and SHA-256 values. Do not edit a failed attempt into a passing attempt; create a new attempt ID whenever candidate bytes, target bytes, runtime identity, or prohibited-repair boundaries change.

## Required manifest identity

`attempt.yaml` records:

- protocol and attempt ID;
- UTC start timestamp;
- exact Sensemaking commit, tree, distribution filename/hash, and version;
- OS, Python, harness/version, adapter target, and scope;
- external repository, branch, commit, tree, and bounded engineering goal;
- Campaign ID and isolated workspace declaration;
- explicit `false` values for manual Campaign repair, artifact repair, validator-output repair, and prior chat supplied to the fresh agent.

The external target may not be `ThorStarlord/sensemaking-skills`.

## Native Skill evidence

The manifest cites two **distinct** records: Skill setup and native invocation. Setup proves placement only and cannot substitute for invocation.

Setup receipt fields:

```yaml
evidence_kind: skill_setup
harness: claude
adapter_target: claude
adapter_scope: project
skill: repo-sensemaker
destination: <resolved discovery destination>
```

Native invocation receipt fields:

```yaml
evidence_kind: native_skill_invocation
harness: claude
skill: repo-sensemaker
session_id: <source-session-id>
invocation_id: <harness-record-id>
observed_at: "<UTC timestamp>"
source: claude_code_native_log
```

Allowed native sources are `claude_code_native_log`, `codex_native_log`, `opencode_native_log`, or `other_native_log`, matched to the declared harness. Filesystem inspection of installed Skills is not invocation evidence.

## Canonical lifecycle

The manifest records these checkpoints in exact order:

```text
repository_diagnosis
artifact_admission
responsibility_authority_decision
capability_inspection
bounded_work
work_evidence
reconciliation
reconciliation_disposition
durable_transition
lineage_inspection
handoff
fresh_context_resume
terminal_or_continue
```

Each checkpoint contains `id`, `status: PASS|FAIL|NOT_REACHED`, and digest-bound evidence references. `PASS` and `FAIL` require evidence. `NOT_REACHED` cannot claim evidence. After a failed/not-reached checkpoint, later checkpoints cannot return to `PASS` in the same frozen attempt.

Qualification additionally requires every checkpoint to pass, with the native invocation explicitly bound to `repository_diagnosis`, the handoff receipt bound to `handoff`, and the fresh-context receipt bound to `fresh_context_resume`.

## Fresh-context boundary

The source session must end before resume. The resume session must have a distinct ID and receive no prior chat transcript. The resume receipt binds the exact SHA-256 of the handoff receipt, proving which persisted handoff was consumed.

## Outcome

`outcome.classification` is `PASS`, `FAIL`, or `INVALID`. A structurally valid `FAIL` remains a valid historical record but is not qualified. A `PASS` outcome is rejected unless every canonical lifecycle checkpoint passes.

## Deterministic verifier

Run locally:

```bash
python -m sensemaking_skills.external_qualification <attempt-dir>
```

Machine-readable output:

```bash
python -m sensemaking_skills.external_qualification <attempt-dir> --json
```

Exit codes:

| Code | Meaning |
|---:|---|
| `0` | evidence package is qualified |
| `2` | package contract or integrity is invalid |
| `3` | package is structurally valid but records a non-PASS outcome |

`--structural-only` succeeds for a structurally valid recorded FAIL/INVALID attempt but never converts it into qualification.

## Manual GitHub Actions lane

Use **External Golden Path Qualification** only after a real harness attempt has been frozen on a branch/ref. Supply the repository-relative `attempt_dir`. The workflow checks out the exact selected SHA, installs the exact checked-out package, runs the verifier, and uploads `external-qualification-result.json` even on failure.

The workflow consumes no model-provider credentials and does not mutate the external target.

## Synthetic fixture boundary

`tests/fixtures/external_golden_path/pass/` is a synthetic contract fixture, not empirical product evidence. Its purpose is to prove verifier mechanics. Green fixture tests do **not** establish real-harness product success.
