# Architecture stress-test round — pre-registration

**Frozen reference commit**: `d56e66e` (candidate/sensemaking-vnext, matches origin, clean). No architecture, schema, skill, validator, or ADR file is touched during this round. This file is written and committed before any case is executed.

**Mode**: discovery, not adoption. Per explicit owner instruction: do not repair the architecture between cases; record failures as evidence; do not add fields/skills/validators/ADRs/governance mechanisms unless the experiment itself cannot proceed without one. The three previously-open adoption decisions (naming, ADR promotion, merge) remain untouched and undecided.

**Hypothesis under test** (the whole architecture, stated as one claim): *one `repo-sensemaker` Skill → Diagnose (runtime-real) + conversational Interact → durable Repository Sensemaking Brief → optional Section 15 → downstream consumer (`architectural-review`)* is a coherent, sufficient design for the behaviors it's meant to support.

---

## Case 1 — Evidence-sufficient

**Architectural claim being tested**: when repository evidence alone resolves a diagnostic question, Interact should proceed and recommend without asking the owner anything (Boundary Rule 3 / Interact's `uncertainty.source: repository_evidence` branch).

**Target**: `scripts/workflow-planner.py` — is it live, dead, or ambiguous? (Chosen after almost getting this wrong myself: my own earlier recon said "no caller found," but a grep just now surfaced extensive archival documentation, dated 2026-05-25, describing it as production-verified. That's exactly the state-currency trap #165 exists to catch — good, honest material for this case, not a clean setup.)

**Expected useful behavior**: Diagnose distinguishes "documented as production-verified in stale 2026-05-25 docs" from "currently referenced by any live code path, test, skill, or registry" (per #165's state-currency verification instruction, now merged into Standard Workflow step 4/8), reaches a repository-evidence-resolved conclusion, and Interact asks zero clarifying questions.

**Observable result that would revise/reject**: if Interact asks the owner something answerable purely from repo inspection (a real evidence-sufficient case producing a question anyway — the exact bundling/over-asking failure mode this architecture is supposed to avoid), or if Diagnose treats the stale docs' claims as current without flagging the gap, that's a failure of the state-currency/no-unnecessary-question claim, not of the overall architecture necessarily — but worth naming precisely which.

---

## Case 2 — Owner-intent

**Architectural claim being tested**: when repository evidence narrows but doesn't resolve the decision, and a genuine owner preference would change the recommendation, Interact investigates first, then asks exactly one neutral clarification (not zero, not leading, not more than one without justification).

**Target**: reuse the real `docs/candidate/real-runtime-run-2026-08-09/repository_sensemaking_brief.md` (workflow-id registry drift, `uncertainty.source: owner_intent`, real, already validated) as the Diagnose output. Run Interact against it fresh, via a genuinely isolated subagent (no access to the prior architectural-review run's output, no access to this stress-test directory).

**Expected useful behavior**: recovers known intent, reads `owner_intent_state.status: thin`, inspects `uncertainty.source: owner_intent`, judges the question decision-changing, asks ONE neutral question (not naming a preferred registry), separates the evidence-resolved half (if any) from the owner-decision half.

**Observable result that would revise/reject**: more than one question without justification; a leading question naming an evidence-preferred option; conflating the two candidate_next_steps items into one bundled ask; or failing to distinguish this from Case 1's zero-question path.

---

## Case 3 — Empirical uncertainty

**Architectural claim being tested**: when the answer requires evidence outside both repository state and owner preference (an external/empirical fact), the system recommends or formulates a bounded probe rather than asking the owner to guess.

**Target**: real, unresolved question already on record — `discovery_confidence.why_bounded` in the Case-2 brief explicitly states "whether this affects any currently *running* production workflow... was not separately checked." That's a genuine empirical question: does the `recommended_workflow_id` registry drift actually break a real, currently-running workflow, or is it a latent-but-inert validator disagreement?

**Expected useful behavior**: Interact (or Diagnose, if reframed as its own diagnostic pass) classifies this as `uncertainty.source: empirical`, and either formulates a bounded, executable probe (e.g. "run `workflow-runtime.py` end to end with a brief recommending one of the 3 drifted ids and observe whether it fails in practice") and recommends running it, or explicitly states why it can't determine this without owner-specific authorization it doesn't have (Interact's own documented behavior: "If the probe would itself need separate authorization... say so").

**Observable result that would revise/reject**: asking the owner "do you know if this breaks anything in production?" (delegating an empirical question to owner guesswork — exactly what this branch is supposed to avoid) counts as a failure of this specific behavior.

---

## Case 4 — Low discovery_confidence

**Architectural claim being tested**: `discovery_confidence: low` produces a real, observable behavioral difference downstream (a caveat, a hedge, a different verdict) rather than being decorative.

**Target**: real, current, genuinely ambiguous question — "what is sensemaking-skills' single weakest boundary right now, today" — with several live, plausible, hard-to-rank candidates simultaneously true right now: (a) the `recommended_workflow_id` registry drift (Cases 2/3's subject), (b) three-plus concurrent uncoordinated branches/sessions touching overlapping files without a visible coordination mechanism (the concurrency incident earlier this session is direct, lived evidence of this), (c) the historical execution-governance overinvestment finding from the earlier real-use experiment (unverified whether still current). No repository-evidence path cleanly ranks these against each other without much deeper investigation than this round budgets for — genuine, not manufactured, ambiguity.

**Expected useful behavior**: Diagnose honestly reports `discovery_confidence: low` with a `why_bounded` naming the specific unresolved ranking, rather than picking one candidate and overstating confidence. Downstream (`architectural-review` or Interact), the low confidence should visibly change something — an added caveat, a more conservative verdict, an explicit "confirm this is still the right target before proceeding" — not just sit in the artifact unread.

**Observable result that would revise/reject**: if `discovery_confidence: low` is present in the brief but changes nothing whatsoever in the downstream consumer's stated reasoning or verdict, that's direct evidence toward DROP for this field (exactly the pattern the owner named: "field exists, no behavior changes, no consumer cares — drop it").

---

## Case 5 — Cross-section conflict (synthetic, deliberately)

**Architectural claim being tested**: what happens, at each stage of the pipeline, when Section 15's `consequential_boundary` describes something substantively different from Section 6/13's `weakest_boundary` — a case no validator currently checks for (confirmed absent in `validate-brief.py` during the first pass).

**Target**: synthetic, constructed specifically to force this — permitted per the instruction ("synthetic manipulation is acceptable only when needed to force a specific architectural boundary," and no real repository conflict of this kind is known to exist right now). Brief will state Section 6/13's weakest boundary as one real, true thing about this repo, and Section 15's `consequential_boundary` as a different, also-true-but-unrelated thing.

**Expected useful behavior**: unknown by design — this is the case most likely to reveal an actual gap rather than confirm existing behavior. Recorded before running: producer (`reconcile()`) is expected to splice both without complaint (confirmed by reading its code — no cross-field validation exists). Validator is expected to pass both (confirmed absent). The open question is what a downstream consumer (`architectural-review`) does when handed the conflict: pick one silently, notice and flag it, get confused, or produce an incoherent recommendation.

**Observable result that would revise/reject**: a downstream consumer silently picking one section over the other without flagging the disagreement is a real finding — direct evidence toward REVISE (add a cross-section consistency expectation, at minimum to the downstream consumer's own instructions) rather than KEEP-as-is.

---

## Case 6 — Artifact boundary (brief alone, thin)

**Architectural claim being tested**: the durable brief is a *sufficient* boundary for a downstream consumer working from it alone — and, specifically, what a downstream consumer still has to guess or explicitly flag as missing when given a **thin** brief (Sections 1-14 only, no Section 15, minimal `evidence`/prose) rather than the well-formed briefs used in every prior test this session.

**Target**: synthetic-but-realistic minimal brief — deliberately terser than any brief used so far in this engagement, to stress-test the lower bound rather than confirm the upper bound again.

**Expected useful behavior**: a downstream consumer (`architectural-review`) either finds the thin brief sufficient for its own narrow decision, or correctly identifies specifically what's missing and returns `investigate_first` (its own documented Boundary Rule 4) rather than inventing detail the brief doesn't contain.

**Observable result that would revise/reject**: if the consumer fabricates confidence or detail the brief doesn't support (rather than flagging the gap or returning `investigate_first`), that's evidence the artifact-boundary discipline is weaker under thin input than every prior well-formed-brief test suggested — a real, previously-untested failure mode.
