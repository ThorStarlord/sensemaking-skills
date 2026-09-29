# Release Authority Audit

**Status:** operator guide for `sensemaking-skills release audit`
**Authority:** subordinate to `docs/release-v1.0-contract.md` and
`docs/PUBLISHING.md`. This command inspects; it never publishes, tags, or
approves.
**Implementation:** `src/sensemaking_skills/release_authority.py`,
`src/sensemaking_skills/release_cli.py`

## Purpose

Answer one mechanical question: *do the repository-owned release identities
agree with each other and with local Git and workflow state?*

## Usage

```bash
sensemaking-skills release audit [--repo-root <path>] [--json]
```

- `--repo-root` defaults to `.`.
- `--json` emits one JSON object (keys sorted) instead of text.
- Exit code `0` when no finding has severity `error`; exit code `3` otherwise.

Text output prints the code (`RELEASE_AUTHORITY_VALID` or
`RELEASE_AUTHORITY_INVALID`), source and target versions, release status, Git
HEAD/tree/dirty state, each finding, and the explicit limit statement.

## What it reconciles

| Input | Where it comes from |
| --- | --- |
| Source version | `pyproject.toml` `project.version` |
| Target version and status | `release-v1.0.yaml` `release.version`, `release.status` |
| Current-identity documents | `README.md`, `STATUS.md`, `docs/PUBLISHING.md`, `docs/release-v1.0-contract.md` |
| Distribution workflow | `.github/workflows/release-candidate.yml` |
| Git identity | `git rev-parse HEAD`, `HEAD^{tree}`, `git status --porcelain` |

Identity relation rules:

- `development` status: source must equal `<target>.dev0`.
- `candidate` or `ready` status: source must equal target, and the working tree
  must be clean.
- any other status is invalid.

## Finding codes

| Code | Meaning |
| --- | --- |
| `RELEASE_METADATA_UNREADABLE` | `pyproject.toml` or `release-v1.0.yaml` could not be read or is malformed. |
| `RELEASE_IDENTITY_RELATION_INVALID` | Source/target relation violates the status rule above. |
| `RELEASE_STATUS_INVALID` | Unsupported `release.status`. |
| `RELEASE_AUTHORITY_DOCUMENT_MISSING` | A current-identity document is missing. |
| `RELEASE_SOURCE_NOT_PROJECTED` | A current-identity document does not contain the source version. |
| `RELEASE_TARGET_NOT_PROJECTED` | A current-identity document does not contain the target version. |
| `RELEASE_DISTRIBUTION_WORKFLOW_MISSING` | `release-candidate.yml` is missing. |
| `RELEASE_WORKFLOW_IDENTITY_BOUNDARY_MISSING` | The workflow lacks a required identity fragment (`source_version=`, `target_version=`, `release_status=`, the PR-head SHA expression, or `push:`). |
| `RELEASE_WORKFLOW_HISTORICAL_IDENTITY_HARDCODED` | The workflow still hardcodes the historical RC1 artifact name. |
| `RELEASE_GIT_IDENTITY_UNAVAILABLE` | Git HEAD, tree, or working state could not be resolved. |
| `RELEASE_FROZEN_SOURCE_DIRTY` | A `candidate`/`ready` source has uncommitted changes. |

## What a PASS does not mean

The JSON payload always sets `qualification_established`,
`publication_established`, and `semantic_truth_established` to `false`.
`RELEASE_AUTHORITY_VALID` therefore does **not** establish CI qualification,
public publication state, semantic correctness, or release-owner
authorization. Those remain separate lifecycle states (validation is not
closure; finding is not authorization).

A dirty working tree is reported in the `Git dirty` field for every status but
is an error only for `candidate`/`ready`; a development checkout with local
edits still audits valid.

## Related

- `docs/release-v1.0-contract.md` - release scope and support claims.
- `docs/release-v1.0-checklist.md` - release checklist.
- `docs/PUBLISHING.md` - publication procedure.
- `scripts/validate-release-contract.py`, `scripts/validate-release-readiness.py`
  - other deterministic release checks.
