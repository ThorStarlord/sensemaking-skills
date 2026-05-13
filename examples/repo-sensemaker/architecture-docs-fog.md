# Example: Architecture Docs Fog

## 1. Fog Type
Architecture Fog (Documentation/System boundary uncertainty).

## 2. Raw Idea
"Should I put the new agent routing logic in CONTEXT.md or a new ARCHITECTURE.md?"

## 3. Likely Underlying Problem
The project lacks a clear hierarchy for "Long-term System Rules" vs. "Short-term Session Context," leading to a "ball of mud" documentation structure.

## 4. Object Under Pressure
The `CONTEXT.md` file boundary and RAG discoverability rules.

## 5. Known / Unknown / Assumed
| Category | Item |
| :--- | :--- |
| **Known** | `CONTEXT.md` is currently 500 lines long. |
| **Unknown** | Will agents check multiple files or do they prefer a single source of truth? |
| **Assumed** | `ARCHITECTURE.md` is better for static, immutable rules. |

## 6. Research Paths
1. Check how Matt Pocock's skills handle system docs.
2. Review current `CONTEXT.md` for sections that haven't changed in 3 months.

## 7. Findings / Current Read
Long-term rules buried in `CONTEXT.md` are often ignored by agents when the file gets too large.

## 8. Candidate Directions
1. Extract routing logic to `docs/architecture/agent-routing.md`.
2. Keep it in `CONTEXT.md` but use a strict header structure.

## 9. Weakest Boundary
The definition of "what constitutes an architecture rule" vs. "session context."

## 10. Smallest Useful Next Step
Run `grill-with-docs` to challenge the current `CONTEXT.md` structure.

## 11. Recommended Next Skill
`grill-with-docs` (Engineering ecosystem).

## 12. Ready-to-Copy Prompt
```markdown
/grill-with-docs

I am proposing moving agent routing logic from `CONTEXT.md` to a new `docs/architecture/agent-routing.md`. 

Challenge this based on:
1. RAG performance (agent discoverability).
2. Maintenance overhead.
3. Consistency with our other documentation patterns.
```

## Expected Behavior Checklist

- [ ] Identifies the primary fog type (Architecture Fog)
- [ ] Names the "Object Under Pressure" (CONTEXT.md structure)
- [ ] Recognizes that `CONTEXT.md` is becoming a "ball of mud"
- [ ] Recommends `grill-with-docs` to align documentation intent
- [ ] Does not perform the extraction itself
