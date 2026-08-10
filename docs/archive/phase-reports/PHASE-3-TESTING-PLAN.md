# Phase 3: Real-World CLI Testing Plan

**Start Date**: 2026-05-25  
**Duration**: 1-2 weeks  
**Goal**: Validate CLI usability, agent workflow integration, and documentation accuracy with real users and repositories  
**Success Criteria**: ≥3 successful end-to-end tests, zero critical bugs, user sign-off on roadmap  
**Blocker for**: Phase 4 (PyPI publication)

---

## Objective

Phase 3 proves that:
1. **CLI installation works** — `pip install -e .` on user machines without errors
2. **Agent workflow integrates** — Users can follow GETTING_STARTED.md and successfully diagnose real repositories
3. **Documentation is clear** — No confusion about CLI vs. agent roles; users complete workflow as documented
4. **Edge cases surface** — Real repositories reveal bugs we didn't find internally
5. **Performance meets expectations** — Diagnosis time is reasonable on actual codebases

This is **not** internal testing; this is real users on real repositories.

---

## Phase 3 Stages

### Stage 1: Scope Definition (Before Testing)

**1.1 Repository Selection**
- Identify 3-5 test repositories across different architectures and sizes
- Criteria:
  - At least one in each domain: UI, product, docs, architecture issues
  - Size range: small (< 10k LOC), medium (10-50k), large (50k+)
  - Should have architectural problems agents haven't seen before
  - Public (GitHub) or private with permission

**1.2 User Selection**
- Identify 3-5 users/teams:
  - At least one new to Claude Code / agents (tests documentation clarity)
  - At least one experienced with agents (tests advanced workflows)
  - Mix of backend, frontend, DevOps engineers
  - At least one non-technical product manager (tests accessibility)
- Each user commits to:
  - 30-60 minutes of testing time
  - Running full workflow (diagnosis + validation + planning)
  - Providing structured feedback (see 1.3 below)

**1.3 Feedback Collection Template**
Users fill this out after testing:

```markdown
## Testing Feedback Form

**Tester Name**: [Name]  
**Repository**: [Repo URL]  
**Date**: [Date]  
**Session Duration**: [Minutes]

### Part 1: Installation & Setup
- [ ] Installation succeeded without errors
- [ ] CLI works (`sensemaking-skills --version`)
- [ ] Python environment was correct
- **Issues**: [List any installation problems]

### Part 2: Documentation Clarity
- [ ] README.md was clear about CLI vs. agent roles
- [ ] GETTING_STARTED.md instructions were followable
- [ ] No confusion about which tool to use for each step
- **Confusion Points**: [What was unclear?]

### Part 3: Workflow Execution
- [ ] Ran `sensemaking-skills analyze --repo /path`
- [ ] Opened repository in Claude Code/agent
- [ ] Read bootstrap skill successfully
- [ ] Agent produced repository_sensemaking_brief
- [ ] Artifact validated without errors
- **Workflow Blockers**: [What stopped you?]

### Part 4: Artifact Quality
- [ ] Brief accurately described repository issues
- [ ] Recommended workflow matched your understanding
- [ ] Evidence citations were clear and correct
- [ ] Plan template was understandable
- **Accuracy Issues**: [What was wrong?]

### Part 5: Performance
- [ ] Agent diagnosis completed in reasonable time (< 10 min)
- [ ] No timeouts or hangs
- [ ] Validation was fast (< 30 sec)
- **Performance Notes**: [Unexpected delays?]

### Part 6: Failure Scenarios (if encountered)
- [ ] Error messages were helpful
- [ ] Recovery procedure was clear
- [ ] Retry logic worked (max 3 attempts)
- **Failure Notes**: [What broke?]

### Part 7: Open Feedback
- **Would you recommend this to a colleague?** [Yes/No/Maybe]
- **What worked well?**
- **What needs improvement?**
- **What's missing?**
- **Blockers for adoption?**
```

---

### Stage 2: Test Execution (Week 1)

**2.1 Parallel Testing** (Run simultaneously with 3-5 users)

For each test:
1. Provide user with:
   - Installation link: `pip install -e .` instructions
   - GETTING_STARTED.md guide
   - Feedback form (section 1.3)
   - Support contact (you)

