# Research: Warrant as a Control Primitive

**Status:** research hypothesis / product-design study  
**Authority:** not an ADR, not a product contract, not a Workflow-v0 change  
**Current application domain:** agentic software engineering / repository-centered engineering  
**Research question:**

> **Is warrant a useful common abstraction connecting evidence to responsibility, action, continuation, claims, closure, and authority?**

This document develops Research Path 2 from `docs/research/control-model-research-agenda.md`.
It is deliberately downstream of the existing operating model rather than a replacement for it.

The current product already uses phrases such as "warranted responsibility," "update the warrant," and "what does the evidence warrant next?" The research question is whether those uses reflect one stable control concept or merely convenient language applied to several different problems.

---

## 1. Current research conclusion

A useful first answer is:

> **Warrant is a target-specific, defeasible relation between the current situation and a proposed claim or transition: given the goal, current state, available evidence, applicable constraints, and authority, is this particular responsibility, action, claim, continuation decision, closure decision, or publication step justified now?**

This suggests a compact control question:

> **What does the current evidence and authority warrant for this specific target?**

The research does **not** support treating warrant as:

- a scalar confidence score;
- a new persistent lifecycle state;
- an artifact that replaces evidence;
- a synonym for authorization;
- a machine-readable permission token;
- proof that every downstream transition is also justified.

The strongest distinction emerging from normal-use evidence is:

```text
warrant for target A
!=
warrant for target B
```

Examples:

```text
evidence that a defect is real
may warrant investigation
but not repair

exact-head green CI
may warrant a claim that the candidate passes configured checks
but not a claim that the original finding is closed

technically correct implementation
may warrant recommendation to merge
but not grant merge authority
```

So the candidate product value of `warrant` is not that it collapses the lifecycle. It is that it gives the active agent one recurring question while preserving the distinct evidence and authority conditions required by each target.

---

## 2. Terms used in this research

### Evidence

Observed or durably recorded information that can support or defeat a claim or transition: repository state, history, contracts, tests, validator results, probes, external facts, owner statements, and similar artifacts.

Evidence is an input to warrant. Evidence is not itself warrant.

### Claim

A proposition the agent wants to assert, such as:

- the defect exists;
- the candidate was implemented;
- configured checks passed;
- the original finding is repaired;
- canonical state is healthy.

Different claims require different evidence.

### Responsibility

A bounded class of work selected because the current state demands it: investigate, repair, retire, reconcile, verify, ask owner, stop, or another bounded engineering responsibility.

### Authority

The permission boundary governing who may decide or perform a consequential action. Authority is not factual evidence that a technical claim is true.

### Warrant target

The specific thing currently under justification. Candidate target classes are:

```text
claim
responsibility selection
action
continue / stop / escalate
closure
publish / merge
```

This list is research vocabulary, not a schema.

### Warrant

The current justification for a particular target, relative to current evidence, state, constraints, and authority.

A useful informal notation is:

```text
W(target | goal, current_state, evidence, constraints, authority)
```

This notation is explanatory only. It is not a proposed runtime function or score.

### Warrant gap

A candidate research term for a currently-live missing premise or permission condition that prevents a contemplated target from being warranted.

For example:

```text
target: repair validator

possible warrant gaps:
- is the validator still a supported responsibility?
- does this repository own the responsibility?
- is the observed behavior a live defect?
- is repair authorized in the current scope?
```

Do not create a `warrant_gap` artifact or field without repeated evidence that explicit representation is useful.

---

## 3. Empirical episode A -- Auteur #62

Issue #62 began as a concrete defect report:

```text
validate-workflow-design.py exits 0 when registries fail to load
```

Repository inspection established that the false-green behavior was real. That evidence warranted a stronger factual claim about the defect and warranted further investigation.

It did **not** yet warrant the requested local error-code repair.

The next evidence established that:

