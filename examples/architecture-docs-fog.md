# Example: Architecture Docs Fog

## 1. Raw Idea
"Should I put the new agent routing logic in CONTEXT.md or a new ARCHITECTURE.md?"

## 2. Likely Underlying Problem
The project lacks a clear hierarchy for "Long-term System Rules" vs. "Short-term Session Context."

## 3. Subject Map
- Documentation Architecture
- Information Retrieval (RAG) efficiency
- Developer Onboarding

## 4. Known / Unknown / Assumed
| Category | Item |
| :--- | :--- |
| **Known** | `CONTEXT.md` is currently 500 lines long. |
| **Unknown** | Will agents check multiple files or do they prefer a single source of truth? |
| **Assumed** | `ARCHITECTURE.md` is better for static, immutable rules. |

## 5. Research Paths
1. Check how Matt Pocock's skills handle system docs.
2. Review current `CONTEXT.md` for sections that haven't changed in 3 months.

## 6. Findings
Long-term rules buried in `CONTEXT.md` are often ignored by agents when the file gets too large.

## 7. Candidate Directions
1. Extract routing logic to `docs/architecture/agent-routing.md`.
2. Keep it in `CONTEXT.md` but use a strict header structure.

## 8. Weakest Boundary
The definition of "what constitutes an architecture rule."

## 9. Smallest Useful Next Step
Run `grill-with-docs` to challenge the current `CONTEXT.md` structure.

## 10. Next Skill Prompt
/grill-with-docs

I am proposing moving agent routing logic from `CONTEXT.md` to a new `docs/architecture/agent-routing.md`. 

Challenge this based on:
1. RAG performance (agent discoverability).
2. Maintenance overhead.
3. Consistency with our other documentation patterns.
