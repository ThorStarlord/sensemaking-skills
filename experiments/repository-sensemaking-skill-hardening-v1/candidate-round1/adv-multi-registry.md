# Repository Sensemaking Brief — adv-multi-registry

## 1. Repository goal

The repository carries no stated goal. The README (`README.md:1`) is a bare title — `# multi-registry` — with no description, no usage instructions, and no intent statement. What the repo *contains* (two workflow registries under `.workflows/registry.yaml` and `docs/workflow-registry.yaml`) suggests its only substantive purpose is to declare a workflow surface for routing, but nothing in the repo says that, and nothing says which registry (if any) is authoritative. The intended goal is therefore **UNKNOWN** from the repository alone (OBSERVED: `README.md:1` is the only documentation and contains no goal text).

## 2. Current shape

Inventory (all files, read in full — recursive listing shows exactly four files):

| Path | Lines | Content |
|---|---|---|
| `README.md` | 1 | `# multi-registry` (title only) |
| `main.py` | 1 | `print('app')` |
| `.workflows/registry.yaml` | 3 | `workflows:` + ids `architecture-implementation-workflow`, `fast-path-workflow` |
| `docs/workflow-registry.yaml` | 3 | `workflows:` + ids `arch-implementation-workflow`, `fastpath-workflow` |

**Runtime flow** (per the Architecture Reconstruction protocol):
- **Startup path**: the only executable artifact is `main.py:1` (`print('app')`); it is a single top-level statement with no entry-point ceremony, no imports, no CLI arguments. Running it prints `app` and exits. OBSERVED.
- **Orchestration**: none — there is no control flow beyond the one statement in `main.py:1`. OBSERVED.
- **Domain/core logic**: none — `main.py:1` performs no domain work. OBSERVED.
- **Persistence/state**: none — no files are written, no database, no cache, no environment-variable reads. OBSERVED (absence of any state-handling code in the only source file).
- **External integration points**: none. OBSERVED.
- **Background work**: none. OBSERVED.
- **Output boundary**: stdout only (`main.py:1`). OBSERVED.
- **Where responsibility becomes unclear**: the registry surface. Two files with the same purpose (`workflows:` → `- id:` lists), in two different locations (`.workflows/registry.yaml:1-3` and `docs/workflow-registry.yaml:1-3`), declare **different** workflow IDs, and nothing in the repo marks either as authoritative, stale, or a duplicate. A consumer (human or agent) cannot determine the repo's routing surface from the repo itself. OBSERVED.

**Dependency semantics**: no package manifest exists (no `pyproject.toml`, `setup.py`, `requirements.txt`, or lockfile was found in the recursive listing), so there are no `declared` dependencies. `main.py:1` imports nothing, so there are no `used`, `runtime`, `test`, `optional`, or `dead` imports. The registry files are not imported by any code — they are configuration data whose consumers are external (downstream routing tooling). The relationship "registry file → downstream router" is therefore **INFERRED** (no consuming code exists in this repo), not observed.

**State model**: no runtime state. The registries are *static* state read by external consumers — which consumer reads them, and which one wins when they conflict, is UNKNOWN.

**Boundary model**: the only meaningful boundary is *repository configuration → external routing tooling*. Nothing on either side is validated: the registries are not checked against any authority, and nothing records which file is the boundary's input.

## 3. Strong signals

- **Minimal, runnable skeleton**: `main.py:1` is a trivially executable program with no build machinery, no framework coupling, and no generated or vendored content (OBSERVED — recursive inventory is four files, zero build/config artifacts). A newcomer can run it with zero setup (DERIVED from `main.py:1`).
- **The `.workflows/registry.yaml` IDs coincide with the canonical registry**: `architecture-implementation-workflow` and `fast-path-workflow` (`.workflows/registry.yaml:2-3`) are both valid IDs in the canonical `skills/workflow-planner/references/workflow-registry.yaml` (canonical `- id: fast-path-workflow` at line 2; `- id: architecture-implementation-workflow` at line 848). If this file is the intended surface, the IDs are correct — though the file itself is untrusted as a *source* (see Section 6).
- **No conflicting product surface**: because `README.md:1` promises nothing, there is no README-vs-code promise mismatch to untangle.

