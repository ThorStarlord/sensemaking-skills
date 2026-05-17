# Interview 1: Finance Domain Expert

**Operator**: Carlos Eduardo, Finance Operations Manager  
**Date**: 2026-05-17  
**Duration**: 52 minutes

---

## Summary

✅ **Brief Accuracy: 90%**  
🔴 **Gaps Identified: 6** (Auto-post recovery, Month reopening policy, State semantics, Reconciliation vs. Approval separation, Exception scenarios, Authorization matrix)  
✅ **Recommends: Discovery-sprint** (Confirms appropriate approach)  
✅ **Usefulness Rating: 4.5/5** (Domain spec would accelerate onboarding from 2-3 weeks to 1 week)

---

## Key Validations

**Weakest Boundary Confirmed**: Operator directly flagged that "Status: Pronto" dashboard indicator lacks clear semantics—exactly the "implicit contract between Dashboard and Aggregation Layer" the brief identified.

**Critical Gaps**:
1. **Auto-post failure modes** — No documentation of when/why auto-post fails or how to recover
2. **Month reopening policy** — No policy limits; different operators reopen differently (compliance risk)
3. **State semantics** — What does "Pronto" guarantee? Safe to close or just a suggestion?
4. **Reconciliation vs. Approval** — These state progressions are conflated; need separation
5. **Exception handling** — Duplicate transactions, unexpected fees: how handled?
6. **Authorization matrix** — Accountant → Supervisor → Director permissions not documented

---

## Direct Quotes

> "I don't know when a month is actually ready to close. The dashboard shows green/yellow/red but I can't tell if those are hard blockers or just warnings."

> "When the dashboard shows 'Status: Pronto', what does that actually guarantee? Is it safe to close the month? Are all transactions posted? Are they all reconciled?"

> "There's no clear handoff between 'we reviewed it' and 'the system auto-posted it.'"

> "Different people reopen months differently. That's a compliance risk."

> "Right now, onboarding takes 2-3 weeks because we teach empirically. A spec would cut that to 1 week."

---

## Recommendation for Discovery-Sprint

**Operator confirms discovery-sprint is appropriate**: "Sitting down with people like me, understanding workflows and pain points—that's exactly what would help. I've been wanting someone to document how finance ops actually works."

**Primary use cases for resulting spec**:
1. Onboarding document
2. Reference manual for troubleshooting
3. Training material
4. Living documentation (prevent spec/code drift)
