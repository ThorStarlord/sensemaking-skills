# Reduced-scope 1.0.0-rc.1 agent verification

This record contains repository-local verification performed on the
`codex/release-remediation-rc1` branch. It is candidate evidence only; it is
not exact-head CI evidence, external-harness evidence, or release-owner
authorization.

## Scope

The verified scope is limited to local Campaign persistence, validation,
semantic inspection, handoff/resume, bundle handling, documented CLI/Python
contracts, package boundaries, and release validators. Native harness,
portability, and semantic-usefulness claims remain excluded.

## Results

| Check | Command | Result |
| --- | --- | --- |
| Focused release suite | `pytest -q tests/test_public_api_contract.py tests/test_cli_contract.py tests/test_cli_json_contract.py tests/test_error_boundary_audit.py tests/test_distribution_hygiene.py tests/test_release_contract.py tests/test_release_readiness_gate.py tests/test_product_lab_boundary.py tests/test_contract_authority.py tests/test_current_documentation.py tests/test_setup_error_boundaries.py tests/test_version_upgrade.py tests/test_test_lane_isolation.py tests/integration/test_version_1_campaign_golden_path.py` | `34 passed in 6.64s` |
| Release contract | `python scripts/validate-release-contract.py --repo-root .` | `PASS` |
| Contract authority | `python scripts/validate-contract-authority.py --repo-root .` | `PASS` |
| Documentation currentness | `python scripts/validate-docs-currentness.py --repo-root .` | `PASS` |
| Product/lab boundary | `python scripts/validate-product-boundary.py` | `PRODUCT_LAB_BOUNDARY_VALID` |
| Error-boundary audit | `python scripts/validate-error-boundaries.py` | `ERROR_BOUNDARIES_VALID` |
| Diff hygiene | `git diff --check` | `PASS` |

## Distribution evidence

Fresh candidate artifacts in `dist-v1-release/` passed `twine check`:

```text
sensemaking_skills-1.0.0-py3-none-any.whl: PASSED
sensemaking_skills-1.0.0.tar.gz: PASSED
```

The wheel and sdist contain no source-only lab modules. Their candidate hashes
are recorded in the repository-level `SHA256SUMS` file. These artifacts were
built before an immutable release commit existed, so the hashes are not final
release provenance.

## Explicitly unresolved gates

- The working tree is not clean; no immutable release head is asserted.
- Exact-head CI evidence is not recorded.
- Release-owner authorization is absent.
- External harness, second-harness portability, and semantic-usefulness
  evidence remain intentionally unqualified.
- The unrestricted full test command has not completed within the available
  bounded run; the focused release lane above is the authoritative result for
  this record.