## 4. Missing pieces

- **Any stated intent**: `README.md:1` is a title only; no goal, no scope, no usage (OBSERVED).
- **An authority marker for the registries**: nothing states which of `.workflows/registry.yaml` or `docs/workflow-registry.yaml` (if either) is authoritative, current, or a duplicate (OBSERVED — neither file contains comments or metadata beyond the id lists).
- **Consistency between the two registries**: they contradict each other on every entry (OBSERVED — see Section 6).
- **Validation of the registry surface**: no tests, no CI configuration, no schema, no linting or validation script exists anywhere in the repo (OBSERVED — absence confirmed by full recursive inventory).
- **A manifest**: no package metadata, so the repo's toolchain and dependencies (if any) are undeclared (OBSERVED — absence).

## 5. Improvement opportunities

- Replace the two registries with a single registry, or delete them and point to the canonical `skills/workflow-planner/references/workflow-registry.yaml` as the sole authority (DERIVED from the duplication in Section 6).
- Add a comment header to whichever registry is kept, stating its authority and refresh date (DERIVED — nothing currently marks authority).
- Add an automated check (e.g., a tiny script or CI step) that fails when any in-repo workflow registry drifts from the canonical registry (DERIVED — no validation exists today).
- Expand `README.md:1` into a two-line statement of purpose (OBSERVED gap: the README has no content).
- Add a smoke test asserting `main.py` exits 0 and prints `app` (DERIVED — no tests exist; low priority given the trivial program).

None of these are urgent blockers for the (trivial) program; they matter because the registry surface is the repo's only real content (DERIVED from Section 2).

## 6. Weakest boundary

The weakest boundary is the **repository's workflow-registry surface**: two duplicated, mutually contradictory registry files, neither grounded in or validated against the canonical registry, with no marker of authority.

**Candidate generation and scoring** (per SKILL.md "Weakest Boundary Reasoning"):

| # | Candidate (where) | evidence_strength | severity | blast_radius | goal_relevance | downstream_blocking | uncertainty |
|---|---|---|---|---|---|---|---|
| 1 | Duplicated, contradictory in-repo registries (`.workflows/registry.yaml:1-3` vs `docs/workflow-registry.yaml:1-3`) | strong | high | high | high | high | low |
| 2 | Declared-but-nonexistent workflow IDs in `docs/workflow-registry.yaml:2-3` (`arch-implementation-workflow`, `fastpath-workflow`) | strong | high | medium | high | high | low |
| 3 | Zero validation of registry content against any authority (absence of tests/CI/checks across the whole repo) | medium | medium | medium | medium | medium | medium |
| 4 | Untested trivial entry point (`main.py:1`) | strong | low | low | low | low | low |

