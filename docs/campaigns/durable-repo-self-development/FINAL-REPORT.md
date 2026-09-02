# Campaign 2 Final Report — Durable Repository-Level Self-Development

```
DATE:        2026-09-02
BRANCH:      campaign/durable-repo-self-development  (base: origin/main @ 06a57d1)
PR:          #269 (DRAFT, not for merge) https://github.com/ThorStarlord/sensemaking-skills/pull/269
CAMPAIGN HEAD AT REPORT:  f4f2f11  (this report + the A/B comparison + CAMPAIGN-STATE v6 follow)
AUTHORITY:   non-authoritative campaign report. Merge of PR #269, ratification of
             any conclusion as product architecture, the nine
             workflow-system-disposition decisions, Goal A authorization, and
             formal campaign termination remain owner decisions
             (CHARTER.md "OWNER-RESERVED DECISIONS").
AUTHOR:      the lead Campaign 2 controller (the context that served as
             Controller A), writing the closure assessment after Controller B
             completed its strategic cycle and reached a legitimate terminal
             disposition. No A-* or B-* checkpoint was edited to produce this.
FORMAT:      OWNER-INSTRUCTION.md "Campaign 2 Final Report" (17 sections, one
             disposition).
SOURCES:     OWNER-INSTRUCTION.md; CHARTER.md; CAMPAIGN-STATE.md v6;
             STARTUP-PROVENANCE.md; controllers/{A-reconstruction-and-selection,
             A-task-A1-reconstruction-probe, A-handoff, B-reconstruction-and-selection,
             B-cycle-result, A-B-comparison}.md; independent re-verification of
             every consequential qualification claim at head f4f2f11.
```

---

## 1. Mission Outcome

**What product capability materially changed.** Repository-level
**development-direction reconstruction** — the ability of an independent
coding-agent controller (or human maintainer, or CI, or `repo-sensemaker`) to
determine, from durable repository + GitHub evidence alone, where product
development currently is and what the highest-leverage warranted development
boundary is. Before Campaign 2 this was reconstructible only by cross-reading
four scattered documents (~15 tool calls) with a real wrong-anchor hazard: the
self-declared "single living status summary" (`STATUS.md`) was stale by an
architecture era, and `roadmap.md` / `goal.md` / `CHANGELOG.md` /
`00-user-intent.md` all pointed at a superseded PyPI/GA/autonomous-router plan.
After Campaign 2 (on the candidate head): `STATUS.md` is a current
ratified/in-flight/deferred surface with an ordered "how to reconstruct current
direction" reading path and an explicit "do not anchor on these" list;
`roadmap.md` and `goal.md` carry historical markers **that the repository's own
deterministic drift machinery now honors**; `CONTEXT.md`'s source-of-truth map
names `STATUS.md`.

**What Campaign 2 established about durable repository-level self-development.**
A genuinely fresh coding-agent **controller** — not merely a fresh worker — can,
from durable Markdown sources + repository/GitHub evidence and a minimal
bootstrap alone: reconstruct a repository's development direction; reverify the
consequential handoff facts (catching stale ones without acting on them);
independently select a strategically warranted task that **rejects parts of the
predecessor's assessment**; commit that selection before any predecessor
feedback; and execute a real deterministic-machinery change with regression
tests. The durable state that made this work is Markdown — a current-direction
surface, a reading path, and historical-in-place markings honored by one
existing classifier function. No schema, new artifact type, workflow, hook,
router, state machine, registry field, or `repo-sensemaker` change was
warranted.

**What Campaign 2 did not establish.** Strict minimality of that durable state
(no comparative / staged-reveal / withheld-field evidence); behaviour at scale
(one succession, one repository, one day); strong controller isolation (same
model family; predecessor process persisted; non-resumption was discipline, not
environment-enforced); `src/`-depth or multi-surface self-development from
durable state (only a modest lift); production-grade reliability; general
autonomous repository development.

## 2. Starting State

- **Starting `origin/main`:** `06a57d1d182a32684275d343a9248429feedbfe6`
  ("Merge pull request #268 …"). Verified 2026-09-02 as the merge commit of
  PR #268 and as an ancestor of (in fact identical to) `origin/main` HEAD.
- **Campaign 2 base:** `06a57d1`. `origin/main` did **not** drift for the entire
  campaign (re-checked by both controllers; `git log 06a57d1..origin/main`
  empty).
