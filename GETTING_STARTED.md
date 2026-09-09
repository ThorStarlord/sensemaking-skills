# Getting Started with Sensemaking Skills v0.3.0

Sensemaking Skills combines agent-native Skills with a local Campaign CLI. The agent supplies semantic judgment; the CLI makes state, evidence, provenance, and explicit decisions durable and mechanically checkable.

## Prerequisites

- Python 3.11+
- A repository/workspace to work on
- A coding-agent harness if you want native Skill execution

## Install

```bash
python -m pip install sensemaking-skills==0.3.0
sensemaking-skills --version
```

Expected output includes `0.3.0`.

For source development:

```bash
git clone https://github.com/ThorStarlord/sensemaking-skills.git
cd sensemaking-skills
python -m venv .venv
# activate the environment
python -m pip install -e .
```

## Install Skills for a harness

Sensemaking Skills does not auto-detect the active harness. Choose the target and scope explicitly.

```bash
# user scope
sensemaking-skills setup-skills --target generic --scope user
sensemaking-skills setup-skills --target claude --scope user
sensemaking-skills setup-skills --target codex --scope user
sensemaking-skills setup-skills --target opencode --scope user

# project scope
sensemaking-skills setup-skills --target claude --scope project --project-root /path/to/repo
```

Use `--dry-run` to preview. Divergent installed Skill trees are preserved unless `--force` is explicit.

## Start a Campaign

```bash
sensemaking-skills campaign init \
  --workspace /tmp/CMP-0001 \
  --campaign-id CMP-0001 \
  --mission "diagnose and repair the repository boundary"

sensemaking-skills campaign status --workspace /tmp/CMP-0001
```

## Diagnose with the agent-native Skill path

Ask the active coding agent to use `repo-sensemaker` against the target repository and produce a canonical artifact such as a `repository_sensemaking_brief`.

The Skill performs semantic diagnosis. Deterministic scripts/CLI validate and persist the result; they do not replace the agent's judgment.

## Admit validated evidence

Installed v0.3 distributions carry the canonical validator runtime:

```bash
sensemaking-skills campaign ingest \
  --workspace /tmp/CMP-0001 \
  --artifact /path/to/repository_sensemaking_brief.md
```

For development, `--framework-root /path/to/sensemaking-skills` may explicitly select a source checkout. A bad explicit override fails closed.

## Inspect capabilities

```bash
sensemaking-skills campaign capabilities \
  --workspace /tmp/CMP-0001 \
  --responsibility architectural_review
```

Capability results are deterministic and unranked. Availability is not selection or execution authority.

## Record an agent-authored decision

Use the explicit decision commands after the active agent has made the semantic judgment:

```bash
sensemaking-skills campaign advance --help
sensemaking-skills campaign defer --help
sensemaking-skills campaign close --help
```

## Inspect evidence lineage and reconciliation

```bash
sensemaking-skills campaign lineage --workspace /tmp/CMP-0001
sensemaking-skills campaign reconciliation --workspace /tmp/CMP-0001
```

These commands reconstruct mechanical provenance/disposition state; they do not decide what the evidence means.

## Handoff and resume

```bash
sensemaking-skills campaign handoff --workspace /tmp/CMP-0001
sensemaking-skills campaign resume --workspace /tmp/CMP-0001
```

The durable handoff allows a fresh context to reconstruct the Campaign without relying on the previous chat transcript.

## Schema compatibility

Current Campaign artifacts use schema version 2. Historical v1 artifacts can be inspected and deterministically qualified through the schema-evolution surface documented in `docs/campaign-schema-evolution.md`.

## Real-harness qualification

A real coding-agent harness attempt can be frozen into the evidence package described in `docs/external-golden-path-verifier.md` and verified with the `sensemaking_skills.external_qualification` module.

Synthetic fixtures validate the verifier itself; they are not substitutes for a real empirical harness run.

## Important boundaries

```text
validator passed != semantic truth
available capability != selected or authorized capability
handoff != recommendation
lineage != warrant
Skill installed != Skill observed/invoked by the harness
external verifier PASS != universal compatibility
```

For current release state, see `STATUS.md` and `docs/productization-v0.3.md`.