- the validator's only fixture was a placeholder that did not exercise meaningful workflow validation;
- current upstream Sensemaking had removed the validator as dead code;
- `validate-repo.py` already covered the live responsibility;
- no live consumer remained beyond harness/fixture/inventory references.

That changed the warranted responsibility from:

```text
repair validator
```

to:

```text
retire obsolete validator responsibility
```

After implementation, exact-head CI and focused checks warranted claims about the **candidate**: the retirement candidate was mechanically healthy and the scoped finding-specific checks passed.

Those checks did not grant merge authority. The issue remained open and the PR remained unmerged until the owner authorized integration.

After guarded integration, canonical push validation, and finding-specific verification on canonical `main`, closure became warranted.

Observed sequence:

```text
defect evidence
  -> warrants investigate

ownership/provenance evidence
  -> warrants retirement responsibility

candidate implementation + exact-head validation
  -> warrants candidate-level implementation/validation claims

owner authorization
  -> permits integration

canonical validation + finding-specific verification
  -> warrants original-finding closure
```

### Lesson

> **Warrant is local to the target. Evidence sufficient for one transition does not automatically propagate to later transitions.**

---

## 4. Empirical episode B -- Sensemaking #147 / PR #180

Issue #147 described ambiguous documentation around `approved_at` and `validity_window.not_before`.

The decision-changing check was deliberately narrow: does current executable behavior already permit approval before `not_before` while gating execution until the window opens?

Direct code and regression tests established yes.

That evidence warranted:

- stopping further architecture investigation;
- a docs-only responsibility;
- no runtime/schema/test/product-design change.

The resulting PR passed the exact-head Validator Ecosystem 18/18.

At that point the technical responsibility was complete, but the PR explicitly remained at an owner integration boundary. Exact-head CI did not grant merge authority.

After owner authorization, the change was merged, canonical `main` was validated, and issue #147 closed.

### Lesson

> **Technical sufficiency and authority are orthogonal inputs. Evidence can justify what should be done without granting permission to perform a protected transition.**

Also:

> **A warrant concept is only useful if it preserves the distinction between "this action is technically justified" and "this actor is authorized to perform it."**

---

## 5. Empirical episode C -- Sensemaking PR #177

Canonical CI initially presented seven failing jobs.

The visible failures did not warrant seven independent repairs. Repository history and live contracts showed three underlying clusters:

1. stale executor-era CI references after the ADR-0013 migration;
2. canonical vocabulary lagging already-live contracts;
3. external-provenance wording being interpreted as a missing local ADR.

Resolving those uncertainties changed the repair responsibilities. The candidate then reached 18/18 exact-head green.

That exact-head result warranted a claim that the candidate satisfied the configured Validator Ecosystem. It did not yet warrant a claim about canonical `main`, because the candidate was not canonical state.

Only after owner-authorized merge and the push-triggered run on the resulting `main` SHA was the canonical-state claim warranted.

### Lesson

> **The target must be named precisely. "Candidate is green" and "canonical state is green" are different claims with different warrant requirements.**

This is one reason a single generic `validated=true` concept is insufficient.

---

## 6. Empirical episode D -- PR #164 and state currency

PR #164 was an exploratory `repo-sensemaker` vNext prototype. It preserved genuine unanswered questions about packaging and further experiments.

Later work moved the product state forward:

- the candidate architecture was stress-tested;
- one prototype field was falsified and removed;
- ADR 0024 recorded owner acceptance of the surviving architecture and four optional extended-analysis fields as the working default;
- current `repo-sensemaker` carries the resulting one-Skill/two-responsibility shape.

The old prototype therefore still contained unanswered questions, but those questions no longer governed the current product decision.

### Lesson

> **Warrant is state-relative and defeasible. A previously-live reason to investigate can lose decision relevance when later evidence or authority changes the current state.**

This adds a currency requirement:

```text
historically unresolved
!=
currently warrant-blocking
```

