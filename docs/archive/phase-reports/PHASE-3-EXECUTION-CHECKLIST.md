# Phase 3 Execution Checklist

**Goal**: Run real-world testing with 3-5 users on real repositories, collect feedback, make go/no-go decision for Phase 4.

**Timeline**: May 25 – Jun 5 (9 days)  
**Decision Point**: Jun 5, 2026 — Proceed to Phase 4 (PyPI) if success criteria met

---

## Pre-Execution (May 25-26)

### Day 1: Define Scope
- [ ] Select 3-5 test users (internal team, partners, or community)
  - [ ] At least one new to Claude Code
  - [ ] At least one with agent experience
  - [ ] Mix of roles: backend, frontend, DevOps, PM
  - **Users selected**: [List names]

- [ ] Confirm each user can commit 1 hour in the May 27–Jun 2 window
  - [ ] [User 1]: Confirmed
  - [ ] [User 2]: Confirmed
  - [ ] [User 3]: Confirmed
  - [ ] [User 4]: Confirmed
  - [ ] [User 5]: Confirmed (if 5 users)

- [ ] Select 3-5 test repositories (or have users bring their own)
  - [ ] Repo 1: [Name/URL] — [Fog type expected]
  - [ ] Repo 2: [Name/URL] — [Fog type expected]
  - [ ] Repo 3: [Name/URL] — [Fog type expected]
  - [ ] Repo 4: [Name/URL] — [Fog type expected] (if 4+ users)
  - [ ] Repo 5: [Name/URL] — [Fog type expected] (if 5 users)

### Day 2: Prepare Materials & Send Kickoff
- [ ] Verify Phase 3 materials exist:
  - [ ] PHASE-3-TESTING-PLAN.md (complete)
  - [ ] PHASE-3-KICKOFF-EMAIL.md (template ready)
  - [ ] PHASE-3-TESTING-FEEDBACK-FORM.md (complete)
  - [ ] GETTING_STARTED.md (up-to-date, tested)

- [ ] Prepare feedback collection system:
  - [ ] Create shared directory: `sensemaking-skills/feedback/`
  - [ ] Create tracking spreadsheet (optional):
    ```
    | User | Repo | Status | Submitted | Comments |
    |------|------|--------|-----------|----------|
    ```
  - [ ] Or: Set up email inbox to collect responses

- [ ] Send kickoff email to all test users
  - [ ] Customize [Tester Name] and [relevant background]
  - [ ] Include repository links or let users choose
  - [ ] Provide direct support contact
  - [ ] Set expectations: 1 hour, flexible May 27–Jun 2

- [ ] Create Phase 3 GitHub issue
  - [ ] Title: `Phase 3: Real-World CLI Testing`
  - [ ] Label: `phase-3-testing`, `testing`
  - [ ] Link to PHASE-3-TESTING-PLAN.md
  - [ ] List testers and repositories
  - [ ] Set deadline: Jun 3 for feedback collection

---

## Execution (May 27 – Jun 2)

### Daily Tasks (May 27-Jun 2)
- [ ] **Every day**: Check for user questions/blockers
  - [ ] Monitor email for support requests
  - [ ] Respond same-day to any issues
  - [ ] Log blockers in Phase 3 GitHub issue

- [ ] **Every 2 days**: Checkpoint message to testers
  - [ ] Email: "How's testing going? Any blockers?"
  - [ ] Offer support if stuck
  - [ ] Collect early feedback snapshots (optional)

### Escalation Path (If User Hits Critical Blocker)
- [ ] User reports issue (e.g., "Agent won't load skills")
- [ ] Provide immediate support:
  - [ ] Debug the specific issue
  - [ ] Create hotfix if needed
  - [ ] Re-test with user after fix
- [ ] Document the issue:
  - [ ] GitHub issue with `phase-3-bug` label
  - [ ] Triage severity: Critical / High / Medium / Low
  - [ ] Link to fix/workaround

---

## Collection & Analysis (Jun 3-4)

### Day 3-4: Collect Feedback
- [ ] Verify all users submitted feedback forms by Jun 3
  - [ ] [User 1]: ✓ Submitted / ⟳ Remind / ✗ Couldn't participate
  - [ ] [User 2]: ✓ Submitted / ⟳ Remind / ✗ Couldn't participate
  - [ ] [User 3]: ✓ Submitted / ⟳ Remind / ✗ Couldn't participate
  - [ ] [User 4]: ✓ Submitted / ⟳ Remind / ✗ Couldn't participate
  - [ ] [User 5]: ✓ Submitted / ⟳ Remind / ✗ Couldn't participate

