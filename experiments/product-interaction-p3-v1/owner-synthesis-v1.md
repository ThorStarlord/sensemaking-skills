# Task P3 — Owner Synthesis (compact, decision-facing)

experiment_type: product_interaction
record: owner-synthesis-v1
target_repository: auteur @ 374abb48fb1f39d1ddb140df9b43b34cf53f4beb
owner_question: "What engineering work would create the most value next?"
produced_from: repo-sensemaker-investigation-v1 (one-shot, read-only)

---

## 1. Recommended action

**Complete the Cartographer pilot v2 behavioral evaluation before any new
feature slice.** Concretely: provide one fixed provider/model through your
normal secure path, generate the ≤8 designed calls, construct and validate the
captures, and run the preregistered two-reviewer blinded review (H1–H6). The
kit is already designed, frozen at a pinned SHA, and waiting only on this
decision.

## 2. Why it matters now

Auteur is at v0.37.1 with 24 minor versions shipped since the last changelog
entry (v0.12.0, 2026-07-22) — yet the core "literary compiler" promise is
behaviorally unproven: pilot v1 didn't establish usefulness, the full
end-to-end authored path has never been run, and your own review record says
"Behavioral usefulness remains unproven." Every feature built on that
unvalidated layer is priority-risky. The marginal cost of finishing the
evaluation is at its lowest now — the design is done, frozen, and blocked only
on a provider decision.

## 3. Strongest supporting evidence

- `docs/reviews/2026-07-28-cartographer-profile-emotional-target-evaluation.md:152` —
  "Is another implementation slice warranted? No; evaluation infrastructure or
  safe provider access is needed first." (your own prior conclusion)
- Same file, line 160 (your live record): "The next operator action is to
  provide one fixed provider/model … then generate at most eight calls and
  construct/validate captures before review. Behavioral usefulness remains
  unproven."
- `docs/superpowers/specs/2026-07-30-cartographer-agent-native-pilot-v2.md:20` —
  pilot v1 "did not establish behavioral usefulness: treatment and control each
  won 2/4 pairs".
- `docs/pilot-report.md:114-117` — "The full end-to-end authoring pilot is not
  complete."

## 4. Strongest credible alternative

**Backfill the version ledger instead** (CHANGELOG v0.13–v0.36, README
coverage for `portfolio` and later subsystems, rename the duplicate ADR-013).
This is real, cheap, and defensible as a bounded deferral if provider access
or reviewer bandwidth is genuinely unavailable. But it resolves none of the
value question — it makes the 24 undocumented versions legible, not validated.
A second, heavier alternative is the end-to-end dogfood project the 07-15
pilot named as its next prerequisite (3–5 Scene Realizations, accepted prose,
one external edit, reconciliation).

## 5. Most important remaining uncertainty

Whether the provider capture is even worth running as designed: if you no
longer believe the Cartographer/profile layer is the highest-value surface
(versus, say, productizing the deterministic engine or changing the creative
interaction entirely), then completing a frozen evaluation of it is
low-value. The evaluation answers "does this feature help?" — it cannot
answer "is this the right feature to be evaluating?" That ranking is yours.

## 6. Cheapest credible next action / probe

The ≤8-call capture itself: one fixed provider/model, local-only retention,
construct and validate the captures (the deterministic validator already
exists), then the two-reviewer review. No new code, no new evaluation
machinery, no repository changes.

## 7. Confidence and why it is bounded

Medium. The evidence that the evaluation is the documented next step is
strong (your own review, the frozen kit). The claim that evaluation should
outrank all feature work rests on an inference about velocity outrunning
evidence (24 versions in ~6 days, changelog gap), which is an inference, not
a measured fact. The recommendation would be wrong if you have an external
reason (market, user demand, contractual) to prioritize a specific feature —
that context is not in the repository.

## 8. Prior owner decision preserved or challenged

**Preserved:** the v2 pilot design — the four retained cases, pinned SHA,
two-reviewer blinded protocol, and H1–H6 preregistration — is exactly what
this recommendation executes; nothing in the repository evidence gives reason
to challenge it.

**Challenged (implicit default, not a stated decision):** the default of
continuing feature velocity while behavioral evidence is pending. The
changelog-vs-code gap (v0.12.0 → v0.37.1) shows that default has been running
for ~24 versions. This recommendation does not ask you to stop features
forever — it asks you to let the ≤8 calls land before the next slice.
