# Validated artifact ingestion — P4 + P11 release portability

P4 connects agent-produced Sensemaking artifacts to durable campaign evidence
without granting epistemic status merely because a file exists. P11 makes that
same canonical validation boundary available from the installed distribution so
a release user does not need a separate Sensemaking source checkout.

## Trust boundary

```text
agent / Skill produces artifact
        ↓
exact source bytes snapshotted
        ↓
canonical scripts/validate-and-report.py
        ↓
selected artifact validator
        ↓
valid=true
        ↓
content-addressed artifact copy
        ↓
append-only admission receipt (written last)
        ↓
campaign evidence
```

The active agent still decides **why** an artifact was produced, what it means,
and whether it changes a decision. P4 decides only whether exact bytes passed
the repository's canonical mechanical validation boundary and can therefore be
admitted as durable evidence.

## File existence is not evidence admission

The campaign workspace now distinguishes three things:

```text
artifacts/<artifact_id>/<sha256>.<ext>
    Canonically validated artifact copies. A file under artifacts/ is ignored
    as campaign evidence unless an admission receipt binds it.

admissions/<artifact_id>/<receipt-sha256>.yaml
    Append-only receipt binding exact artifact bytes to the exact validator
    result and validator identities.

evidence/**
    Ordinary raw evidence. P1 semantics are preserved: physically contained
    regular files here remain directly citable evidence.
```

Therefore:

```text
file under artifacts/
    != validated artifact
    != admitted campaign evidence
```

Dropping a file manually into `artifacts/` does not make it available to a
campaign transition, responsibility dependency, or handoff.

## Admission receipt

Each receipt records:

- campaign id;
- artifact id;
- workspace-relative artifact ref;
- SHA-256 of exact artifact bytes;
- selected validator identity;
- canonical validation timestamp;
- SHA-256 of `scripts/validate-and-report.py`;
- SHA-256 of the selected validator script;
- SHA-256 of the full validator result;
- the full unified validator result;
- schema version.

The receipt itself is content-addressed: its filename is the SHA-256 of its
canonical payload. Reconstruction rejects receipt-field drift, result drift,
artifact-byte drift, campaign-id mismatch, unsafe refs, missing artifact bytes,
and symlink/reparse escapes.

The router/validator digests are historical provenance. P4 does not require the
current installation to retain those exact validator bytes merely to read a
past campaign; it records which exact validator bytes granted admission at the
time.

## Crash ordering

Admission uses a deliberately small ordering rule:

1. validate an immutable temporary snapshot of the source bytes;
2. write/verify the content-addressed artifact copy;
3. write the admission receipt **last**.

If the process stops between steps 2 and 3, the artifact copy is only an orphan
file under `artifacts/`. `CampaignStore.evidence_refs()` ignores it. A retry may
reuse the same content-addressed copy and finish the receipt safely.

No P4 receipt means no P4 artifact evidence.

## CLI

Normal installed-distribution use requires no framework checkout:

```bash
sensemaking-skills campaign ingest \
  --workspace /path/to/CMP-0001 \
  --artifact /path/to/repository_sensemaking_brief.md \
  --target-repo /path/to/target \
  --json
```

`--target-repo` is optional and is forwarded to target-aware validators.
`--probe-report` is also optional and preserves the existing same-episode Probe
Engine authority path used by `validate-brief.py`.

For validator development or compatibility testing, an explicit source checkout
may override the installed runtime:

```bash
sensemaking-skills campaign ingest \
  --workspace /path/to/CMP-0001 \
  --artifact /path/to/artifact.md \
  --framework-root /path/to/sensemaking-skills \
  --json
```

An explicit override is authoritative. If it is malformed or missing the
canonical router, ingestion fails closed; the CLI does not silently substitute
the packaged runtime after the caller selected a checkout.

A successful JSON result uses:

