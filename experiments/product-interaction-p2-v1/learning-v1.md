# Task P2 — Learning Record (assisted-baseline vs POST comparison)

experiment_type: product_interaction
record: learning-v1
recorded_at: 2026-08-08
status: COMPLETE — interaction preserved, no implementation, no repo-sensemaker change

---

## What ran

- Repository investigated: `sensemaking-skills` at `origin/main` @
  `e2e859b60c255c5b02ea74083cfca94db28601d0` (experiment branch
  `experiments/product-interaction-p2-v1`, fresh from `origin/main`).
- Product under test: canonical in-repo `skills/repo-sensemaker/SKILL.md`
  (blob `a5cb5dd71fd75adeb879780b9dc47020cecd5ab3`), standalone agent-native
  invocation, exactly once.
- Owner question: "After P1, should the standalone repo-sensemaker validation
  failure become the next engineering task, or is there higher-value product
  work to do first?"
- Baseline: `ASSISTED_BASELINE` (reconstructed from P1 evidence + P2 prompt),
  explicitly NOT an `OWNER_PRE`. Result: `NO CLEAR PRE INCLINATION` on the
  exact fork, with documented adjacent context (owner's post-P1 plan: probe
  distribution -> fix if confirmed -> then interaction work).
- Artifacts: `charter-v1.md`, `assisted-baseline-v1.md`,
  `repo-sensemaker-investigation-v1.md`, `owner-synthesis-v1.md`,
  `owner-post-v1.md`, `validation-result-v1.json` (raw validator output).

## Observed product behavior (ordinary invocation)

- The skill produced a full 14-section Repository Sensemaking Brief with
  evidence excerpts, logic trace, weakness-type classification, and machine
  handoff.
- **The brief failed its own standalone validation again**: 7 blocking
  `EVIDENCE_QUOTE_NOT_FOUND` (Excerpts 1-7). The producer followed the
  canonical template's Section 8 instruction (placeholder quotes such as
  "see file/lines"; runtime-overwrite assumption) — the documented
  `scripts/validate-and-report.py` path rejects non-verbatim quotes
  (`scripts/validate-brief.py` L728-L762). Excerpt[0] passed only because the
  literal placeholder string "see file/lines" coincidentally exists verbatim
  inside `repo-analysis-template.md` itself — confirming the grounding is
  purely mechanical. Per protocol: no repair, no rerun; preserved as
  observed (`validation-result-v1.json`).
- The failure at the new SHA confirms the P1 failure is not a stale-artifact
  artifact: the standalone validation failure is current at `origin/main`
  after the P1-F distribution repair.

## What the repository evidence established (observed)

