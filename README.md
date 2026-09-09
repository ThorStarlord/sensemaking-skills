# Sensemaking Skills

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

An **agent-native engineering sensemaking and control layer** for software-engineering agents. Sensemaking Skills turns repository uncertainty into durable, evidence-grounded engineering decisions without replacing the active agent's semantic judgment.

**Version:** 0.3.0  
**Status:** Beta; first Campaign-based release line  
**Architecture:** active agent owns semantic control; deterministic machinery owns persistence, validation, provenance, authority checks, and reconstruction  
**Current release program:** P0–P10 integrated; P11 release qualification in progress. See [STATUS.md](STATUS.md).

---

## What v0.3.0 provides

### Durable Sensemaking Campaigns

A **Sensemaking Campaign** carries engineering decision state across agent sessions:

- mission and uncertainty;
- active responsibility and authority;
- validated/admitted evidence;
- transition history and trace;
- deferred work and terminal state;
- artifact/evidence lineage;
- reconciliation disposition state;
- integrity-bound handoff/resume context.

The Campaign makes agent judgment **durable and reconstructible**. It does not replace that judgment.

### Validated artifact admission

```text
artifact bytes
→ canonical validator router
→ selected validator
→ valid=true
→ content-addressed artifact
→ append-only admission receipt
→ Campaign evidence
```

Therefore:

```text
file exists
!= validated artifact
!= admitted Campaign evidence
```

The v0.3.0 distribution includes a build-derived copy of the canonical validator runtime, so normal installed use of `campaign ingest` does **not** require a separate Sensemaking Skills source checkout.

### Explicit agent-authored decisions

The active agent records semantic decisions through typed Campaign surfaces:

```text
campaign advance
campaign defer
campaign close
```

Deterministic code validates/persists the contract; it does not infer the next responsibility from artifact prose.

### Capability inspection without routing

`campaign capabilities` exposes deterministic, unranked capability metadata after the agent supplies a responsibility classification.

```text
warranted responsibility
!= registered capability
!= runtime availability
!= execution authority
```

The registry never chooses a capability for the agent.

### Evidence lineage and reconciliation

`campaign lineage` reconstructs exact evidence-byte identity, provenance, and explicit transition consumption.

`campaign reconciliation` reports mechanical states such as:

```text
disposition_required
disposition_recorded
legacy_unbound
```

Neither surface interprets evidence into semantic truth or an automatic Campaign transition.

### Integrity-bound handoff/resume

`campaign handoff` and `campaign resume` let a fresh process or agent reconstruct stored Campaign state without relying on the previous conversation as the persistence layer.

The handoff is reconstruction context, not a recommendation engine.

### Coding-agent Skill installation adapters

`setup-skills` provides explicit deterministic installation targets for:

- portable/generic Agent Skills locations;
- Claude Code discovery locations;
- Codex discovery locations;
- OpenCode discovery locations.

The important claim ceiling is:

```text
Skill copied to discovery root
!= harness observed Skill
!= Skill selected
!= execution authorized
!= Campaign decision
```

Runtime Skill discovery remains a property of the selected coding-agent harness.

---

## v0.3.0 qualification claim

Sensemaking Skills v0.3.0 claims the **mechanically qualified installed Campaign control layer**.

The release qualifies:

- Campaign representation and lifecycle persistence;
- canonical artifact admission and validator provenance;
- explicit authored-decision contracts;
- capability inspection contracts;
- evidence lineage reconstruction;
- reconciliation disposition reconstruction;
- integrity-bound handoff/resume;
- fresh-process and installed-distribution behavior;
- deterministic Skill installation adapters;
- wheel and sdist build/install metadata.

The release deliberately does **not** claim:

- universal real-harness Skill discovery;
- universal external-repository end-to-end success;
- automatic capability choice;
- automatic semantic next action;
- semantic truth from validator success;
- guaranteed fresh-agent reasoning quality.

A stronger real-harness/external-repository golden path is preserved as **non-blocking post-release dogfood**, not as a v0.3.0 release gate. See [docs/v0.3-external-qualification-protocol.md](docs/v0.3-external-qualification-protocol.md).

---

## What this is not