A warrant assessment should therefore depend on current canonical evidence rather than only on the artifact where a question first appeared.

---

## 7. Candidate properties of warrant

### 7.1 Target-specific

Always ask:

> Warrant for **what**?

Avoid statements such as:

```text
"we have warrant"
```

without a target.

Prefer:

```text
current evidence warrants repository investigation
current evidence warrants a docs-only repair
current evidence warrants the claim that exact-head CI passed
current evidence does not yet warrant finding closure
owner authority permits merge
```

### 7.2 Proportional

The strength of the claim or transition should not exceed the support available for it.

```text
schema valid
-> may warrant structural-validity claim

schema valid
!= analytical correctness
!= original-finding closure
```

### 7.3 Defeasible

New evidence can weaken or remove an earlier warrant.

A green test does not permanently settle a claim if later repository state changes. A historical prototype question does not remain live merely because no one edited the old artifact.

### 7.4 State-relative / currency-sensitive

Warrant should be evaluated against the current relevant state, not remembered state.

This is consistent with the existing `repo-sensemaker` discipline that documented state is not automatically verified current state.

### 7.5 Evidence-traceable

A consequential warrant should be explainable through durable evidence rather than transient confidence or conversation memory.

This does not require a warrant artifact. It requires that material claims/actions remain reconstructable from the evidence that justified them.

### 7.6 Authority-bounded

Some targets require authority in addition to technical evidence.

```text
technical evidence sufficient
+ required authority absent
-> do not perform protected action
```

Authority cannot substitute for truth:

```text
owner authorizes experiment
!= experiment result is known

owner authorizes merge
!= original finding is repaired
```

### 7.7 Non-transitive across lifecycle states

Do not assume:

```text
warranted to investigate
-> warranted to repair
-> warranted to merge
-> warranted to close
```

Each consequential transition must inherit only the evidence/authority that actually supports that target.

---

## 8. Relationship to existing Sensemaking responsibilities

The warrant hypothesis does not require replacing existing product concepts.

### Uncertainty selection

Research Path 1 can be reinterpreted as finding a currently-live **warrant gap** whose resolution has enough decision value to justify investigation.

```text
candidate target
-> what must be true/allowed for it to be warranted?
-> which currently-live gap could materially change the target?
-> resolve that gap from the right source
-> update warrant
```

This does not mean every unknown is a warrant gap.

### Responsibility selection

A responsibility is warranted when the current evidence makes it the appropriate bounded work for the current goal/uncertainty and the current scope permits performing it.

### Mechanical validation

Validation produces bounded evidence about mechanical properties.

It may update warrant for claims such as:

```text
artifact satisfies contract
configured test passed
reference resolves
```

It does not automatically warrant stronger semantic or closure claims.

### Reconciliation

Reconciliation can be understood as a claim-warrant check:

> Does durable evidence actually support the material work claim being made?

This does not need to be renamed or redesigned.

### Repair verification

Repair verification produces evidence specifically relevant to the target:

```text
original finding is closed
```

Generic CI may support that target but does not substitute for finding-specific evidence when the original diagnosis requires it.

### Authority

Authority remains a parallel control dimension. It should not be hidden inside a generic evidence score.

### Orchestration

Orchestration coordinates an already-selected responsibility. Warrant is relevant at the decision boundary that selects or revises that responsibility, not as a replacement scheduler/runtime primitive.

---

## 9. Candidate control loop

If the hypothesis survives normal use, the product may be describable as:

```text
GOAL / AUTHORIZED SCOPE
        |
        v
CANDIDATE TARGET
  claim / responsibility / action / stop / closure / publish
        |
        v
WHAT MUST BE TRUE OR PERMITTED FOR THIS TARGET TO BE WARRANTED?
        |
        v
CURRENTLY-LIVE WARRANT GAPS / DEFEATERS
        |
        v
SELECT EVIDENCE-PRODUCING RESPONSIBILITY
        |
        v
EVIDENCE / AUTHORITY UPDATE
        |
        v
UPDATED TARGET-SPECIFIC WARRANT
        |
        +--> act / claim / continue / stop / escalate / verify
        |
        `--> protected transition only if required authority permits it