2. User runs through workflow:
   ```bash
   # Step 1: Install locally
   git clone https://github.com/ThorStarlord/sensemaking-skills.git
   cd sensemaking-skills
   python -m venv .venv
   source .venv/bin/activate
   pip install -e .
   
   # Step 2: Verify CLI
   sensemaking-skills --version
   
   # Step 3: Prepare repository
   sensemaking-skills analyze --repo /path/to/test/repo
   
   # Step 4: Open in Claude Code
   # User opens the repo in their agent environment
   
   # Step 5: Read bootstrap skill
   # User asks agent: "Read skills/using-sensemaking/SKILL.md"
   
   # Step 6: Diagnose
   # User asks agent: "Use skills/repo-sensemaker/SKILL.md to analyze /path/to/test/repo"
   # Agent produces artifacts/repository_sensemaking_brief.md
   
   # Step 7: Validate
   # User runs: sensemaking-skills validate --artifact artifacts/repository_sensemaking_brief.md
   
   # Step 8: Plan
   # User asks agent: "Use skills/workflow-planner/SKILL.md to convert the brief"
   # Agent produces artifacts/workflow_orchestration_plan.md
   
   # Step 9: Validate plan
   # User runs: sensemaking-skills validate --artifact artifacts/workflow_orchestration_plan.md
   
   # Step 10: Feedback
   # User fills out feedback form (section 1.3)
   ```

3. Timeline for each user: 45-90 minutes
4. Run all 3-5 users in parallel (compressed 1-week window)

**2.2 Issue Tracking**
- Open GitHub issue for Phase 3 testing: `Testing/Phase-3-Real-World-Validation`
- Add labels: `testing`, `phase-3`, `user-feedback`
- As bugs surface, create sub-issues with reproduction steps

**2.3 Daily Sync**
- Collect daily feedback snapshots (email or shared doc)
- Flag blockers immediately
- Escalate critical bugs same-day

---

### Stage 3: Analysis & Decision (End of Week 1)

**3.1 Aggregate Results**
Tally feedback forms:
- Installation success rate (target: 100%)
- Documentation clarity score (target: ≥4/5)
- Workflow completion rate (target: ≥80%)
- Artifact accuracy score (target: ≥4/5)
- Performance acceptance (target: 100%)

**3.2 Bug Severity Classification**
Classify all issues discovered:
- **Critical**: Blocks workflow, data loss, security (fix before Phase 4)
- **High**: Major functionality broken, incorrect diagnosis (fix before Phase 4)
- **Medium**: UI/UX issue, slow performance, confusing error (consider for Phase 3.1 patch or Phase 4)
- **Low**: Typo, minor inconsistency (document for later)

**3.3 Decision Tree**

```
Do we have ≥3 successful end-to-end tests? (All 3-5 users completed without critical bugs)
├─ NO → Found critical blocker
│   ├─ Fix bug
│   ├─ Re-test with same user(s)
│   └─ Retry decision
├─ YES → Proceed to 3.4

Is documentation accuracy ≥80%? (≤1 major confusion point per user)
├─ NO → Fix documentation
│   ├─ Update README.md or GETTING_STARTED.md
│   ├─ Get user feedback on fix
│   └─ Retry if needed
├─ YES → Proceed to 3.4

Are all critical/high bugs fixed?
├─ NO → Fix and re-test
├─ YES → Proceed to 3.4

✓ Phase 3 PASS → Ready for Phase 4 (PyPI publication)
✗ Phase 3 FAIL → Document issues, schedule retry
```

**3.4 Sign-Off**
- Users confirm: "Results match my understanding of repository issues"
- Users confirm: "I would use this tool for my team"
- Document user sign-offs in PHASE-3-TESTING-RESULTS.md

---

## Test Repositories (Candidates)

### Candidate A: Small, UI-Heavy
- Repository: Open-source React component library
- Issue Type: UI fog (poor componentization, styling inconsistency)
- Size: 5-10k LOC
- Purpose: Test on small, focused codebase

### Candidate B: Medium, Product-Driven
- Repository: SaaS backend with API changes
- Issue Type: Product fog (unclear feature boundaries, API drift)
- Size: 15-30k LOC
- Purpose: Test on growing product codebase

### Candidate C: Large, Architecture Heavy
- Repository: Monorepo with service coupling
- Issue Type: Architecture fog (circular dependencies, tight coupling)
- Size: 50-100k LOC
- Purpose: Test on complex architecture problems

### Candidate D: Docs-Focused
- Repository: Documentation site with code examples
- Issue Type: Docs fog (outdated examples, missing API docs)
- Size: 5-15k LOC
- Purpose: Test docs-specific diagnostics

**Selection**: Pick top 3-4 from candidates, prioritizing diversity of fog types.

---

## Testing Environment

### Requirements
- **OS**: Linux, macOS, or Windows (test at least 2 OSes)
- **Python**: 3.11+ (test both 3.11 and 3.12 if possible)
- **Claude Code**: Latest version (verify agents work)
- **Network**: Internet access for GitHub/PyPI

### Provisioning
- Users clone repo locally or use provided container
- Pre-create test repositories in isolated GitHub org or use public repos
- Provide .env template (none needed, but document if future versions require it)

---

## Success Criteria

