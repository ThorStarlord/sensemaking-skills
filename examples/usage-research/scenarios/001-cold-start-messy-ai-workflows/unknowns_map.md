# Unknowns Map

## 1. Knowns
- The `sensemaking-skills` repository uses a central `workflow-registry.yaml` for orchestration.
- The `workflow-orchestrator` can execute `local_execution` steps with validation.
- The `problem-framer` sitting before `unknowns-mapper` correctly identifies the "Object Under Pressure."
- Artifact validation scripts are operational and enforce structural compliance.

## 2. Unknowns
- The exact "noise level" of a first-time user's "messy ideas" and whether `problem-framer` needs additional prompt grounding (e.g., few-shot examples).
- Whether the handoff from Step 2 to Step 3 (`repo-sensemaker`) provides enough "filter context" to prevent the sensemaker from scanning the whole repo unnecessarily.
- The success rate of the `Object Under Pressure` field in identifying the *actual* weakest boundary in a previously unseen repository.

## 3. Assumptions
- We assume that "raw fog" is the primary bottleneck, and once framed, the repository scanning becomes trivial.
- We assume that the user will approve artifacts at the gates without needing significant technical training.
- We assume that the `stopping_rule` in this artifact will be actionable for the `workflow-orchestrator` to decide whether to loop or move forward.

## 4. Risks
- **Over-Scoping**: The research paths defined here might be too broad, leading the user into a "sensemaking loop" where they keep mapping unknowns instead of executing.
- **Template Friction**: The "Object Under Pressure" field might be too technical for some "messy ideas," causing the agent to hallucinate a file that doesn't exist.
- **Handoff Loss**: The `repo-sensemaker` might ignore the specific risks identified here and revert to a generic repository scan.

## 5. Research Paths
- **Path 1 (Routing Clarity)**: Audit the `repo-sensemaker` skill to verify it can consume the `Object Under Pressure` from Step 1 as its primary "Search Seed."
- **Path 2 (Handoff Friction)**: Run a comparative test of Step 2 outputs with and without "Strong Stopping Rule" examples to see if it reduces "Step 3" hallucinations.
- **Path 3 (Instruction Quality)**: Verify if the "Problem Under the Problem" from Step 1 is sufficient to guide the "Research Paths" in Step 2 without manual user intervention.

## 6. Stopping Rule
Stop when every "Risk" identified in Section 4 has a corresponding "Research Path" in Section 5, and the Stopping Rule identifies at least one specific registry file or documentation section that must be validated before Step 3.
