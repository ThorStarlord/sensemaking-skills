# Repository Sensemaking Brief — sensemaking-skills @ origin/main

Investigation for Task P2 (decision-sharpening probe). Canonical
`skills/repo-sensemaker/SKILL.md` standalone invocation, exactly once, at
frozen SHA `e2e859b60c255c5b02ea74083cfca94db28601d0`.

Owner question: "After P1, should the standalone repo-sensemaker validation
failure become the next engineering task, or is there higher-value product
work to do first?"

## 1. Repository goal

`sensemaking-skills` (origin: `ThorStarlord/sensemaking-skills`) builds an
agent-native framework that turns repository uncertainty into a diagnosed fog
type, a Repository Sensemaking Brief, and a workflow orchestration plan that
routes to implementation workflows. The product hypothesis being tested by
P1/P2 is narrower: that `repo-sensemaker` can investigate a repository and
leave the owner in a materially better position to decide what engineering
work should happen next. The repo itself is both the product and the main test
subject of the product-interaction experiments.

## 2. Current shape

- `skills/repo-sensemaker/` — the canonical skill under test (`SKILL.md`,
  `references/` with `repo-analysis-template.md`, `evidence-rules.md`,
  `weakness-types.md`, `ui-fog-signals.md`).
- `scripts/` — validator ecosystem: `validate-brief.py` (brief validator,
  quote grounding), `validate-and-report.py` (documented agent-facing entry
  point), `brief_skeleton.py` + `evidence_quote_extractor.py` (runtime-only
  quote reconciliation), `skill_executor.py` / `workflow-runtime.py`
  (runtime execution path).
- `src/sensemaking_skills/` — installed package: `cli.py` (`analyze`, `test`,
  `validate`), `validation.py` (vocabulary-only validation), `setup_skills.py`
  (0.2.2), packaged `skills/`.
- `skills/workflow-planner/` — downstream consumer (`SKILL.md` reads
  `recommended_workflow_id`, `primary_fog_type`, escalation flags from the
  brief; `references/workflow-registry.yaml`, `references/artifact-contracts.yaml`).
- `experiments/product-interaction-p1-v1/` — P1 evidence (owner-pre/post,
  learning, disposition); P1-R `clean-install-reproduction-p1-r-v1/`; P1-F
  distribution repair merged as PR #156 (commit `1935796`).
- `tests/` — large suite incl. `test_field_contract_agreement.py`,
  `test_quote_grounding_symmetric_normalization.py`, validator fixtures.
- `GETTING_STARTED.md` — documents the agent-native (clone-based) and
  CLI/installed usage paths.

## 3. Strong signals

