# Phase 3 Testing: Feedback Form

**Please fill this out after completing the diagnosis workflow.**

---

## Tester Information

**Your Name**: [Name]  
**Your Role**: [Backend Engineer / Frontend Engineer / DevOps / PM / Other]  
**Experience with AI/Agents**: [New to this / Some experience / Very comfortable]  
**Date**: [YYYY-MM-DD]  
**Session Duration**: [Minutes spent on full workflow]

---

## Part 1: Installation & Setup

### 1.1 Installation Success
- [ ] Cloned repository successfully
- [ ] Virtual environment created without errors
- [ ] `pip install -e .` completed successfully
- [ ] `sensemaking-skills --version` returned 0.2.1

**If installation failed**, describe the issue:
```
[Error message / system info / what happened]
```

### 1.2 Environment
- **OS**: [Linux / macOS / Windows]
- **Python Version**: [3.11 / 3.12 / Other]
- **Did you use Claude Code?**: [Yes / No / No, used different agent]
- **Any environment surprises?**: [None / Describe]

---

## Part 2: Documentation Clarity

### 2.1 README.md
- [ ] Clearly explained the difference between CLI and agent roles
- [ ] Installation instructions were accurate
- [ ] Understood what "agent-native" means
- [ ] Unclear section(s): [List if any]

### 2.2 GETTING_STARTED.md
- [ ] Instructions were in the right order
- [ ] No confusing jumps between tools (CLI → agent → CLI)
- [ ] Examples matched what you actually saw
- [ ] Unclear step(s): [List if any]

### 2.3 Overall Documentation
**On a scale of 1-5**, how clear was the documentation?
- [ ] 1 - Very confusing
- [ ] 2 - Unclear in several places
- [ ] 3 - Mostly clear, some confusion
- [ ] 4 - Clear, minor issues
- [ ] 5 - Very clear

**What was most confusing?** (If you selected 1-3 above)
```
[Description of confusion]
```

---

## Part 3: Workflow Execution

### 3.1 Did You Complete Each Step?
- [ ] Ran `sensemaking-skills analyze --repo /path` successfully
- [ ] Opened repository in Claude Code/agent
- [ ] Read `skills/using-sensemaking/SKILL.md` (bootstrap skill)
- [ ] Agent read `skills/repo-sensemaker/SKILL.md`
- [ ] Agent produced `artifacts/repository_sensemaking_brief.md`
- [ ] Ran `sensemaking-skills validate --artifact repository_sensemaking_brief.md`
- [ ] Agent read `skills/workflow-planner/SKILL.md`
- [ ] Agent produced `artifacts/workflow_orchestration_plan.md`
- [ ] Ran `sensemaking-skills validate --artifact workflow_orchestration_plan.md`

### 3.2 Where Did You Get Stuck? (If any)
**Step/Issue**: [e.g., "Agent wouldn't load skills", "Validation failed with cryptic error"]  
**What happened**: [Description]  
**How we helped / How you fixed it**: [Did support help? Did you find workaround?]

### 3.3 Workflow Difficulty
**On a scale of 1-5**, how difficult was the workflow to follow?
- [ ] 1 - Too complex, too many tools
- [ ] 2 - Somewhat complex
- [ ] 3 - Moderate, manageable
- [ ] 4 - Fairly straightforward
- [ ] 5 - Very straightforward

**Why?** [Your reasoning]

---

## Part 4: Artifact Quality

### 4.1 Repository Sensemaking Brief

**Did the brief accurately describe your repository?**
- [ ] Yes, diagnosis was spot-on
- [ ] Mostly accurate, minor issues
- [ ] Partially accurate, missed something
- [ ] Inaccurate, doesn't match the codebase
- [ ] Unclear what it was describing

**Fog Type Identified**: [What the tool said]  
**Your Assessment**: [Do you agree? Why or why not?]

**Evidence Citations**: Were file references and line numbers correct?
- [ ] All accurate
- [ ] Mostly accurate
- [ ] Some inaccurate
- [ ] Didn't check

**Recommended Next Steps**: Did they make sense for your repository?
- [ ] Yes, exactly what we need
- [ ] Mostly useful
- [ ] Somewhat helpful
- [ ] Not applicable to our situation
- [ ] Unclear what was recommended

### 4.2 Workflow Orchestration Plan

