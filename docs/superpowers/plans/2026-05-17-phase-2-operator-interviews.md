# Phase 2: Operator Interviews & Discovery-Sprint Validation

> **For agentic workers:** This is a research/validation plan, not a code implementation plan. Execute tasks sequentially to conduct operator interviews and measure sensemaking effectiveness.

**Goal:** Validate that product-discovery-sprint workflows produce real value by confirming extracted domain specs match operator mental models and identifying gaps.

**Approach:** Structured interviews with 3 Metamorfose finance operators to test whether the Finance UI sensemaking brief correctly captured domain knowledge and whether recommended workflows help teams.

**Success Criteria:**
- ✅ Operators confirm sensemaking brief matches their mental models
- ✅ Identify 2-3 spec gaps that discovery-sprint should address
- ✅ Operators report research outputs would be useful for implementation teams
- ✅ Measure: Are recommendations actionable? Do they match real workflows?

---

## Phase 2 Overview

### What We're Validating

From Phase 1, the sensemaking pipeline on Finance UI identified:
- **9 unknowns** about domain workflows, data model, state management, navigation
- **Weakest boundary**: Implicit dashboard-aggregation contract
- **Recommended workflow**: product-discovery-sprint
- **Expected outcome**: Extracted domain spec that clarifies workflows and boundaries

**Question for Phase 2**: Does this recommendation actually work? Do operators find it valuable?

### Interview Strategy

1. **Select 3 operators** with different roles (finance director, UI/UX person, developer)
2. **Run 3 structured interviews** (45-60 min each) testing domain knowledge extraction
3. **Analyze findings** against sensemaking brief
4. **Measure effectiveness** (alignment, gaps, usefulness)
5. **Document results** in interview findings report
6. **Recommend** whether to proceed to Phase 3 (implementation planning)

---

## Task 1: Prepare Interview Protocol

### Target Audience

Identify 3 Metamorfose operators with domain knowledge:

**Operator 1: Finance Domain Expert**
- Role: Finance director or operations manager
- Knowledge: Business workflows, user needs, compliance constraints
- Interview focus: Validate domain boundaries and workflow understanding

**Operator 2: Product/Design**
- Role: UI/UX designer or product owner
- Knowledge: User requirements, feature priorities, navigation patterns
- Interview focus: Validate that brief captures user journey and mental models

**Operator 3: Implementation Engineer**
- Role: Backend/frontend developer who built the system
- Knowledge: Technical decisions, state management patterns, data flows
- Interview focus: Validate that spec accurately represents implementation intent

### Interview Protocol

**Duration**: 45-60 minutes per operator  
**Format**: Structured conversation with open-ended questions  
**Artifacts**: Recording/notes capturing key findings

#### Section 1: Context Setting (5 min)

"We ran a sensemaking analysis on your Finance UI to understand what makes it complex. We identified 9 unknowns and created a diagnostic brief. Today we want to validate whether our understanding matches your mental models."

**Introduce**: 
- Sensemaking brief (high-level summary)
- Recommended workflow: product-discovery-sprint
- What we're validating: Does this brief capture the real problem?

#### Section 2: Domain Workflow Validation (15 min)

**Question 1**: "What is the core workflow your finance UI is trying to enable?"

*Validation*: Compare operator's answer to "Core Workflows" section of sensemaking brief.
- Does brief correctly identify the workflow?
- Missing any major workflows?
- Any workflows described inaccurately?

**Question 2**: "What are the 3 hardest parts of using this UI today?"

*Validation*: Map operator's pain points to "Weakest Boundary" identified in brief (dashboard-aggregation contract).
- Do operators confirm the weakest boundary?
- Different pain points? What are they?

**Question 3**: "What decisions had to be made when building this UI? Which ones feel under-documented?"

*Validation*: Compare to "Missing Pieces" and "Design Decisions" sections of brief.
- Confirm which design decisions are implicit vs. explicit
- Identify any decisions we missed

#### Section 3: Data Model & State Management (15 min)

