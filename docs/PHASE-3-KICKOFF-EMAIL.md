# Phase 3 Testing: Kickoff Email Template

---

**Subject**: Help Test Sensemaking Skills — 1 Hour, Real Repository, $[incentive if applicable]

**To**: [Tester Name]

---

Dear [Tester Name],

We're ready to test sensemaking-skills with real users on real repositories, and we'd like your help.

**What we're testing**: A CLI tool + agent workflow that diagnoses repository problems (architecture coupling, missing documentation, unclear product boundaries, etc.). The diagnosis produces an actionable plan.

**Your role**: 
- Install the tool locally (5 minutes)
- Run it on a target repository (40 minutes)
- Fill out a feedback form (15 minutes)
- **Total time commitment**: ~1 hour

**Why we're asking you**:
- You have hands-on experience with [relevant background: agent workflows / architecture / [your domain]]
- Your feedback will directly influence the tool's usability before we publish it publicly

---

## Quick Start

### 1. Clone & Install (5 min)
```bash
git clone https://github.com/ThorStarlord/sensemaking-skills.git
cd sensemaking-skills
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -e .

# Verify it works
sensemaking-skills --version
# Expected: 0.2.1
```

**System requirements**:
- Python 3.11+
- Any OS (Linux, macOS, Windows)
- ~10 minutes for install + dependencies

**Having issues?** Reply to this email with error messages and screenshots.

### 2. Prepare a Repository (5 min)
Choose one of these test repositories (or use your own):

**Option A: Small, UI-focused** (Great for quick testing)
- Pick any open-source React component library
- Or: `https://github.com/airbnb/visx` (visualization library)
- Size: ~5-10k LOC

**Option B: Medium, Product-driven** (Real-world example)
- `https://github.com/ThorStarlord/sensemaking-skills` (this project!)
- Or: Pick a SaaS backend you know
- Size: 10-50k LOC

**Option C: Large, Architecture-heavy** (Complex example)
- `https://github.com/kubernetes/kubernetes` or similar monorepo
- Or: Your own production codebase (if you have permission to share insights)
- Size: 50k+ LOC

We recommend **Option A or B** for first-time testing (faster feedback cycle).

### 3. Run Diagnosis (30-40 min)
Follow the workflow in **GETTING_STARTED.md**:

```bash
# Step 1: Prepare the repository
sensemaking-skills analyze --repo /path/to/your/repo

# Step 2: Open in Claude Code or your agent environment
# (You'll need Claude Code or access to an AI agent that can read files)

# Step 3: Ask the agent to read the bootstrap skill
# In Claude Code: "Read the file `skills/using-sensemaking/SKILL.md` and follow its instructions."

# Step 4: Ask the agent to diagnose your repository
# "Use `skills/repo-sensemaker/SKILL.md` to analyze /path/to/your/repo.
# Produce a `repository_sensemaking_brief` and save it to `artifacts/`."

# Step 5: Validate the brief
sensemaking-skills validate --artifact artifacts/repository_sensemaking_brief.md

# Step 6: Ask the agent to create an orchestration plan
# "Use `skills/workflow-planner/SKILL.md` to convert the brief into a 
# `workflow_orchestration_plan` and save it to `artifacts/`."

# Step 7: Validate the plan
sensemaking-skills validate --artifact artifacts/workflow_orchestration_plan.md
```

This should take 30-40 minutes depending on repository size.

### 4. Fill Out Feedback Form (15 min)
After completing the workflow, fill out the form here:
**[LINK TO: PHASE-3-TESTING-FEEDBACK-FORM.md]**

The form asks simple questions about:
- Whether installation worked
- Whether documentation was clear
- Whether the diagnosis made sense
- Whether the plan was useful
- What could be better

---

## Timeline

| Date | What Happens |
|------|--------------|
| **Today (May 25)** | You receive this email |
| **May 27–Jun 2** | You run through the workflow (at your own pace) |
| **Jun 3** | Submit feedback form |
| **Jun 5** | We analyze results, decide on Phase 4 (PyPI publication) |

**Flexible**: Work on this during your available time. No strict deadline within the week.

---

## Support

If you hit any blockers:
- **Installation errors**: Reply with error messages + system info (OS, Python version)
- **Workflow confusion**: Reply with which step you're stuck on
- **Agent not loading skills**: Common issue — reply and we'll help debug
- **Unexpected behavior**: Reply with details + repository path (if shareable)

We're here to help. This testing is collaborative.

---

## What This Is & Isn't

**This tool diagnoses problems**, not fixes them. After diagnosis, you get:
- A clear description of the core issue (architecture coupling, missing docs, etc.)
- Evidence (specific files and line numbers)
- A recommended workflow to address the problem
- Next steps

**You then decide**: Does the diagnosis match your understanding? Is the recommended workflow helpful?

---

## Why This Matters

We've tested this internally and it works. But real repositories are messy and diverse. Your feedback helps us:
- Fix bugs we didn't find internally
- Clarify documentation
- Understand what's useful vs. what's not
- Build something teams actually want to use

After Phase 3 passes, we publish to PyPI and open to the broader community.

---

## Next Steps

1. **Reply to confirm**: Can you participate? Any scheduling constraints?
2. **Install & run**: Work through the workflow (May 27–Jun 2)
3. **Submit feedback**: Fill out form by Jun 3
4. **We analyze & decide**: Results by Jun 5

---

Thank you for helping us ship this. Your feedback is critical.

Questions?  
Reply to this email.

—  
[Your Name]  
sensemaking-skills team

---

**P.S.** — If you run into issues, that's valuable data. We want to know what breaks so we can fix it before publishing.