```

Compactly:

```text
candidate target
-> warrant check
-> live warrant gap
-> bounded responsibility
-> evidence
-> updated warrant
-> transition or stop
```

This is a research map, not a proposed workflow implementation.

---

## 10. Why `warrant` may be more fundamental than `workflow`

A workflow primarily expresses execution order.

The normal-use cases above repeatedly changed the next responsibility when evidence changed. The stable question was not:

> Which predefined node comes next?

It was:

> What target is justified now, and what is still blocked?

This suggests a possible hierarchy:

```text
Sensemaking control
  -> evaluates target-specific warrant
  -> selects responsibility

execution/orchestration
  -> coordinates the selected responsibility

new evidence
  -> returns to warrant evaluation
```

The hypothesis is **not** that Sensemaking needs a `WarrantEngine`. It is that warranted transition may be a better conceptual primitive than top-level workflow sequencing.

---

## 11. External conceptual influences

These sources supply useful distinctions; they do not define Sensemaking's product contract.

### Toulmin: justification is relational

Stephen Toulmin's *The Uses of Argument* studies how claims are rationally justified through the structure of practical argument rather than treating assertion as self-supporting. The Toulmin tradition's `warrant` concept is especially relevant at the claim level because it distinguishes the supporting information from the reasoning that licenses the claim.

Sensemaking uses the word more broadly in this research: not just data-to-claim support, but justification for target-specific engineering transitions. That extension must be earned by product evidence rather than assumed from the argumentation vocabulary.

### Assurance cases: evidence does not equal claim

Assurance-case research treats a case as argument plus evidence explaining why a particular claim should hold. Work on assurance-case confidence emphasizes defeaters and reasons for doubt, and later Assurance 2.0 work explicitly argues against collapsing confidence into a single attribute or measurement.

Product implication:

> **Do not model warrant as a universal numeric confidence score. Preserve target-specific support, defeaters, and residual uncertainty.**

### Authorization: permission is its own semantic question

Authorization research treats authorization as an independent semantic concept rather than a side effect of implementation mechanics.

Product implication:

> **Keep authorization distinct from evidentiary support. A target can be technically justified but unauthorized, or authorized to attempt without its outcome being established as true.**

---

## 12. Failure modes a warrant framing should prevent

### Warrant propagation

Treating evidence for one lifecycle target as if it automatically justified all downstream transitions.

```text
implemented
-> therefore validated
-> therefore repaired
-> therefore mergeable
-> therefore closed
```

### Confidence substitution

Using confidence language without naming the target or evidence basis.

### Permission substitution

Treating owner permission as evidence that a factual/technical claim is true.

### Evidence substitution

Treating strong technical evidence as permission to mutate/publish when authority is absent.

### Post-hoc warranting

Selecting the desired action first and constructing a rationale afterward rather than letting evidence change the target.

### Stale warrant

Continuing to rely on evidence or unanswered questions whose decision relevance has been superseded by newer canonical state.

### Generic-green closure

Using broad CI success as if it warrants an original-finding closure claim without finding-specific evidence.

---

## 13. What would falsify or revise this model?

Collect normal-use episodes where:

- asking "what does the evidence warrant for this target?" does not improve decision clarity over existing evidence/authority questions;
- competent reviewers consistently use `warrant` in incompatible ways even after the target is named;
- the concept repeatedly obscures rather than clarifies the distinction between evidence and authorization;
- explicit warrant reasoning encourages post-hoc rationalization;
- the bookkeeping/verbosity cost exceeds its decision value;
- target types require such unrelated semantics that a common abstraction becomes vacuous;
- liveness/currency checks cause useful contradictory evidence to be discarded prematurely;
- a single transition routinely requires multiple independent support dimensions that cannot be explained cleanly as one target-specific warrant assessment;
- normal work never produces a case where the warrant framing changes or prevents a consequential decision error.

Repeated failures of the same kind may show that `warrant` should remain explanatory vocabulary rather than a control primitive.

---

## 14. Normal-use dogfood questions

For future engineering episodes, do not add a schema. Ask a few lightweight questions when they can change behavior:

```text
what is the specific target now?
what evidence currently supports it?
what known defeater or warrant gap remains?
what stronger target is NOT yet warranted?
is the relevant evidence current?
does this target require authority independent of technical evidence?
what new evidence would change the target?
```

Especially valuable cases are:

1. evidence warrants a claim but not an action;
2. authority permits an action but evidence is insufficient for a stronger claim;
3. new evidence revokes an earlier responsibility or closure candidate;
4. mechanical validation is green while finding-specific closure remains unwarranted;
5. remaining uncertainty is low-value and action is already sufficiently warranted;
6. two competent reviewers disagree about the target or threshold and the warrant framing either resolves or fails to resolve the disagreement.

---

## 15. Implications for the current product

No product-contract, Workflow-v0, artifact-contract, validator, runtime, or Skill change is warranted by this initial study.

The existing operating loop already contains the important ingredients:

- current evidence;
- nearest decision-changing uncertainty;
- responsibility before Skill;
- bounded work;
- validation;
- reconciliation;
- repair verification;
- KNOW / DECIDE / ACT / PUBLISH authority boundaries;
- update warrant;
- continue / stop / escalate.

The research contribution is a candidate interpretation:

> **Sensemaking may be a control process for repeatedly evaluating and updating what is justified for a specific engineering target as evidence, state, and authority change.**

A stronger candidate product statement is:

> **Sensemaking manages transitions of engineering warrant: it identifies what is not yet justified, selects bounded work that can change that state, and constrains claims and actions to what current evidence and authority support.**

Treat both statements as hypotheses until prospective normal-use dogfood shows that this framing improves real decisions.

---

## 16. Research status and next gate

This document is enough to start a dedicated Path-2 empirical cycle, but not enough to declare warrant a ratified control primitive.

Current status:

```text
research question                         identified
retrospective normal-use evidence          present
candidate qualitative model                present
external conceptual comparison             present
prospective dogfood                         not yet sufficient
repeated falsification attempts             not yet sufficient
product ratification                        not warranted
mechanical formalization                    not warranted
```

Next gate:

> **Use the warrant framing prospectively on a small number of normal engineering transitions and ask whether it changes, prevents, or clarifies a consequential decision.**

If it repeatedly helps, consider whether a small wording clarification in the operating model is warranted.

If it does not, keep `warrant` as explanatory vocabulary and do not build machinery around it.

---

## References / conceptual influences

Repository evidence:

- `docs/agent-native-operating-workflow.md`;
- `docs/decision-orchestration-boundary.md`;
- `skills/using-sensemaking/SKILL.md`;
- `docs/research/uncertainty-selection.md`;
- Auteur issues #62 and #63 and their canonical closure evidence;
- Sensemaking PR #177;
- Sensemaking issue #147 / PR #180;
- Sensemaking PR #164 and ADR 0024.

External conceptual influences:

- Stephen E. Toulmin, *The Uses of Argument*, especially "The Layout of Arguments";
- John B. Goodenough, Charles Weinstock, and Ari Z. Klein, *Toward a Theory of Assurance Case Confidence*, CMU/SEI-2012-TR-002 (2012);
- Robin Bloomfield and John Rushby, *Assessing Confidence with Assurance 2.0* (2022; revised 2024);
- Thomas Y. C. Woo and Simon S. Lam, *Authorization in Distributed Systems: A New Approach* (1993).
