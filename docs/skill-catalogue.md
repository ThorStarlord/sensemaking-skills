# Skill Catalogue

**Status:** descriptive orientation map. It adds no routing, authority, or
selection rule. It is subordinate to each Skill's own `skills/<name>/SKILL.md`,
`docs/system-capability-atlas-v1.md`, and `docs/canonical-vocabulary.yaml`.

The repository ships 51 Skills under `skills/`. This page says what each one
is for and how visible it should normally be. Per the operating discipline,
**choose the responsibility first, then the Skill**; a Skill's existence is not
a reason to invoke it.

Visibility classes (from the System Capability Atlas):

- **Front door** - what a human or coding agent normally starts from.
- **Specialized** - invoke directly only when its bounded responsibility is
  explicitly the task.
- **Conditional/internal** - used at a specific boundary of another flow.
- **Maintenance** - for maintaining the Skills themselves.


## Default cognitive surface

The package still ships the full Skill inventory for compatibility and explicit
specialized use. Normal repository work should begin from a much smaller core:

| Skill | Default role |
| --- | --- |
| `using-sensemaking` | ordinary repository decision/support doctrine |
| `strategic-sensemaking-loop` | one-prompt strategic or delegated terminal mission |
| `repo-sensemaker` | repository-wide diagnosis when current reality is unclear |
| `strategic-repository-analysis` | repository evolution when the future itself is open |
| `output-reconciler` | consequential completed-work claim reconciliation |
| `repair-verifier` | verify a claimed repair against the original finding |
| `handoff` | explicit cross-Skill/context transfer only when needed |

All other Skills are specialized, conditional, maintenance, or domain-pack
capabilities. Their presence in the distribution does not make them part of the
default reasoning path.

```text
shipped
!= default-visible
!= automatically warranted
```

## 1. Front door and setup

| Skill | Purpose | Visibility |
| --- | --- | --- |
| `using-sensemaking` | Bootstrap for coding agents: fog classification, responsibility selection before Skill, validator-error reading, bounded retry, stopping. | Front door (agent) |
| `strategic-sensemaking-loop` | One-prompt start/resume of an end-to-end strategic repository episode, including full-autonomy terminal missions. | Front door (strategic) |
| `setup-sensemaking-skills` | Configure a repository for these Skills (agent instructions, contract references, mode defaults, run-log conventions). Run before first use. | Setup |

## 2. Repository sensemaking (Level 2)

| Skill | Purpose |
| --- | --- |
| `problem-framer` | Turn a vague idea or repository fog into a structured problem frame. |
| `unknowns-mapper` | Separate knowns, unknowns, assumptions, and risks. |
| `repo-sensemaker` | Diagnose a repository into a Repository Sensemaking Brief (purpose, contradictions, weakest consequential boundary). |
| `workflow-planner` | Compatibility/reference planner for registered workflow definitions. Current selection is compatibility-only by default except explicitly promoted bounded subgraphs. |
| `handoff` | Convert an artifact into a ready-to-copy prompt for the next Skill. Conditional/internal. |
| `architectural-review` | Evaluate a proposed architectural response against principal-engineer judgment. |
| `change-impact-analysis` | Identify what a contemplated or completed change affects and what verification it needs. |
| `output-reconciler` | Verify claims about completed work against durable artifacts (verified / disputed / omitted). |
| `repair-verifier` | Re-run the probe after a docs-contract-reconciliation patch and mark each original finding closed or remaining. |
| `docs-aligner` | Align documentation with implementation; sharpen language; update `CONTEXT.md`. |
| `sensemaking-docs-reconciler` | Challenge this repository's architecture against its docs/registries; changes only after user approval. |

## 3. Strategic repository analysis (Level 3/4 boundary)

| Skill | Purpose |
| --- | --- |
| `strategic-repository-analysis` | Model current capability state and compare construction paths; name the decision-changing uncertainty. |
| `strategic-repository-reconciliation` | Reconcile returned evidence against a prior analysis without automatic strategy mutation. |
| `multi-repository-strategic-analysis` | Level-3 analysis over an explicitly selected repository set. |
| `owner-decision-capsule` | Package an owner-reserved decision into options and consequences without choosing for the owner. |
| `thesis-review-packet` | Prepare a Level-4 thesis review packet; does not ratify a change. |
| `external-evidence-packet` | Preserve provenance and currentness limits of evidence that lives outside repository authority. |

## 4. Campaign execution

| Skill | Purpose |
| --- | --- |
| `coding-agent-native-campaign` | Run an approved `coding_agent_native` campaign under the one-word `approve` contract. See [coding-agent-native-campaign.md](coding-agent-native-campaign.md). |

## 5. Optional Product Management domain pack (ADR 0028)

This domain is shipped for explicit product-management work but is not part of the default repository-engineering cognitive surface. Contracts in
`docs/product-management/`, manifests in `skill-manifests/pm/`.

| Group | Skills |
| --- | --- |
| Customer understanding | `persona`, `interview-synthesis`, `customer-journey`, `ideal-customer-profile` |
| Discovery and hypotheses | `discovery`, `opportunity-tree`, `hypothesis`, `pre-mortem` |
| Definition and delivery | `to-prd`, `user-stories`, `acceptance-criteria`, `to-issues` |
| Strategy and planning | `strategy`, `prioritize`, `north-star`, `okr`, `roadmap`, `lean-canvas` |
| Experimentation and fit | `experiment-design`, `ab-test-analysis`, `measure-pmf` |
| Market and commercial | `competitive-analysis`, `battlecard`, `pricing`, `gtm` |
| Launch and communication | `launch-checklist`, `release-notes`, `stakeholder-update` |

`to-issues` is the one PM-adjacent Skill without a `skill-manifests/pm/`
manifest.

## 6. Skill maintenance

| Skill | Purpose |
| --- | --- |
| `usage-researcher` | Behavioral learning loop that evaluates Skill performance in realistic scenarios. |
| `skill-maintainer` | Translate usage research into auditable Skill improvements. |

## Keeping this page current

Add a row when a Skill is added under `skills/`. Manifests for engineering and
PM Skills are listed in `domain-packs/engineering.yaml` and
`domain-packs/product-management.yaml`; see
[semantic-architecture/skill-contract-manifests-and-domain-packs.md](semantic-architecture/skill-contract-manifests-and-domain-packs.md).
