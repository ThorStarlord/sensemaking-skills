# Prototype: repo-sensemaker vNext

**Branch: `prototype/repo-sensemaker-vnext`. This branch is a construction
probe. Its purpose is to make the proposed repo-sensemaker architecture
concrete enough to evaluate. Nothing on it is canonical merely because it
works. Nothing here overrides an Accepted ADR; where this prototype
conflicts with one, the candidate behavior is isolated here and a draft
amendment is sketched, not enacted.**

Built after PR #162 (canonical wiring reconciliation, merged) and while
PR #163 (fog-vocabulary registry-driven fix) is open for review. Neither PR
is affected by this branch.

## Choice table

| Choice | Prototype answer | Evidence level | Where |
|---|---|---|---|
| Interaction ownership | `repo-sensemaker` (Option A) | Provisional — packaging is a hypothesis, not proven; only 1 of 3 candidate options built | [`skills/repo-sensemaker/SKILL.md`](../../skills/repo-sensemaker/SKILL.md) |
| Diagnostic core | Separate skill, `repository-diagnostician` | Provisional | [`skills/repository-diagnostician/`](../../skills/repository-diagnostician/SKILL.md) |
| `uncertainty_source` | Structured field (4 values) | Supported by S1 (n=1, agent-selected target, wording defect noted) | [vNext template](../../skills/repository-diagnostician/references/brief-vnext-template.md) |
| `consequential_boundary` vs `weakest_boundary` | Structured field, `is_demonstrated_weakness` flag | Supported by P4 (n=1) | vNext template; [draft ADR sketch](draft-adr-consequential-boundary.md) |
| `owner_intent_state` | Structured field (known/unresolved/status) | Exploratory — direct response to "never invent owner preference," untested in a real interaction | vNext template |
| `weakness_type: none` | **Rejected** — use `is_demonstrated_weakness: false` + absent `weakness_type` instead | N/A — this is the one place the prototype explicitly did *not* do what an earlier conversation turn proposed, because it would contaminate the ratified D3 taxonomy | [draft ADR sketch](draft-adr-consequential-boundary.md) |
| `domain` (product/architecture/UI/...) | **Not built** | Conceptual only — fog taxonomy already approximates it; building a second axis before reconciling the first was judged premature | — |
| `evidence_status` | **Not built** | Conceptual only — likely belongs nested per-excerpt, not top-level; no concrete case forced it here | — |
| `resolution_mode` | **Not built** (would be a derived lookup from `uncertainty_source`, not authored) | The mapping is written as prose guidance in `repo-sensemaker/SKILL.md`'s workflow diagram, not a stored field | [`skills/repo-sensemaker/SKILL.md`](../../skills/repo-sensemaker/SKILL.md) |
| `discovery_confidence` | **Not built** | Reasoning guidance only, per its own "status" note from the earlier roadmap — no schema | — |
| Routing by uncertainty | **Not built as routing** — documented as agent reasoning guidance in the interaction workflow, not wired into `workflow-planner` | Unproven; ADR 0018 still governs real routing unchanged | [`skills/repo-sensemaker/SKILL.md`](../../skills/repo-sensemaker/SKILL.md) |
| Evidence acquisition tooling | One demonstration tool built (duplicate-authority scan) | Validated against the real repo — correctly finds the known `workflow-orchestrator/`/`skills/workflow-planner/` pair | [`scripts/prototype_duplicate_authority_scan.py`](../../scripts/prototype_duplicate_authority_scan.py) |
| Native downstream consumer | **Not built this pass** | Deferred — see below | — |

## Assumption ledger

**A-01 — repo-sensemaker owns interaction (Option A over B/C).**
Why chosen: simplest concrete implementation of S1's interaction shape;
reuses the existing skill name so the interaction-vs-diagnosis contrast is
legible against `main`.
Evidence: S1 demonstrates the investigate-first/clarify-if-needed *pattern*
works; it says nothing about which module should own it.
Alternative: Option B (generic `sensemaking-interaction` skill), Option C
(one skill, internally separated).
Reversibility: high — deleting `repository-diagnostician/` and restoring
`main`'s `SKILL.md` fully reverts this.
Status: **PROTOTYPE ONLY.**

