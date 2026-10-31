# Getting Started with Sensemaking Skills

Sensemaking Skills combines agent-native Skills with an optional local Campaign CLI. The active coding agent supplies semantic judgment; deterministic tooling makes state, evidence, provenance, explicit decisions, and repository identity durable and mechanically checkable **when that durability is useful**.

**Documentation role:** this is the canonical **human how-to-use entry point** for Sensemaking Skills. Start here when you want to install the product, understand the normal usage sequence, or decide whether a task needs repository sensemaking or durable Campaign state. It intentionally points to deeper references rather than duplicating their contracts.

Use the adjacent references by audience:

- **Workflow composition / canonical Campaign golden paths:** `docs/agent-workflow-golden-path-v1.md`.
- **Single entrypoint for coding agents:** `skills/using-sensemaking/SKILL.md` — understands the repository, explores what it could become, composes the specialized Skills, and implements only when separately authorized ([ADR 0034](docs/adr/0034-ontology-first-adaptive-sensemaking.md)).
- **Long-horizon continuation:** `skills/strategic-sensemaking-loop/SKILL.md` — composed by `using-sensemaking` to resume a strategic episode or full-autonomy mission from one prompt; maintainers may invoke it directly.
- **Control architecture crosswalk:** `docs/adaptive-semantic-control-architecture-v0.md` — how existing control scopes, policy layers, authority, execution/evidence, and strategic reassessment compose; optional reference, not a required workflow.
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

The public PyPI distribution and the repository development source are separate identities. To install the latest package currently published on PyPI:

```bash
python -m pip install sensemaking-skills
sensemaking-skills --version
```

**To use the Skills, install from source (below).** The latest published
distribution (`0.2.1`, checked 2026-10-28) contains no Skill trees and no
`setup-skills` or `semantic` commands, so the Skill installation step below
cannot run from it. A repository that receives the Skills also needs a CLI from
the same source revision for the Steward's `semantic` commands; a pinned
`uv tool install` from a commit works too (`skills/repository-semantic-steward/SKILL.md`,
"Verify and pin the CLI").

The repository source is `1.0.0rc5.dev0`, developing toward the reduced-scope `1.0.0rc5` candidate target on integrated RC4 `main`. RC4 integrated as `9ab42ee1248358bc9bf04d9f68fb49bbf1b2d776` with the exact frozen candidate tree; no RC4 qualification transfers to these changed development bytes. Install from source:

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

With no `--profile` flag, every packaged Skill is installed (52), as before. To install a smaller, dependency-closed set:

```bash
# the public entrypoint and the Skills its repository-understanding path needs (19)
sensemaking-skills setup-skills --target claude --scope user --profile entrypoint

# the same profile plus the Product Management domain pack (46)
sensemaking-skills setup-skills --target claude --scope user --profile entrypoint --include product-management
```

Setup reports which active workflows have their required Skills installed in that location. That is installation availability. It is not workflow liveness and does not authorize execution. A workflow whose required Skills are missing is listed as not available.

Installing the Skills is the only setup the entrypoint needs. Repository
configuration through `setup-sensemaking-skills` is optional and never a
prerequisite for `using-sensemaking`.

## Optional decision transparency

For a detailed audit, ask: "Use `using-sensemaking` on this repository with
maximum decision transparency; explain consequential Skill selections and
skips before acting, and distinguish the observed host events from your
rationale." The agent will explain its choices and reassess specialist results,
then produce a decision audit with the available evidence and its limitations.
This is opt-in; ordinary use remains concise and adaptive. Neither an audit nor
a Skill invocation grants authority to modify or publish repository content.
See `skills/using-sensemaking/references/decision-observability-v1.md` for the
contract and `examples/decision-observability-example.md` for an illustrative
report. Host telemetry varies and self-reported explanations are not proof of
hidden reasoning or causation.

## Choose how much Sensemaking you need

You do not need to create a Campaign for every task. The coding agent should use the lightest process that preserves the required engineering invariants.

