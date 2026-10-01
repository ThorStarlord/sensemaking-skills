# Owner Decision Capsule

## 1. Decision Needed

Whether to authorize a **"simplify hard" program** for the Sensemaking Skills
control surface, and if so **which staged scope** to authorize now.

Trigger: the Strategic Sensemaking trials' control arm found *no demonstrated
benefit* for the skill on 2 of the 3 read-only tasks, against the pre-registered
bar of 2 of 3. Applying that rule, the honest verdict is **simplify hard**, not
"keep investing but simplify" (`docs/normal-use/strategic-sensemaking-trial-program-review.md`).

Interpreting the evidence honestly: **"1 of 3 means no demonstrated benefit yet,
not proven no benefit."** The skill did not demonstrably improve outcomes, and on
one task (Jellyfin) the control did better; the control also avoided
scope-invention on its own. The one clear skill win was catching milestone
inversion (AION). So this capsule packages a *simplification* decision, not a
retirement-or-stop decision.

## 2. Why Repository Evidence Cannot Resolve It

The survey below can establish which surfaces are **consumed** and how much
documentation is **orphaned**. It cannot establish:

- which surfaces the owner **values or intends to keep** for future use;
- the owner's **risk appetite** for removing user-visible skills;
- whether the ceremony cost is worth paying for a benefit the trials could not
  demonstrate at n=3.

Those are preference/policy/reserved-authority premises. Retiring a shipped
product surface is a product decision requiring an ADR (the same discipline the
earlier docs-cleanup decision used). Repository evidence reduces but cannot
settle the choice.

## 3. Credible Options

- **OPTION-A — Stage 1 only: documentation-volume reduction.** Classify every
  orphan/superseded doc and consolidate or archive it; **no runtime, validator,
  contract, or skill changes**. Bounded and highly reversible.
- **OPTION-B — Staged program (recommended shape):** Stage 1 docs → Stage 2
  runtime/enforcement surfaces that no consumer traces to → Stage 3 skill-count
  reduction, each stage independently gated and reversible, none starting before
  the previous stage's suite-green check.
- **OPTION-C — Defer and re-measure first.** Re-run the trials at ≥3 episodes per
  arm per task (fresh control) to test whether the #501 breadth doctrine already
  reduces the recurring friction, before authorizing any cut.
- **OPTION-D — Accept the current state.** Keep the surface and ceremony; revisit
  later. Lowest risk, keeps the recurring cost.

**Option-set adequacy.** A "stop / retire the control layer" option is **not**
packaged as materially credible: the evidence is "no demonstrated benefit *yet*,"
not proven harm; the control avoided scope-invention failures on its own without
evidence the skill harms outcomes; and the single skill win (milestone inversion)
argues against a stop. Presenting a stop option now would overstate the evidence.

## 4. Tradeoffs Reversibility and Deferral

| Option | Payoff | Risk | Reversibility | Deferral effect |
| --- | --- | --- | --- | --- |
| A | Smaller docs surface | Low (docs only; evidence-citation risk handled per-file) | High | Cost of a large orphaned-doc surface persists |
| B | Largest total reduction across docs/runtime/skills | Medium-high, staged | Per-stage high | Each stage can be reviewed/stopped; cuts postpone the RC3 freeze |
| C | Lower uncertainty before cutting | Very low | N/A | No reduction yet; new evidence may flip the verdict either way |
| D | None | None | N/A | Recurring ceremony cost and 495-doc / ~138k-line surface remain unreviewed |

Deferral note: **simplification must precede the RC3 freeze** (a candidate cut
after freezing forces requalification). Deferring (C/D) therefore also defers the
freeze.

## 5. Authority Effects

Selecting an option grants **only that option's staged scope**. No option
authorizes removing anything off-limits:

- artifact contracts, or validators with real consumers (`CLAUDE.md`: a
  validator rule must trace to a real consumer);
- anything pinned by `release-v1.0.yaml` or the qualification evidence;
- historical/evidence docs cited as immutable evidence.

Retiring a shipped **product surface** (Stage 2/3 candidates) would require its
own ADR and explicit owner authorization — the capsule does not grant it.

## 6. Evidence

Read-only survey, 2026-09-29 (`git ls-files`, tracked text files only; method =
substring counts; common-word skill/CLI names are inflated and flagged):

- **Docs volume:** `docs/*.md` = **495 files, ~137,737 lines**. **45** docs have
  zero inbound filename references and **36** have exactly one — mostly dated
  plans (`docs/superpowers/plans/*`), campaign/episode records, and superseded
  handoffs. These are the Stage-1 candidates, but many are *historical evidence*,
  so Stage 1 requires a per-file keep/archive/merge disposition, not deletion.
