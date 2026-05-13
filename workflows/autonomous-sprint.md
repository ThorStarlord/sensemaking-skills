# Autonomous Sprint Workflow

The **Autonomous Sprint** is a high-velocity execution pattern that chains multiple specialized skills together to move from a vague idea to verified, committed code in a single session.

It leverages [Matt Pocock's Skills](https://github.com/mattpocock/skills) to ensure engineering rigor while maintaining maximum automation.

## The Sequence

Copy and paste the following prompt once you have achieved clarity via `project-sensemaker`:

```markdown
prompt 1: use grill-with-docs skill to extract the goal from the context. Answer the questions without my input. Do not wait for my approval before answering the next question. 
prompt 2: use to-prd skill with the output of grill-with-docs skill. Approve the design without my approval and save to the output to the repository documentation. 
prompt 3: use to-issues skill with the ouput of the to-prd skill. Skip the publication to the github. 
promp 4: use triage skill in the output of the to-issues skills. 
prompt 5: use tdd with the output of the to-issues skill. Tackle the highest priority issues first that is not blocked by others issues. create and run the red, green, refactor tests without my input. Do not wait for my approval before moving to the next issue. After the highest priority issues was tackled then move the next highest priority issue until the list is exhausted. 
prompt 6: use handoff skill to create a Feature Completion Summary of the chat session.
prompt 7: commit changes to main repository.
```

## How It Works

| Step | Skill | Role |
| :--- | :--- | :--- |
| **1. Align** | `/grill-with-docs` | Decodes jargon and aligns the agent's mental model with yours. |
| **2. Define** | `/to-prd` | Synthesizes the discussion into a durable technical specification. |
| **3. Decompose** | `/to-issues` | Breaks the PRD into end-to-end "vertical slices" (Tracer Bullets). |
| **4. Verify** | `/triage` | Confirms tasks are ready and generates "Agent Briefs" for each. |
| **5. Execute** | `/tdd` | Writes failing tests first, then the minimal code to pass them. |
| **6. Summarize** | `/handoff` | Compacts the session history for future reference. |
| **7. Persist** | `git commit` | Saves the verified work to the repository. |

## Prerequisites

To run this workflow, you must have Matt Pocock's skills installed in your agent environment:

```bash
npx skills@latest add mattpocock/skills
```

## When to Use

Use this workflow when:
- You have already cleared the initial "fog" using `project-sensemaker`.
- You trust the agent to make technical decisions within the established `CONTEXT.md` and ADRs.
- You want to implement a feature "AFK" (Away From Keyboard) while maintaining high TDD standards.
