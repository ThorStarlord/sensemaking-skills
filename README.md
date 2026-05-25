# Sensemaking Skills

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

An agent-native framework for repository diagnosis and workflow orchestration. Turns repository uncertainty into clear problem frames, research paths, and actionable next-step prompts.

**Status**: Beta (Scenario 5 tested and proven)  
**Current Use**: Agent/Claude Code invocation (not a standalone CLI)  
**Maturity**: Production-ready for agent-based use, user-facing features in development

---

## What This Is

✅ **Proven diagnostic framework** — Scenario 5 budget-exhaustion testing confirms:
- Error recovery with bounded retry logic (3 attempts)
- Graceful escalation when limits exhausted
- Real execution on actual repositories with honest metrics

✅ **Artifact-driven engineering** — All communication happens via durable, validated artifacts:
- `repository_sensemaking_brief` (14-section diagnostic)
- `workflow_orchestration_plan` (10-section execution plan)
- Validation ensures quality and safety

✅ **Agent-native design** — Built for Claude Code and agent invocation:
- Skills defined in SKILL.md files
- Orchestration via artifact handoffs
- No external dependencies

## What This Is NOT

❌ **Not a CLI tool** — No `sensemaking-skills` command (yet)  
❌ **Not a PyPI-installable package** — Can't `pip install` (yet)  
❌ **Not a black-box service** — Requires agent/Claude Code invocation  
❌ **Not a replacement for specialized tools** — Complements PM skills, UI skills, TDD tools  

---

## Current Architecture

### Two Invocation Paths

**Path 1: Claude Code / Agent**
```
Load skill → Invoke skill as agent → Read SKILL.md → Execute procedure
```
This is how it's used today.

**Path 2: Python Scripts (Direct)**
```
python scripts/shadow-mode-runner.py <repo_path>
python scripts/validate-brief.py <artifact_path>
python scripts/validate-plan.py <artifact_path>
```
For testing and automation.

---

## How to Use Today

Sensemaking Skills is currently agent-native. The primary use case is opening this repository in Claude Code or another coding agent and having the agent read the skill instructions.

It is not yet a standalone CLI and is not yet installable from PyPI.

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
- **`validate-and-report.py`** — Full validation pipeline with error recovery

---

## Repository Structure

```
sensemaking-skills/
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
│   ├── validate-brief.py         (Validation)
│   ├── validate-plan.py          (Validation)
│   ├── shadow-mode-runner.py     (Test automation)
│   └── [utilities...]
├── examples/
│   └── [sample briefs and plans]
├── tests/
│   └── [test suite]
├── docs/
│   ├── CONTEXT.md                (Architecture and principles)
│   ├── philosophy/               (Design philosophy)
│   └── adr/                       (Architecture Decision Records)
└── setup.py / pyproject.toml     (Packaging metadata)
```

---

## Evidence of Correctness

### Scenario 5: Budget Exhaustion (Proven)
- ✅ Real artifact with 3 repair attempts
- ✅ Same error persists across attempts
- ✅ No 4th attempt (budget respected)
- ✅ Graceful escalation message

See: [SCENARIO-5-CLEAN-TEST-EVIDENCE.md](SCENARIO-5-CLEAN-TEST-EVIDENCE.md)

### Week 1: Real Execution
- ✅ 10 real repositories tested
- ✅ Real execution times measured (0.131s avg, 0.138s P95)
- ✅ Honest results documented (infrastructure works, repos lack artifacts)

See: [WEEK1-REAL-EXECUTION-EVIDENCE.md](WEEK1-REAL-EXECUTION-EVIDENCE.md)

---

## Next: Roadmap to User-Ready

**Phase 2.1: User-Facing Installation**
- [ ] Create CLI interface (click/argparse)
- [ ] Add entry points in setup.py
- [ ] Enable `sensemaking-skills analyze --repo /path`
- [ ] Publish to PyPI

**Phase 2.2: Documentation**
- [ ] Write GETTING_STARTED.md with real examples
- [ ] Write INSTALLATION.md with step-by-step guide
- [ ] Create API reference documentation
- [ ] Add troubleshooting guide

**Phase 2.3: Quality Gates**
- [ ] Add integration tests for CLI
- [ ] Test on real projects
- [ ] Create user feedback loops

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

- **[CONTEXT.md](CONTEXT.md)** — Architecture overview and principles
- **[GETTING_STARTED.md](GETTING_STARTED.md)** — Real-world examples and workflows
- **[INSTALLATION.md](INSTALLATION.md)** — Step-by-step setup guide
- **[API.md](API.md)** — Python API reference
- **[CLAUDE.md](CLAUDE.md)** — Agent guidelines and hooks

