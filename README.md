# Sensemaking Skills

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

An agent-native engineering sensemaking and control layer for software-engineering agents. It turns repository uncertainty into durable evidence, explicit decisions, and reconstructible next-action context without replacing the active agent's semantic judgment.

**Version:** 0.3.0  
**Status:** Beta; Outer Loop v0 operational baseline  
**Python:** 3.11+  
**Core runtime:** local-first; no server or cloud dependency

## How to use Sensemaking

Choose the entry point for your role instead of reading every document:

| If you are... | Start here | What it owns |
| --- | --- | --- |
| A human/new user trying to use Sensemaking | [`GETTING_STARTED.md`](GETTING_STARTED.md) | Canonical human how-to and first-use walkthrough |
| Looking for the canonical Campaign lifecycle/composition | [`docs/agent-workflow-golden-path-v1.md`](docs/agent-workflow-golden-path-v1.md) | Canonical workflow-composition reference; static guidance, not routing |
| A coding agent using Sensemaking | [`skills/using-sensemaking/SKILL.md`](skills/using-sensemaking/SKILL.md) | Agent-facing operating instructions |
| Trying to understand the deeper responsibility/authority model | [`docs/agent-native-operating-workflow.md`](docs/agent-native-operating-workflow.md) | Level-2 reasoning, artifact, authority, validation, and stopping model |
| Maintaining, validating, or qualifying the repository | [`docs/operations-runbook.md`](docs/operations-runbook.md) | Current operator/qualification runbook |

```text
GETTING_STARTED.md = how to use
agent-workflow-golden-path-v1.md = how surfaces compose
using-sensemaking/SKILL.md = how the coding agent operates
agent-native-operating-workflow.md = why the Level-2 loop works this way
operations-runbook.md = how maintainers operate and qualify it
```

Do not create a parallel `HOW_TO_USE.md` or generic `workflow.md` for the same material. The goal is one clear entry point per audience rather than duplicated instruction surfaces.

## Control architecture

Sensemaking now distinguishes four scopes of reasoning and durable state:

```text
LEVEL 4 — PRODUCT THESIS / STRATEGY REVISION
What product should this be, for whom, and why?
                    |
                    v
LEVEL 3 — STRATEGIC REPOSITORY EVOLUTION
What should change in the product/repository next?
                    |
                    v
LEVEL 2 — RESPONSIBILITY / CAMPAIGN
What bounded responsibility resolves the selected decision?
                    |
                    v
LEVEL 1 — EXECUTION
What concrete steps correctly perform the bounded work?
```

These are **reasoning/control scopes, not four runtime engines**. The active coding agent owns semantic judgment. Deterministic machinery owns only mechanically decidable representation, validation, provenance, persistence, integrity, identity, bounded conformance, and reconstruction.

The governing rule is:

> **Lower levels may execute decisions delegated from higher levels, but they may not silently redefine commitments owned by the higher level.**

The current authority surfaces are:

- `docs/product-strategy.md` — Level-4 product thesis and strategic authority;
- `STATUS.md` — Level-3 Strategic Repository Evolution state;
- `docs/strategic-outer-loop.md` — canonical four-level control model;
- `docs/strategic-state-contract.md` — Level-3 durable strategic-state contract;
- `docs/product-thesis-revision.md` — Level-4 revision and owner-ratification contract;
- `docs/sensemaking-campaign.md` — canonical Level-2 Campaign model;
- ordinary branch/task/test state — Level-1 execution evidence.

The Strategic Frontier is decision-relevant possibility state, **not a backlog**. Selecting a strategic boundary does not automatically authorize implementation. Level 3 may escalate a thesis-level contradiction to Level 4, but it does not silently rewrite the product thesis.

**Outer Loop v0 is now the frozen operational baseline.** Future outer-loop machinery is reopened only by concrete repository/product pressure or explicit owner direction; the existence of conceptual later steps is not a standing implementation roadmap.

## What v0.3 ships

The installed v0.3 package primarily supplies the **Level-2/Level-1 durable and mechanical substrate** used by the active agent. Its core durable abstraction is a **Sensemaking Campaign**: a bounded engineering decision process that survives agent/session boundaries.

The installed product includes:

