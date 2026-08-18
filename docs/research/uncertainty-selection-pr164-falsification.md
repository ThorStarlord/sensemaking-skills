# Research addendum: PR #164 and stale-vs-live uncertainty

**Status:** research evidence / falsification note  
**Authority:** not an ADR, not a product contract, not a Workflow-v0 change  
**Parent research:** `docs/research/uncertainty-selection.md`  
**Observed against:** `main@eca65857b0ac1bc918f688b55d92e0aa88671914` on 2026-08-17

## Question tested

The parent research proposes:

> Resolve the nearest unresolved decision-changing uncertainty before committing to the eventual solution.

PR #164 (`repo-sensemaker vNext exploratory spike`) presented a useful stress case because the prototype branch still contained genuine unanswered questions, including whether its Option-A two-Skill packaging should beat alternatives and whether another owner-originated or independently-invoked experiment should be run.

The apparent next responsibility was therefore:

```text
rebase PR #164
-> rerun its checks
-> run another vNext experiment
```

Before doing that, one earlier dependency in the warrant for spending more evidence-gathering effort was tested:

> **Is PR #164 still the live decision surface, or have its material questions already been harvested and adjudicated elsewhere?**

## Evidence

Repository evidence showed that the answer was the latter:

- PR #164 was explicitly an exploratory prototype and not intended as a production merge.
- `docs/candidate/architecture-decision.md` records that #164 is the evidence record ("what did we learn"), while the candidate branch represented what the product should become.
- That decision selected Option C: Diagnose and conversational Interact remain conceptually separate responsibilities inside one `repo-sensemaker` Skill rather than becoming two independently routable Skills.
- ADR 0024 explicitly names PR #164 as exploratory evidence, records the subsequent stress-test cycle, records that one prototype field (`discovery_confidence`) was falsified and removed, and records owner acceptance of the four surviving `extended_analysis` fields as the working default design.
- Current `skills/repo-sensemaker/SKILL.md` carries the one-Skill/two-responsibility shape and the accepted optional extended-analysis behavior.

The prototype therefore still contained unanswered historical questions, but those questions no longer governed the current product decision.

PR #164 was closed without merge and preserved as historical evidence rather than refreshed as an active implementation candidate.

## Falsification result

This case sharpens the parent hypothesis:

> **An unresolved question is not necessarily an unresolved decision dependency.**

A question should not receive evidence-gathering priority merely because an older artifact still records it as open. The agent should first establish that the uncertainty is still **currently live** in the warrant for a consequential present decision.

A candidate refinement of "nearest" is therefore:

```text
nearest
= earliest currently live unresolved dependency in the present warrant
  whose credible resolution could materially change a consequential decision
```

"Currently live" means that the premise has not already been superseded, answered, made irrelevant, or transferred to another authority by later evidence or decisions.

This is a research refinement only. It does not replace Workflow v0.

## Why this matters

Without the liveness check, a Sensemaking agent can perform perfectly rigorous work against the wrong decision surface. That failure mode looks disciplined locally:

```text
old artifact contains an unresolved question
-> gather authoritative evidence
-> answer the question carefully
```

but is globally wasteful if later canonical evidence has already removed that question from the current warrant.

The failure is not "bad investigation." It is **stale uncertainty selection**.

This adds a distinct failure mode to watch for alongside uncertainty tourism and information-gain substitution:

### Stale uncertainty selection

Treating an unresolved question in historical/prototype evidence as a current blocker without first checking whether later canonical evidence or authority decisions have already superseded its decision relevance.

## Observation trace

```text
goal / authorized scope:
  stress-test the uncertainty-selection policy on PR #164 without implementing first

provisional next decision:
  refresh/rebase #164 and run another vNext experiment

warrant dependencies:
  1. #164 still represents a live product decision
  2. another experiment could materially change that decision
  3. the prototype branch remains an appropriate evidence surface

unresolved uncertainties considered:
  - is Option A better than Option C?
  - would another owner-originated run change the package decision?
  - is #164 still the live decision surface at all?

selected uncertainty:
  is #164 still the live decision surface?

why it was decision-changing:
  a negative answer invalidates the entire proposed experiment/rebase responsibility

source needed to resolve it:
  canonical repository evidence and accepted decision records

selected responsibility:
  inspect current product/ADR state before further experimentation

evidence obtained:
  candidate architecture record, ADR 0024, current repo-sensemaker Skill, PR state

decision before evidence:
  likely refresh #164 and run another experiment

decision after evidence:
  close #164 unmerged as completed exploratory evidence; do not rerun it merely to answer stale prototype questions

wrong-action exposure avoided or accepted:
  avoided unnecessary prototype maintenance and evidence collection against a superseded packaging decision

residual uncertainty at action:
  future normal-use cases may still falsify the accepted design, but that is a new live experiment trigger rather than unfinished #164 work

stop/continue reason:
  stop work on #164 because its remaining questions no longer clear the decision-value bar for the current product decision
```

## Boundary with live defects

This result must not be generalized into "old PR means stale finding."

During the same review, the `integration_fog` validator divergence associated with PR #163 remained observable on current `main`: canonical vocabulary includes `integration_fog`, while `scripts/validate-brief.py` still hard-codes a four-value set that omits it.

That is the inverse case:

```text
old/conflicted PR
!=
stale underlying finding
```

The correct question remains whether the **finding is live in current canonical state**, not whether the artifact that first carried it is old.

Any repair of that validator drift is a separate engineering responsibility and is intentionally out of scope for this research-only note.

## What would revise this refinement?

Revisit the "currently live" qualifier if normal-use cases show that:

- historical unresolved questions routinely retain important option value even after later decisions;
- the liveness check causes the agent to prematurely discard useful contradictory evidence;
- determining liveness costs more than the investigation it is supposed to avoid;
- multiple authorities legitimately keep competing decision surfaces live at once;
- an apparently superseded question later proves to have been a hidden premise in the canonical decision.

Until repeated evidence shows one of those failure modes, the working research hypothesis is:

> **Select among currently live warrant dependencies, not among every unresolved question the repository remembers.**