- **What Campaign 1 already demonstrated** (merged in PR #268): responsibility-
  level, artifact-mediated continuation into a **fresh context** from a durable
  Markdown record, across six responsibility classes; verification-bearing (fresh
  contexts caught ~22 wrong/overstated record facts, none causing a wrong
  action). Its product-surface additions: the operating-map continuation
  subsection, the deterministic-machinery + hooks disposition in
  `decision-orchestration-boundary.md`, `docs/workflow-system-disposition.md`, a
  lazy `workflow_liveness` resolver. Disposition `CAMPAIGN_COMPLETE`.
- **What remained unproven** (Campaign 1's own words, carried into Campaign 2's
  charter): a fresh context taking the **complete semantic campaign-controller**
  role; cross-controller semantic continuation; more than one
  dispatcher/controller; general autonomous self-development; production
  reliability; broad implementation depth; strict minimality of the durable
  continuation state.

## 3. Strategic Task Trace

### Task A — Controller A

```
TASK:                         Establish whether repository-level development
                              direction is reconstructible by an independent
                              controller; classify any failure; deliver the
                              smallest warranted product change (or a verified
                              "no new mechanism warranted").
CONTROLLER:                   A
CAMPAIGN WARRANT:             directly on the central question ("what durable
                              information lets a fresh controller distinguish the
                              next strategically consequential capability from the
                              nearest defect"); bounded; reversible; does not
                              predetermine the solution; would remain warranted
                              even if succession were already solved.
USER / OPERATOR VALUE:        a fresh controller / maintainer reconstructs current
                              development direction from one named surface +
                              pointers, without synthesising 6+ documents or
                              anchoring on a stale plan.
ALTERNATIVE BOUNDARIES:       (1, selected) development-direction reconstruction
                              surface; (2) promote artifact-mediated continuation
                              to a product-offered pattern — thin, largely done by
                              Campaign 1; (3) verification-bearing handoff as an
                              explicit capability — folded into (1); (4)
                              repo-sensemaker brief as direction state — out of
                              ADR 0014 scope; (5) premise check — resolved as (1)'s
                              internal decision-changing uncertainty, not a rival.
DECISION-CHANGING UNCERTAINTY: is direction genuinely NOT reconstructible (change
                              warranted) or already cheaply reconstructible
                              (CAMPAIGN_PREMISE_INVALIDATED / frontier elsewhere)?
BOUNDED RESPONSIBILITIES:     A1 fresh-context reconstruction probe (a tool inside
                              Task A, run as a `general-purpose` sub-agent with
                              the Campaign 2 dir excluded); A2 decide the smallest
                              warranted change from A1 evidence; A3 implement on
                              the campaign branch; A4 validate; A5 update campaign
                              semantic state; A6 handoff.
PRODUCT CAPABILITY ADVANCED:  development-direction reconstruction — the
                              human-facing surface. STATUS.md refreshed into a
                              current-direction + reading-path surface; historical
                              headers on roadmap.md/goal.md; CONTEXT.md +1
                              source-of-truth-map row. Markdown only; no new
                              artifact/schema/Skill/workflow/hook/registry/src.
EVIDENCE PRODUCED:            A1 (controllers/A-task-A1-reconstruction-probe.md):
                              reconstruction possible but ~15 tool calls across 4
                              scattered documents with a wrong-anchor hazard;
                              failure classes CONTEXT_RECONSTRUCTION_COST_EXCESSIVE
                              (primary) + HANDOFF_FACT_INCORRECT (caught). NOT
                              premise-invalidation; NOT campaign instrumentation.
                              Qualified: validate-repo 0; probe gate PASS;
                              test-validators 78/78; core-assertions 99p/1s;
                              exact-head CI GREEN on 431ec43 (draft PR #269).
EVIDENCE CEILING REMAINING:   change unmerged (integrated main still carries the
                              limitation); comparative minimality untested (EC-1);
                              00-user-intent.md + CHANGELOG.md flagged not edited;
                              docs/ historical sprawl documented not archived; the
                              refreshed surface not yet tested by an independent
                              controller reconstructing *from it*.
```

### Task B — Controller B (fresh)

```
TASK:                         Give the probe engine's live-document classifier an
                              explicit, deterministic way for a document to
                              declare itself historical-in-place, and apply it to
                              the documents Task A marked in prose — so the human
                              development-direction reconstruction surface and the
                              deterministic drift machinery agree on which
                              documents are current.
CONTROLLER:                   B (genuinely fresh; bootstrap only)
CAMPAIGN WARRANT:             the *mechanically-enforceable* half of the exact
                              boundary Task A opened; a known material
                              contradiction between two product surfaces Campaign
                              2 changed (acceptance condition 15); "harden only
                              where pressured" with demonstrated *repeated*
                              pressure (roadmap.md, goal.md, CHANGELOG.md,
                              00-user-intent.md all went historical-in-place; the
                              classifier caught only one).
USER / OPERATOR VALUE:        running the probe engine on a repo whose maintainers
                              marked a document historical no longer emits "these
                              sources disagree about the current version" evidence
                              against that document; the machine-readable
                              live-document set matches the human-declared one; a
                              successor does not re-triage roadmap.md/goal.md every
                              reconstruction.
ALTERNATIVE BOUNDARIES:       B-ALT-1 staged-reveal comparative-minimality probe
                              (rejected: measurement, would leave the campaign with
                              zero substantive implementation); B-ALT-2 MG-6
                              product-vs-campaign write-up (folded in as a
                              cycle-result note — risks "restates known facts");
                              B-ALT-3 finish the human surface / CHANGELOG footer /
                              docs sprawl (rejected: instance cleanup, touches an
                              immutable artifact); B-ALT-4 (selected) the machinery
                              marker.
DECISION-CHANGING UNCERTAINTY: does existing machinery already honor Task A's
                              markings (drop the task) or not (change warranted)?
                              [verified live: NOT honored.] Is an opt-in marker the
                              smallest sufficient fix, or is a front-matter schema
                              / path move / name rule needed? [marker is smallest
                              and general.]
BOUNDED RESPONSIBILITIES:     B1 confirm the gap + fix the smallest surface
                              (scripts/probe_relationships.py); B2 apply the
                              marker to roadmap.md/goal.md (not 00-user-intent.md);
                              B3 regression coverage (+4 tests); B4 validate;
                              B5 update campaign semantic state (v5); B6 write the
                              cycle result + closure assessment.
PRODUCT CAPABILITY ADVANCED:  the machine-checkable half of development-direction
                              reconstruction. `_classify_doc_file` gained an
                              optional `declared_status` that wins over path
                              heuristics; `_declared_doc_status()` reads an opt-in
                              `<!-- doc-status: historical -->` marker from the
                              file head (4096 bytes; synonyms superseded/archived);
                              `_discover_docs` wires it through. Pure-path callers
                              unchanged. General affordance: any doc that becomes a
                              point-in-time record while keeping its path can now
                              declare itself in one line.
EVIDENCE PRODUCED:            controllers/B-cycle-result.md. `roadmap.md`/`goal.md`
                              leave the live set; their 5 stale version
                              observations drop from the `version` finding
                              (independently re-verified at f4f2f11: version
                              finding no longer cites roadmap/goal; 27
                              observations). Qualified: validate-repo 0; probe gate
                              PASS (0 blocking); test-validators 78/78;
                              core-assertions 103 passed / 1 skipped (+4 new);
                              probe_relationships-dependent modules 70/70;
                              exact-head CI GREEN on b77ad04 and 7e3f451 and
                              f4f2f11 (all ~20 "Validator Ecosystem" jobs).
EVIDENCE CEILING REMAINING:   change unmerged; the refreshed human surface was
                              never cleanly re-tested by an independent
                              repo-only reconstruction (B's own reconstruction saw
                              the campaign tree — a contaminated test); comparative
                              minimality still untested (EC-1); 00-user-intent.md
                              still historical-in-place with no marker (immutable
                              artifact — deferred); MG-8 (a hand-maintained
                              current-direction surface has no staleness signal of
                              its own) noted, not addressed.
```

## 4. Controller Succession Trace

### Controller A

```
CONTROLLER IDENTITY / CONTEXT:   the coding-agent context that received the owner
                                 instruction, ran the preflight, committed the
                                 bootstrap, and executed Task A. Model
                                 claude-sonnet-5 (Claude Code harness).
HANDOFF HEAD:                     358b5a23018048faa6d5aa46685281769854b4ea
ORIGIN/MAIN AT HANDOFF:           06a57d1 (no drift)
DURABLE SOURCES RECEIVED:         the owner instruction (as this session's task);
                                 Campaign 1's merged docs; the repository @ 06a57d1.
WHAT WAS RECONSTRUCTED:           product mission; integrated product state;
                                 ratified boundary (ADR 0014); Campaign 1 result +
                                 stated limitations; authority model; CI state.
WHAT HAD TO BE REDISCOVERED:      the scattered current-direction picture (CONTEXT.md
                                 "Current evidence strategy" + operating map +
                                 research agenda + campaign dir + issues #218/#226/
                                 #255); the fresh-controller mechanism's isolation
                                 limits.
WHAT REQUIRED REVERIFICATION:     PR #268 merge state and ancestry; origin/main SHA;
                                 CI green on 06a57d1; qualification commands.
WHAT PRIOR FACTS WERE STALE OR WRONG:  (from Campaign 1's own record) none
                                 consequential; roadmap.md/CHANGELOG.md/
                                 00-user-intent.md stale (this became Task A's
                                 subject).
PREDECESSOR FRONTIER ACCEPTED OR REJECTED:  n/a — Campaign 1 assessed no frontier
                                 for repository-level controller succession.
ALTERNATIVE CAPABILITY BOUNDARIES:  five, compared in
                                 A-reconstruction-and-selection.md Part 2.
TASK INDEPENDENTLY SELECTED:     Task A (development-direction reconstruction
                                 surface).
CHECKPOINT SHA:                  a216293 (reconstruction + selection, before Task A
                                 implementation).
HANDOFF PRODUCED:               controllers/A-handoff.md @ 358b5a2 (pre-handoff
                                 invariant 11/11; full provenance; verbatim
                                 bootstrap).
```

### Controller B (fresh)

```
CONTROLLER IDENTITY / CONTEXT:   a fresh `general-purpose` sub-agent context
                                 spawned via the Claude Code `Agent` tool with the
                                 verbatim bootstrap from A-handoff.md and nothing
                                 else. Model claude-sonnet-5 (same family as A;
                                 disclosed). Fresh context window; no shared
                                 transcript; no predecessor private reasoning.
HANDOFF HEAD:                     358b5a2  (received; re-verified)
ORIGIN/MAIN AT CYCLE:            06a57d1  (re-fetched; no drift; disposition
                                 CONTINUE AGAINST RECORDED BASE)
DURABLE SOURCES RECEIVED:         CHARTER.md + CAMPAIGN-STATE.md paths + the
                                 campaign directory + full repo + GitHub. Read
                                 OWNER-INSTRUCTION.md in full.
WHAT WAS RECONSTRUCTED:           mission; available + reserved authority; three
                                 state planes; demonstrated product + campaign
                                 capabilities; evidence ceilings; Task A's change
                                 and its rationale; material gaps; the recorded
                                 frontier.
WHAT HAD TO BE REDISCOVERED:      the probe engine's actual doc-classification
                                 behaviour (Part 3 — this became Task B's subject);
                                 the live `version` finding contents.
WHAT REQUIRED REVERIFICATION:     12 consequential claims (Part 0): origin/main +
                                 no drift; PR #268; commit range; PR #269/#194;
                                 issues #218/#226/#255; ADR statuses incl.
                                 0017–0021 SUPERSEDED-never-Accepted; Task A diff;
                                 Campaign 1's capabilities + limitation; local +
                                 CI qualification.
WHAT PRIOR FACTS WERE STALE OR WRONG:  N-1 (CI recorded for 431ec43 only; 358b5a2
                                 also green) and N-2 (three unfilled `<...>` SHA
                                 placeholders). Both cosmetic; no consequential
                                 fact was wrong. Verification caught them; no wrong
                                 action followed → HANDOFF_FACT_INCORRECT, not
                                 HANDOFF_FACT_TRUST_FAILURE.
PREDECESSOR FRONTIER ACCEPTED OR REJECTED:  PARTIALLY REJECTED. F-d rejected
                                 (measurement-only); F-c confirmed
                                 (OWNER_DECISION_REQUIRED); F-a/F-b folded in, not
                                 adopted as tasks. Task B selected within the same
                                 capability *family* but on the half A had not
                                 done, and it resolved a contradiction A's change
                                 introduced.
ALTERNATIVE CAPABILITY BOUNDARIES:  four, compared in
                                 B-reconstruction-and-selection.md Part 2
                                 (B-ALT-1..4).
TASK INDEPENDENTLY SELECTED:     Task B (machinery marker for historical-in-place
                                 documents).
CHECKPOINT SHA:                  4ccbc70 — committed BEFORE Task B implementation
                                 and BEFORE any predecessor semantic feedback.
HANDOFF PRODUCED:               none (Controller C not warranted). Cycle result:
                                 controllers/B-cycle-result.md @ 7e3f451.
```

## 5. Independence and Harness Assessment

```
LAUNCH MECHANISM:                Claude Code `Agent` tool, subagent_type
                                 general-purpose, single call, run in background.
ISOLATION EVIDENCE:
  - context isolation (no transcript, no predecessor private reasoning):
    HARNESS-REPORTED — the `Agent` tool starts the sub-agent cold; the parent
    session's transcript and thinking are not passed.
  - bootstrap minimality: CONTROLLER-ASSERTED — the prompt was authored to
    contain only mechanical locate-durable-state content and is preserved
    verbatim in A-handoff.md; no mission/rationale/frontier/gaps/next-task.
  - checkpoint immutability: CONTROLLER-ASSERTED — B's 4ccbc70 checkpoint was not
    amended; the predecessor recorded its SHA and did not touch it.
  - non-resumption: CONTROLLER-ASSERTED — the predecessor committed (in
    A-handoff.md, before the spawn) not to steer B and to treat any comparison
    as post-hoc; the retrospective (A-B-comparison.md) was written only after B
    completed.
  - predecessor process non-persistence: NOT ESTABLISHED — the predecessor
    process continued and received B's report through the `Agent` call →
    SUCCESSION_ISOLATION_UNVERIFIED on that dimension.
  - model independence: NOT ESTABLISHED — same model family (claude-sonnet-5).
EXACT BOOTSTRAP:                 controllers/A-handoff.md, "Verbatim bootstrap
                                 given to Controller B".
OUT-OF-BAND INFORMATION:         none beyond that bootstrap.
INFORMATION INTENTIONALLY WITHHELD:  campaign mission text; Task A rationale; the
                                 recorded frontier (F-a..F-d); the material-gap
                                 list; any recommended next task; predecessor
                                 predictions. (All were reconstructible from the
                                 durable sources the bootstrap pointed at — and B
                                 reconstructed them.)
WHETHER CHECKPOINT PRECEDED FEEDBACK:  YES — 4ccbc70 was committed and pushed
                                 before the predecessor gave any semantic
                                 feedback (the predecessor gave none until
                                 A-B-comparison.md, written after B's cycle).
WHETHER PREDECESSOR RETAINED SEMANTIC CONTROL:  NO — Controller A performed only
                                 the mechanical spawn; B selected and executed
                                 Task B with zero predecessor input; acceptance
                                 condition 19 holds.
KNOWN HARNESS LIMITATIONS:       same model family; predecessor process persists;
                                 checkpoint immutability + non-resumption are
                                 discipline, not enforcement; both controllers ran
                                 in the same worktree (sequentially, each from a
                                 clean committed state — no leftovers crossed).
STRONGEST DEFENSIBLE SUCCESSION CLAIM:  a fresh **controller** context, given only
                                 a minimal bootstrap, reconstructed the campaign,
                                 reverified the consequential facts, independently
                                 selected a task that partially rejected the
                                 predecessor's frontier, committed that selection
                                 before any feedback, and executed real qualified
                                 engineering — i.e. genuine transfer of semantic
                                 decision-making authority, with context isolation
                                 harness-reported and process/​model isolation
                                 explicitly unverified.
```

## 6. Integrated vs Candidate State

```
INTEGRATED (origin/main @ 06a57d1):  unchanged for the whole campaign. Its
  STATUS.md is still the pre-Task-A file; its probe still classifies
  roadmap.md/goal.md as live and flags their stale version claims. The
  reconstruction-cost limitation A1 measured still describes integrated main.
CANDIDATE (campaign/durable-repo-self-development @ f4f2f11):  8 commits over base.
  Product-surface delta vs main: STATUS.md, CONTEXT.md (+1 row), roadmap.md,
  goal.md (Task A headers + Task B marker), scripts/probe_relationships.py,
  tests/test_probe_relationships.py. Instrumentation delta: the whole
  docs/campaigns/durable-repo-self-development/ tree.
UNMERGED CHANGES:  all of the above. Nothing from Campaign 2 is on main.
RATIFICATION STATUS:  none. Draft PR #269 only. No ADR, contract, canonical
  vocabulary, registry, liveness overlay, or src/ change anywhere in the campaign.
WHICH CAPABILITY CONCLUSIONS APPLY ONLY TO THE CANDIDATE:  every "development
  direction is now reconstructible from a named surface" and "the drift machinery
  and the human markings agree" claim is TRUE on f4f2f11 and NOT on integrated
  main until an owner merge.
```

## 7. Implementation

Two coherent commit ranges on one cumulative branch.

- **Task A (`431ec43`)** — `STATUS.md` rewritten (+163/−25) into a
  current-direction + "Reconstructing current development direction" reading-path
  surface with an explicit do-not-anchor list; `roadmap.md` +7 and `goal.md` +10
  historical/superseded blockquote headers; `CONTEXT.md` +1 source-of-truth-map
  row. Markdown on existing surfaces only. Scope was **not** enlarged:
  `00-user-intent.md` (a validated immutable `user_intent` artifact) and
  `CHANGELOG.md` were flagged in `STATUS.md`, not edited; the ~45 loose
  historical `docs/*.md` were documented (a discriminator rule in `STATUS.md`),
  not bulk-archived.
- **Task B (`b77ad04`)** — `scripts/probe_relationships.py` (+45/−~10): a new
  `DOC_STATUS_MARKER_RE` + `DOC_STATUS_HEAD_BYTES = 4096` + `_declared_doc_status()`
  (bounded, `OSError`-safe head read) + an optional `declared_status` parameter to
  `_classify_doc_file` that wins over path heuristics, wired through
  `_discover_docs`; docstrings updated. **Pure-path callers are unchanged**, so
  the existing `test_classify_doc_file` needed no edit. `roadmap.md`/`goal.md`
  each get one `<!-- doc-status: historical -->` line. `tests/test_probe_relationships.py`
  +4 regression tests (marker precedence; head-window bound + synonyms +
  prose-not-counted; discovery honours the marker; version-drift excludes a
  marked doc and re-detects it when the marker is removed).

**Why the scope was naturally warranted, not manufactured.** Task A's decision-
changing uncertainty forced a bounded investigation first; its result (limitation
confirmed, small change sufficient) sized the change, not the other way round.
Task B's scope is the exact unfinished half of Task A's boundary plus the
regression coverage that makes it enforced; Controller B explicitly rejected the
larger front-matter-schema option and the instance-cleanup option. No `src/`
change was added "because Campaign 1 lacked one"; the `scripts/` change is where
the demonstrated pressure actually was.

## 8. Durable-State Assessment

| Information | Assessment |
|---|---|
| **Essential** | the mission text (CHARTER-derived); the authority grants + reserved list with sources; the three state-plane SHAs; the ceilings EC-1..EC-5; the failure-class vocabulary; Task A's rationale + A1's evidence (Controller B leaned on all of these). |
| **Saved material work** | the five-boundary comparison in `A-reconstruction-and-selection.md` (B did not re-derive it from scratch; it reused the *frame* and reverified the *facts*); the "reconstruction reading path" A1 produced. |
| **Redundant** | some restatement of Campaign 1's result across CHARTER / CAMPAIGN-STATE / A checkpoint (cheap to reconstruct from `docs/campaigns/agent-native-self-development/`). |
| **Became stale within the campaign** | the "CI green on 431ec43" line (358b5a2 also green — N-1); three `<...>` SHA placeholders (N-2). Both cosmetic; the durable state's own "facts are CLAIMS, reverify" rule handled them. |
| **Was wrong** | nothing consequential. Zero `HANDOFF_FACT_TRUST_FAILURE`. |
| **Required reverification** | every SHA; PR/issue/ADR state; qualification numbers; the probe engine's actual behaviour (Task B's whole premise). |
| **Cheaper to reconstruct than maintain** | the exact merged-PR list; per-ADR status (read the Status line at point of use); the live probe finding contents. |
| **Appears campaign-specific** | the controller-succession provenance; the isolation-limit accounting; the boundary comparisons; the checkpoints themselves. `CAMPAIGN-STATE.md` existing is **not** evidence the product needs an equivalent artifact (H9 held under a second controller). |
| **Appears product-worthy** | a current-direction surface at a named location + a reconstruction reading path + machine-honoured historical markings. This is exactly what Campaign 2 put on the candidate head, and no more. |