1. **The distribution surface repair landed in source.** P1-R (PR #155)
   confirmed PyPI `0.2.1` ships no SKILL.md trees and no `setup-skills`
   command; P1-F (PR #156, `1935796`, merged at `e2e859b`) makes the 0.2.2
   wheel ship canonical skill trees byte-identical, with drift detection.
   `CHANGELOG.md` L9-L12 records this. The P1 sequence "verify distribution ->
   fix if confirmed" is complete.
2. **The validator itself is not broken.** `tests/fixtures/repo-sensemaker-template-canonical.md`
   (a brief with a byte-exact verbatim quote) passes `validate-brief.py`
   cleanly — verified in this run: `valid: true`, zero errors. Quote
   grounding (issue #80, `scripts/validate-brief.py` L728-L762) only rejects
   quotes that are not found verbatim near the cited range.
3. **Runtime quote fidelity is solved by design.** Issue #89 ("Preserve
   verbatim evidence quotes") is CLOSED via acceptance option B: the runtime
   populates quotes deterministically from source ranges
   (`evidence_quote_extractor.py`, wired through `brief_skeleton.reconcile()`,
   invoked by `skill_executor.py` L1973-L1980 in the runtime-skeleton path).
   The model is deliberately removed from the verbatim-copy boundary in
   runtime mode.
4. **Contract discipline is enforced.** `tests/test_field_contract_agreement.py`
   pins machine-field reads to `artifact-contracts.yaml`; the brief contract
   declares its required machine fields and consumers (`workflow-planner`,
   `prompt-handoff`, `sensemaking-docs-reconciler`).
5. **Experimental discipline is high.** P1 preserved its validation failure
   as evidence rather than repairing it; P1-R/P1-F were kept strictly scoped;
   PR #156 explicitly did not touch "the standalone validator issue".

## 4. Missing pieces

1. **Published 0.2.2.** PyPI still serves only `0.2.1` (verified via PyPI
   JSON: `version: "0.2.1"`, one release). The repair exists in source but
   has not reached a single user. `publish or repair PyPI` remains an owner
   decision (explicitly out of P2's scope).
2. **A mode-aware producer instruction.** `skills/repo-sensemaker/references/repo-analysis-template.md`
   L75-L82 tells every producer to write a placeholder quote because "the
   runtime overwrites it" — with no conditional for standalone invocation,
   where no runtime exists to do the overwrite.
3. **A functioning standalone validation surface on the installed path.**
   `src/sensemaking_skills/cli.py` L89-L97: the documented
   `sensemaking-skills validate` command prints instructions to run
   `scripts/validate-and-report.py` and returns — it does not validate, and
   `scripts/` are not shipped in the wheel (setup.py packages only
   `sensemaking_skills`). Documented in `GETTING_STARTED.md` L99 and the
   PyPI README as if it validated.
4. **No dedicated issue for the standalone validation failure.** PR #156's
   body references "the standalone validator issue" as an open item, but a
   title search finds no issue filed for it (P1 preserved it as experiment
   evidence only).
5. **The owner-facing synthesis step.** P1's learning record identified that
   the 14-section machine brief needs translation into a compact owner-facing
   synthesis and the skill has no such step; P1's decision value came from
   that translation being done by the agent, not the product.

## 5. Improvement opportunities

- Make the template's Section 8 quote guidance mode-aware (runtime mode ->
  placeholder; standalone mode -> verbatim quote or a standalone
  reconciliation pass reusing `evidence_quote_extractor.py`).
- Make `sensemaking-skills validate` either validate or stop claiming to
  (and ship the validator in the wheel if validation is a product promise).
- File the standalone validation failure as an issue with the P1 evidence
  reference, so it stops being an orphaned finding.
- Publish 0.2.2 once the owner decides (separate decision).
- Keep experimental scaffolding minimal (P2 has no scorer, no new schema, no
  campaign machinery — correct).

## 6. Weakest boundary

The weakest boundary is the **standalone execution surface of
repo-sensemaker: the producer instructions contradict the artifact contract
unless the runtime is present.**

Concretely, in standalone (agent-native, documented) invocation:

- The template instructs the producer to write `"see file/lines"`-style
  placeholder quotes (repo-analysis-template.md L75-L82), because the runtime
  overwrites quotes before validation (issue #89 design).
- The validator requires every non-empty `quote` to exist verbatim near the
  cited lines, as a blocking check (`EVIDENCE_QUOTE_NOT_FOUND`,
  validate-brief.py L728-L762).
- The quote overwrite only happens in the runtime-skeleton path
  (skill_executor.py L1973-L1980 -> brief_skeleton.reconcile ->
  evidence_quote_extractor); standalone invocation has no reconciliation
  step.
- Therefore a producer that follows the canonical instructions as written,
  standalone, produces a brief that fails its own validation — P1 observed
  exactly this (3 blocking `EVIDENCE_QUOTE_NOT_FOUND` on multiline excerpts),
  and the mechanism is unchanged at the current SHA.

On the installed path the same surface is worse: the documented
`sensemaking-skills validate` command does not validate at all
(cli.py L89-L97) — it prints instructions pointing at repo-only scripts.

This is not a validator defect: the validator correctly enforces the
verbatim-quote contract, the canonical fixture passes, and the runtime path
passes by design. The defect is that the product's own instructions are
**mode-blind**: they assume a runtime that standalone users do not have.

**Weakness type:** Contract Mismatch

(Adjacent but distinct: the CLI `validate` stub is a `Ghost Features`
instance — a documented command with no functioning implementation. Both
sit on the same standalone-validation surface; the Contract Mismatch is the
one that reproduces in the documented agent-native path and is therefore
primary.)

## 6.5. Problem classification (fog type)

- `primary_fog_type`: **architecture_fog** — the codebase signal is an
  execution-surface defect: an implicit, unvalidated dependency of the
  standalone path on a runtime-only reconciliation mechanism, plus a
  documented command that does not function.
- `user_implied_fog_type`: **product_fog** — the owner's question is about
  which product work to sequence next.
- `diagnosis_conflict`: **true** — the owner frames the question as a product
  defect choice ("fix validator vs. product work"); the codebase diagnosis is
  an execution-surface contract mismatch, which reframes what "fixing the
  validator" would even mean.
- `escalation_recommended`: false — the decision is resolvable from
  repository evidence; no human-gate machinery is needed, though the owner's
  judgment is the final arbiter.

## 7. Evidence

- `skills/repo-sensemaker/references/repo-analysis-template.md` (L75-L82):
  "the runtime overwrites `quote` with the exact verbatim text it reads from
  `file`/`lines` before validation runs (issue #89) ... Write a short
  placeholder for `quote` (e.g. `"see file/lines"`) rather than retyping the
  source text." This instruction is unconditional — it does not distinguish
  runtime from standalone invocation.
- `scripts/validate-brief.py` (L728-L762): quote grounding is enforced as a
  blocking `EVIDENCE_QUOTE_NOT_FOUND` when `quote` is non-empty and not found
  verbatim (after line-ending normalization / horizontal-whitespace
  collapsing) within a fixed window of the cited range. A placeholder string
  such as `"see file/lines"` cannot be found in any source file, so a
  template-compliant standalone brief fails.
- `scripts/skill_executor.py` (L1973-L1980): the reconciliation that replaces
  model-authored quotes with extracted source text runs only in the
  runtime-skeleton path (`brief_skeleton.reconcile`, which imports
  `evidence_quote_extractor` — see `scripts/brief_skeleton.py` L50, L319).
  Standalone invocation — the path documented in `GETTING_STARTED.md`
  (L55-L60: "Produce a `repository_sensemaking_brief` artifact ... Then
  validate it by running `python scripts/validate-and-report.py`") — has no
  reconciliation step.
- `tests/fixtures/repo-sensemaker-template-canonical.md` (L18-L25) + live
  check this run: a brief whose excerpt quote is byte-exact passes
  `validate-brief.py` (`valid: true`, zero errors). This isolates the defect
  to the producer-instruction side, not the validator.
- `src/sensemaking_skills/cli.py` (L89-L97): `sensemaking-skills validate`
  echoes "Validating: ..." then prints "To validate artifacts, run: python
  scripts/validate-and-report.py ..." and returns; `--json` is accepted but
  unused. The command performs no validation. `setup.py` packages only
  `sensemaking_skills` (L51), and `MANIFEST.in` does not include `scripts/`,
  so an installed user cannot run the suggested commands either.
- `skills/workflow-planner/SKILL.md` (L26): the downstream consumer reads
  `recommended_workflow_id` from the brief — Section 13 machine fields that
  are independent of Section 8 excerpt quotes. A brief failing only on
  `EVIDENCE_QUOTE_NOT_FOUND` still carries valid routing fields.
- `CHANGELOG.md` (L9-L12) and PyPI JSON (checked this run): 0.2.2 exists in
  source; PyPI still serves 0.2.1 only. The distribution repair has not
  reached users.
- `experiments/product-interaction-p1-v1/learning-v1.md`: P1's standalone
  run failed validation (3 blocking `EVIDENCE_QUOTE_NOT_FOUND`) yet still
  sharpened the owner's decision — the decision value came from the
  investigation substance, not from a validated artifact.

Logic trace: The documented agent-native path (GETTING_STARTED L55-L60) sends
the producer to the canonical skill, whose template (repo-analysis-template.md
L75-L82) instructs placeholder quotes on the assumption that "the runtime
overwrites it". That overwrite exists only in the runtime-skeleton path
(skill_executor.py L1973-L1980 -> brief_skeleton.reconcile ->
evidence_quote_extractor). The validator (validate-brief.py L728-L762)
blocking-rejects non-verbatim quotes — correctly per the artifact contract
(issue #80/#89). The fixture proves the validator passes when quotes are
verbatim, and the runtime proves the product passes when reconciliation
exists. Therefore the failing link is the mode-blind producer instruction in
standalone invocation: instructions and contract agree only when the runtime
is present, so the standalone path is an implicit dependency on a component
it never invokes. The same surface on the installed path degrades further:
the documented CLI validation command (cli.py L89-L97) is a stub, and the
scripts it points to are not shipped. That is why the weakest boundary is the
standalone execution surface (Contract Mismatch), not the validator — and why
"repair the validator" is the wrong framing for the owner's decision.

## 8. Evidence excerpts

```yaml
evidence_excerpts:
  - file: skills/repo-sensemaker/references/repo-analysis-template.md
    lines: L75-L82
    quote: "see file/lines"
    supports_claim: "Template unconditionally instructs placeholder quotes on a runtime-overwrite assumption"
  - file: scripts/validate-brief.py
    lines: L728-L762
    quote: "see file/lines"
    supports_claim: "Validator blocks non-verbatim quotes (EVIDENCE_QUOTE_NOT_FOUND)"
  - file: scripts/skill_executor.py
    lines: L1973-L1980
    quote: "see file/lines"
    supports_claim: "Quote reconciliation runs only in the runtime-skeleton path"
  - file: GETTING_STARTED.md
    lines: L55-L60
    quote: "see file/lines"
    supports_claim: "Documented standalone path: produce brief, then validate with scripts/validate-and-report.py"
  - file: tests/fixtures/repo-sensemaker-template-canonical.md
    lines: L18-L25
    quote: "see file/lines"
    supports_claim: "Canonical fixture uses a byte-exact verbatim quote and passes validation (verified this run)"
  - file: src/sensemaking_skills/cli.py
    lines: L89-L97
    quote: "see file/lines"
    supports_claim: "sensemaking-skills validate is a stub that prints instructions instead of validating"
  - file: skills/workflow-planner/SKILL.md
    lines: L26
    quote: "see file/lines"
    supports_claim: "Downstream consumer reads Section 13 routing fields, independent of excerpt quotes"
  - file: CHANGELOG.md
    lines: L9-L12
    quote: "see file/lines"
    supports_claim: "0.2.2 distribution repair exists in source; PyPI still serves only 0.2.1"
```

## 9. Why this boundary matters

If the standalone execution surface stays as-is, every agent-native run on
the documented path — including the owner's own product-interaction probes —
hits a blocking red gate through no fault of the analysis substance. The
bounded-retry protocol (using-sensemaking) then treats the brief as
unvalidated, and the product's own instructions actively cause the failure
(the template tells the producer to write quotes the validator must reject).
Because the contradictory instruction ships byte-identical in the 0.2.2
skill trees, the defect would propagate to every installed user once 0.2.2
is published. It does NOT block the machine handoff (Section 13 routing
fields are independent of excerpt quotes) and it did NOT block P1's decision
value — so its real impact today is friction and a credibility cost on the
documented path, not a downstream blockage.

## 10. Candidate next steps

1. **Make the standalone validation failure the next engineering task**
   (the owner's option A): file it as an issue, then repair. Note the repair
   target is NOT the validator (fixture passes; contract is correct) but the
   mode-blind guidance + stub CLI. Scope: template Section 8 mode-aware
   wording, GETTING_STARTED standalone reconcile step, CLI validate behavior.
2. **Defer it; do higher-value product work first** (option B): the
   owner-facing synthesis step (P1 learning #2 — the skill has no
   owner-facing surface) and completing the distribution repair by
   publishing 0.2.2, with the mode-aware guidance fix bundled in as a small
   hygiene item.
3. **Measure real-world impact first**: one more standalone-path run at the
   current SHA (the P2 run's own PHASE 5 is exactly this) to confirm the
   failure reproduces post-P1-F; there are no external users yet (PyPI still
   0.2.1), so "impact" today is the owner's own agent runs.
4. **Do nothing / defer indefinitely**: the failure does not block Section 13
   routing or human reading; the runtime path already solves quote fidelity
   for orchestrated runs. Credible only if standalone validation is
   deliberately demoted in the documented workflow.
5. **Reframe instead of repair**: change the documented primary path to make
   the runtime path (or a standalone reconcile step) the default, so the
   standalone path's contradiction disappears by documentation rather than by
   engineering.

## 11. Recommended next step

**Do not make the standalone validation failure the next engineering task.
There is higher-value product work first.**

Recommended sequence, in order:

1. Treat this P2 run's PHASE 5 standalone validation as the one-shot
   reproduction at the current SHA (cheapest credible probe; already paid
   for by this experiment). Expected: the failure reproduces, confirming the
   boundary is current.
2. Then prioritize product/interaction work — the owner-facing synthesis
   step identified in P1 learning — and, in parallel or immediately after,
   the owner's separate decision to publish 0.2.2 (the distribution repair
   still reaches no user).
3. Bundle the standalone-surface fix into that work as a small, testable
   hygiene item (mode-aware Section 8 guidance; make the CLI `validate`
   honest; optionally reuse `evidence_quote_extractor.py` as a standalone
   reconcile step), rather than as a dedicated validator-repair task.

Rationale: (a) the validator is not the defect — the fixture passes and the
runtime path is correct by design, so a "validator repair" task is
mis-scoped from the start; (b) the failure's real impact is a red gate on a
path with no external users and no downstream blockage, and P1 demonstrated
decision value survives it; (c) the owner's own documented post-P1 sequence
(verify distribution -> fix if confirmed -> then return to owner-facing
interaction work) has reached the interaction-work step; (d) the highest
unresolved product uncertainty is the interaction hypothesis itself, which
only the product work advances.

## 12. Recommended workflow

`fast-local-diagnostic` (from `skills/workflow-planner/references/workflow-registry.yaml`
L477-L508: repo-sensemaker -> handoff; `plan_only` is an allowed mode) — the
same shape this P2 run itself follows, with `plan_only` so nothing executes
until the owner decides.

## 13. Machine-readable handoff

```yaml
artifact_id: repository_sensemaking_brief
schema_version: 1
source_intent_ref: artifacts/01-orchestration-run/00-user-intent.md
user_implied_fog_type: product_fog
primary_fog_type: architecture_fog
diagnosis_conflict: true
escalation_recommended: false
evidence:
  - "skills/repo-sensemaker/references/repo-analysis-template.md (L75-L82): placeholder-quote instruction assumes a runtime overwrite that standalone invocation lacks"
  - "scripts/validate-brief.py (L728-L762): blocking verbatim quote grounding (EVIDENCE_QUOTE_NOT_FOUND)"
  - "scripts/skill_executor.py (L1973-L1980): quote reconciliation is runtime-skeleton-path only"
  - "GETTING_STARTED.md (L55-L60): documented standalone path ends with scripts/validate-and-report.py validation"
  - "tests/fixtures/repo-sensemaker-template-canonical.md (L18-L25): verbatim-quote fixture passes validation (verified this run)"
  - "src/sensemaking_skills/cli.py (L89-L97): sensemaking-skills validate is a stub"
  - "skills/workflow-planner/SKILL.md (L26): downstream consumer reads Section 13 routing fields only"
  - "CHANGELOG.md (L9-L12): 0.2.2 in source; PyPI still serves 0.2.1 (verified via PyPI JSON)"
  - "experiments/product-interaction-p1-v1/learning-v1.md: P1 decision value survived the validation failure"
recommended_workflow_id: fast-local-diagnostic
recommended_execution_mode: plan_only
weakest_boundary: "Standalone execution surface: producer instructions (placeholder quotes, runtime-overwrite assumption) contradict the artifact contract unless the runtime is present; installed-path CLI validate is a stub"
weakness_type: Contract Mismatch
weakness_type_explanation: null
required_inputs:
  - user_intent
  - repository_state
created_at: "2026-08-08T06:12:00Z"
immutable: true
```

## 14. Ready-to-copy prompt

"Decision: after P1, should the standalone repo-sensemaker validation failure
become the next engineering task, or is there higher-value product work
first? Evidence-based answer: defer the validator-repair framing. The
validator is correct (fixture passes; runtime reconciliation solves quote
fidelity by design, issue #89 closed); the defect is mode-blind producer
guidance (repo-analysis-template.md L75-L82) plus a stub CLI validate
(cli.py L89-L97) on the standalone/installed surface. Impact today: a red
gate on a documented path with no external users and no downstream blockage
(PyPI still 0.2.1; 0.2.2 unpublished; Section 13 routing unaffected). Next:
reproduce once at the current SHA (this P2 run's PHASE 5), then prioritize
owner-facing interaction/synthesis work per the owner's own post-P1 sequence,
bundling a small mode-aware guidance + CLI-honesty fix, and decide
separately on publishing 0.2.2. Do not start a dedicated validator-repair
task; do not modify the validator."
