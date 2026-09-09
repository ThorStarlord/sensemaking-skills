# Checked-In Qualification Evidence

This directory is the repository-owned landing zone for frozen external golden-path qualification attempts.

## Current empirical state

**No real-harness attempt is checked in by this package.**

The synthetic fixture under `tests/fixtures/external_golden_path/` is test data only and must never be copied here or cited as empirical product evidence.

## Future attempt layout

A checked-in attempt should use:

```text
qualification-evidence/
└── attempts/
    └── <attempt-id>/
        ├── attempt.yaml
        ├── evidence/
        │   └── ...
        └── qualification-evidence.json
```

`attempt.yaml` and its evidence files must satisfy `v0.3-external-golden-path-dogfood-v1`.

`qualification-evidence.json` must be generated from those exact bytes with:

```bash
python -m sensemaking_skills.qualification_evidence \
  qualification-evidence/attempts/<attempt-id> \
  --output qualification-evidence/attempts/<attempt-id>/qualification-evidence.json
```

A PR that changes `qualification-evidence/**` triggers the External Golden Path Qualification contract. CI validates each checked-in attempt structurally and requires its receipt to rebuild exactly from the supplied attempt bytes.

Structurally valid recorded failures may be preserved. They remain `qualified: false` and must not be rewritten into PASS attempts.

```text
checked-in receipt != empirical truth
synthetic fixture != real-harness evidence
valid recorded FAIL != qualified PASS
```