- **Policy-layer docs:** low inbound counts but **all have live test consumers**
  (inquiry 12, metareasoning 11, exploration/warrant/learning 8 each,
  adaptive-policy-coordinator 9, delegated-goal-patterns 6). They are **not**
  "nothing consumes them"; retiring them breaks tests. Stage 2 is therefore a
  *consolidation* question, not a deletion one.
- **Validators:** every `scripts/validate*.py` traces to at least one test/CI/docs
  consumer. Thin-consumer candidates (consolidation, not deletion):
  `validate-error-boundaries` (4), `validate-release-readiness` (4),
  `validate-semantic-reasoning-profile` (4), `validate-change-impact-analysis` (4),
  `validate-multi-repository-strategic-analysis` (4), the six `validate-pm-*`
  (5-11).
- **CLI families:** lowest references `analyze` (125), `journey` (95),
  `organization` (135), `setup-skills` (114); highest `campaign` (2350),
  `semantic` (1751) (both inflated by common words). Consolidation candidates
  are the low-use families.
- **Skills:** **51 canonical** (per `release-v1.0.yaml` / release contract). Lowest
  structured usage concentrates in the **PM/commercial** set:
  `coding-agent-native-campaign` (16), `ideal-customer-profile` (19),
  `external-evidence-packet` (20), `competitive-analysis` / `launch-checklist` /
  `measure-pmf` (21), `gtm` (22), `release-notes` (23), `customer-journey` (26).
  Skill removal is **Stage 3** (user-visible, hard to undo).

Control-arm records: `docs/normal-use/strategic-sensemaking-control-002/003/004.md`.

## 7. Machine-Readable Summary

```yaml
artifact_id: owner_decision_capsule
decision_id: OWNER-DECISION-SIMPLIFY-001
target_repository: ThorStarlord/sensemaking-skills
decision_statement: >-
  Authorize a "simplify hard" program for the Sensemaking Skills control surface,
  and choose the staged scope to authorize now; no surface is removed by this
  artifact.
repository_can_resolve: false
options:
  - option_id: OPTION-A
    statement: "Stage 1 only — classify and consolidate/archive orphaned or superseded documentation; no runtime, contract, validator, or skill changes."
    unlocks: ["Smaller documentation surface", "A per-file disposition method reusable for later stages"]
    tradeoffs: ["Smallest payoff", "Per-file work across ~81 low-link docs", "Historical-evidence docs need care"]
    reversibility: "high (docs-only; each file separately reversible)"
    deferral_effect: "Large orphaned-doc surface and its maintenance cost persist"
    authority_if_selected: ["Edit/consolidate documentation only; no product-surface removal"]
  - option_id: OPTION-B
    statement: "Staged program — Stage 1 docs, then Stage 2 unconsumed runtime/enforcement surfaces, then Stage 3 skill count; each stage gated by suite-green + CI parity and independently reversible."
    unlocks: ["Largest total reduction", "Stage-wise review and stop points"]
    tradeoffs: ["Medium-high risk at Stages 2-3", "Slower", "Stage 3 needs an ADR and is user-visible"]
    reversibility: "per-stage high; Stage 3 low"
    deferral_effect: "Postpones the RC3 freeze by the program duration"
    authority_if_selected: ["Authorizes only the explicitly approved stage; Stage 3 surface retirement still needs its own ADR/owner grant"]
  - option_id: OPTION-C
    statement: "Defer cuts; re-run the trials at >=3 episodes per arm per task with a fresh control to test whether the #501 breadth doctrine already reduces friction."
    unlocks: ["Lower uncertainty before any cut"]
    tradeoffs: ["No reduction yet", "Cost of more episodes", "Result may be 'still directional only' at n=3"]
    reversibility: "n/a (no cuts)"
    deferral_effect: "Delays both simplification and the RC3 freeze"
    authority_if_selected: ["Run additional read-only trials only"]
  - option_id: OPTION-D
    statement: "Accept the current state; keep the surface and ceremony and revisit later."
    unlocks: ["No change risk"]
    tradeoffs: ["Recurring ceremony cost remains", "495-doc / ~138k-line surface stays unreviewed"]
    reversibility: "n/a (no change)"
    deferral_effect: "Keeps the status quo; freeze unblocked by this decision alone"
    authority_if_selected: ["None beyond status quo"]
owner_decision_made_by_artifact: false
implementation_authority_established_by_artifact: false
created_at: "2026-09-30T00:00:00Z"
immutable: true
```