- typed file-backed Campaign state and append-only history;
- validated artifact admission with exact byte/provenance binding;
- explicit agent-authored `advance`, `defer`, and `close` decisions;
- deterministic, unranked capability inspection;
- integrity-bound handoff/resume;
- evidence lineage and reconciliation reconstruction;
- durable target repository snapshot binding with drift detection;
- explicit harness setup adapters for generic Agent Skills, Claude Code, Codex, and OpenCode;
- Campaign schema v2 with deterministic v1 -> v2 representation migration;
- a build-derived canonical validator runtime;
- a deterministic real-harness evidence verifier for frozen external qualification attempts;
- a bounded mechanical Semantic Architecture substrate for repository observations;
- Campaign observability projections, Resume Capsule, replay/provenance graph, and portable integrity bundles;
- B7 semantic-reference resolution/audit over existing Campaign evidence/admission identities, rendered through `campaign semantic-state` and `campaign explain`.

The Level-3/Level-4 Strategic Outer Loop foundation is currently a **repository documentation/authority architecture**, not a shipped autonomous strategic runtime. Installing the package does not create a `StrategicPlanner`, automatically rank the Strategic Frontier, revise product strategy, or generate Campaigns without agent judgment.

The shipped wheel deliberately excludes retained research-lab packages (`campaign_validation`, `campaign_accounting`, `exploratory_authorization`, `exploratory_execution`). Those remain source-only repository/lab infrastructure.

## Product boundary

The active coding agent owns semantic control:

- What responsibility is warranted?
- Which capability, if any, should be selected?
- Is execution authorized?
- What does evidence mean?
- Should the Campaign advance, defer, or close?
- At Level 3, which strategic boundary, if any, is worth selecting next?
- Does new evidence require Level-4 thesis review rather than ordinary repository work?

Deterministic machinery owns mechanically decidable contracts:

- persistence and reconstruction;
- artifact validation/admission;
- provenance and exact-byte identity;
- target repository snapshot identity and drift detection;
- capability metadata/availability representation;
- bounded repository observations with declared scope/completeness/currentness;
- path containment and integrity checks;
- schema representation migration;
- handoff binding;
- manifest/domain cross-reference conformance;
- Campaign provenance projections and portable-bundle integrity;
- reference-resolution integrity under existing authoritative namespaces;
- release/evidence-package verification.

The durable invariants include:

```text
warranted responsibility != available capability != authorized capability
validator passed != semantic truth
admitted evidence != warranted conclusion
lineage != semantic warrant
handoff != semantic recommendation
Skill copied to discovery root != harness observed or invoked Skill
verifier PASS != semantic truth
semantic profile valid != reasoning semantically correct
semantic map relation != architecture judgment
manifest valid != Skill should run
bundle valid != Campaign semantically correct
repository changed != repair succeeded
reference occurrence != reference resolution
reference resolved != current
reference audit pass != semantic truth
not_addressable != invalid
product thesis != strategic state
Strategic Frontier != backlog
strategic boundary selected != implementation authorized
Level-3 state != Level-4 strategy authority
```

## Installation

```bash
python -m pip install sensemaking-skills==0.3.0
sensemaking-skills --version
```

For source development:

```bash
git clone https://github.com/ThorStarlord/sensemaking-skills.git
cd sensemaking-skills
python -m venv .venv
# activate the environment
python -m pip install -e .
```

## Campaign quick start

A Campaign workspace should live outside the target repository. Pass `--target-repo` when you want durable repository identity and working-tree provenance:

```bash
sensemaking-skills campaign init \
  --workspace /path/to/campaigns/CMP-0001 \
  --campaign-id CMP-0001 \
  --mission "understand and repair the repository boundary" \
  --target-repo /path/to/target-repository

sensemaking-skills campaign status --workspace /path/to/campaigns/CMP-0001
sensemaking-skills campaign validate --workspace /path/to/campaigns/CMP-0001
```

Target inspection is mechanical only. Initialization records repository identity, Git HEAD/tree, and a deterministic worktree digest; it does not infer uncertainty, responsibility, capability selection, or authority.

### Admit a validated artifact

```bash
sensemaking-skills campaign ingest \
  --workspace /path/to/campaigns/CMP-0001 \
  --artifact /path/to/repository_sensemaking_brief.md
```

The installed package carries the canonical validator runtime. `--framework-root` remains an explicit development/compatibility override and fails closed if invalid.

### Record an explicit agent decision

```bash
sensemaking-skills campaign advance --help
sensemaking-skills campaign defer --help
sensemaking-skills campaign close --help
```

These commands persist an agent-authored semantic decision. They do not infer the decision from validator output or repository drift.

### Inspect lineage and reconciliation

```bash
sensemaking-skills campaign lineage --workspace /path/to/campaigns/CMP-0001
sensemaking-skills campaign history --workspace /path/to/campaigns/CMP-0001
sensemaking-skills campaign reconciliation --workspace /path/to/campaigns/CMP-0001
```

