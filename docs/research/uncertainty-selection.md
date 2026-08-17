# Research: Selecting Decision-Changing Uncertainty

**Status:** research hypothesis / product-design study  
**Authority:** not an ADR, not a product contract, not a Workflow-v0 change  
**Current application domain:** agentic software engineering / repository-centered engineering  
**Research question:**

> **How should a Sensemaking agent select which unresolved uncertainty to resolve before acting, and when should it stop investigating and act despite residual uncertainty?**

This document deepens the current operating rule:

> **Resolve the nearest unresolved decision-changing uncertainty before committing to the eventual solution.**

It does not replace that rule. It proposes a qualitative interpretation to test through normal engineering work.

---

## 1. Current research conclusion

A useful first answer is:

> **Resolve an uncertainty before acting when the current contemplated decision materially depends on it, a credible alternative answer could change a consequential decision, and the expected downside of acting while wrong is large enough to justify the cost or delay of obtaining evidence. Prefer the earliest such unresolved dependency in the warrant for the contemplated action.**

And stop investigating when:

> **No remaining credible uncertainty is likely to change the warranted responsibility, scope, authority path, stop/continue decision, or closure claim enough to justify the cost or delay of resolving it before action.**

This is deliberately qualitative. It is not a numeric scoring model.

The key product-design distinction is:

```text
uncertainty reduction != decision value
```

An investigation is not valuable merely because it reduces uncertainty. Its value comes from how the resulting evidence could improve the next consequential decision.

---

## 2. What counts as a consequential decision?

For Sensemaking, "decision-changing" should not mean only "changes responsibility class."

Evidence is decision-changing when a credible alternative result could materially change one or more of:

- **responsibility** -- investigate, repair, retire, reconcile, verify, ask owner, stop;
- **scope** -- which component, boundary, artifact, or finding is actually in scope;
- **authority** -- whether the agent may decide, act, publish, merge, or must escalate;
- **continuation** -- whether to keep investigating, perform bounded work, stop, or hand off;
- **closure** -- whether available evidence supports a material claim or finding-specific closure.

Evidence that only changes an implementation detail can still matter, but it normally has lower control priority once the higher-order decision is stable.

---

## 3. Operational meaning of "nearest"

"Nearest" should not mean:

- first uncertainty noticed;
- smallest file distance;
- easiest question;
- uncertainty most related to the requested final implementation;
- uncertainty with the largest amount of missing information.

A better candidate meaning is:

> **The closest unresolved dependency in the warrant for the currently contemplated consequential action.**

Example:

```text
goal: fix validator behavior

candidate action: patch validator

warrant dependencies:
1. this validator is still a supported responsibility
2. this repository owns the responsibility
3. the observed behavior is a live defect rather than retirement residue
4. a local patch is the appropriate repair
5. implementation detail X is correct
```

If dependency 1 or 2 is unresolved, implementation-detail uncertainty at dependency 5 is downstream. Resolve the earlier dependency first when it could invalidate the entire action.

This gives "nearest" a structural meaning: **earliest unresolved premise capable of invalidating or materially redirecting the current warrant.**

---

## 4. Empirical cases from normal engineering work

### Case A -- Auteur issue #63: apparent fixture bug became responsibility retirement

Initial issue framing:

```text
validate-project-classification.py cannot be tested per-fixture
-> classify as repo-wide or add --test-projects-dir
```

The investigation identified a more consequential uncertainty:

> **Does this legacy project-classification responsibility still belong in Auteur's supported vendored Sensemaking surface?**

Repository/provenance evidence showed that:

- the validator's executable contract did not match the harness;
- the required `test-projects/` corpus was absent;
- the validator was part of a curated vendored subset whose next update required a canonical upstream comparison baseline;
- current upstream Sensemaking no longer contained the validator.

Resolving that uncertainty changed the warranted action from a local validator patch to coherent retirement of the unsupported responsibility.

Observed lesson:

> **Ownership/support/provenance uncertainty had higher decision value than implementation-form uncertainty because it could invalidate the repair responsibility itself.**

### Case B -- Auteur issue #62: apparent exit-code bug became ownership retirement

Initial issue framing:

```text
validate-workflow-design.py exits 0 when registry loading fails
-> return a non-zero exit and stable error code
```

The investigation asked instead:

