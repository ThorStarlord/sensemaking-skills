# Method Adaptation v0 — Construction-First Continuation With ORD Observation

**Status:** Owner-requested continuation plan (2026-11-19); executable responsibilities are conditional on current source, genuine consumer value and ordinary repository authority. **This is not a new product thesis, an experiment mandate, a second learning runtime or automatic task queue.**

**Planning baseline:** `ThorStarlord/sensemaking-skills@e6b3dd6f6d60e3862344b4f9dbde214df243d1e2` (merged [PR #932](https://github.com/ThorStarlord/sensemaking-skills/pull/932)). Re-check `main`, changed consumers, hosted checks, authority and working environment before subsequent work.

**Owner-selected objective:** Continue building useful **Method Adaptation v0** functionality: let a host agent develop a *conditional intellectual procedure* from actual work when warranted, preserve its original evidence and authorship, reconsider it during a later consequential decision, and revise, reject or leave it unchanged as evidence changes. The host agent owns semantic judgment. Method invention remains a longer-horizon ambition, not this increment's completion gate.

**Secondary objective:** Observe **Outcome-Responsibility Drift (ORD)** in that same authentic development, without converting construction into another metareasoning research or documentation cycle. See the [dated ORD case](../../agents/build-loop.md#outcome-responsibility-drift-ord-method-adaptation-construction-case-2026-11-19).

## 1. Source-grounded starting point and evidence limits

- [PR #930](https://github.com/ThorStarlord/sensemaking-skills/pull/930) treated an existing source-informed technical repair as sufficient for a broader method-development construction objective; [PR #931](https://github.com/ThorStarlord/sensemaking-skills/pull/931) corrected the completion inference but delivered a conditional record rather than a usable lifecycle.
- [PR #932](https://github.com/ThorStarlord/sensemaking-skills/pull/932) implemented the optional `semantic method context` read path and `semantic method record` producer over existing SCL/AMS/RECALL, with an installed-CLI hosted read-side check. A genuine write-side agent episode and later method reuse were **not observed**. A passing hosted check is not evidence of autonomous learning.
- Implementation: `src/sensemaking_skills/method_adaptation.py` and `src/sensemaking_skills/semantic_cli.py`; active-agent guidance: `skills/using-sensemaking/SKILL.md` and `skills/repository-semantic-steward/references/recall.md`.
- [ADR 0037](../../adr/0037-domain-general-cognitive-development.md) supplies the product objective; [ADRs 0035](../../adr/0035-sensemaking-continuous-learning.md) and [0036](../../adr/0036-adaptive-metareasoning-system.md) locate learning/recall and present-time method judgment. Existing shared evidence, Git review and authority boundaries remain operative.
- [#872](https://github.com/ThorStarlord/sensemaking-skills/issues/872) remains the separate independent later-agent reuse/feedback qualification; [#874](https://github.com/ThorStarlord/sensemaking-skills/issues/874) remains the matched-comparison track. Neither is a blocker to useful authorized construction, nor may either be declared satisfied by a normal-use episode.

**Non-identities:** retained method proposal != agent skill acquisition; CLI retrieval != predecision encounter; a technically successful patch != changed reasoning procedure; an author's self-report != independent evidence; a local task complete != the owner outcome complete.

## 2. Next mission: build through an independently useful engineering responsibility

The next execution session should prioritize **actual engineering value**. The agent selects a genuine, authorized repository task from current code, real consumer friction or meaningful product priorities **without choosing a contrived task to demonstrate learning**. It may choose a source-grounded Method Adaptation consumer limitation, a genuinely valuable adjacent engineering responsibility, or a coherent integration increment, depending on where the strongest retained product value lies.

For a consequential selection, compare realistic paths such as using existing functionality, a focused repair, a more complete reversible integration, and justified nonconstruction. Compare beneficiary effect, capability completeness, opportunity cost, maintainability, source evidence, authority and downside. **Boundedness describes outcome and risk, not a line-count or one-PR ceiling.** Do not privilege a receipt, a knowledge claim, a low-cost patch or an issue's availability over a more valuable authorized capability. Equally, do not build a new runtime or force additional code merely to demonstrate ambition.

Where work is already clearly scoped and authorized, execute it directly. Where the environment lacks a usable repository checkout, a genuine write-side CLI episode cannot be claimed from GitHub-source inspection; use a capable authorized coding environment for that consumer or record the exact blocker. Preserve all protected user work.

### M1 — Select and complete worthwhile work

- **Entry:** Current pinned source, owner objective, actual consumer and authority are known. Check [PR #932](https://github.com/ThorStarlord/sensemaking-skills/pull/932)'s current code rather than treating its receipt as an implementation substitute.
- **Act:** Choose and deliver a valuable engineering outcome within its warranted scope. Record the selected responsibility and material alternatives in the ordinary PR decision note when warranted; no additional mandatory decision form.
- **Acceptance:** A genuine owner-benefiting task is completed, or a specific evidence/authority/environment blocker is reported. The original product objective remains explicit if one local task does not fulfill it.

### M2 — Consume prior methodological experience only when relevant

- **Trigger:** A current task involves a consequential *choice of intellectual procedure*, such as whether to explore, construct, compare, challenge, verify or stop, and earlier methodological experience could materially change it.
- **Act:** Optionally use `sensemaking-skills semantic method context --question "<actual decision>" --repo . --ref HEAD --json`; inspect original source/revision, scope, changed conditions, counterevidence and authority. The lookup is lexical and its returned applicability is `NOT_ESTABLISHED`; the agent, not the command, determines relevance.
- **Acceptance:** If evidence supports a material method disposition, the real decision and observable action are distinguishable from merely receiving candidate records. If no relevant method exists, execute normally and report no methodological learning rather than forcing a match.

### M3 — Exercise genuine write-side use and selective reconciliation

- **Trigger:** An **actually completed** responsibility provides source-grounded reason to retain or correct a conditional reasoning procedure. A revised technical belief or task-local patch alone does not meet this trigger.
- **Act:** In a real Git checkout, author an attributable episode JSON using the documented fields in [Steward RECALL](../../../skills/repository-semantic-steward/references/recall.md#method-adaptation-v0-optional-agent-facing-lifecycle), with the precise source commit, tracked evidence, actual outcome, procedure before/after where observable, conditions, contrary evidence and a limited claim. Stage or commit that genuine episode source before invoking `sensemaking-skills semantic method record --repo . --episode <tracked-episode.json> --output .sensemaking/knowledge/<new-proposal.json> --json`. Then run the existing non-test knowledge proposal check, inspect the source/diff and use ordinary Git review.
- **Disposition:** `develop` or `adapt` only for a genuinely different, explainable *reasoning procedure*; `apply` or `reject` when a reviewed predecessor is considered but no new procedure is warranted; `no_change` (or ordinary RECONCILE without a record) when no durable methodological update is warranted. Preserve old evidence and do not promote shared policy automatically.
- **Acceptance:** Source-grounded consumer execution of the producer is observed when a legitimate episode exists; the newly proposed knowledge is clearly distinguished from accepted reviewed knowledge and from proven learning. If no such episode arises, state that it remains unexercised—not that cognitive development occurred or that a method record is mandatory.

### M4 — Repair the actual consumer seam if warranted

When M1–M3 reveal a concrete limitation—such as inability to supply authenticated source context, incorrect proposal provenance, unusable output for a successor, missing feedback visibility, or costly irrelevant candidate surfacing—identify the owning consumer, compare an integrated repair against direct ordinary agent use and no change, and implement the most valuable coherent authorized fix. This may span components or multiple PRs. Verify the *working* consumer behavior to the degree current repository policy permits.

Do not add a second controller, new universal memory store, automatic method extractor, global method-ranker or policy self-editor merely because a particular implementation would be novel. If current functionality suffices, continue useful work rather than manufacturing a product defect.

### M5 — Later authentic re-entry and feedback

A later genuinely valuable task may independently surface an earlier reviewed method, check its source and applicability, adopt/adapt/reject it, and produce a new attributable result. Preserve original encounters and returned evidence where available; otherwise say `NOT_OBSERVED`. Reconcile material feedback without overwriting history.

Normal construction/ordinary use may establish functional usability; the stronger independence, comparative benefit and longitudinal transfer claims remain owned by #872 and #874. Do not preselect or manipulate tasks to make those studies look successful.

## 3. Observe Outcome-Responsibility Drift without interrupting M1–M5

**ORD definition:** selecting or closing a narrower supporting responsibility as though it fulfilled the owner-level objective, without noticing and accounting for the unmet outcome. The [Build Loop case](../../agents/build-loop.md#outcome-responsibility-drift-ord-method-adaptation-construction-case-2026-11-19) documents the #930–#932 sequence and its evidence limits.

At a **naturally consequential** selection or stop, use the existing PR note/receipt where useful—not a new checklist, telemetry layer or required `ORD` record—to preserve:

- The owner-level outcome and selected bounded responsibility, with source/time context.
- What actually changed for the beneficiary and what part of that outcome remains open.
- Any materially better credible path considered and why it was rejected or deferred (including omission cost).
- Whether constraints narrowed implementation appropriately or were apparently treated as objectives.
- The original contemporaneous evidence available versus later retrospective interpretation.

**Watch for:** claiming a technical-fact fix as method development; treating another accurate lesson or receipt as a complete product outcome; concluding `NO_FURTHER_WARRANT` for the owner's mission after a component-only review; repeatedly choosing easy documentary work without comparing a coherent capability alternative. **Do not infer ORD from patch size or NO_CODE_CHANGE alone.** A justified narrow fix or stop is a legitimate positive observation.

**Competing explanations remain open:** prompt ambiguity and changed owner authority, inherited receipts, the inaccessible local execution environment, model/task selection, or misapplied repository heuristics. Observations across unmatched prompts do not establish a root cause, rate or cure.

Only if a *new authentic consequential* ORD recurrence affects work should the agent consider focused AMS diagnosis or a targeted revision to existing responsibility-selection guidance. That future decision is separate from this construction plan; do not launch a new policy, ADR or synthetic comparison merely because ORD is named.

## 4. Verification, completion and stopping

For this repository's current construction phase, honor `CLAUDE.md` and [Build Loop](../../agents/build-loop.md): review source and exact diff, execute permitted non-test CLI/contract checks when accessible, disclose any tests not run, respect actual hosted checks and merge protections, and do not manufacture synthetic cognitive episodes. Native trace absence means `NOT_OBSERVED`, not an invented predecision read or adapted method.

**Increment completion** requires a useful bounded engineering result with actual consumer verification appropriate to its claim, or a precise blocker. **Method Adaptation lifecycle progress** requires evidence of source-linked procedural consideration and, when justified by real experience, an actual reviewable method update. **Product-wide cognitive improvement** is a separate and much stronger claim. A documentation update or stored proposal alone cannot close that objective.

After any merged increment, compare remaining Method Adaptation responsibilities with the owner's desired state. Continue through further **independently warranted** work within granted authority; stop when no valuable authorized next responsibility exists, the selected increment is complete with no immediate useful successor, or a genuine external/owner boundary is reached. Record which boundary was met. Neither an empty PR queue nor a small diff automatically proves mission completion.

**What this plan is not:** a requirement to re-open the settled Level-4 product definition; a fixed task-ordering engine; mandatory episode recording; a duplicate of the #859 specification or #872/#874 qualification plans; or an excuse to delay retained construction until evidence is perfect.

**Next handoff:** In a suitable coding environment, start from a current source-pinned valuable engineering responsibility; exercise Method Adaptation's conditional read/write paths where genuine need arises; preserve any observed ORD signal incidentally and correct goal-to-responsibility mismatch before claiming broad closure.
