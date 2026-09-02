# Controller B — cycle result (Task B execution + closure assessment)

```
CONTROLLER:   B. Written 2026-09-02, after Task B implementation + validation.
IMMUTABILITY: preserves what Controller B concluded at the end of its cycle.
              Later CAMPAIGN-STATE.md versions may supersede; this file stays
              intact.
INPUTS:       controllers/B-reconstruction-and-selection.md (the pre-impl
              checkpoint, @ 4ccbc70); Task B commit b77ad04; local qualification
              runs; CAMPAIGN-STATE.md v5.
COMMITS:      B reconstruction+selection checkpoint : 4ccbc70  (pushed)
              Task B implementation                : b77ad04  (pushed)
              CAMPAIGN-STATE v5 + this file         : 7e3f451  (pushed)
              (a trailing SHA-backfill commit fills the two `<this commit>`
               references below + the §15 CI conclusions; no content change)
HANDOFF HEAD RECEIVED:  358b5a2   ORIGIN/MAIN AT CYCLE:  06a57d1  (no drift)
```

---

## 1. What Task B was, and why (recap — full rationale in the checkpoint)

**Selected boundary:** the *machinery half* of the development-direction
reconstruction surface (MG-7m). Task A (Controller A) gave `roadmap.md` and
`goal.md` prose "HISTORICAL / SUPERSEDED" headers and rewrote `STATUS.md` into a
current-direction + reconstruction-reading-path surface. But
`scripts/probe_relationships.py::_classify_doc_file` classifies documents from
**path signals only** ("no content analysis"), so it still returned `live` for
both files, and the version-drift probe still emitted their superseded `0.2.1` /
"Phase 2.3" claims as `conflicting_values` evidence against the declared
`0.2.2`. The human reconstruction surface and the deterministic drift machinery
that a fresh controller, CI, and `repo-sensemaker` all rely on **disagreed about
which documents are current** — a residual `CONTEXT_RECONSTRUCTION_COST_EXCESSIVE`
hazard and a known material contradiction between two surfaces Campaign 2
changed (acceptance condition 15).

**Why this and not the alternatives** (§13 of CAMPAIGN-STATE / checkpoint Part 2):
the staged-reveal minimality probe (B-ALT-1) is measurement, not product
advancement, and both Campaign 2 cycles would then be probes; the MG-6 write-up
(B-ALT-2) is largely already documented; human-surface cleanup (B-ALT-3) is
instance-by-instance, and touches an immutable artifact; Goal A (F-c) is
`OWNER_DECISION_REQUIRED`. B-ALT-4 was the only candidate at once *on the
central question*, *substantive implementation*, *naturally bounded*, *warranted
independent of the succession experiment*, and *a resolution of a contradiction
Campaign 2 itself introduced*.

## 2. What was implemented (`b77ad04`)

Deterministic-machinery change only. No new schema, gate, blocking finding type,
artifact type, workflow, hook, router, state machine, or registry field.

**`scripts/probe_relationships.py`:**
- `DOC_STATUS_MARKER_RE` — `<!--\s*doc-status:\s*(?:historical|superseded|archived)\s*-->`,
  case-insensitive. Three synonyms, all meaning "not a live current-state surface".
- `DOC_STATUS_HEAD_BYTES = 4096` — only the document head is scanned, so a
  mention deeper in the body (a doc that *documents* the convention, a quoted
  example) does not reclassify a live document.
- `_declared_doc_status(path)` — bounded head read; returns `"historical"` on a
  marker hit, else `None`; `OSError`-safe.
- `_classify_doc_file(rel, declared_status=None)` — when `declared_status` is
  set it wins over every path heuristic (the author stated the lifecycle
  directly). Pure-path callers (`_classify_doc_file(rel)`) are unchanged — the
  existing `test_classify_doc_file` needed no edit.