**Selection**: candidate 2 (with candidate 1 as its structural mechanism) — the declared-but-nonexistent workflow IDs are the sharpest, most directly evidenced defect, and they are the one with a hard downstream failure mode: a router that consumes `docs/workflow-registry.yaml` emits an invalid workflow ID. Candidate 3 loses because it is absence-evidence only and its failure is softer (nothing *currently* consumes the registries in-repo); candidate 4 loses on goal relevance (the program is not the repo's substantive content). The selection is presented in the mandatory shape:

```text
Boundary: the workflow-registry surface as declared inside the repository —
          specifically docs/workflow-registry.yaml:1-3, contradicted by
          .workflows/registry.yaml:1-3, and ungrounded in the canonical
          skills/workflow-planner/references/workflow-registry.yaml.
Observed contract: the repo ships a `workflows:` registry listing `- id:`
          entries that downstream routing tooling can consume as the
          repository's workflow surface (OBSERVED — both files use the same
          structure as the canonical registry).
Observed violation or uncertainty: docs/workflow-registry.yaml:2-3 declares
          `arch-implementation-workflow` and `fastpath-workflow` — neither ID
          exists in the canonical registry (OBSERVED contrast against
          skills/workflow-planner/references/workflow-registry.yaml, which
          contains `fast-path-workflow` at line 2 and
          `architecture-implementation-workflow` at line 848, and no
          `arch-implementation-workflow` or `fastpath-workflow` anywhere).
          The two in-repo registries contradict each other on every ID
          (OBSERVED — .workflows/registry.yaml:2-3 vs
          docs/workflow-registry.yaml:2-3), and no file states which is
          authoritative (OBSERVED — neither file has metadata or comments).
Evidence:
  - docs/workflow-registry.yaml:2-3 — declares `arch-implementation-workflow`, `fastpath-workflow`
  - .workflows/registry.yaml:2-3 — declares `architecture-implementation-workflow`, `fast-path-workflow`
  - skills/workflow-planner/references/workflow-registry.yaml:2, 848 — canonical IDs (contrast)
  - README.md:1 — no statement of intent or registry authority
  - main.py:1 — trivial program, no registry consumption/validation code
Weakness type: Ghost Features
Logic trace: docs/workflow-registry.yaml:2-3 lists two workflow IDs as if they
  were available workflows. The canonical registry
  (skills/workflow-planner/references/workflow-registry.yaml) — the only
  authoritative source of workflow IDs per the repo-sensemaker skill — lists
  `fast-path-workflow` (line 2) and `architecture-implementation-workflow`
  (line 848) but contains neither `arch-implementation-workflow` nor
  `fastpath-workflow` (OBSERVED by reading the full canonical registry). So
  the docs registry documents a workflow surface that has no implementation
  in the authoritative registry: a declared surface with no reachable
  implementation — the canonical definition of Ghost Features (weakness-types.md).
  The near-miss spelling (`arch-implementation-workflow` vs
  `architecture-implementation-workflow`) makes the ghost easy to mistake for
  a real ID. The contradiction with .workflows/registry.yaml:2-3, which uses
  canonical-valid IDs, shows this is not a coherent alternative namespace but
  an uncoordinated duplicate (DERIVED — two files with identical structure
  and conflicting content, no authority marker). Because the skill forbids
  grounding routing on in-repo registries (SKILL.md, "Workflow Routing"), the
  ghosts cannot be resolved by consulting the repo itself — the boundary stays
  ambiguous and dangerous for any consumer.
Failure consequence: a router or planner that grounds on
  docs/workflow-registry.yaml:2-3 recommends a workflow ID that does not
  exist; the recommendation is rejected as a hallucinated ID (or silently
  "corrected" by guessing, e.g. to `architecture-implementation-workflow`,
  which is exactly the kind of invented substitution the registry-grounding
  rules exist to prevent). Either way, routing dead-ends or drifts from
  intent. A consumer that grounds on .workflows/registry.yaml:2-3 succeeds
  only by luck (its IDs are canonical-valid), which teaches the wrong lesson:
  that in-repo registries are trustworthy.
Confidence: high. The observation is direct (both in-repo registries and the
  canonical registry were read in full; the absent IDs are a fact, not an
  inference). What would raise it further: git history showing
  docs/workflow-registry.yaml to be a stale duplicate of the canonical file,
  or an authoritative statement from the repo owner about which registry (if
  any) is real — both UNKNOWN from the current tree.
Alternatives considered:
  - Candidate 3 (Zero Validation — no automated check anywhere that the
    registries conform to the canonical registry): real but absence-evidence;
    it is the *enabler* of the ghost surface, not the sharpest defect; it
    would be the recommended weakness type if the registries were consistent.
  - Candidate 4 (untested main.py:1): real but low goal relevance — the
    program is incidental; the registry surface is the repo's substance.
  - Vocabulary Drift (IDs in docs/ drift from canonical spelling): rejected as
    the primary label because the drift's consequence is not merely
    terminology mismatch — the drifted IDs name workflows that do not exist
    anywhere, which is the Ghost Features claim; the drift is the mechanism,
    the ghost is the defect.
  - Safety Gaps: rejected — no autonomous workflow with missing human-approval
    gates exists in this repo (nothing executable beyond `print('app')`).
```

**Weakness type:** Ghost Features

## 6.5. Problem classification (fog type)

The primary fog type is **docs_fog** (with contributing architecture_fog), classified from cited evidence, not vibes:

- **Not ui_fog**: the UI Fog Signals Registry's decision tree requires frontend/UI code first; this repo contains none (only `main.py:1`, a non-UI script). Decision tree → "NO → Not ui_fog".
- **Not product_fog**: there is no product contract to be foggy about — `README.md:1` promises nothing (OBSERVED).
- **docs_fog (primary)**: the repo's knowledge surface is stale and self-contradictory. `docs/workflow-registry.yaml:2-3` documents a workflow surface that does not exist in the canonical authority — stale/incorrect documentation of existing behavior (the ghost-feature reasoning's "documentation is stale / docs simply lag the code" case), and the two registries are literally conflicting documentation (`.workflows/registry.yaml:2-3` vs `docs/workflow-registry.yaml:2-3`). Conflicting and stale docs are the listed docs_fog signals (SKILL.md "Fog Classification"). The implementation that exists (`main.py:1`) is coherent; the incoherence lives in the documentation/configuration surface.
- **architecture_fog (secondary, contributing)**: the *mechanism* of the defect is structural — duplicated registries in two locations, no single source of truth, no authority marker, no validation wiring. This structure prevents confident routing, so architecture_fog contributes, but the primary defect is that the docs misdescribe the (canonical) workflow surface; per the ghost-feature decision rule, a mismatch that lives in the documentation is a docs_fog candidate, and the skill explicitly warns against defaulting to architecture_fog when the mismatch lives elsewhere.