## 9. Strategic-Selection Assessment

- **Distinguished frontier from local defects?** Yes, explicitly, both times.
  Task A's gate names the nearby-defect framing ("STATUS.md and roadmap.md are
  stale, update them" — which Campaign 1 had classified no-action) and rejects
  it in favour of the capability framing. Task B's gate names its nearby-defect
  framing ("add roadmap.md to a skip list") and rejects it for the class-level
  affordance.
- **Considered real alternatives?** Yes — five (A) and four (B), each with
  plausibility, supporting evidence, and a warranted/not-warranted call. None
  were manufactured to fill the format.
- **Independently reassessed the predecessor?** Yes — Controller B treated
  F-a..F-d as "LAST ASSESSED CANDIDATE", rejected F-d, confirmed F-c, and
  selected a task the predecessor had not named (the machinery half).
- **Maintained user/operator value?** Yes — both tasks name a concrete operator
  (a fresh controller / maintainer; also CI and `repo-sensemaker` for Task B) and
  an observable value.
- **Avoided selecting work merely to satisfy the experiment?** Yes — Controller B
  explicitly rejected the staged-reveal minimality probe *because* it would have
  made the succession experiment "succeed" while producing no product
  advancement.
- **Where selection remained unstable / open:** Controller B's own reconstruction
  is a *contaminated* test of Task A's refreshed human surface (B also had the
  campaign tree); a clean repo-only re-test was not run. And the campaign did not
  test whether a *third* controller would again converge on the same capability
  family — n=1 succession only.