- `_discover_docs` computes the marker per file and passes it through.
- Module + function docstrings updated ("path signals, plus an explicit in-file
  `doc-status` marker").

**`roadmap.md`, `goal.md`:** one line — `<!-- doc-status: historical -->` — under
the H1, above Task A's blockquote. The prose header is untouched.

**`tests/test_probe_relationships.py`:** +4 regression tests —
- `test_classify_doc_file_explicit_marker_wins_over_path` (pure precedence; no I/O);
- `test_declared_doc_status_reads_marker_from_head_only` (synonyms,
  case-insensitivity, and a marker beyond the head window / as prose does **not**
  count);
- `test_discover_docs_honors_doc_status_marker` (a marked doc at a `live` path is
  discovered `historical`, is absent from `_live_sources`, is counted under
  `by_class["historical"]`);
- `test_version_drift_ignores_marker_declared_historical_doc` (a marked doc's
  stale version token does **not** enter the `conflicting_values` decision set,
  and the finding **re-appears** once the marker is removed).

`00-user-intent.md` was **not** touched (validated immutable `user_intent`
artifact — Task A's caution stands; recorded as DB-1/DB-3 deferred).

## 3. Validation (strongest available referees)

| Referee | Result |
|---|---|
| `python scripts/validate-repo.py` | exit 0 |
| `python scripts/probe-repo.py` + `validate-probe-report.py` + `gate_relationship_findings.py` | **PROBE_GATE: PASS** — 0 blocking. `roadmap.md`/`goal.md` observations (`:23/:85/:89/:115/:134`) **removed** from the `version` finding (30 → 27 observations); `by_class.historical` 481 → 483, `live` 180 → 179. No new blocking finding. |
| `python scripts/test-validators.py` | 78 PASS / 0 FAIL |
| core-assertions pytest (`test_repo_probes`, `test_probe_report_cli`, `test_probe_relationships`, `test_skill_distribution_probe`, `test_gate_relationship_findings`, `test_path_drift`, `test_cli`) | **103 passed / 1 skipped** (was 99/1 — the +4 are the new Task B tests) |
| every `probe_relationships`-dependent module (`test_probe_relationships`, `test_gate_relationship_findings`, `test_stale_accepted_adr_probe`, `test_validation_workflow_commands`, `test_repo_probes`, `test_probe_report_cli`) | **70 passed** |
| exact-head CI on `b77ad04` (PR #269, `pull_request` event) | to be observed after push — recorded in CAMPAIGN-STATE §15 |

**Pre-existing local failures (NOT introduced by Task B — reproduced identically
on the pre-Task-B baseline `4ccbc70` by `git stash`):**
`tests/test_validate_brief_json.py` (`FileNotFoundError` — Campaign 1's deferred
**D2b**); `tests/campaign_validation/test_installed_wheel_setup_skills.py::test_setup_skills_reports_drift_and_requires_force`
(wheel/install platform red); `tests/test_stage1_auteur_prep_package.py::NoPresentTenseEnforcementClaims::test_no_present_tense_runtime_enforcement_claims_in_changed_docs`
(platform red). All are green in Linux CI (the campaign-branch "Validator
Ecosystem" runs were green on `431ec43` and `358b5a2`).

**FO-5 (disclosed):** a broad local `pytest` sweep triggered `pip install -e .`
as a side effect, which regenerated a stale committed
`src/sensemaking_skills.egg-info/` (committed at 0.2.1; pyproject is 0.2.2) and
briefly blocked a `git stash pop`. Recovered with `git checkout -- src/…egg-info/`.
No campaign artifact affected; `b77ad04` contains only the 4 intended files.

## 4. What capability changed

**Product capability advanced:** *the machine-checkable half of repository-level
development-direction reconstruction.* An independent controller, CI's probe
gate, and `repo-sensemaker` now see `roadmap.md` and `goal.md` as historical —
matching Task A's human markings — so a successor no longer has to open those
files, notice the probe flagged them, and reconcile the flag against the prose
header on every reconstruction. "Which documents are current" moved from a
convention (prose a future edit can drift from) to a mechanically enforced,
CI-visible property. The probe's version/ADR drift evidence is also lower-noise
(five fewer false "current-state conflict" observations).

**General affordance added:** any document that becomes a point-in-time record
while keeping its path can now declare itself with one line, and the drift
machinery honors it — the failure *class* (a superseded doc silently stays
"live"), not just the `roadmap.md`/`goal.md` instances.

**Campaign capability advanced (CC-2, CC-3):** a genuinely fresh *controller*
reconstructed the campaign from durable sources, reverified, independently
selected a task partially rejecting the predecessor frontier, and executed a
real deterministic-machinery change with regression tests — complete semantic
controller succession at the honest evidence level the environment supports.

## 5. Did Controller A's frontier (F-a..F-d) survive?

| A's candidate | Disposition after Controller B's cycle |
|---|---|
| **F-a** "the reconstruction surface is a convention, not a tested capability across an independent controller" | **Partially exercised, not selected as a task.** Controller B *is* an independent controller and reconstructed direction from the (Task A) surface + the campaign tree without anchoring on the stale PyPI/GA framing. It is a *contaminated* test of the Task A product surface specifically (B also had the campaign durable tree the bootstrap names). A clean repo-only test was **not** run (would need a fresh sub-context; B-ALT-1 rejected). Task B then removed the machinery-vs-convention gap F-a's "convention" framing implied. |
| **F-b** "MG-6 untouched — product vs campaign-only" | **Partially resolved as a by-product** (CAMPAIGN-STATE §EC-4 / MG-6): machinery-consistency = product; succession provenance / isolation accounting / boundary comparison / checkpoints = campaign-only; durable *rationale* is reused, *facts* are reverified. No product need for a `CAMPAIGN-STATE`-shaped artifact demonstrated. Not made a standalone task (would risk "restates known facts"). |
| **F-c** "Goal A / A1 is owner/environment-blocked, no repo-code deliverable → `OWNER_DECISION_REQUIRED`" | **Confirmed.** Reverified against Issue #255 + `CONTEXT.md` + the 2026-08-31 reassessment. Not campaign work. |
| **F-d** "comparative minimality (EC-1) entirely untested" | **Still true; deliberately not addressed.** B rejected B-ALT-1 (a staged-reveal probe) as measurement-only that would leave Campaign 2 with no substantive implementation. EC-1 is preserved as an explicit ceiling (§19). |

So: A's frontier was **not** adopted as a command. F-c confirmed; F-a/F-b
partially dissolved by Task B + the §EC-4 note; F-d preserved as a ceiling.

## 6. Architecture hypotheses — strengthened / weakened / unchanged

| Hyp. | Assessment |
|---|---|
| **H1 Agent-owned semantic control** | **DEMONSTRATED (bounded).** Both Task A and Task B selections were made by controller judgment against evidence; no script, workflow, or Skill chose them. Controller B rejected parts of the predecessor frontier. Bounded by EC-2 / EC-3 (n=1 succession, same model family, process persistence unverified). |
| **H2 Durable artifact-mediated continuation** | **STRENGTHENED.** The A → B handoff carried mission, authority, three state planes, ceilings, and rationale across a genuinely fresh controller with only the allowed bootstrap; 12 consequential claims reverified true; corrections cosmetic. This is the *controller*-level continuation Campaign 1 explicitly did **not** establish (it had fresh *workers*). Still single-repo / short-horizon (EC-3). |
| **H3 Verification-bearing handoff** | **STRENGTHENED.** No `HANDOFF_FACT_TRUST_FAILURE`; the successor distrusted the `<...>` SHA placeholders and the "CI green on 431ec43 only" line, and reverified from `git`/`gh`. The durable state's own "facts here are CLAIMS; reverify" rule worked as designed. |
| **H4 Strategic outer loop** | **SUPPORTED, not formalized.** The outer loop (mission → capability state → gaps → frontier → bounded task) was carried by Markdown (`CHARTER.md` + `CAMPAIGN-STATE.md` + checkpoints) across the handoff without a schema. Its usefulness is campaign-scoped; **no product need for an equivalent artifact was demonstrated** (formalization rule; charter constraint 8). |
| **H5 Inner task loop** | **SUPPORTED.** Task B ran as decision → uncertainty → cheapest evidence (a live probe run + a source read) → one bounded responsibility → strongest referee → consequence → durable update, with no extra machinery. |
| **H6 Deterministic machinery stays mechanical** | **STRENGTHENED and exercised.** Task B *is* an H6 change: the probe classifier gained an explicit-declaration input; it still emits evidence, never a diagnosis — the model still interprets whether a flagged doc matters. No semantic strategy moved into a script. |
| **H7 Workflows remain optional bounded subgraphs** | **UNCHANGED.** No workflow was used or added. |
| **H8 Hooks unwarranted until a liveness failure exists** | **UNCHANGED.** No hook considered; no recurrent missed-continuation event. |
| **H9 Campaign state ≠ product state** | **STRENGTHENED.** §EC-4: the machinery-consistency finding is product; the succession record is campaign-only. The distinction held up under a second controller. |
| **H10 Rich-state continuation proves sufficiency, not minimality** | **HELD as a ceiling.** The Task A + Task B change set was *sufficient* for Controller B; strict minimality is untested (no comparative evidence); claim ceiling = "smallest currently supported candidate" (§19). |
| **Formalization rule** | **APPLIED, passed.** The marker mechanism cleared the gate: recurring state need (≥4 historical-in-place docs), stable semantics ("this file is a point-in-time record"), repeated omission (only `CHANGELOG.md` was caught before), mechanically useful boundary (`_classify_doc_file`). It stayed an opt-in marker + one function param — not a front-matter schema. |

No hypothesis was **refuted**. The one that most changed is **H2**: Campaign 1's
"fresh workers, not fresh controllers" limitation is now addressed at the honest
evidence level the environment supports.

## 7. Answer to the central campaign question (Controller B, honest level)

> *What is the smallest coherent product capability required for repository-level
> development direction to survive independent campaign-controller replacement
> and continue producing strategically warranted engineering work?*

**Supported as the smallest currently evidenced candidate (not strict
minimality):** a **current-direction Markdown surface** at a named, discoverable
location (`STATUS.md`, named by `CONTEXT.md`'s source-of-truth map) that states
*ratified / in-flight / deferred* plus the *highest-leverage next boundary*, each
pointing at its authoritative source; **an ordered "how to reconstruct current
direction" reading path** on that surface, including an explicit "do not anchor
on these" list; and **historical-in-place markings that the repository's own
deterministic drift machinery honors** (so a successor's probe run agrees with
the human surface rather than contradicting it). No schema, artifact type,
workflow, hook, router, registry field, or `repo-sensemaker` change was
warranted; Markdown plus one opt-in marker honored by one existing classifier
function sufficed.

**What is demonstrated:** this arrangement was *sufficient* for one genuinely
fresh controller (Controller B) to reconstruct direction, reverify, and
independently select + execute warranted engineering, on one repository, over a
short horizon, with the predecessor process still resident.

**What is not demonstrated:** strict minimality (EC-1 — no comparative /
staged-reveal / withheld-field evidence); scale (EC-3 — n=1 repo, n=1
succession); full isolation (EC-2 — same model family, predecessor process
persists, non-resumption is discipline not enforcement); `src/`-depth or
multi-surface implementation from durable state (EC-5, only modestly lifted);
production reliability (MG-4).

## 8. Closure assessment

Against the charter's **Closure rule** — "after the mandatory A → B succession
and two strategic cycles, answer the central question at an honest evidence
level and close when: succession evidence exists; substantive advancement
occurred or was legitimately ruled unwarranted; no remaining material gap is
needed to evaluate the Campaign 2 question; broader limits can be recorded as
ceilings/deferred/future questions":

1. **Succession evidence exists** — CC-2: a genuinely fresh controller took
   semantic control, reconstructed, reverified, and independently selected;
   isolation honestly classified (EC-2).
2. **Substantive advancement occurred** — Task A (development-direction
   reconstruction surface + verified boundary confirmation) **and** Task B (a
   real deterministic-machinery change with regression tests, naturally sized,
   resolving the acceptance-15 contradiction). Neither manufactured or enlarged.
3. **No remaining material gap is *needed* to evaluate the central question** —
   MG-1/MG-2/MG-3 addressed; MG-6 partially resolved; MG-7 (both halves)
   addressed on the candidate head. MG-4 (general autonomous development) and
   MG-5/EC-1 (strict minimality) are explicitly **out of scope** for the
   Campaign 2 question per the closure rule ("does not need to solve general
   autonomous repository development"; "minimality requires comparative
   evidence" is a ceiling, not a blocker).
4. **Broader limits recorded** — EC-1..EC-5, MG-4/MG-5/MG-8, DB-1..DB-3, and the
   isolation ceilings are all in CAMPAIGN-STATE.

**Controller B's disposition read: `CAMPAIGN_COMPLETE`** at an honest evidence
level. A Controller C handoff is **optional** and would add succession-count
evidence (n=2 → n=3) but would **not change the central answer** — so, per "Do
not perform another handoff merely to increase the count," it is not warranted.

**Controller B does not declare the campaign closed.** Campaign **termination is
owner-reserved** (`CHARTER.md` OWNER-RESERVED DECISIONS: "Terminating the
campaign"). Likewise the **merge of PR #269** and any ADR/publication it implies.
Both are recorded as **`OWNER_DECISION_REQUIRED`**. The final-report inputs (the
17-section format in the owner instruction) are assembled across
`CAMPAIGN-STATE.md`, `A-*` and `B-*` checkpoints, and this file; the owner (or a
Controller C, if the owner wants n=3 succession evidence) can produce the
terminal report and set the disposition.

## 9. State planes at end of cycle

```
INTEGRATED (origin/main)  : 06a57d1  — unchanged since campaign start. The
                            Task A + Task B limitations still describe main
                            (its probe still classifies roadmap.md/goal.md as
                            live; STATUS.md there is still the pre-Task-A file).
CANDIDATE (campaign head)  : 7e3f451 (+ trailing SHA-backfill) on campaign/durable-repo-self-development.
                            Product-surface delta vs main: STATUS.md, CONTEXT.md
                            (+1 row), roadmap.md, goal.md (Task A headers + Task B
                            marker), scripts/probe_relationships.py,
                            tests/test_probe_relationships.py.
                            Instrumentation delta: docs/campaigns/durable-repo-self-development/**.
SEMANTIC (CAMPAIGN-STATE)  : v5. Disposition read CAMPAIGN_COMPLETE; termination
                            + merge OWNER_DECISION_REQUIRED.
RATIFICATION               : nothing merged. Draft PR #269 only.
```

## 10. What Campaign 2 has and has not established (one-paragraph summary)

**Established:** (a) a genuinely fresh coding-agent *controller* — not just a
fresh worker — can, from durable Markdown sources + repository/GitHub evidence
and the allowed bootstrap alone, reconstruct a repository's development
direction, reverify the consequential claims (catching stale ones without acting
on them), independently select a strategically warranted task that rejects parts
of the predecessor's assessment, and execute a real deterministic-machinery
change with regression tests; (b) the durable state that made this work is a
*current-direction Markdown surface + a reconstruction reading path + historical
markings the drift machinery honors* — no schema, workflow, hook, router, or new
artifact type was warranted; (c) campaign-succession instrumentation is
distinguishable from product state and does not imply a product artifact.
**Not established:** strict minimality of that durable state (no comparative
evidence); behavior at scale (one repository, one succession, short horizon);
strong controller isolation (same model family; predecessor process persists;
non-resumption is discipline, not enforcement); `src/`-depth self-development;
production-grade reliability; and general autonomous repository development —
all recorded as explicit ceilings, not open threads that keep Campaign 2 running.
