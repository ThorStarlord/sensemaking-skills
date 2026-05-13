# Example: Problem Frame (Interface Skills Run Manifest)

## 1. Raw Fog
"I think Interface Skills needs a run manifest, but I do not know what shape it should take."

## 2. Problem Under the Problem
Agents lose context about which skills ran, what inputs they used, and which reports supersede older ones. There is no deterministic way to reconstruct a session's history for validation.

## 3. Object Under Pressure
The Spec Package structure and the Agent Routing boundary.

## 4. Failure Mode
Future agents reconstruct a run using stale or conflicting report data, leading to a broken system state.

## 5. Success Condition
A machine-readable and human-readable manifest that allows any agent or validator to perfectly reconstruct the run history.

## 6. What Must Be True
- The manifest must be updated automatically at the end of every skill execution.
- It must distinguish between "current state" and "historical attempts."

## 7. Next Artifact
Unknowns Map

## Expected Behavior Checklist
- [x] Captures the "what shape should this take?" fog.
- [x] Identifies context loss as the root problem.
- [x] Names the Spec Package structure as the object under pressure.
- [x] Recommends Unknowns Map as the next artifact.