Target/evidence lineage records provenance; it does not prove a repository change was correct.

## Campaign observability and fresh-context reconstruction

The additive observability surface projects existing Campaign v2 state without becoming a semantic router:

```bash
sensemaking-skills campaign inspect --workspace /path/to/campaigns/CMP-0001
sensemaking-skills campaign explain --workspace /path/to/campaigns/CMP-0001 --ref T1
sensemaking-skills campaign diff --workspace /path/to/campaigns/CMP-0001 --from-transition T1 --to-transition T2
sensemaking-skills campaign resume-context --workspace /path/to/campaigns/CMP-0001
sensemaking-skills campaign replay --workspace /path/to/campaigns/CMP-0001 --at-transition T1
sensemaking-skills campaign graph --workspace /path/to/campaigns/CMP-0001 --format mermaid
```

`resume-context` is a deterministic **Resume Capsule**. It reconstructs durable declared state and optional companion references; it does not emit a recommended next action.

Replay is intentionally bounded by Campaign schema v2: it reconstructs transition prefixes and recorded evidence, not historical full-state snapshots that were never stored.

## Optional cross-Skill semantic companion

A Campaign can carry an append-only semantic-reference companion without changing Campaign schema v2:

```bash
sensemaking-skills campaign semantic-state-append \
  --workspace /path/to/campaigns/CMP-0001 \
  --entry-id S1 \
  --source-skill repo-sensemaker \
  --artifact-ref repository_sensemaking_brief.md \
  --claim-ref C1

sensemaking-skills campaign semantic-state --workspace /path/to/campaigns/CMP-0001
```

Repository-bound Campaigns derive the companion target identity from the current TargetSnapshot digest. Targetless Campaigns require an explicit `--target-ref`.

The companion carries artifact/evidence/claim/uncertainty provenance references, not hidden chain of thought. Its hash chain can establish structural integrity, not semantic truth.

B7 adds a separate outbound reference audit. `campaign semantic-state` reports chain diagnostics plus reference-audit totals/details, while `campaign explain --ref` can render the audit result for matching semantic-companion references. Existing Campaign evidence/admission authority is reused rather than duplicated.

The audit distinguishes `resolved`, `dangling`, `ambiguous`, and `not_addressable`, and keeps addressability separate from semantic meaning. Opaque legacy/claim/profile references remain informational when no authoritative resolver exists.

```text
not_addressable != invalid
resolved != current
reference resolution != semantic support
```

B7 does not change Resume Capsule behavior or Campaign schema v2.

Phase 10 separately retained `semantic_reasoning_profile` as an **optional** companion audit/reconstruction artifact; the profile is not mandatory and is not promoted into Campaign artifact admission.

## Mechanical Semantic Architecture CLI

The installed package provides mechanically bounded repository probes:

```bash
sensemaking-skills semantic probe \
  --repo /path/to/repo \
  --target-ref sha:abc123 \
  --kind python-imports \
  --output /tmp/imports.json

sensemaking-skills semantic probe \
  --repo /path/to/repo \
  --target-ref sha:abc123 \
  --kind manifest-dependencies \
  --output /tmp/dependencies.json

sensemaking-skills semantic probe \
  --repo /path/to/repo \
  --target-ref sha:abc123 \
  --kind exact-search \
  --pattern "needle" \
  --output /tmp/search.json
```

Current v0 probe families are regular-file containment, Python import syntax, supported manifest dependency declarations, and exact UTF-8 literal search.

Probe observations preserve source/method, target ref, scope, completeness, currentness, and evidence refs. They do not turn imports into architecture violations, dependency declarations into runtime-use claims, or zero exact matches into universal absence.

### Bounded Repository Semantic Map

One or more probe outputs can be combined without inventing architecture:

```bash
sensemaking-skills semantic map-build \
  --map-id MAP-1 \
  --target-ref sha:abc123 \
  --observations /tmp/imports.json \
  --observations /tmp/dependencies.json \
  --output /tmp/semantic-map.json
```

The v0 map uses generic repository locators and `DERIVED` mechanical relations. It rejects mixed target refs and explicitly remains incomplete.

## Skill Contract Manifests and Domain Packs

Repository-owned `skill-manifests/` make a Skill's deterministic shell machine-readable: identity, domain, declared responsibilities, canonical inputs/outputs, shared semantic concepts, and repository mutation declaration.

`domain-packs/` currently provides reference manifests for a bounded Engineering slice and the completed Product Management migration.

Conformance can be checked with:

```bash
sensemaking-skills semantic conformance \
  --manifests-dir skill-manifests \
  --domain-packs-dir domain-packs \
  --repo-root .
```