**Question 4**: "How would you explain the data model to a new engineer?"

*Validation*: Compare to data model section of sensemaking brief.
- Does brief accurately represent entities and relationships?
- Are there implicit constraints not documented?
- What would you want to document first?

**Question 5**: "What's the relationship between [X] and [Y]?" 
(Ask about 2-3 key entities from Finance domain: Projects, Transactions, Accounts, Periods)

*Validation*: Confirm cardinality and constraints match brief understanding.

#### Section 4: Spec Usefulness (10 min)

**Question 6**: "If we created a detailed spec capturing this domain knowledge, how useful would it be for new engineers?"

*Validation*: Measure perceived value of research output.
- Would it help with onboarding?
- Would it prevent bugs?
- Would it speed up feature development?

**Question 7**: "What's the one thing you wish was documented that isn't?"

*Validation*: Identify highest-priority spec gaps.
- What documentation would have the most impact?
- How urgent is this gap?

#### Section 5: Workflow Recommendations (10 min)

**Question 8**: "We recommended product-discovery-sprint as the next workflow. Does that make sense given what you see?"

*Validation*: Confirm recommended workflow is appropriate.
- Agree/disagree with discovery-sprint approach?
- What would be a better approach?
- How much time would be realistic?

**Question 9**: "After discovery-sprint produces a domain spec, how would you use it?"

*Validation*: Understand actual usage: implementation guide? Onboarding? Architecture documentation?

---

## Task 2: Conduct Interview 1 (Finance Domain Expert)

**Files:**
- Output: `artifacts/runs/2026-05-17-05-phase2-operator-interviews/01-interview-finance-expert.md`

- [ ] **Step 1: Schedule interview**

Target: Finance director or operations manager at Metamorfose  
Duration: 45-60 minutes  
Method: Video call or in-person  
Preparation: Share sensemaking brief summary 24 hours before

- [ ] **Step 2: Conduct interview**

Follow protocol above (Section 1-5)  
Record key responses and direct quotes  
Note contradictions or surprises  
Ask follow-up questions to clarify

- [ ] **Step 3: Document findings**

Create: `01-interview-finance-expert.md`

```markdown
# Interview 1: Finance Domain Expert

**Operator**: [Name, Role]  
**Date**: 2026-05-17  
**Duration**: [minutes]

## Key Findings

### Domain Workflow Validation
- Q1 (Core workflow): [Operator's answer]
- Validation: [Does this match brief? Gaps?]

### Pain Points
- Q2 (Hardest parts): [Operator's answer]
- Validation: [Confirms weakest boundary?]

### Design Decisions
- Q3 (Undocumented decisions): [Operator's answer]
- Validation: [Which are implicit vs. explicit?]

### Data Model
- Q4 (Data model explanation): [Operator's answer]
- Validation: [Matches brief?]

- Q5 (Entity relationships): [Operator's answers on key relationships]
- Validation: [Cardinality/constraints correct?]

### Spec Usefulness
- Q6 (Usefulness for new engineers): [Rating and reasoning]
- Q7 (Most important missing doc): [Operator's priority gap]

### Workflow Recommendations
- Q8 (Does discovery-sprint make sense?): [Agree/disagree and why]
- Q9 (How would you use the spec?): [Usage scenarios]

## Gaps Identified

[List any spec gaps operator mentioned]

## Surprises

[Any findings that contradicted the sensemaking brief]

## Quotes

"[Direct quote 1]"  
"[Direct quote 2]"  
"[Direct quote 3]"
```

---

## Task 3: Conduct Interview 2 (Product/Design)

**Files:**
- Output: `artifacts/runs/2026-05-17-05-phase2-operator-interviews/02-interview-product-design.md`

- [ ] **Step 1: Schedule interview**

Target: UI/UX designer or product owner at Metamorfose  
Duration: 45-60 minutes  
Method: Video call or in-person

- [ ] **Step 2: Conduct interview**

Follow protocol above, emphasizing:
- User journeys and feature priorities
- Navigation patterns and information architecture
- Feature interactions and dependencies

