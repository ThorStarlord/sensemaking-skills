# 00 — DETAILED_REPOSITORY_ARCHITECTURE_PROTOTYPE_V0 — Scope

**Prototype id:** `DETAILED_REPOSITORY_ARCHITECTURE_PROTOTYPE_V0`
**Aliases accepted:** `RICH_REPOSITORY_REPRESENTATION_PROTOTYPE_V0`
**Explicitly NOT:** `FULL`, PHB `FULL`, a production feature, Goal A evidence,
Issue #218 normal-use evidence, Issue #226, a canonical schema, an ADR.

## Starting state (Section 5 guard)

| Fact | Value |
|---|---|
| Authorization canonical SHA | `8bae09b8a81f60d9786d60795cc4e36653dc292a` |
| `main` at construction start | `ba8968ca1a12caa90ce7beb0ee5fd2dfac055f37` |
| `main` moved? | Yes — 6 commits ahead |
| Intervening commits | `33530fd` `8cd6af4` `b1edd9c` `2d9d1a4` (merge #242) `5921943` `ba8968c` |
| Nature of intervening changes | PHB Hypothesis B bounded-experiment evidence (`artifacts/hypotheses-conditional-representation.md`, `artifacts/pr-242-close-note-33530fd.md`), FULL spike scripts under `experiments/product-hypothesis-b/`, a research-agenda meta-finding paragraph, one `.github/workflows/validation.yml` addition. **No change to PHB machinery, `representation_sufficiency`, MODEL_WARRANT mapping, runtime gating, artifact contracts, ADRs, registries, or canonical product behavior.** |
| Compatibility decision | Compatible. V0 is constructed against latest canonical `ba8968c`. The new PHB spike evidence is *represented* in `07-RESEARCH-CLAIM-MAP.md`, not depended upon. |
| Prototype branch | `research/detailed-repository-architecture-prototype-v0` (worktree `H:/GithubRepositories/smk-dra-v0`, branched from `ba8968c`) |
| Prototype root | `experiments/detailed-repository-architecture-v0/` |

Canonical history was **not** reset or force-moved to preserve the authorization SHA.

## What this prototype is

An intentionally rich, evidence-backed, file-based (Markdown + YAML) representation
of how `sensemaking-skills` actually works — its components, responsibilities,
artifacts, authorities, validation surfaces, product capabilities, lifecycle
states, research claims, and above all the **consequential semantic relationships
between them**.

It is *architecture development by construction*: the competing "rich explicit
architecture" is built so its value (or lack of value) becomes observable,
instead of being endlessly gated behind a representation-sufficiency judgment.

## Research-order inversion (Section 4)

For this task only, the order is:

```
BUILD rich representation
  -> observe what creates decision value
  -> identify structure that only restates cheaply-recoverable facts
  -> compress
  -> THEN reconsider when representation should be materialized
```

Not: representation-sufficiency gate -> MODEL_WARRANT -> wait. This prototype is
*upstream* of that gate and does not modify it.

## Primary questions (from authorization Section 3)

- **A.** Does explicit rich representation create meaningful decision value?
- **B.** Which representation elements create that value?
- **C.** Which elements merely restate cheaply-recoverable repository facts?
- **D.** Which important relationships are hard to recover without explicit representation?
- **E.** Does rich architecture expose authority conflicts / contract mismatches /
  stale claims / hidden dependency boundaries / cross-component impact more directly?
- **F.** What representation is valuable enough to be persistent?
- **G.** What representation is useful only as an on-demand projection?
- **H.** Likely architecture direction: `ALWAYS_RICH` / `CONDITIONAL_RICH` /
  `THIN_PERSISTENT_CORE_PLUS_ON_DEMAND_DETAIL` / `NO_DEDICATED_RICH_REPRESENTATION`
  — **not decided in advance.**

## Artifact surface

| File | Contents |
|---|---|
| `00-PROTOTYPE-SCOPE.md` | this file |
| `01-SYSTEM-OVERVIEW.md` | prose+diagram orientation: what the system is, the real end-to-end flow |
| `02-COMPONENTS.yaml` | component register with id, kind, path, responsibility, explicit non-ownership, lifecycle |
| `03-RELATIONSHIPS.yaml` | typed relationship edges between components/artifacts/authorities, each evidence-backed and epistemically graded |
| `04-ARTIFACT-FLOWS.md` | producer→consumer→validator→transformer chains per durable artifact |
| `05-AUTHORITY-MAP.md` | who defines / enforces / owns runtime identity / wins on conflict, per consequential fact |
| `06-VALIDATION-MAP.md` | which validator/suite protects which contract; declared-but-unenforced; multiply-enforced |
| `07-RESEARCH-CLAIM-MAP.md` | claim-oriented view of research threads: question, evidence class, bounded result, claim ceiling, live status, supersession |
| `08-OPEN-WORK-MAP.md` | open work only where it intersects architectural ownership / unresolved decisions |
| `09-DECISION-VIEWS.md` | prospective architecture questions answered against V0 (filled after freeze) |
| `EVIDENCE-INDEX.yaml` | every load-bearing evidence pointer used, keyed by evidence id |
| `OBSERVATIONS.md` | running log of construction friction + representation-value observations (mutable AFTER freeze; the frozen files are not) |
| `V0-FREEZE-MANIFEST.md` | SHA-256 of every V0 artifact + target repo SHA + freeze declaration |
| `10-PHASE-1-STOP-CHECK.md` | qualitative inventory (counts, friction, redundancy) — no quality score |
| `11-RETROSPECTIVE-CHALLENGES.md` | 5–8 historically consequential episodes replayed against frozen V0 |
| `12-SYNTHESIS.md` | the 10 synthesis answers + architecture-direction disposition |

Filenames are scaffolding, not a frozen product schema.

## Hard boundaries (authorization Sections 22–25, 28–29)

- No graph DB / server / vector DB / embeddings / daemon / watcher / auto-invalidation /
  incremental sync / repo hook / GitHub App / persistence service / web UI / query engine /
  ontology framework / new runtime / "Sensemaking Core" / domain-pack infra.
- No change to `representation_sufficiency`, MODEL_WARRANT mapping, NO/PARTIAL/INCONCLUSIVE
  semantics, Section 13 contract, runtime gating, FULL semantics, warrant validators.
- `GOAL_A_MODIFIED = false`, `GOAL_A_EVIDENCE = false`, `ISSUE_218_MODIFIED = false`,
  `ISSUE_218_EVIDENCE = false`, `ISSUE_226_EXECUTED = false`.
- No new EXP-00xx campaign, no new runner framework, no multi-model replication campaign.
- No merge to `main`. Draft PR only, clearly labelled `ARCHITECTURE PROTOTYPE — NOT PRODUCT ARCHITECTURE`.
- Canonical product documentation is not edited to imply V0 adoption.

## Epistemic grading (used throughout 02/03/05/07)

| Grade | Meaning |
|---|---|
| `DEMONSTRATED` | directly established by durable repository evidence (file+line, ADR section, registry entry, test, implementation) |
| `DERIVED` | follows from two or more `DEMONSTRATED` facts |
| `INTERPRETIVE` | architectural interpretation that remains contestable |
| `HYPOTHESIS` | plausible but unresolved |

These are never flattened to equal confidence.
