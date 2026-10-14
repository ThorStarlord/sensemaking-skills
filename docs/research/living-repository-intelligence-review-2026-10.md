# Living Repository Intelligence: Adversarial Review and Architecture Synthesis (2026-10)

**Status:** analysis record and proposed amendments; **not ratified**.
Part II was revised on 2026-10-14 under the owner's long-term stewardship
mandate.
**Authority:** research only. Does not supersede ADR 0030 or
[`../repository-grounding-plan.md`](../repository-grounding-plan.md). Part II
proposes amendments to them; it is not a parallel roadmap.
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
0030. It does not plan for the three external blockers that have held up the
one comparison it depends on: pack versus no pack on real construction work.
And T2's reversal of T1 is not backed by any new evidence.

Many tests have already been run, including two write-enabled trials. Section
4 lists them and the question each one answered. The plan's weakness is not a
lack of tests. Its central claim rests on the one question those tests have
not yet answered conclusively.

**Horizon correction.** All of that evidence is short-horizon: single sessions
or a few days. It cannot judge what a multi-month steward needs. Under the
owner's mandate of **long-term autonomous repository stewardship**, Part II
proposes the **Stewardship Kernel**:

- three small typed files: boundaries and invariants, a capability map tied to
  goals, and short-lived arc state;
- one CI check for shape, references, coverage and budgets;
- one loop rule: no silent drift, so every boundary change is an explicit,
  delegated amendment.

Everything that can be checked is pushed into tests and lint rules. Prose is
kept only for *why* and *what for*. The kernel is a hypothesis, with a
long-horizon test that can run now.

---

# Part I: Adversarial review

## 1. Currentness defects in the reviewed texts

Each claim was checked against the repository or GitHub on 2026-10-14.

| Claim in T1/T2/T3 | Actual state | Consequence |
| --- | --- | --- |
| PR #536 is open and its comparison should be reused (T1 section 7, T3 Phase 0.7 and Phase 5) | **Closed, not merged**, 2026-10-14. The owner closed it as superseded by PR #540 and the canonical grounding plan. The three-arm study **was never executed**. | T3 Phase 5 builds on a closed plan. |
| The grounding plan's status predates the merged pack (T3 Phase 0.1) | PR #540 already reconciled `repository-grounding-plan.md`. Three stale statements remain: the ADR 0030 amendment still says the pack is "not merged" and "owner review has not happened"; a `STATUS.md` bullet says "No Skill, contract, or Level-4 strategy text has changed yet"; and `grounding-pack-build-001.md` says both "COMPLETE by owner directive" and "can't be called complete" in one paragraph. | Small currentness repairs. They are not a phase. |
| Phase 0.2-0.4, Phase 2 (retrieval) and Phase 3 (learning loop) are future work | PR #540 already ships them as guidance. `using-sensemaking` section 0 covers selective retrieval, source verification, "no exhaustive ontology", and same-change updates after construction. `strategic-sensemaking-loop` updates affected grounding facts after consequential work. `product-strategy.md` now names "continuous, autonomous domain grounding". | **The guidance for T3 Phases 0, 2, and 3 is already merged.** What is missing is a conclusive pack-versus-no-pack result on construction work, not more guidance. |
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
  delegated-decision ratchet (Part II, section 8.7);
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

**Repair.** Admit knowledge entry by entry, through a decision-changing test,
and keep a budget on every store. Part II's kernel (section 8) does this for
structure: typed files with count budgets that a check enforces. Structure can
grow where it is checkable, but the store is never unbounded. Repeated budget
pressure that would drop owner-essential entries is the evidence that would
justify changing the format.

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

**Repair.** Make these three blockers the critical path. Part II, section 11,
shows that the main long-horizon test (a series of sequential fresh sessions)
avoids the runner blocker entirely.

### B4 (High): T2 reverses T1 without new evidence

T2 says "my earlier emphasis on the danger of documentation theater
underweighted ...". No observation was added between T1 and T2. The concession
follows argument, not data. T3 then builds a seven-phase program on the
conceded position.

