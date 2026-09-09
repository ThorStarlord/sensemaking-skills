# Getting Started with Sensemaking Skills v0.3.0

Sensemaking Skills has two cooperating surfaces:

1. **agent-native Skills** for semantic repository diagnosis and bounded engineering work;
2. **local Campaign/validation CLI** for durable state, evidence admission, provenance, reconstruction, and explicit decision contracts.

The active coding agent owns semantic judgment. The CLI does not decide what responsibility, capability, or conclusion is correct.

---

## Prerequisites

- Python 3.11+
- A local repository/workspace
- A compatible coding-agent harness if you want agent-native Skill execution

The core CLI is local-first. Normal Campaign use does not require an API key or a Sensemaking Skills source checkout after installation.

---

## Install

After v0.3.0 is published:

```bash
python -m pip install sensemaking-skills==0.3.0
sensemaking-skills --version
```

Expected:

```text
0.3.0
```

For source development:

```bash
git clone https://github.com/ThorStarlord/sensemaking-skills.git
cd sensemaking-skills
python -m venv .venv
# activate the environment
python -m pip install -e .
```

---

## Make Skills available to an agent

Sensemaking Skills does not auto-detect the active harness. Choose the target and scope explicitly.

### Project scope

```bash
sensemaking-skills setup-skills --target generic --scope project --project-root /path/to/repo
sensemaking-skills setup-skills --target claude --scope project --project-root /path/to/repo
sensemaking-skills setup-skills --target codex --scope project --project-root /path/to/repo
sensemaking-skills setup-skills --target opencode --scope project --project-root /path/to/repo
```

### User scope

```bash
sensemaking-skills setup-skills --target generic --scope user
sensemaking-skills setup-skills --target claude --scope user
sensemaking-skills setup-skills --target codex --scope user
sensemaking-skills setup-skills --target opencode --scope user
```

Installation proves only that the exact packaged Skill tree was placed in the declared discovery location:

```text
Skill copied
!= harness observed Skill
!= Skill selected
!= execution authorized
```

See `docs/harness-adapters.md` for exact paths and compatibility targets.

---

## Campaign quick start

### 1. Initialize a durable Campaign

Keep the Campaign workspace separate from the target repository when practical:

```bash
sensemaking-skills campaign init \
  --workspace /path/to/CMP-0001 \
  --campaign-id CMP-0001 \
  --mission "Diagnose and resolve a bounded engineering problem"
```

Inspect it:

```bash
sensemaking-skills campaign status --workspace /path/to/CMP-0001 --json
sensemaking-skills campaign validate --workspace /path/to/CMP-0001 --json
sensemaking-skills campaign history --workspace /path/to/CMP-0001 --json
```

### 2. Diagnose the repository through an agent-native Skill

Ask the active coding agent to use the packaged `repo-sensemaker` Skill against the target repository and produce a `repository_sensemaking_brief`.

The legacy/simple Python helper is not a substitute for the agent-native semantic diagnosis path.

### 3. Admit the validated brief as Campaign evidence

```bash
sensemaking-skills campaign ingest \
  --workspace /path/to/CMP-0001 \
  --artifact /path/to/repository_sensemaking_brief.md \
  --target-repo /path/to/target \
  --json
```

In v0.3.0, normal installed-distribution ingestion uses the packaged canonical validator runtime. No `--framework-root` is required.

The trust boundary is:

```text
artifact file
!= validated artifact
!= admitted Campaign evidence
```

### 4. Record the agent-authored responsibility/authority decision

Use the appropriate explicit P5 surface:

```text
campaign advance
campaign defer
campaign close
```

The agent supplies the semantic decision and cited evidence. Deterministic machinery validates and persists it.

See `docs/campaign-decisions.md` for the exact options/contract.

### 5. Inspect capabilities

After the agent classifies the active responsibility:

```bash
sensemaking-skills campaign capabilities \
  --workspace /path/to/CMP-0001 \
  --responsibility-type architecture_review \
  --json
```

The result is deterministic and unranked. The registry does not select a capability for the agent.

### 6. Perform bounded work

The active agent may use a registered Skill, ordinary coding, or honestly stop if authority/evidence is insufficient.

