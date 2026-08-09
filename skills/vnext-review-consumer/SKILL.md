---
name: vnext-review-consumer
description: "PROTOTYPE (prototype/repo-sensemaker-vnext, not canonical): a handoff-aware architectural-review-shaped consumer of the Repository Sensemaking Brief vNext. Built specifically to test whether analysis_vnext fields let a downstream consumer preserve decision-relevant nuance that the generic canonical architectural-review skill loses."
---

# vnext-review-consumer (PROTOTYPE — one native downstream consumer)

**Purpose of this skill's existence**: not to replace
[`architectural-review`](../architectural-review/SKILL.md) (canonical,
proven, ADR 0018's only routable workflow — unchanged, untouched by this
prototype). This skill exists to answer one question concretely: *does
consuming `analysis_vnext` actually preserve something a generic consumer
of the plain canonical brief would lose or get wrong?* Built after reading
the real `architectural-review/SKILL.md` in full, so every comparison below
is against its actual documented behavior, not an assumption about it.

## Same shape as the generic consumer, on purpose

Input: `repository_sensemaking_brief` (vNext) + `proposed_direction`.
Output: one of `pursue | pursue_narrowed | investigate_first | defer |
reject`, **plus** two new outcomes this skill can reach that the generic
one cannot represent at all (see below). Same boundary rule as canonical:
does not re-diagnose the repository; trusts the brief.

## Five concrete behavioral differences from generic `architectural-review`

### 1. `is_demonstrated_weakness: false` changes the framing question

Generic: evaluates "does the proposal address the identified weakness" —
presumes a weakness. If canonical `weakness_type` is absent (which the
generic skill's own Boundary Rule #4 conflates with "the brief is
incomplete or insufficient"), it may wrongly return `investigate_first`
for a brief that is actually complete and simply describes a non-defect
choice (P4's actual shape).

This skill: reads `analysis_vnext.consequential_boundary.is_demonstrated_weakness`
directly. If `false`, reframes the question as "does the proposal resolve
the consequential choice, and how reversible is that resolution?" — never
returns `investigate_first` merely because `weakness_type` is absent when
`is_demonstrated_weakness: false` explicitly says that's expected.

### 2. `uncertainty.source` picks the right kind of "not ready"

Generic: exactly one escape hatch for insufficiency —
`investigate_first`, "recommend running a more comprehensive fog
workflow." One-size-fits-all.

This skill: if the brief carries unresolved `uncertainty`, branch on
`source` before choosing an outcome:
- `repository_evidence` → `investigate_first` (matches generic — more
  investigation genuinely is the right next step here).
- `empirical` → new outcome `probe_first`: recommend the bounded probe
  from `uncertainty.question`; do not evaluate the architectural proposal
  against an unconfirmed empirical premise.
- `owner_intent` → new outcome `awaiting_owner_input` (see #3 — same
  outcome, reached via a different field).
- `external_environment` → `investigate_first`, but naming the external
  system to inspect, not "run a fog workflow" (nothing in this repo can
  resolve it).

### 3. `owner_intent_state.status` can block rendering a decision entirely

Generic: no field for this. Would proceed to render `pursue`/`reject`
using whatever's in the brief — silently resting the verdict on an
assumption about owner intent if the brief's prose doesn't happen to flag
the gap loudly enough for the reviewer (human or model) to notice.

This skill: checks `owner_intent_state.status` **first**, before any other
reasoning. If `blocking_unknown`, returns `awaiting_owner_input` and stops
— explicitly refuses to render `pursue`/`pursue_narrowed`/`defer`/`reject`
on a decision the brief itself says it couldn't confidently characterize
without owner input it doesn't have. This is the single clearest
"the native consumer prevents an invented-intent decision" test case.

### 4. `domain` (list) flags out-of-lens decision components

Generic: architecture-only lens by construction (its whole framing is
architectural risk / principal-engineer judgment). A brief whose
`domain` is `[product, architecture]` (P4's actual shape) would get a
purely architectural verdict that reads as if it covers the whole
decision.

This skill: if `domain` includes anything other than `architecture`,
states explicitly which domain(s) this review does not evaluate (e.g.
"the canonical-surface choice is a product decision outside this review's
competence; this review only addresses the architectural consequences of
whichever surface is chosen").

### 5. `discovery_confidence.level: low` qualifies the whole verdict

Generic: no representation for "we might be looking at the wrong
boundary." Any confidence issue has to be inferred from prose, if present
at all.

This skill: if `discovery_confidence.level` is `low`, prefixes its verdict
with an explicit caveat that the review is conditioned on a boundary that
repository-diagnostician itself was not confident was the right one, and
recommends against treating a `pursue` verdict here as high-confidence
regardless of how the architectural reasoning itself reads.

## Two new outcomes, only representable because analysis_vnext exists

- `probe_first` — the proposal cannot be evaluated until a bounded
  empirical probe resolves what's currently a hypothesis. Distinct from
  `investigate_first` (more repository investigation) and from `defer`
  (sound but wrong timing) — this is "sound reasoning, unconfirmed
  premise."
- `awaiting_owner_input` — the review cannot responsibly render a verdict
  without owner-owned information the repository can't supply. Distinct
  from `investigate_first` for the same reason `owner_intent` uncertainty
  is distinct from `repository_evidence` uncertainty everywhere else in
  this prototype (S1).

Both outcomes are new schema surface. They are declared here, in this
prototype skill, only — no canonical `artifact-contracts.yaml` entry, no
`weakness_type`-style ADR 0015 classification. If this skill is ever
promoted, these outcomes need their own review, same as everything else
here.

## Boundary rules (unchanged from generic, restated)

1. Does not re-diagnose the repository — trusts the vNext brief.
2. Evidence reuse only — cites brief sections, not repository files
   independently.
3. Not registered in canonical `skill-registry.yaml` or any workflow.
   Invoked directly during evaluation of this prototype.
4. Does not claim `architectural-review`'s proven-route status (ADR 0018)
   for itself. This is a comparison exercise, not a replacement.

## References

- [architectural-review](../architectural-review/SKILL.md) — the generic consumer being compared against (canonical, unchanged)
- [Repository Sensemaking Brief vNext template](../repository-diagnostician/references/brief-vnext-template.md)
- [Prototype assumption ledger](../../docs/prototypes/repo-sensemaker-vnext.md)