## 7. Evidence

All evidence below is OBSERVED (files read in full) unless labeled otherwise.

1. `docs/workflow-registry.yaml:2-3` declares `- id: arch-implementation-workflow` and `- id: fastpath-workflow`. Neither ID appears anywhere in the canonical `skills/workflow-planner/references/workflow-registry.yaml` (read in full; canonical IDs include `fast-path-workflow` at line 2 and `architecture-implementation-workflow` at line 848). This is the ghost surface: documented workflows with no implementation in the authoritative registry.
2. `.workflows/registry.yaml:2-3` declares `- id: architecture-implementation-workflow` and `- id: fast-path-workflow` — canonical-valid IDs. The two in-repo registries therefore contradict each other on every entry (OBSERVED; DERIVED: identical structure, conflicting content).
3. `README.md:1` contains only `# multi-registry` — no intent, no statement of registry authority (OBSERVED).
4. `main.py:1` contains only `print('app')` — no code consumes, validates, or reconciles either registry, so nothing in-repo detects the conflict (OBSERVED; the *absence* of validation is DERIVED from the full inventory: no tests, no CI config, no scripts).
5. The canonical registry additionally shows a workflow whose purpose is registry-drift resolution — `docs-contract-reconciliation` (`skills/workflow-planner/references/workflow-registry.yaml:127-130`), which is the routing-relevant fact for Section 12 (OBSERVED).

**Logic trace:** The cited evidence establishes, first, that `docs/workflow-registry.yaml:2-3` declares workflow IDs that have no implementation in the only authoritative registry (evidence 1); second, that the repo simultaneously ships a second registry with different, canonical-valid IDs (evidence 2), so the ghost surface is not an isolated typo but one half of an uncoordinated duplication; third, that nothing in the repo marks either file authoritative (evidence 3) and nothing validates the surface (evidence 4), so the conflict cannot be resolved from inside the repo. Following the skill's registry-grounding rule — in-repo registries are untrusted and only the canonical registry is authoritative — the consequence is that any consumer of this repo's registry surface faces a Ghost Features trap: a documented workflow set that cannot be routed to, with the ambiguity unresolvable from the repository itself. The weakest boundary is therefore the registry surface, classified as Ghost Features, and the fog is docs_fog: the repository's documentation of its workflow surface is stale and self-contradictory while its actual implementation is coherent.