Capture durable work evidence through the normal repository/test/artifact surfaces. Do not create a special Campaign-only execution backdoor.

### 7. Reconcile and explicitly disposition the result

Inspect admitted reconciliation evidence:

```bash
sensemaking-skills campaign reconciliation --workspace /path/to/CMP-0001 --json
```

Mechanical states include:

```text
disposition_required
disposition_recorded
legacy_unbound
```

A report does not automatically decide the Campaign transition. The active agent explicitly `advance`s, `defer`s, or `close`s and cites the relevant evidence when warranted.

### 8. Inspect exact evidence lineage

```bash
sensemaking-skills campaign lineage --workspace /path/to/CMP-0001 --json
```

Lineage reconstructs exact bytes/provenance/consumption links. It does not claim semantic sufficiency.

### 9. Handoff and resume

```bash
sensemaking-skills campaign handoff --workspace /path/to/CMP-0001 --json
sensemaking-skills campaign resume --workspace /path/to/CMP-0001 --json
```

Resume reconstructs durable Campaign state in a fresh process. It does not invent the next semantic action.

---

## Standalone validation utilities

Repository/source-development users may still call canonical scripts directly:

```bash
python scripts/validate-and-report.py artifacts/repository_sensemaking_brief.md
python scripts/validate-and-report.py artifacts/workflow_orchestration_plan.md
```

Installed Campaign users should prefer `campaign ingest`, which uses the self-contained packaged validator runtime and records admission provenance.

---

## Core artifacts

### `repository_sensemaking_brief`

An evidence-grounded repository diagnosis produced by `repo-sensemaker`.

### `workflow_orchestration_plan`

A bounded workflow plan produced when planning is warranted. A plan is not automatic execution authority.

### Reconciliation / repair-verification reports

Evidence about bounded work outcomes. Their presence or validator success does not automatically determine the Campaign decision.

---

## Core trust boundaries

```text
validator passed != conclusion is true
admitted evidence != warranted responsibility
available capability != authorized capability
reconciliation evidence != Campaign decision
lineage != semantic warrant
handoff != semantic recommendation
Campaign Controller != semantic router
```

---

## Troubleshooting

### `Skill not found`

First inspect whether you installed into the intended explicit adapter/scope:

```bash
sensemaking-skills setup-skills --target <generic|claude|codex|opencode> --scope <user|project> ...
```

A successful copy does not prove that the selected harness has loaded or exposed its native Skill mechanism. Consult that harness's runtime/discovery behavior if the files are present but not observed.

### `campaign ingest` reports `ARTIFACT_VALIDATOR_ERROR`

This is a validator/runtime infrastructure error, not a semantic rejection of the artifact. Normal installed v0.3.0 use should not need `--framework-root`.

### Artifact validation is rejected

Treat the canonical validator errors as contract feedback. Do not manually edit Campaign receipts/artifacts to bypass admission.

### Campaign validation/reconstruction fails

Do not repair Campaign YAML/receipts by hand. Preserve the failing state and diagnose the product/integrity failure through the documented Campaign contracts.

---

## What v0.3.0 does and does not claim

v0.3.0 mechanically qualifies the installed Campaign control layer and deterministic Skill installation adapters.

It does **not** claim universal real-harness Skill discovery, universal external-repository success, or guaranteed fresh-agent semantic quality.

The stronger external golden path remains available as non-blocking post-release dogfood in `docs/v0.3-external-qualification-protocol.md`.

---

## More information

- `README.md` — product overview and quick start
- `INSTALLATION.md` — installation details
- `STATUS.md` — exact current release/qualification state
- `CONTEXT.md` — governing architecture and terminology
- `docs/sensemaking-campaign.md` — canonical Campaign product model
- `docs/productization-v0.3.md` — release plan and claim ceiling
- `docs/artifact-ingestion.md` — validation/admission boundary
- `docs/campaign-decisions.md` — authored decision contracts
- `docs/capability-registry.md` — capability inspection
- `docs/campaign-lineage.md` — lineage reconstruction
- `docs/campaign-reconciliation.md` — reconciliation lifecycle
- `docs/campaign-handoff-resume.md` — handoff/resume
- `docs/harness-adapters.md` — coding-agent installation targets
