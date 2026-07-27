# Repository Sensemaking Brief

Reconstructed fixture (not a copy of the evidence directory) reproducing
Evidence 0013's real structural defect: Section 8 contains a malformed
doubled ```yaml fence (an inner ```yaml opened without closing the outer
one). The old document-wide regex safeguard matched this fence -- the
first ```yaml...``` pair in the document -- instead of the real Section 13
authoritative block, and incorrectly reported "no weakness_type key found."

## 8. Evidence excerpts

```yaml
<!-- REQUIRED: comment line inside the fence, as in the real defect -->

```yaml
evidence_excerpts:
  - file: CONTEXT.md
    lines: L1-L3
    quote: "irrelevant excerpt content"
    supports_claim: "irrelevant"
```
```

## 13. Machine-readable handoff

```yaml
artifact_id: repository_sensemaking_brief
schema_version: 1
weakness_type: Vocabulary Drift
required_inputs:
  - user_intent
immutable: true
```