- [ ] **Step 3: Document findings**

Create: `02-interview-product-design.md`  
Same format as Interview 1

---

## Task 4: Conduct Interview 3 (Implementation Engineer)

**Files:**
- Output: `artifacts/runs/2026-05-17-05-phase2-operator-interviews/03-interview-implementation-engineer.md`

- [ ] **Step 1: Schedule interview**

Target: Backend or frontend developer who built Finance UI  
Duration: 45-60 minutes  
Method: Video call or in-person

- [ ] **Step 2: Conduct interview**

Follow protocol above, emphasizing:
- Technical decisions and their rationale
- State management and data flow patterns
- Technical debt and architectural constraints

- [ ] **Step 3: Document findings**

Create: `03-interview-implementation-engineer.md`  
Same format as Interview 1

---

## Task 5: Analyze Interview Findings

**Files:**
- Output: `artifacts/runs/2026-05-17-05-phase2-operator-interviews/04-interview-analysis.md`

- [ ] **Step 1: Compare findings across operators**

Create cross-operator comparison:

```markdown
| Question | Finance Expert | Product/Design | Engineer | Consensus? |
|----------|---|---|---|---|
| Q1: Core workflow | [Answer 1] | [Answer 2] | [Answer 3] | [Y/N] |
| Q2: Pain points | [Answer 1] | [Answer 2] | [Answer 3] | [Y/N] |
| ... | ... | ... | ... | ... |
```

- [ ] **Step 2: Validate sensemaking brief against findings**

| Brief Section | Operator Feedback | Match? | Gap? |
|---|---|---|---|
| Weakest boundary | [Findings] | Y/N | [Gap] |
| Data model | [Findings] | Y/N | [Gap] |
| Domain workflows | [Findings] | Y/N | [Gap] |
| Design decisions | [Findings] | Y/N | [Gap] |

- [ ] **Step 3: Identify consensus and disagreements**

Consensus findings: What all 3 operators agreed on?  
Disagreements: Where did operators differ?  
Implications: What do disagreements tell us?

- [ ] **Step 4: Compile gap list**

Priority gaps identified by operators:
1. [Gap 1] — Mentioned by [Operator(s)], Impact: [High/Medium/Low]
2. [Gap 2] — Mentioned by [Operator(s)], Impact: [High/Medium/Low]
3. [Gap 3] — Mentioned by [Operator(s)], Impact: [High/Medium/Low]

- [ ] **Step 5: Document analysis**

Create: `04-interview-analysis.md`

```markdown
# Interview Analysis: Sensemaking Brief Validation

## Consensus Findings

[What all operators agreed on]

## Disagreements & Implications

[Where operators disagreed, what it means]

## Gap Analysis

[Identified spec gaps with priority]

## Sensemaking Brief Accuracy

| Section | Accuracy | Notes |
|---|---|---|
| Weakest boundary | [High/Medium/Low] | [Details] |
| Domain workflows | [High/Medium/Low] | [Details] |
| Data model | [High/Medium/Low] | [Details] |
| Design decisions | [High/Medium/Low] | [Details] |

**Overall Brief Accuracy**: [High/Medium/Low]
- Strengths: [What brief got right]
- Weaknesses: [What brief missed]

## Recommended Prioritization for Discovery-Sprint

Based on operator feedback, prioritize discovery in this order:
1. [Topic 1] — [Why operators emphasized this]
2. [Topic 2] — [Why operators emphasized this]
3. [Topic 3] — [Why operators emphasized this]

## Operator Satisfaction

- Would new engineers find this spec useful? [Operator feedback and rating]
- Would it help with onboarding? [Feedback]
- Would it prevent bugs? [Feedback]
- Overall usefulness rating: [1-5 scale with reasoning]
```

---

## Task 6: Measure Sensemaking Effectiveness

**Files:**
- Output: `artifacts/runs/2026-05-17-05-phase2-operator-interviews/05-effectiveness-measurement.md`