**Give the Skill a repository, not a feature request.** Once
`using-sensemaking` is invoked, "Use `using-sensemaking` on this repository"
is sufficient to discover **what the repository is, what it could become, and
which direction is warranted**. On a first visit the agent establishes a
source-grounded model of the product's domain and architecture (reusing one
that already exists), explores possible futures broadly enough to challenge the
first visible candidate, and then selects or recommends a direction, with its
evidence, alternatives and remaining uncertainty. A semantic foundation with a
coverage report, a possibility landscape, an architecture synthesis, a
strategic disposition, a concrete next responsibility and a justified
no-change are all complete outcomes; none requires a code change. A list of
files read, a review of just the Skill itself or "return to the roadmap" is not
that output, and the agent does not invent work.

This repository-only entry authorizes understanding and reasoning, **not
automatically code changes, push or merge**. Explicit requests for bounded implementation or
an ongoing delegated construction mission take precedence and retain the
target repository's authority and verification boundaries.

For example, "Use `using-sensemaking` to diagnose the `sensemaking-skills`
repository" names a **method** and a **repository-wide target**. "Diagnose
`skills/using-sensemaking/` itself" explicitly scopes the target to that
component. The agent should preserve that distinction and correct the scope
if the user identifies a misinterpretation; neither prompt selects a feature.

### Ground an unfamiliar target repository for autonomous work

Start with the target's product intent and current code, not a procedural
checklist. If `.sensemaking/intent.md` and `invariants.md` already exist,
read those plus the task-relevant context or decisions, then check consequential
claims at their sources. If no pack exists, reuse `CONTEXT.md`, `AGENTS.md`,
`CLAUDE.md`, tests, and product documentation; a pack is **optional** and
must not block useful authorized work. The small
[`templates/grounding-pack/`](templates/grounding-pack/README.md) format is
for non-derivable intent, domain distinctions, traps, and decisions that
another session would otherwise lose. Never duplicate the repository's class
or module inventory.

When implementation of a product goal is delegated, the agent should identify the highest-value
remaining difference between intended user experience and current behavior;
select, implement, and verify a bounded improvement; update only affected
durable knowledge; and continue without repeated owner routing until the
goal or a genuine authority/external boundary is reached. The owner can
delegate product and architectural choices within an agreed goal; delegation
does not itself authorize protected external actions.

### Use existing repository knowledge during active coding

When a consequential architecture choice depends on a previous design
decision, look for reviewed `.sensemaking/knowledge/*.json` records in the
target repository. The
[Repository Semantic Steward](skills/repository-semantic-steward/SKILL.md)
provides source-checked RECALL and RECONCILE guidance, including historical
alternatives and conservative change auditing. For an exact committed index
already present outside the target checkout, retrieve relevant context with:

```bash
sensemaking-skills semantic knowledge-query --db /outside/knowledge.sqlite \
  --repository owner/repository --target-ref "$INDEXED_SHA" \
  --operation context-for --subject src/relevant_module.py --repo . --json
```

`owner/repository`, the source path and `$INDEXED_SHA` are caller-provided
examples, not repository-specific facts. If no suitable index exists, read the
Git-authored knowledge and cited current source directly; normal engineering
work must not wait for an index bootstrap. The query only describes its
indexed revision, and `workspace_context` discloses unindexed edits. Review
`context.alternatives` and any `NOT_ASSESSED` / `TRUNCATED` gaps rather than
assuming historical information is complete. See the
[persistent knowledge CLI contract](docs/semantic-architecture/persistent-knowledge-cli.md).
This discovery guidance does not install Skills or enable other harnesses
automatically.

### Optional: attach the view to an active Campaign

Use this only when a Campaign already binds the target and its responsibility is
the change in progress. The intended sequence is: read the Campaign
responsibility; request the context of the files that change; inspect the
original authority and source those records cite; build ordinary code; and
reconcile only consequential knowledge. No Skill, planner or onboarding step is
required.