> **Should Auteur still own this validator at all?**

Evidence showed that:

- the false-green behavior was real;
- the only fixture was a placeholder and did not exercise meaningful workflow validation;
- upstream had explicitly removed the validator as dead code because `validate-repo.py` covered its live checks;
- Auteur retained `validate-repo.py`, which still verified the supported workflow compatibility surface;
- no live consumer remained beyond harness/fixture/inventory references.

Resolving that uncertainty changed the warranted action from hardening a local error-code contract to retiring the obsolete validator responsibility.

Observed lesson:

> **A defect can be real while repairing the defective component is still unwarranted.**

### Case C -- Sensemaking PR #177: seven red CI jobs became migration/authority reconciliation

Initial visible problem:

```text
canonical CI has seven failing jobs
-> fix the failing tests/jobs
```

The governing uncertainties were instead:

- were the missing test files accidentally deleted, renamed, or intentionally retired?
- did canonical vocabulary lag live contracts, or should live contracts be removed?
- was a probe blocker a genuine missing local ADR or an external-provenance ambiguity?

Evidence showed three clusters of migration/authority drift rather than seven independent defects. The repair removed stale executor-era CI references, reconciled canonical vocabulary to already-live contracts, and clarified external provenance. Surviving current-runtime protections remained load-bearing and the full 18-job matrix passed.

Observed lessons:

1. **Visible failures are not necessarily independent responsibilities.**
2. **The first repair can reveal the next uncertainty; selection is recursive.**
3. **Do not restore retired machinery merely because a stale verifier still names it.**
4. **Stopping was warranted only after the current-runtime contract, not every historical artifact, was mechanically green.**

---

## 5. Relevant external theory

This research is informed by, but should not be subordinated to, formal decision theory.

### Rational metareasoning / value of computation

Russell and Wefald's rational-metareasoning line treats internal computation as an action with cost whose benefit is improved external decision quality. Later work on selecting computations formalizes the question "which computation should be performed next?" in terms of expected improvement to the eventual decision.

Product implication:

> **Investigation is instrumentally valuable through its effect on the engineering decision, not because more reasoning is inherently better.**

### Decision value versus information gain

Recent computation-allocation work makes an especially useful distinction: information gain and decision value coincide only under particular loss functions. For action-selection/simple-regret problems, maximizing information gain can rank computations badly because information can be abundant yet irrelevant to the terminal decision.

Product implication:

> **Sensemaking should not maximize uncertainty reduction, novelty, repository coverage, or information gain as a proxy for good control. It should prioritize decision-relevant evidence.**

### Stopping as part of the same control problem

Metareasoning models include an explicit stop action: continue computation while some available computation has enough expected value to justify its cost; otherwise act.

Product implication:

> **Selecting what to investigate and deciding when investigation should give way to action are one product-design problem, not two unrelated mechanisms.**

### Irreversibility and option value

Work on irreversible decisions under uncertainty shows that waiting for information can have value when acting commits state and future information may alter the decision.

Product implication, used cautiously by analogy:

> **The evidence threshold should generally rise with consequence, propagation, and irreversibility. Cheap reversible or information-producing actions can tolerate more residual uncertainty than consequential state-changing or publication actions.**

---

## 6. Candidate qualitative selection policy

At a decision point, the active agent should first name the **contemplated consequential decision** rather than enumerate every unknown in the repository.

Then use the following sequence.

### Step 1 -- State the provisional next decision

Examples:

- repair this component;
- retire this responsibility;
- reconcile docs and implementation;
- ask the owner;
- run an empirical probe;
- publish / merge;
- claim closure;
- stop.

If no provisional decision exists yet, the immediate responsibility may simply be orientation / repository sensemaking.

### Step 2 -- Identify the warrant dependencies

Ask:

> **What must be true for this decision to be warranted?**

Keep this bounded. Prefer the few premises whose failure would materially redirect the next action.

### Step 3 -- Mark credible unresolved dependencies

An uncertainty is a candidate blocker when:

1. the contemplated decision depends on it; and
2. there is a credible alternative answer given current evidence; and
3. that alternative could materially change responsibility, scope, authority, continuation, or closure.

Do not elevate merely interesting unknowns into blockers.

### Step 4 -- Compare candidate uncertainties qualitatively

Use these dimensions as reasoning prompts, not scores.

