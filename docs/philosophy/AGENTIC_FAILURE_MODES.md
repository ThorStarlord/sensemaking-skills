# Agentic Failure Modes

## The Thesis of Anticipated Failure
We cannot predict every specific error, but we can anticipate **classes of failure**. Reliability engineering in agentic workflows is the practice of converting "specific unknown errors" into "predictable error classes," which can then be countered by guardrails, validators, and tests.

## The Taxonomy of Agentic Failure

| Class | Definition | Example |
|-------|------------|---------|
| **1. Input Ambiguity** | User request is vague; agent guesses. | "Make this better" becomes a random plan. |
| **2. Wrong Routing** | Agent chooses the wrong skill or workflow. | Product language triggers PRD instead of diagnosis. |
| **3. Artifact Weakness** | Output is too vague for the next skill. | `problem_frame.md` lacks an inspectable proxy. |
| **4. Handoff Failure** | Consumer skill cannot parse upstream artifact. | `unknowns_map.md` lacks search seeds. |
| **5. Boundary Violation** | Skill performs work outside its instructions. | `problem-framer` starts implementation. |
| **6. Hallucinated Evidence** | Agent cites files or facts it did not inspect. | Claims registry contains a non-existent workflow. |
| **7. Path Hygiene Error** | Agent uses absolute or local file paths. | Use of `file:///` or machine-specific paths. |
| **8. Over-Maintenance** | Agent patches skill logic for a flawed fixture. | Scenario 005 (The Trap). |
| **9. Validator Mismatch** | Validator enforces a wrong or stale contract. | Plan fails due to an outdated validation script. |
| **10. Status Overclaiming** | System claims more maturity than proven. | Claiming "Stable" after a single guided run. |

## Failure Mode and Effects Analysis (FMEA)
We use FMEA to design prevention and detection mechanisms for every step in the Sensemaking Pipeline.

| Step | Possible Failure | Detection | Prevention |
|------|------------------|-----------|------------|
| **problem-framer** | Vague Object Under Pressure (OUP) | Artifact linter / Schema check | Require "Inspectable Proxy" field |
| **unknowns-mapper** | Missing search seeds | Handoff validation | Mandatory "Search Seeds" section |
| **workflow-orchestrator** | Wrong workflow selected | Registry match check | Must cite Registry ID and Intent |
| **skill-maintainer** | Over-maintenance (Mistaken Patch) | Defect Classification gate | Mandatory RCA before `SKILL.md` edit |
| **parallel-task** | File interference | File ownership matrix | Isolated output directory constraints |

## Universal Mechanisms
While the "surface form" of errors changes across domains (UI vs. Strategy vs. Code), the underlying failure mechanisms (Ambiguity, Routing, Handoff) are universal. By targeting these 10 classes, we build a reliability layer that scales across all specialized skill packs.

## Usage in Maintenance
Every `skill_improvement_plan.md` must categorize the observed defect into one of these 10 classes. If the defect is not categorized, the improvement plan is considered **Contract Invalid**.