## 8. Evidence excerpts

```yaml
evidence_excerpts:
  - file: docs/workflow-registry.yaml
    lines: L1-L3
    quote: "workflows:\n  - id: arch-implementation-workflow\n  - id: fastpath-workflow"
    supports_claim: "In-repo docs registry declares workflow IDs (arch-implementation-workflow, fastpath-workflow) that do not exist in the canonical workflow registry — a declared surface with no implementation (Ghost Features)."
  - file: .workflows/registry.yaml
    lines: L1-L3
    quote: "workflows:\n  - id: architecture-implementation-workflow\n  - id: fast-path-workflow"
    supports_claim: "Second in-repo registry lists different, canonical-valid IDs, proving the two registries contradict each other and that neither can be trusted as the authoritative surface."
  - file: README.md
    lines: L1
    quote: "# multi-registry"
    supports_claim: "README is a bare title with no intent statement and no statement of which registry is authoritative."
  - file: main.py
    lines: L1
    quote: "print('app')"
    supports_claim: "The only executable artifact is trivial and neither consumes nor validates the registries; the registry surface is the repository's only substantive content."
```

## 9. Why this boundary matters

If left weak, this boundary breaks routing for anyone who uses the repository:

- A downstream `workflow-planner` step that grounds on `docs/workflow-registry.yaml:2-3` will emit `arch-implementation-workflow` or `fastpath-workflow` as the recommended workflow; the validator rejects these as hallucinated IDs (`HALLUCINATED_WORKFLOW_ID`), so the run dead-ends at the handoff.
- The near-miss spelling invites silent "correction" to `architecture-implementation-workflow` — an invented substitution that the registry-grounding rules exist to prevent, and one that can mask the underlying staleness indefinitely.
- A consumer that happens to ground on `.workflows/registry.yaml:2-3` succeeds by luck, reinforcing the false belief that in-repo registries are authoritative — the exact failure mode the skill's "never ground routing on in-repo registries" rule targets.
- Because nothing validates the surface (no tests, no CI), the conflict will persist silently until a routing failure surfaces it.

## 10. Candidate next steps

1. **Run `docs-contract-reconciliation`** (canonical workflow for resolving drift between documentation, registries, and contracts) to produce a reconciliation report for the two in-repo registries against the canonical registry.
2. **Add an automated drift check** — a small script/CI step that fails when any in-repo workflow registry ID is absent from the canonical registry (addresses the Zero Validation enabler).
3. **Collapse or delete the duplicated registries** — keep one authoritative file (or none, pointing to the canonical registry), and mark it as such in a header comment.
4. **Expand `README.md`** to state the repo's purpose and the registry authority, so the intent gap (Section 4) closes.
5. **Escalate to a human** to confirm whether this repository is a live project or a test fixture before any implementation runs — the registry surface is the repo's only content, and the fixture hypothesis (duplicated-registry corpus pattern) is plausible but UNKNOWN from the tree.

## 11. Recommended next step

Run **`docs-contract-reconciliation`** (guided execution) — it is the smallest concrete action with the highest leverage: it produces the reconciliation report that resolves the docs_fog (which registry is stale, which IDs are ghosts) without implementing anything, and its output directly feeds step 2 (the drift check). This is diagnostic-shaped work, consistent with this brief's No-Implementation boundary.

## 12. Recommended workflow

**`docs-contract-reconciliation`** (from the canonical `skills/workflow-planner/references/workflow-registry.yaml:127-159`).

