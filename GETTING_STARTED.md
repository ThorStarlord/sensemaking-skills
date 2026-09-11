# Getting Started with Sensemaking Skills v0.3.0

Sensemaking Skills combines agent-native Skills with an optional local Campaign CLI. The active coding agent supplies semantic judgment; deterministic tooling makes state, evidence, provenance, explicit decisions, and repository identity durable and mechanically checkable **when that durability is useful**.

**Documentation role:** this is the canonical **human how-to-use entry point** for Sensemaking Skills. Start here when you want to install the product, understand the normal usage sequence, or decide whether a task needs repository sensemaking or durable Campaign state. It intentionally points to deeper references rather than duplicating their contracts.

Use the adjacent references by audience:

- **Workflow composition / canonical Campaign golden paths:** `docs/agent-workflow-golden-path-v1.md`.
- **Coding agent instructions:** `skills/using-sensemaking/SKILL.md`.
- **Deeper Level-2 responsibility/authority model:** `docs/agent-native-operating-workflow.md`.
- **Maintainer/operator validation and qualification:** `docs/operations-runbook.md`.

```text
GETTING_STARTED.md = human how-to entry point
!= workflow engine
!= semantic routing authority
!= operations/qualification runbook
```

## Prerequisites

- Python 3.11+
- A repository/workspace to work on
- A coding-agent harness if you want native Skill execution

## Install

```bash
python -m pip install sensemaking-skills==0.3.0
sensemaking-skills --version
```

Expected output includes `0.3.0`.

For source development:

```bash
git clone https://github.com/ThorStarlord/sensemaking-skills.git
cd sensemaking-skills
python -m venv .venv
# activate the environment
python -m pip install -e .
```

## Install Skills for a harness

Sensemaking Skills does not auto-detect the active harness. Choose the target and scope explicitly.

```bash
# user scope
sensemaking-skills setup-skills --target generic --scope user
sensemaking-skills setup-skills --target claude --scope user
sensemaking-skills setup-skills --target codex --scope user
sensemaking-skills setup-skills --target opencode --scope user

# project scope
sensemaking-skills setup-skills --target claude --scope project --project-root /path/to/repo
```

Use `--dry-run` to preview. Divergent installed Skill trees are preserved unless `--force` is explicit.

## Choose how much Sensemaking you need

You do not need to create a Campaign for every task. The coding agent should use the lightest process that preserves the required engineering invariants.

```text
Known narrow change, locally evidenced, one context
-> direct bounded work + relevant tests

Correct repository responsibility is uncertain
-> use the Sensemaking control loop; repo-sensemaker may be useful

Material completed-work or repair claim
-> stronger evidence / reconciliation / finding-specific verification when warranted

Repository-specific decision state must survive fresh contexts,
agents, machines, or a long-running responsibility
-> use a Campaign for durability and reconstruction
```

The current product model separates several reasons for stronger support:

- **user supervision capability** affects how much explanation/scaffolding is useful;
- **desired delegation** affects how much repository-answerable judgment the agent should exercise within granted authority;
- **decision complexity** affects investigation/sensemaking rigor;
- **consequentiality** affects caution, evidence, validation, and reconciliation;
- **continuation complexity** affects whether durable Campaign state is worth its cost.

These are qualitative agent judgments, not scores, modes, or routing rules.

```text
more guidance != more visible machinery
large task != Campaign required
high consequentiality != Campaign required
desired delegation != granted authority
```

For the detailed agent-facing interpretation, see `skills/using-sensemaking/references/adaptive-guidance-v0.md`.

## Delegate a complete repository mission

For high-delegation development, you can give the coding agent a **terminal product-scope mission** rather than manually sequencing every intermediate feature, refactor, or repair.

Prefer an **authoritative product scope** over vague phrases such as "all features" or "everything in the repository." Product strategy may define purpose/user/JTBD while PRDs, accepted product/design decisions, capability contracts, and acceptance criteria define required realization.

Ready-to-copy example:

```text
Goal: Build this repository until every feature and capability explicitly required by the current authoritative product scope is implemented and satisfies its applicable acceptance and repository-qualification criteria.

Operating policy: Use Sensemaking to determine the warranted repository responsibility at each step. Reconstruct current repository reality before assuming documented work is still missing. Resolve decision-changing uncertainty before implementation. Use repo-sensemaker when repository-wide diagnosis could materially change the next responsibility. Use durable Campaign state when continuation complexity makes transient context unreliable. After each bounded responsibility, reconcile the resulting capability state and reassess what, if anything, is warranted next.

Scope discipline: Treat only current authoritative product commitments as requirements. Do not convert backlog items, candidate directions, speculative improvements, historical plans, stale issues, or optional future capabilities into required work unless an authoritative product/repository decision has promoted them.

Authority discipline: Desired delegation does not expand granted authority. Do not silently revise product-thesis commitments, perform reserved external actions, merge, release, deploy, publish, or make destructive changes unless those actions are authorized.

Stop conditions: Stop when all authoritative requirements are satisfied or legitimately dispositioned and no unresolved decision-changing gap prevents claiming scope completion; when no further repository change is warranted; when progress requires a reserved owner/product-thesis decision; or when an external blocker prevents further authorized work.
```

This prompt delegates **intermediate engineering judgment**, not unlimited authority. The agent may move through product/design clarification, architecture/domain reconciliation, implementation, documentation/integrity repair, and qualification when those responsibilities are warranted, but it should not manufacture work merely to keep the mission active.

For shorter goal patterns, repair missions, architecture/design reconciliation, long-running delegation, and prompt anti-patterns, see `skills/using-sensemaking/references/delegated-goal-patterns.md`.

## Diagnose when repository sensemaking is warranted

Ask the active coding agent to use `using-sensemaking` as its control discipline. When repository-wide evidence could materially change the next responsibility, `repo-sensemaker` can produce a canonical `repository_sensemaking_brief`.

Typical reasons include:

- repository reality may contradict the apparent task;
- ownership or architecture boundaries are unclear;
- docs, tests, implementation, and plans may disagree;
- the task crosses unfamiliar subsystems;
- the next responsibility cannot be selected safely from the request alone.

Skip repository-wide diagnosis when the task is already mechanically narrow and locally evidenced.

The Skill performs semantic diagnosis. Deterministic scripts/CLI validate and persist results; they do not replace the agent's judgment.

## Start a Campaign when durable continuation is warranted

A Campaign is the central durable Level-2 abstraction. Use it when repository-specific decision state needs to survive agent/session boundaries or otherwise become reconstructible. A Campaign is **not** the universal entry point for Sensemaking.

For a directly initialized Campaign:

```bash
sensemaking-skills campaign init \
  --workspace /tmp/CMP-0001 \
  --campaign-id CMP-0001 \
  --mission "diagnose and repair the repository boundary" \
  --target-repo /path/to/repository

sensemaking-skills campaign status --workspace /tmp/CMP-0001
```

Initialization records repository identity/state and creates durable structure. It does not infer the uncertainty, responsibility, capability selection, or authority.

For repository-level strategic work, inspect Level-3 state first and use `campaign strategy handoff` only after the active agent has explicitly selected a current frontier item and responsibility.

## See the current Campaign golden paths

When Campaign durability is warranted, the CLI exposes static navigation for composing existing Campaign surfaces. It does not choose a flow or execute its steps. The canonical workflow-composition reference is `docs/agent-workflow-golden-path-v1.md`.

```bash
sensemaking-skills campaign workflow list
sensemaking-skills campaign workflow show single-repository
sensemaking-skills campaign workflow show fresh-context
sensemaking-skills campaign workflow show transferred-campaign
sensemaking-skills campaign workflow show multi-repository
```

The same agent-facing reference ships at `skills/using-sensemaking/references/golden-paths-v1.md`.

```text
flow shown != flow recommended
step listed != step authorized
golden path != workflow engine
Campaign flow catalog != mandatory Sensemaking choreography
```

## Admit validated evidence

Installed v0.3 distributions carry the canonical validator runtime:

```bash
sensemaking-skills campaign ingest \
  --workspace /tmp/CMP-0001 \
  --artifact /path/to/repository_sensemaking_brief.md
```

For development, `--framework-root /path/to/sensemaking-skills` may explicitly select a source checkout. A bad explicit override fails closed.

