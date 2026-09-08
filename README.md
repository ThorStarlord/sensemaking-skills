# Sensemaking Skills

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

An agent-native engineering sensemaking and control layer for software-engineering agents. It turns repository uncertainty into evidence-grounded, warranted next action.

**Status**: Beta; v0.3 campaign productization active  
**Current Use**: Agent-native Skills + local CLI/campaign utilities (v0.2.2)  
**Maturity**: P0–P4 of the v0.3 Campaign product are integrated; P5 — agent-authored campaign decisions — is the current implementation frontier. See [STATUS.md](STATUS.md), [docs/sensemaking-campaign.md](docs/sensemaking-campaign.md), and [docs/productization-v0.3.md](docs/productization-v0.3.md).

---

## What This Is

✅ **Evidence-grounded responsibility selection** — Sensemaking helps an active agent determine what kind of engineering responsibility is warranted next from repository evidence and unresolved uncertainty. The active agent owns the top-level control loop.

✅ **Durable Sensemaking Campaigns** — A Campaign carries goal, uncertainty, responsibility, authority, evidence, validated artifacts, transition history, deferred work, and continuation/terminal state across agent sessions. The Campaign makes agent judgment reconstructible; it does not replace that judgment.

✅ **Artifact-driven engineering** — Communication across bounded responsibilities happens through durable, validated artifacts:
- `repository_sensemaking_brief` (14-section diagnostic)
- `workflow_orchestration_plan` (10-section planning artifact)
- validators, reconciliation reports, and repair-verification evidence constrain what may be claimed
- Campaign artifact admission preserves exact validated bytes as durable evidence without treating file existence as epistemic status

✅ **Agent-native design** — Agent-agnostic skills, invoked by any coding agent:
- Skills defined in SKILL.md files
- The agent selects responsibility before choosing a Skill
- Runtime/orchestration machinery coordinates execution where useful; it does not own the product-level decision loop
- No external service dependencies in the core CLI

## What This Is NOT

❌ **Not a centralized agent orchestrator** — The active coding agent owns the recursive control loop. Sensemaking governs what responsibility is warranted; orchestration coordinates how selected work is executed.  
❌ **Not a semantic router** — Campaign state, validators, capability metadata, and artifacts do not automatically decide what the agent should do next.  
❌ **Not a fully autonomous CLI diagnosis engine** — Repository diagnosis is agent-led; the CLI provides campaign/state/validation utilities.  
❌ **Not a service** — No server, no cloud dependency. The core package is entirely local; only the optional `exploratory_execution` subsystem calls the GitHub REST API (`api.github.com`) for issue-approval tracking.  
❌ **Not a replacement for specialized tools** — Complements PM skills, UI skills, TDD tools.  
❌ **Full diagnosis requires an agent harness** — The CLI utilities work standalone; agent-driven diagnosis requires a coding-agent harness (Claude Code is one supported harness, not the only one).

See [docs/sensemaking-campaign.md](docs/sensemaking-campaign.md) for the canonical Campaign product model, [docs/agent-native-operating-workflow.md](docs/agent-native-operating-workflow.md) for the current operating model, [docs/decision-orchestration-boundary.md](docs/decision-orchestration-boundary.md) for the control boundary, and [docs/productization-v0.3.md](docs/productization-v0.3.md) for the active delivery plan.

---

## What You Need to Use This

- Python 3.11+
- A local repository to analyze
- No API keys or external credentials required for the CLI itself

**sensemaking-skills is a local-first Python utility.** The package itself reads repository files, validates artifacts, runs local scripts, and produces diagnostic Markdown outputs. The core CLI makes no external API calls and requires no credentials. One optional subsystem, `exploratory_execution` (issue/approval tracking for governed experiment runs), calls the GitHub REST API at `api.github.com` and requires a GitHub personal access token; it fails closed when unauthenticated or unreachable.

For full agent-driven diagnostics, use the included SKILL.md files with any coding-agent harness (Claude Code, Codex, Pi, Hermes). Any LLM/API access is handled by that harness, not by sensemaking-skills.

## Installation

### Option 1: From PyPI (Recommended)

```bash
pip install sensemaking-skills
sensemaking-skills --version
```