- **Why this workflow**: its stated purpose is to "Resolve drift between documentation, registries, artifact contracts, templates, and validator rules" (canonical registry lines 128-130). The diagnosed defect is exactly that: in-repo registries drifting from (and conflicting with) the canonical registry.
- **Why not the closest alternatives**: `docs-implementation-workflow` (line 812) generates documentation but does not reconcile it against an authority — the repo does not need new docs, it needs conflicting ones resolved. `architecture-implementation-workflow` (line 848) would refactor structure — appropriate only if the secondary architecture_fog were primary, and heavier than the diagnosis supports. `fast-path-workflow` (line 2) auto-invokes an implementation workflow, which is premature while the registry surface is unverified. Escalation was considered and rejected: a canonical workflow fits the evidence, so escalation is not required.
- **Execution mode**: `guided_execution` — one of `docs-contract-reconciliation`'s allowed modes (canonical registry lines 137-140: `plan_only`, `prompt_chain`, `guided_execution`); it keeps human gates at each step, matching the diagnostic nature of the handoff.
- **Preconditions before it can run**: none missing — it needs only `repository_state`, which exists (the four files inspected here).
- **Routing authority note**: this recommendation is grounded exclusively in the canonical registry. The in-repo registries (`.workflows/registry.yaml`, `docs/workflow-registry.yaml`) were **not** used as routing sources; per the repo-sensemaker skill they are untrusted and stale-eligible.

## 13. Machine-readable handoff

```yaml
artifact_id: repository_sensemaking_brief
schema_version: 1
target_repo: experiments/repository-sensemaking-skill-hardening-v1/corpus/adv-multi-registry
workflow_registry_source: skills/workflow-planner/references/workflow-registry.yaml (canonical only; in-repo registries .workflows/registry.yaml and docs/workflow-registry.yaml are untrusted/stale-eligible and were not used for routing)
source_intent_ref: artifacts/01-orchestration-run/00-user-intent.md
user_implied_fog_type: unknown
primary_fog_type: docs_fog
diagnosis_conflict: false
escalation_recommended: false
escalation_required: false
evidence:
  - "docs/workflow-registry.yaml (lines 2-3): declares workflow IDs arch-implementation-workflow and fastpath-workflow that do not exist in the canonical skills/workflow-planner/references/workflow-registry.yaml (Ghost Features)"
  - ".workflows/registry.yaml (lines 2-3): duplicate registry with canonical-valid IDs (architecture-implementation-workflow, fast-path-workflow), contradicting docs/workflow-registry.yaml on every entry"
  - "README.md (line 1): bare title only; no intent and no statement of registry authority"
  - "main.py (line 1): trivial print program; no code consumes or validates the registries"
  - "skills/workflow-planner/references/workflow-registry.yaml (lines 2, 127-140, 848): canonical IDs fast-path-workflow and architecture-implementation-workflow; docs-contract-reconciliation exists for registry-drift resolution with allowed modes plan_only/prompt_chain/guided_execution"
recommended_workflow_id: docs-contract-reconciliation
recommended_execution_mode: guided_execution
weakest_boundary: Ghost Features
weakness_type: Ghost Features
weakness_type_explanation: null
required_inputs:
  - user_intent
  - repository_state
created_at: "2026-08-07T04:10:00Z"
immutable: true
timestamps:
  analyzed_at: "2026-08-07T04:10:00Z"
```

## 14. Ready-to-copy prompt

> Repo-sensemaking brief for `adv-multi-registry` (4 files: `README.md:1` title-only; `main.py:1` `print('app')`; `.workflows/registry.yaml:1-3` and `docs/workflow-registry.yaml:1-3` conflicting workflow registries). Primary fog: docs_fog (secondary architecture_fog). Weakest boundary: Ghost Features — `docs/workflow-registry.yaml:2-3` declares workflow IDs (`arch-implementation-workflow`, `fastpath-workflow`) that do not exist in the canonical `skills/workflow-planner/references/workflow-registry.yaml` (which has `fast-path-workflow` at line 2 and `architecture-implementation-workflow` at line 848); the two in-repo registries contradict each other and no file marks either authoritative; nothing in the repo validates them. Do NOT ground routing on either in-repo registry — the canonical registry is the only authority. Recommended workflow: `docs-contract-reconciliation` in `guided_execution` mode (allowed: plan_only, prompt_chain, guided_execution) to produce a registry-drift reconciliation report; do not auto-invoke any implementation workflow until the reconciliation confirms which registry (if any) is real. Precondition to verify first: confirm with a human whether this repository is a live project or a test fixture.