| Dimension | Question | Higher priority when... |
|---|---|---|
| **Dependency proximity** | How early is this uncertainty in the warrant chain? | a contrary answer invalidates downstream work |
| **Decision branching** | What could change if the answer differs? | responsibility/scope/authority/stop state changes |
| **Alternative plausibility** | Is the contrary answer credible from current evidence? | repository/history/probes give it real support |
| **Wrong-action exposure** | What happens if we act under the wrong assumption? | action is costly, propagating, externally visible, hard to reverse, or creates false closure |
| **Evidence economy** | How cheaply and reliably can this be resolved? | authoritative evidence is accessible at low cost/delay |
| **Option preservation** | Can we act safely while keeping alternatives open? | low reversibility raises priority; reversible action lowers it |

A common high-priority pattern is:

```text
high dependency proximity
+ high decision branching
+ credible alternative
+ high wrong-action exposure
+ cheap authoritative evidence
        -> resolve before acting
```

A common low-priority pattern is:

```text
low decision branching
+ weakly plausible alternative
+ reversible bounded action
+ expensive investigation
        -> preserve residual uncertainty and act
```

### Step 5 -- Select the evidence-producing responsibility

Once the uncertainty is selected, choose the responsibility that can resolve it from the right source:

```text
repository evidence    -> inspect
empirical reality      -> probe
owner intent            -> ask owner
external environment    -> inspect externally if authorized
```

Then choose a Skill/tool only after the responsibility is clear.

### Step 6 -- Reassess after evidence

The result may:

- confirm the provisional decision;
- change its scope;
- change the responsibility class;
- expose a new nearer uncertainty;
- reveal an authority boundary;
- make action unnecessary;
- warrant action;
- warrant stopping.

The loop is therefore recursive, not a one-time uncertainty ranking.

---

## 7. Candidate stopping policy

The agent should not seek zero uncertainty.

A working stopping rule is:

> **Act when no remaining credible unresolved dependency has enough potential to change a consequential decision to justify the cost, delay, or authority burden of obtaining more evidence first.**

Practical checks:

1. **Could any remaining credible uncertainty change the responsibility, scope, authority path, stop/continue state, or closure claim?**
   - no -> act / stop as warranted;
   - yes -> continue below.

2. **Would acting while wrong create material exposure?**
   - high -> raise evidence threshold;
   - low/reversible -> tolerate more residual uncertainty.

3. **Can the uncertainty be resolved cheaply and authoritatively?**
   - yes -> resolve it;
   - no -> compare investigation burden with wrong-action exposure.

4. **Is the contemplated action itself information-producing and safely reversible?**
   - yes -> performing it may be the warranted investigation;
   - no -> do not use action as a substitute for missing authority/evidence.

5. **Is the remaining uncertainty fundamentally owner intent or publication authority?**
   - yes -> stop technical investigation and ask/escalate at the genuine authority boundary.

Residual uncertainty should be preserved when material; it does not need to be eliminated for action to be warranted.

---

## 8. Reversibility is a threshold modifier, not a routing table

Do not encode:

```text
reversible -> act
irreversible -> investigate
```

Instead:

> **As wrong-action consequences and irreversibility increase, weaker unresolved dependencies become more important to resolve before action.**

Examples:

Low-cost / reversible / information-producing:

- inspect files or history;
- run a read-only validator/probe;
- create a local draft;
- test an isolated hypothesis.

Higher-consequence / less reversible:

- remove a supported capability;
- rewrite a public contract;
- mutate external tracker state;
- publish a release;
- merge into canonical state;
- declare a material finding closed.

The second group should generally require stronger evidence and clearer authority.

---

## 9. Failure modes this policy should prevent

### Premature implementation

```text
visible bug
-> implementation details
```

when support/ownership/provenance could invalidate the repair.

### Uncertainty tourism

Investigating many unknowns because they are interesting rather than because they could change a decision.

### Information-gain substitution

Choosing the investigation that teaches the most rather than the one that best improves the next decision.

### Owner escalation too early

Asking the owner a question repository evidence can answer.

### Owner escalation too late

Continuing technical research after the remaining uncertainty is genuinely owner intent or publication authority.

### False closure

Treating green validation as sufficient when a finding-specific uncertainty still governs closure.