```json
{
  "ok": true,
  "code": "ARTIFACT_ADMITTED",
  "artifact_id": "repository_sensemaking_brief",
  "artifact_ref": "artifacts/repository_sensemaking_brief/<sha256>.md",
  "admission_ref": "admissions/repository_sensemaking_brief/<receipt-sha256>.yaml",
  "artifact_sha256": "...",
  "validator": "validate-brief.py",
  "validation_timestamp": "...",
  "router_sha256": "...",
  "validator_sha256": "..."
}
```

The canonical router may dispatch either to a specialized validator or to the
generic `validate-artifact.py` fallback. P4 uses the same unified JSON contract
for both paths; it does not treat the fallback as a weaker admission mechanism.

## Failure taxonomy

Campaign CLI exit codes from P3 remain unchanged. P4 adds two artifact-specific
failure classes:

| Exit | Code | Meaning |
| ---: | --- | --- |
| `5` | `ARTIFACT_VALIDATION_REJECTED` | The canonical validator ran successfully and rejected the artifact. No evidence is admitted. |
| `6` | `ARTIFACT_VALIDATOR_ERROR` | The canonical router/validator boundary could not be executed or trusted. This is not evidence that the artifact itself is invalid. |

Workspace/integrity failures continue to use the P3 campaign exits (`3`/`4`).
Persistence failures during the content-addressed copy or receipt write are
classified as workspace failures rather than leaking as an unrelated generic
process error.

This distinction prevents an infrastructure failure from being mislabeled as a
negative semantic or validation finding about the artifact.

## Installed validator runtime

The repository-root `scripts/` and `skills/` trees remain the canonical sources
for validator implementation and contracts. P11 does **not** introduce a second
manually maintained validator implementation.

During wheel construction, the existing custom `build_py` step derives a
self-contained runtime beneath the built package:

```text
sensemaking_skills/validator_runtime/
├── scripts/   # exact build-time copy of canonical repository scripts/
├── skills/    # exact build-time copy of canonical repository skills/
└── docs/
    └── canonical-vocabulary.yaml
```

`campaign ingest` uses that installed runtime by default. In editable/source
checkout development, when the generated runtime is not present, the service
uses the one exact repository root containing the imported package. It does not
search arbitrary directories or pick a "nearby" validator checkout.

The admission receipt continues hashing the exact router and selected validator
bytes that actually ran. Packaging therefore changes deployment portability,
not the P4 provenance or trust model.

The release qualification must prove that an installed wheel can:

```text
campaign init
→ campaign ingest without --framework-root
→ validator accept/reject exact bytes
→ preserve router/validator SHA-256 provenance
→ reconstruct admitted evidence
```

from a working directory outside the Sensemaking source checkout.

## Compatibility with P1–P3 workspaces

P1–P3 campaign workspaces did not contain `admissions/`. On first access under
P4+, an initialized legacy workspace receives one empty structural
`admissions/` directory. This migration grants no evidence status and leaves
existing raw `evidence/` refs unchanged.

Pre-P4 files that happen to exist under `artifacts/` are **not** grandfathered
as validated evidence. If an older campaign state or transition depended on one
of those paths as evidence, P4 reconstruction fails closed until the relevant
artifact can be canonically validated and admitted. The migration never creates
a receipt retroactively and never infers that a historical file must have been
valid merely because earlier code could see it.

This is an intentional trust-boundary tightening rather than a silent backward-
compatibility shortcut.

## Non-goals

P4/P11 portability does **not**:

- interpret artifact semantics;
- choose a responsibility or capability;
- automatically advance campaign state;
- grant execution authority;
- make every artifact directory entry trustworthy;
- replace artifact-specific validators;
- create a semantic truth validator;
- silently fall back from an explicitly selected bad framework checkout;
- maintain a second hand-edited validator implementation inside the package.

P5 may use admitted artifact refs as inputs to explicit **agent-authored**
decisions. That step preserves the same separation: validated evidence is
available to judgment; it is not judgment itself.