### Option 2: From Source

```bash
# Clone the repository
git clone https://github.com/ThorStarlord/sensemaking-skills.git
cd sensemaking-skills

# Create and activate a Python environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install locally
pip install -e .

# Verify the CLI
sensemaking-skills --version
```

Expected version: `0.2.2`

### CLI Commands

```bash
# Prepare a repository for agent-led diagnosis
sensemaking-skills analyze --repo /path/to/my/repo

# Validate an artifact after agent creates it
sensemaking-skills validate --artifact artifacts/repository_sensemaking_brief.md

# Run test automation
sensemaking-skills test

# Durable Campaign foundation
sensemaking-skills campaign init --workspace /path/to/CMP-0001 --campaign-id CMP-0001 --mission "..."
sensemaking-skills campaign status --workspace /path/to/CMP-0001
sensemaking-skills campaign validate --workspace /path/to/CMP-0001
sensemaking-skills campaign history --workspace /path/to/CMP-0001

# Admit exact canonically validated artifact bytes as Campaign evidence
sensemaking-skills campaign ingest \
  --workspace /path/to/CMP-0001 \
  --artifact /path/to/repository_sensemaking_brief.md \
  --framework-root /path/to/sensemaking-skills
```

P5 will add explicit agent-authored `campaign advance`, `campaign defer`, and `campaign close` decision surfaces. Those commands must preserve the rule that the active agent supplies semantic judgment while deterministic machinery validates and persists the contract.

### Make Skills Available to Your Agents

After installation, install skills to your agent-discoverable locations:

```bash
# Install to ~/.agents/skills (default for OpenCode, local agents)
sensemaking-skills setup-skills

# Install to Claude Code / Superpowers plugin cache
sensemaking-skills setup-skills --target claude-superpowers

# Install to both locations
sensemaking-skills setup-skills --target all

# Preview what would be installed without actually installing
sensemaking-skills setup-skills --dry-run

# Overwrite existing skills
sensemaking-skills setup-skills --force
```

Once installed, agents can invoke the skills:
```
/skill using-sensemaking       # Bootstrap: teaches fog classification
/skill repo-sensemaker         # Diagnostic: analyzes repositories
/skill workflow-planner        # Planning: creates orchestration plans
```

---

## Current Architecture

### Agent-native Campaign control

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
durable workspace
```

The durable control invariant is:

```text
warranted responsibility
!= available capability
!= authorized capability
```

Campaign machinery records and enforces contracts; it does not become the semantic router.

### Two Invocation Paths

**Path 1: Claude Code / Agent**
```
Load skill → Invoke skill as agent → Read SKILL.md → Execute procedure
```
This is how full semantic diagnosis is performed.

**Path 2: Python / CLI utilities**
```
sensemaking-skills campaign status ...
python scripts/probe-repo.py ...
python scripts/validate-and-report.py ...
```
For durable campaign state, validation, testing, and automation.

---

## How to Use

### Two Usage Paths

**Path 1: Agent-native (Recommended for Diagnosis)**

Use Claude Code or another agent environment for full repository diagnosis:

```bash
# 1. Clone and open in Claude Code
git clone https://github.com/ThorStarlord/sensemaking-skills.git
cd sensemaking-skills

# 2. Ask your agent to read the bootstrap skill
# Read `skills/using-sensemaking/SKILL.md`

# 3. Then ask the agent to diagnose your target repository
# Use `skills/repo-sensemaker/SKILL.md` to analyze /path/to/my/repo
# Produce artifacts and validate them
```

**Path 2: Local CLI (Utilities)**

Use the CLI for campaign persistence, validation, testing, and environment preparation:

```bash
sensemaking-skills analyze --repo /path/to/my/repo
sensemaking-skills validate --artifact artifacts/repository_sensemaking_brief.md
sensemaking-skills campaign status --workspace /path/to/CMP-0001 --json
sensemaking-skills test --repos 100
```

**Note:** The CLI `analyze` command prepares the environment and prints instructions for the agent-led diagnosis workflow. It does not generate the brief by itself — the agent (reading the skills) does that work.

### Option 1: Use Locally with Claude Code or Another Agent

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ThorStarlord/sensemaking-skills.git
   cd sensemaking-skills
   ```