**A-02 — `uncertainty_source` has exactly 4 values
(`repository_evidence`/`empirical`/`owner_intent`/`external_environment`).**
Why chosen: matches the original conceptual discussion's own examples
exactly; S1 directly exercised the `repository_evidence`/`owner_intent`
split.
Evidence: S1 (behavioral), `external_environment`/`empirical` unexercised
by any experiment so far.
Alternative: fewer values (S1 only needed 2); more values (not yet
motivated by any case).
Reversibility: high — this is prose/template, read by nothing canonical.
Status: **PROTOTYPE ONLY.**

**A-03 — `resolution_mode` is not a stored field.**
Why chosen: every example given for it, in every prior turn of the source
discussion, was a deterministic function of `uncertainty_source` alone —
storing it as an independently authored field creates a class of bug where
the two fields disagree with each other for no reason.
Evidence: no counterexample has been raised where `resolution_mode` needs
information `uncertainty_source` doesn't already carry.
Reversibility: high.
Status: **PROTOTYPE ONLY**, and the one item in this ledger closest to
"probably right regardless of which packaging option wins."

**A-04 — `weakness_type: none` rejected in favor of
`is_demonstrated_weakness: false`.**
Why chosen: adding a non-mechanism sentinel into a 7-item taxonomy of
defect *mechanisms* contaminates that taxonomy; a companion boolean flag
keeps the taxonomy's meaning intact while still letting the brief be
truthful about non-defect findings.
Evidence: P4's forced `Contract Mismatch` labeling of a non-defect finding.
Alternative considered and rejected: new enum value (contaminates
taxonomy, per the same reasoning ADR 0015's D4 addendum already used to
reject Option C — "relocates brittleness rather than removing it").
Reversibility: high — schema-only, not wired into any canonical validator.
Status: **PROTOTYPE ONLY** — see
[draft ADR sketch](draft-adr-consequential-boundary.md).

**A-05 — the duplicate-authority scan groups by trailing path suffix within
the same top-level directory prefix only when prefixes differ.**
Why chosen: two sibling skills legitimately having their own
`references/notes.md` under the *same* `skills/` prefix is not evidence of
anything; two different top-level trees (e.g. `workflow-orchestrator/` vs
`skills/workflow-planner/`) sharing a suffix is the actual S1-shaped
pattern.
Evidence: validated directly against the real repository — correctly
surfaces the known, deliberately-kept
`workflow-orchestrator/references/artifact-contracts.yaml` /
`skills/workflow-planner/references/artifact-contracts.yaml` pair and
nothing else.
Reversibility: high — read-only script, not wired into CI.
Status: **PROTOTYPE ONLY**, but this one has passing tests against real
repository state, not just constructed fixtures.
**Revised after owner review**: originally scanned the filesystem
(`os.walk`) under a misleadingly-named `find_tracked_files()`, repeating
the exact class of mistake P4's `.venv` correction identified — workspace
≠ tracked product. Now prefers `git ls-files` and reports which evidence
source (`git_tracked` vs `filesystem_fallback`) produced each result; a new
test proves an untracked file is correctly excluded when run inside a git
repo.

## Fixes applied after owner review of #164 (2026-08-09)

Six internal-coherence issues were found reviewing the first prototype pass
— all fixed, nothing else changed, per the owner's explicit "then stop":

1. `repository-diagnostician/SKILL.md` told the model to record
   `weakness_type: none` for legitimate-unresolved-choice findings —
   directly contradicting the vNext template and A-04's explicit rejection
   of that sentinel. Fixed to say: set `is_demonstrated_weakness: false`,
   leave canonical `weakness_type` absent.
2. The vNext template stored `recommended_next_information_action` — a
   duplicate, model-authored copy of the pure function of `uncertainty.source`
   that A-03 already said shouldn't be independently authored (it could
   silently disagree with `source`, e.g. `owner_intent` + `probe`). Removed;
   the mapping lives once, in `repo-sensemaker/SKILL.md`'s workflow diagram.
