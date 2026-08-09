# Repository Sensemaking Brief — sensemaking-skills @ 27aa2442

## 1. Repository goal

This repository is the **sensemaking-skills framework**: a local-first, artifact-driven, agent-native meta-layer that turns project uncertainty ("fog") into problem frames, research paths, and workflow-routed skill executions (CONTEXT.md L3-L4, L6-L8). Its flagship product surface is the **repo-sensemaker skill** — the diagnostic skill that this very brief is produced by — plus the orchestration/validation layer around it.

The repository is also, simultaneously, the **object of the frozen owner question**: "Should the next engineering work focus on interaction design or on standalone-contract cleanup (the four infrastructure gaps)?" — where "interaction design" means the S1-class product-interaction work for repo-sensemaker (investigation-first / clarify-if-needed owner interaction) and "standalone-contract cleanup" means the four gaps in 00-user-intent.md (evidence-rules dual-mode rendering; execution-mode decision criteria; skill-hygiene validator; artifact contracts for PM/engineering). The question is therefore self-referential: it asks where the next engineering effort in *this* repo should go, and the repo's own records (the P-series experiments) are direct evidence about one of the two options.

## 2. Current shape

- **Canonical skill trees** live under `skills/`: 15 skills including `skills/repo-sensemaker/` (SKILL.md + references: evidence-rules.md, repo-analysis-template.md, weakness-types.md, ui-fog-signals.md) and `skills/workflow-planner/` (SKILL.md + references: workflow-registry.yaml, skill-registry.yaml, artifact-contracts.yaml, execution-modes.md). `src/sensemaking_skills/setup_skills.py` L13-L18 declares `skills/` "the single authoritative repository-root skills/ tree" that the wheel ships (pyproject.toml L49 packages `skills/**/*`).
- **Legacy root copies** still exist and were the target of the infrastructure-fix work: `repo-sensemaker/references/` (evidence-rules.md 5806 B with dual-mode; repo-analysis-template.md 4502 B with a mode toggle; **no SKILL.md**) and `workflow-orchestrator/references/` (artifact-contracts.yaml 10216 B in old schema format; execution-modes.md with an AGENTS.md note; **no workflow-registry.yaml, no skill-registry.yaml, no SKILL.md**).
- **Validation stack**: `scripts/` contains ~30 validators; the shared loader `scripts/_validator_utils.py` L98-L115 resolves all registries from the **canonical** `skills/workflow-planner/references/` paths. `scripts/validate-skill-hygiene.py` (the INFRA-003 deliverable) is the sole validator that reads the **legacy** `workflow-orchestrator/references/` paths.
- **Tests**: `tests/` includes the INFRA deliverables' tests (`test_evidence_dual_mode.py`, `test_skill_hygiene_validator.py`, `test_artifact_contracts_pm_engineering.py`) and the pre-existing `test_field_contract_agreement.py` guardrail.
- **Governance**: 23 ADRs in `docs/adr/`; CONTEXT.md (391 lines) documents the architecture and known gaps; roadmap.md / CURRENT-PROJECT-STATUS.md describe a Phase 3-5 rollout that the commit history shows was completed and then superseded by hardening and experiment work.
- **Experiments**: `experiments/` holds `repository-sensemaking-skill-hardening-v1/` (hardening campaign closed with "CLOSED - REVISE (human disposition)" per reflog), `product-interaction-p1-v1` … `p4-v1` (owner POST + learning records), and the current probe `solution-interaction-s1-v1/` (charter + assisted context; this brief is its investigation artifact).
- **Version identity**: pyproject.toml L7 declares 0.2.2; README.md L77 still says "Expected version: 0.2.1" — minor version drift in the public surface.

## 3. Strong signals

