# PM distribution: candidate profiles and the installation contract

**Status:** agent proposal. Nothing here changes installer behavior. It refines the candidate default profile from [distribution-reconciliation.md](distribution-reconciliation.md), selects an interface for the planned selector, and lists what remains open. The owner has not yet decided the questions in section 6.

**Baseline:** `origin/main` after the M1 merge (`c088714f`). Dependency checks were run by static scan of `skills/` and the packaged registries at that revision. Tests were not run.

## 1. The entrypoint profile (candidate default)

A profile is a set of Skills selected by dependency closure from the public entrypoint and the workflows it can run. It is not selected by domain or by support tier.

**Members (20):**

| Skill | Why it is in the profile |
| --- | --- |
| `using-sensemaking` | The public entrypoint (ADR 0034 B). |
| `repository-semantic-steward` | The semantic foundation. Path-referenced by `using-sensemaking` and `repo-sensemaker`. |
| `repo-sensemaker` | Repository orientation. Named owner, and the target of several path references. |
| `strategic-repository-analysis` | Possibility exploration and construction paths. Named owner, and path-referenced by `repo-sensemaker`. |
| `strategic-repository-reconciliation` | Reconsideration after evidence. Named owner. |
| `strategic-sensemaking-loop` | Cross-session continuation (ADR 0034 line 54). Named owner. |
| `multi-repository-strategic-analysis` | Named owner, used only for an explicit repository set. |
| `external-evidence-packet` | Named owner for decision-changing external evidence. |
| `owner-decision-capsule` | Named owner for owner-reserved choices. |
| `thesis-review-packet` | Routed to by the controller for `THESIS_REVIEW`. |
| `architectural-review` | Named owner for adversarial challenge. |
| `change-impact-analysis` | Named in the controller's guided-entry reference. |
| `output-reconciler` | Named owner for completed-work claims. |
| `repair-verifier` | Named owner for repaired findings. Used by `docs-contract-reconciliation`. |
| `workflow-planner` | Holds the artifact contracts and registries that core Skills read by path. |
| `problem-framer` | Named owner for problem framing. Used by `full-fog-workflow` and `full-local-sensemaking`. |
| `unknowns-mapper` | Named owner for unknowns. Used by `full-fog-workflow` and `full-local-sensemaking`. |
| `sensemaking-docs-reconciler` | Named owner for docs and implementation that disagree. Used by `docs-contract-reconciliation`. |
| `handoff` | Final step of `full-local-sensemaking` and `fast-local-diagnostic`. |
| `coding-agent-native-campaign` | Campaign approval discipline. `conversation_approval.py` states the coding agent enforces it per this Skill, and the runtime cannot see the transcript. Without it, approvals run without the documented discipline. |

**Closure check.** The scan found no required reference from a member to an excluded non-PM Skill. The only non-PM mentions outside the member set are examples: `docs-aligner` as an example skill id in `repo-sensemaker/SKILL.md` line 329, `to-issues` as an example consumer in `repo-sensemaker/references/evidence-rules.md` line 50, and `to-prd` and `tdd` as examples in `handoff/SKILL.md` line 8.

The references from members to PM Skills are of three kinds, and each is classified in [distribution-reconciliation.md](distribution-reconciliation.md) section 2.2:

- **Named owners in the controller.** `pre-mortem` (adversarial challenge) and `experiment-design` (experiment design). Both are now conditional, with a stated fallback (M2).
- **Workflow steps.** `discovery` in `full-local-sensemaking`, a conditional step, and `to-prd` in `docs-implementation-workflow`, an unconditional step. Both carry a stated fallback or a stated installation requirement (M2).
- **Historical pointers.** Status notes in the skill registry. They are not dependencies.

**Workflows.** Under the entrypoint profile, four active workflows are runnable: `full-fog-workflow`, `fast-local-diagnostic`, `full-local-sensemaking` (its discovery branch excepted) and `docs-contract-reconciliation`. Five active workflows need Skills outside the profile. They are conditional, and they run only when the add-on that supplies those Skills is installed:

| Workflow | Needs | Supplied by |
| --- | --- | --- |
| `setup-sensemaking-repo` | `setup-sensemaking-skills` | `--profile full` |
| `docs-architecture` | `docs-aligner` | `--profile full` |
| `skill-maintenance-loop` | `skill-maintainer` | `--profile full` |
| `skill-evaluation-workflow` | `usage-researcher`, `skill-maintainer` | `--profile full` |
| `docs-implementation-workflow` | `to-prd` | `--include product-management` |

**Excluded from the entrypoint profile:** `docs-aligner`, `to-issues`, `skill-maintainer`, `usage-researcher` and `setup-sensemaking-skills`. Together with the 27 PM Skills, they account for the rest of the 52.

`to-issues` is excluded because only compatibility-only workflows need it. `skill-maintainer`, `usage-researcher` and `setup-sensemaking-skills` are excluded because they serve the maintenance and setup workflows, not the repository-understanding path. Whether those workflows should stay active in the default experience is owner question G.

