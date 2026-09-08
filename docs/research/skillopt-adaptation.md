# SkillOpt Influence and Adaptation in Sensemaking Skills

**Status:** Research provenance and adaptation record  
**Authority:** Informational / historical; not an ADR, runtime contract, Skill specification, experiment authorization, or v0.3 implementation requirement  
**Sensemaking snapshot reviewed:** `edef666680dd159f21af4835b5ecc4ccad45881a`  
**SkillOpt repository:** `microsoft/SkillOpt`  
**SkillOpt revision reviewed:** `79124b37e9a6371e13b753f8bcd7adb1e493ade1`  
**Current product model:** [`../sensemaking-campaign.md`](../sensemaking-campaign.md)  
**Current delivery plan:** [`../productization-v0.3.md`](../productization-v0.3.md)

## 1. Purpose

This document records how ideas examined in Microsoft SkillOpt influenced or resemble work in Sensemaking Skills, where those ideas live today, and which SkillOpt mechanisms are deliberately outside the current product boundary.

It exists to preserve provenance without collapsing distinct claims.

The governing distinction is:

```text
inspiration
!= direct adaptation
!= generalized product principle
!= implementation
!= product commitment
```

Sensemaking Skills is not a fork, reimplementation, or productization of SkillOpt. The current Sensemaking product is the **Sensemaking Campaign**: a durable engineering decision process in which the active coding agent retains semantic control and deterministic machinery preserves state, evidence, authority, provenance, transitions, and reconstruction.

SkillOpt is relevant primarily as an influence on **Skill-quality experimentation and qualification discipline**, plus several broader methodological parallels.

## 2. Source and attribution policy

### 2.1 SkillOpt source snapshot

This record pins SkillOpt at:

```text
microsoft/SkillOpt
79124b37e9a6371e13b753f8bcd7adb1e493ade1
```

The external claims below were checked against these files at that revision:

- [`README.md`](https://github.com/microsoft/SkillOpt/blob/79124b37e9a6371e13b753f8bcd7adb1e493ade1/README.md)
- [`docs/index.md`](https://github.com/microsoft/SkillOpt/blob/79124b37e9a6371e13b753f8bcd7adb1e493ade1/docs/index.md)
- [`docs/sleep/README.md`](https://github.com/microsoft/SkillOpt/blob/79124b37e9a6371e13b753f8bcd7adb1e493ade1/docs/sleep/README.md)

A future SkillOpt revision may behave differently. This document does not silently float with SkillOpt `main`.

### 2.2 Sensemaking sources

Current product disposition is checked against merged Sensemaking `main` at:

```text
edef666680dd159f21af4835b5ecc4ccad45881a
```

Relevant current sources include:

- [`../sensemaking-campaign.md`](../sensemaking-campaign.md)
- [`../productization-v0.3.md`](../productization-v0.3.md)
- [`../../STATUS.md`](../../STATUS.md)
- [`../campaign-semantics.md`](../campaign-semantics.md)
- [`../artifact-ingestion.md`](../artifact-ingestion.md)

Historical Empirical Skill Qualification work is represented by closed, unmerged research PRs and the disposition preserved on current `main`:

- [PR #273 — `research: preregister empirical Skill qualification v1`](https://github.com/ThorStarlord/sensemaking-skills/pull/273)
- [PR #276 — `experiment: EXP-0006 diagnostic results — do not merge`](https://github.com/ThorStarlord/sensemaking-skills/pull/276)

Those PRs are historical research evidence, **not merged product authority**.

### 2.3 Attribution vocabulary

Use the following labels when describing lineage:

| Label | Meaning |
|---|---|
| `OWNER_ATTESTED_DIRECT_ADAPTATION` | The owner identifies SkillOpt as a source of the idea and the historical Sensemaking design contains a concrete adaptation of that mechanism. This is provenance, not a claim of copied code or identical semantics. |
| `REPOSITORY_VERIFIED_GENERALIZATION` | A current Sensemaking product mechanism embodies a broader principle compatible with or reinforced by the SkillOpt work, but this document does not claim SkillOpt was its sole cause. |
| `CONCEPTUAL_PARALLEL` | The systems exhibit a useful similarity, but direct historical lineage is not established here. |
| `RESEARCH_ONLY` | The mechanism existed only in exploratory/qualification work and is not current Campaign behavior. |
| `DEFERRED` | Potentially useful later, but not part of the active v0.3 roadmap. |
| `NOT_ADOPTED` | Explicitly outside the current product boundary. |

This vocabulary prevents resemblance from being rewritten as provenance.

## 3. What SkillOpt does at the pinned revision

Only mechanisms relevant to this comparison are summarized here.

### 3.1 Skill document as optimization state

SkillOpt treats a natural-language Skill document as trainable state while leaving target model weights unchanged.

Its research-engine loop is represented as:

```text
rollout
→ reflect
→ aggregate
→ select
→ update Skill document
→ gated validation
→ next iteration / epoch
```

The optimizer analyzes scored trajectories, produces edit patches, selects/clips updates, applies them to the Skill document, and evaluates the candidate behind a validation gate.

### 3.2 Bounded updates and held-out gating

At the pinned revision, SkillOpt describes:

- bounded add/delete/replace edits to a Skill document;
- a learning-rate-like edit budget;
- held-out/selection-split validation;
- candidate acceptance gated on validation performance in its default paper-style path;
- rejected-edit memory/buffering;
- epoch-level slow/meta updates.

These mechanisms make Skill improvement an explicit candidate-evaluation process rather than an unreviewed one-shot rewrite.

### 3.3 Separate target and optimizer roles

SkillOpt separates the target performing tasks from optimizer behavior that reflects on trajectories and proposes Skill updates.

That separation is relevant to Sensemaking because it reinforces the idea that **the object being evaluated should not silently decide its own acceptance conditions**.

### 3.4 Multi-harness execution

SkillOpt supports multiple model/execution backends and documents execution through agent harnesses including Codex and Claude Code, with additional integration shells in its deployment companion.

This is relevant as a portability example, not as evidence that Sensemaking's own harness-neutral architecture originated only from SkillOpt.

### 3.5 SkillOpt-Sleep

SkillOpt-Sleep is a separate deployment-time workflow. At the pinned revision it can:

```text
harvest supported coding-agent sessions
→ mine recurring tasks
→ replay tasks
→ consolidate through bounded edits
→ gate on held-out tasks
→ stage proposal
→ human adoption
```

It explicitly stages proposals for review/adoption and does not add a separate optimization loop to ordinary agent requests.

Sensemaking does **not** currently adopt this nightly self-evolution workflow.

## 4. Why Sensemaking examined SkillOpt

Sensemaking had a recurring product/research problem:

> How can a Skill be improved from observed defects without treating a plausible rewrite as proof of improvement?

A naive process would be:

```text
observe weakness
→ edit Skill
→ new Skill becomes current
```

The SkillOpt comparison reinforced a stricter pattern:

```text
observe behavior
→ attribute defect
→ create bounded candidate
→ evaluate candidate separately
→ preserve comparison evidence
→ promote only under an explicit acceptance boundary
```

Sensemaking adapted this problem to its own governance, evidence, and agent-native architecture rather than importing SkillOpt's optimizer loop wholesale.

## 5. Adaptation map

| SkillOpt concept | Sensemaking treatment | Lineage / disposition | Current home |
|---|---|---|---|
| Skill document is candidate state | Exact baseline and candidate Skill identity | `OWNER_ATTESTED_DIRECT_ADAPTATION`, `RESEARCH_ONLY` | Empirical Skill Qualification / PR #273 |
| Held-out validation | Frozen Q/T holdout corpus separated from candidate authoring | `OWNER_ATTESTED_DIRECT_ADAPTATION`, `RESEARCH_ONLY` | Holdout protocol summarized by PR #273 and current `STATUS.md` |
| Candidate-specific gate | Baseline-vs-candidate blind qualification before any promotion claim | `OWNER_ATTESTED_DIRECT_ADAPTATION`, `RESEARCH_ONLY` | Empirical Skill Qualification scaffold |
| Bounded Skill edit | Candidate budget: one target Skill, one modified file, at most two instruction regions; full rewrite prohibited | `OWNER_ATTESTED_DIRECT_ADAPTATION`, `RESEARCH_ONLY` | PR #273 experiment contract |
| Selection/evaluation split discipline | D for diagnosis; Q/T held out; T unopened unless Q is `IMPROVED` | `OWNER_ATTESTED_DIRECT_ADAPTATION`, `RESEARCH_ONLY` | PR #273 qualification scaffold |
| Prevent leakage between train/eval information | Fresh holdout-custodian context, split-leak detection, leakage invalidates candidate cycle | `OWNER_ATTESTED_DIRECT_ADAPTATION`, `RESEARCH_ONLY` | PR #273 holdout protocol |
| Separate evaluation record from candidate authoring | Blind evaluator records and post-unblinding normalization separated | `OWNER_ATTESTED_DIRECT_ADAPTATION`, `RESEARCH_ONLY` | PR #273 deterministic scaffold |
| Acceptance should be evidence-gated | Candidate classification fails closed across `IMPROVED`, `EQUIVALENT`, `MIXED`, `REGRESSED`, `INCONCLUSIVE` | `OWNER_ATTESTED_DIRECT_ADAPTATION`, `RESEARCH_ONLY` | PR #273 qualification scaffold |
| Candidate should not auto-promote | Automatic adoption/merge prohibited | `OWNER_ATTESTED_DIRECT_ADAPTATION`, `RESEARCH_ONLY`; also consistent with current authority model | PR #273 / current product non-goals |
| Exact candidate identity matters | Exact-head qualification and content-addressed artifact/evidence identity | `REPOSITORY_VERIFIED_GENERALIZATION` | release qualification, P4 artifact admission |
| Candidate existence does not imply acceptance | `file exists != validated artifact != admitted evidence` | `REPOSITORY_VERIFIED_GENERALIZATION` | P4 artifact admission |
| Evaluation is evidence, not truth | `validator passed != semantic conclusion is true` | `REPOSITORY_VERIFIED_GENERALIZATION` | Campaign product model |
| Multiple execution harnesses | Harness-neutral Campaign core with planned adapters | `CONCEPTUAL_PARALLEL`, P10 planned | v0.3 P10 |
| Optimizer-generated edits | No automatic Skill mutation in Campaign | `NOT_ADOPTED` | Campaign non-goals |
| Epoch / learning-rate optimization | No Campaign epoch or edit-rate optimizer | `NOT_ADOPTED` | Campaign non-goals |
| Rejected-edit optimizer buffer | No production Skill-edit memory buffer | `DEFERRED` / `NOT_ADOPTED` for v0.3 | none |
| Automatic Skill ranking | Explicitly excluded | `NOT_ADOPTED` | Campaign/v0.3 non-goals |
| SkillOpt-Sleep nightly self-evolution | No automatic harvest/replay/consolidate loop | `NOT_ADOPTED` | Campaign/v0.3 non-goals |
| Human review before adopting staged changes | Compatible with Sensemaking's explicit authority boundary | `CONCEPTUAL_PARALLEL` | authority model / future optional laboratory |

## 6. Empirical Skill Qualification adaptation

The strongest SkillOpt-derived work in Sensemaking was **not** the Campaign runtime. It was the attempted Empirical Skill Qualification v1 research program.

### 6.1 Adapted loop

The Sensemaking research design translated the optimization problem into:

```text
frozen baseline Skill
        ↓
D diagnostic evidence
        ↓
defect attribution
        ↓
fresh holdout freeze
        ↓
one bounded candidate OR NO_SKILL_CHANGE
        ↓
blind baseline-vs-candidate Q
        ↓
only if Q == IMPROVED: unopened T
        ↓
qualified classification + claim ceiling
        ↓
separate promotion authority
```

This is **not** identical to SkillOpt's optimizer loop.

Sensemaking added stricter governance concerns that are native to this repository:

- explicit authorization per execution stage;
- exact framework / Skill / target / validator identity;
- durable experiment accounting;
- candidate-author vs holdout-custodian separation;
- no hidden retries or repair;
- non-scalar candidate classification;
- explicit claim ceilings;
- automatic merge/adoption prohibited;
- `NO_SKILL_CHANGE` permitted as a valid diagnostic outcome.

### 6.2 Holdout discipline

PR #273 pre-registered a fresh-context holdout protocol in which:

- the candidate-author context could see D but not substantive Q/T cases before candidate freeze;
- a fresh holdout-custodian context would freeze exact Q/T manifests before candidate text existed;
- accidental Q/T leakage would invalidate the candidate cycle rather than cause silent regeneration;
- T would remain unopened unless Q was exactly `IMPROVED`;
- the claimed isolation was procedural/process isolation, not cryptographic secrecy.

This is a concrete Sensemaking adaptation of held-out candidate evaluation, made stricter around agent-context contamination.

### 6.3 Bounded candidate discipline

The planned candidate budget was deliberately small:

```text
max target Skills:        1
max modified files:       1
max instruction regions:  2
full Skill rewrite:        prohibited
automatic adoption/merge:  prohibited
```

The purpose was to make a candidate attributable and falsifiable rather than to maximize the chance that an optimization cycle "succeeds."

### 6.4 Actual experiment disposition

The research did **not** complete a candidate qualification cycle.

Current `STATUS.md` preserves the actual ceiling:

- three D attempts were preserved;
- Q/T holdout identity was frozen;
- a candidate-context contamination audit occurred;
- no candidate had been authored before the contamination event;
- no substantive Q/T candidate execution was completed;
- the program stopped under the owner productization pivot.

Therefore this record must **not** claim:

- Empirical Skill Qualification was empirically validated as an improvement system;
- a candidate Skill improved `repo-sensemaker`;
- Q/T generalization succeeded;
- the optimizer/qualification mechanism should be productized.

The correct claim is narrower:

> SkillOpt-inspired evaluation discipline was translated into a rigorous Sensemaking qualification design, and parts of that design were exercised, but the full candidate-qualification hypothesis was not completed.

## 7. Ideas generalized into the product

Some lessons from the SkillOpt comparison became useful beyond Skill optimization. These are best described as **generalized influences**, not direct copies.

### 7.1 Exact identity before acceptance

Skill optimization requires knowing which candidate is being evaluated.

Sensemaking generalized the same discipline across engineering artifacts and releases:

```text
exact candidate
→ exact validation evidence
→ exact acceptance boundary
```

Current examples include:

- exact-head CI qualification before merge;
- candidate invalidation after any post-qualification change;
- content-addressed admitted artifacts;
- admission receipts binding exact bytes to exact validator identity/results.

This practice also has independent origins in Sensemaking's own release-qualification and provenance work. SkillOpt should therefore be treated as **reinforcing influence**, not exclusive provenance.

### 7.2 Existence is not epistemic acceptance

The candidate-vs-accepted distinction generalizes cleanly:

```text
new Skill candidate
!= improved Skill
```

and in P4:

```text
file exists
!= validated artifact
!= admitted campaign evidence
```

Both express the same broad rule: **mere production of an artifact does not grant it epistemic status**.

### 7.3 Mechanical evaluation is not semantic truth

SkillOpt's gate evaluates candidate performance under a defined benchmark/evaluation contract.

Sensemaking generalizes the caution further:

```text
validator passed
!= semantic conclusion is true
```

A validator can establish that a representation or measured condition passed its contract. The active agent still interprets what that evidence means for the engineering decision.

### 7.4 Portability across harnesses

SkillOpt demonstrates that Skill artifacts and evaluation can be exercised across multiple harnesses.

Sensemaking independently requires its Campaign model to survive changes in coding-agent environments. P10 therefore plans adapters for Claude Code, Codex, OpenCode, and generic agent environments while keeping harness-specific semantics outside the Campaign core.

This is a `CONCEPTUAL_PARALLEL`, not a claim that P10 is copied from SkillOpt.

## 8. The Skill-quality laboratory vs the Campaign product

The permanent architectural separation should be:

```text
                    Sensemaking Skills
                           │
              ┌────────────┴────────────┐
              │                         │
              ▼                         ▼
     Sensemaking Campaign       Skill-quality laboratory
       product control            optional research
          substrate                  mechanism
              │                         │
      durable engineering        baseline / candidate
      state + decisions          holdout qualification
      evidence + authority       contamination controls
      transitions + handoff      comparative evidence
```

Therefore:

```text
Skill-quality laboratory
!= Campaign control loop
```

The Campaign should not automatically optimize the Skills it uses.

The Campaign is responsible for making engineering judgment durable and reconstructible. A Skill-quality laboratory, if invoked at all, is a separate bounded responsibility for testing whether a Skill change is actually warranted and better.

## 9. Deliberately not adopted into v0.3

The current product deliberately excludes the defining automation mechanisms of SkillOpt.

### 9.1 No optimizer model in the Campaign loop

The Campaign does not observe work, generate Skill patches, and promote them automatically.

### 9.2 No automatic Skill mutation

`docs/sensemaking-campaign.md` explicitly lists self-modifying Skills and autonomous SkillOpt loops among the product's non-goals.

### 9.3 No epoch-driven optimization

Sensemaking v0.3 does not introduce:

- epochs;
- learning-rate/edit-rate schedules;
- automatic slow/meta updates;
- optimizer-maintained rejected-edit buffers;
- automatic benchmark-driven Skill promotion.

### 9.4 No SkillOpt-Sleep-style autonomous nightly cycle

Sensemaking does not currently:

```text
harvest agent sessions
→ mine repeated tasks
→ replay them
→ mutate Skills
→ gate candidates
→ stage nightly Skill updates
```

Such a system might be useful someday, but it is not required for the Campaign product and should not be built merely because the mechanism exists elsewhere.

### 9.5 No automatic Skill ranking or semantic routing

Even if multiple capabilities are available, Sensemaking preserves:

```text
warranted responsibility
!= available capability
!= authorized capability
```

An optimizer score or capability registry must not silently become product-level semantic routing.

## 10. Optional future integration — not a roadmap commitment

A future integration could be compatible with the Campaign architecture **only if the active agent explicitly warrants Skill improvement as a separate responsibility**.

A safe conceptual path would be:

```text
ordinary Campaign evidence
        ↓
agent identifies a recurring Skill-specific defect
        ↓
agent explicitly selects Skill-improvement responsibility
        ↓
separately authorized Skill-quality laboratory
        ↓
bounded candidate
        ↓
independent held-out qualification
        ↓
explicit promotion authority
        ↓
new Skill revision, if warranted
```

This has two important properties:

1. real engineering pressure creates the reason to improve the Skill;
2. optimization machinery never owns the top-level Campaign decision loop.

This is a **future option**, not part of P5, not required for v0.3, and not permission to restart EXP-0006 automatically.

## 11. Relationship to the current v0.3 roadmap

The active roadmap remains:

```text
P0–P4  merged
P5     agent-authored decisions — CURRENT
P6     capability registry
P7     handoff/resume
P8     artifact/evidence lineage
P9     reconciliation lifecycle
P10    harness adapters
P11    v0.3 qualification/release
```

SkillOpt-derived Skill-quality machinery is **not inserted into this sequence**.

In particular:

- P5 does not optimize Skills;
- P6 does not rank Skills automatically;
- P8 lineage does not imply optimizer training data;
- P10 harness adapters do not imply SkillOpt execution;
- P11 does not require autonomous Skill evolution.

If later product evidence warrants a Skill-quality product feature, it should receive its own owner decision, scope, authority boundary, and qualification plan.

## 12. Non-goals of this document

This record does not:

- claim Sensemaking implements SkillOpt;
- claim SkillOpt is the sole intellectual source of Sensemaking's validation discipline;
- claim code was copied from SkillOpt;
- revive or authorize EXP-0006;
- expose substantive Q/T holdout content;
- claim Empirical Skill Qualification succeeded;
- authorize a candidate Skill;
- add a Skill ranking algorithm;
- add autonomous Skill mutation;
- change Campaign semantics;
- change P5 scope;
- create a new ADR.

## 13. Claim ceiling

The strongest supported synthesis is:

> Sensemaking Skills used SkillOpt as an important methodological influence when designing a stricter empirical Skill-qualification approach. The adaptation emphasized exact candidate identity, bounded changes, held-out evaluation, context separation, fail-closed qualification, and no automatic promotion. That research program stopped before a complete candidate Q/T qualification cycle. Several broader lessons are now reflected in Sensemaking's product discipline—especially exact identity, gated evidence admission, and separation of mechanical validation from semantic judgment—but those generalized product mechanisms also have independent Sensemaking provenance. The current Sensemaking Campaign deliberately does not include SkillOpt's autonomous optimizer or nightly self-evolution loop.

Anything stronger requires new historical or empirical evidence.

## 14. Source map

### External SkillOpt

- Microsoft SkillOpt repository, pinned revision `79124b37e9a6371e13b753f8bcd7adb1e493ade1`
- `README.md` — skill-as-trainable-state overview, bounded edits, held-out validation, rejected-edit buffer, slow/meta updates, harness results
- `docs/index.md` — rollout/reflection/aggregate/select/update/gate pipeline and deep-learning analogy
- `docs/sleep/README.md` — deployment-time harvest/mine/replay/consolidate/gate/stage/adopt flow and human-adoption boundary

### Sensemaking current product

- [`../sensemaking-campaign.md`](../sensemaking-campaign.md)
- [`../productization-v0.3.md`](../productization-v0.3.md)
- [`../../STATUS.md`](../../STATUS.md)
- [`../artifact-ingestion.md`](../artifact-ingestion.md)

### Sensemaking historical research

- [PR #273](https://github.com/ThorStarlord/sensemaking-skills/pull/273) — Empirical Skill Qualification v1 preregistration and bounded candidate/holdout contract
- [PR #276](https://github.com/ThorStarlord/sensemaking-skills/pull/276) — EXP-0006 diagnostic results workspace; closed unmerged under productization pivot

Historical research PRs are evidence of what was designed/exercised at the time. They are not current runtime/product authority.
