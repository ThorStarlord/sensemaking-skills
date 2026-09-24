# Strategic Normal-Use Failure Taxonomy v1

**Status:** descriptive normal-use evidence guide  
**Authority:** subordinate to Strategic Repository Sensemaking v1, Strategic Sensemaking Loop v1, Policy Hierarchy v0, and current repository authority  
**Runtime effect:** none; no score, automatic detector, schema, or mandatory logging requirement

## 1. Purpose

The current repository strategy is `NO_CHANGE / NORMAL_USE_HANDOFF`.
Normal use should therefore generate evidence about whether the integrated
strategic-control surfaces fail repeatedly in material ways before another
construction package is opened.

This taxonomy makes those failures easier to name without converting ordinary
use into a synthetic benchmark or experiment program.

```text
observed friction
!= product defect automatically

single occurrence
!= recurring material pressure

taxonomy category
!= automatic issue

normal-use evidence
-> reconcile only when decision-relevant
```

## 2. Core failure families

### F1 — Premature convergence

**Signal:** the analysis commits to a familiar/local solution before materially
different repository-level opportunities have been considered.

Examples:

- one visible subsystem dominates the analysis despite cross-system evidence;
- the first plausible idea becomes the Strategic Frontier;
- breadth exploration merely restates the prompt.

Reassessment pressure is stronger when the missed alternative would have changed
the selected responsibility or construction path.

### F2 — Exhaustive-search ceremony

**Signal:** breadth/depth machinery expands work without improving the decision.

Examples:

- every subsystem receives an artificial opportunity;
- depth is performed on low-materiality candidates;
- the Strategic Exploration Summary becomes an idea dump;
- settled execution re-runs repository-wide breadth analysis.

This is the opposite failure of premature convergence.

### F3 — Weak frontier synthesis

**Signal:** observations are collected but not compressed into deeper
decision-relevant candidates.

Examples:

- several symptoms remain separate backlog-like bullets;
- frontier candidates are implementation tasks rather than strategic leverage
  points;
- candidate boundaries overlap so strongly that the real shared problem remains
  hidden.

### F4 — False option diversity

**Signal:** the analysis manufactures nominally different paths that share the
same decisive assumption or downstream framing.

Examples:

- all paths begin after the same unchallenged milestone;
- implementation variants are presented as strategic alternatives;
- a third path is invented only to avoid a binary option set.

Goal Fitness / orthogonality challenge should normally catch this.

### F5 — Goal inversion / proxy capture

**Signal:** a measurable milestone, qualification state, proxy, or evidence gate
quietly replaces the governing product outcome.

Examples:

- release-candidate hardening becomes the goal while required features remain
  incomplete;
- test coverage becomes the target instead of the behavior the tests are meant
  to support;
- exact-SHA qualification becomes the strategic frontier despite an upstream
  product-completion gap.

### F6 — Evidence conservatism / construction starvation

**Signal:** strategically grounded unbuilt futures are repeatedly rejected
because they lack prior proof of future success.

Examples:

- `DEFER` or `INVESTIGATE` is chosen solely because a new capability has not
  already demonstrated value;
- a bounded useful build is replaced by evidence-only work even when normal use
  would provide sufficient evidence;
- omission cost is ignored.

Strategic Hypothesis Admission and Value-Producing Action are intended to guard
against this failure.

### F7 — Experiment reflex

**Signal:** uncertainty is repeatedly converted into experimental work when
cheaper sufficient evidence or retained reversible construction exists.

Examples:

- a diagnostic Skill manufactures experiment responsibility;
- an experiment is selected without decision discrimination;
- confounder-control cost exceeds what the actual claim requires;
- result analysis self-authorizes another experiment.

### F8 — Qualification/hardening preemption

**Signal:** verification or release-hardening repeatedly consumes the strategic
frontier before the underlying product capability is sufficiently complete.

This differs from F5: F5 is a **goal-model error**; F8 is an **action-allocation
error** that may occur even when the goal is correctly stated.

### F9 — Resume regression

**Signal:** a fresh context cannot reconstruct the latest semantically valid
boundary or needlessly repeats completed stages.

Examples:

- strategy is rerun despite a current analysis and selected responsibility;
- reconciliation is ignored because a newer file timestamp is mistaken for
  semantic precedence;
