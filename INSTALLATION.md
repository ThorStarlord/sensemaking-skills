# Installation & Setup Guide — Sensemaking Skills v0.3.0

This guide covers installing the first Campaign-based Sensemaking Skills release and making its agent-native Skills available to compatible coding-agent harnesses.

## Current state

v0.3.0 is a local Python package and CLI with durable Campaign support.

Available product surfaces include:

```text
sensemaking-skills --version
sensemaking-skills setup-skills
sensemaking-skills campaign ...
```

The package is designed to be installed from a distribution artifact. Normal installed Campaign use does not require the Sensemaking Skills source checkout.

Repository diagnosis itself remains agent-led through the packaged Skills; the deterministic CLI stores/validates/reconstructs Campaign state and evidence rather than replacing semantic agent judgment.

---

## Prerequisites

- Python 3.11+
- Git only if installing/working from source
- a compatible coding-agent harness if you want agent-native Skill execution

Verify Python:

```bash
python --version
```

---

## Install from PyPI

After v0.3.0 publication:

```bash
python -m pip install sensemaking-skills==0.3.0
sensemaking-skills --version
```

Expected:

```text
0.3.0
```

Verify the Campaign CLI:

```bash
sensemaking-skills campaign --help
```

---

## Install from source for development

```bash
git clone https://github.com/ThorStarlord/sensemaking-skills.git
cd sensemaking-skills
python -m venv .venv
```

Activate the environment:

**Windows PowerShell**
```powershell
.\.venv\Scripts\Activate.ps1
```

**Windows cmd**
```cmd
.venv\Scripts\activate.bat
```

**macOS/Linux**
```bash
source .venv/bin/activate
```

Then:

```bash
python -m pip install -e .
sensemaking-skills --version
```

---

## Install agent-native Skills

Sensemaking Skills uses explicit adapters; it does not infer which coding-agent harness is active.

### Generic / portable Agent Skills

```bash
sensemaking-skills setup-skills --target generic --scope user
```

Project scope:

```bash
sensemaking-skills setup-skills \
  --target generic \
  --scope project \
  --project-root /path/to/repository
```

### Claude Code

```bash
sensemaking-skills setup-skills --target claude --scope user
```

Project scope:

```bash
sensemaking-skills setup-skills \
  --target claude \
  --scope project \
  --project-root /path/to/repository
```

### Codex

```bash
sensemaking-skills setup-skills --target codex --scope user
```

Codex user scope honors `$CODEX_HOME/skills` and defaults to `~/.codex/skills`. Project scope uses the portable `.agents/skills` root:

```bash
sensemaking-skills setup-skills \
  --target codex \
  --scope project \
  --project-root /path/to/repository
```

### OpenCode

```bash
sensemaking-skills setup-skills --target opencode --scope user
```

Project scope:

```bash
sensemaking-skills setup-skills \
  --target opencode \
  --scope project \
  --project-root /path/to/repository
```

### Installation drift behavior

```text
missing
→ install

current exact packaged tree
→ no-op success

different
→ preserve installed bytes + report drift

--force
→ explicit replacement
```

Use `--dry-run` when you want to inspect the deterministic setup action without writing destination state.

A successful setup proves placement only:

```text
Skill copied to discovery root
!= harness observed Skill
!= Skill selected
!= execution authorized
```

See `docs/harness-adapters.md` for the complete adapter contract.

---

## Start a Campaign

```bash
sensemaking-skills campaign init \
  --workspace /path/to/CMP-0001 \
  --campaign-id CMP-0001 \
  --mission "Diagnose and resolve a bounded engineering problem"
```

Then inspect:

```bash
sensemaking-skills campaign status --workspace /path/to/CMP-0001 --json
sensemaking-skills campaign validate --workspace /path/to/CMP-0001 --json
sensemaking-skills campaign history --workspace /path/to/CMP-0001 --json
```

Campaign workspaces contain durable state/trace/transitions/evidence/admission/lineage data under fail-closed filesystem boundaries.

---

## Agent-led repository diagnosis

Use a compatible coding-agent harness to invoke/read the packaged `repo-sensemaker` Skill against the target repository.

