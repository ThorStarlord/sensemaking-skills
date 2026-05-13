# Example: Premature PRD Routing (Negative Fixture)

## 1. Fog Type
Product Fog / Strategy Fog (Deep uncertainty).

## 2. Raw Idea
"I want to build an AI assistant for my school, maybe with WhatsApp, maybe a web app, maybe something with games. I need a PRD now."

## 3. Likely Underlying Problem
The user is attempting to solve for the "how" before defining the "who," "why," or "what." This is a high-risk scenario for premature implementation.

## 4. Object Under Pressure
The Solution Architecture and User Value Proposition.

## 5. Known / Unknown / Assumed
| Category | Item |
| :--- | :--- |
| **Known** | The target audience is a school. |
| **Unknown** | What specific problem is being solved? (Admin? Pedagogy? Student communication?) |
| **Unknown** | What is the technical literacy of the users? |
| **Assumed** | An AI assistant is the correct solution. |

## 6. Research Paths
1. Interview stakeholders at the school to identify the most painful workflow.
2. Evaluate technical constraints (WhatsApp vs. Web App accessibility).

## 7. Findings / Current Read
No research performed yet. Unknowns are too fundamental to choose a downstream routing path.

## 8. Candidate Directions
1. Perform discovery to narrow the problem space.
2. Grill the idea to challenge the "AI Assistant" assumption.

## 9. Weakest Boundary
The link between the "AI Technology" and a "Verified User Need."

## 10. Smallest Useful Next Step
Do NOT route to PRD. Use `/grill-me` to challenge assumptions and clarify the core problem.

## 11. Recommended Next Skill
`grill-me` (Engineering/Product ecosystem).

## 12. Ready-to-Copy Prompt
```markdown
/grill-me

I want to build an AI assistant for a school but I'm unsure about the platform (WhatsApp vs. Web) or the primary function.

Challenge my assumptions:
1. Why is an "AI Assistant" the right tool for a school?
2. What specific school pain point am I solving?
3. Who is the primary user (teacher, student, parent, admin)?
```

## Expected Behavior Checklist

- [ ] Identifies the primary fog type (Product/Strategy Fog)
- [ ] Correctly identifies that unknowns are too fundamental to route to a solution (e.g., PRD)
- [ ] Recommends a discovery/grilling path instead of an implementation path
- [ ] Adheres to the "Confidence Rule": refuses to route downstream until assumptions are named