1. **Mature governance**: 23 ADRs, a canonical-vocabulary registry, mode-coverage tracking, and a three-level validator hierarchy — the repo institutionalizes its own design principles (CONTEXT.md L36-L135, L340-L355).
2. **Field-contract guardrail exists and is real**: `tests/test_field_contract_agreement.py` L1-L16 was born from a real silent-routing bug and enforces that every machine field the runtime reads is declared in the canonical artifact contracts — a genuine, non-degenerate test.
3. **The four infrastructure-gap deliverables exist and are committed at the freeze SHA**: the May 28 commit "infra: Stabilize sensemaking skills with contracts, validation, and documentation" (reflog line 387) is an ancestor of the freeze commit; the PRD, issue list, dual-mode evidence rules, execution decision tree, skill-hygiene validator script, package.json script, and the four PM/engineering schemas are all present in the working tree, which is clean except the three unrelated frozen-identity entries. The work is not missing — it is mis-wired (see Sections 4-6).
4. **P-series decision-sharpening evidence is consistent and owner-rated**: P1-P4 each recorded an owner POST of "useful" / "clearly useful", with dispositions USEFUL_CONFIRMATION→STRONG_SHARPENING across four repositories, including a documentation-light one (P4). The owner closed the P-series deliberately (experiments/product-interaction-p4-v1/learning-v1.md L191-L200) rather than continuing to accrue value-validation cases.
5. **Distribution precondition was fixed**: P1's "serious execution-surface defect" (shipped wheel lacking skill trees) was confirmed by P1-R and repaired by P1-F (commit 1935796d, version 0.2.2, "wheel ships canonical skill trees, setup-skills resolves packaged resources with drift detection").

## 4. Missing pieces

1. **Dual-mode evidence rules are absent from the canonical skill tree**. The canonical `skills/repo-sensemaker/references/evidence-rules.md` (712 B) contains the five single-mode rules and no "investigative"/"durable" vocabulary; the dual-mode document (5806 B) lives in the legacy `repo-sensemaker/references/evidence-rules.md`. The canonical `skills/repo-sensemaker/references/repo-analysis-template.md` has no `<!-- mode: investigative | durable -->` toggle; the legacy `repo-sensemaker/references/repo-analysis-template.md` L87 does. Agents loading the canonical skill (the path `setup_skills.py` installs and the frozen identity fixes) never receive the INFRA-001 deliverable.
2. **The INFRA-001 test validates the wrong copy**: `tests/test_evidence_dual_mode.py` L11, L17, L49 hard-code `repo-sensemaker/references/*` — the legacy paths — so the test green-lights content the canonical tree does not contain.
3. **The skill-hygiene validator's two substantive checks silently no-op**: `scripts/validate-skill-hygiene.py` L90 loads `workflow-orchestrator/references/workflow-registry.yaml` and L121-L122 loads `workflow-orchestrator/references/skill-registry.yaml` and `artifact-contracts.yaml`; the first two files do not exist in `workflow-orchestrator/references/` (that directory contains only artifact-contracts.yaml and execution-modes.md), and the code responds with early `return` — L93-L94 "Skip if workflow registry doesn't exist" and L124-L129 — i.e., checks 2 and 3 PASS without checking anything. Only check 1 (npm scripts in `docs/*.md` and root AGENTS.md) executes.
4. **The INFRA-003 tests assert pass-on-clean, not detection**: `tests/test_skill_hygiene_validator.py` L44-L55 ("detects missing skill ID" / "detects missing artifact contract") merely run the validator and assert `returncode == 0` on the current codebase — exactly what a silently-skipping validator returns. No negative fixture is injected anywhere.
5. **The INFRA-002 cross-reference note is missing from the canonical copy**: the AGENTS.md decision-tree note exists in legacy `workflow-orchestrator/references/execution-modes.md` L3 but not in canonical `skills/workflow-planner/references/execution-modes.md` (no "Decision Tree"/"AGENTS.md" match anywhere in `skills/workflow-planner/references/`).
6. **The two artifact-contracts.yaml copies have diverged**: the canonical copy (`skills/workflow-planner/references/artifact-contracts.yaml` L185-L263) declares `prd`/`issue_list`/`agent_brief`/`code_patch` with `scope_expansion_requires_approval` required and `scope_expansion_status` recommended; the legacy copy (L112-L140) declares the same four ids with `prd_id`, `date`, `status` required instead — two divergent "contracts" for the same artifacts, and the new validator cross-refs against the legacy one.
7. **README version drift**: README.md L77 "Expected version: 0.2.1" vs pyproject.toml L7 "version = 0.2.2".
8. **No value-production runs exist** (CONTEXT.md L266, L322): every run to date is system-proving; the P-series are experiments, not orchestrator value-production runs.

