# Deployment Checklist: Shadow Mode (Week 1)

**Date**: 2026-05-25  
**Phase**: Shadow Mode Deployment  
**Status**: READY FOR EXECUTION

---

## Pre-Deployment: Code & Infrastructure

### Code Verification
- [ ] All Phase 4.3 bug fixes applied (workflow-planner.py lines 88-116)
- [ ] All validators functional (validate-brief.py, validate-plan.py, validate-artifact.py)
- [ ] All 4 implementation workflows registered in workflow-registry.yaml
- [ ] Artifact contracts current in artifact-contracts.yaml
- [ ] Bootstrap skill operational (using-sensemaking/SKILL.md)
- [ ] Diagnostic skill operational (repo-sensemaker/SKILL.md)

### Environment Setup
- [ ] Staging environment available (separate from production)
- [ ] Database/logging configured
- [ ] API endpoints configured
- [ ] Agent execution environment ready
- [ ] No production traffic isolation confirmed

### Documentation Review
- [ ] DEPLOYMENT-GUIDE-2026-05-25.md reviewed
- [ ] PHASE-4-4-OPERATOR-RUNBOOKS.md reviewed
- [ ] Known limitations understood (PHASE-4-5-PRODUCTION-GATE.md)
- [ ] SLOs defined and baselined
- [ ] Escalation procedures documented

---

## Shadow Mode Execution (Week 1)

### Day 1-2: Initial Deployment

**Deployment Steps**:
- [ ] Deploy code to staging environment
- [ ] Verify all scripts execute without errors
  - [ ] `scripts/validate-and-report.py` works
  - [ ] `scripts/workflow-planner.py` works
  - [ ] `scripts/validate-brief.py` works
  - [ ] `scripts/validate-plan.py` works
- [ ] Verify skill files readable and parseable
- [ ] Verify workflow registry loads correctly
- [ ] Verify artifact contracts validated correctly

**Testing**:
- [ ] Run 5-10 manual test diagnostics on sample repos
- [ ] Verify brief artifacts generated
- [ ] Verify plans generated
- [ ] Verify validation passes/fails as expected
- [ ] Verify escalation logic triggers correctly

**Verification**:
- [ ] No runtime errors in logs
- [ ] No unexpected exceptions
- [ ] No permission issues
- [ ] Agent behavior matches expectations from Phase 4.1

### Day 3-5: Sample Repository Testing

**Test Execution**:
- [ ] Run diagnostics on 100+ sample repositories
  - [ ] 20 small repos (<100 files)
  - [ ] 30 medium repos (100-1000 files)
  - [ ] 30 large repos (1000-5000 files)
  - [ ] 20 very large repos (>5000 files)

**Metrics Collection**:
- [ ] Validation success rate (target: >95%)
- [ ] Validation failure count and types
- [ ] Execution time per repo
- [ ] Escalation rate (expected: <30%)
- [ ] Error distribution by type

**Issue Tracking**:
- [ ] Log all validation failures with error_id
- [ ] Log all execution errors with stack traces
- [ ] Log any unexpected behavior
- [ ] Categorize issues (critical vs. non-critical)

### Day 6-7: Analysis & Go/No-Go Decision

**Metrics Analysis**:
- [ ] Validation success rate calculated
  - [ ] Target: >95%
  - [ ] Actual: ____%
- [ ] Escalation rate calculated
  - [ ] Target: <30%
  - [ ] Actual: ____%
- [ ] Performance metrics reviewed
  - [ ] Average execution time: ___
  - [ ] P95 execution time: ___
  - [ ] Cost per repo: ___

**Issues Assessment**:
- [ ] Critical issues found: ___
- [ ] Non-critical issues found: ___
- [ ] Patterns identified: ___________
- [ ] Root causes determined: ___________

**Go/No-Go Decision**:
- [ ] Validation success >95%? ☐ YES ☐ NO
- [ ] Performance acceptable? ☐ YES ☐ NO
- [ ] No critical issues? ☐ YES ☐ NO
- [ ] Ready for pilot? ☐ GO ☐ NO-GO

**If GO**:
- [ ] Document all findings
- [ ] Archive all test logs
- [ ] Notify pilot team lead
- [ ] Proceed to Week 2 (Pilot Rollout)

**If NO-GO**:
- [ ] Document blocking issues
- [ ] Create action items
- [ ] Re-plan Week 1
- [ ] Do NOT proceed to pilot

---

## Success Criteria for Shadow Mode

| Criterion | Target | Actual | Status |
|-----------|--------|--------|--------|
| Validation success rate | >95% | ___ % | ☐ PASS ☐ FAIL |
| No runtime errors | <5 total | ___ errors | ☐ PASS ☐ FAIL |
| Escalation rate | <30% | ___ % | ☐ PASS ☐ FAIL |
| Performance P95 | <10 seconds | ___ s | ☐ PASS ☐ FAIL |
| Cost per repo | $0.005-0.010 | $___ | ☐ PASS ☐ FAIL |
| No new bugs found | Yes | ___ bugs | ☐ PASS ☐ FAIL |

**Overall Shadow Mode Status**: ☐ GO ☐ NO-GO

---

## Monitoring Setup for Shadow Mode

### Metrics to Track Daily
- [ ] Successful validations
- [ ] Failed validations
- [ ] Validation errors (by error_id)
- [ ] Execution time (min, avg, max, P95)
- [ ] Escalation triggers
- [ ] Resource usage (CPU, memory)

### Alert Conditions
- [ ] Validation success rate drops below 90%
- [ ] Execution time exceeds 10 seconds
- [ ] New error types appear
- [ ] Escalation rate jumps above 40%
- [ ] Runtime exceptions occur

### Daily Report Template
```
Shadow Mode Report: [DATE]

Metrics:
- Validation success: [X]%
- Validations run: [N]
- Failures: [M]
- Escalations: [K]
- Avg execution time: [T]s
- Issues found: [I]

New Issues:
[List any new issues found]

Status:
☐ On Track ☐ Issues Found ☐ Blocking Issues
```

---

## Transition to Week 2

**Approval Required Before Proceeding**:
- [ ] Go/No-Go decision documented
- [ ] All metrics reviewed
- [ ] Issues resolved or mitigated
- [ ] Pilot team identified (10-20 users)
- [ ] Pilot plan reviewed

**Notification Required**:
- [ ] Operations team notified
- [ ] Pilot team lead notified
- [ ] Infrastructure team notified
- [ ] Escalation contacts confirmed

---

**Shadow Mode Start Date**: [TO BE SET]  
**Shadow Mode End Date**: [TO BE SET - 7 days after start]  
**Pilot Rollout Date**: [TO BE SET - depends on Go decision]  
**General Availability Date**: [TO BE SET - 7 days after pilot start]