## 2. Add-on: the Product Management domain pack

Membership: the 27 Skills in `skill-manifests/pm/`. Closure: the PM set needs only `using-sensemaking`, which is in every profile (section 2.2, E-6, of the reconciliation record). Installing the add-on satisfies `pre-mortem`, `experiment-design` and the `docs-implementation-workflow` requirement. It does not change any member of the entrypoint profile.

## 3. Interface: `--profile` against `--domain`

The planned interface was `--domain product-management` and `--domain all`. The comparison:

| Criterion | `--domain` | `--profile` |
| --- | --- | --- |
| Matches the owner's framing | No. It classifies Skills by domain, which the owner rejected. Maintainer and setup Skills would also need a domain name. | Yes. A profile is a dependency-closed set. |
| Name collisions in this CLI | None | Already used as a named-bundle choice in `campaign resume-profile` (`campaign_resume_v2_cli.py` line 49) and `campaign usability` (`campaign_usability_cli.py` line 165). The shape matches. |
| Name collisions in the repository | None | `core` is already an ecosystem name in the skill registry, so `--profile core` is rejected. |
| Behaviour when the default changes | Not applicable | `default` is rejected, because its meaning would change at M4. |
| Compatibility | Works | Works |

**Decision (agent proposal).** Use `--profile` with two values, and add a repeatable `--include` for add-ons:

- `--profile entrypoint` installs the entrypoint profile (20 Skills).
- `--profile full` installs every packaged Skill (52). This reproduces today's behaviour exactly.
- `--include product-management` adds the PM add-on (27). It is repeatable and additive. It never removes a Skill.

**Naming.** `entrypoint` describes what the profile is closed under (ADR 0034 B). It is not a domain, a tier or a default. Owner question E asks whether to keep it.

**Compatibility rules, for M3 and M4:**

- M3 adds the flags. With no flag, the installed set stays all 52, exactly as today.
- M4 changes only the no-flag default, to `entrypoint`. `--profile full` keeps today's set. The release note announces the change one release ahead.
- No flag, profile or add-on ever deletes an installed Skill. `copy_skill` is unchanged, so a divergent tree still needs `--force` (`setup_skills.py` lines 174-191).
- The wheel is unchanged. The selector filters at install time.

**Acceptance counts for M3 tests (proposed):**

| Invocation | Installed Skills |
| --- | --- |
| no flag | 52 |
| `--profile full` | 52 |
| `--profile entrypoint` | 20 |
| `--profile entrypoint --include product-management` | 47 |

## 4. The smallest next implementation increment (M3)

Add the two profile names and the `--include` flag to `setup-skills`. Define the membership once, in a data file that a test checks against the closure in section 1. The no-flag default stays `full`. The tests assert the four counts above, and that a second run of the same invocation reports every Skill as current.

This increment changes no default behaviour, so it can ship before any owner decision on M4.

## 5. Remaining dependencies after M2

- **Runtime enforcement of conditional installation.** Sections 1 and 2 state the requirements in text. Nothing at runtime checks whether a required Skill is installed. The skill registry has an `availability.requires_installed_skill` field. Whether the runtime already honours it is unverified and must be checked as the first step of M3.
- **`coding-agent-native-campaign` and the entrypoint profile.** Section 1 includes it, which is an agent proposal. Owner question H covers it.
- **Packaged registry copy.** It lacks three compatibility-only workflows that the canonical copy has (R6). Syncing them changes the installed catalogue, so it waits for M3.
- **Installed copies outside a profile.** A user who installed all 52 keeps them. No profile removes them.

## 6. Owner questions

Each is marked by who framed it. None is an owner decision.

- **G (agent framing).** Keep the maintenance and setup workflows active for the default experience. The consequence is that their Skills belong to `full`, or to an add-on that is not yet defined. The alternative is a liveness change under ADR 0027. This record proposes no liveness change.
- **H (agent framing).** Campaign approval: include `coding-agent-native-campaign` in the entrypoint profile, as section 1 does, or leave it to `full`. The recommendation is to include it, because ADR 0029 places optional Campaign durability in current scope and the runtime's approval discipline depends on this Skill.
- **E (agent framing).** Keep the names `entrypoint`, `full` and `--include`.
- **D (agent framing).** The release in which M4 changes the no-flag default.
- **C (agent framing).** Whether `to-prd` in `docs-implementation-workflow` stays a conditional installation requirement, as M2 states, or moves to the core as a stated exception. This record keeps the conditional requirement.

## 7. Verification

- Static reading and a scripted closure scan at `origin/main` `c088714f`.
- Registry and workflow YAML parsed after the edits. `validate-repo.py` run on the M2 tree (see the pull request).
- Tests that read the edited files were read for their assertions. The edits keep every string they check.
- Unit tests: `NOT_RUN` under the current construction policy.
