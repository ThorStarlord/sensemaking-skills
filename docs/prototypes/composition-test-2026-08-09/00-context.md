# Composition test — context and framing

**AGENT_SELECTED_TARGET** (matching the P2-P4/S1 experiment convention):
this question was chosen by me, not posed by a real owner in the moment.
The proportional claim this test can support: "given an agent-selected
plausible repository decision, the two-skill composition (repo-sensemaker →
repository-diagnostician → vnext-review-consumer) was exercised end-to-end
and observed for redundant vs. distinct reasoning." It does NOT establish
owner demand or test a genuinely owner-originated decision — see
`04-composition-assessment.md` for what this specifically cannot show.

**Target repository:** sensemaking-skills itself (this repo).

**Question:** Given everything currently true about this repository (PR
#163 open, the stale `fog_type` runtime alias, three further
canonical-vocabulary.yaml drift items discovered incidentally, a real
version-string drift, and the previously-recorded INFRA-004 gap), what is
the single most consequential boundary right now, and what should happen
next?

**Why this question, not "should Option A be kept"**: using the prototype
to evaluate its own packaging question would be circular in a way that
makes the result hard to interpret. This question is real, decision-
relevant, and genuinely separate from the packaging question — a cleaner
test of whether the *process* (delegate → brief → consume) works, not of
the packaging conclusion itself.

**Sequence exercised:**
1. `repository-diagnostician` investigates and produces a vNext brief —
   `01-repository-diagnostician-brief.md`.
2. `repo-sensemaker`'s interaction layer reads the brief, decides whether
   to ask, and recommends — `02-repo-sensemaker-interaction-synthesis.md`.
3. `vnext-review-consumer` evaluates a concrete `proposed_direction`
   against the brief — `03-vnext-review-consumer-output.md`.
4. Honest assessment of whether the split helped or added ceremony —
   `04-composition-assessment.md`.