```bash
sensemaking-skills campaign working-context --workspace "$CAMPAIGN" --json \
  --knowledge-db /outside/knowledge.sqlite \
  --knowledge-repository owner/repository \
  --knowledge-ref "$INDEXED_SHA" \
  --knowledge-repo . \
  --knowledge-path src/relevant_module.py \
  --knowledge-path src/related_module.py
```

- The four `--knowledge-*` identity and index options are all-or-nothing. Repeat
  `--knowledge-path` for up to eight files. Each file keeps its own coverage; the
  files are not implied to depend on one another.
- The knowledge checkout must be the Campaign target's repository. A mismatch, an
  unindexed revision or a failed query is an explicit error, never a silent
  fallback.
- The attached view is added beside the Campaign fields and changes none of them.
  It describes the indexed revision. Read the original source before relying on
  it, and check `caveats` for historical, dirty or unassessed coverage.

Skip Campaign entirely for a clear bounded task. Using this view does not establish
S5 longitudinal reuse or S6 transfer; those claims need separate qualification.

### Default product-facing path

You normally need only three entry surfaces:

```text
human first use
-> GETTING_STARTED.md

any repository request (understand, explore, decide, or implement when authorized)
-> using-sensemaking

long-horizon or full-autonomy continuation
-> composed by using-sensemaking (strategic-sensemaking-loop)
```

Use a specialized Skill directly when its bounded responsibility is explicitly
what you need. Deeper policy, continuity, Campaign, journey, organization,
semantic-architecture, and validator surfaces should appear only when they
materially help the current work.

For the full map, see
[`docs/system-capability-atlas-v1.md`](docs/system-capability-atlas-v1.md).


```text
Known narrow change, locally evidenced, one context
-> direct bounded work + relevant tests

Exploratory creative/UI design with unresolved experiential value
-> expose an isolated bootable preview with enough smoke checks to inspect it
-> observe genuine interaction before hardening speculative layout behavior
-> keep no-data-loss, persistence, security and author-authority safeguards

You want to understand a repository or what it could become
-> use using-sensemaking; it builds or reuses the semantic foundation first
   and can finish with no code change

Repository/product future itself is open and you want plausible construction paths
-> using-sensemaking composes strategic-repository-analysis for Level-3 analysis

You want a long-horizon episode to resume from one prompt
-> using-sensemaking composes strategic-sensemaking-loop
-> it reuses current artifacts and skips stages that are already complete

You want FULL AUTONOMY / FULL DELEGATION toward a terminal repository outcome
-> using-sensemaking with strategic-sensemaking-loop's autonomous terminal mission
-> it continues across bounded responsibilities until the terminal goal or a genuine stop boundary

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

A preview booting successfully verifies inspectability, not usability. Firsthand
feedback may justify a reversible personal design direction but not universal
preference; before a development default handles real content, verify touched
save/reopen/recovery and authority invariants. This is existing proportional
rigor, not a new Spike Mode or permission to bypass protected transitions.

```text
more guidance != more visible machinery
large task != Campaign required
high consequentiality != Campaign required
desired delegation != granted authority
```

For the detailed agent-facing interpretation, see `skills/using-sensemaking/references/adaptive-guidance-v0.md`.

## Delegate a complete repository mission

For high-delegation development, you can delegate a **terminal repository
outcome** instead of manually sequencing every feature, refactor, or repair.

A useful product-completion mission is:

```text
Goal: Build this repository until every feature and capability explicitly
required by the current authoritative product scope is implemented and satisfies
its applicable acceptance and repository-qualification criteria.

Operating policy: Reconstruct current repository reality before assuming work is
still missing. Resolve decision-changing uncertainty before implementation. Use
repo-sensemaker when repository-wide evidence could materially change the next
responsibility. Use durable Campaign state when continuation complexity makes
transient context unreliable. After each bounded responsibility, reassess what,
if anything, is warranted next.

Scope discipline: Treat only current authoritative product commitments as
requirements. Backlog items, candidate directions, stale issues, historical
plans, and speculative improvements do not become required work unless current
authority promotes them.

