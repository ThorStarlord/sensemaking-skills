# S1 — Owner synthesis (compact, decision-facing)

experiment_type: solution_interaction
record: owner-synthesis-v1
target_repository: sensemaking-skills @ 27aa2442e5395f8793023882d5ed5e94861755e4
owner_question (agent-selected, frozen): "Should the next engineering work focus
on interaction design or on standalone-contract cleanup (the four infrastructure gaps)?"
produced_from: repo-sensemaker-investigation-v1 (one canonical, read-only run)
clarification: one question asked and used — owner answered (a)

---

## 1. Recommended action

**Focus on interaction design (the S1-class work); complete the four-gap
"contract cleanup" as a ~1-day wiring reconciliation fast-follow — not as a
competing priority.** The question's premise is wrong in a useful way: the
four infrastructure gaps were implemented and committed on 2026-05-28
("infra: Stabilize..."), but mis-wired — deliverables landed in legacy root
copies that agents never load, the canonical `skills/` trees were never
updated, and the skill-hygiene validator silently skips its two substantive
checks. "Cleanup" is not an open project; it is a finished-then-broken wiring
job.

## 2. Why this matters now

The contract layer's trust is currently false: the validator built to "break
before deployment" validates two of three checks against non-existent files
and passes, and its tests certify that. The next format drift will not be
caught by the very machinery built to catch it — exactly the failure mode
00-user-intent.md commissioned the work to prevent. Meanwhile the P1
execution-surface precondition for interaction work is fixed (0.2.2), the
P-series is closed, and your own recorded direction (P2-P4) is interaction
discovery. Nothing blocks S1; the mis-wiring quietly compounds.

## 3. Consequential decision boundary identified

The question presumed two open workstreams. The evidence shows one of them
("contract cleanup") is done-but-mis-wired, so the real decision is:
**interaction design as the substantive direction vs. honestly completing an
already-decided INFRA reconciliation** — a sequencing question, not a
two-workstream choice. Weakest boundary: canonical-vs-legacy tree wiring of
the contract layer (Weakness type: Implicit Dependencies).

## 4. Strongest observed evidence

- INFRA-001 dual-mode evidence rules exist only in
  `repo-sensemaker/references/evidence-rules.md` (L5-L10); the canonical
  `skills/repo-sensemaker/references/evidence-rules.md` has zero dual-mode
  vocabulary (grep for durable|investigative under `skills/` = 0), and
  `tests/test_evidence_dual_mode.py` hard-codes the legacy paths (L11/L17/L49).
- `scripts/validate-skill-hygiene.py` loads
  `workflow-orchestrator/references/{workflow-registry,skill-registry}.yaml`
  (L90, L121-L122) — neither exists there — and returns early (L93-L94,
  L124-L129). Every other validator resolves registries canonically via
  `scripts/_validator_utils.py` (L98-L115).
- Two `artifact-contracts.yaml` files declare the same four contracts with
  divergent schemas (canonical L185-L263 vs legacy L112-L140).
- Your own records ratify interaction design: P2 owner POST (L50-L59), P3
  learning (L110-L122), P4 learning (L191-L200: "Task S1... agreed next
  direction").

## 5. Strongest credible alternative

**(b) Reconciliation first.** Defensible if you consider the false-green
validator a trust blocker that must be cleared before any product work
touches the canonical tree. The evidence doesn't support treating it as a
prerequisite: the reconciliation is small, independent of the interaction
probe, and the probe itself doesn't depend on dual-mode content.

## 6. Most important remaining uncertainty

Whether your recorded direction (S1/interaction design) is still current —
**resolved by the clarification answer: (a) interaction design first,
reconciliation as fast-follow.** Residual uncertainty is minor and
non-decision-changing (README 0.2.1 vs pyproject 0.2.2 version drift;
standalone-validation usability gap, issue #89 — itself S1-class material).

## 7. Cheapest justified next action / probe

The contract-layer reconciliation (~1 day, no code risk): port dual-mode
evidence rules + template toggle into `skills/repo-sensemaker/references/`,
add the decision-tree note to `skills/workflow-planner/references/execution-modes.md`,
repoint `validate-skill-hygiene.py` at canonical paths, replace the
pass-on-clean tests with real negative fixtures, delete the legacy root
copies. Recommended workflow: `docs-contract-reconciliation` (plan_only).
Then S1-class interaction design proceeds as the focus.

## 8. Confidence and why bounded

Medium-high on the diagnosis: the mis-wiring facts are directly observed
(files, greps, validator code paths, git ancestry) — only the "silently skips"
behavior is static-path inference (deterministic, but not executed). Bounded
on direction: the recommendation's direction rests on your recorded prior
decisions plus your clarification answer, not on repository inference alone.

## 9. Owner intent

**Asked and used.** One high-information question (frozen in
clarification-v1.md) was asked because the counterfactual held — an answer of
(b) would have made reconciliation the focus. You answered (a), which the
evidence supports.

## 10. Prior owner decisions

**Preserved:** P-series closed (no P5); S1 as agreed next direction; PyPI
publication not re-promoted (P2 standing correction); INFRA acceptance
criteria as stated in the PRD. Nothing challenged.

## 11. What repository evidence established vs. what required owner judgment

- **Established by evidence:** the four gaps are committed-but-mis-wired;
  the canonical tree lacks two of the four fixes; the validator no-ops on
  checks 2-3; tests green-light legacy content; the P1 execution surface is
  fixed.
- **Required your judgment:** the direction/sequencing choice — which thread
  is the focus next. That is strategic priority, not derivable from the tree.

---

**Probe note:** Canonical validation failed with 16 quote-verification
errors. The result is preserved as execution evidence and is not used to
determine the S1 interaction disposition; no repair or rerun occurred.