## 5. Improvement opportunities

- After reconciliation (Section 11), delete the legacy root copies `repo-sensemaker/` and `workflow-orchestrator/` (or add a validate-repo.py drift check that fails when canonical and legacy reference files differ) so two-source-of-truth drift cannot recur.
- Repoint `scripts/validate-skill-hygiene.py` at the canonical registry paths via `_validator_utils` (it already exposes `load_workflow_registry`/`load_skill_registry`/`load_artifact_contracts`), and make the detection tests inject real negative fixtures (bad npm ref, fake skill id, fake artifact id) per the PRD's own acceptance criteria (PRD L108-L113).
- Add the dual-mode section to the canonical evidence-rules.md and the mode toggle to the canonical template, then delete the legacy copies so `test_evidence_dual_mode.py`'s paths still resolve.
- Update README version claims to 0.2.2 (or re-check what was actually published).
- Consider a canonical-tree integrity check inside `validate-repo.py` so "canonical tree satisfies its own contracts" becomes a checked invariant rather than an accident.

## 6. Weakest boundary

The weakest boundary is the **canonical-vs-legacy tree wiring of the contract layer**: the repository's own quality gates (tests and the INFRA-003 validator) validate *legacy root copies* of the skill references (`repo-sensemaker/references/`, `workflow-orchestrator/references/`) — copies that agents never load and that `setup_skills.py` never installs — while the canonical `skills/` trees that agents actually consume were never updated with the INFRA-001/INFRA-002 deliverables. The consequence is that the infrastructure-fix work the owner commissioned in 00-user-intent.md appears complete (deliverables exist, tests pass) while the canonical skill surface silently lacks two of the four fixes, and the validator that was supposed to prevent exactly this class of drift (missing cross-references) skips its two substantive checks against non-existent paths.

**Weakness type:** Implicit Dependencies

The mechanism is: skills/scripts/tests depend on specific file paths (`repo-sensemaker/references/evidence-rules.md`, `workflow-orchestrator/references/workflow-registry.yaml`, `workflow-orchestrator/references/skill-registry.yaml`) that are not declared anywhere as canonical and that diverge from the canonical tree installation actually uses — "depend on files or paths not explicitly defined or validated," verbatim the Implicit Dependencies definition (weakness-types.md L5). It carries a Zero Validation flavor (checks 2-3 of the validator validate nothing), but the root cause is the unenforced path dependency, not the absence of a check.

## 6.5. Problem classification (fog type)

**primary_fog_type: architecture_fog.** The codebase's actual signal is structural: duplicated reference trees with divergent content, a validator reading non-existent paths, tests pinning non-canonical locations. This is module-boundary/coupling drift in the framework's own structure, not a screen/flow problem (no frontend: ui-fog-signals Tier 1 check fails at "no frontend code"), not a documentation-absence problem (the repo is heavily documented), and not a user-needs problem in the code itself. The *owner's question* implies product_fog (a prioritization/direction decision), which is why `diagnosis_conflict` is true — but the conflict is the finding: the "contract cleanup" option is largely a done-but-mis-wired artifact, so the genuine open decision space is the interaction-design direction.

## 7. Evidence

