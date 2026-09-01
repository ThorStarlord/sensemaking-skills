# Normal-Use Control-Model Evidence Lane

**Status:** research-operations note / standing normal-use evidence lane  
**Authority:** not an ADR, not a product contract, not a roadmap commitment, not a Workflow-v0 change  
**Tracker:** Issue #218  
**Baseline:** `main@c9092951dc1c494b329c1d2c15bcd654e6dd3dbf`  
**Primary application domain:** agentic software engineering / repository-centered engineering

## 1. Purpose

The bounded research sequence through Path 4 is complete enough to stop manufacturing a new synthetic path by default.

The next useful evidence source is ordinary engineering work.

This lane exists to preserve a **small, decision-relevant corpus of real normal-use episodes** so recurring friction can determine whether a focused follow-up study is warranted.

It is deliberately lightweight:

- no new research path is created merely by using this lane;
- no governed experiment campaign is required;
- no schema, score, state machine, Skill, workflow, routing policy, or runtime component is introduced;
- no task is performed merely to generate research evidence;
- no requirement exists to trace every engineering action.

The canonical control-model agenda remains authoritative for research priority and promotion discipline.

## 2. Current research posture

The current product remains a software-engineering sensemaking/control layer.

The highest-value continuing research question is still:

> **How should a Sensemaking agent determine which unresolved uncertainty is worth resolving before acting?**

The existing operating rule remains:

> **Resolve the nearest unresolved decision-changing uncertainty before committing to the eventual solution.**

The next phase should improve, qualify, or falsify that rule through normal use rather than by inventing another abstraction first.

Path 2, Path 3, and Path 4 remain observationally live as secondary hypotheses, but they do not require dedicated studies unless recurring real evidence creates a concrete reason.

## 3. What qualifies as an episode

Capture an episode only when all of the following are substantially true:

1. it arose from **ordinary engineering work**, not a constructed research scenario;
2. there was a **consequential decision** involving responsibility, scope, authority, continuation, or closure;
3. at least one credible alternative decision or responsibility existed at the decision point;
4. evidence gathering, acting, stopping, or escalation could plausibly have changed the decision;
5. enough durable evidence exists to reconstruct what happened without inventing hidden state.

Good candidates include:

- a visible defect whose correct responsibility may actually be retirement, reconciliation, ownership clarification, or no action;
- several live uncertainties competing to govern the next responsibility;
- a cheap evidence lookup that prevents costly or irreversible work;
- an `act_now` decision where further investigation looks attractive but non-gating;
- a case where green validation is insufficient for the actual closure claim;
- a case where owner intent or authority becomes the genuine remaining blocker;
- a case where orchestration pressure begins selecting materially different engineering work;
- a naturally arising non-software case that tests the Path 4 transfer hypothesis without being constructed for that purpose.

Do **not** capture:

- routine implementation details after the consequential responsibility is already stable;
- every successful validation run;
- unknowns that are merely interesting and do not affect the next decision;
- synthetic scenarios created solely to populate the tracker;
- retrospective stories that cannot be grounded in durable evidence.

## 4. Primary observation priority — uncertainty selection

Prefer episodes that can sharpen or falsify the uncertainty-selection model.

Especially useful signals include:

- **uncertainty tourism:** investigation reduces uncertainty but does not improve the decision;
- **premature action:** a cheap consequential uncertainty was skipped and avoidable rework or false closure followed;
- **competing live dependencies:** multiple plausible uncertainties could materially redirect the next responsibility;
- **stopping difficulty:** it is genuinely unclear whether to gather more evidence or act now;
- **reviewer disagreement:** competent reviewers repeatedly choose different governing uncertainties;
- **poor explainability:** the selected uncertainty cannot be explained in terms of responsibility, scope, authority, continuation, or closure;
- **myopic decision value:** an apparently low-immediate-value investigation repeatedly proves enabling for later evidence;
- **analysis paralysis:** the agent keeps investigating after remaining uncertainty no longer justifies its cost or delay.

A successful episode is useful too. The lane should not collect only failures. Evidence that the current rule prevents wrong work, selects a cheaper authoritative source, or produces a clean stop decision is relevant corroboration.

## 5. Secondary watchlist

When an eligible normal-use episode naturally exposes another research boundary, preserve it without automatically opening a new study.

### Path 2 — warrant

Watch for cases where target-specific warrant:

- changes or clarifies the selected responsibility;
- prevents an unsupported transition or claim;
- exposes an authority/verification distinction;
- becomes verbose, circular, ambiguous, or unhelpful.

### Path 3 — decision versus orchestration

Watch for repeated cases where:

- deterministic execution coordination starts implicitly choosing a different engineering responsibility; or
- Sensemaking would need generic scheduling, retry, queue, persistence, DAG, or worker-management machinery merely to coordinate already-selected work.