2. **Open this repository in your agent environment.**

3. **Ask the agent to read the bootstrap skill:**
   ```
   Read `skills/using-sensemaking/SKILL.md`.
   Then use `skills/repo-sensemaker/SKILL.md` to analyze `/path/to/target/repo`.
   Produce a `repository_sensemaking_brief`.
   Validate the artifact with `scripts/validate-and-report.py`.
   ```

4. **For workflow planning, ask the agent to use the generated brief:**
   ```
   Use `skills/workflow-planner/SKILL.md` to convert the brief into a `workflow_orchestration_plan`.
   Validate the plan with `scripts/validate-and-report.py`.
   ```

#### Optional: Install Skills into Claude Code

If your Claude Code environment supports local skill installation, you can copy the skills directory:

```bash
mkdir -p ~/.claude/skills
cp -R skills/* ~/.claude/skills/
```

Then restart or reload Claude Code if needed.

Depending on your Claude Code setup, you may be able to invoke:

```
/skill repo-sensemaker
/skill workflow-planner
```

If those commands are not available, use the fallback method above: ask the agent to read the relevant `SKILL.md` files directly.

### Option 2: Validate Existing Artifacts with Python Scripts

Python scripts validate artifacts produced by agents. They do not currently replace the agent-led diagnosis process.

**Validate a repository sensemaking brief:**
```bash
python scripts/validate-and-report.py artifacts/repository_sensemaking_brief.md
```

**Validate a workflow orchestration plan:**
```bash
python scripts/validate-and-report.py artifacts/workflow_orchestration_plan.md
```

**Run individual validators directly:**
```bash
python scripts/validate-brief.py artifacts/repository_sensemaking_brief.md --json
python scripts/validate-plan.py artifacts/workflow_orchestration_plan.md --json
```

**Run shadow-mode test automation:**
```bash
python scripts/shadow-mode-runner.py
```

---

## Core Skills

### Diagnostic Skills
- **`repo-sensemaker`** — Analyzes repository structure and produces a 14-section diagnostic brief
- **`workflow-planner`** — Converts diagnostic brief into a 10-section orchestration plan

### Validation Skills
- **`validate-brief.py`** — Validates repository_sensemaking_brief artifacts against contract
- **`validate-plan.py`** — Validates workflow_orchestration_plan artifacts against contract
- **`validate-and-report.py`** — Canonical validation router/report boundary

---

## Tooling

### Probe Engine

Deterministic repository probes for verified current state. `repo-sensemaker`
consumes the report it produces; you can also run it standalone on any repo:

```powershell
python scripts/probe-repo.py --repo-root <path> [--output probe-report.yaml]
```

The report (`probe-report.yaml`) contains git state, the verification-gap metric
`Vg` (declared vs CI-enforced checks, from README + `.github/workflows`), the
context-entropy metric `Ce` (untracked+ignored volume / tracked volume), test
collection stats, validator fixture coverage, and change churn. Validate a
report with `python scripts/validate-probe-report.py <report.yaml>`.

## Repository Structure

```
sensemaking-skills/
├── src/sensemaking_skills/
│   ├── campaign_semantics/         (Typed Campaign domain contracts)
│   ├── campaigns/                  (Durable workspace, service, artifact admission)
│   ├── campaign_accounting/        (Campaign run accounting)
│   ├── campaign_validation/        (Campaign validation)
│   ├── exploratory_authorization/  (Exploratory capability minting)
│   ├── exploratory_execution/      (Exploratory execution incl. GitHub approval)
│   ├── commands/                   (CLI commands)
│   └── defaults/                   (Default configuration)
├── skills/
│   ├── repo-sensemaker/
│   │   ├── SKILL.md              (Skill definition)
│   │   ├── agents/               (Agent definitions)
│   │   └── references/           (Fog classification rules)
│   ├── workflow-planner/
│   │   ├── SKILL.md
│   │   ├── agents/
│   │   └── references/           (Workflow registry, artifact contracts)
│   └── [other skills...]
├── scripts/
│   ├── validate-and-report.py    (Canonical validator router/report boundary)
│   ├── validate-brief.py         (Validation)
│   ├── validate-plan.py          (Validation)
│   ├── shadow-mode-runner.py     (Test automation)
│   └── [utilities...]
├── examples/
│   └── [sample briefs and plans]
├── tests/
│   └── [test suite]
├── CONTEXT.md                     (Architecture and principles)
├── docs/
│   ├── sensemaking-campaign.md   (Canonical Campaign product model)
│   ├── productization-v0.3.md    (Active versioned delivery plan)
│   ├── philosophy/               (Design philosophy)
│   ├── adr/                      (Architecture Decision Records)
│   └── archive/                  (Archived phase reports)
└── setup.py / pyproject.toml     (Packaging metadata)
```

