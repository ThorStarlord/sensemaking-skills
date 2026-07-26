# Owner-Facing Product-Contract Review

**Date**: 2026-07-26
**Trigger**: closure of the auteur external-validation campaign (PR #67, #69,
#70, #72, #73, #75, #77, #78; final state: `main@8fd58f7`, PR #78 = last
authorized rerun, Stage A `BRIEF VALIDATION FAILED` on `UNKNOWN_WEAKNESS_TYPE`)
**Nature of this document**: decision-analysis input for the repo owner. It
does not change any ADR status, close/open/edit any GitHub issue or PR, alter
any validator or prompt, merge any evidence PR, or claim production readiness.
Every recommendation below is a recommendation pending explicit owner
sign-off. No auteur rerun, no live model workflow, no implementation was
performed to produce this document.

---

## 0. Campaign result, stated plainly

Four external-repo attempts against `auteur`, three real bugs found and fixed,
zero successful end-to-end external golden-path proofs:

| PR | Failure | Root cause | Fixed by |
|---|---|---|---|
| #67 | `HALLUCINATED_FILE` on 4 real files | validator resolved citations against framework repo, not target repo | #69 |
| #70 | `NO_LOGIC_TRACE`, `EVIDENCE_EXCERPT_FIELD` x9 | live prompt never named the required evidence sub-fields or the "Logic trace:" marker | #72 |
| #73 | Stage A passed structurally; substantive audit found an unsupported "ghost feature" claim (no contradiction search) | prompt didn't require disconfirmation search before absence claims | #75 (+ #77 trace v2 to make this auditable) |
| #78 | `UNKNOWN_WEAKNESS_TYPE` | model wrote a specific, well-cited weakest-boundary claim ("acceptance subsystem integration") that never used one of the 7 registered vocabulary terms verbatim | **not fixed — campaign stopped by design** |

