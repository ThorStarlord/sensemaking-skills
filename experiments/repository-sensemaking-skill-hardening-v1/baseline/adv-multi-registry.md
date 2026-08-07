---
artifact_id: repository_sensemaking_brief
schema_version: 1
target_repo: experiments/repository-sensemaking-skill-hardening-v1/corpus/adv-multi-registry
source_intent_ref: artifacts/01-orchestration-run/00-user-intent.md
created_at: "2026-08-07T01:15:00Z"
primary_fog_type: docs_fog
workflow_registry_source: skills/workflow-planner/references/workflow-registry.yaml
recommended_workflow_id: docs-contract-reconciliation
escalation_required: false
weakest_boundary:
  type: Vocabulary Drift
  evidence: "docs/workflow-registry.yaml:2-3 lists workflow ids 'arch-implementation-workflow' and 'fastpath-workflow', which do not exist in the canonical skills/workflow-planner/references/workflow-registry.yaml (it has 'fast-path-workflow' at line 2 and 'architecture-implementation-workflow' at line 848), while .workflows/registry.yaml:2-3 lists the exact canonical spellings - the two repo-local registries disagree and one has drifted from the authoritative vocabulary."
immutable: true
---

# Repository Sensemaking Brief

Target repository: `experiments/repository-sensemaking-skill-hardening-v1/corpus/adv-multi-registry` — a four-file fixture (`README.md`, `main.py`, `.workflows/registry.yaml`, `docs/workflow-registry.yaml`) whose only substantive content is two conflicting workflow-registry metadata files. This brief is diagnostic only; no implementation is performed.

## 1. Repository goal

The repository is titled only `# multi-registry` (`README.md:1`) and contains a single one-line script `print('app')` (`main.py:1`). The only real content is workflow-routing metadata: `.workflows/registry.yaml:1-3` and `docs/workflow-registry.yaml:1-3` both claim to enumerate the sensemaking workflow IDs that apply to this repository. The apparent goal is a minimal application scaffold that also self-describes its workflow routing — but the goal is never stated anywhere, and the two registries that would define the routing contradict each other, so the repository's actual intent is unreadable from its own metadata.

## 2. Current shape

The repository is four small files:

- `README.md` (1 line) — bare heading `# multi-registry` (`README.md:1`); no body, no purpose statement, no usage.
- `main.py` (1 line) — `print('app')` (`main.py:1`); the entire executable surface.
- `.workflows/registry.yaml` (3 lines) — a `workflows:` list with ids `architecture-implementation-workflow` (`:2`) and `fast-path-workflow` (`:3`).
- `docs/workflow-registry.yaml` (3 lines) — a `workflows:` list with ids `arch-implementation-workflow` (`:2`) and `fastpath-workflow` (`:3`).

Absent entirely (structural proof from the directory listing): any README body or docs, any tests, any packaging metadata, any CI, and any code beyond the single `print` call.

## 3. Strong signals

- **Canonical spelling in `.workflows/registry.yaml`**: `architecture-implementation-workflow` (`:2`) and `fast-path-workflow` (`:3`) are exactly the ids registered in `skills/workflow-planner/references/workflow-registry.yaml` (lines 848 and 2 respectively) — whoever wrote this file had the authoritative vocabulary.
- **Conventional metadata placement**: workflow metadata lives in the conventional `.workflows/` and `docs/` locations rather than being scattered or inline.
- **Well-formed YAML**: both registry files parse cleanly (structure is valid; only the values in one file are wrong).
- **Trivially auditable surface**: four files, ~8 non-empty lines total, so the drift is cheap to diagnose and to fix in either direction.

## 4. Missing pieces

- **A stated purpose**: `README.md:1` is a bare title with no description of what the repo is or does.
- **Any implementation**: `main.py:1` prints a constant string; there is no code for the registries to describe.
- **A single source of truth for routing metadata**: two registries exist (`.workflows/registry.yaml`, `docs/workflow-registry.yaml`) with no pointer, no `schema_version`, and no note about which is authoritative.
- **Validation of registry contents**: nothing checks that repo-local workflow ids exist in the canonical registry, so the invalid ids in `docs/workflow-registry.yaml:2-3` ship silently.
- **Tests or CI**: no test files and no pipeline exist.

## 5. Improvement opportunities