Authority discipline: Desired delegation does not expand granted authority. Do
not silently revise product-thesis commitments or infer permission to merge,
release, deploy, publish, mutate external systems, or perform destructive
actions.

Stop conditions: Stop when authoritative requirements are satisfied or
legitimately dispositioned and no decision-changing gap blocks the completion
claim; when no further repository change is warranted; when a reserved owner or
product-thesis decision is required; or when an external blocker prevents
further authorized work.
```

This delegates **intermediate engineering judgment**, not unlimited scope or
authority. For additional bounded mission patterns and anti-patterns, see
`skills/using-sensemaking/references/delegated-goal-patterns.md`.

### Run a full-autonomy terminal mission

When you want Sensemaking to keep selecting and completing warranted
responsibilities until a terminal outcome is reached, use
`strategic-sensemaking-loop` with the autonomous terminal-mission profile.

A canonical prompt is:

```text
Run this repository mission with FULL AUTONOMY and FULL REPOSITORY DELEGATION.

TARGET:
[TARGET_SYSTEM_OR_FEATURE]
or AUTONOMOUS_HIGHEST_LEVERAGE_BOTTLENECK

TERMINAL GOAL:
Advance the authoritative product scope until the target capability/system is
construction-complete and satisfies all repository-answerable acceptance and
qualification criteria.

AUTONOMY:
Proceed through repository-answerable decisions and implementation
responsibilities without waiting for further approval. After each consequential
responsibility, reconcile current reality, identify the highest-value remaining
difference to the terminal goal, establish the next warranted responsibility,
and continue automatically.

STRATEGIC SEARCH:
Run repository-wide breadth -> frontier candidates -> proportional depth ->
construction paths only when Level 3 is genuinely open or reopened. Generate
only materially real alternatives; do not force an arbitrary count. When
strategy is already settled, resume at the current responsibility/execution/
reconciliation boundary.

CONSTRUCTION:
Prefer BUILD / REVERSIBLE BUILD when retained construction is warranted and more
useful than separate evidence-only work. Complete every decision-relevant
vertical layer required by the capability without manufacturing irrelevant
architecture.

FIELD VALIDATION:
External trials, panels, professional asset production, and live telemetry are
deferred until construction completeness unless current authoritative
requirements make them genuine prerequisites. Synthetic personas and
first-principles reasoning may guide construction decisions but are not empirical
evidence.

EVIDENCE:
Implement -> verify -> reconcile -> promote repository status only when the
evidence supports the claim. Do not leave TODOs, placeholders, empty stubs, or
deliberately incomplete happy-path-only behavior where the target requires the
omitted behavior.

AUTHORITY:
Full repository delegation covers ordinary repository-local construction,
repair, refactor, deletion, documentation, tests, qualification, status updates,
issues, branches, commits, and pull requests. Merge, release/deployment,
credentials/billing, Level-4 thesis choices, genuine owner-preference decisions,
destructive external mutation, and cross-repository scope expansion remain
separately governed unless explicitly granted.

STOP ONLY WHEN:
- the terminal repository outcome is satisfied and supported by applicable
  repository-answerable evidence;
- no further repository change is warranted;
- a genuine owner/Level-4 decision is required;
- an unavoidable external blocker prevents all remaining warranted work; or
- the next required action exceeds granted authority.
```

The target token `AUTONOMOUS_HIGHEST_LEVERAGE_BOTTLENECK` means: select the
highest-value remaining difference between current repository reality and the
authoritative terminal outcome, using qualitative Sensemaking judgment rather
than a numeric priority score.

Full autonomy does **not** force breadth search after every responsibility and
does not imply automatic backlog execution. A responsibility can complete while
the terminal mission remains open; after reconciliation, the loop should select
the next warranted responsibility and continue.

Construction-before-field-validation is a mission policy, not a universal
Sensemaking law. When external evidence is an authoritative prerequisite for a
specific safety, legal, regulatory, or product claim, the agent must preserve
that prerequisite or narrow the claim rather than bypass it.

Synthetic personas are design-reasoning aids, not observed users:

```text
synthetic persona
!= empirical user evidence

