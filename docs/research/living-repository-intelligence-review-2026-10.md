# Living Repository Intelligence: Adversarial Review and Architecture Synthesis (2026-10)

**Status:** analysis record and proposed amendments; **not ratified**
**Authority:** research only. Does not supersede ADR 0030 or
[`../repository-grounding-plan.md`](../repository-grounding-plan.md). Part II
proposes amendments to that plan; it is not a parallel roadmap.
**Evidence as of:** `main@758bd85` (PR #540 merged), GitHub state read 2026-10-14.
**Evidence class:** repository and GitHub inspection, plus two local CLI runs.
No new agent trial was run.

## 0. Summary

Three texts were reviewed:

- **T1**, "Critical analysis: from repository knowledge to autonomous
  engineering". This is a skeptical review with a P0-P4 roadmap.
- **T2**, a revision that concedes T1's skepticism and argues for continuous
  documentation and a detailed ontology.
- **T3**, "Living Repository Intelligence", a 7-phase implementation plan
  built on T2.

**Verdict.** The direction holds: agents should use product understanding to
choose and build worthwhile improvements under delegation. **The plan does not
hold.** Its flagship pilot targets knowledge that the repository's own
evidence says agents already get from code. It re-plans guidance that PR #540
already shipped. It adds an unbudgeted knowledge store that works around ADR
0030. It does not plan for the three external blockers that have actually
held up evaluation. And T2's reversal of T1 is not backed by any new evidence.

The repository's evidence points to a narrower lever:
**unrecorded decisions, not missing structure.** Part II therefore proposes a
*decision-first* design. Every change is an amendment to existing primitives:
an admission test for knowledge, a delegated-decision ratchet, a
citation-on-use convention, and separate evaluations for cold-start and
accumulation. It adds no new runtime, schema, tag, Skill, or validator.

---

# Part I: Adversarial review

## 1. Currentness defects in the reviewed texts

Each claim was checked against the repository or GitHub on 2026-10-14.

| Claim in T1/T2/T3 | Actual state | Consequence |
| --- | --- | --- |
| PR #536 is open and its comparison should be reused (T1 section 7, T3 Phase 0.7 and Phase 5) | **Closed, not merged**, 2026-10-14. The owner closed it as superseded by PR #540 and the canonical grounding plan. The three-arm study **was never executed**. | T3 Phase 5 builds on a closed plan. |
| The grounding plan's status predates the merged pack (T3 Phase 0.1) | PR #540 already reconciled `repository-grounding-plan.md`. Three stale statements remain: the ADR 0030 amendment still says the pack is "not merged" and "owner review has not happened"; a `STATUS.md` bullet says "No Skill, contract, or Level-4 strategy text has changed yet"; and `grounding-pack-build-001.md` says both "COMPLETE by owner directive" and "can't be called complete" in one paragraph. | Small currentness repairs. They are not a phase. |
| Phase 0.2-0.4, Phase 2 (retrieval) and Phase 3 (learning loop) are future work | PR #540 already ships them as guidance. `using-sensemaking` section 0 covers selective retrieval, source verification, "no exhaustive ontology", and same-change updates after construction. `strategic-sensemaking-loop` updates affected grounding facts after consequential work. `product-strategy.md` now names "continuous, autonomous domain grounding". | **The guidance for T3 Phases 0, 2, and 3 is already merged.** What is missing is behavioral evidence, not guidance. |
| `validate` CLI misreports success (T1 P0, T3 Phase 0.6) | **Confirmed.** `sensemaking-skills validate --artifact <malformed> --json` prints usage instructions as text and exits **0**. `docs/cli-contract-v1.0.yaml` declares `artifact_invalid: 5`, `artifact_validator_error: 6`, and one JSON object on stdout. On the same file, `scripts/validate-brief.py` returns `valid: false` and exits 1, which also differs from the contract's 5. `tests/test_cli.py` covers only help, missing, and nonexistent paths. | Real defect, but independent of the strategy (see B13). |
| The installed Skill differs from the GitHub version (T1 P2, T3 Phase 0.5) | **Confirmed, and larger than stated.** The #515 comment of 2026-10-14 reports installed/source sizes of 46,936/40,325 characters for `using-sensemaking` and 15,240/18,209 for `strategic-sensemaking-loop`. | Any attribution-sensitive trial must byte-verify first. |
| 51 Skill packages; 18 read-only episodes with 0 clearly Skill-favorable tasks; replay and stress-test findings | Correct. | None. |

## 2. Where it breaks

Findings are ranked by severity. Each one names what breaks, the evidence,
and the repair.

### B1 (High): the flagship pilot targets knowledge agents already derive from code

T3 Phase 1 builds a relational map of Copy Essence generation and Trait
effects. The repository already tested a fresh agent on **this exact domain**
(`historical-replay-study-2026-10.md`, "Fresh-session usability test"):

- The agent got the mechanics from code without asking: the rate function, the
  per-Copy formula, the files that apply it, and the authority rule.
- It still needed a human for three **unrecorded decisions**: the stacking
  rule, whether the request is in Campaign One scope, and whether the effect is
  Copy-only or permanent. It also needed balance numbers.
- It found four **doc/code contradictions**: "multiplicative" naming over an
  additive sum; "qualifying" Copies versus any Copy at maturity 100 or more;
  `ESSENCE_GENERATION_BONUS` documented but never read; and a shadowed constant.
- The record's own conclusion: "The next useful step is an owner decision on
  those three questions ... rather than more pack content."

T3's own stop rule ("stop if the map merely repeats existing documentation
and code") is therefore **predicted to fire by evidence T3 cites**.

**Repair.** Replace Phase 1 with *decision closure* on the same domain:

- record the four contradictions as invariants or traps;
- close the stacking and Copy-only/permanent questions through the
  delegated-decision ratchet (Part II, D3);
- send the scope question to the owner.

### B2 (High): an unbudgeted second store works around ADR 0030

T2 says "I would not impose an arbitrary limit on conceptual detail". T3 keeps
the pack compact but lets "deeper relational knowledge become as
sophisticated as the domain warrants".

ADR 0030 decision 4 is explicit: budgets are hard limits, and over-budget
files are cut or merged, not supplemented with new files. The canonical plan
already has the right trigger for format change: the format is revised when
the pack cannot stay within budget without dropping lines the owner considers
essential. "As the domain warrants" has no operational test.

The baseline that test would have to resist: `docs/` holds 507 Markdown files
and about 720k words. 132 of the 243 commits since 2026-09-01 are `docs:`
commits.

**Contradicts ADR 0030 decision 4** (flagged per `docs/agents/domain.md`).

**Repair.** Admit knowledge entry by entry, through a decision-changing test
(D1), and keep the budgets. Hitting budget pressure while dropping
owner-essential lines is the only evidence that would justify a separate
relational layer.

### B3 (High): T3 re-plans shipped work and leaves the real blockers unplanned

Every evaluation phase (T3 Phases 4-6) depends on three things T3 does not own
or plan for:

1. **An admissible target.** #515 has been `UNPINNED` since 2026-10-04 and was
   re-audited on 2026-10-14. Auteur has about 77 open Studio PRs; Metamorfose,
   The-Long-Continuity, and atlas-midgard are in flight.
2. **An independent coding-agent runner.** Per #515 (2026-10-14), no
   independently launched coding-agent context was available in the operator
   workspace. The replay study found that a shared `node_modules` leaked
   between arms.
3. **Human product evidence.** External playtesting was approved as
   "DEFERRED / TBD" with no owner and no date.

**Repair.** Make these three blockers the critical path, with the cheapest
unblocking step for each (Part II, section 11).

### B4 (High): T2 reverses T1 without new evidence

T2 says "my earlier emphasis on the danger of documentation theater
underweighted ...". No observation was added between T1 and T2. The concession
follows argument, not data. T3 then builds a seven-phase program on the
conceded position.

The repository's claim-ceiling discipline exists to stop exactly this. T1's
skepticism was calibrated to the stress test, the replays, and the usability
test, and that evidence has not changed.

**Repair.** A stance changes only when an observation changes. Each position
should state the observation that would move it. Part II, section 6 does this
for its own thesis.

T2's real contributions are framing, not evidence: a working definition of
learning, and "retrieve, don't inject".

### B5 (Medium-High): cold-start grounding and cumulative learning are conflated

T1's "demanding test" and T3 Phase 4 require an **unfamiliar** repository.
The thesis, however, is **accumulation**: later decisions improve because
earlier work taught something. One test cannot measure both.

Accumulation needs **successive ordinary tasks on the same repository**. That
also avoids the admission bottleneck in B3: a series of real tasks does not
need a "fresh, unused, multi-responsibility mission".

**Repair.** Run separate tests (E1 and E2 in Part II).

### B6 (Medium): the key metrics have no collection method

T3 lists "decisions materially changed by retrieved repository knowledge" and
"consequential belief updated" as measures. It defines no way to observe
either during normal use.

T3's Phase 3 exit ("a subsequent agent ... avoid[s] a repeated mistake") is
unfalsifiable at n=1 without a counterfactual. The probes would again be
written by the agent that wrote the knowledge, a bias the stress test already
recorded.

**Repair.**

- **Citation-on-use** (D4): log a decision that a grounding entry changed at
  the moment it happens.
- **Trap replays** built from *real incidents* (recurring ones where
  possible), not designed probes. Candidates:
  - the base-advance merge-qualification boundary, observed twice (#218);
  - stale CI selectors after wording-test removal (#537/#538);
  - the multiplicative/additive contradiction.

### B7 (Medium): the success criterion rewards invented work

T3 rewards "a worthwhile improvement that the user did not explicitly
prescribe". `product-strategy.md` lists *inventing work* as a failure mode.
Without a discriminator, these two collide.

In addition, the completion criteria (section 12) include product-value
judgments that need human evidence the owner has deferred. As written, the
program may never be completable.

**Repair.** An unprescribed improvement counts only if two things hold:

- it traces to a recorded goal or non-goal;
- it survives owner acceptance, blind where possible.

Separate the agent-checkable criteria from the human-required ones. The
minimal human ask is a **blind preference between two diffs**, which takes
minutes. It is not a playtest.

### B8 (Medium): decision rules have no pre-registered thresholds

"Expand when demonstrably better" with n of 1-3 lets the result be read after
the fact. The repository already has a precedent: the trial program used a
pre-registered "skill-favorable on at least 2 of 3" bar.

**Repair.** Pre-register the bar before running anything (section 12).

### B9 (Medium): the guidance cost is not netted against "simplify hard"

PR #540 grew the four core Skills by about 370 words:

| Skill | Before | After |
| --- | --- | --- |
| `using-sensemaking` | 5,130 | 5,287 |
| `repo-sensemaker` | 4,806 | 4,840 |
| `strategic-sensemaking-loop` | 2,271 | 2,352 |
| `strategic-repository-analysis` | 3,064 | 3,164 |

The owner-ratified verdict is **simplify hard**, and the grounding plan's
Phase 4 targets a core of at most 1,500 words. T3 Phase 2 would add further
retrieval guidance.

**Repair.** Apply a word-neutral rule: any guidance added pays for itself
with deletions until the Phase 4 target is met.

### B10 (Medium): duplicate evaluation tracks

- T3 Phase 4 (multi-step mission with a fresh-context handoff) duplicates
  Trial 002/002R (#515). #515 already has stricter agreed controls: an
  unannounced break, a separate context, and byte-verified installed Skills.
- T3 Phase 5 revives the closed #536.

**Repair.** Use 002R as the only continuation test. Keep the
compact-guidance comparison optional, as #536's closing note says.

### B11 (Low-Medium): mission state has no promotion rule

T3 correctly says temporary mission state must not become permanent product
truth. It does not say what happens to durable discoveries made *inside* a
mission. When the Campaign or handoff is archived, they are lost.

**Repair.** Ask one promotion question at mission close (D4).

### B12 (Low): a typed relationship vocabulary invites schema growth

The relationship types (`supports`, `constrains`, `depends_on`, ...) mix
structural facts with causal product claims. A typed vocabulary attracts a
validator with no consumer, which breaks the `CLAUDE.md` rule that validator
rules must trace to real consumers. T3 also coins new names ("Living
Repository Intelligence", "Layers A-D") for existing concepts (Grounding
Pack, Campaign, handoff). That goes against the glossary rule in
`docs/agents/domain.md`.

**Repair.** Keep prose. State causal claims as `[hypothesis]` lines with a
falsifier (D2). Use the glossary vocabulary.

### B13 (Low strategic, real defect): the `validate` CLI belongs in its own fix

T1 and T3 are right about the defect (section 1) but file it as "P0" of a
knowledge roadmap. It is an independent trust defect, and finding it does not
make it part of the strategy.

**Repair.** A standalone PR:

- delegate to the existing brief validator;
- map results to the contract's exit codes 5 and 6;
- emit JSON on `--json`;
- add malformed-artifact tests.

## 3. What survives

| Source | Keep |
| --- | --- |
| T1 | **Causal hypotheses, not just relationships** (the strongest idea across all three texts). The bottleneck taxonomy. "The highest-value knowledge is intent, decisions, and exceptions that cannot cheaply be reconstructed." Future reuse as the admission criterion. "Autonomy eliminates unnecessary dependence on human *direction*, not on human *evidence*." Continue reversible work and preserve alternatives. Three senses of "learning". Do not hide the answer in the pack. |
| T2 | Learning means new evidence changes a later judgment, as a four-step update. Documentation counts only if it changes the ability to predict, decide, or act. Retrieve; do not inject. |
| T3 | Four *logical* knowledge kinds (not files). "Long-term product knowledge survives the mission; temporary mission state does not." The comparison controls: separate installs, no future leakage, verified Skill identity. The risk register. "No work package is automatically a reason to add a Skill, schema, validator, or CLI command." |

## 4. The bottleneck question, against the evidence so far

T1 rightly says the "repository knowledge is the principal bottleneck"
premise is not established. Here is the evidence tagged by *binding
constraint*, meaning what actually limited progress.

| Observation | Binding constraint | Was missing derivable or relational repository knowledge binding? |
| --- | --- | --- |
| Synthetic stress test, 4 probes x 2 arms | None. Existing target docs already guarded every trap. | No |
| Historical replays, 2 tasks x 2 arms | None. The tasks were fully specified. | No |
| Fresh-session usability test (Copy Essence) | Three **unrecorded decisions**, plus doc/code contradictions | No for mechanics; **yes for decisions** |
| Auteur assessment | External product evidence | No |
| Trial program and remeasure (3 + 18 episodes) | Judgment and escalation calibration | No |
| Trial 002/002R (#515) | Target admission and an independent runner | No |
| Dark Factory #83 (#218, 2026-10-14) | Provider transport and observability | No |

**Claim ceiling.** None of these was designed to detect a knowledge
bottleneck. Most are synthetic, and the target repositories are unusually well
documented. Even so, there are **zero** observations where missing relational
structure was binding. There is **one** where missing *decisions* were, and
the rest were limited by external evidence, infrastructure, or authority.

---

# Part II: Architecture synthesis (PRD/spec)

## 5. Problem

Under delegation, a capable coding agent working in a well-documented
repository stalls or escalates mainly at **decision gaps**: owner intent
nobody recorded, choices nobody made, alternatives rejected without a written
reason, and traps learned once but not kept. Each gap costs an owner question,
or risks invented intent. Today the Grounding Pack records owner *answers* but
offers no legitimate way to *close* a gap without the owner. Nothing records
whether a pack entry ever changed a decision.

## 6. Thesis (falsifiable)

**H1 (adopted as the working hypothesis).** For delegated product work in
documented repositories, autonomy is limited more by unrecorded decisions and
by external evidence or infrastructure than by missing derivable or relational
structure. The grounding lever is therefore **decision closure plus decision
memory**. Relational knowledge is admitted only where it changes a decision.

**H1 is weakened by:**

- binding-constraint tags (section 11, E1) that show *relationship
  misinterpretation* binding in a material share of real episodes; or
- a paired comparison in which a relational-map arm beats a decisions-only arm
  (E4).

**H2 (the T2/T3 thesis, kept open).** A richer relational model materially
improves decisions. H2 is tested only when H1's evidence points to
misinterpretation (E4).

## 7. Users and job

**Primary user:** the high-delegation repository owner (`product-strategy.md`,
section 3).

**Job:** "Let the agent keep building toward my goal without asking me
things it could legitimately settle. Show me what it settled, so I can
overturn it cheaply."

## 8. Design

The design reuses existing primitives throughout. Retrieval is **unchanged**
(it shipped in PR #540).

### D1: Knowledge unit and admission test

Every grounding entry must answer four questions. This covers intent lines,
invariants, decision records, and any relational note.

1. **Decision:** which future decision does it change?
2. **Non-derivability:** why would a competent agent not recover it from
   code, tests, or docs in a few minutes?
3. **Source:** what single primary provenance tag supports it, and has the
   source's *content* been checked, not only its path?
4. **Recheck:** what change would invalidate it?

An entry that fails any question is not recorded. If it is mechanically
checkable, write a test instead. Relational content lives in `decisions/` or
`context.md`, under the existing budgets.

### D2: Claim kinds

The six existing tags stay. Causal product claims are `[hypothesis]` lines
with a one-clause falsifier ("weakened by: ..."). A hypothesis may motivate a
reversible prototype. It never justifies an irreversible change on its own
(this is existing rule).

### D3: Delegated-decision ratchet (amends ADR 0030 decision 5)

When delegated work hits an owner-dependent question:

1. **Search existing records.** This is the current ratchet. If an applicable
   decision exists, use it.
2. **Reversible, inside the delegated objective, and not protected.** The
   agent decides. It writes `decisions/NNNN-*.md` tagged
   `[delegated: date]`, with the rejected alternatives, the reason, and the
   reversal cost. It adds one line to the open decisions in `intent.md`
   ("delegated, awaiting confirmation"), then continues.
3. **Irreversible, value-laden beyond the delegation, or protected**
   (scope boundaries, merge, release, deploy). The agent asks the owner and
   keeps doing independent reversible work in the meantime. The answer is
   recorded as `[owner: date]`.
4. **Blocked on external evidence** (for example, balance numbers). The
   question is recorded as open. Nothing is invented.

The owner reviews delegated decisions **asynchronously and in batches**.
Confirming one upgrades its tag to `[owner: date]`. Reversing one records the
reason, which becomes a high-value intent line.

**Worked example (Copy Essence):**

- Make the naming and docs match the additive code. This is a delegated,
  behavior-neutral change, and the agent records "multiplicative was intended"
  as a `[hypothesis]` for the owner.
- Copy-only versus permanent effect: delegated, if it can be prototyped
  reversibly.
- Campaign One scope: owner.
- Balance numbers: blocked on external evidence.

### D4: Learning as promotion at transitions

- **At each PR.** Ask one question: "Did this produce a decision-changing,
  non-derivable fact, or invalidate an entry?" If yes, update it in the same
  PR. If no, change nothing. This is already the guidance.
- **Citation-on-use.** When an entry changes a decision, the PR description
  says so in one line: `Grounding used: <entry> -> chose X over Y`. Its
  consumers are the retain/simplify decision (plan Phase 4) and E1. It needs
  no validator and no schema.
- **At mission close.** Promote durable facts from Campaign or handoff state
  through D1, and discard the rest.

### D5: Retirement

At each refresh, entries that current code contradicts are corrected or
removed. At the Phase 4 decision, entries never cited across the E1 series
become candidates for removal. Budgets remain hard.

### D6: Hygiene, independent of the thesis

- the `validate` CLI fix (B13);
- the currentness repairs (section 1);
- byte-verifying the installed Skill before any attribution-sensitive trial.

## 9. Non-goals

The design adds no ontology runtime, graph store, search index, new provenance
tag, artifact field, validator, Skill, or CLI command. It adds no plan
document beyond amendments to the canonical plan. It makes no change to merge,
release, or deploy authority. Mission state does not become product truth. No
"Living Repository Intelligence" brand is introduced; the glossary vocabulary
stays.

## 10. Guidance budget

D1, D3, and D4 enter `using-sensemaking` section 0 **by replacement**, so the
net word count is zero or negative. The plan's Phase 4 target (a core of at
most 1,500 words) stays binding.

## 11. Evaluation

There are four tests, kept separate (B5, B10).

| Test | Question | Design | Gate |
| --- | --- | --- | --- |
| **E1 Accumulation** (warm) | Do owner questions and rework fall as decisions accumulate? | Successive **real, authorized** tasks on `React_incremental_game_prototype`, logged in the plan's Phase 3 table plus three columns: delegated decisions made, delegated decisions later reversed, and citations-on-use. Each row also tags the binding constraint. | Target access only. **No manufactured tasks.** |
| **E2 Paired cold-start** (causal) | Does pack visibility change outcomes? | Same task and base in separate containers, with only pack visibility varied. At least 3 tasks with an applicable recorded decision, plus 1 warranted-decline task. The owner judges blind and pairwise. | A qualified runner (WP-6). Otherwise record **NOT TESTED**. |
| **E3 Continuation** | Can a fresh context resume? | Trial 002R as specified in #515. | #515 admission. |
| **E4 Relational** (conditional) | Does a relational map beat decisions-only? | Decisions-only arm against decisions plus a relational-map arm, on a domain where E1 recorded misinterpretation. | At least 2 E1 rows tagged with relationship misinterpretation as the binding constraint. |

**Metrics.**

- owner questions per task;
- ratchet misses;
- **delegated-decision reversal rate** (the autonomy-quality signal);
- rework commits and CI failures after "done";
- invariant violations;
- citations-on-use;
- pack words;
- core guidance words.

**Unblocking the critical path (B3).**

- **Runner.** Check whether separate cloud coding-agent sessions meet the
  isolation controls: a fresh container and dependency install, no
  transcript, a pinned model, and byte-verified Skill copies. This is a
  checkable fact, not an owner design question.
- **Target.** E1 needs ordinary successive tasks, not a fresh multi-step
  mission.
- **Human evidence.** Use a blind diff preference, which takes minutes, in
  place of a playtest wherever the claim is about code or product choice
  rather than player experience.

## 12. Decision rules (pre-registered)

| Condition | Action |
| --- | --- |
| E1 after at least 5 tasks: owner questions per task not below the first two tasks **and** zero citations-on-use | NO DEMONSTRATED BENEFIT (local). Stop adding grounding content and keep the pack minimal. |
| Delegated-decision reversal rate above 1/3 | Delegation is outrunning recorded intent. Ask, record intent, and do not widen delegated scope. |
| Reversal rate at or below 1/3 **and** owner questions per task falling | Supports D3 locally. Keep it and carry it to a second repository. |
| E2: pack arm preferred or tied with fewer owner questions on at least 2 of 3 tasks, and no more invariant violations | Retain provisionally (one repository, small N). |
| E2 misses the bar | Simplify, per plan Phase 3 rules. |
| Any irreversible action justified only by `[hypothesis]` or `[delegated]` | **Material failure.** Pause D3. |

## 13. Work packages

Each work package is one small PR.

| WP | Repo | Change | Depends on |
| --- | --- | --- | --- |
| WP-1 | this | `validate` CLI: honest exit codes and JSON, plus malformed-artifact tests | none |
| WP-2 | this | Currentness: ADR 0030 status amendment, the stale `STATUS.md` bullet, the build-001 contradiction | none |
| WP-3 | this | Amend `repository-grounding-plan.md` and `using-sensemaking` section 0 with D1-D4 and the E1-E4 split, word-neutral | owner ratification of D3 (ADR 0030 amendment) |
| WP-4 | target | Copy Essence decision closure: four traps recorded, delegated decisions, scope question queued (the first E1 row) | WP-3, target access |
| WP-5 | target | E1 series over subsequent real tasks | WP-4 |
| WP-6 | this | Runner qualification: one throwaway isolation check and a result note | owner approval of spend |
| WP-7 | target | E2 paired comparison | WP-6, admitted tasks |
| WP-8 | this | Plan Phase 4 decision (retain, revise, or simplify) and the core-guidance shrink | E1, optionally E2 |
| WP-9 | target | E4, only if triggered | E1 trigger |

## 14. Risks

| Risk | Mitigation |
| --- | --- |
| Delegated decisions drift into invented intent | Scoped to the delegated objective; reversible only; asynchronous owner review; reversal rate tracked. |
| Citation-on-use becomes ceremony | One line, only when a decision actually changed. A missing citation is data, not a violation. |
| E1 trend read as causation | Trend claims are local and observational. Causal claims need E2. |
| Admission test applied loosely | Phase 4 retirement removes uncited entries, and the budgets bind. |
| This record becomes another plan pile | It only proposes amendments. WP-3 folds the accepted ones into the canonical plan, and this file stays an analysis record. |

## 15. Owner decisions requested

These three are genuinely the owner's. Everything else here is agent-decidable.

1. **Ratify D3.** May the agent settle reversible, in-scope product questions
   as `[delegated]` decisions, with asynchronous review? This amends ADR 0030
   decision 5.
2. **Approve spend for WP-6** (runner qualification).
3. **Answer or delegate** the Copy Essence Campaign One scope question.

## 16. Answer to T1's deeper question

Sensemaking should make an agent better at *moving a product toward a
desirable future*. On current evidence, the mechanism is not accumulating
understanding as such. It is **closing decision gaps at the lowest legitimate
authority, and remembering the closures**. Understanding is admitted when it
changes a decision. Autonomy is measured by how rarely the owner has to
overturn what the agent decided.
