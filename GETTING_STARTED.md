# Getting Started with Sensemaking Skills v0.3.0

Sensemaking Skills combines agent-native Skills with a local Campaign CLI. The agent supplies semantic judgment; the CLI makes state, evidence, provenance, explicit decisions, and repository identity durable and mechanically checkable.

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

## See the current golden paths

The CLI exposes static navigation for composing existing Campaign surfaces. It does not choose a flow or execute its steps.

```bash
sensemaking-skills campaign workflow list
sensemaking-skills campaign workflow show single-repository
sensemaking-skills campaign workflow show fresh-context
sensemaking-skills campaign workflow show transferred-campaign
sensemaking-skills campaign workflow show multi-repository
```

The same agent-facing reference ships at `skills/using-sensemaking/references/golden-paths-v1.md`.

```text
flow shown != flow recommended
step listed != step authorized
golden path != workflow engine
```

## Start a Campaign

For a directly initialized Campaign:

```bash
sensemaking-skills campaign init \
  --workspace /tmp/CMP-0001 \
  --campaign-id CMP-0001 \
  --mission "diagnose and repair the repository boundary" \
  --target-repo /path/to/repository

sensemaking-skills campaign status --workspace /tmp/CMP-0001
```

For repository-level strategic work, inspect Level-3 state first and use `campaign strategy handoff` only after the active agent has explicitly selected a current frontier item and responsibility.

## Diagnose with the agent-native Skill path

Ask the active coding agent to use `repo-sensemaker` against the target repository and produce a canonical artifact such as a `repository_sensemaking_brief` when repository-wide sensemaking is warranted.

The Skill performs semantic diagnosis. Deterministic scripts/CLI validate and persist the result; they do not replace the agent's judgment.

## Admit validated evidence

Installed v0.3 distributions carry the canonical validator runtime:

```bash
sensemaking-skills campaign ingest \
  --workspace /tmp/CMP-0001 \
  --artifact /path/to/repository_sensemaking_brief.md
```

For development, `--framework-root /path/to/sensemaking-skills` may explicitly select a source checkout. A bad explicit override fails closed.

## Reconstruct and preflight

```bash
sensemaking-skills campaign resume-profile \
  --workspace /tmp/CMP-0001 \
  --profile working \
  --json

sensemaking-skills campaign preflight \
  --workspace /tmp/CMP-0001 \
  --json
```

Use `campaign doctor` when a mechanical preflight failure needs a bounded diagnostic path.

## Inspect capabilities after responsibility selection

```bash
sensemaking-skills campaign capability-context \
  --workspace /tmp/CMP-0001 \
  --responsibility-type architectural_review \
  --json
```

Capability results are deterministic and unranked. Availability/compatibility is not selection or execution authority.

## Record an agent-authored decision

Use the explicit decision commands after the active agent has made the semantic judgment:

```bash
sensemaking-skills campaign advance --help
sensemaking-skills campaign defer --help
sensemaking-skills campaign close --help
```

## Complete and optionally archive a terminal Campaign

`campaign close` remains the semantic terminal decision. Only afterward can a deterministic completion receipt be created:

```bash
sensemaking-skills campaign closeout --workspace /tmp/CMP-0001 --json
sensemaking-skills campaign completion-receipt --workspace /tmp/CMP-0001 --json
sensemaking-skills campaign archive --workspace /tmp/CMP-0001 --json
```

Archive is a nondestructive marker, not a success judgment.

## Transfer a Campaign to a different path or machine

Inspect bundle bytes before durable import:

```bash
sensemaking-skills campaign bundle-inspect --bundle /path/to/CMP-0001.bundle --json
sensemaking-skills campaign bundle-resume-context --bundle /path/to/CMP-0001.bundle --json
```

After explicit import, provide the local target path rather than asking Sensemaking to discover it:

```bash
sensemaking-skills campaign target rebind \
  --workspace /path/to/imported/CMP-0001 \
  --target-repo /new/path/to/repository \
  --json
```

Rebinding accepts only the same recorded repository identity and exact recorded Git/worktree state. It is not target refresh.

## Multi-repository Campaigns

Additional repositories are explicitly added by alias. Relationships are explicitly authored, then mechanically checked:

```bash
sensemaking-skills campaign multi-target add --help
sensemaking-skills campaign multi-target relate --help
sensemaking-skills campaign multi-target verify --help
sensemaking-skills campaign multi-target dependency-check --help
sensemaking-skills campaign multi-target graph --help
```

Multi-target membership or dependency validity is not proof that the architecture or execution order is correct.

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

Synthetic fixtures validate the verifier itself; they are not substitutes for a real empirical harness run. Current owner direction does not require new experiments as a prerequisite for bounded repository-only/hermetic construction.

## Important boundaries

```text
validator passed != semantic truth
available capability != selected or authorized capability
handoff != recommendation
lineage != warrant
flow shown != flow recommended
step listed != authorized action
completion receipt != proof of correctness
archive != success
repository rebound != repository selected
multi-target relation valid != architecture correct
Skill installed != Skill observed/invoked by the harness
external verifier PASS != universal compatibility
```

For current release/strategic state, see `STATUS.md`, `docs/operations-runbook.md`, and `docs/productization-v0.3.md`.