## 10. Minimality Assessment

```
WHAT STATE ARRANGEMENT WAS SHOWN SUFFICIENT:
  a current-direction Markdown surface at a named, discoverable location
  (STATUS.md, named by CONTEXT.md's source-of-truth map) stating ratified /
  in-flight / deferred + the highest-leverage next boundary, each pointing at its
  authoritative source; an ordered "how to reconstruct current direction" reading
  path with an explicit do-not-anchor list; and historical-in-place markings that
  the repository's deterministic drift machinery honours. Plus, for the campaign
  itself: CHARTER.md + CAMPAIGN-STATE.md + per-controller checkpoints (Markdown).
WHAT COMPARATIVE EVIDENCE EXISTS:
  none of the strict kind. No smaller-state candidate was tested; no staged-reveal
  reconstruction was run; no field was deliberately withheld to force a classified
  failure. Controller B rejected the optional minimality probe (B-ALT-1) with
  reasons (measurement-only; would leave the campaign with no substantive
  implementation; contamination risk).
WHAT WAS SHOWN REDUNDANT:
  only weakly — some cross-file restatement of Campaign 1's result; the "CI green
  on 431ec43" line once 358b5a2 was also green.
WHAT WAS SHOWN NECESSARY:
  by a real reconstruction failure: a machine-checkable historical signal — Task A
  built the human surface, and Controller B's cycle demonstrated that WITHOUT the
  machinery half a successor still re-triages roadmap.md/goal.md every run because
  the probe contradicts the prose. That is a genuine "a missing element matters"
  data point (owner instruction's minimality-evidence examples).
WHAT WAS NOT TESTED:
  a smaller durable-state arrangement; a repo-only (uncontaminated) reconstruction
  from the refreshed surface; whether any CAMPAIGN-STATE field is unnecessary;
  scale (n>1 succession, n>1 repo).
WHETHER STRICT MINIMALITY WAS DEMONSTRATED:
  NO. The supported claim is "smallest currently supported candidate" /
  "supported but not fully demonstrated". EC-1 stands.
```