### Irreversibility blindness

Using the same evidentiary threshold for a cheap reversible probe and a consequential canonical mutation.

### Analysis paralysis

Continuing investigation after remaining uncertainty has low decision value relative to its cost.

---

## 10. What would falsify or revise this model?

Collect normal-use episodes where:

- the selected "nearest" uncertainty repeatedly does not change or improve the decision;
- a downstream uncertainty turns out to have been more decision-relevant than the earliest dependency;
- the qualitative dimensions produce repeated reviewer disagreement without helping explain the choice;
- investigation cost dominates and the policy over-investigates;
- acting early repeatedly causes avoidable rework or false closure;
- reversibility proves too weak/strong a modifier;
- the agent cannot distinguish a credible alternative from speculative possibility;
- a useful investigation has low immediate decision value but high enabling value for later evidence, exposing a myopic-policy failure.

Repeated failures of the same kind may justify deeper formalization. A single difficult case does not.

---

## 11. Observation template for future dogfood

Do not create a schema yet. Preserve the following in research notes or issue/PR evidence when useful:

```text
goal / authorized scope:
provisional next decision:
warrant dependencies:
unresolved uncertainties considered:
selected uncertainty:
why it was decision-changing:
source needed to resolve it:
selected responsibility:
evidence obtained:
decision before evidence:
decision after evidence:
rough investigation cost/delay:
wrong-action exposure avoided or accepted:
residual uncertainty at action:
stop/continue reason:
what would have changed the selection:
```

The most useful outcome is not a large trace corpus. It is enough repeated evidence to discover whether the same selection boundary fails in normal work.

---

## 12. Implications for Workflow v0

No Workflow-v0 edit is warranted yet.

The existing rule remains:

> **Resolve the nearest unresolved decision-changing uncertainty before committing to the eventual solution.**

This research proposes an interpretation to test:

```text
nearest
= earliest unresolved dependency in the current warrant
  whose credible resolution could materially change a consequential decision

worth resolving now
= decision value is high enough relative to evidence cost/delay
  and wrong-action exposure

stop investigating
= no remaining credible uncertainty clears that bar
```

Only repeated normal-use failures should earn a Workflow-v0 revision, formal uncertainty representation, or automation.

---

## 13. Product-design implication

The strongest emerging distinction is:

> **Sensemaking should manage decision-relevant uncertainty, not uncertainty in general.**

That keeps the product narrower than a generic research/planning agent and stronger than a simple observe-think-act loop.

A candidate product-level control statement is:

> **Before consequential action, identify the earliest unresolved premise capable of materially changing what is warranted; resolve it when the decision value of evidence exceeds the burden of obtaining it, otherwise act while preserving residual uncertainty.**

Treat this as a research hypothesis until normal-use evidence warrants promotion.

---

## References / conceptual influences

These sources provide conceptual vocabulary; they do not define Sensemaking's product contract.

- Stuart Russell and Eric Wefald, *Do the Right Thing: Studies in Limited Rationality* (MIT Press, 1991) and related work on rational metareasoning / value of computation.
- Nicholas Hay, Stuart Russell, David Tolpin, Solomon Eyal Shimony, *Selecting Computations: Theory and Applications* (UAI; arXiv:1408.2048).
- Alexander Tuisov, *Search as Computation Allocation* (2026 preprint; arXiv:2607.27871), especially the distinction between information gain and decision value and the explicit stop action.
- C. Nicolò De Sabbata, Theodore R. Sumers, Thomas L. Griffiths, *Rational Metareasoning for Large Language Models* (2024; arXiv:2410.05563), as evidence that cost-sensitive metareasoning can be operationalized for LLM inference without making more reasoning intrinsically better.
- Ben S. Bernanke, *Irreversibility, Uncertainty, and Cyclical Investment* (NBER Working Paper 0502, 1980; QJE 1983), for the option value of waiting for information before irreversible action.

Repository evidence used in this research:

- `ThorStarlord/auteur` issue #63 and its Workflow-v0 / closure evidence;
- `ThorStarlord/auteur` issue #62 and its Workflow-v0 / closure evidence;
- `ThorStarlord/sensemaking-skills` PR #177 canonical-CI reconciliation;
- `docs/agent-native-operating-workflow.md`;
- `docs/research/control-model-research-agenda.md`.
