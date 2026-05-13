# Example: Interface Skills Run Manifest

## 1. Raw Idea
"I think Interface Skills needs a run manifest, but I do not know what shape it should take."

## 2. Likely Underlying Problem
Agents lose context about which skills ran, what inputs they used, what artifacts changed, and which reports supersede older reports.

## 3. Subject Map
- Spec Package Architecture
- Report Lifecycle
- Agent Routing
- Validator Design
- Fixture Stability

## 4. Known / Unknown / Assumed
| Category | Item |
| :--- | :--- |
| **Known** | We have `00-index.md`. We have `reports/`. |
| **Unknown** | Should the manifest be human-readable, machine-readable, or both? |
| **Assumed** | Future agents will need to reconstruct a run to avoid stale data. |

## 5. Research Paths
1. What information do future agents need to reconstruct a run?
2. Does this overlap with `00-index.md`?
3. What can a validator enforce deterministically?

## 6. Findings
Research suggests that a machine-readable format (YAML/JSON) is better for validators, but a Markdown summary is better for human review.

## 7. Candidate Directions
1. Add `RUN-MANIFEST.md` for human readability.
2. Add a "Run History" section to `00-index.md`.
3. Add a machine-readable `run-manifest.yaml`.

## 8. Weakest Boundary
The transition between an agent finishing a run and a human approving the report.

## 9. Smallest Useful Next Step
Prototype three formats for comparison.

## 10. Next Skill Prompt
/prototype

Prototype three run manifest formats for Interface Skills:
1. `RUN-MANIFEST.md`
2. Run History section inside `00-index.md`
3. machine-readable `run-manifest.yaml`


## Expected Behavior Checklist

- [ ] Identifies the primary fog type (Architecture Fog)
- [ ] Names the "Object Under Pressure" (Spec Package / Run Manifest)
- [ ] Identifies the "Weakest Boundary" (Agent completion vs Human approval)
- [ ] Recommends `/prototype` to compare options
- [ ] Does not create the manifest or build the validator