| Criterion | Target | Measurement |
|-----------|--------|-------------|
| Installation Success | 100% | 0 install failures across all users |
| Documentation Clarity | ≥80% | ≤1 major confusion point per user avg |
| Workflow Completion | ≥80% | ≥3 of ≥4 users complete full workflow |
| Artifact Accuracy | ≥80% | Brief correctly identifies fog type |
| Critical Bugs | 0 | No blockers in Phase 3; fix all before Phase 4 |
| User Confidence | High | Users say "Yes, I'd use this" |

**Gate**: All criteria must pass before proceeding to Phase 4.

---

## Contingency Plans

### If Installation Fails
- Likely cause: Python path, virtual environment, or package discovery
- Action: Collect error logs, debug src/ layout issue, provide hotfix
- Retry: Same user after fix

### If Documentation Is Unclear
- Likely cause: CLI vs. agent boundary confusion or missing context
- Action: Rewrite confusing section, test with fresh user
- Escalate: If ≥2 users confused on same point, it's a doc bug

### If Agent Workflow Fails
- Likely cause: Agent doesn't load skills correctly or artifact path issue
- Action: Verify SKILL.md is readable; check artifact contract compliance
- Support: Provide agent debugging help to user

### If Performance Is Poor
- Likely cause: Large repository, complex analysis taking >10 min
- Action: Measure actual time; if >15 min, investigate caching
- Note: Acceptable if rare; document as known limitation

### If We Find a Critical Bug
- Action: Fix immediately
- Validation: Re-run with same user to confirm fix
- Timeline: Don't wait for all users; fix fast, validate, move on

---

## Parallel Shadow Mode (Optional, Phase 3.1)

**Recommendation**: Run in **parallel** with user testing, not sequentially.

If time permits, also run shadow-mode test automation:
```bash
python scripts/shadow-mode-runner.py --repos 100 --output PHASE-3-SHADOW-RESULTS.md
```

This provides quantitative data (success rate, error patterns) to compare with qualitative user feedback.

**Shadow mode output informs**:
- Whether we found issues users didn't (e.g., edge cases)
- Whether user feedback generalizes to larger sample
- Performance profile across repository types

---

## Output Artifacts

After Phase 3 completes, produce:

1. **PHASE-3-TESTING-RESULTS.md**
   - Summary of all feedback
   - Bug list with severity and status
   - User sign-offs
   - Go/no-go decision for Phase 4

2. **PHASE-3-TESTING-LOG.md** (optional)
   - Detailed timeline of each user session
   - Issues found and fix status
   - Performance measurements
   - One-off edge cases

3. **Updated GETTING_STARTED.md or README.md**
   - Corrections based on user confusion points
   - Clarifications on common issues

4. **Phase 3 GitHub Issues**
   - Tracked as `phase-3-testing` label
   - Links to feedback form responses
   - Cross-referenced with fixes

---

## Timeline

| Milestone | Duration | Dates |
|-----------|----------|-------|
| Stage 1: Scope Definition | 1-2 days | May 25-26 |
| Stage 2: Test Execution | 5-7 days | May 27-Jun 2 |
| Stage 3: Analysis & Decision | 2-3 days | Jun 3-5 |
| **Phase 3 Total** | **8-12 days** | **May 25 - Jun 5** |

**Decision Point**: Jun 5 — Proceed to Phase 4 if all success criteria met.

---

## Next: Phase 4 (Contingent on Phase 3 Pass)

After Phase 3 sign-off:
- Create GitHub release: `git tag v0.2.1 && git push origin v0.2.1`
- Publish to PyPI: `python -m twine upload dist/*`
- Update installation docs to show `pip install sensemaking-skills`
- Announce on community channels

See DEPLOYMENT-GUIDE-2026-05-25.md for detailed Phase 4 procedures.

---

## How to Execute This Plan

1. **Select test users**: Reach out to 3-5 candidates, confirm commitment (30-60 min)
2. **Prepare test repos**: Ensure candidates are public/accessible
3. **Send kickoff email**: Provide installation link, GETTING_STARTED.md, feedback form
4. **Track daily**: Collect status updates, flag blockers same-day
5. **Debrief**: Gather all feedback forms by end of week
6. **Analyze**: Tally results, classify bugs, make decision
7. **Document**: Write PHASE-3-TESTING-RESULTS.md with go/no-go

---

## Questions for User

Before starting Phase 3, clarify:

1. **Who are the 3-5 test users?** (Internal team, external partners, or open call?)
2. **Which test repositories?** (Use candidates above or different ones?)
3. **Timeline preference**: Compressed 1 week or spread over 2?
4. **Should we run shadow-mode in parallel?** (Adds quantitative data but takes 2-3 hours compute)
5. **Are we testing PyPI installation or `pip install -e .` first?** (Phase 3 = local install; Phase 4 = PyPI)

---

**Status**: Ready to execute Phase 3.  
**Blocker**: Need to identify test users and repositories.  
**Next**: User confirms scope, we proceed with stage 1 or stage 2 immediately.
