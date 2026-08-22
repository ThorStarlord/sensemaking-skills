# ADR 0016: Evidence Policy for Repository Findings

**Status**: ACCEPTED (with a ratified addendum) — 2026-07-26 by explicit
owner decision (D5, D9) recorded in
`docs/OWNER-DECISION-PACKAGE-2026-07-26.md`
**Date**: 2026-07-25 (revised 2026-07-26; current-contract reconciliation 2026-08-18)
**Resolves**: Issue #31

**2026-07-26 addendum, owner-ratified**: the auteur campaign (PR #73, #75,
#77, #78) directly exercised this ADR's mechanics live. The owner explicitly
approved:
- **D5**: the independent substantive evidence audit is **mandatory only for
  absence/unreachability/dead-code/safety/ghost-feature and other high-risk
  claims**, not for every brief — this resolves the "which claims require
  evidence" threshold this ADR's promotion condition named explicitly.
- **D9**: PR #78's `UNKNOWN_WEAKNESS_TYPE` failure is legitimate under the
  current (brittle) contract, not a model-reasoning failure, and not a
  successful external validation either. The trace evidence (completed
  Grep/Read contradiction searches against real `auteur` symbols) confirms
  PR #75's contradiction-search discipline held live, independent of the
  unrelated taxonomy failure that stopped the run.

The owner's approval also separately ratified **D6** (human review depth:
approval required for every final brief during the next phase) — recorded
here because D6 has no other existing ADR home (see the product-contract
review's Part 6 issue mapping), though it is not itself part of this ADR's
promotion condition.

At the time of the 2026-07-26 revision, the product-contract review
(`docs/PRODUCT-CONTRACT-REVIEW-2026-07-26.md`, Part 4) additionally identified
one new deterministic check worth considering — verifying a cited `quote` is
actually present in the target file at/near the cited line range. That was a
candidate direction at this ADR revision, not part of the owner decision
recorded above. It was subsequently implemented through issue #80 / PR #81;
see the current-contract reconciliation below.

**2026-08-18 current-contract reconciliation — no new policy decision**:
subsequent implementation work evolved the concrete brief representation while
preserving this ADR's accepted evidence-policy boundary. Issue #80 / merged
PR #81 (`9a7d7d5ddc1f345dbac45da4cf480bbbe552aa30`) redesigned the brief contract
and implemented deterministic quote grounding. The current contract now has
three intentionally distinct evidence surfaces:

- Section 7 is the human-facing evidence narrative / logic trace. Current
  producer guidance supports investigative and durable citation modes, chosen
  for the consumer, while preserving state-currency and claim-provenance
  discipline.
- Section 8 carries structured `evidence_excerpts` objects with `file`, `lines`,
  `quote`, and `supports_claim`. The validator uses these for excerpt-shape and
  source-grounding checks.
- Section 13's authoritative machine-readable handoff carries a required
  `evidence` list of short file-level citation strings. `evidence` and
  `evidence_excerpts` are deliberately different fields; an
  `evidence_excerpts`-only Section 13 handoff does not satisfy the canonical
  machine-field contract.

The current validator also blocks a cited excerpt whose source text cannot be
grounded within the documented bounded line window (`EVIDENCE_QUOTE_NOT_FOUND`)
and reports a non-blocking warning when the quote is found only outside the
exact cited range or ambiguously within that window
(`EVIDENCE_QUOTE_WINDOW_MATCH`). This remains deterministic evidence-integrity
checking; whether the quote substantively supports the claim remains a human /
domain judgment, with the D5 high-risk audit boundary unchanged.

This 2026-08-18 edit reconciles the Accepted ADR with the already-operative
contract. It does **not** introduce a new evidence policy, field, validator
rule, routing behavior, Skill behavior, or Workflow-v0 change.

---

## Context

`repository_sensemaking_brief.md` and other findings artifacts need a
consistent, validator-enforceable evidence policy. Prior experience in this
repo (CLAUDE.md verification-discipline notes) already shows that an
over-strict evidence format (`Lx`-only citations) rejected valid output —
so this policy must be validated against what a real validator actually
consumes, not designed in the abstract.

## Decision

**Which claims require evidence**: Every claim that drives a consequential
diagnostic or routing recommendation (fog-type classification, recommended
workflow when present, weakest-boundary identification) requires supporting
evidence. Incidental observations in prose do not need their own independent
excerpt merely because they appear in the brief. D5 further requires an
independent substantive audit for absence/unreachability/dead-code/safety/
ghost-feature and other high-risk claims.

**Current representation**: Evidence is represented in complementary forms,
not one duplicated canonical field:

1. Section 7 contains the human-readable evidence narrative and required logic
   trace.
2. Section 8 contains structured excerpt objects:

```yaml
evidence_excerpts:
  - file: "path/relative/to/repo-root"
    lines: "10-20"
    quote: "..."
    supports_claim: "..."
```

3. Section 13 contains the authoritative machine-readable handoff field:

```yaml
evidence:
  - "path/to/file.ext (lines L10-L15): short citation supporting the diagnosis"
```

Both structured forms are machine-parseable, but they serve different
purposes. `evidence_excerpts` carries detailed source-grounding information;
`evidence` is the required machine-handoff summary consumed as part of the
artifact contract. The current contract and regression tests explicitly reject
using `evidence_excerpts` as a substitute for the required Section-13
`evidence` field.

**Path representation**: repository paths are relative to the target repository
root and use portable repository-relative forms rather than machine-specific
absolute paths.

**Placement**: evidence stays in dedicated evidence surfaces (Sections 7 and
8) plus the bounded Section-13 machine handoff, rather than being scattered as
ad hoc per-finding schema fragments.

**Citation format and consumer compatibility**: Section-8 excerpt `lines`
accepts both bare line numbers/ranges and `Lx`/`Lx-Ly` forms. Current producer
guidance additionally distinguishes investigative evidence (location-rich for
human inspection) from durable evidence (stable, grep-verifiable references
for downstream consumers). The active consumer/validator contract determines
which citation detail is required; do not infer that one historical syntax is
universally required across every consumer generation.

**Deterministic versus substantive validation**: validators may verify source
existence, line syntax/bounds, excerpt shape, and quote grounding. They do not
thereby prove that a quote supports a claim, that contradictory evidence does
not exist, or that the diagnosis/recommendation is substantively correct.
Those remain evidence-interpretation / review responsibilities.

## Consequences

- `validate-brief.py` requires the current machine-readable `evidence` field
  and independently checks the brief's evidence narrative/excerpt surfaces.
- Section-8 excerpts use the four-field `file` / `lines` / `quote` /
  `supports_claim` shape and are subject to deterministic quote grounding.
- Feeds ADR 0015 (deterministic fields): machine-consumed evidence structure is
  deterministic while recommendation and explanatory prose remain
  model-variable; deterministic structure does not imply substantive truth.
- High-risk evidence classes retain the D5 substantive-audit requirement even
  when all mechanical validators pass.

## Owner sign-off required

~~The mechanics below are already implemented and evidence-backed; owner
should confirm the "which claims require evidence" threshold before
promoting to Accepted.~~

**Given, 2026-07-26**: the owner ratified the threshold as D5 in
`docs/OWNER-DECISION-PACKAGE-2026-07-26.md`. Promoted to Accepted.

---

## Hypothesis

Claims that materially drive diagnosis or recommendation require supporting
evidence; incidental prose does not require an independent excerpt; evidence
structure is machine-checkable while substantive support remains a review
judgment. Citation syntax should be strict enough for the active consumer but
not stricter than the consumer actually requires.

## Supporting evidence

- PR #59 ("live Step-1 semantic validity proven", issue #58) specifically
  exercised the evidence-authority-hierarchy and evidence-citation-grammar
  path in a live `repo-sensemaker` run, and the resulting
  `repository_sensemaking_brief.md` passed `validate-brief.py` with real
  evidence content — direct evidence the mechanics work against live model
  output, not just fixtures.
- PR #65's live Step-2 evidence cites the brief's evidence as the basis for
  `proposed_direction.md`'s content, showing the evidence chain is consumed
  downstream, not just produced and ignored.
- CLAUDE.md's verification-discipline section documents the `Lx`-only format
  having previously and concretely rejected valid bare-number citations — a
  real, already-corrected incident rather than a hypothetical risk.
- Issue #80 / PR #81 implemented the later brief-contract redesign under this
  already-ratified policy: the Section-13 `evidence` handoff field, Section-8
  excerpt grounding, deterministic `EVIDENCE_QUOTE_NOT_FOUND` failure, and
  bounded-window warning semantics were updated as one producer/consumer
  contract change.
- `tests/test_repo_sensemaker_evidence_contract.py` directly exercises the
  current `evidence` machine-field contract, including negative cases for
  missing, empty, malformed, and stale `evidence_excerpts`-only handoffs.
- `tests/test_weakness_type_and_quote_contract.py` and
  `tests/test_quote_grounding_symmetric_normalization.py` exercise the current
  deterministic quote-grounding boundary without turning source existence into
  a substantive correctness claim.

## Missing evidence

- Mechanical evidence integrity still cannot establish whether an excerpt
  actually supports the claimed conclusion, whether important contradictory
  evidence was omitted, or whether the selected weakest boundary is useful;
  those remain substantive review questions by design.
- The accepted threshold (high-risk claims require deeper independent audit;
  ordinary consequential claims require proportionate evidence) remains a
  policy judgment. Normal-use evidence should continue to test whether it is
  too weak or too burdensome.
- Investigative versus durable producer guidance is a later operational
  refinement. Revisit if a real downstream consumer demonstrates that the two
  modes cannot coexist cleanly with the structured excerpt contract.

## Experiment or review trigger

Revisit if a consequential claim can pass the current evidence contract with
no meaningful supporting evidence; if deterministic grounding repeatedly
accepts misleading excerpts or rejects valid ones; if investigative/durable
mode differences create real consumer failures; or if a new artifact type
requires an evidence representation that does not fit this policy.

## Status rationale

**2026-08-18 current-contract reconciliation**: the accepted policy remains
operative. Issue #80 / PR #81 and later evidence guidance evolved its concrete
brief representation and deterministic grounding mechanics without changing
the D5 policy boundary. This ADR now describes that current contract and,
consistent with the ADR status convention, records `Resolves: Issue #31`.

**2026-07-26 update — promoted to Accepted.** Owner sign-off on the
enforcement threshold (D5) is now given, which was this ADR's stated
promotion condition. Preserved for record, the prior rationale:

**Provisional**: the then-current shape (`evidence_excerpts` YAML block, dual
citation format, placement) was implemented and exercised against live model
output in PR #59 and #65, going beyond a bare proposal. It was held short of
Accepted because the enforcement boundary (which claims strictly require
evidence) had not been tested by a validator actually rejecting a
non-compliant claim, and owner sign-off on the threshold itself was
outstanding.