- Consolidate to one repo-local registry (or delete both and link the canonical `skills/workflow-planner/references/workflow-registry.yaml`), recording which file is authoritative.
- Add a lightweight check (script or CI step) that verifies every repo-local workflow id against the canonical registry — this would have caught the drift immediately.
- Expand `README.md:1` into a real purpose statement (what the app does, what the registries are for).
- Pin a `schema_version` or canonical-registry reference in whichever registry is kept, so future drift is detectable.

## 6. Weakest boundary

The weakest boundary is the repository's workflow-routing metadata itself: two registries, `.workflows/registry.yaml:1-3` and `docs/workflow-registry.yaml:1-3`, both claiming to enumerate the workflows that apply to this repo, and disagreeing with each other. `docs/workflow-registry.yaml:2` lists `arch-implementation-workflow` and `:3` lists `fastpath-workflow` — neither id exists anywhere in the canonical `skills/workflow-planner/references/workflow-registry.yaml` (which contains `fast-path-workflow` at line 2 and `architecture-implementation-workflow` at line 848), whereas `.workflows/registry.yaml:2-3` uses those exact canonical spellings. Any router or skill that consumes `docs/workflow-registry.yaml` will emit workflow ids that the validator rejects as hallucinated (`HALLUCINATED_WORKFLOW_ID`), or, worse, will silently route to a workflow that does not exist.

Logic trace: `docs/workflow-registry.yaml:2-3` and `.workflows/registry.yaml:2-3` are the only two files in the repository that carry machine-actionable routing vocabulary, and they disagree: the docs copy spells the ids `arch-implementation-workflow` (missing "-itecture") and `fastpath-workflow` (missing the hyphen), while the `.workflows` copy spells them `architecture-implementation-workflow` and `fast-path-workflow`. Cross-checking both spellings against the canonical registry (`skills/workflow-planner/references/workflow-registry.yaml`: `fast-path-workflow` at line 2, `architecture-implementation-workflow` at line 848; no `arch-implementation-workflow` or `fastpath-workflow` anywhere in its 22 registered ids) shows that the `.workflows` copy matches the authoritative vocabulary exactly and the `docs` copy matches nothing. Terms in the repository's documentation that do not match the authoritative vocabulary — and that have drifted even from the repo's own `.workflows` copy — are precisely the `Vocabulary Drift` weakness type ("Terms used in the README don't match the code or directory structure"). The near-miss spellings (`arch-implementation-workflow` vs `architecture-implementation-workflow`) are the same failure mode the validator's hallucinated-ID check exists to catch, which is why this boundary is the most dangerous thing in the repo: it is unenforced metadata that looks plausible.

**Weakness type:** Vocabulary Drift

## 6.5. Problem classification (fog type)

**Primary fog type: `docs_fog`.** Classification reasoning: the repository contains no frontend code at all (no React/Vue/Angular/HTML/CSS), so per the UI Fog Signals Registry decision tree it is not `ui_fog`; the code is a single one-line `print` call with no module boundaries, coupling, state management, or performance problems, so it is not `architecture_fog`; there is no vague user need or missing feature spec — the defect is that the repository's own specifications (its workflow registries) are inconsistent and unreliable, which matches the `docs_fog` definition ("Missing documentation, unclear specifications, knowledge gaps"). No user-intent artifact was supplied for this fixture run, so `user_implied_fog_type: unknown` and `diagnosis_conflict: false` — there is no user claim to conflict with the codebase diagnosis.

## 7. Evidence

- `README.md:1` — `# multi-registry`: the entire documentation surface is a bare title; no purpose is stated.
- `main.py:1` — `print('app')`: the entire implementation; there is no code the registries could describe.
- `.workflows/registry.yaml:2` — `- id: architecture-implementation-workflow`: canonical spelling, matches `skills/workflow-planner/references/workflow-registry.yaml:848`.
- `.workflows/registry.yaml:3` — `- id: fast-path-workflow`: canonical spelling, matches `skills/workflow-planner/references/workflow-registry.yaml:2`.
- `docs/workflow-registry.yaml:2` — `- id: arch-implementation-workflow`: not present in the canonical registry (which registers `architecture-implementation-workflow`, not this spelling).
- `docs/workflow-registry.yaml:3` — `- id: fastpath-workflow`: not present in the canonical registry (which registers `fast-path-workflow`, not this spelling).
- Canonical-registry cross-check: `skills/workflow-planner/references/workflow-registry.yaml` registers 22 workflow ids (lines 2-942), including `fast-path-workflow` (line 2), `docs-contract-reconciliation` (line 127), and `architecture-implementation-workflow` (line 848); neither `arch-implementation-workflow` nor `fastpath-workflow` appears anywhere in the file.

