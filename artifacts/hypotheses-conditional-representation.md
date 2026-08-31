# Hypotheses — Conditional Representation (pre-experiment speculation)
Source brief: `c104a81` @ `phb-conditional-representation-candidate`, vg 0.67, ce 0.05
Research question: `docs/research/control-model-research-agenda.md` — Do we need detailed architecture by default or only when warranted?
Status: SPECULATION — not evidence. Each must be tested before hardening (CONTEXT.md:321).

## H1: PARTIAL fails rarely (<20%)
- Hypothesis: Shallow evidence + conditional PARTIAL is sufficient for most tasks; FULL only needed for cross-cutting decisions (repo split, migration, control-kernel extract).
- Reasoning: Probe shows 4015 tracked, ce 0.05 clean; churn hot on workflow-runtime/CONTEXT.md only. PR #242 bounded PARTIAL succeeded.
- Confidence: Medium
- Test (slice for U1): Run repo-sensemaker on 2 structurally different repos (framework vs product app like auteur) and record sufficiency judgment.
- Falsified if: Product app needs FULL to parse its own boundaries (e.g., narrative-architecture.md) on first diagnosis.

## H2: Warrant is not yet stable enough for a schema
- Hypothesis: Two independent agents will disagree 30-40% on sufficient vs PARTIAL because representation_sufficiency is producer judgment (CONTEXT.md:149).
- Reasoning: Agenda explicitly defers warrant schema until repeated useful responsibility + stable semantics + manual burden (CONTEXT.md:146-159).
- Confidence: Medium-high
- Test (U2): Two agents independently judge sufficiency on same repo/brief, compare agreement rate.
- Falsified if: Agreement >90% without extra guidance.

## H3: vg 0.67 is credibility debt, not logic bug
- Hypothesis: Fixing README↔CI mismatch (validation.yml:42) to vg 0.0 will not flip H1, but is required for external validity.
- Reasoning: Declared validate-brief/plan vs enforced gate-a pytest are disjoint; conditional logic doesn't depend on them.
- Confidence: High
- Test (U3): Align README/CI, re-probe vg 0.0, re-validate brief.
- Falsified if: Enforcing declared validators fails the brief.

## H4: Conditional pattern generalizes, implementation does not (yet)
- Hypothesis: "Add detail only when needed" generalizes; our MODEL_WARRANT + artifact-contracts implementation is domain-specific to agent-control repos.
- Reasoning: Research agenda domain-general vs domain-specific split is still open (CONTEXT.md:270-290).
- Confidence: Medium
- Test (U4): Dogfood same probes on 1 non-framework product repo.
- Falsified if: Same probes yield useful PARTIAL decision outside framework.

## H5: Sufficiency stays agent-proposes, owner-disposes
- Hypothesis: Agent may judge sufficiency, but FULL materialization requires explicit owner/authority gate (AGENTS.md:5 finding != authorization, CONTEXT.md:227 Can KNOW != Can DECIDE).
- Reasoning: Auto-FULL risks building expensive structure without authorization.
- Confidence: High
- Test (U5): Route next FULL candidate through architectural-review with owner decision gate.
- Falsified if: Owner consistently defers to agent and gate never changes outcome across 3 runs.

## Results (2026-08-30 dogfood slices)

### H1 slice — 2026-08-30
- Method: repo-sensemaker shallow probe on 2 repos: sensemaking-skills (c104a81, framework) vs auteur (3c0b614, product, 296 docs/109 historical/376 churn, artifacts/probe-report-auteur.yaml:54)
- Result: Both needed at most PARTIAL, neither needed FULL. sensemaking-skills → SUFFICIENT (fix vg), auteur → INSUFFICIENT_BOUNDED (read narrative-architecture.md + ADRs).
- Verdict: SUPPORTS H1 (PARTIAL sufficient, FULL not required). Not falsified.

### H2 slice — 2026-08-30 (2 independent pairs)
- Pair 1 (sensemaking-skills c104a81, clear vg 0.67/ce 0.05): Agent A SUFFICIENT, Agent B SUFFICIENT → AGREE
- Pair 2 (auteur 3c0b614, fuzzy 296/109 docs): Agent A INSUFFICIENT_BOUNDED, Agent B INSUFFICIENT_BOUNDED → AGREE
- Pairs: 2/2 agreed (4/4 judgments, 0 disagreements). Predict was 30-40% disagreement.
- Verdict: CONTRADICTS H2 as stated; warrant more stable than guessed on these cases. Sample n=2 pairs too small to promote — need 5+ pairs. Do not harden schema yet.

---
### H3 slice — 2026-08-30 (autonomous, no owner input) — VERIFIED 33530fd
- Action: Added Level 6 to `.github/workflows/validation.yml:639` to enforce README-declared `scripts/validate-brief.py`, `validate-plan.py`, `validate-and-report.py`, `shadow-mode-runner.py`
- Probe re-run: `vg 0.67 → 0.0` (declared 6/6 enforced, notes ''), `ci_enforcement()` verified locally + exact-head CI green on 33530fd (all tests pass per owner)
- Verdict: SUPPORTS H3 — credibility debt closed without flipping H1; H1/H2 now durable. Repair-verified.

---
Next warranted responsibility: Re-validate updated brief and push exact-head CI on c104a81; then promote H1/H2 from speculation → evidence.
