# Frequently Asked Questions

**Current repository source:** `1.0.0rc3.dev0`  
**Next release-candidate target:** `1.0.0rc3`  
**Release phase:** development — RC2 is not yet frozen or published.

Current product/release authority lives in `STATUS.md`,
`docs/product-strategy.md`, `docs/adr/0029-current-product-boundary.md`,
`release-v1.0.yaml`, and `docs/operations-runbook.md`. This FAQ is
explanatory only; executable contracts and those authority surfaces win if prose
drifts.

## Installation & Setup

### Q: How do I install Sensemaking Skills?

For the latest public PyPI distribution:

```bash
python -m pip install sensemaking-skills
sensemaking-skills --version
```

The public package may lag current repository development. To use current
`main` / source development:

```bash
git clone https://github.com/ThorStarlord/sensemaking-skills.git
cd sensemaking-skills
python -m venv .venv
# activate the environment
python -m pip install -e .
sensemaking-skills --version
```

Current source should report `1.0.0rc2.dev0` while the repository is developing
toward `1.0.0rc2`.

### Q: What are the supported systems?

The current reduced-scope release target supports Python 3.11 and 3.12 on
Windows and Linux. The shipped Python dependencies are declared in
`pyproject.toml` and currently include Click and PyYAML.

### Q: Does Sensemaking require external services?

The core product is local-first and has no server, cloud, database, or network
requirement. A coding-agent harness may use its own model/API service; that is a
property of the harness, not the Sensemaking package.

## Usage

### Q: Where should a new user start?

Use `GETTING_STARTED.md`. Coding agents should use
`skills/using-sensemaking/SKILL.md`. Maintainers and release operators should
use `docs/operations-runbook.md`.

### Q: What is the current product?

Sensemaking Skills is an agent-native repository decision-support and control
layer. It helps an active coding agent turn uncertainty into grounded evidence,
explicit decisions, bounded responsibilities, optional durable Campaign state,
and reconstructible next-action context without replacing the agent's semantic
judgment.

### Q: Do I need a Campaign for every task?

No. Use the lightest process that preserves the required engineering
invariants. Campaign state is useful when repository-specific decision context
must survive sessions, agents, machines, or long-running responsibilities.

### Q: How do I diagnose a repository?

Use the Sensemaking control loop and invoke `repo-sensemaker` when
repository-wide evidence could materially change the next responsibility. The
canonical output remains a grounded `repository_sensemaking_brief`.

### Q: What are the four primary fog types?

The canonical diagnostic vocabulary contains product, UI, documentation, and
architecture fog. Fog classification is diagnostic compression, not automatic
routing authority.

### Q: Can I use different coding-agent harnesses?

The repository can install its generic Agent Skills into explicit discovery
roots for supported targets such as generic Agent Skills environments, Claude
Code, Codex, and OpenCode. The release contract does **not** currently claim
native-harness compatibility or cross-harness portability beyond its declared
support/evidence ceiling.

## Campaigns and artifacts

### Q: What Campaign schema is current?

Campaign schema **v2** is the durable Version 1.0 representation. Supported
historical v1 inputs are accepted only through deterministic migration and are
normalized to v2 without semantic reinterpretation.

### Q: Can Sensemaking work with multiple repositories?

Campaign mechanics support explicitly selected multi-repository targets and
caller-authored relationships. They do not automatically discover repositories
and do not provide atomic cross-repository commit, deploy, or rollback
coordination.

### Q: Does validation decide whether a claim or strategy is true?

No. Mechanical validation establishes mechanically decidable representation,
integrity, provenance, identity, or conformance properties.

```text
validator passed != semantic truth
evidence admitted != responsibility warranted
capability available != capability selected or authorized
```

## Releases

### Q: Is `1.0.0rc1` the current release candidate?

No. `1.0.0rc1` remains historical qualified provenance for exact source
`70542d47412d98ee6dfae5de6df29bf271304568`. Continued development superseded
it as the identity of current `main`.

The repository is currently `1.0.0rc2.dev0` in development toward
`1.0.0rc2`. RC2 will be minted only when candidate-changing work has converged
and one exact source state is ready for fresh qualification.

### Q: Is final Version 1.0 ready?

Not yet. Final publication is a separate release-owner transition governed by
`docs/release-v1.0-contract.md`, `docs/release-v1.0-checklist.md`, and
`scripts/validate-release-readiness.py`.

Native-harness compatibility, cross-harness portability, and semantic usefulness
are currently deferred/excluded from the reduced-scope support promise rather
than silently treated as proven.

## Troubleshooting

### Q: `sensemaking-skills` is not found after installation.

Confirm the environment containing the installation is active, then run:

```bash
python -m pip show sensemaking-skills
python -m sensemaking_skills.cli --version
```

### Q: A Skill install differs from the repository version.

Use `sensemaking-skills setup-skills ... --dry-run` first. Divergent installed
Skill trees are preserved unless replacement is explicitly requested with
`--force`.

### Q: Where do I report problems?

Use the repository's GitHub issues. For contribution expectations, see
`CONTRIBUTING.md` and `CODE_OF_CONDUCT.md`.

## Project

### Q: How is this licensed?

MIT License. See `LICENSE`.

### Q: What is the roadmap?

Current strategic direction is represented by `docs/product-strategy.md` and
`STATUS.md`. Historical PRDs, phase reports, old roadmap entries, and candidate
directions are not automatically current commitments.