## 11. Context-Cost Assessment

### A → (A1 fresh sub-context)

```
REPOSITORY REDISCOVERY:   the scattered current-direction picture — CONTEXT.md
                          "Current evidence strategy" + operating map + research
                          agenda + docs/campaigns/agent-native-self-development/
                          (the freshest strategic narrative) + the docs/ sprawl.
                          ~16 documents.
GITHUB REDISCOVERY:       issues #218/#226/#255 (live workstreams + their exact
                          boundaries); recent merged PRs for "what changed last".
DURABLE-STATE VALUE:      Campaign 1's CAMPAIGN-STATE.md capability table with
                          per-row evidence pointers — "the single most useful
                          current-state surface" the probe found.
REDUNDANT STATE:          ~45 loose historical docs/*.md; the stale root files.
DANGEROUS-TO-TRUST STATE: roadmap.md, CHANGELOG.md, 00-user-intent.md, the user
                          auto-memory — all point at a superseded PyPI/GA plan;
                          ADRs 0017–0021 look decided by title.
EXPENSIVE RATIONALE PRESERVED:  *why* the repo is in a "harden only where
                          pressured / do not build" posture (must read the
                          research-agenda meta-finding + Campaign 1 closure + the
                          Goal A substrate halt together).
```

### A → B (the actual succession)