**Did the plan make sense?**
- [ ] Clear and actionable
- [ ] Mostly clear, minor confusion
- [ ] Somewhat confusing
- [ ] Doesn't match the brief
- [ ] Unclear what workflow was chosen

**Workflow Selected**: [Name of workflow]  
**Is it the right workflow for the problem?**
- [ ] Yes, matches the diagnosis
- [ ] Probably, makes sense
- [ ] Unsure
- [ ] No, different workflow needed

**Would you follow this plan?**
- [ ] Yes, ready to start
- [ ] Probably, with some clarification
- [ ] Maybe, would need to review with team
- [ ] No, doesn't match our priorities

---

## Part 5: Performance

### 5.1 Speed & Responsiveness
- **Time to diagnose** (from `analyze` to brief production): [Minutes]
- **Time to validate** (validate-and-report.py): [Seconds]
- **Overall smoothness**: [Smooth / Occasional lag / Slow / Hung]

### 5.2 Did You Experience Issues?
- [ ] No issues, ran smoothly
- [ ] Minor lag but acceptable
- [ ] Noticeably slow
- [ ] Timeout or hang

**If yes**: Describe what happened:
```
[Issue description, system load, repository size]
```

---

## Part 6: Error Handling & Recovery

### 6.1 Did You Hit Any Errors?
- [ ] No errors at all
- [ ] Minor errors, self-correcting
- [ ] Errors that required investigation
- [ ] Errors that blocked the workflow

### 6.2 If Validation Failed...
**Error Message**: [Copy the error JSON or text]

**Was the error message helpful?**
- [ ] Clear and actionable
- [ ] Somewhat helpful
- [ ] Cryptic or confusing
- [ ] No error recovery info provided

**Did agent/script suggest a fix?**
- [ ] Yes, fix worked
- [ ] Yes, fix didn't work
- [ ] No fix suggested, had to debug
- [ ] No errors encountered

**Bounded Retry Logic** (3-attempt limit):
- [ ] Didn't encounter validation failures, N/A
- [ ] Hit 1 failure, fixed it, retried successfully
- [ ] Hit multiple failures, agent escalated gracefully
- [ ] Unclear what the retry policy was

---

## Part 7: Critical Feedback

### 7.1 What Worked Well?
```
[List 2-3 things that impressed you or worked smoothly]
```

### 7.2 What Needs Improvement?
```
[List 2-3 biggest friction points or confusing aspects]
```

### 7.3 What's Missing?
```
[Features, documentation, tools, or workflows that would help]
```

### 7.4 Blockers for Adoption
**If your team were to use this tool**, what would prevent adoption?
```
[Missing features, cost, complexity, compatibility issues, etc.]
```

### 7.5 Final Question

**Would you recommend this tool to a colleague?**
- [ ] Definitely yes — ready to promote
- [ ] Probably yes — useful with minor caveats
- [ ] Maybe — would need to see more
- [ ] Probably not — needs more work
- [ ] Definitely not — too many issues

**Why?**
```
[Your reasoning]
```

---

## Part 8: Optional Deep Dive

### 8.1 Specific Feature Feedback
If you have thoughts on specific features or workflows:
```
[e.g., "The fog classification was helpful, but couldn't distinguish between X and Y", 
"The workflow_orchestration_plan would be better if it included estimated effort"]
```

### 8.2 Comparison to Alternatives
Have you used similar tools (architecture analyzers, code review tools, diagnostics)?
```
[Tool name: How does sensemaking-skills compare?]
```

### 8.3 Domain-Specific Notes
If you tested on a specific domain (microservices, frontend, docs, etc.):
```
[Domain-specific observations, what worked/didn't work for this type of codebase]
```

---

## Part 9: Submission

**Ready to submit?**

1. Save this form as: `PHASE-3-FEEDBACK-[YourName]-[Date].md`
2. Add it to the repo: `sensemaking-skills/feedback/`
3. Or email to: [testing coordinator email]

---

## Thank You

Your feedback is critical. Thank you for taking the time to test and provide detailed responses.

Results will be analyzed and summarized by **June 5, 2026**. You'll hear from us about next steps.

Questions during testing?  
Reply directly or reach out to: [support contact]

---

**Privacy Note**: Your feedback will be reviewed by the core team only. Repository paths and specific company information will be anonymized in any shared reports.
