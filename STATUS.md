# Status

**Version**: 0.2.2 (see [pyproject.toml](pyproject.toml), [CHANGELOG.md](CHANGELOG.md))
**Last updated**: 2026-08-26 (Goal A protocol amendment — independent evaluator usefulness authority)

## Current product-validation priority

**Goal A — External Product Validation** is the current product-validation
strategy. The approved protocol is canonical at
[docs/research/goal-a-external-product-validation-protocol.md](docs/research/goal-a-external-product-validation-protocol.md).

```text
Goal A       = ACTIVE
A1           = ACTIVE  (absolute product utility)
A2           = DEFERRED / UNAUTHORIZED
Goal B / E3  = FROZEN / DEFERRED
```

Goal A validates the ratified product scope (a validated, human-reviewed
`repository_sensemaking_brief`) through constructed external
product-validation episodes. Protocol approval does **not** authorize episode
execution; no repositories/tasks have been selected and no episodes have run.
Goal B / research-grade E3 remains FROZEN / DEFERRED. See the canonical
protocol for the full approved semantics and boundaries.

## Current state

- Distribution-drift probe engine: CRLF normalization (`line_ending_only` vs
  `content_drift`) and the `--sync` flag are merged; global skills are
  synchronized (content drift 0, missing 0).
- Documentation reconciled: README version/API claims match the codebase, ADR
  0011 restored, and 97 historical phase/completion reports archived.
- Probe engine (`scripts/repo_probes.py`, `scripts/probe-repo.py`) is the
  verified-state source consumed by `repo-sensemaker`.

## Where to look

| Topic | Location |
| :--- | :--- |
| Architecture and principles | [CONTEXT.md](CONTEXT.md) |
| Usage and install | [README.md](README.md), [GETTING_STARTED.md](GETTING_STARTED.md), [INSTALLATION.md](INSTALLATION.md) |
| Change history | [CHANGELOG.md](CHANGELOG.md) |
| Design decisions | [docs/adr/](docs/adr/) |
| Historical phase/completion reports | [docs/archive/phase-reports/](docs/archive/phase-reports/) |

This file is the single living status summary at the repo root. Dated
phase/completion/deployment reports are archived under
`docs/archive/phase-reports/` and are not updated here.
