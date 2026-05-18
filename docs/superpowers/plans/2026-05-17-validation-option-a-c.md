# Validation Option A + C: Heuristic Robustness & Edge Cases

> **For agentic workers:** Use superpowers:subagent-driven-development to execute this plan task-by-task.

**Goal:** Validate that the dynamic chaining routing heuristic (`research_needed = (unknowns_count >= 5) OR (clarity_assessment == "low")`) works across diverse systems and find any failure modes.

**Architecture:** Parallel execution of two validation streams:
- **Option A**: Run full sensemaking pipeline on 2-3 additional Metamorfose systems (different complexity levels)
- **Option C**: Test edge cases (ultra-simple systems, validate unknowns_count threshold behavior)

**Tech Stack:** sensemaking-skills (problem-framer, unknowns-mapper, repo-sensemaker), metamorfose-edutech (target systems)

---

## System Selection

### Option A: Heuristic Robustness (Full Pipeline Runs)

| System | Size | Problem Type | Expected Unknowns | Test Goal |
|--------|------|--------------|-------------------|-----------|
| **guardians** | 365 lines | User management | ~4-6 | Validate threshold behavior |
| **pedagogico** | 12 lines | Content/curriculum | ~1-3 | Test simple system (expect research_needed=false) |

### Option C: Edge Cases (Targeted Tests)

| System | Size | Problem Type | Test Goal |
|--------|------|--------------|-----------|
| **comunicacao** | 7 lines | Messaging (ultra-simple) | Find lower boundary of unknowns_count |
| **pedagogico** | 12 lines | Content system (very simple) | Validate clarity_assessment on minimal systems |

---

## Task 1: Analyze Guardians System (Option A, Full Pipeline)

**Files:**
- Read: `metamorfose-platform/app/admin/guardians/page.tsx`
- Output: `artifacts/2026-05-17-03-metamorfose-guardians/` (numbered 01-05)

- [ ] **Step 1: Problem-framer on guardians system**

Run: `problem-framer <metamorfose-platform root>`  
Focus: What is the guardians system trying to solve? What's unclear?  
Expected output: 01-problem-frame.md

- [ ] **Step 2: Unknowns-mapper on guardians system**

Run: `unknowns-mapper <path-to-artifacts/01-problem-frame.md>`  
Focus: Map uncertainties, generate routing signals  
Expected: unknowns_count estimate and clarity_assessment  
Output: 02-unknowns-map.md

- [ ] **Step 3: Evaluate routing signal**

Check: Does unknowns_count match expected ~4-6?  
Check: Does clarity_assessment align with system simplicity?  
Expected: research_needed = true (unknowns >= 5) OR false (unknowns < 5, high clarity)

- [ ] **Step 4: Run repo-sensemaker (if research_needed=true)**

If research_needed triggered: Execute repo-sensemaker  
Output: 03-sensemaking-brief.md

- [ ] **Step 5: Create run analysis**

Output: 04-run-analysis.md  
Document: Routing signal validation, patterns observed, comparison to Finance/Classes

- [ ] **Step 6: Commit guardians run**

Move artifacts to `runs/2026-05-17-03-metamorfose-guardians/`  
Commit to main

---

## Task 2: Analyze Pedagogico System (Option A, Full Pipeline)

**Files:**
- Read: `metamorfose-platform/app/admin/pedagogico/page.tsx`
- Output: `artifacts/2026-05-17-04-metamorfose-pedagogico/`

- [ ] **Step 1: Problem-framer on pedagogico system**

Run: `problem-framer <metamorfose-platform root>`  
Focus: What does pedagogico do? How clear is its purpose?  
Output: 01-problem-frame.md

- [ ] **Step 2: Unknowns-mapper on pedagogico system**

Run: `unknowns-mapper <path-to-01-problem-frame.md>`  
Expected: unknowns_count ~1-3 (very simple system)  
Output: 02-unknowns-map.md

- [ ] **Step 3: Evaluate routing signal**

Check: Does unknowns_count < 5?  
Check: Is clarity_assessment = "high"?  
Expected: research_needed = false (both conditions suggest no research needed)

- [ ] **Step 4: Document baseline**

If research_needed = false: Create 03-baseline-analysis.md  
Document: What makes this system clear and simple  
Why unknowns_count stayed below threshold

- [ ] **Step 5: Commit pedagogico run**

Move artifacts to `runs/2026-05-17-04-metamorfose-pedagogico/`  
Commit to main

---

## Task 3: Edge Case - Comunicacao System (Option C, Ultra-Simple)

