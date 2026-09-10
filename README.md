# Sensemaking Skills

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

An agent-native engineering sensemaking and control layer for software-engineering agents. It turns repository uncertainty into durable evidence, explicit decisions, and reconstructible next-action context without replacing the active agent's semantic judgment.

**Version:** 0.3.0  
**Status:** Beta; post-milestone v0.3 baseline  
**Python:** 3.11+  
**Core runtime:** local-first; no server or cloud dependency

## What v0.3 ships

The core abstraction is a **Sensemaking Campaign**: a durable engineering decision process that survives agent/session boundaries.

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
- Campaign observability projections, Resume Capsule, replay/provenance graph, and portable integrity bundles.

The shipped wheel deliberately excludes retained research-lab packages (`campaign_validation`, `campaign_accounting`, `exploratory_authorization`, `exploratory_execution`). Those remain source-only repository/lab infrastructure.

## Product boundary

The active coding agent owns semantic control:

- What responsibility is warranted?
- Which capability, if any, should be selected?
- Is execution authorized?
- What does evidence mean?
- Should the Campaign advance, defer, or close?

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

The optional semantic companion is a workspace-level additive artifact and does not introduce Campaign schema v3.

## Semantic Architecture development policy

Phase 10 already ran a bounded real-repository common-envelope experiment and retained `semantic_reasoning_profile` as an optional companion (**Outcome A**).

The subsequent owner-authorized policy is build-first: additional empirical experiments may be deferred while a concrete missing capability has a clear mechanical contract. Mechanical verification remains continuous.

The **Construction Diminishing-Returns Gate** stops further speculative construction when architecture can no longer resolve competing designs, formalization outpaces consumption, maintenance dominates capability growth, or the decisive question becomes behavioral value rather than mechanical correctness.

See `docs/semantic-architecture/README.md`, `docs/semantic-architecture/implementation-plan.md`, and `docs/semantic-architecture/build-first-policy.md`.

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
- Not a universal planner or capability-ranking engine.
- Not a semantic truth validator.
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
  semantic_architecture/    bounded probes/map/state/conformance substrate
  semantic_cli.py           mechanical semantic CLI registration
  campaign_observability_cli.py Campaign projections/companion/portability
  external_qualification.py frozen real-harness evidence verifier
  skill_trees/              build-derived installed Skill trees
  validator_runtime/        build-derived installed validator runtime
skills/                     canonical agent-native Skill sources
skill-manifests/            repository-owned deterministic Skill interface manifests
domain-packs/               repository-owned domain reference manifests
scripts/                    canonical validation/probe tooling
tests/                      product, installed-wheel, integration, and retained-lab tests
docs/                       canonical product, semantic architecture, release, and runbook docs
experiments/                retained research evidence/lab material
```

## Canonical documentation

- `STATUS.md` — current release/product state.
- `docs/milestone-runbook.md` — operating and qualification runbook.
- `docs/sensemaking-campaign.md` — canonical Campaign product model.
- `docs/campaign-target-snapshot.md` — target provenance and drift contract.
- `docs/campaign-observability-and-portability.md` — observability, semantic companion, Resume Capsule, replay/graph, and bundles.
- `docs/semantic-architecture/README.md` — Semantic Architecture index.
- `docs/semantic-architecture/implementation-plan.md` — build-first semantic roadmap.
- `docs/semantic-architecture/build-first-policy.md` — diminishing-returns gate.
- `docs/semantic-architecture/mechanical-semantic-substrate.md` — probes/map/state contracts.
- `docs/semantic-architecture/skill-contract-manifests-and-domain-packs.md` — manifest/domain conformance.
- `docs/product-management/capability-migration-matrix.md` — completed PM capability migration/maturity ledger.
- `docs/product-management/qualification-levels.md` — PM qualification policy.
- `docs/product-lab-boundary.md` — shipped product vs retained lab boundary.
- `docs/external-golden-path-verifier.md` — real-harness evidence verification protocol.

## Development

For locally reproducible Product Validation, Lab Validation, release-candidate, repository-probe, installed-wheel, and filesystem-security commands, use `docs/milestone-runbook.md`. The checked-in workflows remain executable CI authority:

```text
.github/workflows/validation.yml
.github/workflows/lab-validation.yml
.github/workflows/release-candidate.yml
.github/workflows/publish.yml
```

The release version is declared only in `pyproject.toml`; `sensemaking_skills.__version__` derives it from installed distribution metadata.

License: MIT.