**Logic trace:** The repository carries two machine-actionable registry files. `.workflows/registry.yaml:2-3` uses the exact canonical ids (`architecture-implementation-workflow`, `fast-path-workflow`), while `docs/workflow-registry.yaml:2-3` uses near-miss spellings (`arch-implementation-workflow`, `fastpath-workflow`) that appear nowhere in the canonical registry and that contradict the repo's own `.workflows` copy. Because `README.md:1` provides no purpose statement and `main.py:1` provides no code, the registries are the only specification of how this repository is meant to be processed — and that specification is internally contradictory, with the `docs/` copy drifted from the authoritative vocabulary. That is `Vocabulary Drift`: the documented terms do not match the authoritative vocabulary, so any consumer of `docs/workflow-registry.yaml` will resolve to non-existent workflow ids. Since the defect lives in the repository's documentation/metadata layer rather than in code structure, this classifies as `docs_fog`.

## 8. Evidence excerpts

```yaml
evidence_excerpts:
  - file: docs/workflow-registry.yaml
    lines: L2
    quote: "  - id: arch-implementation-workflow"
    supports_claim: "The docs registry spells the workflow id without '-itecture'; this exact spelling does not exist in the canonical registry."
  - file: docs/workflow-registry.yaml
    lines: L3
    quote: "  - id: fastpath-workflow"
    supports_claim: "The docs registry drops the hyphen from 'fast-path-workflow'; this exact spelling does not exist in the canonical registry."
  - file: .workflows/registry.yaml
    lines: L2
    quote: "  - id: architecture-implementation-workflow"
    supports_claim: "The .workflows registry uses the exact canonical spelling (workflow-registry.yaml:848), showing the two repo-local registries disagree."
  - file: .workflows/registry.yaml
    lines: L3
    quote: "  - id: fast-path-workflow"
    supports_claim: "The .workflows registry uses the exact canonical spelling (workflow-registry.yaml:2), contradicting docs/workflow-registry.yaml."
  - file: README.md
    lines: L1
    quote: "# multi-registry"
    supports_claim: "The entire README is a bare title; the repository's purpose and routing intent are undocumented."
  - file: main.py
    lines: L1
    quote: "print('app')"
    supports_claim: "The entire implementation is a constant print; there is no code for the workflow registries to describe."
```

## 9. Why this boundary matters

Routing metadata is the entry point for any automated processing of this repository. A router consuming `docs/workflow-registry.yaml:2-3` will either emit a workflow id the validator rejects as hallucinated (`HALLUCINATED_WORKFLOW_ID`, a blocking error) or, if the invalid id is consumed by a system that does not validate, silently invoke a workflow that does not exist anywhere. The near-miss spellings make the drift especially insidious: `arch-implementation-workflow` and `fastpath-workflow` look like plausible ids and will pass human review, while every consumer that trusts the docs copy produces different behavior from every consumer that trusts the `.workflows` copy. Two sources of truth also mean the drift will widen over time as the copies are maintained independently, and because `README.md:1` states no purpose and `main.py:1` implements nothing, there is no code or documentation to anchor which registry is correct. Until the registries are reconciled against the canonical `skills/workflow-planner/references/workflow-registry.yaml`, this repository cannot be reliably routed, validated, or extended.

## 10. Candidate next steps

1. **Reconcile the two registries**: keep one authoritative repo-local registry (`.workflows/registry.yaml`, which already uses canonical ids) and either correct or remove `docs/workflow-registry.yaml` — the smallest fix is changing `docs/workflow-registry.yaml:2-3` to `architecture-implementation-workflow` and `fast-path-workflow`, or deleting the file and pointing at the canonical registry.
2. **Add a validation check**: a script or CI step that verifies every repo-local workflow id against `skills/workflow-planner/references/workflow-registry.yaml` (this would have flagged both invalid ids immediately).
3. **Write a real README**: expand `README.md:1` into a purpose statement covering what the app does and which workflow registry is authoritative.
4. **Decide the repository's identity**: is this an application (`main.py`) that happens to carry routing metadata, or a workflow-metadata repo? If both, split them; if only metadata, drop the misleading `print('app')` scaffold.
5. **Pin the source of truth**: record `schema_version` and the canonical-registry reference in the surviving registry so future drift is detectable.