---

## Evidence of Correctness

### Scenario 5: Budget Exhaustion (Proven)
- ✅ Real artifact with 3 repair attempts
- ✅ Same error persists across attempts
- ✅ No 4th attempt (budget respected)
- ✅ Graceful escalation message

See: [docs/archive/phase-reports/SCENARIO-5-CLEAN-TEST-EVIDENCE.md](docs/archive/phase-reports/SCENARIO-5-CLEAN-TEST-EVIDENCE.md)

### Week 1: Real Execution
- ✅ 10 real repositories tested
- ✅ Real execution times measured (0.131s avg, 0.138s P95)
- ✅ Honest results documented (infrastructure works, repos lack artifacts)

See: [docs/archive/phase-reports/WEEK1-REAL-EXECUTION-EVIDENCE.md](docs/archive/phase-reports/WEEK1-REAL-EXECUTION-EVIDENCE.md)

---

## Next: P5 — Agent-Authored Campaign Decisions

The repository's active program is **productization / implementation**, not Goal A experiment execution.

P0–P4 are integrated. The current bounded frontier is P5:

```text
sensemaking-skills campaign advance
sensemaking-skills campaign defer
sensemaking-skills campaign close
```

The active coding agent supplies the semantic decision. Deterministic Campaign machinery validates evidence/authority/state contracts and persists a reconstructible transition. P5 must not infer semantic next action, rank Skills, or turn validator output into automatic routing.

After P5, the planned v0.3 sequence is capability registry → durable handoff/resume → artifact/evidence lineage → reconciliation lifecycle → harness adapters → external golden-path release qualification.

Goal A and other research programs remain preserved evidence/research surfaces. They are not the current product-development queue unless explicitly reactivated by owner direction. See [STATUS.md](STATUS.md) and [docs/productization-v0.3.md](docs/productization-v0.3.md) for the active state and roadmap.

---

## Development

**Contributing:**
- Bug reports: [Issues](https://github.com/ThorStarlord/sensemaking-skills/issues)
- Feature requests: [Discussions](https://github.com/ThorStarlord/sensemaking-skills/discussions)
- Pull requests welcome — please include tests

**Philosophy:**
See [docs/philosophy/ARTIFACT_DRIVEN_AGENTIC_ENGINEERING.md](docs/philosophy/ARTIFACT_DRIVEN_AGENTIC_ENGINEERING.md) for the design principles behind this system.

---

## License

MIT License. See [LICENSE](LICENSE) for details.

---

## Quick Links

- **[STATUS.md](STATUS.md)** — Current implementation frontier and operating state
- **[Canonical Sensemaking Campaign model](docs/sensemaking-campaign.md)** — Durable product definition
- **[v0.3 Productization Plan](docs/productization-v0.3.md)** — Active versioned delivery roadmap
- **[CONTEXT.md](CONTEXT.md)** — Architecture overview and principles
- **[GETTING_STARTED.md](GETTING_STARTED.md)** — Real-world examples and workflows
- **[INSTALLATION.md](INSTALLATION.md)** — Step-by-step setup guide
- **[API.md](API.md)** — Python API reference
- **[CLAUDE.md](CLAUDE.md)** — Agent guidelines and hooks
- **[Agent-native operating workflow](docs/agent-native-operating-workflow.md)** — Current top-level control loop
- **[Decision vs. orchestration boundary](docs/decision-orchestration-boundary.md)** — Control ownership boundary
- **[Control-model research agenda](docs/research/control-model-research-agenda.md)** — Non-ratified research questions