**Files:**
- Read: `metamorfose-platform/app/admin/comunicacao/page.tsx`
- Output: Direct inline analysis (no full pipeline, just assessment)

- [ ] **Step 1: Quick assessment of comunicacao**

Read the file (7 lines)  
Estimate: How many unknowns would a human identify?  
Question: Is this system so simple that unknowns_count rounds to 0?

- [ ] **Step 2: Run unknowns-mapper (minimal)**

Focus: Attempt to map uncertainties in 7-line system  
Observe: What happens when you try to identify unknowns in ultra-minimal code?  
Output: Edge-case-comunicacao-analysis.md

- [ ] **Step 3: Document findings**

Output: 05-edge-case-analysis.md  
Question: Did unknowns_count=0 cause routing to fail or skip research?  
Finding: Is the heuristic robust to minimal systems?

- [ ] **Step 4: Add to meta-analyses**

Create: `meta-analyses/03-option-a-c-validation-report.md`  
Document: Findings from all 3+ runs, threshold validation

---

## Task 4: Edge Case - Pedagogico System (Option C, Very Simple)

**Files:**
- Read: `metamorfose-platform/app/admin/pedagogico/page.tsx`
- Output: Already analyzed in Task 2, reuse data

- [ ] **Step 1: Use pedagogico data from Task 2**

unknowns_count from Task 2: ~1-3  
clarity_assessment from Task 2: "high"

- [ ] **Step 2: Analyze clarity_assessment edge case**

Question: With unknowns_count < 5 AND clarity="high", should research_needed=false?  
Validation: Does our heuristic correctly identify this as "no research needed"?

- [ ] **Step 3: Document edge case outcome**

Add to meta-analyses report: Pedagogico behavior at threshold

---

## Task 5: Consolidate Findings (Meta-Analysis)

**Files:**
- Create: `meta-analyses/03-option-a-c-validation-report.md`

- [ ] **Step 1: Compare all 4 runs**

| System | Unknowns | Clarity | Research Needed | Problem Type |
|--------|----------|---------|-----------------|--------------|
| Finance | 9 | medium | true | Complex |
| Classes | 8 | high | true | Simple (hidden knowledge) |
| Guardians | ? | ? | ? | Medium |
| Pedagogico | ~1-3 | high | false | Ultra-simple |

- [ ] **Step 2: Validate heuristic**

Did unknowns_count >= 5 threshold work consistently?  
Did clarity_assessment distinguish problem types?  
Any edge cases or surprises?

- [ ] **Step 3: Identify patterns**

Pattern 1: How does unknowns_count correlate with actual complexity?  
Pattern 2: Does clarity_assessment predict research_needed?  
Pattern 3: Any failure modes found in edge cases?

- [ ] **Step 4: Recommend next steps**

Based on findings: Should heuristic be adjusted?  
Based on failures: Where does system need hardening?  
Recommendation: Ready for Option B (real operator interviews)?

---

## Success Criteria

**Option A (Heuristic Robustness):**
- ✅ Guardians run completes with valid unknowns_count and routing signal
- ✅ Pedagogico run confirms simple systems stay below threshold (research_needed=false)
- ✅ Unknowns_count >= 5 threshold validated across 4 systems (Finance, Classes, Guardians, +1)

**Option C (Edge Cases):**
- ✅ Comunicacao (7-line system) processed without errors
- ✅ Edge case analysis documents behavior at unknowns_count extremes
- ✅ No critical bugs found in minimal systems

**Consolidated Finding:**
- ✅ Heuristic is robust OR requires adjustment (documented)
- ✅ Ready for Option B (operator interviews) OR needs refinement

---

## Execution Timeline

- **Day 1**: Option A runs (Guardians + Pedagogico full pipeline) — 2-3 hours
- **Day 1-2**: Option C edge case testing — 1 hour  
- **Day 2**: Meta-analysis consolidation — 1 hour
- **Total**: 4-5 hours over 2 days

---

## Artifact Numbering

New runs will follow established pattern:

```
artifacts/
├── runs/
│   ├── 2026-05-17-03-metamorfose-guardians/
│   │   ├── 01-problem-frame.md
│   │   ├── 02-unknowns-map.md
│   │   ├── 03-sensemaking-brief.md
│   │   └── 04-run-analysis.md
│   ├── 2026-05-17-04-metamorfose-pedagogico/
│   │   ├── 01-problem-frame.md
│   │   ├── 02-unknowns-map.md
│   │   └── 03-baseline-analysis.md
│
├── meta-analyses/
│   ├── 01-comparative-routing-analysis.md
│   ├── 02-next-phase-decision-framework.md
│   └── 03-option-a-c-validation-report.md
```
