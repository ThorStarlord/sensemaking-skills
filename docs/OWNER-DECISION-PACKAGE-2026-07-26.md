# Owner Decision Package

**Date**: 2026-07-26
**Source**: `docs/PRODUCT-CONTRACT-REVIEW-2026-07-26.md` (local, uncommitted —
see note below)
**Nature of this document**: decision-support only. No code, validator,
prompt, contract, test, or runtime change was made. No commit was created. No
GitHub issue, PR, or ADR was modified, closed, or merged. No auteur rerun. No
recommendation from the source review is treated as accepted here — every
review recommendation is presented as a proposal pending your explicit
sign-off in the response form at the end.

**Provenance note**: the source review file exists only in the local working
tree (`git status` shows it as `??`, untracked, never committed or pushed). It
is not on any branch, local or remote, other than sitting uncommitted in this
checkout. It is not lost or on an unmerged branch — it simply hasn't been
committed. That is a separate, small decision (commit it? where?) that this
package does not resolve on your behalf.

---

## Part 1 — Review-document verification

The source review contains all 11 required elements:

1. Recommended product boundary — Part 1 (Interpretation A)
2. Field-ownership model — Part 2 (table)
3. Weakness-type contract analysis — Part 3 (5-option evaluation table)
4. Evidence policy — Part 4 (7-layer table)
5. Readiness ladder — Part 5 (6-level table)
6. Auteur campaign interpretation — Part 6 (per-PR table)
7. Open-work disposition — Part 7 (per-issue/PR table)
8. Recommended next phase — Part 8
9. Owner decisions — Part 9 (7 items)
10. ADR update plan — Final deliverable, item 11
11. Implementation prompt — Final deliverable, item 12

**Contradictions or unsupported assertions found**:

- **One internal inconsistency, minor**: Part 0's summary table and Part 6
  both correctly attribute PR #78's failure as unfixed-by-design, but Part 8's
  "Rationale for rejecting the alternatives" paragraph labels a fifth external
  repo as "Option C" while Part 8's own numbered options list later calls it
  "Option C" too (`C. Test a second external repository` in this task's
  numbering) — the source review's internal Part 8 lettering (A/B/C/D from its
  own Part 8, not this task's D10 lettering) is self-consistent but does not
  match this task prompt's D10 option lettering. Not a factual error, just a
  labeling collision between two independently-lettered option lists. Flagged
  so it isn't mistaken for the review contradicting itself substantively.
- **No unsupported assertion found that lacks a citable PR/ADR/issue**: every
  claim in Parts 0, 1, 3, 5, 6 traces to a specific PR number, ADR section, or
  file/line (e.g. `scripts/validate-brief.py:279-286`), which was
  independently verified against the actual file during the original review
  (confirmed again here by re-reading the review text against the earlier
  research — no drift found).
- **One place where the review states an absence of evidence rather than
  inventing a default**: Part 9's items 5 and 7 ("not settled by this
  review") are correctly left open rather than the review picking a default
  for the owner — this is the right behavior, not a gap.
- **No recommendation found that contradicts the cited evidence.** The
  weakest link in the chain is Part 3's Option B "Migration cost" and
  "Routing compatibility" cells, which describe a hypothetical future
  consumer ("a router/report can read it") that does not exist yet — this is
  clearly framed as a future capability, not a present fact, so it is not a
  contradiction, just worth flagging as the one place the review reasons
  slightly ahead of current code.

No edits were made to the review document.

---

## Part 2 — Decision register