Expected primary artifact:

```text
repository_sensemaking_brief
```

The CLI does not autonomously author that semantic diagnosis.

---

## Admit an artifact from an installed package

After the agent produces the artifact:

```bash
sensemaking-skills campaign ingest \
  --workspace /path/to/CMP-0001 \
  --artifact /path/to/repository_sensemaking_brief.md \
  --target-repo /path/to/target \
  --json
```

v0.3.0 packages a build-derived canonical validator runtime, so normal installed use does **not** require:

```text
--framework-root /path/to/sensemaking-skills
```

An explicit `--framework-root` remains a development/compatibility override. If explicitly supplied and invalid, ingestion fails closed instead of silently falling back.

The admission boundary remains:

```text
artifact bytes
→ canonical validator router
→ selected validator
→ valid=true
→ content-addressed artifact
→ append-only admission receipt
→ Campaign evidence
```

Validator success establishes contract validity, not semantic truth.

---

## Continue the Campaign

The public Campaign surfaces include:

```text
campaign advance
campaign defer
campaign close
campaign capabilities
campaign reconciliation
campaign lineage
campaign handoff
campaign resume
```

See the corresponding documents under `docs/` for exact command options and contracts.

The active agent owns semantic choices. Deterministic machinery validates representation/evidence/authority constraints and persists reconstructible state.

---

## Source-development validator commands

When developing from a repository checkout, canonical validators can still be run directly:

```bash
python scripts/validate-and-report.py artifacts/repository_sensemaking_brief.md
python scripts/validate-and-report.py artifacts/workflow_orchestration_plan.md
```

Installed Campaign users should normally use `campaign ingest` so admission/provenance is recorded durably.

---

## Verify a release distribution

For a local candidate wheel:

```bash
python -m venv .verify
# activate .verify
python -m pip install dist/sensemaking_skills-0.3.0-py3-none-any.whl
sensemaking-skills --version
sensemaking-skills campaign --help
```

For production verification after publication:

```bash
python -m pip install sensemaking-skills==0.3.0
sensemaking-skills --version
sensemaking-skills campaign --help
```

The repository's release-candidate CI separately clean-installs both wheel and sdist and verifies packaged Skills plus validator runtime resources.

---

## Troubleshooting

### `sensemaking-skills: command not found`

Confirm the environment containing the package is active:

```bash
python -m pip show sensemaking-skills
python -m sensemaking_skills.cli --version
```

### Skill files were installed but the harness does not expose them

This is a harness-runtime/discovery issue, not proof that setup failed. P10 qualifies deterministic destination mapping and exact Skill-tree copying; runtime discovery is intentionally outside the v0.3.0 claim.

### `ARTIFACT_VALIDATOR_ERROR`

Treat it as validator/runtime infrastructure failure. Do not mislabel it as semantic artifact rejection and do not manually create an admission receipt.

### `ARTIFACT_VALIDATION_REJECTED`

The canonical validator executed normally and rejected the artifact contract. Repair/reproduce the artifact through the ordinary agent workflow, then retry admission.

### Campaign reconstruction/integrity error

Do not manually edit Campaign state, trace, receipts, or lineage to force continuation. Preserve the failing workspace and diagnose the integrity problem.

---

## Development tests

From a source checkout:

```bash
python -m pytest tests/ -v
```

The repository also has exact-head CI gates for Campaign validation, installed-wheel behavior, filesystem confinement, and v0.3 release distributions.

---

## v0.3.0 claim ceiling

v0.3.0 mechanically qualifies the installed Campaign control layer and deterministic harness installation adapters.

It does **not** claim universal real-harness Skill discovery, universal external-repository end-to-end success, automatic semantic routing, or guaranteed fresh-agent reasoning quality.

The stronger external runtime test is preserved as non-blocking post-release dogfood in `docs/v0.3-external-qualification-protocol.md`.

---

## Version information

- Package: `sensemaking-skills`
- Version: `0.3.0`
- Python: `>=3.11`
- Status: Beta; Campaign-based release line
- Release authority: exact-head P11 qualification + owner-gated integration/publication