The repository's claim-ceiling discipline exists to stop exactly this. T1's
skepticism was calibrated to the stress test, the replays, and the usability
test, and that evidence has not changed.

**Repair.** A stance changes only when an observation changes. Each position
should state the observation that would move it. Part II, section 5, applies
this rule to its own change of position.

T2's real contributions are framing, not evidence: a working definition of
learning, and "retrieve, don't inject".

### B5 (Medium-High): cold-start grounding and cumulative learning are conflated

T1's "demanding test" and T3 Phase 4 require an **unfamiliar** repository.
The thesis, however, is **accumulation**: later decisions improve because
earlier work taught something. One test cannot measure both.

Accumulation needs **successive ordinary tasks on the same repository**. That
also avoids the admission bottleneck in B3: a series of real tasks does not
need a "fresh, unused, multi-responsibility mission".

**Repair.** Run separate tests. Part II, section 11, makes accumulation the
main test: a session series on one repository.

### B6 (Medium): the key metrics have no collection method

T3 lists "decisions materially changed by retrieved repository knowledge" and
"consequential belief updated" as measures. It defines no way to observe
either during normal use.

T3's Phase 3 exit ("a subsequent agent ... avoid[s] a repeated mistake") is
unfalsifiable at n=1 without a counterfactual. The probes would again be
written by the agent that wrote the knowledge, a bias the stress test already
recorded.

**Repair.**

- **Citation-on-use** (Part II, section 8.6): log a decision that a grounding entry changed at
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

**Repair.** Pre-register the bar before running anything (Part II, section
11).

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

**Repair.** Promote durable lessons when each arc closes (Part II, section
8.3).

### B12 (Low): a typed relationship vocabulary invites schema growth

The relationship types (`supports`, `constrains`, `depends_on`, ...) mix
structural facts with causal product claims. A typed vocabulary attracts a
validator with no consumer, which breaks the `CLAUDE.md` rule that validator
rules must trace to real consumers. T3 also coins new names ("Living
Repository Intelligence", "Layers A-D") for existing concepts (Grounding
Pack, Campaign, handoff). That goes against the glossary rule in
`docs/agents/domain.md`.

**Repair.** Keep prose. State causal claims as `[hypothesis]` lines with a
falsifier (Part II, section 8.6). Use the glossary vocabulary.

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

## 4. What has already been tested, and the bottleneck question

### 4.1 Tests already run

In this record, a **test** is a run that was set up in advance, whose outcome
was recorded, and where some outcome would have counted against the claim
being tested. Every entry below meets that definition. They differ in **which
question** each one answers.

- A *behavior test* asks whether the agent does the right thing. It needs no
  comparison arm.
- A *comparison test* asks whether X does better than the same agent without
  X. It needs a control arm on the same task and base.

