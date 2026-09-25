# Autonomous Terminal Mission Continuation v1 — Handoff

**Status:** IMPLEMENTED / PR OPEN / QUALIFICATION PENDING  
**Issue:** #473 — Autonomous Terminal Mission Continuation v1  
**Feature PR:** #474 — feat: add Autonomous Terminal Mission Continuation v1  
**Date:** 2026-09-24

## 1. Why this package exists

Strategic Sensemaking already had:

- a robust Level-3 decision model;
- artifact-aware resume;
- a high-delegation repository envelope;
- value-producing action preference;
- bounded BUILD / REVERSIBLE BUILD / VERIFY / INQUIRE / EXPERIMENT action shapes;
- returned-evidence reconciliation;
- explicit protected-transition boundaries.

The remaining product gap was continuation across **multiple bounded
responsibilities under one terminal repository mission**.

Normal high-delegation guidance could continue through ordinary
repository-answerable work, but it did not make the terminal-mission law explicit
enough:

```text
responsibility completed
!= mission completed

mission incomplete
-> reconcile current reality
-> identify highest-value remaining difference
-> establish next warranted responsibility
-> continue
```

This package makes that behavior first-class inside the existing
`strategic-sensemaking-loop` front door without creating another Skill,
planner, authority model, or runtime.

## 2. Integrated candidate behavior

### Autonomous terminal-mission profile

The loop now explicitly recognizes:

- `FULL AUTONOMY`;
- `FULL DELEGATION`;
- `AUTONOMOUS_HIGHEST_LEVERAGE_BOTTLENECK`;
- equivalent terminal-outcome delegation.

The canonical detailed reference is:

`skills/strategic-sensemaking-loop/references/autonomous-terminal-mission-v1.md`.

### Repeated responsibility continuation

After each consequential responsibility, the profile requires:

```text
execute
-> verify
-> reconcile
-> compare current reality with terminal goal
-> identify material remaining difference
-> establish next warranted + authorized responsibility
-> continue
```

The mission does not become backlog execution and does not continue after the
terminal outcome is already satisfied.

### Conditional breadth / depth

The profile reuses the Strategic Exploration Funnel only at a genuine
`ANALYZE / REOPEN_ANALYSIS` boundary.

It explicitly rejects:

- mandatory exactly-three architecture generation;
- repository-wide breadth after every responsibility;
- deep design of every breadth candidate;
- numeric leverage/priority scoring.

`AUTONOMOUS_HIGHEST_LEVERAGE_BOTTLENECK` means qualitative selection of the
highest-value remaining difference to the authoritative terminal outcome.

### Decision-relevant vertical completion

"Complete the vertical stack" now means every layer materially required by the
selected capability, potentially including domain, interface, persistence,
integration, user/operator, observability, content/progression, compatibility,
documentation, and qualification.

It does not require irrelevant architecture merely to satisfy a generic
checklist.

### Construction before field validation

A terminal mission may explicitly defer external user trials, beta feedback,
professional asset production, panels, or live telemetry until construction
completeness.

That policy is mission-scoped and defeasible by authoritative safety, legal,
regulatory, product, or repository prerequisites.

```text
external validation deferred
!= externally validated
```

### Synthetic-persona claim discipline

First-principles heuristics and synthetic personas may support
construction-stage design judgment.

They may not be represented as:

- empirical user evidence;
- usability validation;
- stakeholder approval;
- live product evidence.

### Evidence-gated canonical promotion

The profile preserves:

```text
implement
-> verify
-> reconcile
-> promote status/authority only when supported
```

Delegated authority to update status/capability manifests does not predetermine
that the evidence supports promotion.

### Protected-transition authority

The ordinary full-autonomy repository envelope may include:

- repository analysis and bounded responsibility selection;
- implementation/repair/refactor/deletion;
- tests/docs/qualification;
- repository-local status/capability updates when warranted;
- issues/branches/commits/pull requests;
- continued repository-answerable work.

The following remain separately governed unless explicitly granted and permitted
by repository policy:

- merge;
- release/deployment;
- external publication;
- credentials/security/account changes;
- billing/spending;
- destructive external mutation;
- cross-repository scope expansion;
- Level-4 thesis revision;
- genuine owner-preference decisions.

The profile allows explicit mission-specific grants such as:

```text
MERGE_AUTHORITY = YES
RELEASE_AUTHORITY = NO
DEPLOY_AUTHORITY = NO
```

without inferring them from autonomy wording.

## 3. Product-surface integration

The candidate updates:

- `skills/strategic-sensemaking-loop/SKILL.md`;
- `skills/strategic-sensemaking-loop/agents/openai.yaml`;
- `skills/strategic-sensemaking-loop/references/autonomous-terminal-mission-v1.md`;
- `skills/using-sensemaking/SKILL.md`;
- `skills/using-sensemaking/references/delegated-goal-patterns.md`;
- `GETTING_STARTED.md`;
- `docs/strategic-sensemaking-loop-v1.md`;
- `README.md`;
- `STATUS.md`;
- `CHANGELOG.md`;
- focused regression coverage in `tests/test_autonomous_terminal_mission_v1.py`.

No new top-level Skill is introduced.

## 4. Qualification target

The candidate should preserve existing Strategic Sensemaking Loop contracts and
establish mechanically that:

- the existing loop is still the single front door;
- Skill frontmatter remains `name` + `description` only;
- UI metadata retains its existing "one prompt" contract;
- full-autonomy trigger language is discoverable;
- repeated responsibility continuation is explicit;
- breadth remains conditional and does not force three paths;
- vertical completion is decision-relevant rather than maximal architecture;
- construction-before-field-validation preserves claim boundaries;
- synthetic personas remain non-empirical;
- status promotion requires verification/reconciliation;
- protected transitions remain separately governed;
- human entry points expose the canonical terminal-mission prompt;
- no new planner/runtime/permission/priority/Campaign machinery appears.

Final exact-head qualification is pending GitHub Actions for PR #474.

## 5. Claim ceiling

If the candidate passes repository qualification, it can establish:

- coherent repository representation of full-autonomy terminal-mission
  continuation;
- compatibility with existing Skill/control contracts;
- explicit authority and claim boundaries;
- a reusable canonical human invocation pattern.

It does **not** establish:

- that agents will always select the objectively best remaining responsibility;
- that every repository should use full autonomy;
- that field validation is unnecessary;
- that synthetic personas predict real users;
- that full autonomy grants merge/release/deployment authority;
- that every capability requires a maximal vertical architecture;
- comparative superiority over other autonomous coding workflows;
- that a new planner, scheduler, permission engine, or autonomous runtime is
  warranted.

## 6. Current posture

```text
ISSUE_473_AUTONOMOUS_TERMINAL_MISSION_CONTINUATION_V1
= IMPLEMENTED_PR_OPEN_QUALIFICATION_PENDING

NEW_TOP_LEVEL_SKILL = NO
NEW_RUNTIME = NO
NEW_AUTHORITY_MODEL = NO
MERGE_AUTHORITY_EXPANSION = NO
```

After qualification, normal use should observe whether terminal missions
actually reduce unnecessary approval stops while preserving goal, authority,
evidence, and stopping discipline.