| ID | Decision | Options | Review recommendation | Consequence if accepted | Consequence if rejected | Evidence strength |
|---|---|---|---|---|---|---|
| **D1** | Product boundary | A. Human-reviewed brief assistant / B. Validated autonomous pipeline / C. Workflow router + pipeline / D. Full pre-implementation planning system / E. Semi-autonomous dev orchestrator | **A** | Scope narrows to brief production; ADR 0014 "in scope" section narrows; routing/tracker/deployment work (#33/#34/#35) stays held | Product boundary stays at ADR 0014's current broader draft (closer to B/D); #33/#34/#35 could unblock sooner but on a boundary not evidenced by the campaign | **Strong** — every one of 4 campaign failures occurred inside brief production; zero evidence exists either way about routing/pipeline behavior externally, so B/C/D/E are not falsified, just unproven |
| **D2** | Weakness taxonomy role | A. Routing-critical, blocking / B. Required metadata, non-blocking / C. Advisory only / D. Remove the taxonomy | **B** | `weakness_type` becomes a real field but never fails an artifact by itself | If A: current blocking behavior continues, risking repeat PR #78-style rejections of substantively sound briefs; if C or D: less structure for any future consumer | **Strong for "not blocking"** (direct PR #78 evidence of over-blocking) — **weak for "required" vs "advisory"** (no downstream consumer exists yet to require it for) |
| **D3** | Weakness-type representation | A. Exact term in prose / B. Dedicated structured enum field / C. Deterministic post-generation classifier / D. Primary+secondary multi-label / E. No machine-readable field | **B** | Field declared in contract, skeleton, and prompt; validator checks the field, not prose wording | If A (status quo): the exact PR #78 failure mode recurs on the next external attempt; if C: brittleness moves into a new classifier component rather than disappearing; if D: more contract surface than the review judges necessary right now | **Strong against A** (direct failure evidence) — **moderate for B over D** (D is reasoned as "more than needed for the first fix," not evidenced as wrong) |
| **D4** | Handling an unknown/unmatched weakness type | A. Hard validation failure / B. Valid artifact + warning + human review / C. Runtime auto-assigns nearest type / D. Allow `Other` with explanation | Review does **not** clearly pick one — it recommends `Other` as an enum option (leaning D) but also says the field should be "recommended," i.e., its absence produces at most a warning (leaning B). **This is an unresolved design choice, not a clear recommendation** — do not treat B or D as ratified. | Depends on which is chosen; B and D are not mutually exclusive (could do both) | If C is chosen instead: reintroduces the same classifier-brittleness risk flagged for D3-Option C | **Weak / genuinely open** — the review's own text hedges between B and D without picking one |
| **D5** | Substantive evidence audit policy | A. Mandatory for every brief / B. Mandatory for absence/unreachability/dead-code/safety/high-risk claims / C. Optional human review / D. Second-model audit for every brief / E. No formal audit | **B** | Audit triggers only on the highest-risk claim class; routine claims skip it | If A: audit cost applies to every brief regardless of risk, unproven whether that's sustainable; if C or E: PR #73's exact failure mode (unsupported ghost-feature claim passing structurally) could recur uncaught | **Strong** — PR #73 is direct, specific evidence that skipping the audit on an absence claim let a real defect through; no evidence bears on whether *non*-high-risk claims need the same audit |
| **D6** | Human review depth | A. Human approves every final brief / B. Human reviews only high-risk claims / C. Human reviews only validator warnings / D. Fully autonomous output | **Explicitly left unresolved by the review** (Part 9, item 5) — preserved as unresolved here, not defaulted | N/A until chosen | N/A until chosen | **None** — the review states plainly that no repo evidence favors one answer |
| **D7** | Next readiness target | A. Remain experimental / B. Internally proven / C. Externally exercised / D. Externally validated / E. Limited production pilot / F. General production readiness | Review recommends **D** as the next target, explicitly **not** skipping to E. Current justified level is **C** (already met) — stated separately per instruction, not inferred as "next = C+1" | Next phase (Part 8/D10) targets clearing the ratified D8 evidence bar for external `repo-sensemaker` Stage A brief validation before any pilot claim (this does not require architectural-review or workflow Step 2 — see the 2026-07-26 ratification note below) | If E is chosen as the next target: a pilot would run before the taxonomy-brittleness defect (D3) is fixed, risking a 5th failure in the same bug family | **Moderate** — D is a reasoned next step, not something the campaign proves is the *only* valid next target; skipping to E is not shown to be wrong, just judged premature |
| **D8** | External-validation bar | A. One external repo, repeatable success / B. Two+ structurally different repos / C. Real maintainer use on one repo / D. Multiple repos + real maintainer use | **Explicitly left unresolved by the review** (Part 9, item 7) — preserved as unresolved here | N/A until chosen | N/A until chosen | **None** — only one external repo (`auteur`) has ever been tried; no evidence distinguishes these bars |
| **D9** | PR #78 interpretation | A. Legitimate product failure, taxonomy must remain blocking / B. Legitimate under current contract but evidence the contract is overly brittle / C. Model-compliance failure only / D. Successful external validation despite validator rejection | **B** | PR #78 is read as contract-defect evidence, motivating D3/D2 fixes, not as proof the model failed or that the run succeeded | If A: no contract change is warranted, campaign would need a 5th rerun on an unchanged validator; if D (must be explicitly rejected regardless): would misrepresent the campaign's result to any future reader of the record | **Strong** — the trace shows completed, genuine contradiction-search Grep/Read activity and a specific cited claim; the review's own text states this directly. **D is explicitly rejected**, not merely deprioritized — no reading of the evidence supports D. |
| **D10** | Next phase | A. Contract redesign, brief + validators only / B. Another auteur rerun / C. Second external repository / D. Human-reviewed pilot / E. Broader workflow development / F. Documentation consolidation only | **A** | Scoped, bounded implementation work (Part 8's phase definition) begins only after D1/D2/D3/D9 are ratified | If B or C chosen instead: risks repeating the same diagnosed bug family before it's fixed (per Part 8's own rationale); if E chosen: contradicts issue #27's "fix the spine before adding breadth" principle with zero new supporting evidence for doing so | **Strong for rejecting B/C before D3 lands** (direct, stated reasoning); **moderate for A over D/F** (reasoned trade-off, not an evidenced necessity) |

---

## Part 3 — Decision dependencies

```text
D1 (product boundary)
  → gates whether D7/D8 (readiness) and any routing/pipeline work (#33) are
    even in scope to discuss next; also gates D10 indirectly (a contract
    redesign for "brief production" only makes sense if D1 = A)

D2, D3, D4 (weakness-taxonomy contract — must be decided together, not
  independently: D2's severity, D3's representation, and D4's edge-case
  handling are three faces of one contract)
  → D2 constrains D3 (a blocking taxonomy (D2=A) makes D3's "Option A status
    quo" tolerable in a way non-blocking does not; a non-blocking taxonomy
    (D2=B/C) makes D3=B the natural fit)
  → D3 constrains D4 (D4 only has content once D3 picks a field shape — "Other
    with explanation" (D4=D) presumes a structured field exists to hold
    "Other")

D5, D6 (trust model — audit scope and human-review depth are two views of the
  same underlying question: how much does a human have to check)
  → depends weakly on D2/D3 (if weakness type is advisory/non-blocking, the
    audit and human-review burden shifts more fully onto the free-form
    weakest-boundary prose, which was already the case per Part 2's table —
    so this dependency is real but not blocking)

D7, D8 (readiness evidence — what counts as "validated," and how many repos/
  how much real use is required — are the same evidence question at two
  granularities: readiness *level* and readiness *bar*)
  → depends on D1 (a broader boundary (B/D) would require readiness evidence
    for routing/pipeline behavior too, not just brief production; D1=A keeps
    D7/D8 scoped to brief-only evidence)

D9 (PR #78 interpretation)
  → logically prior to D2/D3/D4, since D9 is the evidentiary basis *for*
    recommending a taxonomy change at all — if D9 were A instead of B, D2/D3
    would have no motivating evidence to change anything
  → independent of D1/D7/D8 (it's a narrow factual read of one PR, not a
    scope decision)

D10 (next phase)
  → depends on all of the above: cannot be finalized (scope, entry/exit
    criteria) until D1 is picked (defines what "in scope" means) and D2/D3/D4
    are picked (defines exactly what the contract redesign changes)
```

Recommended resolution order, adjusted slightly from the prompt's suggested
order to put D9 first (since it's the evidentiary premise for D2/D3/D4, not a
peer of them):

```text
D9 → D1 → (D2, D3, D4 together) → (D5, D6 together) → (D7, D8 together) → D10
```

This differs from a strict "D1 first" ordering because D9 is a factual/
evidentiary read of a single PR that doesn't depend on any scope decision —
resolving it first costs nothing and removes ambiguity before the scope
conversation starts. If you prefer to keep D1 strictly first, that reordering
doesn't change any other dependency in the chain.

---

## Part 4 — Proposed default package (proposal only — requires your approval)

| ID | Proposed default | Status |
|---|---|---|
| D1 | A | Review recommendation |
| D2 | B | Review recommendation |
| D3 | B | Review recommendation |
| D4 | **Unresolved** — review hedges between B and D | **Not defaulted; needs your input** |
| D5 | B | Review recommendation |
| D6 | **Unresolved** | **Not defaulted; needs your input** |
| D7 (current level) | C — externally exercised (factual, already met) | Not a decision, a status |
| D7 (next target) | D — externally validated | Review recommendation |
| D8 | **Unresolved** | **Not defaulted; needs your input** |
| D9 | B (D explicitly rejected regardless of anything else) | Review recommendation, high confidence |
| D10 | A | Review recommendation, conditional on D1/D2/D3/D9 above |

**Unresolved choices, restated plainly**: D4 (unknown-type handling), D6
(human-review depth), D8 (external-validation bar). None of these were
defaulted by the review or by this package — they require your judgment
because no repository evidence distinguishes the options.

---

## Part 5 — Implementation consequences (not implemented)

If the default package (Part 4) is approved as-is:

- `weakness_type` becomes a real, enum-validated field in
  `artifact-contracts.yaml` (D3=B), containing the 7 existing terms plus
  something for the unresolved D4 case.
- The `UNKNOWN_WEAKNESS_TYPE` prose-substring validator check is retired or
  downgraded to a warning (D2=B), not removed entirely — a brief without a
  valid `weakness_type` still produces output, just flagged.
- The weakest-boundary **prose remains fully model-generated and
  human-reviewed** — D3 only adds a parallel structured field, it does not
  constrain or template the narrative text (consistent with ADR 0015's
  existing split, Part 2 of the source review).
- **No routing decision may depend on `weakness_type`** unless D2 is later
  changed to A — as advisory/non-blocking metadata, nothing in
  `workflow-planner` may treat its absence or value as a routing input. This
  is a real constraint on any future implementation, not just documentation.
- High-risk claims (absence, unreachability, dead-code, safety-gap, missing-
  validation) require the substantive audit before a brief is treated as
  final (D5=B); routine claims do not.
- Any documentation, run log, or ADR text produced going forward must **stop
  using the phrase "production ready"** for anything beyond what Part 5 of
  the source review calls "externally exercised" (the currently justified
  level) until D7's next target ("externally validated") is actually met by
  satisfying the ratified D8 evidence bar for external repository-sensemaking
  briefs (not a workflow Step 2 / architectural-review pass) — this is a
  standing constraint on language, not merely a recommendation, per
  CLAUDE.md's existing verification-discipline rule.

None of the above has been implemented. This is a statement of what
*would* follow, for your review before any of it happens.

---

## Part 6 — ADR and issue mapping

| Decision | ADR | Issue | Needed action after approval |
|---|---|---|---|
| D1 | ADR 0014 | #29 | Narrow ADR 0014's "In scope" section to brief production only; ADR stays **Proposed** until you promote it |
| D2, D3, D4 | ADR 0015 (field classification), ADR 0016 (evidence/taxonomy-adjacent) | #30, #31 | Add `weakness_type` addendum to ADR 0015 (new controlled-vocabulary deterministic field); note the D4 resolution once made; both stay **Provisional** |
| D5, D6 | ADR 0016 | #31 | Ratify "which claims require evidence audit" threshold (D5); D6 has no ADR home yet — would need a new addendum or a new ADR if you want it documented, since no existing ADR covers human-review depth as a product-wide policy |
| D7, D8 | ADR 0021 | #36 | Update ADR 0021 with D7's next-target framing and, once D8 is resolved, the explicit external-validation bar; ADR stays **Proposed**, external-repo gap remains open until met |
| D9 | ADR 0016 (evidentiary precedent) | #31 (indirectly — supports the "which claims require evidence" discussion) | No status action; this is a factual interpretation of PR #78, useful as cited precedent in ADR 0016's "Supporting evidence" section if ADR 0016 is revised later |
| D10 | none directly — this is an implementation-scope decision, not a product-contract ADR | new implementation-tracking issue, **to be created only after D1/D2/D3/D9 are approved** | Nothing today; do not create the tracking issue until you've signed off |

No status is changed by this document.

---

## Part 7 — Owner response form

**Provenance correction, 2026-07-26**: an earlier revision of this document
copied a fully-filled-in response form and labeled it "RATIFIED." That form
was an assistant-authored example ("a reasonable owner response could look
like this"), not a response the owner personally entered or explicitly
approved. Treating an assistant's example as owner sign-off would be exactly
the "recommendation quietly becomes decision" failure this whole package
exists to prevent. That labeling has been corrected below.

**Assistant recommendations are decision support. They are not owner
authorization; only your own words in this file constitute that.**

### Recommended default package (from Part 4 — proposal only)

This is what the product-contract review and this package's own analysis
suggest, restated here for convenience. It is not a decision.

```markdown
- D1 Product boundary: A — Human-reviewed repository-analysis assistant
  producing a brief.
- D2 Weakness taxonomy role: B — Required metadata but non-blocking.
- D3 Weakness-type representation: B — Dedicated structured enum field.
- D4 Unknown weakness handling: unresolved in Part 4 (review hedges between
  B and D) — no default recommendation.
- D5 Substantive audit policy: B — Mandatory for absence, unreachability,
  dead-code, safety, ghost-feature, and other high-risk claims.
- D6 Human review depth: unresolved in Part 4 — no default recommendation.
- D7 Next readiness target: D — Externally validated (current justified
  level is C, already met).
- D8 External-validation bar: unresolved in Part 4 — no default
  recommendation.
- D9 PR #78 interpretation: B — Legitimate under the current contract, but
  evidence that the contract is overly brittle.
- D10 Next phase: A — Contract redesign limited to the brief artifact and
  its validators.
```

### Owner decisions

**RATIFIED 2026-07-26.** The owner approved the following in their own
words ("I approve the conservative package as follows..."), explicitly
leaving D7 and D8 open. This is the first genuine owner ratification in
this document's history — distinct from the earlier, corrected mistake of
treating an assistant-authored example as sign-off.

```markdown
## Owner decisions

- D1 Product boundary:
  A — Human-reviewed repository-analysis assistant producing an
  evidence-grounded brief.

- D2 Weakness taxonomy role:
  B — Weakness taxonomy is required metadata but non-blocking.

- D3 Weakness-type representation:
  B — Weakness type uses a dedicated structured enum field.

- D4 Unknown weakness handling:
  D — Allow `Other` with a required explanation; an unknown type must not
  invalidate the brief.

- D5 Substantive audit policy:
  B — Substantive audit is mandatory for absence, unreachability,
  dead-code, safety, ghost-feature, and other high-risk claims.

- D6 Human review depth:
  A — Human approval is required for every final brief during the next
  phase.

- D7 Next readiness target:
  D — Externally validated. **RATIFIED 2026-07-26 (later same day, following
  PR #81 closure)**, superseding the earlier UNDECIDED status recorded
  above. This does not itself advance the achieved readiness level, which
  remains "Externally exercised" until the D8 evidence bar is actually met.

- D8 External-validation bar:
  Success on at least two structurally different external repositories,
  including: clean structural Stage A validation; deterministic evidence
  grounding; substantive audit of every high-risk claim; no target-repository
  mutation; pinned framework and target revisions; repeatability evidence;
  and real human usefulness evaluation on at least one target. **RATIFIED
  2026-07-26 (later same day)**, superseding the earlier UNDECIDED status
  recorded above.

- Experiment authorization:
  E4 — staged plan. **RATIFIED 2026-07-26.** Only **Stage 1 planning**
  (controlled auteur rerun) is authorized now, via one GitHub issue (#83).
  **Stage 1 execution is not yet authorized** and requires a separate,
  explicit owner instruction issued after the owner reviews the final
  pinned revisions, model/provider configuration, environment, and exact
  command. Stage 2 (second structurally different repository — not workflow
  "Step 2"; that is an unrelated concept, see ADR 0021's D7 note) is
  conditional and unauthorized, gated on the owner reviewing successful
  Stage 1 evidence. Stage 3 (real-maintainer usefulness evaluation) is
  conditional and unauthorized, gated on the owner reviewing successful
  Stage 2 evidence. Any failed stage stops the sequence — the failure is
  preserved as evidence and returned to the owner; no automatic
  repair-and-rerun is authorized. **This planning-only boundary is a
  deliberate, explicit revision**: an earlier informal draft of this
  decision used the phrase "Stage 1 is authorized for execution now"; that
  phrasing is superseded and does not apply. The authorized boundary is
  planning only, as stated here.

- D9 PR #78 interpretation:
  B — PR #78 was a legitimate rejection under the current contract, but it
  also demonstrates that the current contract is overly brittle.

- D10 Next phase:
  A — Begin the contract-redesign phase, limited to the brief artifact and
  its validators.

## Modifications or constraints

- Do not rerun auteur during this phase.
- Do not expand into routing, task generation, Wayfinder integration, or
  broader orchestration.
- Preserve all historical evidence PRs unchanged.
- Do not weaken evidence integrity or target-write confinement.
- Keep ADR 0021 Proposed while D7, D8, and its remaining promotion
  conditions are unresolved.
```

**2026-07-26 update (later same day)**: D7 and D8 above, and experiment
authorization (E4, staged), have since been explicitly ratified by the
owner — see the updated D7/D8/Experiment-authorization entries above. This
supersedes the "Modifications or constraints" bullet "Do not rerun auteur
during this phase" only to the extent of authorizing *planning* for a Stage
1 controlled rerun (one GitHub issue); it does not authorize executing that
rerun, which still requires separate explicit owner instruction. All other
modifications/constraints above remain in force unchanged (no routing/
Wayfinder/broader-orchestration expansion, historical evidence PRs
untouched, no weakened evidence integrity or target-write confinement).

**Effect on Part 6's ADR/issue mapping**: D1 (ADR 0014's condition) is
ratified — promotable. D2/D3/D4 (ADR 0015's condition) are ratified —
promotable. D5 (ADR 0016's condition) is ratified — promotable; D9 is
recorded there too as ratified interpretive precedent, though it isn't
itself part of ADR 0016's promotion condition. D6 is ratified but has no
existing ADR home (Part 6 flagged this gap already) — recorded here, not
retrofitted into an ADR that doesn't cover it. **D7/D8 are now ratified**
(see the 2026-07-26 update above), but ADR 0021's promotion condition is
still not fully met — it stays Proposed, because its three other named
owner-decision items (cost/concurrency, supported-agent commitments,
platform scope) remain outstanding regardless of D7/D8's ratification.