❌ **Not a centralized agent orchestrator** — the active coding agent owns the recursive semantic control loop.  
❌ **Not a semantic router** — Campaign state, validators, capability metadata, and artifacts do not automatically decide what the agent should do next.  
❌ **Not an autonomous CLI diagnosis engine** — repository diagnosis remains agent-led.  
❌ **Not a semantic truth validator** — validator success establishes contract validity, not correctness of an engineering conclusion.  
❌ **Not a hosted service** — the Campaign core is local and file-backed.  
❌ **Not proof that every harness discovers every installed Skill** — P10 qualifies deterministic installation destinations, not universal runtime behavior.

---

## Requirements

- Python 3.11+
- A local repository/workspace
- A compatible coding-agent harness if you want agent-native Skill execution

The core Campaign CLI itself is local-first. One optional historical subsystem, `exploratory_execution`, can call the GitHub REST API for governed issue/approval tracking and requires separate authentication when used.

---

## Installation

### PyPI

After v0.3.0 publication:

```bash
pip install sensemaking-skills==0.3.0
sensemaking-skills --version
```

Expected:

```text
0.3.0
```

### Source development

```bash
git clone https://github.com/ThorStarlord/sensemaking-skills.git
cd sensemaking-skills
python -m venv .venv
# activate the environment
python -m pip install -e .
sensemaking-skills --version
```

---

## Campaign quick start

### 1. Initialize

```bash
sensemaking-skills campaign init \
  --workspace /path/to/CMP-0001 \
  --campaign-id CMP-0001 \
  --mission "Diagnose and resolve a bounded engineering problem"
```

Inspect the durable state:

```bash
sensemaking-skills campaign status --workspace /path/to/CMP-0001 --json
sensemaking-skills campaign validate --workspace /path/to/CMP-0001 --json
sensemaking-skills campaign history --workspace /path/to/CMP-0001 --json
```

### 2. Diagnose through an agent-native Skill

Use a compatible coding-agent harness to run the packaged `repo-sensemaker` Skill against the target repository and produce a `repository_sensemaking_brief`.

The CLI does not replace this semantic agent step.

### 3. Admit the validated artifact

```bash
sensemaking-skills campaign ingest \
  --workspace /path/to/CMP-0001 \
  --artifact /path/to/repository_sensemaking_brief.md \
  --target-repo /path/to/target \
  --json
```

Normal installed-distribution use needs no `--framework-root`.

### 4. Record the agent's decision

Use the explicit decision surfaces described in [docs/campaign-decisions.md](docs/campaign-decisions.md):

```text
campaign advance
campaign defer
campaign close
```

The agent supplies responsibility, authority, evidence, success conditions, and decision rationale required by the relevant contract.

### 5. Inspect available capabilities

```bash
sensemaking-skills campaign capabilities \
  --workspace /path/to/CMP-0001 \
  --responsibility-type architecture_review \
  --json
```

The output is deterministic and unranked. The agent still chooses what, if anything, to execute.

### 6. Inspect reconciliation and lineage

```bash
sensemaking-skills campaign reconciliation --workspace /path/to/CMP-0001 --json
sensemaking-skills campaign lineage --workspace /path/to/CMP-0001 --json
```

### 7. Handoff and resume

```bash
sensemaking-skills campaign handoff --workspace /path/to/CMP-0001 --json
sensemaking-skills campaign resume --workspace /path/to/CMP-0001 --json
```

The resume envelope reconstructs durable Campaign context; it does not invent semantic next action.

---

## Install Skills for a coding-agent harness

Use `setup-skills` explicitly; Sensemaking Skills does not auto-detect which coding agent is running.

### Project scope

```bash
# Portable/generic Agent Skills
sensemaking-skills setup-skills --target generic --scope project --project-root /path/to/repo

# Claude Code
sensemaking-skills setup-skills --target claude --scope project --project-root /path/to/repo

# Codex
sensemaking-skills setup-skills --target codex --scope project --project-root /path/to/repo

# OpenCode
sensemaking-skills setup-skills --target opencode --scope project --project-root /path/to/repo
```

### User scope

```bash
sensemaking-skills setup-skills --target generic --scope user
sensemaking-skills setup-skills --target claude --scope user
sensemaking-skills setup-skills --target codex --scope user
sensemaking-skills setup-skills --target opencode --scope user
```

Drift is fail-closed:

```text
missing   → install
current   → no-op success
different → preserve existing bytes + report failure
--force   → explicit replacement
```

See [docs/harness-adapters.md](docs/harness-adapters.md) for exact discovery-root mappings and compatibility targets.

---

## Architecture