repository qualified
!= externally validated
!= production deployed
```

Protected-transition authority may be granted separately, for example:

```text
MERGE_AUTHORITY = YES
RELEASE_AUTHORITY = NO
DEPLOY_AUTHORITY = NO
```

Repository policy still controls whether the transition is actually available.

### Verify Skill identity before attribution-sensitive trials

Record three separate identities: the reviewed source revision, the installed
Skill tree in the intended discovery root, and the instructions actually loaded
by the host. A matching installation does not prove which Skill the host loaded,
especially when multiple discovery roots or cached sessions exist.

For a file-based installation, run the existing drift probe from a reviewed
source checkout, selecting the actual root and Skill explicitly:

```bash
git rev-parse HEAD
python scripts/probe_skill_distribution.py --repo-root . \
  --installed-dir /path/to/actual/skills --skill using-sensemaking --no-write
```

Without `--installed-dir` the probe uses `~/.agents/skills`, which may not be
the Codex, Claude, or other host's selected root. It compares the entrypoint
and references; inspect the complete tree separately when extra files or local
customizations matter. Without `--sync`, the probe does not modify installed
Skills. **`--no-write`
only suppresses the report file: `--sync --no-write` still changes installed
Skills.** Without `--skill`, sync can affect multiple Skills. Before an explicit
replacement, identify the intended root, inspect and preserve divergent files,
and limit the operation to the authorized Skill.

For the loaded identity, use the host's actual invocation and content or version
evidence when available. A catalog entry or a file comparison alone does not
establish it. If the host does not expose that evidence, record the loaded
identity as unknown; a running session need not reload an updated file. Hosted
or non-filesystem Skill surfaces may have a separate update mechanism.

```text
repository Skill current
!= harness-loaded Skill current automatically

behavior observed under stale/unknown Skill identity
-> useful normal-use evidence may remain
-> causal attribution to the current Skill revision is weaker
```

Do not throw away the episode. Record the mismatch and narrow the claim.

The first bounded normal-use episode is preserved in
`docs/normal-use/autonomous-terminal-mission-trial-001.md`.

Canonical details:
`skills/strategic-sensemaking-loop/references/autonomous-terminal-mission-v1.md`.

## Diagnose or analyze repository evolution

Ask the active coding agent to use `using-sensemaking` as its control discipline.

When repository-wide evidence could materially change the next bounded responsibility, `repo-sensemaker` can produce a diagnostic `repository_sensemaking_brief`.

When the question is higher-level—**what could this repository become, what coherent ways could it be constructed from here, and what strategic uncertainty distinguishes those futures?**—use `strategic-repository-analysis`. It produces a `strategic_repository_analysis` containing a current-system model, capability/limitation map, Strategic Frontier, coherent construction paths, qualitative comparison, decision-changing uncertainty, and a semantic strategic disposition.

When you want the agent to **start or resume the entire strategic episode without manually prompting every transition**, use `strategic-sensemaking-loop`. It composes the existing strategic analysis, responsibility, execution, evidence-return, reconciliation, and reserved-decision surfaces. It does not create a master artifact or force all stages to run.

When a later repository state needs to be compared with an earlier strategic
analysis, author a new analysis with explicit continuity metadata when that
relationship is decision-relevant. Deterministic projections are then available:

```bash
sensemaking-skills strategy inspect --artifact artifacts/strategic_repository_analysis.md
sensemaking-skills strategy paths --artifact artifacts/strategic_repository_analysis.md
sensemaking-skills strategy uncertainty --artifact artifacts/strategic_repository_analysis.md
sensemaking-skills strategy assumptions --artifact artifacts/strategic_repository_analysis.md
sensemaking-skills strategy compare --before /path/to/older.md --after /path/to/newer.md
sensemaking-skills strategy drift --artifact artifacts/strategic_repository_analysis.md --repo /path/to/repo
sensemaking-skills strategy history --artifact /path/to/sra-1.md --artifact /path/to/reconciliation.md --artifact /path/to/sra-2.md
sensemaking-skills strategy graph --artifact /path/to/sra-1.md --artifact /path/to/reconciliation.md --artifact /path/to/sra-2.md
```

`strategy drift` reports typed mechanically observable source/evidence/declared
governing-authority currentness. `strategy history` and `strategy graph`
project only relationships declared in explicitly supplied analysis/reconciliation
artifacts. They do not declare strategy invalid, infer causal history, select a
path, or require reanalysis by themselves.

Optional path-transition references such as `PATH-2/T1` help locate bounded
work inside a longer strategic trajectory when that reconstruction would
otherwise be difficult. They are not roadmap tasks or automatic next actions.

```text
repository diagnosis
!= repository evolution synthesis

