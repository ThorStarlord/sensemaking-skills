# PM distribution: installation profiles and the installation contract

**Status:** implemented in M3 (`main` `b89dcbab`, merged from PR #684). The owner decisions C, D, E, G and H are recorded in [distribution-owner-decision.md](distribution-owner-decision.md) section 8. The no-flag default is unchanged: every packaged Skill is installed. The M4 default change is not decided.

**Source of truth:** `src/sensemaking_skills/defaults/install-profiles.yaml`. `scripts/validate-contract-authority.py` checks it in CI.

## 1. Profiles and add-on

| Name | Kind | Skills | Selected by |
| --- | --- | --- | --- |
| `full` | profile | every packaged Skill (52) | `--profile full`, or no flag |
| `entrypoint` | profile | 19 | `--profile entrypoint` |
| `product-management` | add-on | 27 PM Skills | `--include product-management`, repeatable |

`--include` is additive and never removes a Skill. `entrypoint` plus `product-management` installs 46.

A profile selects which packaged Skill trees are copied. It does not change workflow liveness (ADR 0027), execution authority or any Skill's release tier.

## 2. The entrypoint profile

Members are selected by dependency closure from `using-sensemaking`, not by domain or tier:

`using-sensemaking`, `repository-semantic-steward`, `repo-sensemaker`, `strategic-repository-analysis`, `strategic-repository-reconciliation`, `strategic-sensemaking-loop`, `multi-repository-strategic-analysis`, `external-evidence-packet`, `owner-decision-capsule`, `thesis-review-packet`, `architectural-review`, `change-impact-analysis`, `output-reconciler`, `repair-verifier`, `workflow-planner`, `problem-framer`, `unknowns-mapper`, `sensemaking-docs-reconciler`, `handoff`.

**Excluded:** `coding-agent-native-campaign` (owner decision H: a specialized exploratory approval protocol, not a general dependency of Campaign durability; available under `full`), `docs-aligner`, `to-issues`, `skill-maintainer`, `usage-researcher`, `setup-sensemaking-skills`, and the 27 PM Skills.

**Closure check.** `validate-contract-authority.py` fails if a Markdown path reference from any member names a Skill outside the profile. Named references are reviewed separately. The named PM owners `pre-mortem` and `experiment-design` are conditional (M2), with stated fallbacks.

## 3. Workflow availability, as installed

`setup-skills` reports, for each destination, which active catalogue workflows have their required Skills present there. This is installation availability. It is not workflow liveness and it does not authorize execution. A workflow missing a required Skill is listed as not available.

Verified in scratch roots at merge time (nine active workflows):

| Install | Installed Skills | Active workflows available here |
| --- | --- | --- |
| no flag, or `--profile full` | 52 | 9 of 9 |
| `--profile entrypoint` | 19 | 4 of 9 |
| `--profile entrypoint --include product-management` | 46 | 4 of 9 |

The four available under `entrypoint` are `full-fog-workflow`, `fast-local-diagnostic`, `full-local-sensemaking` and `docs-contract-reconciliation`. `full-local-sensemaking` keeps its conditional `discovery` branch with the fallback stated in the workflow text.

Not available under `entrypoint`, with the Skills each needs:

| Workflow | Needs | Available with |
| --- | --- | --- |
| `docs-architecture` | `docs-aligner` | `--profile full` |
| `docs-implementation-workflow` | `docs-aligner` (step 1) and `to-prd` (step 2) | `--profile full` (`--include product-management` supplies only `to-prd`) |
| `setup-sensemaking-repo` | `setup-sensemaking-skills` | `--profile full` |
| `skill-maintenance-loop` | `skill-maintainer` | `--profile full` |
| `skill-evaluation-workflow` | `skill-maintainer`, `usage-researcher` | `--profile full` |

`docs-implementation-workflow` requires `to-prd` in the PM add-on, as owner decision C directs. It does not silently substitute another Skill. It also requires `docs-aligner`, which the earlier contract text omitted. The workflow text in both registry copies now names both requirements.

## 4. Interface: `--profile` and `--include`

The selector is `setup-skills --profile entrypoint|full` with repeatable `--include product-management`. This is owner decision E. Two alternatives were rejected:

- `--domain` classifies Skills by domain, which the owner rejected. Maintainer and setup Skills would also need a domain name.
- `--profile core` collides with the skill registry's `core` ecosystem name.

`--profile` follows the CLI's existing named-choice pattern, for example the campaign resume profiles.

The public Python signature `setup_skills` is frozen and unchanged. The selector is `setup_skill_profile`, which is not in `__all__`. Its signature digest is still covered by `docs/public-api-v1.0.yaml`.

## 5. Compatibility

- With no flag, the installed set is every packaged Skill, the same as before M3. The installed tree is byte-identical to the previous release.
- Nothing deletes an installed Skill. `copy_skill` replaces a same-named tree only under `--force`. A divergent tree is still refused without it.
- `--dry-run` creates nothing and reports the planned set.
- Unknown profiles and add-ons, and profile members that are not packaged, fail before anything is copied.

## 5a. The M4 default change

M4 would make `entrypoint` the no-flag default. Owner decision D: M4 is not part of M3 or the current RC5 development target. It is reconsidered for the first suitable release after an M3-bearing release has announced the change, through a separate rollout decision. Until then the default is `full`.

Consequences the owner accepted by decision H, to state in that release note:

- `coding-agent-native-campaign` is not installed by `entrypoint`. Campaign approval discipline is documented in that Skill, and the runtime cannot see the conversation (`exploratory_execution/conversation_approval.py`). Under `entrypoint`, approval discipline is not installed.
- Maintenance and setup workflows are not runnable under `entrypoint` (G: their liveness is preserved).

## 6. Remaining dependencies

- **Planner and runtime wiring.** The availability check lives in `workflow_availability.py` and is used by the installer. Planner, runtime and `WorkflowRegistry` selection still depend on liveness alone. A consumer that presents workflows as runnable must check installation availability as well. This is the next engineering increment, separate from M4.
- **Packaged workflow registry.** The packaged copy still lacks three compatibility-only workflows that the canonical copy has. Owner direction keeps this outside M3, unless a current contract requires it.
- **Installed copies outside a profile.** A user who installed all 52 keeps them. No profile removes them.

## 7. Owner decisions and open items

| Item | Status |
| --- | --- |
| C: `to-prd` stays in the PM add-on; `docs-implementation-workflow` must require it explicitly | Decided, implemented |
| D: no default change in M3 or RC5; M4 reconsidered after an M3-bearing release has announced it | Decided. The rollout decision itself remains open. |
| E: `--profile entrypoint|full` and additive `--include product-management` | Decided, implemented |
| G: setup and maintenance liveness preserved; catalogue eligibility separate from installation availability | Decided, implemented |
| H: `coding-agent-native-campaign` excluded from `entrypoint`; available under `full` | Decided, implemented |
| M4 rollout: which release announces the default change, and when | Open, owner decision |
| Planner and runtime consumers of installation availability | Open, next increment |
| Packaged workflow registry differences | Outside M3 |