3. `uncertainty.question` was commented "only meaningful when source is
   owner_intent" — wrong; every source has an unresolved question
   (empirical and repository_evidence examples added to the template).
   Only the *conversion* of that question into something to ask the owner
   is owner_intent-specific, and that conversion is the interaction layer's
   job, not the diagnostic core's.
4. `repo-sensemaker/SKILL.md`'s empirical-uncertainty branch said to
   "propose ... (or just run) the probe" — directly contradicting this same
   skill's Boundary Rule #1 ("No implementation"), and ignoring that some
   probes are themselves ADR 0017/0021-gated. Fixed to formulate-and-
   recommend only, with an explicit hand-off note.
5. The vNext `evidence_note` copied the real, unchanged citation-authority
   hierarchy (code/tests > ADRs > ...) as if it were a total ordering for
   resolving code-vs-ADR *disagreements* too. Split into two axes:
   citation trust (unchanged) vs. descriptive-vs-normative evidence, with
   disagreement between the two now reported as drift rather than resolved
   by rank.
6. See A-05 above — scanner tracked-vs-filesystem fix.

## What was deliberately deferred this pass (not built)

Per the same "don't build twenty skills" / "mechanical tools only when a
real investigation needs them" discipline established earlier in this
project:

- **`domain` axis** — fog taxonomy already approximates it; reconcile the
  first taxonomy before adding a second.
- **`evidence_status` axis** — no concrete case has forced this yet; likely
  belongs nested per-excerpt (in `evidence_excerpts`), not top-level.
- **`discovery_confidence` schema** — kept as reasoning guidance only, per
  its own stated status; no field added.
- **Full evidence-acquisition tool suite** (git history/ancestry,
  tracked-vs-untracked, package/wheel inspection, version drift, CI
  inspection, dependency structure, runtime helpers) — one demonstration
  tool was built and validated; the rest should be built when a real
  investigation actually needs each one, not speculatively.
- **Native downstream consumer(s)** — building even one well is a
  substantial scope item on its own (a real skill, understanding the vNext
  handoff, with its own tests); not attempted this pass so the pieces that
  *were* built (interaction layer, diagnostic core, brief vNext) could get
  real engineering attention instead of seven shallow attempts.
- **Uncertainty-aware routing as actual routing** — documented as agent
  reasoning guidance in `repo-sensemaker/SKILL.md`'s workflow diagram;
  not wired into `workflow-planner` or any registry. ADR 0018 governs real
  routing, unchanged.
- **Registering either prototype skill** in `skill-registry.yaml` or any
  workflow — would make this prototype's existence part of the canonical
  skill inventory, contradicting the isolated-surface premise.

## What this prototype cannot establish, by design

- **Whether a real owner finds this interaction useful.** Nothing here
  exercises a real owner-originated decision. That's the one thing S1's own
  disposition (PROMISING, not CONFIRMED) already said was the needed next
  evidence, and building more prototype code doesn't produce it.
- **Whether Option A beats B or C.** Only Option A was built. The
  comparison this ledger enables is "read Option A's SKILL.md files and
  judge coherence," not "empirically compare three implementations."
- **External validation status.** Unaffected — governed by ADR 0021's
  ratified, staged experiment-authorization process, which this prototype
  does not touch and cannot self-authorize past.

## Files on this branch

- `skills/repository-diagnostician/SKILL.md`, `references/brief-vnext-template.md` (new)
- `skills/repo-sensemaker/SKILL.md` (restructured, this branch only)
- `scripts/prototype_duplicate_authority_scan.py`,
  `tests/test_prototype_duplicate_authority_scan.py` (new, 6/6 passing,
  includes a real-repo sanity check)
- `docs/prototypes/repo-sensemaker-vnext.md` (this file)
- `docs/prototypes/draft-adr-consequential-boundary.md`,
  `docs/prototypes/draft-adr-diagnostic-interaction-split.md` (draft
  sketches, not filed ADRs)

## Recommendation

Keep — as a reference for evaluating Option A specifically, and as the home
for the two draft ADR sketches, which have value independent of whether
this branch itself is ever merged. Discard or heavily revise before any of
`repository-diagnostician`, the vNext brief fields, or the restructured
`repo-sensemaker` role are treated as more than "one candidate that now
exists to look at."