strategic disposition
!= implementation authorization
```

Typical reasons include:

- repository reality may contradict the apparent task;
- ownership or architecture boundaries are unclear;
- docs, tests, implementation, and plans may disagree;
- the task crosses unfamiliar subsystems;
- the next responsibility cannot be selected safely from the request alone.

Skip repository-wide diagnosis when the task is already mechanically narrow and locally evidenced.

The Skill performs semantic diagnosis. Deterministic scripts/CLI validate and persist results; they do not replace the agent's judgment.


When the open strategic question spans **multiple repositories whose identities are already explicitly selected**, use `multi-repository-strategic-analysis` to compare capability ownership and boundary/allocation futures. Do not use it to discover repositories automatically or to turn explicit dependencies into an execution schedule.

```text
explicit repository set + material boundary decision
-> multi-repository-strategic-analysis

automatic repository discovery
-> not supported / not authorized
```

When strategic work reaches a return or reserved-decision boundary, use the
smallest companion surface that preserves the decision:

```text
returned evidence materially changes a prior strategic analysis
-> strategic-repository-reconciliation

owner preference / policy / reserved authority is the missing premise
-> owner-decision-capsule

a governing Level-4 commitment is materially challenged
-> thesis-review-packet

decision-changing evidence comes from outside repository authority
-> external-evidence-packet
```

These packets are semantic-agent artifacts. They do not automatically mutate
strategy, make the owner's choice, ratify a thesis revision, or turn external
evidence into repository truth.

## Analyze consequential change impact

Use `change-impact-analysis` when the implementation target is known but a safe
completion claim depends on understanding what else the change materially affects.

Typical examples:

- a shared contract/API change;
- an ADR/authority boundary change;
- a release identity or qualification change;
- a change that can stale documentation/claims;
- an explicitly scoped cross-repository interface change.

```text
reference occurrence != material impact
impact identified != change authorized
follow-up responsibility != backlog item
```

The output is `change_impact_analysis`. It records affected surfaces,
verification/reconciliation needs, bounded follow-up responsibilities, and one
closure effect; it does not execute or authorize the follow-up.

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

## Use the small Campaign root first

`campaign --help` shows the durable kernel only. Secondary composition,
history, portability, graph, strategy, and compatibility tools are under
`campaign advanced`. Historical direct command paths remain callable during
the compatibility window, but new guidance should use the advanced namespace.

## See the current Campaign golden paths

When Campaign durability is warranted, the CLI exposes static navigation for composing existing Campaign surfaces. It does not choose a flow or execute its steps. The canonical workflow-composition reference is `docs/agent-workflow-golden-path-v1.md`.

```bash
sensemaking-skills campaign advanced workflow list
sensemaking-skills campaign advanced workflow show single-repository
sensemaking-skills campaign advanced workflow show fresh-context
sensemaking-skills campaign advanced workflow show transferred-campaign
sensemaking-skills campaign advanced workflow show multi-repository
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

sensemaking-skills campaign advanced preflight \
  --workspace /tmp/CMP-0001 \
  --json
```

Use `campaign doctor` when a mechanical preflight failure needs a bounded diagnostic path.

## Inspect capabilities after responsibility selection

```bash
sensemaking-skills campaign advanced capability-context \
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