- The distribution repair (P1-F, PR #156, `1935796`) landed in source and
  the 0.2.2 wheel ships canonical skill trees; PyPI still serves only the
  confirmed-broken 0.2.1 (no release published; external check).
- The validator is not defective: the canonical fixture
  (`tests/fixtures/repo-sensemaker-template-canonical.md`) passes
  `validate-brief.py` with zero errors (verified this run); quote grounding
  is the designed contract (issue #80/#89).
- Quote fidelity is solved by design in the runtime path only
  (`evidence_quote_extractor.py` + `brief_skeleton.reconcile`, invoked at
  `scripts/skill_executor.py` L1973-L1980); issue #89 is closed via that
  design (option B: runtime populates quotes deterministically).
- The template's placeholder-quote instruction
  (`repo-analysis-template.md` L75-L82) is unconditioned on mode, and 0.2.2
  ships those skill files byte-identical — the contradiction would ship to
  installed users.
- The installed-path validation surface is additionally broken: the
  documented `sensemaking-skills validate` command is a stub
  (`src/sensemaking_skills/cli.py` L89-L97) and `scripts/` are not shipped in
  the wheel.
- Downstream routing fields (Section 13) are consumed by `workflow-planner`
  independently of excerpt quotes; the failure does not block the machine
  handoff.
- There are no external users of a working release (PyPI 0.2.1 broken, 0.2.2
  unpublished).

## What repo-sensemaker inferred (not directly observed)

- That the failure's real impact does not justify making it the next major
  engineering task, and that higher-value product work (the owner-facing
  synthesis step) should come first — inferred from the impact evidence plus
  the owner's documented post-P1 sequence.
- That "publishing 0.2.2" is higher-value product work — **inference the
  owner explicitly rejected**: PyPI was a previously-closed optional
  distribution experiment, and P2 produced no new evidence to reopen it.
- That the mode-aware guidance fix is small enough to bundle into product
  work rather than stand alone — inferred cost/benefit, not measured.

## What the owner judged useful

- **Reframing** (decision-sharpening): "fix the validator" -> "producer /
  runtime contract is inconsistent with standalone validation" — this
  changes what work would be authorized.
- **Impact evidence** (decision-sharpening): the failure did not prevent P1
  decision value; Section 13 routing remained usable — this helps priority,
  not just diagnosis.
- The CLI `validate` stub was treated as a finding, not automatically
  decision-sharpening.
- Overall POST: "Useful and decision-relevant overall ... That better
  justifies continuing higher-value product/interaction discovery first."
  (verbatim in `owner-post-v1.md`).

## What remains uncertain

- Whether the red gate actually degrades owner (or future user) decisions in
  practice — one observation (P1) suggests it does not block decision value;
  still unmeasured.
- Whether external users will exist soon (depends on the owner's separate
  optional PyPI decision), which would change the impact ranking.
- The owner's own next move after P2 was not re-elicited beyond the POST
  (the protocol stops at POST judgment).

## Qualitative disposition

**USEFUL_CONFIRMATION.** The owner's direction remained broadly similar
(product/interaction discovery first — consistent with the owner's own
post-P1 plan), but an important alternative was challenged/reframed (the
"validator repair as next task" option was reframed into a mode/producer-
contract issue, materially changing what work would be authorized) and
confidence became substantially better justified via impact evidence. Not
`STRONG_SHARPENING`: the action did not materially change (the assisted
baseline's documented context already pointed to interaction work next). Not
`MISLEADING` overall, but the interaction's synthesis did overreach on one
item (0.2.2 publication) which the owner corrected — see product lesson 4.

Key evaluation question — "Did this interaction leave the owner in a
materially better position to decide what engineering work should happen
next?" — **Yes**: the owner's POST states the decision is better justified
and the framing of the candidate task is corrected, with a specific
overreach explicitly carved out.

## What this single interaction teaches about the desired product

1. **The reframing is the product's sharpest value**: converting "broken
   validator" into "mode/producer-contract inconsistency" changed what work
   the owner would authorize without any code change. P2 provides a second
   supporting case (after P1) that decision value can come from the
   investigation and synthesis even when the machine artifact fails
   standalone validation.
2. **The standalone validation failure is current, reproducible, and
   instruction-caused**: it survived the distribution repair; the canonical
   template itself causes it in standalone mode. This is a genuine product
   defect on the documented path — but a guidance/contract defect, not a
   validator defect, so "validator repair" is the wrong task label.
3. **The red gate did not block decision value in either P1 or P2** — the
   strongest current evidence that the validation failure is lower-priority
   than interaction work; it remains the main empirical support for the
   sequencing recommendation.
4. **The owner-facing synthesis can overreach beyond its evidence**: the
   synthesis re-promoted a previously-closed optional decision (PyPI
   publication) without new evidence, and the owner had to correct it. A
   product that sharpens decisions must preserve prior owner decisions and
   distinguish "unfinished technical state" from "product priority" —
   synthesis overreach is a failure mode to watch (and the cheapest guard is
   citing the evidence behind each recommended item).
5. **The assisted-baseline design worked as intended**: `NO CLEAR PRE
   INCLINATION` forced the interaction to earn its usefulness on the fork,
   and the owner's POST confirms it did — while the claim stays honestly
   bounded (usefulness/justification, not a measured PRE->POST delta).

## Broader product hypothesis

Hypothesis: "When an owner is uncertain about consequential engineering
work, repo-sensemaker can investigate the repository and leave the owner in
a materially better position to decide what should happen next."

P2 is one replication attempt, not general validation. On this second real
case the interaction was judged useful and decision-relevant, it reframed
the candidate task (changing what work would be authorized), and it better
justified the owner's direction — while also demonstrating a synthesis
overreach failure mode the owner had to correct. Two cases are not a
dataset; the hypothesis remains plausible and worth further real
interactions, with attention to (a) synthesis evidence-discipline and (b)
whether the standalone validation red gate should be fixed to de-noise
future probes (owner's decision).

## Non-authorizations (explicit)

- No implementation of any recommended follow-up (no guidance fix, no CLI
  change, no validator change, no PyPI action).
- No repo-sensemaker modification.
- No salvage/merge of the hardening candidate.
- No change to the evaluation system.
- No P3, no campaign machinery, no scorer, no new schema.
- The recommended follow-up (reproduction already performed as PHASE 5;
  interaction/synthesis work; optional mode-aware guidance fix) is recorded
  as the owner's next decision — not executed.

## Owner acceptance (additive record; does not rewrite any observed evidence)

recorded_at: 2026-08-08 (owner response to the P2 final report)

- The owner **accepted Task P2 as a valid product-discovery result** and
  confirmed the qualitative disposition `USEFUL_CONFIRMATION`.
- Accepted claim (owner's framing, proportional to the weakened protocol):
  "Given a real unresolved engineering question, repo-sensemaker produced a
  reframing that the owner judged useful and decision-relevant, and that
  reframing better justified the owner's existing direction." Not claimed:
  an independently captured PRE->POST decision change.
- Wording refinement applied per owner instruction: the stronger phrase
  "second replication" (this file, lesson 1) is replaced with "second
  supporting case", because P2 differs materially from P1 (assisted
  baseline vs independent PRE; same repository ecosystem) and therefore
  strengthens the hypothesis without being a strong independent
  replication in the experimental sense.
- Owner's refined product-learning framing: repo-sensemaker may be good at
  discovering and reframing local repository evidence while still needing
  stronger discipline around (a) preserving prior owner decisions and (b)
  distinguishing "unfinished technical state" from "product priority"
  (see lesson 4).
- Owner's stated next step (recorded, NOT authorized or started here):
  close P2 cleanly; do not fix the validator yet; do not turn the
  "mode-aware guidance + CLI honesty" idea into a P2-F; the highest-value
  next product experiment is P3 on ANOTHER repository, challenging the
  alternative explanation that repo-sensemaker is unusually effective on
  its own repository, keeping the lighter P2 interaction model (real owner
  question -> minimal existing context -> one interaction -> compact
  recommendation -> owner's free response). No scorer, no implementation,
  no validator repair.

## Stop condition reached

Learning record complete (with owner-directed wording refinement applied).
STOP per charter — nothing further is implemented or changed in this task.
