#!/usr/bin/env python3
"""Phase 1 Real-Agent Orchestration Test Orchestrator.

This script sets up and documents the test execution, but the actual
agent behavior testing must be done with a fresh agent session.

Responsibilities:
1. Prepare test fixtures
2. Document test scenarios
3. Define expected artifacts
4. Capture results
5. Generate test report
"""

import os
import sys
import json
import tempfile
from pathlib import Path
from datetime import datetime


class Phase1TestOrchestrator:
    """Orchestrate Phase 1 real-agent tests."""

    def __init__(self, repo_root: str, output_dir: str = None):
        self.repo_root = repo_root
        self.output_dir = output_dir or os.path.join(repo_root, "test-results", "phase1")
        self.test_results = {}
        self.timestamp = datetime.now().isoformat()

    def prepare_test_environment(self):
        """Prepare directories and logging."""
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(os.path.join(self.output_dir, "fixtures"), exist_ok=True)
        os.makedirs(os.path.join(self.output_dir, "results"), exist_ok=True)
        print(f"[OK] Test environment prepared in {self.output_dir}")

    def document_test_scenario(self, scenario_num: int, scenario_name: str, description: str):
        """Document test scenario."""
        scenario_dir = os.path.join(self.output_dir, f"scenario-{scenario_num}")
        os.makedirs(scenario_dir, exist_ok=True)

        doc = {
            "scenario": scenario_num,
            "name": scenario_name,
            "description": description,
            "timestamp": self.timestamp,
            "status": "pending"
        }

        with open(os.path.join(scenario_dir, "manifest.json"), "w") as f:
            json.dump(doc, f, indent=2)

        return scenario_dir

    def generate_test_plan_summary(self):
        """Generate summary of test plan."""
        summary = """# Phase 1 Real-Agent Orchestration Test Execution Plan

## Test Scenarios

### Scenario 1: Happy Path (Valid Diagnosis)
- Agent reads bootstrap skill
- Agent diagnoses repository
- Produces valid brief
- Validation passes on first try
- Agent completes Phase 1

Expected: 1 validation attempt, VALID result

---

### Scenario 2: Auto-Fix Path (Missing Field)
- Agent diagnoses repository
- Produces brief with missing evidence
- Validation fails: logic_error
- Agent detects it's fixable
- Agent adds evidence and retries (Attempt 2)
- Validation passes

Expected: 2 validation attempts, Attempt 1 FAILED, Attempt 2 VALID

---

### Scenario 3: Escalation Path (Repeated Error)
- Agent diagnoses (Attempt 1)
- Validation fails with error_id X
- Agent retries (Attempt 2)
- Same error_id X appears
- Agent escalates instead of retrying blindly
- Agent presents structured escalation to user

Expected: Agent recognizes same error_id and escalates

---

### Scenario 4: Semantic Conflict (Workflow Routing)
- Agent diagnoses: primary_fog_type = product_fog
- Agent plans workflow: chosen_workflow_id = ui-implementation-workflow (wrong)
- Validation detects: semantic_conflict
- Agent corrects workflow choice
- Retry passes

Expected: semantic_conflict detected, agent fixes routing

---

### Scenario 5: Budget Exhaustion (3-Attempt Limit)
- Attempt 1: error (agent escalates if logic_error)
- Attempt 2: different error or retry (agent adapts)
- Attempt 3: still not fixed
- Agent escalates: "Tried 3 times, can't proceed"

Expected: Agent respects bounded retry limit

---

## Key Outputs to Capture

For each scenario, preserve:
1. Agent transcript (what it said/did)
2. repository_sensemaking_brief artifact
3. validate-and-report.py JSON output
4. validation_run_log.md entries
5. Any failures or behavior gaps

---

## Pass/Fail Criteria

### PASS Scenario 1
- [ ] Agent reads skill
- [ ] Agent diagnoses repo
- [ ] Produces valid brief
- [ ] validate-and-report.py returns valid=true
- [ ] record-validation.py logs entry
- [ ] Agent completes without errors

### PASS Scenario 2
- [ ] Attempt 1: validation fails with specific error_id
- [ ] Agent fixes the issue
- [ ] Attempt 2: validation passes
- [ ] Run log shows both attempts

### PASS Scenario 3
- [ ] Attempt 1: failure with error_id X
- [ ] Attempt 2: SAME error_id X appears
- [ ] Agent escalates instead of retrying
- [ ] Escalation message is structured and helpful

### PASS Scenario 4
- [ ] semantic_conflict detected
- [ ] Agent identifies routing problem
- [ ] Agent corrects workflow choice
- [ ] Retry passes

### PASS Scenario 5
- [ ] Attempt 1, 2, 3 executed
- [ ] Agent respects 3-attempt limit
- [ ] Agent escalates with summary

---

## Decision Gate

If ALL scenarios pass:
-> Phase 1 is agent-proven. Begin Phase 2.

If ANY scenario fails:
-> Identify the specific gap and fix.
-> Rerun the test.

---

Test Plan: docs/phase-1-real-agent-orchestration-test-plan.md
Milestone Criteria: docs/PHASE-1-NEXT-MILESTONE.md
Execution Date: {timestamp}
"""
        return summary.format(timestamp=self.timestamp)

    def create_test_results_template(self):
        """Create template for recording test results."""
        template = {
            "test_run": {
                "timestamp": self.timestamp,
                "phase": "Phase 1",
                "test_type": "Real-Agent Orchestration",
                "scenarios": {}
            }
        }

        # Add scenario templates
        for scenario_num in range(1, 6):
            template["test_run"]["scenarios"][f"scenario_{scenario_num}"] = {
                "name": f"Scenario {scenario_num}",
                "status": "pending",
                "attempts": [],
                "artifacts_produced": [],
                "json_outputs": [],
                "run_log_entries": [],
                "failures": [],
                "notes": ""
            }

        results_path = os.path.join(self.output_dir, "results", "test-results.json")
        with open(results_path, "w") as f:
            json.dump(template, f, indent=2)

        return results_path

    def generate_execution_guide(self):
        """Generate step-by-step execution guide."""
        guide = """# Phase 1 Real-Agent Orchestration Test - Execution Guide

## Before You Start

1. Open fresh Claude Code / Cursor session
2. No prior context about sensemaking-skills
3. SessionStart hook will surface the bootstrap skill automatically

---

## Scenario 1: Happy Path

### User Task
"Diagnose this repository using sensemaking-skills.
Read the bootstrap skill if you haven't seen it yet.
Follow the three-step diagnosis pattern."

### What Agent Should Do
1. Read skills/using-sensemaking/SKILL.md
2. Invoke repo-sensemaker skill
3. Produce repository_sensemaking_brief
4. Call python3 scripts/validate-and-report.py
5. Get valid=true response
6. Call python3 scripts/record-validation.py
7. Complete Phase 1

### Capture
- [ ] Agent transcript
- [ ] repository_sensemaking_brief artifact
- [ ] validate-and-report.py JSON response
- [ ] validation_run_log.md entry
- [ ] Final summary from agent

### Pass Criteria
- Agent completes without errors
- Validation returns valid=true
- Run log has 1 entry with VALID result

---

## Scenario 2: Auto-Fix Path

### Setup
Same as Scenario 1, but the agent initially misses the evidence section.

### What Agent Should Do
1. Diagnose (Attempt 1)
2. Validate -> error_id: repository_sensemaking_brief.evidence.logic_error
3. Agent recognizes: "logic_error, needs re-analysis"
4. Agent re-reads codebase, adds evidence
5. Retry (Attempt 2)
6. Validate -> valid=true
7. Complete

### Capture
- [ ] Both validation attempts in run-log
- [ ] error_id appears in both (shows tracking)
- [ ] Attempt 2 result is VALID
- [ ] Agent's reasoning for fix

### Pass Criteria
- Attempt 1 fails with specific error_id
- Attempt 2 passes
- Agent doesn't retry blindly, solves the problem

---

## Scenario 3: Escalation Path

### Setup
Repository where same error repeats.

### What Agent Should Do
1. Attempt 1: diagnose, validate -> error_id: X
2. Attempt 2: agent retries, validate -> error_id: X (SAME)
3. Agent detects: "same error came back, don't retry"
4. Agent escalates to user
5. User provides input or guidance
6. Attempt 3: retry with user context
7. Complete or escalate again

### Capture
- [ ] Both error_ids in run-log (showing they're the same)
- [ ] Agent's escalation message
- [ ] User input
- [ ] Attempt 3 result

### Pass Criteria
- Agent escalates on repeat error, doesn't retry blindly
- Escalation message includes error_id, message, suggested_fixes
- Agent respects bounded retry

---

## Scenario 4: Semantic Conflict

### Setup
Repository where fog type doesn't match workflow choice.

### What Agent Should Do
1. Diagnose brief: primary_fog_type = product_fog [OK]
2. Plan workflow: chosen_workflow_id = ui-implementation-workflow [WRONG]
3. Validate plan -> semantic_conflict detected
4. Agent recognizes: "workflow routing mismatch"
5. Agent corrects to: product-implementation-workflow
6. Retry -> valid=true

### Capture
- [ ] Semantic conflict detection in validation JSON
- [ ] Agent's decision to correct workflow
- [ ] Retry result

### Pass Criteria
- semantic_conflict error_type detected
- Agent understands it's a routing error
- Agent fixes workflow choice
- Retry passes

---

## Scenario 5: Budget Exhaustion

### Setup
Repository with unfixable issue.

### What Agent Should Do
1. Attempt 1: diagnose, validate -> error (logic_error)
2. Attempt 2: retry with different approach -> error (different error_id)
3. Attempt 3: retry again -> still not valid
4. Agent escalates: "Tried 3 times, still stuck"

### Capture
- [ ] 3 validation attempts in run-log
- [ ] Different error_ids across attempts
- [ ] Agent respects 3-attempt limit
- [ ] Escalation summary

### Pass Criteria
- Agent respects bounded retry (max 3)
- Agent escalates with summary
- No infinite loops or retry past 3

---

## Recording Results

After each scenario, create a result entry in results/test-results.json:
- scenario: 1
- status: passed
- attempts: [list of validation attempts]
- artifact_path: artifacts/repository_sensemaking_brief.md
- validation_result.valid: true
- notes: Agent successfully completed Phase 1 on first try

---

## Final Deliverable

After all scenarios, produce:

1. Test execution transcript (what agent did)
2. Artifacts (briefs, plans, validation outputs)
3. Run-log (validation_run_log.md)
4. Results JSON (structured test results)
5. Recommendation (Phase 1 agent-proven or needs fixes)

---

## Decision Gate

PASS -> Phase 1 is agent-proven. Begin Phase 2.
FAIL -> Fix the identified gap, rerun the scenario.

---

Execution Date: {timestamp}
"""
        return guide.format(timestamp=self.timestamp)

    def run(self):
        """Run test preparation."""
        print("\n" + "="*70)
        print("PHASE 1 REAL-AGENT ORCHESTRATION TEST ORCHESTRATOR")
        print("="*70)

        # Prepare environment
        self.prepare_test_environment()

        # Generate test plan summary
        summary = self.generate_test_plan_summary()
        summary_path = os.path.join(self.output_dir, "TEST-PLAN-SUMMARY.md")
        with open(summary_path, "w") as f:
            f.write(summary)
        print(f"[OK] Test plan summary: {summary_path}")

        # Generate execution guide
        guide = self.generate_execution_guide()
        guide_path = os.path.join(self.output_dir, "EXECUTION-GUIDE.md")
        with open(guide_path, "w") as f:
            f.write(guide)
        print(f"[OK] Execution guide: {guide_path}")

        # Create results template
        results_path = self.create_test_results_template()
        print(f"[OK] Results template: {results_path}")

        # Document scenarios
        for i in range(1, 6):
            scenario_names = [
                "Happy Path (Valid Diagnosis)",
                "Auto-Fix Path (Missing Field)",
                "Escalation Path (Repeated Error)",
                "Semantic Conflict (Workflow Routing)",
                "Budget Exhaustion (3-Attempt Limit)"
            ]
            descriptions = [
                "Agent diagnoses repo, produces valid brief, validation passes",
                "Agent produces brief with missing evidence, retries with fix",
                "Agent encounters same error twice, escalates instead of retrying",
                "Agent detects semantic conflict in workflow routing, corrects it",
                "Agent exhausts 3-attempt budget, escalates with summary"
            ]
            self.document_test_scenario(i, scenario_names[i-1], descriptions[i-1])

        print(f"[OK] All 5 scenarios documented")
        print("\n" + "="*70)
        print("TEST ORCHESTRATION COMPLETE")
        print("="*70)
        print(f"\nTest output directory: {self.output_dir}")
        print(f"\nNext steps:")
        print(f"1. Read: {guide_path}")
        print(f"2. Open fresh Claude Code / Cursor session")
        print(f"3. Run Scenario 1 with fresh agent")
        print(f"4. Capture results in: {results_path}")
        print(f"5. Proceed through remaining scenarios")
        print(f"\nDecision gate: PASS -> Phase 2 | FAIL -> Fix gap, rerun")
        print()


if __name__ == "__main__":
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    orchestrator = Phase1TestOrchestrator(repo_root)
    orchestrator.run()
