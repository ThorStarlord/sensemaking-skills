# T1 Pilot Task — Semantic Mechanism Routing (disposable, instrument-calibration only)

pilot_id: T1
family: T1
disposable: true (never a main-study candidate)
repository state: frozen SHA `a7b957d738f5e1c42b6dd06824c3e6029d816bcd`, no fixture changes required beyond what the task itself asks for

## Visible task contract

This repository ships a `sensemaking_skills` Python package that other
repositories install as a dependency to get sensemaking workflow support.
When a repository installs the package but hasn't yet set up any of its own
sensemaking scaffolding (no `skills/workflow-planner/` directory, no
`.sensemaking/` directory — a bare, freshly-installed target repo), it
should still have a baseline set of workflows available out of the box.

Add a new workflow definition, available out of the box to every repository
that installs this package — including ones that have not created any
sensemaking scaffolding of their own yet — with these exact properties:

```
id: duplicate-detection-workflow
display_name: Duplicate Detection Workflow
purpose: Scan a repository for duplicated logic or configuration and report
  the findings without modifying anything.
allowed_execution_modes:
  - plan_only
  - guided_execution
steps:
  - id: 1
    skill: repo-sensemaker
    step_type: local_execution
    gate: review_diagnosis
    input_source: repository_state
    output_artifact: repository_sensemaking_brief
```

(`initial_inputs` and `requires_run_log` are up to you — follow the existing
convention used by other workflow entries in whichever file you determine is
the right place for this. `description` is optional.)

## Non-goal

Do not just add this entry to every workflow-registry file you can find "to
be safe." Determine which file actually governs the "available out of the
box, even before the target repo has its own scaffolding" behavior, and add
it there. Adding it to the wrong file, or to both without understanding
which one the described scenario actually depends on, does not satisfy this
task.
