# Architectural Review Recommendation — Template

Use this template when the architectural-review skill executes. Replace all bracketed sections with analysis results.

---

## Summary

[One-paragraph summary of the architectural recommendation and its key reasoning]

---

## Analysis

### Proposed Response Alignment

[How does the proposed response address the identified fog? Map each proposal component to specific fog classifications or evidence from the brief.]

### Risk Identification

[Enumerate specific, testable risks. Format: "Risk: [description] — Impact: [concrete consequence]"]

**Authority boundary risks**: [Does the proposal create competing authorities or orchestration layers?]

**Performance bottleneck risks**: [Does the proposal introduce new bottlenecks or relocate existing ones?]

**User experience risks**: [Does the proposal create indirection or coupling that affects UX?]

**Technical debt risks**: [Does the proposal defer or amplify technical debt?]

---

## Recommendation

### Decision

[One of: pursue | pursue_narrowed | investigate_first | defer | reject]

### Reasoning

[Detailed justification for the decision, including how risks were weighed and what constraints apply]

### Success Measures (if pursue)

[Required only for pursue decisions]

- **Metric**: [What will be measured]
- **Baseline**: [Current state]
- **Target**: [Desired outcome]
- **Measurement Method**: [How measurement will be performed]

### Reversal Conditions (if defer/reject)

[When would this decision change? Specific, testable conditions.]

### Investigation Steps (if investigate_first)

[What additional investigation is needed? Format as actionable steps.]

### Narrowed Scope (if pursue_narrowed)

- **Approved scope**: [Explicitly approved aspects]
- **Excluded scope**: [Explicitly excluded aspects]
- **Constraints**: [Conditions that must hold for approval]

---

## Machine-readable Decision

```yaml
artifact_id: architectural_review_recommendation
decision: [pursue | pursue_narrowed | investigate_first | defer | reject]
confidence: [high | medium | low]
risks_identified:
  - "Risk 1: description"
  - "Risk 2: description"
success_measures:
  metric: "[if pursue: what metric]"
  baseline_status: "[if pursue: current value]"
  target: "[if pursue: target value]"
  measurement_method: "[if pursue: how to measure]"
created_at: "[ISO timestamp]"
created_by: "[skill name or agent identifier]"
```

---

## Notes

[Any additional context or caveats about this recommendation]