Conformance rejects missing Skill files, duplicate IDs/list values, unknown canonical semantic concepts, pack/manifest mismatches, and fields that would imply semantic truth/routing authority.

A valid manifest does not mean the Skill is warranted for the current task.

## Portable Campaign bundles

Campaign workspaces can be exported as exact-byte integrity bundles:

```bash
sensemaking-skills campaign bundle-export \
  --workspace /path/to/campaigns/CMP-0001 \
  --output /path/outside/workspace/CMP-0001.zip

sensemaking-skills campaign bundle-verify --bundle /path/CMP-0001.zip
sensemaking-skills campaign bundle-import --bundle /path/CMP-0001.zip --workspace /new/path/CMP-0001
```

Bundles contain exact workspace bytes plus a deterministic SHA-256/size manifest. Verification rejects unsafe paths, symlinks, duplicate/undeclared/missing files, digest/size mismatch, and unsupported format/version. Export destinations inside the source workspace are rejected.

Bundle integrity does not establish semantic Campaign correctness or prove the original target repository remains available.

## Handoff and resume

```bash
sensemaking-skills campaign handoff --workspace /path/to/campaigns/CMP-0001
sensemaking-skills campaign resume --workspace /path/to/campaigns/CMP-0001
```

A handoff reconstructs durable context; it does not recommend the next semantic action. Target-bound fresh-context resume verifies that the live target repository still matches the durable current snapshot.

## Make Skills discoverable to coding-agent harnesses

Harness selection is explicit; Sensemaking Skills does not auto-detect the running agent.

```bash
sensemaking-skills setup-skills --target generic --scope user
sensemaking-skills setup-skills --target claude --scope user
sensemaking-skills setup-skills --target codex --scope user
sensemaking-skills setup-skills --target opencode --scope user
sensemaking-skills setup-skills --target claude --scope project --project-root /path/to/repo
```

Setup preserves drift protection. Copying a Skill into a discovery root is not evidence that a harness observed or natively invoked it.

## Campaign schema compatibility

Current Campaign artifacts use **schema version 2**. Historical v1 artifacts are accepted only through deterministic one-way representation migration. Migration does not reinterpret evidence, select work, or grant authority.

The optional semantic companion and B7 audit remain workspace-level/additive behavior and do not introduce Campaign schema v3.

## Semantic Architecture development policy

Phase 10 already ran a bounded real-repository common-envelope experiment and retained `semantic_reasoning_profile` as an optional companion (**Outcome A**).

The subsequent owner-authorized policy is build-first: additional empirical experiments may be deferred while a concrete missing capability has a clear mechanical contract. Mechanical verification remains continuous.

The **Construction Diminishing-Returns Gate** stops further speculative construction when architecture can no longer resolve competing designs, formalization outpaces consumption, maintenance dominates capability growth, or the decisive question becomes behavioral value rather than mechanical correctness.

The Strategic Outer Loop uses the same discipline: higher-scope concepts should first be carried by existing authority surfaces, and new deterministic machinery must not be added merely to mirror the conceptual model.

See `docs/semantic-architecture/README.md`, `docs/semantic-architecture/implementation-plan.md`, `docs/semantic-architecture/build-first-policy.md`, and `docs/semantic-architecture/b7-semantic-reference-audit-design-preflight.md`.

## Real-harness qualification

The package includes `sensemaking_skills.external_qualification`, the **real-harness qualification verifier** for frozen evidence packages from actual coding-agent harness runs. A synthetic fixture can prove the verifier contract but cannot manufacture real-harness origin evidence.

Repository, semantic, PM, and installed-wheel qualification do not substitute for required native-harness/portability evidence when a stronger support claim depends on it.

## Release qualification

v0.3 release candidates are qualified on the exact PR head by three complementary authority lanes:

1. **Product Validation** — Python 3.11/3.12 Campaign product, installed wheel, repository contracts, and filesystem security.
2. **Lab Validation** — retained source-only research/lab suites, separate from shipped-product authority.
3. **Release Candidate Distribution** — wheel + sdist build, exact artifact/install assertions, installed validator runtime, and candidate digests.

Tagged publication remains a separate owner action.

## What this is not

- Not a centralized semantic router.
- Not an autonomous project manager.
- Not an `OuterLoopEngine` or deterministic `StrategicPlanner`.
- Not an automatic Strategic Frontier ranking system.
- Not an automatic product-thesis revision mechanism.
- Not a universal planner or capability-ranking engine.
- Not a universal semantic-reference registry.
- Not a semantic truth validator.
- Not a currentness inference engine.
- Not a complete repository knowledge graph.
- Not a cloud service.
- Not automatic external mutation authority.
- Not a claim that copied Skills were observed or invoked by a harness.
- Not a mechanism for silently rebinding an existing Campaign to a different target repository.