- [ ] If ≥1 user didn't submit: Follow up
  - [ ] Call/email to understand why
  - [ ] Offer extension if legitimate blocker
  - [ ] Document if they encountered critical failure

- [ ] Consolidate all feedback
  - [ ] Copy forms to `sensemaking-skills/feedback/` directory
  - [ ] Extract key quotes/themes
  - [ ] Create feedback summary spreadsheet

### Tally Results
- [ ] **Installation Success Rate**
  - [ ] Target: 100% (all users installed without critical errors)
  - [ ] Actual: [X out of Y users]
  - [ ] Issues found: [List any install-related bugs]

- [ ] **Documentation Clarity** (average rating from feedback form)
  - [ ] Target: ≥4/5 average
  - [ ] Actual: [Average rating]
  - [ ] Confusion points: [List most common]

- [ ] **Workflow Completion Rate**
  - [ ] Target: ≥80% (≥3 of 4 users complete full workflow)
  - [ ] Actual: [X out of Y users completed]
  - [ ] Dropoff points: [Which steps did people struggle with?]

- [ ] **Artifact Accuracy** (Brief correctly identifies fog type)
  - [ ] Target: ≥80% (≥3 briefs match user understanding)
  - [ ] Actual: [Percentage of accurate briefs]
  - [ ] Misclassifications: [e.g., "Called it product_fog but was actually architecture_fog"]

- [ ] **Critical Bugs Found**
  - [ ] Target: 0 blockers
  - [ ] Actual: [List critical bugs, if any]
  - [ ] Fixed/Unfixed: [Status of each]

- [ ] **User Confidence** (Would they recommend?)
  - [ ] Target: Majority say "Definitely/Probably Yes"
  - [ ] Actual: [Tally of responses]
  - [ ] Reasons for "Maybe/No": [List objections]

### Classify Bugs by Severity
- [ ] **Critical**: Blocks workflow, data loss, or completely wrong diagnosis
  - [ ] Issue 1: [Description]
    - [ ] Severity confirmed
    - [ ] Fix assigned
    - [ ] Re-test with user: [Date]

- [ ] **High**: Major functionality broken or significantly inaccurate
  - [ ] Issue 1: [Description]
  - [ ] Issue 2: [Description]
  - [ ] Plan: Fix before Phase 4? [Yes/No]

- [ ] **Medium**: UI/UX issue, performance, or confusing error message
  - [ ] Issue 1: [Description]
  - [ ] Plan: Fix now or defer to Phase 3.1 patch? [Decision]

- [ ] **Low**: Typo, minor inconsistency, documentation nit
  - [ ] Issue 1: [Description]
  - [ ] Plan: Document for future, don't block Phase 4 [Decision]

---

## Decision & Gate (Jun 5)

### Success Criteria Check
```
✓ = Criterion Met
✗ = Criterion Failed (action required)
⟳ = Conditional (depends on fix)

Installation Success Rate ≥ 100%:        [ ] ✓  [ ] ✗
Documentation Clarity ≥ 4/5 avg:         [ ] ✓  [ ] ✗
Workflow Completion ≥ 80%:               [ ] ✓  [ ] ✗
Artifact Accuracy ≥ 80%:                 [ ] ✓  [ ] ✗
Critical Bugs Found = 0:                 [ ] ✓  [ ] ✗
User Confidence (majority "Yes"):        [ ] ✓  [ ] ✗
```

### Decision Tree

**Are all 6 criteria ✓?**

- **YES** → Proceed to Phase 4 sign-off
  - [ ] Document in PHASE-3-TESTING-RESULTS.md: "PASS"
  - [ ] Get explicit sign-off from users:
    - [ ] User 1 confirms: "Results match my understanding"
    - [ ] User 2 confirms: "Results match my understanding"
    - [ ] User 3 confirms: "Results match my understanding"
  - [ ] Create release notes for Phase 4
  - [ ] Next: Begin Phase 4 (PyPI publication)

- **NO** → Diagnose failure, fix, retry
  - [ ] Identify which criterion(s) failed
  - [ ] Root cause of failure:
    - [ ] Installation bug → Fix setup.py/pyproject.toml → Re-test
    - [ ] Documentation unclear → Rewrite section → Get feedback
    - [ ] Artifact inaccurate → Debug diagnostic logic → Re-test
    - [ ] Critical bug found → Fix code → Re-test with same user

  - [ ] **Retry Window**: Jun 6-10 (optional, depends on severity)
    - [ ] If easy fix (doc rewrite): 1-day turnaround → Re-test 1 user
    - [ ] If code fix needed: 2-3 days → Re-test all users affected
    - [ ] If major issue: Document, plan for Phase 3.1 patch after Phase 4