## 11. Recommended next step

Reconcile the two conflicting registries: correct `docs/workflow-registry.yaml:2-3` to the exact canonical ids (`architecture-implementation-workflow`, `fast-path-workflow`), or delete the file and leave `.workflows/registry.yaml:1-3` (already canonical) as the single source of truth, with an explicit note in `README.md:1` stating which file is authoritative. This is the smallest change with the highest leverage: it removes the only machine-actionable inconsistency in the repository, so that every consumer — human or automated — resolves the same valid workflow ids, and it makes future drift detectable. This brief is diagnostic only; no implementation is performed.

## 12. Recommended workflow

`docs-contract-reconciliation` — verified against `skills/workflow-planner/references/workflow-registry.yaml:127` ("Resolve drift between documentation, registries, artifact contracts, templates, and validator rules."). It is the registry workflow whose purpose exactly matches the diagnosed boundary: drift between the repository's registries and the authoritative registry. The repo-local `docs/workflow-registry.yaml:2-3` ids `arch-implementation-workflow` and `fastpath-workflow` were considered and rejected — they do not exist in the canonical registry, and recommending them would reproduce the very hallucination the validator's `HALLUCINATED_WORKFLOW_ID` check blocks. Recommended execution mode: `guided_execution` (allowed for `docs-contract-reconciliation` in the registry) — the reconciliation requires a human decision about which repo-local file is authoritative and whether the repo is an app, metadata, or both, so the drift fix should be reviewed rather than run autonomously.

## 13. Machine-readable handoff

```yaml
artifact_id: repository_sensemaking_brief
schema_version: 1
source_intent_ref: artifacts/01-orchestration-run/00-user-intent.md
user_implied_fog_type: unknown
primary_fog_type: docs_fog
diagnosis_conflict: false
escalation_recommended: false
evidence:
  - "docs/workflow-registry.yaml (lines L2-L3): lists workflow ids 'arch-implementation-workflow' and 'fastpath-workflow' that do not exist in the canonical workflow registry"
  - ".workflows/registry.yaml (lines L2-L3): lists the canonical ids 'architecture-implementation-workflow' and 'fast-path-workflow' - the two repo-local registries contradict each other"
  - "README.md (line L1): bare title '# multi-registry' with no purpose statement"
  - "main.py (line L1): 'print('app')' - trivial script, no implementation for the registries to describe"
recommended_workflow_id: docs-contract-reconciliation
recommended_execution_mode: guided_execution
weakest_boundary: Vocabulary Drift
weakness_type: Vocabulary Drift
weakness_type_explanation: null
required_inputs:
  - user_intent
  - repository_state
created_at: "2026-08-07T01:15:00Z"
immutable: true
```

## 14. Ready-to-copy prompt

> Run workflow `docs-contract-reconciliation` with `repository_state = [this repository]` for repository `experiments/repository-sensemaking-skill-hardening-v1/corpus/adv-multi-registry`. The repo-sensemaker brief classifies this as `docs_fog` with weakest boundary `Vocabulary Drift`: the repository carries two conflicting workflow registries — `.workflows/registry.yaml:2-3` uses the canonical ids `architecture-implementation-workflow` and `fast-path-workflow`, while `docs/workflow-registry.yaml:2-3` uses `arch-implementation-workflow` and `fastpath-workflow`, neither of which exists in `skills/workflow-planner/references/workflow-registry.yaml`. Constrain the plan to reconciliation: pick one authoritative repo-local registry (or link the canonical one), correct or remove `docs/workflow-registry.yaml`, and add a check that every repo-local workflow id is verified against the canonical registry. Do not use, recommend, or implement `arch-implementation-workflow` or `fastpath-workflow` — they are not registered workflow ids. Also surface, as an up-front clarification, whether this repository is meant to be an application (`main.py` prints a constant) or a workflow-metadata repository, and expand `README.md` from its bare title accordingly.