### Path 4 — domain transfer

Preserve naturally arising cross-domain evidence when it occurs.

Do not construct a new cross-domain test merely to add an episode. The useful question is whether the control relation survives real domain semantics without forced software analogy.

## 6. Recording timing

Prefer capture close to the consequential decision, after enough evidence exists to describe the state truthfully.

A practical sequence is:

1. do the normal engineering work;
2. if a qualifying decision point appears, preserve the decision state and plausible alternative;
3. obtain the evidence required by the work itself;
4. record the resulting decision effect and residual uncertainty;
5. link exact durable repository evidence.

Do not delay or distort the engineering work merely to improve the research record.

## 7. Recording method

The rolling index is **Issue #218**.

Use one issue comment per qualifying episode. Keep the comment human-readable; this is not a machine-validated schema.

Use the observation fields already defined in `docs/research/uncertainty-selection.md`:

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

Also include, when available:

- exact issue / PR / commit / file / workflow-run references;
- whether the episode primarily corroborates, weakens, or remains ambiguous for the current uncertainty-selection interpretation;
- any secondary Path 2 / Path 3 / Path 4 signal;
- whether the same failure boundary has appeared before.

Do not invent unavailable machine-local or executor-local evidence.

## 8. Evidence-quality discipline

The lane should resist both hindsight bias and failure-only selection.

For each recorded episode:

- distinguish evidence available **at the decision point** from evidence learned later;
- preserve the plausible competing responsibility rather than rewriting the story as inevitable;
- record residual uncertainty instead of manufacturing certainty;
- state when the decision effect is ambiguous;
- separate technical evidence from action/merge/publication authority;
- distinguish candidate validity, canonical-state validity, and finding-specific closure when they differ;
- prefer exact durable repository references over prose recollection.

Historical artifacts may preserve useful evidence without remaining the correct current implementation vehicle.

## 9. Pattern review — when to open a focused study

A single difficult episode does **not** justify formalization.

Open a focused bounded study only after **materially similar normal-use episodes recur** and expose a stable enough question, such as:

- the same uncertainty-selection failure repeats across independent work;
- reviewer disagreement repeats around the same qualitative boundary;
- the same manual reasoning burden repeatedly causes mistakes, delay, or false closure;
- decision/orchestration ownership repeatedly becomes unclear in the same way;
- naturally arising cross-domain cases repeatedly require the same conceptual qualification.

When recurrence appears:

1. identify the smallest common failure boundary;
2. select and freeze the relevant real episode set **before synthesis**;
3. formulate the narrowest research question supported by those episodes;
4. preserve counterexamples and ambiguous cases;
5. prefer a bounded qualitative result before proposing machinery.

Do not create a new Path number merely because enough comments exist.

## 10. Formalization gate

The existing promotion rule remains unchanged:

```text
repeated useful responsibility
+ stable enough semantics
+ repeated manual burden/error
+ mechanically expressible boundary
        -> candidate for formalization
```

Conceptual elegance, one successful case, or one frustrating case is insufficient.

This lane does not authorize:

- an uncertainty score or ranking engine;
- a warrant schema or `WarrantEngine`;
- automatic routing;
- a new workflow lifecycle;
- a new Skill merely for evidence capture;
- a decision/orchestration state machine;
- a generic Sensemaking Core or domain-pack architecture;
- automatic domain detection;
- scheduler, queue, worker, persistence, DAG, retry, or other generic runtime machinery;
- automatic episode capture.

## 11. Relationship to existing evidence

This lane complements rather than replaces existing repository evidence practices.

Relevant precedents include:

- `artifacts/dogfood-evidence-index.md`, which preserves provenance and separates historical from current-state dogfood evidence;
- `docs/research/warrant-prospective-dogfood.md`, which shows how prospective normal-use evidence can change a consequential decision without earning new machinery;
- `docs/research/uncertainty-selection.md`, which contains the canonical qualitative selection/stopping model and observation template;
- `docs/research/control-model-research-agenda.md`, which sets the current priority and research-discipline boundary.

The standing tracker should link to those artifacts where relevant rather than duplicating them.

## 12. Operating status

At establishment:

```text
standing tracker                     Issue #218
new post-Path-4 normal-use episodes  2
   (001 — Issue #190 safe-edit boundary; 002 — PR #249 merge base-advance race)
recurring failure boundary            none yet (each episode is a distinct, first-occurrence boundary)
focused follow-up study               none yet
formalization candidate               none yet
```

The desired state is not a large dataset. It is enough honest normal-use evidence to discover whether a recurring decision boundary actually needs deeper research or product change.

Until such evidence appears:

> **Keep using the current software-engineering control model, preserve consequential episodes when they arise naturally, and let repeated real friction—not another synthetic path—choose the next research question.**
