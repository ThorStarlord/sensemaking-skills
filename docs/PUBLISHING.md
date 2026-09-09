# Publishing Sensemaking Skills v0.3.0

This document defines the publication boundary for the first Campaign-based release.

## Release authority

The sole literal release version is `pyproject.toml` `[project].version`.

A release candidate must be qualified from one exact commit by:

1. Product Validation;
2. Lab Validation;
3. Release Candidate Distribution.

The exact candidate head must be green in all required lanes before merge. Merge qualification does not itself publish to PyPI.

## Candidate distribution gate

`.github/workflows/release-candidate.yml`:

- checks out the exact PR head;
- validates the product/lab boundary;
- runs release-contract, Campaign schema-evolution, and external-verifier tests;
- builds both wheel and sdist;
- runs `python -m twine check dist/*`;
- requires exact `0.3.0` artifact identities;
- records SHA-256 digests;
- clean-installs both distributions;
- verifies CLI version/Campaign surface, schema v2, shipped/lab separation, packaged Skills, and packaged validator runtime;
- uploads the exact candidate distributions as a workflow artifact.

## Merge

Merge only the qualified exact head. If the candidate head moves, the previous qualification does not transfer to the new bytes.

After merge, verify that `main` contains the qualified tree/changes and that the merge ancestry is the intended one.

## Tag

Tagging is an explicit owner release action. The tag should identify the intended merged release commit, for example:

```bash
git tag v0.3.0 <release-commit>
git push origin v0.3.0
```

Do not tag an unqualified or stale candidate.

## PyPI publish workflow

`.github/workflows/publish.yml` triggers on `v*` tags. It:

1. checks out the tagged commit;
2. builds distributions;
3. runs `twine check`;
4. uploads only after metadata validation succeeds.

The workflow requires the configured `PYPI_API_TOKEN` secret.

## Post-publish verification

From a clean environment:

```bash
python -m venv /tmp/sensemaking-v030
# activate it
python -m pip install --upgrade pip
python -m pip install sensemaking-skills==0.3.0
sensemaking-skills --version
sensemaking-skills campaign --help
```

Verify the installed product still exposes Campaign schema v2 and does not expose retained source-only lab packages.

## Real-harness empirical evidence

The deterministic external qualification verifier ships in v0.3. A frozen real-harness attempt may be verified independently of publication timing.

A synthetic verifier fixture is not a real harness run. A real-harness PASS supports only the bounded claim encoded by that exact frozen evidence package; it does not establish universal harness compatibility or semantic truth.
