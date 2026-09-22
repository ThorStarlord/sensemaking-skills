# Final Version 1.0 Release Evidence Boundary

**Status:** release-finalization support contract  
**Scope:** final `1.0.0` readiness evidence only  
**Authority:** mechanical evidence consumption; no release-owner decision, live GitHub verification, or publication authority

## Purpose

Final release evidence is produced **after** an exact source head has been
qualified. Recording that evidence must not mutate the source bytes whose identity
it attests.

Therefore final readiness consumes provenance-bound sidecars that are outside
tracked source identity:

```text
exact final source head
-> Product Validation PASS
-> Release Candidate Distribution PASS
-> final wheel/sdist SHA-256 records
-> explicit release-owner authorization
-> validate-release-readiness.py
-> READY / BLOCKED
```

The default sidecar directory is:

```text
.release-evidence/
```

It is gitignored. Operators may instead pass explicit paths outside the repository.

```text
sidecar recorded
!= source bytes changed

recorded workflow result
!= independently queried GitHub truth

owner authorization file
!= authorization synthesized by tooling

READY
!= package published
```

## Exact-head CI evidence

Default path:

```text
.release-evidence/ci.yaml
```

Shape:

```yaml
schema_version: 1
release_version: "1.0.0"
source_sha: "<40-character exact final Git HEAD>"
product_validation:
  workflow: "Product Validation"
  run_id: 123456789
  conclusion: success
release_candidate_distribution:
  workflow: "Release Candidate Distribution"
  run_id: 123456790
  conclusion: success
```

The final readiness validator checks:

- schema version;
- release version against `release-v1.0.yaml`;
- `source_sha` against current Git HEAD;
- required workflow identities;
- positive integer run IDs;
- `success` conclusions.

The file is an explicit evidence record. The validator does not call GitHub to
prove that the run IDs exist.

## Release-owner authorization

Default path:

```text
.release-evidence/owner-authorization.yaml
```

Shape:

```yaml
schema_version: 1
release_version: "1.0.0"
source_sha: "<40-character exact final Git HEAD>"
decision: AUTHORIZE_FINAL_1_0_PUBLICATION
authorized_by: "<release owner identity>"
authorized_at: "<timestamp>"
```

Only the release owner may supply this decision. The validator checks the
recorded decision and exact source binding; it never creates the authorization.

## Artifact digests

Default path:

```text
dist/SHA256SUMS
```

An explicit path may be supplied with `--artifact-digests`, including a
downloaded `release-SHA256SUMS.txt` from Release Candidate Distribution.

The digest record must contain SHA-256 entries for both final artifacts:

```text
sensemaking_skills-1.0.0-py3-none-any.whl
sensemaking_skills-1.0.0.tar.gz
```

The validator checks record shape and expected artifact coverage. It does not
recompute hashes unless the artifacts themselves are separately verified by the
distribution workflow/operator.

## Final gate invocation

Using defaults:

```bash
python scripts/validate-release-readiness.py --repo-root .
```

Using explicit out-of-tree evidence:

```bash
python scripts/validate-release-readiness.py \
  --repo-root . \
  --ci-evidence /secure/release/ci.yaml \
  --owner-authorization /secure/release/owner-authorization.yaml \
  --artifact-digests /secure/release/release-SHA256SUMS.txt
```

A `READY` result means the declared reduced-scope Version 1.0 release gates are
mechanically represented as complete for the exact current source head.

It does **not** establish:

- semantic usefulness;
- native-harness compatibility;
- cross-harness portability;
- publication success;
- correctness of the owner's decision;
- stronger claims than `release-v1.0.yaml` authorizes.
