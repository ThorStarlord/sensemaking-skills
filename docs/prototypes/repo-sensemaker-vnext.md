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
| `domain` (list) | **Built, round 2** — reuses canonical fog vocabulary base names, deliberately multi-valued (unlike `primary_fog_type`) | Exploratory; motivated by P4's actual finding spanning product+architecture; one real judgment call surfaced in the composition test (does a second domain value always mean "withhold judgment," or only sometimes — see A-09) | vNext template |
| `evidence_status_notes` (per-excerpt) | **Built, round 2** — vNext-only list keyed to Section 8 excerpts by (file, lines), not a new field on `evidence_excerpts` itself | Exploratory — not yet exercised against a real cross-excerpt confidence disagreement | vNext template |
| `resolution_mode` | **Not built** (confirmed correct, round 2) — still a derived lookup from `uncertainty_source`, not authored | The mapping is written as prose guidance in `repo-sensemaker/SKILL.md`'s workflow diagram, not a stored field | [`skills/repo-sensemaker/SKILL.md`](../../skills/repo-sensemaker/SKILL.md) |
| `discovery_confidence` | **Built, round 2** — `{level, why_bounded}`, formalizing the existing S1 owner-synthesis "confidence and why bounded" prose pattern | Exploratory; used meaningfully once in the composition test (`level: high`, grounded in direct observation) | vNext template |
| Routing by uncertainty | **Not built as routing** — documented as agent reasoning guidance in the interaction workflow, not wired into `workflow-planner` | Unproven; ADR 0018 still governs real routing unchanged | [`skills/repo-sensemaker/SKILL.md`](../../skills/repo-sensemaker/SKILL.md) |
| Evidence acquisition tooling | **Three tools, round 2**: duplicate-authority scan, tracked-vs-workspace comparator (P4 `.venv` pattern), version-drift detector (S1's README-vs-pyproject pattern). A fourth (git bulk-arrival) considered, deferred. | All three validated against real, previously-documented findings in this repo, not just constructed fixtures — see A-05, A-07, A-08 | `scripts/prototype_*.py` |
| Native downstream consumer | **Built, round 2** — `vnext-review-consumer`, architectural-review-shaped, 5 documented behavioral differences from the real canonical `architectural-review` skill | Exploratory; exercised once in the composition test | [`skills/vnext-review-consumer/SKILL.md`](../../skills/vnext-review-consumer/SKILL.md) |
| End-to-end composition | **Run once, round 2** — real artifacts, agent-selected real question about this repo | Modest positive evidence for the brief-as-boundary; inconclusive on Option A vs. C packaging — see A-10 and the dedicated writeup | [`docs/prototypes/composition-test-2026-08-09/`](composition-test-2026-08-09/00-context.md) |

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

## Round 2 — vNext expansion under the Mode B standing instruction (2026-08-09)

Authorized as a formally scoped Mode B prototype objective. Entries A-06
through A-10 below follow the same format as A-01 through A-05.

**A-06 — `domain` is a list, reusing canonical fog vocabulary, not a new
taxonomy.**
Why chosen: the earlier deferral reasoning ("fog taxonomy already
approximates this; reconcile first") is still correct for a *single-valued*
domain — but `primary_fog_type` structurally cannot be multi-valued
(ADR 0018 routing needs exactly one value), and P4's actual finding
(canonical-surface choice = product; how the two implementations diverged
= architecture) is multi-domain. `domain` adds behavioral value
specifically by being a list, not by being a second taxonomy.
Evidence: P4 (n=1) for multi-domain findings existing at all; the
composition test (n=1) for a real judgment call about when a second value
should change downstream behavior (see A-09).
Alternative: leave `primary_fog_type` as the only domain signal (status
quo) — rejected because it already silently drops information today.
Reversibility: high — vNext-only field.
Falsifiable by: a review of several real briefs where `domain` never ends
up multi-valued, or is multi-valued but downstream behavior never differs
based on it.
Status: **PROTOTYPE ONLY.**

**A-07 — tracked-vs-workspace comparator prefers `git ls-files`, reports
provenance.**
Why chosen: directly operationalizes P4's own `.venv` correction as a
reusable check, correcting the same mistake the original duplicate-
authority scanner made (A-05) before its own fix, this time built correctly
from the start.
Evidence: validated against a constructed fixture reproducing P4's exact
numbers (2 tracked vs. 22 workspace files, 20 under `.venv/`), AND against
this repo's real `scripts/` directory. Note: while finishing round 2, this
same tool's own real-repo sanity test transiently failed because two new,
not-yet-committed prototype scripts sat untracked in `scripts/` — a correct
detection, not a bug, that resolves once those files are committed (see
verification section below).
Reversibility: high — read-only script.
Falsifiable by: a directory where a high untracked ratio is normal and
expected (the tool would need a per-directory allowlist it doesn't have).
Status: **PROTOTYPE ONLY**, 6/6 tests passing.

**A-08 — version-drift detector is narrow (README vs. pyproject.toml
only), not a general cross-manifest version comparator.**
Why chosen: a naive "flag any version-string mismatch across manifests"
tool would false-positive on this repo immediately —
`pyproject.toml`'s `0.2.2` and `package.json`'s `4.1.0` are legitimately
independent (Python package version vs. npm tooling version), never meant
to match. S1's actual finding compared the *same* conceptual version
(the package's own) as declared canonically vs. as mentioned in prose.
Narrower claim, but a true one instead of a noisy one.
Evidence: reproduces S1's exact finding, confirmed still live on this repo
right now (`README.md:77` says `0.2.1`, `pyproject.toml` says `0.2.2`) —
this was S1's own finding, unresolved since it was recorded as
"minor and non-decision-changing" and evidently never revisited.
Reversibility: high.
Falsifiable by: a case where README/pyproject drift genuinely doesn't
matter (S1 already judged this instance that way) — the tool still
correctly reports it; whether to *act* on a true report is a separate,
undecided question this tool deliberately doesn't answer.
Status: **PROTOTYPE ONLY**, 6/6 tests passing, real-repo case confirmed.

**A-09 — git-history bulk-arrival detector (the third evidence-tool
candidate) deferred, not built.**
Why deferred: the task explicitly weighted vertical integration (one
downstream consumer, one real composition test) over a third evidence
tool; two tools each validated against a real prior finding were judged
sufficient evidence that "operationalize prior findings as reusable
scripts" works as an approach, without needing a third instance to prove
the same point again.
Reversibility: n/a — not built.
Status: candidate for a future round if a real investigation specifically
needs it (per this project's own "tools when needed" discipline), not
scheduled.

**A-10 — one native downstream consumer (`vnext-review-consumer`), five
documented behavioral differences from real `architectural-review`.**
Why chosen: architectural-review is this repo's only ADR-0018-proven route
and the natural comparison point — building against it (having read its
real `SKILL.md` in full first) makes "what does native preserve that
generic loses" a checkable claim, not an assertion.
Evidence: the composition test exercised all five documented differences
at least conceptually; only two were actually load-bearing for the
specific proposal evaluated (`is_demonstrated_weakness: true` selecting
the standard framing branch — confirming the skill doesn't ALWAYS take the
exotic path; `owner_intent_state.status: thin`, not `blocking_unknown`,
correctly not triggering the hard stop). The `domain`-as-competing-lens
check (difference #4) forced a real judgment call not resolved before
this run — see the composition assessment for the distinction it
surfaced (registry-file-touched vs. genuinely-competing-authority).
Reversibility: high — not registered in any canonical registry/workflow.
Falsifiable by: a real case where the "generic" `architectural-review`
skill, run on the same brief, produces the same or better judgment despite
not reading `analysis_vnext` — this test didn't run that comparison
directly (no real invocation of the generic skill occurred), which is a
real limitation, not a settled point.
Status: **PROTOTYPE ONLY**, one deep vertical, not five shallow.

## What was deliberately deferred this pass (round 2 status)

Per the same "don't build twenty skills" / "mechanical tools only when a
real investigation needs them" discipline, now updated — several round-1
deferrals were built this round (domain, evidence_status_notes,
discovery_confidence, two more evidence tools, one downstream consumer,
one composition test); what's still deferred:

- **`evidence_status` beyond the vNext-only sibling-list form** — not
  merged into canonical Section 8's `evidence_excerpts` schema (ADR
  0016-governed, untouched by design).
- **A fourth+ evidence tool** (git history/ancestry, package/wheel
  inspection, CI/runtime configuration helpers) — see A-09.
- **A second/third downstream consumer, or Options B/C implementations**
  — the composition test's result (inconclusive on packaging, modest-
  positive on artifact boundary) doesn't yet give a concrete reason to
  build an alternative for comparison; per the task's own instruction,
  documented as unresolved rather than built for symmetry.
- **Uncertainty-aware routing as actual routing** — still documented as
  agent reasoning guidance only, not wired into `workflow-planner` or any
  registry. ADR 0018 governs real routing, unchanged.
- **Registering any prototype skill** in `skill-registry.yaml` or any
  workflow — still deliberately outside the canonical skill inventory.
- **Running the real `architectural-review` skill on the same brief for a
  direct comparison** — the composition test compared `vnext-review-
  consumer`'s design against `architectural-review`'s documented behavior
  by reading its `SKILL.md`, not by actually invoking it side-by-side on
  the same input. A real comparison run is a candidate for the next round,
  not done here.

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
- **Whether the brief-as-boundary result from the composition test
  generalizes.** The one composition test run (round 2) was authored
  end-to-end by a single continuous agent with full memory of the whole
  investigation — it cannot distinguish "the brief was genuinely
  sufficient for the consumer step" from "the same agent already knew
  everything and didn't need to re-derive it regardless of which document
  it was writing." A test that could tell those apart needs the consumer
  step authored from a fresh context given only the brief, not a
  continuation of the session that produced it. See
  `composition-test-2026-08-09/04-composition-assessment.md` for the full
  treatment — this limitation is argued there, not glossed over.

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
- **Round 2 additions:**
  `scripts/prototype_tracked_vs_workspace_scan.py` +
  `tests/test_prototype_tracked_vs_workspace_scan.py` (6/6 passing),
  `scripts/prototype_version_drift_scan.py` +
  `tests/test_prototype_version_drift_scan.py` (6/6 passing),
  `skills/vnext-review-consumer/SKILL.md` (new downstream consumer),
  `docs/prototypes/composition-test-2026-08-09/` (4 artifacts: context,
  brief, interaction synthesis, consumer output, plus the honest
  assessment)

## Round 3 — real-use validation (2026-08-09)

A genuine owner-originated question ("what should I focus on next for
product value, what should I stop investing in") was run through the
pipeline for the first time, with real invocation-level context separation
(via the Agent tool) between the diagnostic core and the downstream
consumer — the specific limitation the round-2 composition test flagged as
unresolvable by a single self-administered session. Full record:
[`docs/prototypes/real-use-experiment-2026-08-09/`](real-use-experiment-2026-08-09/05-retrospective.md).

Headline results: the brief-as-boundary hypothesis held cleanly under real
separation (downstream consumer used zero repository access, verdict
`pursue_narrowed` reasoned correctly from brief content alone).
`uncertainty.source` and `is_demonstrated_weakness` were both concretely
load-bearing. A real interaction-layer design gap was found and caught
live by the owner (bundling an evidence-resolved fix with an
evidence-supported-but-unauthorized policy recommendation as if both were
equally ready to act on) — recorded as a REVISE item, not silently fixed.
See the retrospective for the full KEEP/REVISE/DROP/UNKNOWN/NEXT EVIDENCE
breakdown.

## Recommendation

Keep — now with one real-use data point behind it, not zero. The
diagnostic-core/downstream-consumer boundary has cleared its first
genuinely-separated test; the interaction-layer/diagnostic-core boundary
has not yet been tested the same way (see round 3's UNKNOWN section) and
the interaction layer itself has one named, unfixed design gap. Continue
treating every field and packaging choice as provisional — round 3 changed
confidence levels on several, but ratified none.