- conversation memory is required to know what happens next.

### F10 — Responsibility/capability collapse

**Signal:** the presence of a Skill, workflow, or tool determines what work is
selected.

Examples:

- a registered capability is treated as a recommendation;
- fog classification automatically routes implementation;
- a workflow identifier is treated as execution authority.

### F11 — Warrant/authority collapse

**Signal:** justified work is treated as authorized, or broad delegation is
treated as protected-transition authority.

Examples:

- green qualification is treated as merge/release permission;
- `proceed autonomously` is interpreted as Level-4 preference authority;
- a decision packet is treated as the owner's decision.

### F12 — Validation/semantic-truth collapse

**Signal:** mechanical validation is used as proof that the semantic conclusion
is correct or that the governing goal is satisfied.

Examples:

- schema-valid strategic analysis is called strategically correct;
- generic CI is used as finding-specific repair proof;
- admitted evidence is treated as warranted conclusion.

### F13 — Reconciliation omission

**Signal:** consequential returned evidence does not update, reaffirm, reopen, or
explicitly leave unchanged the relevant decision model.

Examples:

- implementation contradicts a material assumption but strategy silently
  continues;
- execution evidence changes responsibility but no reconciliation occurs;
- evidence is accumulated without affecting continuation.

### F14 — Over-reconciliation ceremony

**Signal:** trivial execution details trigger strategic artifacts even though
they cannot change Level 3.

This is the symmetric failure of F13.

### F15 — Owner-decision fabrication

**Signal:** the repository tries to answer a genuinely preference-sensitive or
reserved premise.

Examples:

- the agent selects between product identities based on repository evidence that
  cannot establish owner preference;
- an incomplete option set is forced into a binary capsule;
- Level-4 commitments are silently revised.

### F16 — Global freeze from a local blocker

**Signal:** one unavailable verification/external gate stops unrelated
independently warranted repository work.

The inverse failure also matters: continuing work that actually depends on or
routes around the blocked gate.

### F17 — Front-door leakage / orchestration ceremony

**Signal:** the user must manually sequence internal semantic responsibilities
that the one-prompt loop can reconstruct.

Examples:

- requiring `strategic-repository-analysis -> using-sensemaking -> handoff ->
  reconciliation` prompts for an ordinary strategic episode;
- forcing `handoff` between stages handled by the same active agent;
- exposing internal policy vocabulary when it cannot change user action.

### F18 — Compatibility authority leakage

**Signal:** historical workflow/runtime surfaces regain semantic routing
authority merely because they still exist.

Examples:

- legacy fog-to-workflow routing becomes current behavior;
- deprecated registry entries are treated as supported product direction;
- retained research machinery becomes shipped-product authority.

## 3. Evidence record for a material occurrence

No new artifact is required. When a failure materially changes repository
strategy or responsibility, preserve only the evidence needed by the existing
surface (issue, reconciliation, handoff, Campaign evidence, or ordinary
repository documentation).

A useful human-readable occurrence note is:

```text
Observed category:
Repository/context:
Concrete behavior:
Expected governing boundary:
Decision/product effect:
Recurring or isolated:
Existing artifact/evidence refs:
Does this warrant repository change now? yes / no / uncertain
```

Do not assign numeric severity or confidence merely because a category exists.

## 4. Reopen rule

A new construction package is more strongly warranted when ordinary use shows a
**recurring material failure** whose correction is mechanically/documentarily
bounded and not already handled by current guidance.

Examples of weak reopen evidence:

- one awkward explanation;
- a user preferring different wording;
- a hypothetical failure not observed in use;
- a synthetic benchmark invented solely to exercise the taxonomy.

Examples of stronger reopen evidence:

- the same category changes the selected responsibility across multiple real
  episodes;
- a fresh context repeatedly cannot resume without conversation memory;
- strategic breadth repeatedly misses materially different paths;
- experiment reflex persists despite the current Experiment Economy guidance;
- Goal Fitness repeatedly allows proxy capture.

## 5. Relationship to the current normal-use handoff

This taxonomy operationalizes the existing `STATUS.md` reassessment questions.
It does not supersede them.

```text
taxonomy
= shared language for normal-use evidence

taxonomy
!= mandatory telemetry
!= defect database
!= issue generator
!= strategic scorer
```
