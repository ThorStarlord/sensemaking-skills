# [EXPERIMENTAL] Autonomous Sprint Workflow

> [!CAUTION]
> **Status**: Experimental / Alpha
> This workflow is designed for high-velocity, automated execution. It is **unstable** and may produce unexpected results or architectural drift if not carefully monitored.

> [!IMPORTANT]
> **Mandatory Human Approval Gates**:
> - Do not approve PRDs or designs without explicit user permission.
> - Do not commit directly to `main` by default; use feature branches unless the user overrides.
> - Scripts enforce structure, but skills provide judgment. **Humans approve usefulness.**

The **Autonomous Sprint** is a high-velocity execution pattern that chains multiple specialized skills together to move from a vague idea to verified, committed code in a single session.

It leverages [Matt Pocock's Skills](https://github.com/mattpocock/skills) to ensure engineering rigor while maintaining maximum automation.

Copy and paste the following prompt once you have achieved clarity via `repo-sensemaker`:

```markdown
prompt 1: use docs-aligner skill to extract the goal from the context. Answer each question by exploring the codebase and existing docs. If a decision is not documented, make the most conservative architectural recommendation consistent with the project's domain language (CONTEXT.md). Prepare the alignment report and STOP for my review.

prompt 2: use to-prd skill with the output of docs-aligner skill. Synthesize the design using the updated CONTEXT.md and any new ADRs as the source of truth. Save the PRD to the `docs/` directory and STOP for my review.

prompt 3: use to-issues skill with the output of the to-prd skill. Break the work into AFK-compatible vertical slices (tracer bullets). Prepare the issue list and STOP for my review.

prompt 4: use triage skill on the output of the to-issues skills. Ensure an AGENT-BRIEF.md is generated for each issue. Move them to `ready-for-agent/` and STOP for my review.

prompt 5: use tdd with the output of the triage skill. Consume the Agent Briefs for each issue. Tackle the highest priority, unblocked issues first. Run the red-green-refactor loop. For each successful vertical slice, create a feature branch and prepare a commit summary for my review. DO NOT commit to main or push without explicit approval.

prompt 6: use handoff skill to create a Feature Completion Summary of the chat session.
```

## How It Works

| Step | Skill | Role |
| :--- | :--- | :--- |
| **1. Align** | `/docs-aligner` | Self-interviews using code/docs to reach shared understanding. |
| **2. Define** | `/to-prd` | Synthesizes a spec based on the new `CONTEXT.md`. |
| **3. Decompose** | `/to-issues` | Breaks work into AFK-compatible vertical slices. |
| **4. Brief** | `/triage` | Generates `AGENT-BRIEF.md` for each task. |
| **5. Build** | `/tdd` | Executes TDD cycles and **prepares commit summaries**. |
| **6. Summary** | `/handoff` | Creates a completion summary of the session. |

> [!IMPORTANT]
> **Prerequisite**: You must have run `/setup-matt-pocock-skills` in the target repository at least once for these skills to function correctly.

## Prerequisites

To run this workflow, you must have Matt Pocock's skills installed in your agent environment:

```bash
npx skills@latest add mattpocock/skills
```

## When to Use

Use this workflow when:
- You have already cleared the initial "fog" using `repo-sensemaker`.
- You trust the agent to make technical decisions within the established `CONTEXT.md` and ADRs.
- You want to implement a feature "AFK" (Away From Keyboard) while maintaining high TDD standards.