## Repository structure

```text
src/sensemaking_skills/
  campaign_semantics/       typed Campaign contracts + schema evolution
  campaigns/                durable workspace/service/admission/lineage/target snapshots/bundles
  semantic_architecture/    bounded probes/map/state/reference-audit/conformance substrate
  semantic_cli.py           mechanical semantic CLI registration
  campaign_observability_cli.py Campaign projections/companion/reference audit/portability
  external_qualification.py frozen real-harness evidence verifier
  skill_trees/              build-derived installed Skill trees
  validator_runtime/        build-derived installed validator runtime
skills/                     canonical agent-native Skill sources
skill-manifests/            repository-owned deterministic Skill interface manifests
domain-packs/               repository-owned domain reference manifests
scripts/                    canonical validation/probe tooling
tests/                      product, installed-wheel, integration, and retained-lab tests
docs/                       canonical product, strategic, semantic architecture, release, and runbook docs
experiments/                retained research evidence/lab material
```

## Canonical documentation

Read the repository from higher-scope authority into bounded execution. For ordinary usage, start with the audience map near the top of this README rather than reading this entire authority list.

- `GETTING_STARTED.md` — canonical human how-to-use entry point and first-use walkthrough.
- `skills/using-sensemaking/SKILL.md` — canonical agent-facing usage instructions.
- `docs/agent-workflow-golden-path-v1.md` — canonical workflow-composition reference; static guidance only.
- `docs/product-strategy.md` — Level-4 product thesis, boundary, hypotheses, and strategic authority.
- `STATUS.md` — current Level-3 Strategic Repository Evolution state and cross-program status.
- `docs/strategic-outer-loop.md` — canonical four-level control model and Level-3/Level-4 relationship.
- `docs/strategic-state-contract.md` — Level-3 durable strategic-state contract.
- `docs/product-thesis-revision.md` — Level-4 strategy revision and owner-ratification contract.
- `docs/product-operating-model.md` — value stream, responsibility ownership, governance, delegation, and escalation.
- `docs/agent-native-operating-workflow.md` — Level-2 agent-native responsibility/Campaign operating map.
- `docs/operations-runbook.md` — current operator-facing operations and qualification runbook; checked-in workflows remain executable authority.
- `docs/sensemaking-campaign.md` — canonical Campaign product model.
- `docs/campaign-target-snapshot.md` — target provenance and drift contract.
- `docs/campaign-observability-and-portability.md` — observability, semantic companion, B7 reference audit, Resume Capsule, replay/graph, and bundles.
- `docs/semantic-architecture/README.md` — Semantic Architecture index; orthogonal semantic/layer view.
- `docs/semantic-architecture/implementation-plan.md` — build-first semantic roadmap.
- `docs/semantic-architecture/build-first-policy.md` — diminishing-returns gate.
- `docs/semantic-architecture/build-first-handoff.md` — B1–B7 exact-head qualification handoff.
- `docs/semantic-architecture/b7-semantic-reference-audit-design-preflight.md` — B7 design authority and resolver/abort contract.
- `docs/semantic-architecture/mechanical-semantic-substrate.md` — probes/map/state contracts.
- `docs/semantic-architecture/skill-contract-manifests-and-domain-packs.md` — manifest/domain conformance.
- `docs/product-management/capability-migration-matrix.md` — completed PM capability migration/maturity ledger.
- `docs/product-management/qualification-levels.md` — PM qualification policy.
- `docs/product-lab-boundary.md` — shipped product vs retained lab boundary.
- `docs/external-golden-path-verifier.md` — real-harness evidence verification protocol.
- `docs/strategic-repository-evolution-audit-2026-09-11.md` — current Level-3 repository-wide audit and Outer Loop v0 freeze decision.

Historical milestone runbooks are retained for reconstruction only and are not current operational authorities.

## Development

For the current locally reproducible Product Validation, Lab Validation, release-candidate, repository-contract, installed-wheel, filesystem-security, Campaign, and strategic-state commands, use `docs/operations-runbook.md`. The checked-in workflows remain executable CI authority:

```text
.github/workflows/validation.yml
.github/workflows/lab-validation.yml
.github/workflows/release-candidate.yml
.github/workflows/publish.yml
```

The release version is declared only in `pyproject.toml`; `sensemaking_skills.__version__` derives it from installed distribution metadata.

License: MIT.