- [ ] **Step 1: Compare brief to operator mental models**

Metric: **Brief Accuracy Score**

```
Accuracy = (Accurate sections / Total sections) × 100%

Example:
- Weakest boundary: ✅ Correct
- Domain workflows: ✅ Correct
- Data model: ⚠️ Partially correct (missing constraints)
- Design decisions: ❌ Missed 3 key decisions
- Navigation: ⚠️ Partially correct

Accuracy = (2 + 0.5 + 0.5) / 5 = 60%
```

- [ ] **Step 2: Measure recommendation usefulness**

Metric: **Workflow Recommendation Score**

Questions:
- Do operators agree discovery-sprint is the right next step? (Y/N)
- Would produced spec be useful? (1-5 scale)
- How much time is realistic? (hours/days)
- Priority urgency? (high/medium/low)

Score = (Agreement + Usefulness + Realism) / 3

- [ ] **Step 3: Identify actionable gaps**

Metric: **Spec Gap Impact Score**

For each identified gap:
- Impact if unfixed: High/Medium/Low
- Ease of fixing: High/Medium/Low  
- Operator priority: 1-5 scale

Priority = Impact × (1 - Ease) × OperatorRating

Gaps sorted by priority

- [ ] **Step 4: Create effectiveness report**

Create: `05-effectiveness-measurement.md`

```markdown
# Sensemaking Effectiveness Measurement

## Brief Accuracy Score

**Overall Accuracy**: [60%/70%/80%/90%+]

By section:
- Weakest boundary: [Correct/Partially/Incorrect]
- Domain workflows: [Correct/Partially/Incorrect]
- Data model: [Correct/Partially/Incorrect]
- Design decisions: [Correct/Partially/Incorrect]
- [Other sections]: [Status]

**Interpretation**: [What does this score mean for Phase 3?]

## Workflow Recommendation Usefulness

**Discovery-sprint recommendation score**: [1-5]
- Do operators agree it's the right next step? [Y/N]
- Would produced spec be useful? [Rating + reasoning]
- Realistic timeline? [Hours/days]

## Actionable Gaps

| Gap | Impact | Ease | Priority | Note |
|---|---|---|---|---|
| [Gap 1] | High | Easy | 1 | Operators emphasized this |
| [Gap 2] | High | Hard | 2 | Important but complex |
| [Gap 3] | Medium | Easy | 3 | Nice-to-have |

## Confidence for Phase 3

**Ready to proceed?** [GO / CAUTION / NO-GO]

- Brief accuracy: [Good/Adequate/Poor] foundation for Phase 3
- Operators' confidence: [High/Medium/Low] that recommendations will help
- Gaps manageable? [Y/N] Can discovery-sprint address them?

## Next Steps

If GO:
1. Use interview feedback to refine domain spec
2. Design discovery-sprint with prioritized topics
3. Proceed to Phase 3 (implementation planning with refined spec)

If CAUTION:
1. Run additional mini-interviews on specific topics
2. Refine brief based on gaps
3. Re-validate with subset of operators
4. Then proceed to Phase 3

If NO-GO:
1. Document why sensemaking approach isn't working
2. Recommend alternative validation strategy
3. Consider whether Phase 2 revealed fundamental approach issues
```

---

## Task 7: Create Phase 2 Final Report

**Files:**
- Output: `artifacts/runs/2026-05-17-05-phase2-operator-interviews/README.md`

- [ ] **Step 1: Synthesize all findings**

Create executive summary of:
- What operators confirmed about sensemaking brief
- What gaps they identified
- What they want documented first
- Whether they think recommended workflow is right

- [ ] **Step 2: Document overall conclusions**

Create: `artifacts/runs/2026-05-17-05-phase2-operator-interviews/README.md`

