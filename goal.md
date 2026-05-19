# Goal: Sensemaking Skills

## North Star

Turn a high-level project goal into a fully executed implementation — with the user only providing the goal and reviewing the final output.

## What This Means in Practice

The user gives:
- A description of what they want to build (e.g., "a proactive marketing SaaS for low-tech small business owners")
- An execution mode (autonomous / guided / plan-only)

The system handles:
- Classifying the project type and fog
- Selecting the right workflow from the registry
- Sequencing the right skills in order
- Validating each artifact before the next step
- Stopping only at explicit approval gates or on validation failure

The user reviews:
- Final artifacts (PRD, implementation plan, issues, handoff prompt)
- Gate decisions at critical transitions (in guided mode)

## The Two-Skill Core

```
raw_goal
  → repo-sensemaker      (diagnoses fog, classifies project, routes internally)
  → workflow-planner (picks workflow from registry, executes skill sequence)
  → artifacts            (validated outputs ready for downstream use)
```

## Success Criteria

- A real project (not a system-proving test) runs from raw goal to final artifacts without requiring low-level decisions from the user.
- The system correctly classifies project type, selects workflow, and sequences skills — all from a plain-language goal description.
- Compounding errors are caught at each step by the validator stack before they propagate.
- Multiple parallel projects can be handed off to the system without cognitive overhead.

## What This Is Not

- A replacement for specialized skills (PM skills, creative writing, UI, engineering). Those skills do the domain work. This system routes to them.
- A fully autonomous agent that never needs human input. Approval gates at critical transitions are a feature, not a bug.
- A general-purpose coding agent. It orchestrates skills; it does not write code directly.