```
REPOSITORY REDISCOVERY:   the probe engine's actual doc-classification behaviour
                          (Task B's whole premise — not in any durable summary);
                          the live `version` finding contents.
GITHUB REDISCOVERY:       PR #269 CI status per head; PR/issue/ADR landscape
                          (all reverified, all matched).
DURABLE-STATE VALUE:      the CHARTER + CAMPAIGN-STATE + A checkpoints carried the
                          mission, authority, three state planes, ceilings, and
                          Task A's rationale across the handoff with only cosmetic
                          staleness. The five-boundary *frame* saved re-derivation.
REDUNDANT STATE:          Controller B noted no material redundancy it had to wade
                          through; the durable state was "dense, not padded".
DANGEROUS-TO-TRUST STATE: the "CI green on 431ec43" line and the `<...>` SHA
                          placeholders — B distrusted both and reverified from
                          git/gh (this is the verification-bearing design working).
EXPENSIVE RATIONALE PRESERVED:  the five-boundary comparison and the Strategic
                          Selection Gate for Task A — Controller B reused the
                          frame and the alternative set rather than rebuilding
                          them, then made its own call.
```

(Qualitative only — no reconstruction was instrumented for precise
file/token counts beyond the sub-agents' self-reported ~15–22 tool calls.)

## 12. Failure Assessment

```
FO-1  CONTEXT_RECONSTRUCTION_COST_EXCESSIVE (product, mild)
  DECISION AFFECTED:            none (A1 reached a defensible answer).
  MISSING / STALE INFORMATION:  no single current-direction surface; the
                                source-of-truth map did not name where current
                                state lived.
  VERIFICATION OUTCOME:         A1 distrusted the stale surfaces and cross-checked.
  SMALLEST REPAIR:              STATUS.md refresh + a reconstruction reading path
                                (Task A). Machinery half: the doc-status marker
                                (Task B).
  RECURRENCE EVIDENCE:          first Campaign 2 measurement; Campaign 1 R1 showed
                                the analogous cost *with* a dedicated record.
  PRODUCT OR HARNESS:           product.
  INFRASTRUCTURE WARRANTED:     no — Markdown + one classifier param sufficed.

FO-2  HANDOFF_FACT_INCORRECT (caught)
  roadmap.md / CHANGELOG.md / 00-user-intent.md / auto-memory carry wrong
  consequential facts ("Phase 2.3 / v0.2.1 Beta / GA rollout" / "PRODUCTION
  READY"). The fresh context distrusted and cross-checked → no wrong action →
  HANDOFF_FACT_INCORRECT, not ..._TRUST_FAILURE. Repair: historical headers +
  markers on roadmap.md/goal.md (machine-honoured after Task B); the rest flagged
  in STATUS.md. auto-memory is not a repo file and cannot be fixed from the
  product.

FO-3  HANDOFF_STATE_CONTAMINATION-adjacent (harness, minor, disclosed)
  The A1 sub-agent's own broad Grep surfaced ~30 lines of the excluded Campaign 2
  directory. Disclosed; files not opened; visible lines agreed with independently
  reached conclusions. Immaterial. Lesson: scope Grep/Glob away from the excluded
  path in a future probe prompt, not only "don't open" it.

FO-4  probe false positive (non-blocking)
  A-task-A1-reconstruction-probe.md adds 2 non-blocking adr/status_claim_mismatch
  evidence findings — the probe reads a verbatim "ADR 0017 / 0021 ... never
  Accepted" quote as a claim of *accepted*. Gate PASSES (this type never blocks).
  Left as-is (verbatim evidence). No product or campaign consequence.

FO-5  harness hiccup (disclosed, Controller B)
  A broad local pytest sweep triggered `pip install -e .`, regenerating a stale
  committed src/sensemaking_skills.egg-info/ (0.2.1 vs pyproject 0.2.2) and
  briefly blocking a git stash pop. Recovered with `git checkout --`. No campaign
  artifact affected; b77ad04 contains only the 4 intended files.
```

No failure required new infrastructure. None was a `HANDOFF_FACT_TRUST_FAILURE`,
`CAMPAIGN_STATE_INSUFFICIENT`, `STRATEGIC_SELECTION_UNSTABLE`,
`AUTHORITY_RECONSTRUCTION_FAILURE`, `CAPABILITY_DISCOVERY_FAILURE`,
`BASELINE_DRIFT_MATERIAL`, or `CONTEXT_RECONSTRUCTION_COST_EXCESSIVE` of a
blocking degree.

## 13. Architecture Consequences

| Claim | Status |
|---|---|
| **Strategic outer loop** (mission → capability state → gaps → frontier → bounded task) as durable representation | **SUPPORTED BUT NOT FULLY DEMONSTRATED.** Carried by Markdown (CHARTER + CAMPAIGN-STATE + checkpoints) across the handoff without a schema; its usefulness is campaign-scoped; **no product need for an equivalent artifact was demonstrated.** |
| **Inner task loop** (uncertainty → bounded responsibility → evidence → validation → reassessment → closure) | **DEMONSTRATED (bounded).** Both tasks ran as this loop with no extra machinery. |
| **Durable artifact-mediated continuation** (H2) | **DEMONSTRATED at the *controller* level** for the first time (Campaign 1 had fresh workers): a fresh controller reconstructed + reverified + independently selected + executed from Markdown + a minimal bootstrap. Bounded by EC-2/EC-3 (n=1, same model family, process persists). |
| **Independent controller succession** | **DEMONSTRATED with recorded isolation limits.** Semantic decision authority transferred; checkpoint preceded feedback; predecessor did not resume control. Isolation: context HARNESS-REPORTED; process/model isolation UNVERIFIED. |
| **Campaign-state vs product-state distinction** (H9) | **STRENGTHENED.** Held under a second controller; the machinery-consistency finding was correctly classed *product*, the succession provenance *campaign-only*. |
| **Skill formalization** | **STILL HYPOTHETICAL / not warranted.** No recurring responsibility crossed the formalization gate; no Skill was created. |
| **Workflow role** (H7) | **UNCHANGED.** No workflow used or added; PR #268's bounded disposition not reopened. |
| **Deterministic machinery** (H6) | **STRENGTHENED and exercised.** Task B *is* an H6 change — the classifier gained an explicit-declaration input and still emits evidence, never a diagnosis. No semantic strategy moved into a script. |
| **Hooks** (H8) | **UNCHANGED / not warranted.** No recurrent missed-continuation event; no hook considered. |
| **Formal repository-development-state representation** | **NOT WARRANTED.** The evidence points the other way: Markdown on existing surfaces + one opt-in marker honoured by one existing function was sufficient. Formalization rule applied and *passed for the marker* (recurring need, stable semantics, repeated omission, mechanically useful boundary) — and it stayed a marker, not a schema. |
| **Strict minimality** (H10) | **HELD AS A CEILING — not demonstrated.** Sufficiency shown; comparative evidence absent. |

No hypothesis was **REFUTED**. The one that most changed is **H2**.

## 14. Qualification

```
EXACT CANDIDATE BRANCH / HEAD:   campaign/durable-repo-self-development @ f4f2f11
                                 (this report + A-B-comparison + CAMPAIGN-STATE v6
                                 add a further docs-only commit).
EXACT CURRENT origin/main:       06a57d1  (no drift for the whole campaign).
TARGETED TESTS (re-run by this author at f4f2f11):
  validate-repo.py .............. exit 0
  probe gate (probe-repo + validate-probe-report + gate_relationship_findings)
       ........................... PASS, 0 blocking; `version` finding no longer
                                   cites roadmap.md/goal.md (27 observations)
  test-validators.py ........... 78 / 78
  core-assertions + probe_relationships + stale-accepted-adr pytest
       ........................... 111 passed / 1 skipped
BROADER TESTS:
  Controller B ran the probe_relationships-dependent module set (70/70) and the
  core-assertions set (103 passed / 1 skipped, +4 new Task B tests).
VALIDATORS:                       validate-repo.py, test-validators.py, the probe
                                 engine + its report validator + the blocking-
                                 findings gate — all green on the candidate head.
BUILD / PACKAGE CHECKS:           CI's installed-wheel smoke jobs exercise the
                                 build; green on the campaign heads.
CI:                              "Validator Ecosystem" (~20 jobs) GREEN on EVERY
                                 pushed campaign head via draft PR #269's
                                 pull_request event: 431ec43, 358b5a2, 4ccbc70,
                                 b77ad04, 7e3f451, f4f2f11.
PR STATE:                         #269 OPEN, DRAFT, head f4f2f11, base main.
MERGE STATE:                      not merged. Owner decision.
INTEGRATED-MAIN STATE:            unchanged (06a57d1). The candidate's capability
                                 conclusions do not apply to main until merge.
REMAINING EXCEPTIONS (pre-existing on main; NOT introduced; reproduced on the
pre-Task-B baseline 4ccbc70; green in Linux CI):
  - tests/test_validate_brief_json.py (Campaign 1's deferred D2b — fixture drift).
  - tests/campaign_validation/test_installed_wheel_setup_skills.py::test_setup_skills_reports_drift_and_requires_force
    (wheel/install platform red).
  - tests/test_stage1_auteur_prep_package.py::NoPresentTenseEnforcementClaims::…
    (platform red).
  - src/sensemaking_skills.egg-info/PKG-INFO committed at Version 0.2.1 vs
    pyproject 0.2.2 (inherited from main; CI's "assert tree not mutated" jobs
    restore egg-info before checking; the probe's package.json version finding is
    the same class). Not Campaign 2's to fix.
```

## 15. Remaining Limitations

- **Product limitations.** The development-direction reconstruction surface is a
  *convention plus one machine-checkable signal*, exercised by one controller on
  one repository. `00-user-intent.md` is still historical-in-place with no marker
  (a validated immutable `user_intent` artifact — deferred). `CHANGELOG.md`'s
  "Deployment Timeline" footer is still misleading text (already
  `historical`-classified; flagged in STATUS.md). The ~45 loose historical
  `docs/*.md` are documented, not archived. `STATUS.md` itself has no mechanical
  staleness signal (MG-8) — the same failure mode can recur.
- **Engineering debt (deferred, pre-existing, none in CI).** D2b, the two
  platform reds, the stale `egg-info` version, and Campaign 1's D8/D17/D18/D19.
- **Unvalidated hypotheses.** That the durable-state arrangement is minimal (no
  comparative evidence); that a *third* controller would again converge on the
  same capability family; that the refreshed `STATUS.md` alone (no campaign tree)
  suffices for an independent reconstruction (B's test was contaminated).
- **Owner decisions (standing, not campaign blockers).** Merge of PR #269; any
  ratification of a Campaign 2 conclusion as product architecture; the nine
  `docs/workflow-system-disposition.md` §6 items; Goal A execution authorization;
  formal campaign termination.
- **Environment blockers.** None for Campaign 2. (Goal A's substrate blocker,
  Issue #255, is outside Campaign 2's scope — confirmed by both controllers as
  `OWNER_DECISION_REQUIRED`, not campaign work.)
- **Intentionally deferred.** The staged-reveal minimality probe; the human-
  surface instance cleanup (CHANGELOG footer, docs sprawl, `00-user-intent.md`);
  a `STATUS.md` staleness validator (MG-8 — premature; needs a demonstrated
  recurrence).
- **Campaign 2 experimental limitations.** n=1 succession; one repository; one
  day; two strategic cycles.
- **Harness limitations.** Same model family; the `Agent`-tool sub-agent returns
  its report to the parent (predecessor process persists); checkpoint
  immutability and non-resumption are discipline, not enforcement; both
  controllers used the same worktree (sequentially, clean).
- **Isolation limitations.** `SUCCESSION_ISOLATION_UNVERIFIED` on predecessor-
  process non-persistence and on model independence. A stronger variant (owner
  launches Controller B in a wholly separate session / different model) was
  offered and not exercised.
- **Minimality limitations.** No comparative evidence; claim ceiling is "smallest
  currently supported candidate".

## 16. Answer to the Central Question

> *What is the smallest coherent product capability required for repository-level
> development direction to survive independent campaign-controller replacement
> and continue producing strategically warranted engineering work?*

**SUPPORTED AS THE SMALLEST CURRENTLY EVIDENCED CANDIDATE** (not strict
minimality):

> A **current-direction Markdown surface** at a named, discoverable location
> (here `STATUS.md`, named by `CONTEXT.md`'s source-of-truth map) that states
> *ratified / in-flight / deferred* plus the *highest-leverage next boundary*,
> each pointing at its authoritative source; **an ordered "how to reconstruct
> current direction" reading path** on that surface, including an explicit
> "do not anchor on these" list; and **historical-in-place markings that the
> repository's own deterministic drift machinery honours**, so a successor's
> probe run agrees with the human surface instead of contradicting it.

Nothing heavier was warranted: no schema, artifact type, workflow, hook, router,
state machine, registry field, or `repo-sensemaker` change. Markdown plus one
opt-in marker honoured by one existing classifier function sufficed for one
genuinely fresh controller to reconstruct direction, reverify, and independently
select + execute warranted engineering.

Distinctions, stated plainly:
- **DEMONSTRATED SUFFICIENT:** the arrangement above, for **one** fresh
  controller, **one** repository, a **short** horizon, with the predecessor
  process still resident.
- **STRICT MINIMALITY DEMONSTRATED:** **no.** No smaller-state / staged-reveal /
  withheld-field comparison was run.
- **SUPPORTED BUT NOT FULLY DEMONSTRATED:** that the same arrangement scales to
  more successions / repositories / model families; that the `STATUS.md` surface
  *alone* (without the campaign tree) carries a clean reconstruction.
- **STILL HYPOTHETICAL:** any formal repository-development-state representation;
  Skill/hook/workflow formalization of the outer loop.
- **REFUTED:** nothing.

## 17. Campaign Disposition

```
CAMPAIGN_COMPLETE
```

**Why.** The charter's closure rule is met: (1) the central question is answered
at an honest evidence level (§16); (2) controller-succession evidence exists —
a genuinely fresh controller took semantic control, reconstructed, reverified,
independently selected against the predecessor's frontier, checkpointed before
feedback, and executed qualified engineering (§4, §5, `A-B-comparison.md`);
(3) substantive product advancement occurred — Task A (development-direction
reconstruction surface + a verified boundary confirmation that was *not*
premise-invalidation) **and** Task B (a real deterministic-machinery change with
regression tests, naturally sized, resolving the acceptance-15 contradiction Task
A introduced); (4) no remaining material gap is *necessary* to evaluate the
Campaign 2 question — MG-1/MG-2/MG-3 addressed, MG-6 partially resolved, MG-7
(both halves) addressed on the candidate head; MG-4 (general autonomous
development) and MG-5/EC-1 (strict minimality) are explicitly out of scope per
the closure rule; (5) the broader limits are recorded as evidence ceilings and
deferred work (§15), not open threads.

Acceptance conditions (charter): 1–9, 11, 19 **met** by the A→B succession and
Controller B's checkpoint-before-feedback; 10 **met** (Task A + Task B,
naturally sized); 12 **met** (both selections distinguished the frontier from
nearby defects); 13 **met** (no premature infrastructure — Markdown + one marker;
formalization rule applied and passed *as a marker*); 14 **met** (Controller B
narrowed/dissolved parts of Controller A's frontier); 15 **met** (Task B
resolved the contradiction Task A introduced; independently re-verified —
`version` finding no longer cites roadmap/goal); 16 **met** for a qualified PR
head with pre-existing exceptions classified; 17, 18 **met** (this section and
§10/§15/§16 state the ceilings; no strict-minimality claim is made).

It is **not** `OWNER_DECISION_REQUIRED` as a disposition: no safe bounded
campaign work is *blocked* by an owner decision. The residual owner actions
(merge PR #269; ratify any conclusion; the nine disposition items; Goal A
authorization; formal termination) are the repository's standing
integration/ratification boundary — the same boundary that closed Campaign 1 —
not a campaign blocker. It is **not** `EXTERNAL_BLOCKER` (the fresh-controller
experiment ran) and **not** `CAMPAIGN_PREMISE_INVALIDATED` (the premise held:
development direction did **not** cleanly survive independent reconstruction from
the product's designated surfaces, and a small Markdown + machinery change made
it do so for one fresh controller).

**A Controller C handoff is not warranted** — it would add succession-count
evidence (n=2 → n=3) but would not change the central answer, and the owner
instruction forbids another handoff "merely to increase the count".

**Owner-reserved, carried forward:** merge of PR #269; whether to ratify the
`STATUS.md` / `doc-status` marker convention as product architecture; the nine
`docs/workflow-system-disposition.md` §6 decisions; Goal A execution
authorization; and the formal act of terminating Campaign 2.