```markdown
# Phase 2: Operator Interviews Complete

**Date**: 2026-05-17  
**Operators Interviewed**: 3 (Finance Expert, Product/Design, Engineer)  
**Duration**: ~3 hours total  
**Recommendation**: [GO / CAUTION / NO-GO for Phase 3]

## Executive Summary

[One paragraph summarizing findings and confidence level]

## Brief Validation Results

- **Overall Accuracy**: [X%]
- **Strongest findings**: [What brief got right]
- **Gaps identified**: [Number and type]
- **Operator confidence**: [High/Medium/Low] in recommendations

## Key Discoveries

1. [Discovery 1 with operator quotes]
2. [Discovery 2 with operator quotes]
3. [Discovery 3 with operator quotes]

## Recommended Next Steps

### If GO for Phase 3:
1. Refine domain spec using interview feedback
2. Design 2-3 day discovery-sprint with prioritized topics
3. Plan implementation team handoff
4. Proceed to Phase 3 (implementation planning)

### If CAUTION:
1. [Specific refinements needed]
2. Schedule follow-up validation
3. Re-validate before proceeding

### If NO-GO:
1. Document why this approach didn't work
2. Recommend alternative validation strategy

## Artifacts

- `01-interview-finance-expert.md` — Domain expert interview notes
- `02-interview-product-design.md` — Product/design operator interview
- `03-interview-implementation-engineer.md` — Implementation engineer interview
- `04-interview-analysis.md` — Cross-operator analysis and gap synthesis
- `05-effectiveness-measurement.md` — Sensemaking effectiveness metrics

## Lessons Learned

[What Phase 2 revealed about sensemaking approach]
```

- [ ] **Step 2: Commit Phase 2 artifacts**

```bash
git add artifacts/runs/2026-05-17-05-phase2-operator-interviews/
git commit -m "docs: complete Phase 2 operator interviews and validation

Conducted 3 structured interviews validating sensemaking brief against:
- Finance domain expert (workflows, pain points, business logic)
- Product/design operator (user journeys, feature priorities)
- Implementation engineer (technical decisions, state management)

Results: [Brief accuracy X%, Y gaps identified, Z% operator confidence]
Recommendation: [GO/CAUTION/NO-GO for Phase 3]

Interview findings, analysis, and effectiveness metrics documented."
git push origin main
```

---

## Success Criteria

- [ ] ✅ 3 operators interviewed (Finance Expert, Product/Design, Engineer)
- [ ] ✅ Interview findings documented with direct quotes
- [ ] ✅ Sensemaking brief validated against operator mental models
- [ ] ✅ Gaps identified and prioritized
- [ ] ✅ Effectiveness metrics calculated
- [ ] ✅ Clear GO/CAUTION/NO-GO recommendation for Phase 3
- [ ] ✅ All artifacts committed to main branch

---

## Timeline

| Task | Duration | Status |
|------|----------|--------|
| Task 1: Prepare protocol | 2-3 hrs | ⏳ Pending |
| Task 2: Interview 1 (Domain) | 1-2 hrs | ⏳ Pending |
| Task 3: Interview 2 (Product) | 1-2 hrs | ⏳ Pending |
| Task 4: Interview 3 (Engineer) | 1-2 hrs | ⏳ Pending |
| Task 5: Analysis | 2-3 hrs | ⏳ Pending |
| Task 6: Effectiveness measurement | 1-2 hrs | ⏳ Pending |
| Task 7: Final report | 1-2 hrs | ⏳ Pending |
| **Total** | **~9-16 hours** | **⏳ Ready to start** |

---

## Notes

- **Operator Availability**: Phase 2 requires access to actual Metamorfose finance operators. If unavailable, can proceed with simulated interviews (using domain knowledge from Phase 1 artifacts to generate likely operator responses).
- **Interview Quality**: Structured protocol ensures consistency across interviews while allowing for follow-up questions and deep exploration.
- **Measurement Focus**: Effectiveness metrics tie back to Phase 1 heuristic validation — confirming sensemaking pipeline produces value in real-world settings.
- **Phase 3 Gate**: GO/CAUTION/NO-GO recommendation determines whether to proceed to implementation planning with confidence that sensemaking approach is working.
