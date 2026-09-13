# Frequently Asked Questions

**Repository release baseline: `0.3.0` (Beta).**

Current product/release authority lives in `STATUS.md`, `docs/product-strategy.md`,
`docs/adr/0029-current-product-boundary.md`, and `docs/operations-runbook.md`.
This FAQ is explanatory only; executable behavior and those authority surfaces
win if prose drifts.

## Installation & Setup

### Q: How do I install sensemaking-skills?
For the current repository version, install from source:

```bash
git clone https://github.com/ThorStarlord/sensemaking-skills.git
cd sensemaking-skills
python -m pip install -e .
```

A matching packaged release can be installed after an explicitly tagged
publication exists. Repository qualification alone does not imply publication.

### Q: What are the system requirements?
Python 3.11 or higher. Shipped dependencies are declared by `pyproject.toml`.

## Usage

### Q: How do I start?
Use `GETTING_STARTED.md` for the human first-use sequence. A durable Campaign is
available when repository-specific decision state must survive fresh contexts,
agents, machines, or long-running work, but not every Sensemaking task requires
Campaign state.

### Q: What is the current product?
Sensemaking Skills is an agent-native repository decision-support and control
layer. It combines repository sensemaking, evidence/authority discipline,
optional durable Campaign state, bounded capability inspection, reconstruction,
reconciliation, and mechanical qualification while leaving semantic judgment to
the active coding agent.

### Q: Can I use this with different coding-agent harnesses?
Yes. Agent-facing Skills can be installed into supported discovery roots for
generic Agent Skills environments, Claude Code, Codex, and OpenCode. Core
Sensemaking operation remains local-first.

## Campaigns and artifacts

### Q: What format is the repository sensemaking brief?
The canonical `repository_sensemaking_brief` remains a Markdown artifact. Do not
infer a future-version export commitment from historical roadmap material.

### Q: Can Sensemaking work with more than one repository?
Current Campaign mechanics support explicitly selected multi-repository targets
and caller-authored relationships. They do not automatically discover
repositories and do not provide atomic cross-repository commit/deploy/rollback
coordination.

### Q: Does validation decide whether a claim or strategy is true?
No. Mechanical validation establishes mechanically decidable representation,
integrity, provenance, identity, or conformance properties. It does not turn
those properties into semantic truth, strategic priority, or execution
authority.

## Troubleshooting

### Q: `sensemaking-skills` command not found
Install the project/distribution in the active environment, then verify:

```bash
sensemaking-skills --version
sensemaking-skills campaign --help
```

### Q: A Campaign or artifact validation command fails
Use the reported diagnostic first, then consult `docs/operations-runbook.md` for
the current operator-facing validation and qualification commands. Older
milestone runbooks are historical evidence rather than current authority.

### Q: An agent cannot discover the Skills
Use `sensemaking-skills setup-skills --help` and select the harness and scope
explicitly. Project-scoped setup requires an explicit project root.

## Project and Version 1.0

### Q: What's the roadmap?
Version 1.0 is the current release target, but readiness is determined from the
current repository contracts and exact-head qualification rather than an old
feature checklist. The historical `docs/PRD-V1-Sensemaking.md` records a
superseded May 2026 five-skill product definition and is not current V1
authority.

### Q: Is this production-ready?
The current repository baseline is `0.3.0` Beta. Repository qualification can
establish bounded code, package, persistence, validation, and release-contract
properties, but stronger empirical or semantic claims retain their existing
evidence ceilings. A Version 1.0 release candidate must be qualified from its
own exact candidate head. Tagging/publication remains a separate owner action.

### Q: How is this licensed?
MIT License. See `LICENSE`.

## Still Have Questions?

- `README.md` — product overview and entry points
- `GETTING_STARTED.md` — human first-use guidance
- `STATUS.md` — current Level-3 repository state
- `docs/product-strategy.md` — current Level-4 product strategy
- `docs/operations-runbook.md` — current validation/qualification operations
