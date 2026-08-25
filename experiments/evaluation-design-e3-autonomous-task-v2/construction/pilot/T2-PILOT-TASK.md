# T2 Pilot Task — Constrained State Transformation (disposable, instrument-calibration only)

pilot_id: T2
family: T2
disposable: true (never a main-study candidate)
repository state: frozen SHA `a7b957d738f5e1c42b6dd06824c3e6029d816bcd`, no fixture changes required beyond what the task itself asks for

## Visible task contract

Some older, hand-authored `workflow_orchestration_plan` artifacts (predating
the `chosen_workflow_id` standardization) used the field name
`target_workflow_id` instead. The routing code and the artifact contracts
need to agree that this is a legitimate, optional alias — right now neither
recognizes it.

Make `target_workflow_id` a supported alias for a workflow-orchestration
plan's chosen-workflow field:

1. Make the orchestration routing code willing to read `target_workflow_id`
   as one of the field names it accepts for this purpose, alongside the
   ones it already accepts.
2. Declare `target_workflow_id` as an **optional** (not required) machine
   field on the specific artifact contract that this field actually
   appears on — declaring it as required would break every existing plan
   artifact that doesn't have it; declaring it on the wrong artifact
   wouldn't reflect where the field actually lives.

Do not modify any other artifact contract, and do not remove, rename, or
change the requiredness of any existing machine field anywhere in the
contracts file. This repo enforces "artifacts are the API between skills"
with an automated guardrail test — your change must keep it green, and the
guardrail is necessary but not sufficient (see below).

## Non-goal

Making the automated guardrail test pass is necessary but not sufficient.
The contract should describe where the field genuinely lives, not just
satisfy the test by whatever means happens to be easiest.
