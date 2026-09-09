# Qualification Evidence Receipts

**Status:** repository-owned qualification evidence contract  
**Scope:** deterministic receipts for structurally valid frozen external golden-path attempts  
**Empirical boundary:** receipt generation does not attest real-harness origin

## Purpose

`sensemaking_skills.external_qualification` already decides whether a frozen attempt satisfies the external golden-path package contract. Package 3 adds a second, narrower artifact:

```text
frozen attempt package
        ↓
external qualification verifier
        ↓
structurally valid attempt
        ↓
qualification evidence receipt
```

The receipt makes the exact verified package portable and reconstructible. It binds:

- the exact `attempt.yaml` SHA-256;
- every evidence file the verifier actually consumed and its exact SHA-256;
- the declared Sensemaking candidate identity;
- runtime/harness/adapter identity;
- external target repository identity;
- Campaign identity;
- recorded `PASS`, `FAIL`, or `INVALID` outcome;
- whether the external verifier classified that exact package as qualified.

## Claim ceiling

A qualification evidence receipt means only:

> These exact bytes formed a structurally valid frozen attempt, and the repository verifier produced this exact outcome for them.

It does **not** mean:

```text
receipt exists != semantic truth
receipt exists != real-harness origin proven
fixture receipt != empirical product evidence
qualified receipt != universal repository support
qualified receipt != universal harness support
```

The deterministic repository code cannot observe the historical fact that a human actually ran Claude Code, Codex, OpenCode, or another harness. That origin event must be established by the frozen harness-native evidence and the external operator protocol. The receipt deliberately carries `evidence_scope: mechanically_verified_frozen_attempt` rather than an empirical-attestation field.

## Receipt shape

The JSON receipt contains:

```text
schema_version
evidence_scope
protocol
attempt_id
manifest_sha256
package_sha256
outcome
qualified
sensemaking_candidate
runtime
external_target
campaign_id
verified_evidence[]
receipt_sha256
```

`package_sha256` is the canonical digest of:

```text
manifest SHA-256
+ sorted verified evidence path/SHA-256 bindings
```

`receipt_sha256` is the canonical digest of the complete receipt body excluding only `receipt_sha256` itself.

This creates two distinct boundaries:

```text
package_sha256 -> exact attempt package bytes
receipt_sha256 -> exact derived qualification evidence record
```

## Create a receipt

After freezing an attempt:

```bash
python -m sensemaking_skills.external_qualification <attempt-dir> --json
python -m sensemaking_skills.qualification_evidence \
  <attempt-dir> \
  --output qualification-evidence.json
```

Receipt creation is allowed only when the attempt is **structurally valid**. A structurally valid recorded `FAIL` or `INVALID` can receive a receipt because failed attempts are evidence too. Their receipt preserves `qualified: false` and their non-PASS outcome.

A structurally invalid attempt cannot produce a receipt.

The writer is append-only at the destination path: it refuses to overwrite an existing receipt.

## Verify an existing receipt

```bash
python -m sensemaking_skills.qualification_evidence \
  <attempt-dir> \
  --verify qualification-evidence.json
```

Verification rebuilds the expected receipt from the supplied attempt and requires exact equality. It fails closed when:

- the attempt package is no longer structurally valid;
- evidence bytes changed or disappeared;
- the attempt manifest changed;
- receipt fields were added, removed, or rewritten;
- `receipt_sha256` no longer matches the receipt body;
- the receipt belongs to different attempt bytes.

## GitHub Actions behavior

The manual **External Golden Path Qualification** workflow now produces two different artifacts:

```text
external-qualification-result.json
external-qualification-evidence.json   # only for structurally valid attempts
```

The result artifact is uploaded even when the attempt is invalid so failure remains inspectable.

The evidence receipt is uploaded only when the external verifier reports a structurally valid package (`PASS`, `FAIL`, or `INVALID`). A verifier-contract failure does not receive an evidence receipt.

This prevents:

```text
invalid package -> durable qualification evidence
```

while preserving:

```text
valid recorded failure -> durable failure evidence
```

## Synthetic fixture boundary

`tests/fixtures/external_golden_path/pass/` remains synthetic. Tests may build a receipt from it to prove receipt mechanics, but that receipt is still synthetic contract evidence.

```text
synthetic fixture
+ deterministic receipt
!= empirical real-harness qualification
```

No checked-in real external attempt currently exists merely because this receipt machinery exists. A real-harness PASS still requires an actual external harness attempt frozen under the protocol described in `docs/external-golden-path-verifier.md`.
