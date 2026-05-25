# Installation & Setup Guide

This guide covers setting up **sensemaking-skills** for development and use with Claude Code.

---

## Current State

**What this is:**
- ✅ Agent-native framework (Claude Code + Python scripts)
- ✅ Artifact-driven diagnostic system
- ✅ Proven in production testing (Scenario 5, Week 1 shadow mode)

**What this is NOT (yet):**
- ❌ CLI tool (`sensemaking-skills` command)
- ❌ PyPI package (`pip install sensemaking-skills`)
- ❌ Standalone service

---

## Prerequisites

- **Python 3.11+** (required)
- **Git** (for cloning repository)
- **Claude Code** (recommended for agent-native invocation)
- ~500 MB disk space (including sample test artifacts)

Verify Python version:
```bash
python3 --version
```

Expected output: `Python 3.11.x` or higher

---

## Installation Steps

### Step 1: Clone the Repository

```bash
git clone https://github.com/ThorStarlord/sensemaking-skills.git
cd sensemaking-skills
```

### Step 2: Create Virtual Environment (Recommended)

```bash
python3 -m venv venv
```

Activate it:
- **Windows (PowerShell):**
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
- **Windows (cmd):**
  ```cmd
  venv\Scripts\activate.bat
  ```
- **macOS/Linux:**
  ```bash
  source venv/bin/activate
  ```

### Step 3: Install in Development Mode

```bash
pip install -e .
```

This installs the package in editable mode, allowing you to modify source files without reinstalling.

### Step 4: Verify Installation

```bash
python3 -c "import sys; print('Python path:', sys.executable); print('Version:', sys.version)"
```

Test the validation scripts:
```bash
python3 scripts/validate-brief.py --help
python3 scripts/validate-plan.py --help
python3 scripts/shadow-mode-runner.py --help
```

---

## Invocation Paths

### Path 1: Claude Code / Agent (Recommended)

This is the primary use case. The agent reads skill instruction files and executes workflows.

**Setup:**
1. Open this repository in Claude Code or your agent environment
2. Ask the agent to read `skills/using-sensemaking/SKILL.md`

**Usage:**
Ask the agent to use the skills. Example:
```
Read skills/repo-sensemaker/SKILL.md and diagnose /path/to/my/repo.
Then read skills/workflow-planner/SKILL.md to create a plan.
Validate both artifacts using scripts/validate-and-report.py.
```

**Optional: Install Skills into Claude Code**

If your Claude Code environment supports local skill installation, you can copy skills:

```bash
mkdir -p ~/.claude/skills
cp -R skills/* ~/.claude/skills/
```

Restart Claude Code if needed. Depending on your setup, you may be able to invoke:
```
/skill repo-sensemaker
/skill workflow-planner
```

**If those commands don't work**, use the method above: ask the agent to read the SKILL.md files directly. Both work equally well.

See **GETTING_STARTED.md** for detailed examples.

### Path 2: Validate Artifacts with Python Scripts

Python scripts validate artifacts produced by agents. They do not run diagnostics—the agent does that.

**Validate a brief:**
```bash
python3 scripts/validate-and-report.py artifacts/repository_sensemaking_brief.md
```

**Validate a plan:**
```bash
python3 scripts/validate-and-report.py artifacts/workflow_orchestration_plan.md
```

**Run individual validators:**
```bash
python3 scripts/validate-brief.py artifacts/repository_sensemaking_brief.md --json
python3 scripts/validate-plan.py artifacts/workflow_orchestration_plan.md --json
```

**Run tests:**
```bash
python3 scripts/shadow-mode-runner.py
```

---

## Project Structure

```
sensemaking-skills/
├── skills/                    # Agent-executable skills
│   ├── using-sensemaking/     # Bootstrap skill (load this first)
│   ├── repo-sensemaker/       # Repository diagnosis
│   └── workflow-planner/      # Workflow orchestration
├── scripts/                   # Standalone Python tools
│   ├── validate-brief.py      # Brief validation
│   ├── validate-plan.py       # Plan validation
│   └── shadow-mode-runner.py  # Test runner
├── artifacts/                 # Output artifacts (generated)
├── logs/                      # Execution logs
├── tests/                     # Test suite
├── docs/                      # Documentation
└── setup.py                   # Package metadata (enables pip install -e .)
```

---

## Common Workflows

### Quick Diagnosis (5 minutes)

In Claude Code, ask the agent:

```
Read skills/using-sensemaking/SKILL.md.
Then use skills/repo-sensemaker/SKILL.md to diagnose /path/to/my/repo.
Save the brief to artifacts/ and validate it with:
python scripts/validate-and-report.py artifacts/repository_sensemaking_brief.md
```