---

## Post-Decision: Create Results Document

### Document: PHASE-3-TESTING-RESULTS.md

- [ ] Executive Summary
  - [ ] Test period: May 27 – Jun 2, 2026
  - [ ] Participants: [List names and roles]
  - [ ] Repositories tested: [List with sizes/types]
  - [ ] Go/No-Go Decision: [PASS / PASS WITH CAVEATS / FAIL / RETRY]

- [ ] Key Findings
  - [ ] Installation success: [Rate + any issues]
  - [ ] Documentation clarity: [Rate + most confusing points]
  - [ ] Workflow execution: [% completion + blockers]
  - [ ] Artifact accuracy: [% accuracy + misclassifications]
  - [ ] Performance: [Avg diagnosis time, any timeouts]
  - [ ] User satisfaction: [Summary of "would you recommend"]

- [ ] Bugs & Fixes
  - [ ] Critical bugs: [List with fix status]
  - [ ] High bugs: [List with defer/fix decision]
  - [ ] Medium/Low: [Summary, documented for later]

- [ ] User Testimonials (anonymized or attributed)
  - [ ] Quote 1: [What worked well]
  - [ ] Quote 2: [What needs work]
  - [ ] Quote 3: [Would they use this?]

- [ ] Next Steps
  - [ ] If PASS: Schedule Phase 4 (PyPI publication)
  - [ ] If RETRY: Planned re-test date and scope
  - [ ] If FAIL: Document hold and next actions

---

## Final: Commit & Notify

- [ ] Commit all Phase 3 artifacts:
  ```bash
  git add PHASE-3-TESTING-RESULTS.md PHASE-3-EXECUTION-CHECKLIST.md feedback/
  git commit -m "docs: Phase 3 testing complete, PASS decision"
  git push origin main
  ```

- [ ] Close Phase 3 GitHub issue:
  - [ ] Mark as completed
  - [ ] Link to PHASE-3-TESTING-RESULTS.md
  - [ ] Document next milestone (Phase 4 date)

- [ ] Notify test users:
  - [ ] Thank them for participation
  - [ ] Share (anonymized) results summary
  - [ ] Tell them when tool goes to PyPI
  - [ ] Invite them to Phase 5 (general availability feedback)

---

## Optional: Run Shadow Mode in Parallel

If resources permit, run shadow-mode testing **while user feedback is being collected** (May 27–Jun 2):

- [ ] Run shadow-mode automation:
  ```bash
  python scripts/shadow-mode-runner.py --repos 100 --output PHASE-3-SHADOW-RESULTS.md
  ```

- [ ] Shadow mode completes by Jun 3
- [ ] Compare shadow-mode results (quantitative) with user feedback (qualitative)
- [ ] Use for validation: "Do user findings generalize to 100+ repos?"

---

## Timeline at a Glance

| Date | Milestone | Status |
|------|-----------|--------|
| May 25 | Scope defined, kickoff sent | [ ] Complete |
| May 27-Jun 2 | User testing (parallel) | [ ] Complete |
| Jun 3 | Feedback collected | [ ] Complete |
| Jun 4 | Analysis & tally | [ ] Complete |
| Jun 5 | Decision made | [ ] Complete |
| Jun 6+ | Results documented, Phase 4 kickoff (if PASS) | [ ] Complete |

---

## Success Criteria (Final Check)

Before declaring Phase 3 complete, verify:

- [ ] ≥3 users successfully completed end-to-end workflow
- [ ] No critical blockers remain unfixed
- [ ] Installation success rate = 100%
- [ ] Documentation clarity ≥ 80% (≤1 major confusion point per user)
- [ ] Artifact accuracy ≥ 80% (brief matches reality)
- [ ] Users signal confidence: "Yes, I'd use this" or better
- [ ] PHASE-3-TESTING-RESULTS.md document exists and is final
- [ ] All feedback forms collected and archived in `feedback/`
- [ ] Go/No-Go decision made and documented

**✓ All criteria met = Phase 3 PASS = Proceed to Phase 4**

---

## Questions Before Starting?

Before you begin Phase 3, clarify:

1. **Who are the 3-5 test users?** (Names, roles, availability)
2. **Which repositories will they test?** (Or should they choose their own?)
3. **What's the support contact?** (Who answers questions during testing?)
4. **Should we run shadow-mode in parallel?** (Yes/No — adds data but requires compute)
5. **Is Phase 4 scheduled?** (When can PyPI publication happen if Phase 3 passes?)

---

**Ready to execute?** Use this checklist to track progress.  
**Questions?** Clarify above before May 25 end of day.  
**Timeline confirmed?** Begin Phase 3 May 27.