```text
active coding agent
  semantic judgment
        ↓
validated artifact / explicit decision
        ↓
CampaignService
        ↓
CampaignStore
        ↓
campaign_semantics
        ↓
durable filesystem workspace
```

The central invariant is:

```text
Campaign Controller != semantic router
```

And the trust boundaries include:

```text
validator passed != conclusion is true
admitted evidence != warranted responsibility
available capability != authorized capability
lineage != semantic warrant
reconciliation evidence != Campaign decision
handoff != semantic recommendation
harness discovery path != Skill selection or authority
```

---

## Core agent-native Skills

- **`repo-sensemaker`** — repository diagnosis and `repository_sensemaking_brief`
- **`workflow-planner`** — evidence-grounded workflow/orchestration planning
- **`architectural-review`** — architecture analysis
- **`docs-aligner`** — documentation/domain-alignment analysis
- **`sensemaking-docs-reconciler`** — bounded documentation reconciliation
- **`output-reconciler`** — output reconciliation
- **`repair-verifier`** — bounded repair verification
- additional packaged Skills are discoverable through the shipped Skill trees

Skills are agent-native procedures. The active agent decides which warranted capability to use; the Campaign runtime does not centrally route them.

---

## Validation and distribution evidence

The repository uses exact-head CI gates including:

- Validator Ecosystem on Python 3.11 and 3.12;
- Campaign lifecycle/recovery suites;
- installed-wheel smoke/distribution regressions;
- path-containment and Windows device-name proofs;
- exact-head conditional-representation checks;
- release-candidate wheel+sdist build and `twine check`;
- clean wheel/sdist installation checks.

See [STATUS.md](STATUS.md) for the current qualified candidate identity and run records.

---

## Repository structure

```text
sensemaking-skills/
├── src/sensemaking_skills/
│   ├── campaign_semantics/
│   ├── campaigns/
│   ├── campaign_validation/
│   ├── defaults/
│   └── ...
├── skills/                         # canonical agent-native Skill sources
├── scripts/                        # canonical validator/probe sources
├── tests/
├── docs/
│   ├── sensemaking-campaign.md
│   ├── productization-v0.3.md
│   ├── campaign-decisions.md
│   ├── capability-registry.md
│   ├── campaign-lineage.md
│   ├── campaign-reconciliation.md
│   ├── campaign-handoff-resume.md
│   └── harness-adapters.md
├── CONTEXT.md
├── STATUS.md
├── pyproject.toml
└── setup.py
```

The built distribution additionally derives packaged Skill trees and the validator runtime from the canonical repository sources; those generated package trees are distribution artifacts, not second hand-maintained authorities.

---

## Development and release

- Bug reports: [Issues](https://github.com/ThorStarlord/sensemaking-skills/issues)
- Feature requests: [Discussions](https://github.com/ThorStarlord/sensemaking-skills/discussions)
- Pull requests welcome with appropriate qualification evidence
- Publishing procedure: [docs/PUBLISHING.md](docs/PUBLISHING.md)
- Changelog: [CHANGELOG.md](CHANGELOG.md)

If a release defect is found after publication, publish a newly qualified patch version such as `0.3.1`; do not rewrite a published `0.3.0` identity.

---

## Quick links

- **[STATUS.md](STATUS.md)** — current implementation/release state
- **[Canonical Sensemaking Campaign](docs/sensemaking-campaign.md)** — durable product model
- **[v0.3 Productization Plan](docs/productization-v0.3.md)** — active release plan and claim ceiling
- **[Artifact Ingestion](docs/artifact-ingestion.md)** — validation/admission trust boundary
- **[Campaign Decisions](docs/campaign-decisions.md)** — agent-authored transition contracts
- **[Capability Registry](docs/capability-registry.md)** — deterministic capability inspection
- **[Campaign Lineage](docs/campaign-lineage.md)** — exact evidence provenance/consumption
- **[Campaign Reconciliation](docs/campaign-reconciliation.md)** — mechanical disposition reconstruction
- **[Handoff/Resume](docs/campaign-handoff-resume.md)** — fresh-process reconstruction
- **[Harness Adapters](docs/harness-adapters.md)** — Skill installation destinations
- **[Post-release External Dogfood](docs/v0.3-external-qualification-protocol.md)** — optional stronger runtime protocol
- **[CONTEXT.md](CONTEXT.md)** — architecture and governing principles

## License

MIT License. See [LICENSE](LICENSE) for details.