| Test | Kind | Question it answered | Result |
| --- | --- | --- | --- |
| **Trial 001** (`React_incremental_game_prototype`, 2026-09-25, target PR #154) | Write-enabled behavior test on a real repository; one arm | Can an agent using Sensemaking resume from stale state, build one bounded responsibility end to end, verify it, and stop at the authority boundary? | **Supported** on all 12 observed properties. Hosted Build Validation passed on the exact head. Limits: one repository, a stale installed Skill, no control arm. |
| **Trial 002 mission, run inline** (Auteur, 2026-09-27, Auteur PRs #291-#293) | Write-enabled behavior test, run in the same session, so its evidence ceiling is lower | Can it build a multi-package construction on a second repository without prompts? | Three green PRs with no prompts in between. An **independent review returned No-go** and found real defects: unresolvable IDs silently dropped, an invariant claimed without a test, and focused CI that never ran the existing suites. The defects were fixed after owner decisions and the PRs merged. |
| **Strategic trials 002-004, controls, and remeasure** (Pydantic, Jellyfin, AION; 2026-09-29/30) | Read-only comparison test, Skill versus no-Skill control; 3 episodes per arm per task in the remeasure | Does the Skill change which responsibility the agent picks? | **0 of 3** tasks clearly favored the Skill, against a pre-registered bar of 2 of 3. The owner ratified "simplify hard". |
| **Grounding stress test** (2026-10-12) | Read-only comparison test, pack versus no pack; 4 trap probes | Does the pack prevent specific mistakes? | Both arms avoided all four traps. The pack's marginal value was not shown. |
| **Historical replays** (2026-10-12) | Write-enabled comparison test, pack versus no pack; 2 merged tasks | Does the pack change outcomes on real past tasks? | Both arms were correct. **Inconclusive**, because the tasks were fully specified, information leaked from later commits, and the arms shared a cache. |
| **Fresh-session usability test** (2026-10-12) | Read-only behavior test; one arm | Can a fresh agent onboard using the pack? | It got the mechanics from code. Three decisions were not recorded anywhere. |
| **Episode 011** (Auteur Studio, 2026-10-13, Auteur PR #404) | Write-enabled normal-use episode | Real construction under delegation | A real browser flow exposed import-safety and authoring-UX problems. The results are agent-reported, and the PR is open. |
| **StoryLedger rehearsal** (#515, 2026-10-14) | Synthetic practice | Calibrate the Trial 002 evaluator | 9/9 acceptance checks passed on the completed candidate. This was practice, not a trial. |

What these tests support: **bounded autonomous construction behavior**
(Trials 001 and the inline 002 mission, Episode 011), and good stopping at
authority boundaries.

What they have not settled:

1. **Pack versus no pack on construction work.** The replays tried this and
   were inconclusive.
2. **Skill versus no Skill on construction work.** Every comparison test so
   far was read-only.
3. **Official Trial 002/002R with a fresh-context resume** (#515).

The Living Repository Intelligence plan's central claim depends on item 1.

### 4.2 The bottleneck question

T1 rightly says the "repository knowledge is the principal bottleneck"
premise is not established. Here is the evidence tagged by *binding
constraint*, meaning what actually limited progress.

| Observation | Binding constraint | Was missing derivable or relational repository knowledge binding? |
| --- | --- | --- |
| Trial 001 | Merge authority (withheld by design); human play evidence deferred | No. The agent rebuilt current state from stale local state on its own. |
| Trial 002 mission, inline | Verification scope (focused CI skipped the existing suites); defects caught by independent review; owner-content inputs (target, seals) | No |
| Episode 011 | Merge held by the owner; human author feedback | No |
| Synthetic stress test, 4 probes x 2 arms | None. Existing target docs already guarded every trap. | No |
| Historical replays, 2 tasks x 2 arms | None. The tasks were fully specified. | No |
| Fresh-session usability test (Copy Essence) | Three **unrecorded decisions**, plus doc/code contradictions | No for mechanics; **yes for decisions** |
| Auteur assessment | External product evidence | No |
| Trial program and remeasure (3 + 18 episodes) | Judgment and escalation calibration | No |
| Official Trial 002/002R (#515) | Target admission and an independent runner | No |
| Dark Factory #83 (#218, 2026-10-14) | Provider transport and observability | No |

**Claim ceiling.** None of these was designed to detect a knowledge
bottleneck. Several are synthetic, and the target repositories are unusually
well documented. Even so, across ten observations, including three
write-enabled ones, there are **zero** where missing relational structure was
binding. There is **one** where missing *decisions* were. The rest were limited
by verification, external evidence, infrastructure, or authority.

**Horizon ceiling.** Every observation above was short-horizon: one session,
or at most a few days. Several were substantial construction, but none ran
across many sessions. This table therefore says nothing about what
multi-month stewardship needs. Architectural drift and intent drift build up
across sessions, and no test here could have exposed them. Part II, section 5,
takes this up.

---

# Part II: Architecture synthesis under a long-term stewardship mandate (PRD/spec)

*Revised 2026-10-14. This replaces the earlier decision-first synthesis. Its
parts that still hold (delegated decisions, the admission test, causal
hypotheses with falsifiers) are folded in below (section 8.6).*

## 5. Mandate, and what it changes

**Owner mandate (stated in session, 2026-10-14):** *long-term autonomous
repository stewardship*. An agent evolves a complex repository over dozens of
sessions across months. It carries multi-stage feature arcs, explores
divergent options, and prevents architectural drift, without continuous human
micro-steering. Recording this in `product-strategy.md` would be a Level-4
revision; it is proposed here, not made.

**What the mandate changes in this review.**

- **The section 4 evidence is short-horizon.** All ten observations were
  single sessions or a few days. Several were substantial construction:
  Trial 001 changed 13 files across domain, engine, UI and tests. None ran
  across many sessions, so none can show what a multi-month steward needs.
  "Zero cases of missing relational structure" is a short-horizon result. It
  is not an argument against long-horizon mechanisms.
- **Two failure modes become central** that short tasks cannot expose:
  - *Architectural drift.* Each session makes a locally reasonable change,
    and together they erode the boundaries. This is the "erosion and drift"
    of Perry and Wolf (1992) and the "Big Ball of Mud" of Foote and Yoder
    (1997).
  - *Intent drift.* Features accumulate that no longer serve a stated goal.
- **The owner cannot be the memory.** Delegated decisions (section 8.7) must
  cover architectural decisions too.

**What it does not change.**

- **Prose documentation is not the established remedy for drift; it erodes
  too.** The established remedies are *executable* architecture rules
  (fitness functions and dependency rules; Ford, Parsons and Kua, 2017) plus
  recorded *rationale* (decision records; Nygard, 2011).
- This repository shows the same pattern at small scale. The first Grounding
  Pack had 3 wrong citations among about a dozen checked, within a day of
  being written. ADR 0030's status amendment went stale within two days.
  Prose about code drifts faster than code.
- **Nothing here has yet been shown to improve outcomes.** The design below is
  a hypothesis, with a cheap long-horizon test (section 11).

**Why this position changed.** Part I criticized T2 for reversing without new
evidence, so the same rule applies here. Two things moved:

1. **A validity argument.** Horizon is a dimension the evidence never varied,
   and the first synthesis under-weighted that.
2. **Re-weighting existing evidence.** The doc-rot observations above argue
   for knowledge that is *mechanically checked*.

No new outcome evidence was added. The result is therefore a design to test,
not a finding.

## 6. What a steward must not lose between sessions

| Failure across sessions | What prevents it | Where it lives |
| --- | --- | --- |
| **Architectural drift**: boundaries erode a little each session | Boundary rules enforced in CI; every change to a boundary is explicit | `architecture.yaml` plus native lint rules |
| **Intent drift**: features stop serving goals | Every capability links to a stated goal | `capabilities.yaml` -> goal IDs in `intent.md` |
| **Lost arcs**: a multi-session feature stalls or restarts | Durable stage state the next session resumes from | `arcs/<id>.yaml` |
| **Re-exploration**: rejected designs get retried | Rejected options recorded with the reason | `decisions/` |
| **Kernel rot**: the knowledge itself decays | Reference, coverage and budget checks that fail CI | the check |
| **Owner micro-steering** | The agent amends the kernel itself as `[delegated]`; the owner reviews diffs in batches | provenance tags |

## 7. Design principle

**Enforce what can be checked. Index what must be read. Delete what is
finished.**

1. **Executable first.** If an invariant can be a test, a type or a lint rule,
   it becomes one, and the kernel only points to it. Prose invariants are
   capped.
2. **Typed index, prose rationale.** Things the agent navigates and a checker
   verifies go in small typed YAML files: components, invariants,
   capabilities and arcs. Prose is kept only for *why* (decision records)
   and *what for* (`intent.md`).
3. **Lifecycle with deletion.** Arc state is deleted when the arc closes,
   after its durable lessons are promoted. Budgets are counts of entries, so
   files cannot grow by accumulating prose.

## 8. The Stewardship Kernel

The kernel extends the existing Grounding Pack at `.sensemaking/`. It adds
three typed files and one check. `invariants.md` shrinks or disappears as its
content moves into tests, lint rules, or typed `manual` entries.

| File | Kind | Status |
| --- | --- | --- |
| `intent.md` | prose, 800 words | exists; goals get stable IDs (`G1`, `G2`, ...) |
| `architecture.yaml` | typed | new |
| `capabilities.yaml` | typed | new |
| `arcs/<id>.yaml` | typed; deleted when the arc closes | new |
| `decisions/NNNN-*.md` | prose, 250 words each | exists; also records options explored and rejected |
| `context.md` | prose | optional; only domain terms that are easy to confuse |

### 8.1 `architecture.yaml`: boundaries and invariants

The examples in this section are illustrative. Their names are not taken from
any real repository.

```yaml
version: 1
components:            # 5-15 boundaries, not a file map
  - id: core
    paths: ["src/game/core/**"]
    owns: "Deterministic simulation state and rules"
    may_depend_on: []
  - id: features
    paths: ["src/features/**"]
    owns: "Player-facing feature slices"
    may_depend_on: [core]
unowned_ok: ["scripts/**"]
invariants:
  - id: INV-1
    rule: "Simulation code never imports UI or browser APIs"
    enforced_by: {lint: ".dependency-cruiser.cjs#core-is-headless"}
    why: decisions/0003-deterministic-core.md
    tag: "[delegated: 2026-10-15]"
  - id: INV-2
    rule: "Balance numbers come from playtest evidence, never invented"
    enforced_by: {manual: "not mechanically checkable; reviewed at arc close"}
    why: intent.md
    tag: "[owner: 2026-10-12]"
retired:               # removed invariants keep their reason until the next arc close
  - {id: INV-0, why: decisions/0006-merge-stores.md}
```

Import rules are enforced by the ecosystem's own tool (for example
dependency-cruiser, import-linter or ArchUnit). The kernel does not parse
imports itself.

### 8.2 `capabilities.yaml`: what the product can do, and its gaps

```yaml
version: 1
capabilities:          # user-visible outcomes, not functions
  - id: CAP-essence
    outcome: "Player gains Essence passively from mature Copies"
    serves: [G2]
    status: shipped    # planned | partial | shipped | deprecated
    components: [core]
    verified_by: ["src/game/core/__tests__/essenceRate.test.ts"]
    gaps:
      - "Stacking is additive in code but named multiplicative -> decisions/0007 (delegated, awaiting confirmation)"
      - "[hypothesis] Showing per-Copy contribution improves pacing; weakened by: playtest shows no change in session length"
```

This file is the **starting point for exploration**:

- A new arc starts from a gap in a capability that serves a goal.
- Divergent exploration happens on throwaway branches.
- The chosen option ships. The rejected options go into a decision record,
  so later sessions do not try them again.

### 8.3 `arcs/<id>.yaml`: multi-session feature arcs

```yaml
id: ARC-forge-v2
goal: "Standing orders handle maintenance without player micromanagement"
serves: [G1]
capabilities: [CAP-forge-assistance]
stages:                # at most 8
  - {id: S1, outcome: "Domain model and rules", status: done, evidence: "PR #154"}
  - {id: S2, outcome: "Player-facing configuration", status: next}
  - {id: S3, outcome: "Balance hooks behind the evidence gate", status: planned}
open_decisions: ["decisions/0011 (delegated, awaiting confirmation)"]
exit: ["S1-S3 done", "CAP-forge-assistance is shipped", "check passes"]
```

At most three arcs may be active at once. When an arc closes:

1. Its durable lessons are promoted into invariants, capabilities or decision
   records.
2. Everything else is discarded, and the file is deleted. Git history keeps
   it.

**Dark Factory boundary.** When Dark Factory runs a mission, its Campaign
state is canonical and no arc file is created. The arc file is the lean,
in-repository form for missions started through the Sensemaking front door
(`docs/dark-factory-autonomy-boundary.md`). It is state stored in the target
repository, not a runtime controller.

### 8.4 The check

The check is one small script, shipped as a template and run in the target
repository's CI. It exits non-zero on any failure and supports `--json`,
unlike the `validate` CLI defect in B13.

It verifies five things:

1. **Shape:** required fields, types and enums in the three YAML files.
2. **References:**
   - path globs match files;
   - `enforced_by` tests and lint configs exist;
   - `why` links resolve;
   - capability `components` and `serves` goal IDs exist;
   - arc capabilities exist.
3. **Coverage:** every source file under the configured roots maps to exactly
   one component, or to `unowned_ok`. New code that creates an unmapped area
   fails the check, which makes this the cheapest drift signal available.
4. **Budgets:**
   - at most 15 components;
   - at most 25 invariants, of which at most 5 are `manual`;
   - at most 40 capabilities;
   - at most 3 active arcs;
   - at most 8 stages per arc.
5. **Completion:** every `shipped` capability has at least one verifier.

It does not judge meaning, score anything, or parse imports.

### 8.5 The stewardship loop

Every session follows this loop, whether a person or Dark Factory started it.

1. **Orient.** Run the check. Read the goals and non-goals in `intent.md`,
   the three YAML files, and the active arc. Together these should stay under
   about 3,000 words.
2. **Select.** Take the active arc's next stage. If there is no active arc,
   open one from a capability gap that serves a goal.
3. **Build.** Work inside the component boundaries.
   - If the change needs a different boundary, amend `architecture.yaml` in
     the same PR, with a decision record.
   - Removing an invariant moves it to `retired:`, with a reason.
   - **There is no silent drift:** every architecture change either conforms
     or is explicitly amended.
4. **Close.** Update the stage status with evidence. When an arc closes,
   promote its lessons, delete the arc file, and review the `manual`
   invariants.

### 8.6 What carries over from the earlier synthesis

- **Admission test for prose.** A decision record or intent line must name
  the decision it changes, why an agent could not derive it from code, its
  source, and what would make it stale.
- **Causal hypotheses with a falsifier.** These now live in capability
  `gaps`.
- **Citation-on-use** (optional). When a kernel entry changes a decision, the
  PR description says so in one line.
- **Delegated decisions,** now extended to architecture (section 8.7).

### 8.7 Authority

- **The agent may amend** components, invariants, capabilities and arcs as
  `[delegated: date]` entries. Every boundary or invariant change needs a
  decision record.
- **The owner reviews** kernel diffs in batches, and a typed diff is short to
  read. Confirming an entry changes its tag to `[owner: date]`.
- **Protected** (owner only): changing goals or non-goals in `intent.md`;
  deprecating a shipped capability; merge, release and deploy.

## 9. What the kernel deliberately excludes

- file maps, class taxonomies, and any ontology of relationship types;
- a graph store or search index;
- an import parser of its own;
- new provenance tags;
- any Sensemaking runtime or scheduler;
- an arc file when Dark Factory owns the mission;
- growth beyond the count budgets.

When a budget binds, merge or retire entries. Repeated budget pressure is
evidence that the format itself is wrong.

## 10. Why typed, and why only this much

`CLAUDE.md` requires every validator rule to trace to a real consumer. Each
typed field here has two:

- the check, run in CI;
- the next session's agent, which uses it to find its way.

Fields that neither consumer reads are left out. Typing is what lets the
check enforce coverage and references. The check, in turn, keeps the kernel
from rotting the way prose did in this repository.

## 11. Testing over a long horizon

A long-horizon claim needs a long-horizon test, and the evidence in section 4
cannot provide one.

| Test | Design | Measures |
| --- | --- | --- |
| **Session series** (the main test) | One real multi-stage arc in `React_incremental_game_prototype`, run over at least 6 **fresh sessions**. Each session starts from repository state only, with no transcript. | correct next stage chosen on resume; silent drift (boundary changes without an amendment, found by review); retries of rejected options; owner interventions per session; delegated-decision reversal rate; kernel size over time |
| **Drift probes** (cheap and synthetic, and labeled as such) | 2-3 tasks whose quickest implementation breaks a recorded boundary, each run in fresh sessions with and without the kernel | whether the boundary is respected, explicitly amended, or silently broken |

The session series needs only **sequential** fresh sessions, which any
harness can provide. It does **not** need the isolated parallel runner that
blocks the paired comparison (B3). It can therefore run now, given access to
the target repository and an arc the owner chooses.

**Decision rules**, pre-registered and applied after session 6:

| Result | Action |
| --- | --- |
| Silent drift is 0; correct resume in at least 5 of 6 sessions; owner interventions are not rising | Keep the kernel and extend it to a second repository. |
| The check is bypassed, or the kernel is stale despite the check | The mechanism is wrong. Revise it before extending. |
| Budgets bind repeatedly, and owner-essential entries would be lost | The format is wrong. Revise the budgets or the granularity. |
| Delegated-decision reversal rate is above 1/3 | Delegation is running ahead of recorded intent. Record more intent before widening scope. |

## 12. Build sequence

Three steps, each of one or two PRs.

1. **This repository.**
   - Add the three YAML templates and the check script to
     `templates/grounding-pack/`, with tests for exit codes, JSON output and
     malformed files.
   - Add the stewardship loop to `using-sensemaking` section 0 **by
     replacement**, so the word count does not grow.
   - Fix the `validate` CLI (B13) in a separate PR.
2. **Target repository: bootstrap.**
   - Build the kernel from existing authority: `AGENTS.md`, `CLAUDE.md`,
     `specification/`, and the current pack.
   - Add one to three native dependency rules for the boundaries that matter
     most.
   - Wire the check into CI.
3. **Target repository: run the series.** Run the session series on the arc
   the owner chooses, record one table row per session, and decide after
   session 6.

## 13. Risks

| Risk | Mitigation |
| --- | --- |
| The kernel becomes the new documentation pile | Count budgets enforced by the check; arc files deleted on close; prose limited to intent and decisions |
| Components are drawn too fine and become a file map | At most 15 components, each owning a stated responsibility |
| Agents amend boundaries too freely | Every amendment needs a decision record; the owner reviews in batches; the reversal rate is tracked |
| Typed files give false confidence | The check verifies references and coverage, not meaning; meaning is reviewed when each arc closes |
| Duplicate state with Dark Factory | No arc file when Dark Factory owns the mission |

## 14. Owner decisions requested

1. **Ratify the kernel** as an amendment to ADR 0030: three typed files, the
   check, and count budgets.
2. **Choose the real arc** in `React_incremental_game_prototype` for the
   session series.
3. **Ratify delegated authority** over kernel amendments, including
   architecture amendments, with batched review.
4. **Record the stewardship mandate** in `product-strategy.md` as a Level-4
   revision, if you want it there.

## 15. Answer to the owner's question

> What is the leanest, most executable mechanism that lets an autonomous
> agent maintain long-term architectural coherence and explore product
> improvements across sessions, without documentation bloat?

Three small typed files and one check, with everything that can be checked
pushed down into tests and lint rules:

- **Boundaries and invariants** (`architecture.yaml`), enforced by native
  tools.
- **A capability map** tied to goals (`capabilities.yaml`). This is where
  exploration starts.
- **Short-lived arc state** (`arcs/`), deleted when each arc closes.
- **A check** for shape, references, coverage and budgets, run in CI.
- **One loop rule:** no silent drift. Every boundary change is an explicit,
  delegated amendment.

Prose is limited to *why* (decision records) and *what for* (intent). The
agent maintains all of it. The owner reviews typed diffs instead of answering
questions.