## Reconstruct and preflight

```bash
sensemaking-skills campaign resume-profile \
  --workspace /tmp/CMP-0001 \
  --profile working \
  --json

sensemaking-skills campaign preflight \
  --workspace /tmp/CMP-0001 \
  --json
```

Use `campaign doctor` when a mechanical preflight failure needs a bounded diagnostic path.

## Inspect capabilities after responsibility selection

```bash
sensemaking-skills campaign capability-context \
  --workspace /tmp/CMP-0001 \
  --responsibility-type architectural_review \
  --json
```

Capability results are deterministic and unranked. Availability/compatibility is not selection or execution authority.

## Record an agent-authored decision

Use the explicit decision commands after the active agent has made the semantic judgment:

```bash
sensemaking-skills campaign advance --help
sensemaking-skills campaign defer --help
sensemaking-skills campaign close --help
```

## Complete and optionally archive a terminal Campaign

`campaign close` remains the semantic terminal decision. Only afterward can a deterministic completion receipt be created:

```bash
sensemaking-skills campaign closeout --workspace /tmp/CMP-0001 --json
sensemaking-skills campaign completion-receipt --workspace /tmp/CMP-0001 --json
sensemaking-skills campaign archive --workspace /tmp/CMP-0001 --json
```

Archive is a nondestructive marker, not a success judgment.

## Transfer a Campaign to a different path or machine

Inspect bundle bytes before durable import:

```bash
sensemaking-skills campaign bundle-inspect --bundle /path/to/CMP-0001.bundle --json
sensemaking-skills campaign bundle-resume-context --bundle /path/to/CMP-0001.bundle --json
```

After explicit import, provide the local target path rather than asking Sensemaking to discover it:

```bash
sensemaking-skills campaign target rebind \
  --workspace /path/to/imported/CMP-0001 \
  --target-repo /new/path/to/repository \
  --json
```

Rebinding accepts only the same recorded repository identity and exact recorded Git/worktree state. It is not target refresh.

## Multi-repository Campaigns

Additional repositories are explicitly added by alias. Relationships are explicitly authored, then mechanically checked:

```bash
sensemaking-skills campaign multi-target add --help
sensemaking-skills campaign multi-target relate --help
sensemaking-skills campaign multi-target verify --help
sensemaking-skills campaign multi-target dependency-check --help
sensemaking-skills campaign multi-target graph --help
```

Multi-target membership or dependency validity is not proof that the architecture or execution order is correct.

## Inspect evidence lineage and reconciliation

```bash
sensemaking-skills campaign lineage --workspace /tmp/CMP-0001
sensemaking-skills campaign reconciliation --workspace /tmp/CMP-0001
```

These commands reconstruct mechanical provenance/disposition state; they do not decide what the evidence means.

## Handoff and resume

```bash
sensemaking-skills campaign handoff --workspace /tmp/CMP-0001
sensemaking-skills campaign resume --workspace /tmp/CMP-0001
```

The durable handoff allows a fresh context to reconstruct the Campaign without relying on the previous chat transcript.

## Schema compatibility

Current Campaign artifacts use schema version 2. Historical v1 artifacts can be inspected and deterministically qualified through the schema-evolution surface documented in `docs/campaign-schema-evolution.md`.

## Real-harness qualification

A real coding-agent harness attempt can be frozen into the evidence package described in `docs/external-golden-path-verifier.md` and verified with the `sensemaking_skills.external_qualification` module.

Synthetic fixtures validate the verifier itself; they are not substitutes for a real empirical harness run. Current owner direction does not require new experiments as a prerequisite for bounded repository-only/hermetic construction.

## Important boundaries

```text
validator passed != semantic truth
available capability != selected or authorized capability
handoff != recommendation
lineage != warrant
flow shown != flow recommended
step listed != authorized action
completion receipt != proof of correctness
archive != success
repository rebound != repository selected
multi-target relation valid != architecture correct
Skill installed != Skill observed/invoked by the harness
external verifier PASS != universal compatibility
```

For current release/strategic state, see `STATUS.md`, `docs/operations-runbook.md`, and `docs/productization-v0.3.md`.