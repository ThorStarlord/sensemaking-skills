> **HISTORICAL (pre-ADR-0013, 2026-08)**: runner-led orchestration record,
> preserved as historical evidence. The ratified execution model is agent-native
> (ADR 0013); the programmatic second-model runner was retired.

# Candidate architecture decision — repo-sensemaker vNext integration

**Branch:** `candidate/sensemaking-vnext`, built from `main` @ `e790f30` (identical tip; PR #163 not yet merged, not included here — see "Known dependency" below). Built under [Mode B+](../../docs/prototypes/repo-sensemaker-vnext.md) (owner-broadened delegation, 2026-08-09): architecture/implementation authority delegated, merge-to-main withheld pending owner review.

**Relationship to #164**: `prototype/repo-sensemaker-vnext` (PR #164) is preserved as the evidence record — "what did we learn." This branch is "what should the product now look like," starting fresh from `main`, using #164's ledger/experiments as evidence and constraints, not as a backlog to implement literally.

This document records the judgment calls made before writing code, per the working mode's own instruction ("record the assumption and alternatives" before implementing). It is not exhaustive design documentation — see commit messages and inline comments for implementation detail.

---

## Decision 1: Packaging — Option C (one skill, internally separated), not Option A (two skills)

**Evidence hierarchy applied** (per Mode B+): the *behavior* (durable-brief-as-boundary, investigate-first, neutral clarification, evidence-resolved-vs-owner-authorized distinction) has real evidence — tier 1/2, survived two genuinely isolated subagent replications (round 3, round 3b of the real-use experiment). The *packaging* (two Skill files vs. one) has zero differentiating evidence between A and C at any point in #164's history — every real-use test exercised the artifact boundary, never the packaging boundary itself.

**New grounding fact, not available during #164** (found during recon of this branch's actual production wiring, not the prototype's conversational-only invocation): `repo-sensemaker` is invoked two structurally different ways in this repo —
1. **Automated runtime execution** (`ClaudeAgentSdkSkillExecutor` + `scripts/brief_skeleton.py`'s `build_skeleton()`/`reconcile()`): a single non-interactive step. There is no chat channel back to an owner mid-run — the deliverable is the artifact, full stop.
2. **Direct conversational invocation**: a user or agent talking to `repo-sensemaker` directly, where asking a clarifying question is possible and meaningful.

The "interaction layer" behavior (ask-if-decision-changing) can only ever execute in mode 2. Giving it its own Skill file with its own `skill-registry.yaml` entry would imply it's an independently routable, runtime-invocable unit — which would be actively misleading, since it structurally cannot run inside the automated runtime path at all. This is a concrete, mechanical reason for Option C beyond "no evidence differentiates them": the two responsibilities don't just *happen* to be usable together, one of them (diagnose) is runtime-invocable and the other (interact) is conversational-only by construction.

**Decision**: `repo-sensemaker/SKILL.md` stays one file, with two clearly labeled, separately-headed responsibilities:
- **Diagnose** — unchanged mechanics (Stage 1 intent comparison, evidence gathering, brief production via the runtime skeleton), extended only by the new optional Section 15 fields (Decision 2). Runs identically whether invoked by the runtime or a human.
- **Interact** — explicitly scoped to conversational invocation only, documented as such. Reads the brief (including Section 15) and applies investigate-first / neutral-clarify / synthesize. Does not run, and is documented as not running, during automated runtime step execution.

`repository-diagnostician` (the prototype's separate diagnostic-core skill) is not carried forward as a file — its content (the brief-producing logic) is what "Diagnose" already is in canonical `repo-sensemaker`, extended per Decision 2. Nothing is lost; the file itself is dropped as duplicate packaging with no behavior it uniquely provided.

## Decision 2: Which vNext fields survive, per "if useful -> implement; if redundant -> collapse; if unsupported -> omit"

| Field | Verdict | Why |
|---|---|---|
| `uncertainty.source` + `uncertainty.question` | **Keep, as-is** | Strongest, most repeatedly load-bearing evidence of any field (S1, round 3, round 3b). |
| `consequential_boundary` + `is_demonstrated_weakness` | **Keep, as-is** | Real verdict-changing evidence (P4; round 3's `pursue` vs `pursue_narrowed`). |
| `owner_intent_state` | **Keep, revised** | `status` (sufficient/thin/blocking_unknown) does real, distinct gating work. The separate freestanding `unresolved` prose is dropped — it duplicated `uncertainty.question` (the unresolved thing, when `source: owner_intent`) and could silently drift from it (retrospective's own REVISE note). New shape: `{known, status}` only; the "what's unresolved" content lives in `uncertainty.question`, referenced not restated. |
| `domain` | **Keep, tightened** | Produced one real, distinct effect (out-of-lens disclosure) in round 3 — modest but genuine, tier-1 evidence. The round-2 composition test's open question ("does a 2nd domain value always mean withhold judgment?") is resolved by rule, not left to per-instance judgment: any domain value outside a consumer's own competence is always a disclosure trigger, never silent. |
| `discovery_confidence` | **DROPPED, 2026-08-10** (superseding this row's original "Keep, as-is") | Originally kept on the strength of pre-vNext prior art; the 2026-08-10 architecture stress-test's Case 4 confirmed — not merely left untested — that no consumer instruction (`architectural-review`'s Boundary Rule 6, `repo-sensemaker`'s Interact) reads this field at all, at any value. "Field exists, nothing reads it" was the pre-registered drop criterion; removed rather than wired in on the grounds that inventing consumer behavior to justify a field's survival inverts what a discovery pass is for. See `docs/candidate/stress-test-2026-08-10/` and the draft ADR's Round 2 section. |
| `evidence_status_notes` | **Omit** | Never exercised in any real run across #164's entire history (tier 5, purely speculative). Dropped per YAGNI; can be reintroduced if a real cross-excerpt disagreement ever actually occurs. |
| `weakness_type: none` sentinel | **Stays rejected** | Already correctly not built (twice-confirmed); `is_demonstrated_weakness: false` + absent canonical `weakness_type` is the right encoding, unchanged. |
| `resolution_mode` | **Stays not-a-field** | Confirmed correct twice already; remains prose guidance in the Interact section, not a stored value. |

## Decision 3: How the new fields attach to the real artifact (the production-reality finding)

Read `scripts/brief_skeleton.py` directly (not from memory of the prototype). Its `reconcile()` function rebuilds the artifact from a fixed skeleton (`build_skeleton()`) and only ever splices model content into pre-declared holes (`MODEL_YAML_FIELDS`, `MODEL_SECTIONS`, plus the specially-handled `evidence_excerpts` marker pair). **Any content the model produces outside those declared holes — including a hypothetical freeform "Section 15" appended after Section 14 — is silently discarded by `reconcile()`.** This is exactly why the prototype's identical-looking Section 15 never had to survive this: PR #164 stated explicitly it was "invoked directly during evaluation... not through `workflow-runtime.py`... the canonical runtime-owned-skeleton protocol... is unaffected by this branch." For the candidate to be real, it isn't.

**Decision**: extend `brief_skeleton.py` itself — a new, dedicated `## 15. Extended analysis (candidate)` section with its own `MODEL_SECTION:extended_analysis:BEGIN/END` marker pair holding a YAML fence, structurally identical in kind to how `evidence_excerpts` (Section 8) is already special-cased as "model, constrained yaml" distinct from both free prose and the flat Section 13 fields. `reconcile()` gets a new harvest/splice step for it, following the existing `evidence_excerpts` pattern. Per ADR 0015's explicit requirement ("any new field added to a contract must be classified at proposal time"), every new field here is classified **model, constrained** (not free prose) — same class as `weakness_type` — and is validated as **non-blocking** (warnings only) by `validate-brief.py`, matching the precedent ADR 0015/0016's own addenda already set for unratified structured fields. `artifact-contracts.yaml` gets a new `recommended_machine_fields`-equivalent entry for the block, explicitly marked candidate/unratified in its notes.

## Decision 4: Downstream consumers

Read `skills/architectural-review/SKILL.md` directly. It already consumes the brief as a whole document (not field-by-field), already has an `investigate_first` fallback for an "incomplete or insufficient" brief, and its Boundary Rule 1 already forbids re-diagnosing the repository. **No new consumer skill is needed** — the prototype's `vnext-review-consumer` existed only because no real consumer had been tested against; `architectural-review` already composes safely with additive fields by construction (it never enumerates required fields, it reads the document).

**One real, bounded addition**: round 3's evidence showed `is_demonstrated_weakness` and `domain` change a real verdict (`pursue` vs `pursue_narrowed`; explicit out-of-lens disclosure) when a downstream reviewer uses them. `architectural-review/SKILL.md` gets a short, explicitly-optional paragraph: *if* Section 15 is present, factor `is_demonstrated_weakness` into scope (a proposal addressing only part of a demonstrated weakness is narrower than the evidence, not defective) and `domain` into competing-lens disclosure. Absence of Section 15 changes nothing — this is additive guidance, not a new requirement.

## Known dependency, deliberately not duplicated here

`validate-brief.py`'s `primary_fog_type` check still hardcodes 4 fog types (missing `integration_fog`) on this branch, because PR #163 (the registry-driven fix) is still open, unmerged, on `main`. That is a separately-scoped, already-built, already-reviewed `main`-track repair (lane 1) — reimplementing it here would duplicate work and create a conflict when #163 eventually merges and this branch rebases. This candidate inherits that gap unchanged and depends on #163 merging before `integration_fog` briefs validate cleanly through either branch.

## What this decision does NOT do

Does not touch `workflow-runtime.py`'s `_WORKFLOW_ID_FIELDS`/`_FOG_TYPE_FIELDS`/routing logic — none of the new fields drive auto-routing, so `test_field_contract_agreement.py`'s guard is untouched by design, not by oversight. Does not modify `scripts/workflow-planner.py` (found to be dead/uncalled code during recon) — unrelated to this architecture, left alone to avoid scope creep. Does not merge to `main`.