**E1 — The four gaps are implemented and committed at the freeze SHA.**
The commit "infra: Stabilize sensemaking skills with contracts, validation, and documentation" is on main's ancestry (`.git/logs/HEAD` line 387: `51360cea → 9bf36df8`), well before the freeze commit (`.git/logs/HEAD` line 856: `d980bcdb → 27aa2442` "experiments/p3-v1: cross-repository decision-sharpening probe complete"). The working tree at freeze is clean except the three unrelated frozen-identity entries (modified `src/sensemaking_skills.egg-info/PKG-INFO`, untracked `.reasonix/`, untracked `experiments/product-interaction-p4-v1/`), so every INFRA deliverable file observed below is tracked and committed. The PRD (PRD-SENSEMAKING-SKILLS-INFRASTRUCTURE-FIX.md L9-L21) and issue list (ISSUE-LIST-SENSEMAKING-INFRASTRUCTURE-FIX.md L24-L151) define the four gaps as the user's goal.
Logic trace: the owner question offers "standalone-contract cleanup (the four infrastructure gaps)" as a candidate for *next* engineering work; the repository evidence shows that work was already executed and committed ~2 months before the freeze. The gap between the question's premise ("cleanup is pending") and the tree's state ("cleanup is done") is the first and largest reframe.

**E2 — The INFRA-001 deliverable landed in the legacy copy, not the canonical tree.**
The dual-mode document is `repo-sensemaker/references/evidence-rules.md` L5-L10 ("two output modes... Investigative... Durable") and L43-L64 (durable mode: file paths only, grep-verifiable); its template counterpart has the toggle at `repo-sensemaker/references/repo-analysis-template.md` L87. The canonical `skills/repo-sensemaker/references/evidence-rules.md` (the file the canonical SKILL.md's own References section points to) contains the five single-mode rules and no mode vocabulary; a repo-wide grep for `durable|investigative` under `skills/` returns zero matches. The INFRA-001 test hard-codes the legacy paths (`tests/test_evidence_dual_mode.py` L11, L17, L49).
Logic trace: what gets installed and consumed is `skills/` (setup_skills.py L13-L18; pyproject.toml L49). A test that validates `repo-sensemaker/references/` therefore measures content that no consumer receives, and its green result creates the false impression that INFRA-001 is delivered to the product. The canonical skill surface still runs single-mode evidence rules — which is precisely the dual-mode gap 00-user-intent.md L7 names.

**E3 — The INFRA-003 validator silently skips its two substantive checks.**
`scripts/validate-skill-hygiene.py` L90 loads `workflow-orchestrator/references/workflow-registry.yaml` and L121-L122 loads `workflow-orchestrator/references/skill-registry.yaml`; the directory listing of `workflow-orchestrator/references/` contains only `artifact-contracts.yaml` and `execution-modes.md`. The code path then returns early: L93-L94 (`return errors  # Skip if workflow registry doesn't exist`) and L124-L129 (skip if skill registry missing). Every other validator resolves registries from the canonical path (`scripts/_validator_utils.py` L98-L115 → `skills/workflow-planner/references/`). The INFRA-003 tests (`tests/test_skill_hygiene_validator.py` L44-L55) assert only `returncode == 0` on the clean tree — no injected negative fixtures — so a silently-skipping validator passes.
Logic trace: the PRD's own acceptance criteria (PRD-SENSEMAKING-SKILLS-INFRASTRUCTURE-FIX.md L108-L113) require the validator to *detect* a missing skill id and a missing artifact contract. The delivered validator cannot detect anything in checks 2-3 (its inputs do not exist), and the delivered tests cannot distinguish detection from no-op. The "skill-hygiene validator" thus validates, in practice, only `npm run` references in docs — the least consequential of the three checks.

**E4 — INFRA-002's note is in the legacy copy only.**
`workflow-orchestrator/references/execution-modes.md` L3 carries the "Agent Decision Tree" cross-reference; a grep for `Decision Tree|AGENTS.md` across `skills/workflow-planner/references/` returns nothing, so the canonical workflow-planner execution-modes document lacks the note. The decision tree itself (`docs/AGENTS.md` L1-L10, L77-L88) is present and matches the PRD's INFRA-002 acceptance criteria (1-3 skills / 4+ skills / "don't wait" override).
Logic trace: the primary INFRA-002 deliverable (the decision tree) is in place, but the cross-file note that routes orchestrator users to it exists only in the legacy copy — the same canonical-vs-legacy split as E2.

**E5 — The four PM/engineering contracts exist in two divergent versions.**
Canonical `skills/workflow-planner/references/artifact-contracts.yaml` L185-L263 declares `prd`, `issue_list`, `agent_brief`, `code_patch` with `source_intent_ref`/`user_goal_preserved_as`/`scope_expansion_proposed`/`scope_expansion_requires_approval`; legacy `workflow-orchestrator/references/artifact-contracts.yaml` L112-L140 declares the same four ids with `prd_id`/`date`/`status` required instead. `tests/test_artifact_contracts_pm_engineering.py` exists for the canonical set. The new validator's check 3 cross-refs against the legacy set (E3).
Logic trace: two files both claim to be "artifact contracts" for the same artifacts with different required fields; the runtime and validator stack read one, the INFRA-003 validator reads the other. This is the exact format-drift failure mode 00-user-intent.md L16 says the work was meant to prevent — now embodied by the fix itself.

**E6 — The owner's own recorded decisions already point to interaction design.**
P2 owner POST (experiments/product-interaction-p2-v1/owner-post-v1.md L50-L59): the owner's direction is "continuing higher-value product/interaction discovery first," with a standing correction that prior-decided-optional items (PyPI publication) must not be re-promoted without new evidence. P3 learning (experiments/product-interaction-p3-v1/learning-v1.md L110-L122): P-series paused; the owner's stated next step is "solution discovery for the owner-facing agent-native interaction" — invocation, synthesis, installation, persistence of owner context. P4 learning (experiments/product-interaction-p4-v1/learning-v1.md L191-L200): P-series closed by owner disposition ("no P5"); "Task S1 (Owner Interaction Shape Probe) proposed by the owner... recorded here as the agreed next direction; NOT started." P4 also sharpened the interaction shape: autonomous investigation → decision-level recommendation, with the one targeted owner question as an optional refinement (L52-L66, L96-L102).
Logic trace: the owner question asks me to choose between interaction design and contract cleanup. The repository's own experiment records show the owner already chose interaction design as the direction (P2-P4) and closed the evaluation campaign that would have justified more of it; the contract-cleanup option, meanwhile, is not an open workstream but a finished-then-mis-wired one. The evidence therefore supports: interaction design as the focus, plus a small reconciliation to complete the prior INFRA decision honestly.

**E7 — The P1 execution-surface precondition is resolved.**
P1 learning (experiments/product-interaction-p1-v1/learning-v1.md L72-L87) found the distribution/execution surface was a precondition for interaction work ("a precondition for any interaction improvement to have value") and that the standalone validation path had a usability gap (template's runtime-overwrite assumption, issue #89). P1-F (reflog line 850: "distribution surface repair - wheel ships canonical skill trees, setup-skills resolves packaged resources with drift detection (0.2.2)") closed the distribution half; pyproject.toml L49 now ships `skills/**/*`. The standalone-validation usability gap (runtime-owned skeleton assumption vs. documented standalone path) remains an open interaction-design-adjacent issue — which is itself S1-class material, not contract-cleanup material.
Logic trace: the main historical blocker to interaction-design work was the execution surface; it is fixed. No equivalent blocker stands between the owner and S1. The remaining contract-layer defect (E2-E5) is real but small and does not block an interaction probe.

## 8. Evidence excerpts

```yaml
evidence_excerpts:
  - file: 00-user-intent.md
    lines: L5-L10
    quote: "see file/lines"
    supports_claim: The four infrastructure gaps are the user's stated goal; this is the "contract cleanup" option in the owner question.
  - file: scripts/validate-skill-hygiene.py
    lines: L90-L94
    quote: "see file/lines"
    supports_claim: Check 2 loads a workflow-registry path that does not exist under workflow-orchestrator/references/ and silently returns.
  - file: scripts/validate-skill-hygiene.py
    lines: L121-L129
    quote: "see file/lines"
    supports_claim: Check 3 loads skill-registry.yaml and artifact-contracts.yaml from the legacy path; missing registry triggers silent skip.
  - file: tests/test_skill_hygiene_validator.py
    lines: L44-L55
    quote: "see file/lines"
    supports_claim: The "detection" tests only assert returncode 0 on the clean tree; no negative fixture is injected.
  - file: repo-sensemaker/references/evidence-rules.md
    lines: L5-L10
    quote: "see file/lines"
    supports_claim: Dual-mode (investigative/durable) documentation exists — but in the legacy root copy.
  - file: skills/repo-sensemaker/references/evidence-rules.md
    lines: L1-L5
    quote: "see file/lines"
    supports_claim: The canonical skill tree's evidence rules contain no dual-mode vocabulary; INFRA-001 never reached the consumed surface.
  - file: tests/test_evidence_dual_mode.py
    lines: L11-L24
    quote: "see file/lines"
    supports_claim: The INFRA-001 test validates the legacy paths, green-lighting content the canonical tree lacks.
  - file: workflow-orchestrator/references/execution-modes.md
    lines: L3
    quote: "see file/lines"
    supports_claim: The AGENTS.md decision-tree note exists in the legacy execution-modes copy.
  - file: skills/workflow-planner/references/execution-modes.md
    lines: L1-L11
    quote: "see file/lines"
    supports_claim: The canonical workflow-planner execution-modes document lacks the decision-tree note.
  - file: skills/workflow-planner/references/artifact-contracts.yaml
    lines: L185-L263
    quote: "see file/lines"
    supports_claim: The four PM/engineering contracts exist in the canonical contract registry.
  - file: workflow-orchestrator/references/artifact-contracts.yaml
    lines: L112-L140
    quote: "see file/lines"
    supports_claim: A divergent second version of the same four contracts (prd_id/date/status) exists in the legacy registry.
  - file: scripts/_validator_utils.py
    lines: L98-L115
    quote: "see file/lines"
    supports_claim: The canonical registry path is skills/workflow-planner/references/; validate-skill-hygiene.py is the outlier.
  - file: experiments/product-interaction-p4-v1/learning-v1.md
    lines: L191-L200
    quote: "see file/lines"
    supports_claim: Owner closed the P-series and proposed Task S1 (interaction-shape probe) as the agreed next direction.
  - file: experiments/product-interaction-p2-v1/owner-post-v1.md
    lines: L50-L59
    quote: "see file/lines"
    supports_claim: Owner's recorded direction is product/interaction discovery first; prior decisions are not reopened without new evidence.
  - file: .git/logs/HEAD
    lines: L387
    quote: "see file/lines"
    supports_claim: The infra stabilization commit (9bf36df8) is on main's ancestry, before the freeze SHA 27aa2442.
  - file: pyproject.toml
    lines: L7
    quote: "see file/lines"
    supports_claim: Package version is 0.2.2; README.md L77 still claims 0.2.1 (minor public-surface drift).
```

## 9. Why this boundary matters

If the canonical-vs-legacy wiring stays as it is, three bad things compound:

1. **The contract layer's trust is false.** 00-user-intent.md commissioned the four gaps "to prevent ad-hoc format drift" and "provide automated validation that breaks before deployment" (00-user-intent.md L14-L17). The delivered validator validates two of three checks against non-existent files and passes; the delivered tests certify that. The next drift will not be caught by the very machinery built to catch it — the exact failure mode the PRD says must "break before deployment, not in production" (00-user-intent.md L17).
2. **The owner's question cannot be answered on its own terms.** "Standalone-contract cleanup" is offered as pending work; the evidence says it is finished-but-mis-wired. Deciding focus on the premise that the gaps are open would either (a) re-do work that exists (waste), or (b) accept the current green tests as proof of completion (false assurance). Either way the decision is made against a misread of the tree.
3. **Interaction-design work inherits the defect.** The interaction shape being productized (investigation-first, one targeted question, decision-level recommendation) is delivered *by* the canonical repo-sensemaker skill; if the canonical tree's reference layer silently lags (single-mode evidence rules, missing execution-mode note), the productized surface ships with two of its four promised fixes absent.

None of this is catastrophic — it is a bounded reconciliation, not a rewrite. But it is exactly the kind of boundary the repo-sensemaker method exists to find: an unenforced dependency between what the repo claims to validate and what it actually validates.

## 10. Candidate next steps

1. **Reconcile the contract layer** (smallest, weakest-boundary repair): port the dual-mode evidence rules + template toggle and the execution-modes decision-tree note into the canonical `skills/` trees; repoint `scripts/validate-skill-hygiene.py` at the canonical registry paths; replace the pass-on-clean tests with real negative fixtures; then delete the legacy `repo-sensemaker/` and `workflow-orchestrator/` root copies (or add a drift check to validate-repo.py). ~1 day.
2. **Proceed with interaction design (S1)** as the substantive direction: run the Owner Interaction Shape Probe comparing interaction shapes on a real repository decision, per the owner's recorded next step (P4 learning L195-L200). This is the direction the evidence — and the owner's own records — support; the reconciliation above is a fast-follow, not a prerequisite blocker.
3. **Do nothing / defer both**: keep the freeze state; the mis-wiring persists but nothing in the current experiment pipeline depends on the canonical tree's dual-mode content. Credible only as a deliberate, time-boxed choice; as an unspoken state it is the drift trap the evidence already shows beginning.
4. **Re-run INFRA validation with honest fixtures before any further contract work**: implement the PRD's own acceptance tests (PRD L108-L113, L230-L239) as real negative tests, confirming which checks actually fail today — this converts the mis-wiring from inference into measured fact at low cost.
5. **Reopen P-series-style evaluation** (counter to owner disposition): another interaction probe on a third-party repo. Explicitly not recommended — the owner closed the series with diminishing-returns reasoning (P4 learning L191-L194); no new evidence in this investigation contradicts that closure.

## 11. Recommended next step

**Answer to the frozen owner question:** focus on **interaction design**. The four-gap contract cleanup is not an open workstream: the deliverables are implemented and committed at the freeze SHA, and what remains of them is a bounded wiring reconciliation, not a 2-day project. The interaction-design direction is the one the repository's own experiment records already ratify (P2 owner direction "product/interaction discovery first"; P3 "solution discovery for the owner-facing agent-native interaction"; P4 "Task S1... agreed next direction"), and the P1 execution-surface precondition for it is fixed (0.2.2).

The smallest concrete action with highest leverage is the **contract-layer reconciliation** (candidate 1), because it is the weakest boundary, it honestly completes the owner's prior INFRA decision, and it prevents the false-green assurance from silently compounding — after which S1 proceeds as the focus. Concretely: port the dual-mode evidence rules and template toggle into `skills/repo-sensemaker/references/`, add the decision-tree note to `skills/workflow-planner/references/execution-modes.md`, repoint `scripts/validate-skill-hygiene.py` (L90, L121-L122) at the canonical `skills/workflow-planner/references/` paths via `_validator_utils`, replace the pass-on-clean assertions in `tests/test_skill_hygiene_validator.py` with injected negative fixtures, and delete the legacy `repo-sensemaker/` and `workflow-orchestrator/` root copies.

## 12. Recommended workflow

`docs-contract-reconciliation` — "Resolve drift between documentation, registries, artifact contracts, templates, and validator rules" (skills/workflow-planner/references/workflow-registry.yaml L127-L159). Its step chain (repo-sensemaker → sensemaking-docs-reconciler → handoff) matches the reconciliation exactly, and it permits `plan_only`, keeping this diagnostic phase implementation-free. If the owner instead wants the *direction* itself formally risk-reviewed before committing, `architectural-review-planning-workflow` (registry L942-L979) is the fallback — but the reconciliation is the smaller, evidence-first move.

## 13. Machine-readable handoff

```yaml
artifact_id: repository_sensemaking_brief
schema_version: 1
source_intent_ref: "00-user-intent.md (root) + frozen S1 owner question: interaction design vs standalone-contract cleanup"
user_implied_fog_type: product_fog
primary_fog_type: architecture_fog
diagnosis_conflict: true
escalation_recommended: false
evidence:
  - "scripts/validate-skill-hygiene.py (L90, L121-L122): checks 2-3 read workflow-orchestrator/references/* paths; L93-L94, L124-L129 silently skip when files are absent"
  - "workflow-orchestrator/references (directory listing): contains only artifact-contracts.yaml and execution-modes.md; registry inputs for the validator do not exist"
  - "tests/test_skill_hygiene_validator.py (L44-L55): detection tests assert only returncode 0 on the clean tree"
  - "repo-sensemaker/references/evidence-rules.md (L5-L10, L43-L64): dual-mode docs exist in the legacy root copy only"
  - "skills/repo-sensemaker/references/evidence-rules.md (L1-L5): canonical skill tree has no dual-mode vocabulary (grep durable|investigative under skills/ = 0 matches)"
  - "tests/test_evidence_dual_mode.py (L11, L17, L49): INFRA-001 test validates legacy paths, not the canonical tree"
  - "workflow-orchestrator/references/execution-modes.md (L3): decision-tree note present in legacy copy; absent from skills/workflow-planner/references/execution-modes.md (L1-L11)"
  - "skills/workflow-planner/references/artifact-contracts.yaml (L185-L263) vs workflow-orchestrator/references/artifact-contracts.yaml (L112-L140): two divergent versions of the four PM/engineering contracts"
  - "scripts/_validator_utils.py (L98-L115): canonical registry path is skills/workflow-planner/references/; validate-skill-hygiene.py is the sole outlier"
  - ".git/logs/HEAD (L387, L856): infra stabilization commit 9bf36df8 predates freeze SHA 27aa2442; the four-gap deliverables are committed, not pending"
  - "experiments/product-interaction-p4-v1/learning-v1.md (L191-L200): P-series closed; S1 (interaction-shape probe) recorded as the agreed next direction"
  - "experiments/product-interaction-p2-v1/owner-post-v1.md (L50-L59): owner direction is product/interaction discovery first; prior decisions not reopened without new evidence"
recommended_workflow_id: docs-contract-reconciliation
recommended_execution_mode: plan_only
weakest_boundary: "Canonical-vs-legacy tree wiring of the contract layer: quality gates validate legacy root copies (repo-sensemaker/references/, workflow-orchestrator/references/) that agents never load, while the canonical skills/ trees lack the INFRA-001/002 deliverables and validate-skill-hygiene.py silently skips its two substantive checks."
weakness_type: Implicit Dependencies
weakness_type_explanation: null
required_inputs:
  - user_intent
  - repository_state
created_at: "2026-08-08T12:00:00Z"
immutable: true
```

## 14. Ready-to-copy prompt

For `workflow-planner` (plan_only) after this brief:

> Consume `experiments/solution-interaction-s1-v1/repo-sensemaker-investigation-v1.md`. Plan workflow `docs-contract-reconciliation` in plan_only mode against this repository. Scope: (1) dual-mode evidence rules (investigative/durable) and the `<!-- mode: investigative | durable -->` template toggle must land in the canonical `skills/repo-sensemaker/references/` tree; (2) the AGENTS.md decision-tree note must land in `skills/workflow-planner/references/execution-modes.md`; (3) `scripts/validate-skill-hygiene.py` must read registries from `skills/workflow-planner/references/` via `_validator_utils` and must fail loudly (not skip) when a registry is missing; (4) `tests/test_skill_hygiene_validator.py` detection tests must inject negative fixtures (missing npm script, missing skill id, missing artifact contract); (5) after reconciliation, legacy root copies `repo-sensemaker/` and `workflow-orchestrator/` are candidates for deletion or drift-check coverage — decide which, and record the decision. Do not implement; produce the reconciliation plan with the drift diagnosis and validator blind spots. Owner decision context: the four-gap contract cleanup was the owner's prior intent and is ~complete-but-mis-wired; the substantive next direction is interaction design (S1), per P2-P4 experiment records — this plan is the bounded completion, not a competing workstream.