The decision surface now treats bookkeeping as machinery: `--transition-id`,
`--to-state`, and (for advance) `--responsibility-id` are optional and are
generated deterministically when omitted. The agent still supplies the semantic
content: decision, responsibility statement, blocked decision, scope, authority
classification, evidence, and success conditions.

```text
agent supplies semantics
machine supplies bookkeeping

authority classification recorded
!= authority granted or enforced
```

## Complete and optionally archive a terminal Campaign

`campaign close` remains the semantic terminal decision. Only afterward can a deterministic completion receipt be created:

```bash
sensemaking-skills campaign advanced closeout --workspace /tmp/CMP-0001 --json
sensemaking-skills campaign advanced completion-receipt --workspace /tmp/CMP-0001 --json
sensemaking-skills campaign advanced archive --workspace /tmp/CMP-0001 --json
```

Archive is a nondestructive marker, not a success judgment.

## Transfer a Campaign to a different path or machine

Inspect bundle bytes before durable import:

```bash
sensemaking-skills campaign advanced bundle-inspect --bundle /path/to/CMP-0001.bundle --json
sensemaking-skills campaign advanced bundle-resume-context --bundle /path/to/CMP-0001.bundle --json
```

After explicit import, provide the local target path rather than asking Sensemaking to discover it:

```bash
sensemaking-skills campaign advanced target rebind \
  --workspace /path/to/imported/CMP-0001 \
  --target-repo /new/path/to/repository \
  --json
```

Rebinding accepts only the same recorded repository identity and exact recorded Git/worktree state. It is not target refresh.

## Multi-repository Campaigns

Additional repositories are explicitly added by alias. Relationships are explicitly authored, then mechanically checked:

```bash
sensemaking-skills campaign advanced multi-target add --help
sensemaking-skills campaign advanced multi-target relate --help
sensemaking-skills campaign advanced multi-target verify --help
sensemaking-skills campaign advanced multi-target dependency-check --help
sensemaking-skills campaign advanced multi-target graph --help
```

Multi-target membership or dependency validity is not proof that the architecture or execution order is correct.

## Inspect evidence lineage and reconciliation

```bash
sensemaking-skills campaign advanced lineage --workspace /tmp/CMP-0001
sensemaking-skills campaign advanced reconciliation --workspace /tmp/CMP-0001
```

These commands reconstruct mechanical provenance/disposition state; they do not decide what the evidence means.

## Handoff and resume

```bash
sensemaking-skills campaign advanced handoff --workspace /tmp/CMP-0001
sensemaking-skills campaign advanced resume --workspace /tmp/CMP-0001
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

For current release/strategic state, see `STATUS.md`, `docs/operations-runbook.md`, and `docs/release-v1.0-contract.md`.

## Reconstruct a full decision journey

When strategy, responsibility, execution, evidence return, and reassessment already exist but are spread across different surfaces, use Decision Journey Productization v1.

Start with caller-selected guidance:

`bash
sensemaking-skills journey guide --intent repository-future
`

Available intents are deliberately small and static:

- `repository-future`;
- `responsibility-unclear`;
- `selected-work`;
- `returned-work`;
- `repository-changed`;
- `change-consequences`;
- `multi-repo-boundary`.

This is guidance, not automatic routing. The command does not invoke the suggested capability.

For fresh-agent context, explicitly choose a profile:

`bash
sensemaking-skills journey context --profile strategic --strategy-artifact artifacts/strategic_repository_analysis.md
sensemaking-skills journey context --profile responsibility --workspace /path/to/CMP-1
sensemaking-skills journey context --profile execution --workspace /path/to/CMP-1
sensemaking-skills journey context --profile reassessment --workspace /path/to/CMP-1 --change-impact-artifact artifacts/change_impact_analysis.md
`

For the complete contract, companion templates, and playbooks, see:

- `docs/decision-journey-productization-v1.md`
- `docs/decision-journey-playbooks.md`

