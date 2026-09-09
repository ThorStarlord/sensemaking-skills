# Product / Lab Boundary

**Status:** Product boundary contract  
**Scope:** Packaging, release authority, CI, and retained research machinery

Sensemaking Skills contains two deliberately different surfaces in one source
repository:

1. the **shipped product**, centered on agent-native Sensemaking Campaigns,
   durable reconstruction, artifact admission, decisions, reconciliation,
   lineage, handoff/resume, harness adapters, and packaged Skills; and
2. the **retained research lab**, which preserves the Two-Lane experiment
   machinery and empirical qualification infrastructure used to investigate
   earlier product questions.

Keeping both histories in the repository is useful. Shipping both as one
runtime product is not.

## Shipped product

The Python distribution includes the ordinary `sensemaking_skills` package
except for the source-only lab package families listed below. Product behavior
is qualified by `.github/workflows/validation.yml`.

Important product surfaces include:

- `sensemaking_skills.campaign_semantics`
- `sensemaking_skills.campaigns`
- Campaign CLI / decision / handoff / lineage / reconciliation commands
- harness adapters and `setup-skills`
- path containment and ordinary repository-sensemaking support
- packaged canonical Skill trees

The product wheel has only the dependencies needed by those surfaces. In
particular, `jsonschema` and `rfc8785` are not core runtime dependencies.

## Source-only lab

The following package families remain version-controlled and testable from a
source checkout, but are intentionally excluded from the published wheel:

- `sensemaking_skills.campaign_validation`
- `sensemaking_skills.campaign_accounting`
- `sensemaking_skills.exploratory_authorization`
- `sensemaking_skills.exploratory_execution`

Associated research surfaces include `scripts/execution_infra/`,
`tests/campaign_accounting/`, `tests/campaign_preparation/`,
`tests/execution_infra_tests/`, `experiments/`, and `docs/experiments/`.

Exclusion from the product wheel is **not** deletion, deprecation of the
historical evidence, or a claim that the experiments were invalid. It is a
runtime/product boundary: research mechanisms do not silently become product
capabilities.

Lab dependencies are declared in `requirements-lab.txt`. Lab maintenance is
qualified by `.github/workflows/lab-validation.yml`, which is explicitly
runnable and is also path-triggered when lab surfaces change.

## Release authority

`pyproject.toml` is the single release/package metadata authority.

- The release version is declared only in `[project].version`.
- `setup.py` contains only the custom build hook needed to derive packaged
  Skill trees from the canonical repository-root `skills/` directory.
- `package.json` is private repository tooling metadata and declares no release
  version.
- `sensemaking_skills.__version__` is derived at runtime from installed Python
  distribution metadata rather than copied into source.
- generated `src/sensemaking_skills.egg-info/` metadata is ignored and must not
  be committed.

This removes the previous four-way release-authority coupling between
`pyproject.toml`, `setup.py`, `package.json`, and `__init__.py`.

## CI authority

Two workflows have different jobs:

- **Product Validation** (`.github/workflows/validation.yml`) is the ordinary
  PR/main gate for shipped product behavior and package boundaries.
- **Lab Validation** (`.github/workflows/lab-validation.yml`) preserves the
  research suites and runs when lab paths change or when explicitly dispatched.

The pre-split all-in-one validator workflow is retained verbatim under
`docs/archive/ci/validator-ecosystem-pre-core-lab-split.yml` as historical
implementation evidence. It is outside `.github/workflows/` and therefore no
longer executes automatically.

## Invariant

```text
retained research evidence
!= shipped product capability
!= blocking product CI
```

The source repository may continue to hold all three. Their authority is now
explicit rather than inferred from co-location.