Every fix found so far has been a validator/prompt scoping bug, not a
reasoning failure. PR #78's own evidence states the model performed genuine
contradiction search (PR #75's fix held) and produced a falsifiable, cited
claim — it just didn't recite one of seven fixed strings. No merged evidence
anywhere shows a full Stage A→B→C→D pass against an external repository.
ADR 0021's "internally proven, externally unvalidated" framing is unchanged.

---

## Part 1 — Product boundary

### The five interpretations, evaluated against actual repo state

**A. Repository-analysis assistant producing a human-reviewed brief**
- *Supports*: `repo-sensemaker` → `repository_sensemaking_brief.md` is the
  only artifact stage that has ever passed live against an external repo (PR
  #73, structurally). Designed to be read by a human or downstream skill, not
  executed directly.
- *Missing*: nothing — this is the subset of the product proven to work.
- *Validators sensible for this product*: mostly yes. The one rule that
  doesn't fit "human-reviewed brief" framing is `UNKNOWN_WEAKNESS_TYPE` (Part
  3).
- *Was the campaign testing the right thing*: yes — every campaign failure so
  far is inside this single artifact's production path.

**B. Validated artifact-production pipeline (brief → plan → downstream, machine-gated)**
- *Supports*: the proven golden path (ADR 0014's evidence note) is intent →
  repo-sensemaker → brief → architectural-review Step 2 → recommendation →
  run log → exit 0, for exactly one workflow
  (`architectural-review-planning-workflow`), proven only on this repository,
  never externally end-to-end.
- *Missing*: the external leg never got past Stage A on any of 4 attempts.
  Stage B/C/D have zero external evidence — every external attempt stopped at
  Stage A by design.
- *Validators sensible*: yes in principle, but 3 of 4 Stage-A failures were
  the validator/prompt being wrong, not the pipeline concept.
- *Right thing tested*: yes — this is exactly the interpretation ADR 0021
  says is unvalidated; it just hasn't succeeded yet.

**C. Workflow router + artifact pipeline**
- *Supports*: `workflow-planner` and the registry exist and are exercised
  internally.
- *Missing*: no external evidence the router picks correctly across
  differently-shaped repos — routing was never reached externally.
- *Validators*: routing-field contract tests are solid, unrelated to this
  campaign's failures.
- *Right thing tested*: no — routing was never reached.

**D. Pre-implementation planning system**
- Same evidence as B, narrower framing (stops at a recommendation). This is
  what ADR 0014 already proposes. No new evidence changes that framing.

**E. Semi-autonomous software-development orchestrator**
- *Supports*: none. No PR shows the system writing/reviewing/merging code or
  acting on a third-party tracker.
- *Missing*: everything beyond artifact production.
- *Right thing tested*: no — never on the table for this campaign.

### Recommendation

**Adopt interpretation A, narrowly, as the settled scope for the next
phase**: a repository-analysis assistant that produces a validated,
human-reviewed brief — not B. Every failure in this campaign happened inside
brief production, before routing or a second workflow step was reached
externally. Claiming B (or ADR 0014's current framing, which already
includes routing) as the settled boundary now would claim more than the
evidence shows twice in a row. B/D remain the aspirational next boundary once
brief production clears an external repo end-to-end.

Recommend ADR 0014 stay **Proposed**, with its "in scope" section narrowed to
brief production only, until an external repo clears Stage A.

---

## Part 2 — Field classification for `repository_sensemaking_brief`

| Field | Current owner | Recommended owner | Validation method | Human review required |
|---|---|---|---|---:|
| Artifact metadata (`artifact_id`, `created_at`, `created_by`, `immutable`) | runtime-deterministic | unchanged | `validate-artifact.py` generic schema check | No |
| Workflow ID (`recommended_workflow_id`) | model-generated, validator-constrained | unchanged | exact-match against `workflow-registry.yaml` (`HALLUCINATED_WORKFLOW_ID`) | Yes (routing decision) |
| Fog type (`primary_fog_type`) | model-generated, validator-constrained | unchanged | contract-declared enum check | Yes (routing decision) |
| **Weakness type** | **not a field — inferred by substring match over free prose** | **promote to a dedicated controlled-vocabulary field** (Part 3) | currently: substring match; recommended: enum match on a real field | Yes either way |
| Weakest-boundary prose | model-generated, human-reviewed | unchanged | required-section presence only | Yes |
| Evidence excerpts (`evidence_excerpts` block) | controlled-vocabulary deterministic (structure) / model-generated (content) | unchanged | YAML-parse + per-field presence (`EVIDENCE_EXCERPT_FIELD`) | Spot-check |
| `quote` | model-generated, validator-constrained (presence only) | unchanged | presence + non-empty | Yes (truthfulness not validator-checkable) |
| `supports_claim` | model-generated, validator-constrained (presence only) | unchanged | presence + non-empty | Yes |
| Logic trace | model-generated, validator-constrained (marker-phrase presence) | unchanged | substring check for "logic trace" | Yes |
| Recommended workflow | see workflow ID | — | — | — |
| Next action / recommendation prose | model-generated, human-reviewed | unchanged | required-section presence only | Yes |

Consistent with ADR 0015 except weakness type, which has no dedicated field —
inferred from prose via substring match, neither honestly
"controlled-vocabulary deterministic" (no field exists) nor
"model-generated, human-reviewed" (a validator silently gates on it anyway).

---

## Part 3 — The weakness-type contract, end to end

**Vocabulary**: 7 fixed terms (`skills/repo-sensemaker/references/weakness-types.md`):
Vocabulary Drift, Contract Mismatch, Ghost Features, Safety Gaps, Implicit
Dependencies, Zero Validation, Orphaned Examples.

**Supplied to model**: via `build_semantic_authorities_block` injection
(established PR #59; PR #78 confirms the list is in fact injected — the model
just didn't use one exact string).

**Where it appears in the artifact**: nowhere as a field, only inside the free
"Weakest boundary" prose section.

**Validator detection** (`scripts/validate-brief.py:279-286`):
```python
weakest_boundary = sections.get("weakest boundary", "")
if weakest_boundary and weakness_types:
    if not any(kind.lower() in weakest_boundary.lower() for kind in weakness_types):
        errors.append(_code_error(UNKNOWN_WEAKNESS_TYPE, ...))
```
Substring matching over free prose — exactly the class of check ADR 0015 says
should not exist, and the same anti-pattern CLAUDE.md already documents once
for the `Lx`-only citation format, recurring in a second field.

**Dedicated machine-readable field**: none.

**Can prose and classification disagree?** Yes — PR #78 is a live instance:
"acceptance subsystem integration" (a specific, cited claim about
`ReviewService.accept()`) arguably fits Ghost Features or Implicit
Dependencies, but the model chose its own more precise phrase and the
validator can't see a classification because there isn't one.

**Must every real weakness fit exactly one registered type?** No — this is an
unforced assumption. A 7-item closed taxonomy for arbitrary repository
weaknesses is more likely to be underinclusive than the model is likely to be
imprecise about bucket choice. PR #78's own evidence calls this "brittle to
paraphrase."

### Option evaluation

| Option | Determinism | Validator simplicity | Semantic accuracy | Model compliance risk | Taxonomy brittleness | Human interpretability | Routing compatibility | Migration cost | Failure behavior |
|---|---|---|---|---|---|---|---|---|---|
| **A — exact term in prose** (current) | Low (string match on free text) | High (already shipped) | Low — forces prose to serve two masters | High — 2 of 4 campaign failures are this family (#70's field-naming, #78's vocabulary) | High — closed taxonomy, no escape hatch | Medium — the string is buried in a paragraph | None (nothing downstream reads it) | Zero | Hard-fails structurally valid, well-cited output |
| **B — dedicated structured field** | High (enum-validated field, like `primary_fog_type`) | High (identical pattern already proven for fog type) | High — field is classification, prose is explanation, independently checked | Low — model fills one clear field instead of hiding a keyword in prose | Medium — still closed 7-term enum, but decoupled from prose wording | High — field is scannable, prose still readable | High — a real field a router/report can read | Low-medium — contract + skeleton + prompt update, same pattern as PR #72 | Fails only if field is absent/invalid, not if prose paraphrases |
| **C — runtime-derived classification** (deterministic post-processor maps prose → type) | Medium — deterministic code, but classifying open-ended prose deterministically is itself brittle (reintroduces keyword/regex matching one layer down) | Medium — new code to write and maintain | Medium — a classifier can't understand nuance the model already expressed correctly | Low for the model, but shifts risk to the classifier's brittleness | High — the classifier has the same closed-taxonomy problem as Option A, just moved | Medium — a human still has to trust the post-hoc mapping | Medium | Medium-high — new component to build, test, and maintain | Silent misclassification is a worse failure mode than a loud validator error |
| **D — multi-label taxonomy** (primary + zero-or-more secondary types) | High if implemented as structured fields | Medium — validator must check a list, not a scalar | High — matches reality better (PR #78's own diagnosis: two terms "arguably fit") | Low | Lower — reduces forced-choice brittleness | Medium — more fields to read | High | Medium — larger contract change than B | More forgiving, but adds ambiguity about what "primary" means downstream |
| **E — advisory taxonomy** (metadata, non-blocking) | Same as B structurally, but validator never fails on it | High | High | None — cannot block on it | Low — no forced choice needed since it can't block | High | Medium — a router could still prefer classified briefs | Low | Never blocks; a brief with no/`Other` classification still passes |

### Recommendation

**Option B**, with the specific rule from Option E for the failure mode: a
dedicated `weakness_type` field, enum-validated, but **not yet a hard
required/blocking field** — i.e., B's structure with E's non-blocking
severity until a real downstream consumer is named. Concretely:
1. Add `weakness_type` to `artifact-contracts.yaml` for
   `repository_sensemaking_brief` as a `recommended_machine_field` (enum: the
   7 existing terms + `Other`).
2. Retire `UNKNOWN_WEAKNESS_TYPE` as a hard failure on the *prose* substring
   check — a validator change, therefore **not** performed by this review;
   a recommendation for a follow-up PR.
3. Defer Option D (multi-label) and Option C (runtime classifier) — D adds
   real value (PR #78 shows two terms "arguably fit") but is more contract
   surface than needed for the first fix; C relocates brittleness rather than
   removing it and should not be pursued at all unless B is shown
   insufficient.

This recommendation is not self-executing: no validator, prompt, or contract
file is modified as part of this review.

---

## Part 4 — Evidence policy

**Layer-by-layer, from ADR 0016 / PR #73 / #75 / #78**:

| Layer | Checkable deterministically? | By a second model? | By a human? | Only via real-world use? |
|---|---|---|---|---|
| 1. File exists | Yes (`HALLUCINATED_FILE` check, PR #69-fixed) | — | — | — |
| 2. Line range exists | Yes (regex grammar check, PR #54's `evidence-rules.md` hardening) | — | — | — |
| 3. Quote matches file content | Partially — a diff/grep check could verify a quote's substring exists at/near the cited range; **not currently implemented** | Yes, cheaply | Yes | — |
| 4. Quote supports the local claim | No — requires semantic judgment | Yes (a second model can flag non-sequiturs) | Yes (final authority) | — |
| 5. Stronger repo evidence doesn't contradict the claim | No — this is exactly what PR #75's contradiction-search discipline asks the *producing* model to do, but a validator can't verify a negative search was exhaustive | Yes (a second model can attempt its own contradiction search) | Yes | Partially — repeated real use surfaces missed contradictions over time |
| 6. Weakest-boundary conclusion is useful/appropriately scoped | No | Yes, weakly | Yes | Yes — this is fundamentally a usefulness judgment |
| 7. Recommendation suitable for downstream work | No | Yes, weakly | Yes | Yes |

**Recommended evidence policy for the next phase**:
- Layers 1–2 stay deterministic validator checks (already correct, already
  hardened by PR #54/#69).
- Layer 3 (quote-matches-file) is a **new, cheap, deterministic check worth
  adding**: verify the cited quote is a substring of the file at/near the
  cited line range. This is mechanical, not semantic, and directly prevents a
  cheap class of fabrication (citing a real file/line but an invented quote)
  that no current validator catches.
- Layers 4–5 (semantic support, contradiction-completeness) are **not**
  validator-checkable and should not be forced into one — this is the exact
  mistake `UNKNOWN_WEAKNESS_TYPE` already makes for taxonomy; don't repeat it
  for evidence semantics. These belong to the substantive audit (human or a
  structured second-model review), not the structural validator.
- Layers 6–7 (usefulness, downstream suitability) are only really answered by
  real maintainer use — no amount of pre-production audit substitutes for
  this, consistent with ADR 0021's already-correct framing that production
  readiness needs real use, not just structural proof.

**Explicit rules**:
- **Executable code vs. comments/docstrings**: authority hierarchy already
  exists and is sound (PR #75/#54: code/tests > contracts/registries >
  accepted ADRs > canonical docs > open issues/proposed ADRs > historical
  status docs > untracked drafts). No change recommended.
- **Negative/absence claims**: require the PR #75 contradiction-search
  discipline (search for direct implementations, symbol/enum usages,
  reachable callees, and deliberately search for falsifying evidence) —
  already shipped and exercised live in PR #78's trace. No change
  recommended.
- **Contradiction searches**: should be recorded in the logic trace (already
  required per PR #75); recommend this remain a documentation requirement,
  not a separately validator-checked one, since completeness of a search
  cannot be mechanically verified (layer 5 above).
- **Uncertainty**: the model should downgrade to stated uncertainty when a
  contradiction search cannot be completed — already part of PR #75's
  fix. No change recommended.
- **Stale planning documents**: covered by the same authority hierarchy
  (historical status docs rank below code/tests/current docs). No change
  recommended.
- **External-repository citations**: require `target_repo`-aware path
  resolution (PR #69) — already fixed and should remain the standard for any
  future cross-repo run.
- **Evidence-audit requirement**: see below.

**Should the independent substantive audit be mandatory for every brief,
mandatory only for absence/high-risk claims, optional during development, or
replaced by another mechanism?**

Recommend: **mandatory only for absence/high-risk claims** (ghost-feature,
dead-code, unreachability, missing-validation claims — i.e. exactly the class
PR #75 already flags for contradiction-search discipline), not for every
brief. Rationale: layers 1-3 are cheap and can run on every brief via the
validator; layers 4-7 require human or second-model judgment and don't scale
to every run, but absence claims are specifically the highest-risk claim type
(PR #73 is direct evidence: a structurally valid brief carried an
unsupported absence claim) and warrant the audit every time. This is not
"optional during development" — PR #73 shows skipping it in early campaign
stages let a real defect through; it's targeted-mandatory, scoped to the
claim type most likely to be wrong.

---

## Part 5 — Readiness definition

| Readiness level | Required proof | Current status |
|---|---|---|
| Experimental | Any live run producing a structurally-checkable artifact | **Met** — PR #52 onward |
| Internally proven | Full golden path (Step 1 + Step 2, positive AND negative) live on this repository, for at least one workflow | **Met** — PR #57, #59, #60, #62, #64, #65 (`architectural-review-planning-workflow`) |
| Externally exercised | At least one live run attempted against a genuinely external repository, whether or not it passes, with target-immutability and safety controls verified | **Met** — PR #67/#70/#73/#78, all confirm target immutability and safety-control holding even on failure |
| Externally validated | At least one live external run reaches a structurally valid, substantively-audited artifact through Stage A **and** Step 2 (positive path) | **Not met** — 0 of 4 attempts passed Stage A cleanly; none reached Step 2 externally |
| Limited production (pilot) | Externally validated, PLUS repeatability across more than one external repository, PLUS at least one instance of unprompted maintainer usefulness (a human other than the campaign author finding the output actionable) | **Not met** — depends on the level above |
| Generally production-ready | Limited production, PLUS defined failure-rate expectations across repos/models, PLUS multi-provider/platform coverage commitments, PLUS cost/concurrency policy (ADR 0021's named owner-decision items) | **Not met** |

**Additional specifics**:
- Internal Step 1: met. Internal Step 2 positive/negative: met (PR #65).
- External Step 1 structural validity: **not met** — 0/4 (closest was PR #73,
  which passed structurally but failed substantive audit; PR #78's failure
  was structural).
- External substantive correctness: **not evaluated** — never reached (every
  attempt stopped at or before the substantive-audit gate except #73, which
  failed it).
- External Step 2: **never attempted** — no external run reached Stage A
  cleanly enough to proceed.
- Target immutability: **met, repeatedly** — confirmed across all 4 attempts
  via git-status, tracked-file manifests, and (from PR #77 onward)
  PreToolUse/PostToolUse pairing analysis.
- Usefulness to maintainers: **not evaluated** — no maintainer outside the
  campaign has used an output.
- Repeatability: **partially evidenced** — the same class of bug (evidence
  contract naming, then taxonomy vocabulary) recurring across attempts is
  itself a repeatability signal, but not the good kind; no repeat *success*
  exists yet.
- More than one external repository: **not met** — only `auteur` has been
  used.
- Model/provider/platform coverage: **not evaluated** — every run used the
  same executor/model configuration.
- Failure-rate expectations: **not defined** — an explicit owner decision
  per ADR 0021.
- Human-review requirements: **defined for the brief artifact** (Part 2),
  **not yet defined** as a product-wide policy for what "production" review
  looks like.

**Highest currently justified readiness level: "Externally exercised."**
Not "externally validated" — that requires a passing Stage A + Step 2, which
has not happened in 4 attempts.

---

## Part 6 — Interpreting the auteur campaign

| PR | What it falsified | What it improved | Category | Boundary or contract? |
|---|---|---|---|---|
| #67 | Falsified the assumption that citation validation was topology-agnostic (repo-root vs. target-repo) | Fixed a real path-resolution bug (#69) | Implementation defect | Contract only — the evidence policy (ADR 0016) was right, the code enforcing it had a bug |
| #70 | Falsified the assumption that the live prompt already explained the evidence-excerpt schema | Fixed prompt to name required fields and the logic-trace marker (#72) | Process gap (prompt didn't teach its own contract) | Contract only |
| #73 | Falsified the assumption that structural validity implies substantive correctness | Added contradiction-search discipline (#75) and trace v2 observability (#77) to make this auditable at all | Product-contract problem — this is the most important finding: structural pass was insufficient evidence, exactly the class of error CLAUDE.md's "Done requires running the real path" rule warns about | Both — it changed what "passing" should require (contract), and confirmed the underlying diagnosis capability itself is sound once evidence discipline is enforced (not a boundary problem) |
| #78 | Falsified the assumption that the taxonomy-substring check is a reasonable proxy for classification quality | Nothing new fixed (campaign stopped by design); the *diagnosis* itself is the deliverable | Product-contract problem, not a model limitation — trace evidence shows genuine contradiction search and a specific, falsifiable, well-cited claim | Contract only — this is a validator/taxonomy-representation defect (Part 3), not evidence the product's scope or the model's reasoning is unsound |

**Was `UNKNOWN_WEAKNESS_TYPE` a legitimate rejection under the intended
product?** Under the *product as currently specified* (a validator requiring
exact vocabulary), yes, technically legitimate — the rule fired as written.
Under the *product's actual intent* (validate that the model correctly
identified a real, well-supported weakness), no — the rejection is a false
negative on a substantively sound artifact, which is the brittle-taxonomy
problem, not a legitimate quality gate.

**Did the run provide enough evidence to judge the substantive
`ReviewService.accept()` claim?** No. The evidence (completed, non-trivial
Grep/Read searches against real symbols in `auteur`) is consistent with a
genuine investigation, but the mandatory substantive audit was never reached
— Stage A failed on the unrelated vocabulary check first. This review does
not judge whether the `ReviewService.accept()` claim is true; that
determination requires the substantive audit this campaign correctly refused
to skip.

**What claims remain prohibited?** No claim that the external golden path is
proven, validated, or successful. No claim that `ReviewService.accept()`'s
gap is confirmed (the substantive audit never ran). No claim of production
readiness at any level beyond "externally exercised" (Part 5). PR #78 is not,
and must not be reinterpreted as, a successful external validation.

---

## Part 7 — Disposition of current open work

| Item | Recommended disposition | Why |
|---|---|---|
| #27 (Wayfinder parent map) | **Active** — remains the correct parent tracking issue; its own stated principle ("fix the spine before adding breadth") is exactly what this review reinforces | Nothing here is superseded; the campaign is evidence *for* its own standing principle |
| #29 (product boundary) | **Active** — narrow ADR 0014's scope per Part 1 before accepting | Evidence supports A, not the broader B/D framing currently drafted |
| #30 (deterministic vs. model-variable fields) | **Revise** — add the weakness-type field-classification gap (Part 2/3) as an explicit sub-item; otherwise ADR 0015's mechanics are sound | Taxonomy is right; one field was never classified into it |
| #31 (evidence policy) | **Active, largely settled** — ADR 0016's mechanics held up again (PR #75/#78); owner sign-off on "which claims require evidence" is the only remaining open item; add Part 4's quote-verification (layer 3) recommendation as a sub-item | No new evidence contradicts ADR 0016; one cheap deterministic gap identified |
| #32 (readiness criteria for new features) | **Owner decision required** — blocks #36; unaffected by this campaign directly but its resolution is a prerequisite | Not evaluated in this review's scope |
| #33 (workflow-routing policy) | **Hold** — depends on #29 narrowing first (ADR 0014's consequences section says so directly) | Routing was never reached by this campaign; nothing new to decide yet |
| #34 (findings → tracker tasks) | **Hold** — same dependency on #29 | Out of this campaign's scope entirely |
| #35 (Wayfinder/prototypes scope) | **Hold** — explicitly deferred pending #29 per ADR 0014's own consequences section | Unaffected by this campaign |
| #36 (production-readiness) | **Held** — do not unblock until #29/#30 narrow; ADR 0021's checklist stands, external-repo criterion still unmet after 4 attempts | Unblocking now would let a readiness claim ride on an unresolved boundary question |
| PR #52 (live golden-path proof attempt, run 0002) | **Preserve as historical evidence** | Real, valuable evidence of the *first* live Step-1 failure class (workflow-ID/skill-ID confusion, line-format grammar) — do not merge (it's evidence-only), do not delete |
| Issue #53 / PR #54 (align live prompt with brief validator contract) | **Preserve as historical evidence / already-landed fix** | #54 already merged the producer-side fix for #53's diagnosed gap; #53 itself should stay open only if some sub-item of it is still unaddressed — recommend owner confirm closure eligibility directly (this review does not close it) |
| PR #67 (experiment 0009, external Stage A, citation bug) | **Preserve as historical evidence** | Do not merge; first documented instance of the target-repo citation bug, root cause for #69 |
| PR #70 (experiment 0010, external rerun, evidence-field bug) | **Preserve as historical evidence** | Do not merge; root cause for #72 |
| PR #73 (experiment 0011, external rerun 2, unsupported claim) | **Preserve as historical evidence** | Do not merge; root cause for #75/#77; single most important campaign finding (Part 6) |
| PR #78 (experiment 0012, final rerun, `UNKNOWN_WEAKNESS_TYPE`) | **Preserve as historical evidence** | Do not merge; the direct trigger for this review and for Part 3's recommendation |

No issue or PR is recommended for closure as superseded. This review performs
no mutation of any GitHub item.

---

## Part 8 — Proposed next phase

**Recommended: Option A — Contract redesign and deterministic taxonomy
fields** (not C, a fifth external repo; not E, broader workflow
implementation; not D, consolidation-only).

Rationale for rejecting the alternatives: rerunning against `auteur` or a new
repo (Option C) before fixing the diagnosed taxonomy brittleness risks a 5th
failure in the same bug family the campaign has now twice implicated
(evidence-field naming, then vocabulary matching) — that would produce
evidence about validator debt, not product readiness, and burns another live
external-repo cycle for a predictable, already-diagnosed reason. A human-
reviewed pilot (Option B) is attractive but premature until the boundary
(#29) and taxonomy contract (#30) are actually settled by the owner — piloting
against an unsettled contract just produces more of the same "what should the
contract have been" evidence this review already has enough of. Broader
workflow implementation (Option E) directly contradicts issue #27's own
standing principle ("fix the spine before adding breadth") and this review's
own Part 1 finding that routing has never been reached externally.
Consolidation-only (Option D) undershoots — there is a concrete, scoped,
low-risk contract fix identified (Part 3) that is worth doing before the next
external attempt, not merely documenting.

### Phase definition

- **Objective**: resolve #29 (product boundary) and #30 (weakness-type field
  gap specifically) via explicit owner sign-off, then implement the Option B
  structured `weakness_type` field (Part 3) plus the layer-3 quote-existence
  check (Part 4), with no validator regression.
- **Non-goals**: no new external-repo run; no routing/workflow-selection
  changes (#33 stays held); no tracker-sync or deployment work (#34/#35 stay
  held); no change to the contradiction-search discipline (#31/#75, already
  sound); no multi-label taxonomy (Option D) or runtime classifier (Option C)
  — deferred, not part of this phase.
- **Entry criteria**: owner sign-off on Part 1's recommended boundary (A,
  narrowed) and Part 3's recommended weakness-type option (B, non-blocking).
- **Exit criteria**: `weakness_type` field declared in
  `artifact-contracts.yaml`, skeleton/prompt updated to request it
  (mirroring PR #72's pattern), `UNKNOWN_WEAKNESS_TYPE` prose-substring check
  retired or downgraded to non-blocking, layer-3 quote-existence check added
  to `validate-brief.py`, `scripts/test-validators.py` green, one internal
  (this-repository) live re-run of `repo-sensemaker` confirming the new field
  round-trips and the old failure mode no longer blocks a substantively sound
  brief.
- **Maximum scope**: brief-artifact contract and its two validators
  (`validate-brief.py`, `validate-and-report.py`'s brief invocation path).
  Nothing in `workflow-planner`, `architectural-review`, or any other skill.
- **Expected artifacts**: an updated `artifact-contracts.yaml` entry, an
  updated `repo-sensemaker` skeleton/prompt, an updated `validate-brief.py`,
  a passing internal live re-run's evidence record (same evidence-preservation
  convention as `experiments/evidence/000x-*`), and ADR updates per the plan
  below.
- **Stopping rule**: if the internal re-run surfaces a new, different
  structural failure (as has happened twice already for unrelated reasons),
  stop and diagnose before proceeding to any external attempt — do not chain
  fixes without re-verifying live.
- **Issues activated**: #29 (resolved by sign-off), #30 (resolved for the
  weakness-type sub-item; other sub-items may remain open), #31 (the
  layer-3 quote-check sub-item resolved; the broader threshold question
  remains for owner sign-off separately).
- **Issues deferred**: #32, #33, #34, #35, #36 (all remain held/blocked per
  Part 7 until #29/#30 are actually ratified, independent of this phase's
  implementation work).

---

## Part 9 — Owner decisions

1. **What is the product boundary?** A (repository-analysis assistant
   producing a human-reviewed brief, narrowly) vs. B/D (validated pipeline
   including routing) vs. broader (C/E). *This review recommends A.*
2. **Is weakness type routing-critical or advisory?** Routing-critical (must
   gate artifact validity) vs. advisory (useful metadata, never blocks).
   *This review recommends advisory-severity, structured-field
   representation (Option B/E hybrid).*
3. **Must weakness type be explicit structured data?** Yes (dedicated field)
   vs. no (keep inferring from prose). *This review recommends yes.*
4. **Is substantive evidence audit mandatory for every brief, only for
   absence/high-risk claims, optional during development, or replaced by
   another mechanism?** *This review recommends: mandatory only for
   absence/high-risk claims.*
5. **What level of human review is part of the product?** Every brief
   reviewed before use vs. spot-check vs. none (fully autonomous consumption
   downstream). *Not settled by this review — genuinely an owner call with
   no repo evidence pointing to one answer over another.*
6. **What readiness level is the next target?** "Externally validated" (at
   least one clean external Stage A + Step 2 pass) vs. skip straight to
   "limited production" pilot-style validation. *This review recommends
   targeting "externally validated" next, after the Part 8 contract fix, not
   skipping ahead.*
7. **Should external success require one repo, multiple repos, or real
   maintainer use?** *Not settled by this review — the current campaign only
   ever tested one external repo (`auteur`), so no repo evidence
   distinguishes these options; this is a pure scope/cost decision for the
   owner.*

---

## Final deliverable summary

1. **Recommended minimal product boundary**: Interpretation A — repository-
   analysis assistant producing a validated, human-reviewed brief (Part 1).
2. **Field-ownership table**: Part 2.
3. **Weakness-type contract recommendation**: Option B (dedicated
   `weakness_type` enum field), non-blocking severity, `UNKNOWN_WEAKNESS_TYPE`
   prose-substring check retired (Part 3).
4. **Evidence-policy recommendation**: keep layers 1-2 deterministic, add a
   new cheap layer-3 quote-existence check, keep layers 4-7 as human/audit
   judgment (not validator-enforced); mandatory substantive audit scoped to
   absence/high-risk claims only (Part 4).
5. **Readiness-level model**: experimental → internally proven → externally
   exercised → externally validated → limited production → generally
   production-ready (Part 5 table).
6. **Highest currently justified readiness level**: **Externally exercised**
   (Part 5).
7. **Auteur-campaign interpretation**: 3 implementation/process fixes, 1
   unresolved product-contract defect (taxonomy brittleness); the single most
   important finding is PR #73's demonstration that structural validity does
   not imply substantive correctness (Part 6).
8. **Open-work disposition table**: Part 7.
9. **One recommended next phase**: Option A — contract redesign
   (`weakness_type` field + layer-3 evidence check), scoped narrowly, no new
   external-repo run until it lands (Part 8).
10. **Owner-decision checklist**: Part 9.
11. **Proposed ADR update plan** (recommendations only — no status changed by
    this review):
    - **ADR 0014** (product boundary): narrow "In scope" to brief production
      only; keep **Proposed** pending owner sign-off on the narrower framing.
    - **ADR 0015** (deterministic/model-variable fields): add an explicit
      addendum classifying `weakness_type` as a new controlled-vocabulary
      deterministic field once Part 8's phase lands; keep **Provisional**
      until then.
    - **ADR 0016** (evidence policy): add the layer-3 quote-existence check
      as a decision once implemented; keep **Provisional** — the
      "which claims require evidence" threshold sign-off is still the
      binding blocker, unaffected by this phase.
    - **ADR 0021** (production readiness): add this campaign's four PRs as
      supporting/missing evidence entries under the existing "internally
      proven, externally unvalidated" framing; no status change — remains
      **Proposed** with the external-repo gap still open (now with a
      documented, diagnosed reason for the latest failure rather than an
      undiagnosed one).
12. **Exact implementation prompt for the chosen next phase** (provided
    below; **not executed** as part of this review):

```markdown
Implement the weakness-type contract redesign approved by the owner
following the 2026-07-26 product-contract review
(docs/PRODUCT-CONTRACT-REVIEW-2026-07-26.md).

Scope: brief-artifact contract only. Do not touch workflow-planner,
architectural-review, or any other skill. Do not run a live external-repo
experiment as part of this work.

1. Add `weakness_type` to `skills/workflow-planner/references/artifact-contracts.yaml`
   under `repository_sensemaking_brief`, as a `recommended_machine_field`,
   enum-constrained to the 7 terms in
   `skills/repo-sensemaker/references/weakness-types.md` plus `Other`.
2. Update the runtime-owned skeleton (`scripts/brief_skeleton.py`) to
   pre-create a `weakness_type:` field alongside the existing
   `evidence_excerpts:` YAML block.
3. Update the live execution instruction (`build_semantic_authorities_block`
   in `scripts/skill_executor.py`) to explicitly name the `weakness_type`
   field and its enum, the same way PR #72 named `quote`/`supports_claim`.
4. In `scripts/validate-brief.py`, retire or downgrade the
   `UNKNOWN_WEAKNESS_TYPE` prose-substring check (lines ~279-286) to a
   non-blocking warning; add validation of the new `weakness_type` field
   (enum membership) as the authoritative check instead.
5. Add a new deterministic check: for each entry in `evidence_excerpts`,
   verify the `quote` text is a substring of the cited file at/near the
   cited line range (layer 3 from the evidence-policy review). Fail with a
   new, distinct error code (e.g. `EVIDENCE_QUOTE_MISMATCH`), not by
   repurposing an existing code.
6. Update `scripts/test-validators.py` fixtures to cover: a valid brief with
   `weakness_type` set correctly, one with a mismatched quote
   (`EVIDENCE_QUOTE_MISMATCH`), and one with a missing/invalid
   `weakness_type` value (warning, not hard failure).
7. Run `python scripts/test-validators.py` and `python scripts/validate-repo.py`
   clean.
8. Perform one internal (this-repository, not external) live re-run of
   `repo-sensemaker` to confirm the new field round-trips against real model
   output and that a substantively sound brief no longer fails on taxonomy
   wording alone. Record this as a new `experiments/evidence/0013-*` entry
   following the existing evidence-preservation convention.
9. Do not open a new external-repo campaign PR as part of this work. Do not
   change ADR statuses — file the ADR addenda proposed in this review's Part
   9(11) as draft text for owner review, not as accepted changes.
```