Expected output: `artifacts/repository_sensemaking_brief.md`

### Full Analysis with Workflow Plan

In Claude Code, ask the agent:

```
Read skills/using-sensemaking/SKILL.md.
Use skills/repo-sensemaker/SKILL.md to analyze /path/to/my/repo.
Use skills/workflow-planner/SKILL.md to create a plan based on the brief.
Validate both artifacts:
  python scripts/validate-and-report.py artifacts/repository_sensemaking_brief.md
  python scripts/validate-and-report.py artifacts/workflow_orchestration_plan.md
```

Expected outputs:
- `artifacts/repository_sensemaking_brief.md`
- `artifacts/workflow_orchestration_plan.md`

### Running Tests

```bash
# Run all tests
python3 -m pytest tests/ -v

# Run specific test
python3 -m pytest tests/test_validate_brief.py::test_valid_brief -v

# Run with coverage
python3 -m pytest tests/ --cov=scripts --cov-report=html
```

---

## Configuration

### Environment Variables

Optional configuration (not required for basic use):

```bash
# Logging level (DEBUG, INFO, WARNING, ERROR)
export SENSEMAKING_LOG_LEVEL=INFO

# Artifact output directory (default: artifacts/)
export SENSEMAKING_ARTIFACTS_DIR=./artifacts

# Timeout for diagnostic operations (seconds, default: 300)
export SENSEMAKING_TIMEOUT=300
```

---

## Troubleshooting

### Python Version Error

**Error:** `python3: command not found` or wrong version

**Solution:**
```bash
# Check installed Python versions
python --version
python3 --version

# Use the correct version
python3.11 -m venv venv  # explicit version
```

### Import Errors

**Error:** `ModuleNotFoundError: No module named 'sensemaking'`

**Solution:**
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate.ps1  # Windows PowerShell

# Reinstall in editable mode
pip install -e .
```

### Script Execution Permission Denied

**Error:** `Permission denied: scripts/validate-brief.py`

**Solution:**
```bash
# Make scripts executable
chmod +x scripts/*.py

# Or run with python3
python3 scripts/validate-brief.py artifacts/brief.md
```

### Artifact Validation Fails

**Error:** Validation script reports invalid artifact

**Solution:**
1. Check artifact format matches contract (see `CONTEXT.md`)
2. Verify required fields are present
3. Run with verbose output:
   ```bash
   python3 scripts/validate-brief.py artifacts/brief.md --verbose
   ```
4. Check validation rules in `scripts/validate-brief.py` for detailed error messages

### Skills Not Loading

**Issue:** Skill invocation (`/skill using-sensemaking`) doesn't work or skills don't appear

**Solution:**
1. Ensure repository is open in Claude Code
2. Check `.claude/hooks/sessionstart.md` exists
3. Restart Claude Code session
4. **Fallback:** Ask the agent to read the skill files directly:
   ```
   Read the file skills/using-sensemaking/SKILL.md and follow its instructions.
   ```
   This method works in all environments, regardless of skill registration setup.

---

## Development Setup

### Creating a Feature Branch

```bash
git checkout -b feature/your-feature-name
```

### Running Tests Before Commit

```bash
# Run full test suite
python3 -m pytest tests/ -v

# Run with coverage report
python3 -m pytest tests/ --cov=scripts --cov-report=term-missing
```

### Committing Changes

```bash
git add scripts/ skills/ tests/ docs/
git commit -m "feat: description of changes"
git push origin feature/your-feature-name
```

Then create a pull request.

---

## Updating the Package

To get the latest changes:

```bash
git pull origin main
```

If you have local changes:
```bash
git stash
git pull origin main
git stash pop
```

---

## Next Steps

1. **Read GETTING_STARTED.md** for real usage examples
2. **Read CONTEXT.md** for domain knowledge (fog types, artifact contracts)
3. **Explore skills/** directory to understand skill structure
4. **Run tests** to verify everything works: `python3 -m pytest tests/ -v`

---

## Getting Help

- **Technical issues:** Check logs/ directory for execution logs
- **Validation errors:** Run with `--verbose` flag
- **Questions about fog types:** See CONTEXT.md Sections 2-3
- **Artifact format questions:** See `skills/workflow-planner/references/artifact-contracts.yaml`

---

## Version Info

- **Package:** sensemaking-skills
- **Version:** 0.2.0
- **Python:** 3.11+
- **Status:** Beta (Production-ready, agent-native)
- **Last Updated:** 2026-05-25
