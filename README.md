# Sensemaking Skills

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

An agent-native engineering sensemaking and control layer for software-engineering agents. It turns repository uncertainty into durable evidence, explicit decisions, and reconstructible next-action context without replacing the active agent's semantic judgment.

**Version:** 0.3.0  
**Status:** Beta; v0.3 release baseline  
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
- explicit harness setup adapters for generic Agent Skills, Claude Code, Codex, and OpenCode;
- Campaign schema v2 with deterministic v1 -> v2 representation migration;
- a build-derived canonical validator runtime so `campaign ingest` works from the installed distribution;
- a deterministic real-harness evidence verifier for frozen external qualification attempts.

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
- capability metadata/availability representation;
- path containment and integrity checks;
- schema representation migration;
- handoff binding;
- release/evidence-package verification.

The durable invariants are:

```text
warranted responsibility != available capability != authorized capability
validator passed != semantic truth
admitted evidence != warranted conclusion
lineage != semantic warrant
handoff != semantic recommendation
Skill copied to discovery root != harness observed or invoked Skill
verifier PASS != semantic truth
```

## Installation

```bash
python -m pip install sensemaking-skills==0.3.0
sensemaking-skills --version
```

Expected:

```text
0.3.0
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

```bash
sensemaking-skills campaign init \
  --workspace /path/to/CMP-0001 \
  --campaign-id CMP-0001 \
  --mission "understand and repair the repository boundary"

sensemaking-skills campaign status --workspace /path/to/CMP-0001
sensemaking-skills campaign capabilities --workspace /path/to/CMP-0001 --responsibility architectural_review
```

### Admit a validated artifact

The installed package carries the canonical validator runtime, so `--framework-root` is no longer required for normal installed use:

```bash
sensemaking-skills campaign ingest \
  --workspace /path/to/CMP-0001 \
  --artifact /path/to/repository_sensemaking_brief.md
```

`--framework-root` remains an explicit development/compatibility override. If supplied, a bad override fails closed rather than silently falling back to the packaged runtime.

### Record an explicit agent decision

```bash
sensemaking-skills campaign advance --help
sensemaking-skills campaign defer --help
sensemaking-skills campaign close --help
```

These commands persist an agent-authored semantic decision. They do not infer the decision from validator output.

### Inspect lineage and reconciliation

```bash
sensemaking-skills campaign lineage --workspace /path/to/CMP-0001
sensemaking-skills campaign reconciliation --workspace /path/to/CMP-0001
```

### Handoff and resume

```bash
sensemaking-skills campaign handoff --workspace /path/to/CMP-0001
sensemaking-skills campaign resume --workspace /path/to/CMP-0001
```

A handoff reconstructs durable context; it does not recommend the next semantic action.

## Make Skills discoverable to coding-agent harnesses

Harness selection is explicit; Sensemaking Skills does not auto-detect the running agent.

```bash
# user scope
sensemaking-skills setup-skills --target generic --scope user
sensemaking-skills setup-skills --target claude --scope user
sensemaking-skills setup-skills --target codex --scope user
sensemaking-skills setup-skills --target opencode --scope user

# project scope
sensemaking-skills setup-skills --target claude --scope project --project-root /path/to/repo
```

Setup preserves drift protection: missing trees are copied, matching trees are left alone, divergent trees are reported and preserved unless `--force` is explicit.

## Campaign schema compatibility

Current Campaign artifacts use **schema version 2**. Historical v1 artifacts are accepted only through deterministic one-way representation migration. Migration does not reinterpret evidence, select work, or grant authority, and append-only historical transition bytes are not rewritten merely to modernize serialization.

See `docs/campaign-schema-evolution.md`.

## Real-harness qualification

The package includes `sensemaking_skills.external_qualification`, which verifies a frozen evidence package from a real coding-agent harness run. The verifier checks exact candidate/target/runtime identities, evidence digests, Skill installation vs native invocation evidence, Campaign lifecycle checkpoints, no-manual-repair/no-prior-chat boundaries, and fresh-context handoff/resume integrity.

A synthetic fixture proves the verifier contract. **A real-harness PASS result is empirical evidence and must come from a real frozen external attempt.** The repository does not convert a fixture PASS into a claim that a real harness performed the run.

See `docs/external-golden-path-verifier.md`.

## Release qualification

v0.3 release candidates are qualified on the exact PR head by three complementary lanes:

1. **Product Validation** — Python 3.11/3.12 Campaign product, installed wheel, repository contracts, and filesystem security.
2. **Lab Validation** — retained source-only research/lab suites, kept separate from shipped-product authority.
3. **Release Candidate Distribution** — wheel + sdist build, `twine check`, exact artifact names, fresh installs, schema-v2/product-lab assertions, installed validator-runtime checks, and candidate artifact digests.

Tagged publication also runs `twine check` before upload.

## What this is not

- Not a centralized semantic router.
- Not an autonomous project manager.
- Not a universal planner or capability-ranking engine.
- Not a semantic truth validator.
- Not a cloud service.
- Not automatic external mutation authority.
- Not a claim that copied Skills were observed or invoked by a harness.

## Repository structure

```text
src/sensemaking_skills/
  campaign_semantics/       typed Campaign contracts + schema evolution
  campaigns/                durable workspace/service/admission/lineage
  commands/                 CLI implementation surfaces
  external_qualification.py frozen real-harness evidence verifier
  skill_trees/              build-derived installed Skill trees
  validator_runtime/        build-derived installed validator runtime
skills/                     canonical agent-native Skill sources
scripts/                    canonical validation/probe tooling
tests/                      product, installed-wheel, integration, and retained-lab tests
docs/                       canonical product, architecture, release, and research docs
experiments/                retained research evidence/lab material
```

## Canonical documentation

- `STATUS.md` — current release/product state.
- `docs/sensemaking-campaign.md` — canonical Campaign product model.
- `docs/productization-v0.3.md` — v0.3 delivery/release baseline.
- `docs/campaign-schema-evolution.md` — schema v2 compatibility contract.
- `docs/product-lab-boundary.md` — shipped product vs retained lab boundary.
- `docs/external-golden-path-verifier.md` — real-harness evidence verification protocol.
- `docs/harness-adapters.md` — deterministic harness setup roots.
- `docs/artifact-ingestion.md` — validated artifact admission and installed runtime.

## Development

Run the shipped-product validation locally from a source checkout with the same commands encoded in `.github/workflows/validation.yml`. Retained lab validation is separately defined in `.github/workflows/lab-validation.yml`.

The release version is declared only in `pyproject.toml`; `sensemaking_skills.__version__` derives it from installed distribution metadata.

License: MIT.
