# Installation & Setup Guide — Sensemaking Skills

This guide covers installation of the public distribution and the current Version 1.0 development line. Current repository source identity is `1.0.0rc3.dev0` targeting `1.0.0rc3`; the qualified `1.0.0rc2` candidate remains frozen historical provenance.

## Requirements

- Python 3.11 or 3.12
- `pip`
- A coding-agent harness only if you want native Skill discovery/execution

The core installed package is local-first and does not require a server or cloud account.

## Install from PyPI

The public PyPI distribution may lag the repository development line. Install the latest published distribution without treating it as the identity of current `main`:

```bash
python -m pip install sensemaking-skills
sensemaking-skills --version
```

A PyPI version, a repository development version, and a frozen release candidate are distinct provenance claims.

## Install from source

```bash
git clone https://github.com/ThorStarlord/sensemaking-skills.git
cd sensemaking-skills
python -m venv .venv
# activate the environment
python -m pip install -e .
```

## What the wheel contains

The Version 1.0 target wheel is intended to contain the shipped Campaign/runtime surface, build-derived Skill trees, and the build-derived canonical validator runtime used by normal `campaign ingest` operations.

The wheel intentionally does **not** contain retained research-lab packages:

```text
sensemaking_skills.campaign_validation
sensemaking_skills.campaign_accounting
sensemaking_skills.exploratory_authorization
sensemaking_skills.exploratory_execution
```

Those remain repository/source-lab infrastructure.

## Install Skills into harness discovery roots

Harness and scope selection are explicit.

### Generic Agent Skills

```bash
sensemaking-skills setup-skills --target generic --scope user
sensemaking-skills setup-skills --target generic --scope project --project-root /path/to/repo
```

### Claude Code

```bash
sensemaking-skills setup-skills --target claude --scope user
sensemaking-skills setup-skills --target claude --scope project --project-root /path/to/repo
```

### Codex

```bash
sensemaking-skills setup-skills --target codex --scope user
sensemaking-skills setup-skills --target codex --scope project --project-root /path/to/repo
```

Codex user scope honors explicit `CODEX_HOME` configuration and otherwise uses the documented default.

### OpenCode

```bash
sensemaking-skills setup-skills --target opencode --scope user
sensemaking-skills setup-skills --target opencode --scope project --project-root /path/to/repo
```

Use `--dry-run` to preview and `--force` only when you explicitly intend to replace a divergent installed Skill tree.

## Verify the Campaign CLI

```bash
sensemaking-skills campaign --help
sensemaking-skills campaign init --help
sensemaking-skills campaign ingest --help
sensemaking-skills campaign capabilities --help
sensemaking-skills campaign lineage --help
sensemaking-skills campaign reconciliation --help
sensemaking-skills campaign handoff --help
sensemaking-skills campaign resume --help
```

## Validator runtime

Normal installed use does not need a source checkout:

```bash
sensemaking-skills campaign ingest \
  --workspace /path/to/CMP-0001 \
  --artifact /path/to/artifact.md
```

For development/compatibility testing you may explicitly provide:

```bash
--framework-root /path/to/sensemaking-skills
```

An invalid explicit override fails closed; it is never silently replaced with another runtime.

## Schema version

Version 1.0 emits Campaign schema version 2 and can deterministically read/qualify supported v1 representations. See `docs/campaign-schema-evolution.md`.

The Version 1.0 target support and claim ceiling is documented in
[`docs/release-v1.0-contract.md`](docs/release-v1.0-contract.md).

## Development/lab dependencies

The shipped product dependencies are intentionally small. To run retained research/lab suites from a source checkout, install `requirements-lab.txt` separately according to the repository CI workflow.

## Troubleshooting

- **`0+unknown` from a raw source import:** install the project/distribution so `importlib.metadata` can resolve `sensemaking-skills` version metadata.
- **Skill tree differs:** run setup with `--dry-run`; use `--force` only if replacement is intentional.
- **Project-scoped setup fails:** provide an explicit existing `--project-root`; the tool does not infer it from cwd/editor/git state.
- **Artifact validation runtime error:** reinstall the package or explicitly select a valid source checkout with `--framework-root`.

For architecture and release state, see `README.md`, `STATUS.md`, and `docs/release-v1.0-contract.md`.
