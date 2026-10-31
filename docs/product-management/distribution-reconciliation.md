# PM distribution: dependency analysis, migration path and touchpoints

**Status:** planning record. It changes no behavior. Companion to [distribution-owner-decision.md](distribution-owner-decision.md), which records the owner's selection of Disposition 2 and the authority level of each item.

**Baseline:** `origin/main` `39718ecb`. Line references are to that revision. Bare Skill paths such as `using-sensemaking/SKILL.md` are relative to `skills/`.

**Authority:** the milestone path, the candidate profiles and the classifications below are agent proposals. They are not owner decisions unless the owner decision record says so.

## 1. Scope

**In scope:** the dependency analysis the owner decision needs, a migration path with compatibility guarantees, and a register of downstream touchpoints.

**Out of scope:** installer code, Skill edits, registry edits, release-contract edits, ADR changes, Skill removal and release publication. Each is a later increment with its own authority.

## 2. Core membership and dependency analysis

### 2.1 Non-PM membership

The non-PM set is the **25 Skills** in the release tier: the front door (1), the supported engineering Skills (11) and the internal Skills (13). Its PM complement is the 27 Skills in `skill-manifests/pm/`. Together they make 52.

This record does not decide which of the 25 belong in the default install. That is the subject of the profile analysis in the next milestone. The table below only states what each Skill is reached through.

| Skill | Release tier | Reached through |
| --- | --- | --- |
| `using-sensemaking` | front door (internal) | Entrypoint (ADR 0034 B) |
| `repo-sensemaker` | supported | Controller row for repository orientation; `docs-contract-reconciliation` workflow |
| `strategic-repository-analysis` | supported | Controller rows for exploration and construction paths; path references from `repo-sensemaker` and `repository-semantic-steward` |
| `strategic-repository-reconciliation` | supported | Controller row for reconsideration |
| `multi-repository-strategic-analysis` | supported | Controller row, used only for an explicit repository set |
| `external-evidence-packet` | supported | Controller row for decision-changing external evidence |
| `owner-decision-capsule` | supported | Controller row for owner-reserved choices |
| `thesis-review-packet` | supported | Controller text routes `THESIS_REVIEW` here |
| `architectural-review` | supported | Controller row for adversarial challenge (see E-1) |
| `change-impact-analysis` | supported | Named in `using-sensemaking/references/guided-entry-v1.md` |
| `output-reconciler` | supported | Controller row for completed-work claims |
| `repair-verifier` | supported | Controller row for repaired findings |
| `repository-semantic-steward` | internal | Controller row for semantic foundation; path references from `using-sensemaking` |
| `strategic-sensemaking-loop` | internal | Controller row for cross-session continuation; path reference from `using-sensemaking` (ADR 0034 line 54 makes it an internal continuation) |
| `workflow-planner` | internal | Contracts and registries that core Skills read by path |
| `problem-framer` | internal | Controller row for problem framing |
| `unknowns-mapper` | internal | Controller row for unknowns that block a decision |
| `sensemaking-docs-reconciler` | internal | Controller row for docs and implementation that disagree |
| `handoff` | internal | Final step of several active workflows |
| `docs-aligner` | internal | `docs-architecture` workflow; named in `repo-sensemaker` only as an example |
| `to-issues` | internal | Compatibility-only workflows; named in `repo-sensemaker` evidence rules as an example consumer |
| `skill-maintainer` | internal | `skill-maintenance-loop`, `skill-evaluation-workflow` |
| `usage-researcher` | internal | `skill-evaluation-workflow` |
| `setup-sensemaking-skills` | internal | `setup-sensemaking-repo` workflow; ADR 0034 makes setup optional |
| `coding-agent-native-campaign` | internal | Campaign approval discipline. `src/sensemaking_skills/exploratory_execution/conversation_approval.py` states that the discipline is enforced by the coding agent in conversation, per that Skill, and that the runtime cannot see the transcript. No Skill names it. |

### 2.2 Reported PM dependencies, with liveness

Liveness is read from `skills/workflow-planner/references/workflow-liveness.yaml` (ADR 0027). A `compatibility_only` workflow is not eligible for current recommendation, selection or execution.

| Edge | Location | Kind | Liveness | Necessity | Compatibility consequence if PM is absent |
| --- | --- | --- | --- | --- | --- |
| E-1 `pre-mortem` | `using-sensemaking/SKILL.md` line 430; `using-sensemaking/references/adaptive-skill-composition-v1.md` line 23 | Named owner in the controller's adversarial-challenge row, with no fallback | Live | Optional second lens. `architectural-review` is also named as owner. | The controller would name an uninstalled Skill. Needs conditional wording. |
| E-2 `experiment-design` | `using-sensemaking/references/experiment-economy-v1.md` lines 65-69 | Named owner once experiment warrant exists, with no fallback | Live when experiment warrant exists | Specialist. The reference states the design criteria itself. | The controller would name an uninstalled Skill. Needs a stated fallback. |
| E-3 `discovery` | `full-local-sensemaking` workflow, step 3-conditional | Conditional step, inserted only when `unknowns_map.research_needed == true` | Active | Conditional. The false branch skips the step. | The true branch has no installed executor. Needs an explicit fallback. |
| E-4 `to-prd` | `docs-implementation-workflow`, step 2 | Unconditional step producing `prd` | Active | Required for that workflow's output | The workflow cannot complete. Needs a conditional installation requirement. |
| E-5 `to-prd`, `discovery`, `triage`, `tdd`, `prd` | `implementation-workflow`, `experimental-autonomous-sprint`, `architecture-implementation-workflow`, `product-to-issues`, `product-discovery-sprint`, `product-strategy-sprint`, `product-autonomous-sprint`, `product-implementation-workflow`, `ui-*` workflows | Workflow steps | `compatibility_only` in the canonical overlay | Not eligible for current recommendation | None while compatibility-only. Would become a dependency if reactivated. |
| E-6 PM Skills reach `using-sensemaking` | `discovery`, `experiment-design`, `hypothesis`, `lean-canvas`, `pricing` reference `experiment-economy-v1.md` | Path reference from PM to core | Always satisfied | Required by PM, provided by the controller | None. The controller is in every profile. |
| E-7 PM Skills name each other | `to-prd` names `pre-mortem`, `user-stories` and `acceptance-criteria` | Internal to PM | Always satisfied within the PM set | Within PM | None |
| E-8 example mentions | `repo-sensemaker/references/evidence-rules.md` line 50 names `to-prd` and `to-issues` as example consumers; `repo-sensemaker/SKILL.md` line 173 uses "discovery/research" as a phrase | Example or prose | Not a dependency | None | None |
| E-9 registry status notes | `skill-registry.yaml` status notes on PM entries | Historical pointers to `skills/<name>/` | Not a dependency | None | Dangling pointers in a partial install. No runtime effect. |
| E-10 CLI vocabulary | `using-sensemaking/references/golden-paths-v1.md`, "strategy inspect" | The `sensemaking-skills strategy` CLI group (`src/sensemaking_skills/strategy_cli.py`) | Not a dependency | None | None |

### 2.3 Consequences of the liveness reading

- **Active PM-dependent workflows are two.** `docs-implementation-workflow` (E-4) and `full-local-sensemaking` (E-3). All other PM-referencing workflows are `compatibility_only`.
- **The eight workflows naming unshipped identities are compatibility-only.** So the unshipped references affect no current recommendation. They are reference hygiene, not a distribution blocker.
- **The packaged liveness overlay agrees** on every workflow it lists. Its three missing workflows (`artifact-reconciliation`, `architecture-implementation-workflow`, `architectural-review-planning-workflow`) are compatibility-only in the canonical overlay and absent from the packaged catalog.

### 2.4 Required resolutions

- **R1, composition row for adversarial challenge (E-1).** Keep `architectural-review` as the controller's owner. Mark `pre-mortem` as an optional specialist that applies when the PM domain pack is installed. State what the controller records when it is absent. Edit both locations.
- **R2, experiment-design fallback (E-2).** When experiment warrant exists and `experiment-design` is absent, the controller applies the design criteria already stated in `experiment-economy-v1.md` and states the design's claim ceiling. `experiment-design` applies when installed.
- **R3, the two active PM-dependent workflows (E-3, E-4).** E-3 gets an explicit fallback on its false-to-true branch. E-4 gets a stated conditional installation requirement in its step description. Enforcement of that requirement at runtime is not in this milestone set (section 4, remaining dependencies).
- **R4, compatibility-only references.** Leave them. They are not eligible and not material to distribution.
- **R5, registry grouping.** Add `using-sensemaking` to the `core` ecosystem. Move `to-prd` from `drafting` to `product`. Add a header note that `deprecated` on PM entries refers to legacy invocation metadata, not to Skill support.
- **R6, two workflow-registry copies.** The packaged copy lacks three workflows, all compatibility-only. Syncing them would change the packaged catalog. That is a behavior change for the installed CLI, so it waits for the profile contract.

### 2.5 Closure rule for a later check

Walk the named owners, path references and workflow steps from each member of a profile. A walk that reaches a PM Skill passes only if the edge is listed in section 2.2 with its resolution in place. This record specifies the check. It does not build it.

## 3. PM opt-in behavior

**Membership.** The 27 PM Skill trees, the same set as the release tier's PM entries and `skill-manifests/pm/`.

**Closure.** The PM set needs no engineering Skill beyond the controller.

- All 27 PM manifests declare empty `consumes`. No PM artifact depends on an engineering artifact.
- Five PM Skills reach `using-sensemaking` by path (E-6). The controller is in every profile, so this edge is always satisfied.
- `to-prd`'s reference template names `to-issues` as prose (E-8).

**Selector (proposed; not final).** Milestone M3 decides the interface. The candidates and their comparison are in the profile contract. Either way the selector adds the 27 PM trees and never removes one.

**Default.** Before M4 the default remains all 52 Skills, which is today's behavior. From M4 the default is a dependency-complete profile. Its membership is a later proposal.

**When PM is absent.** The controller must not name an absent PM Skill as available. If a PM specialist would be warranted, the controller records that it was not installed and uses the fallback (R1, R2). This behavior is proposed, not yet stated anywhere.

**Visibility.** Installation, not harness visibility, makes PM opt-in. Host discovery was not observed, so the docs must not promise what a harness will list.

**Release wording.** PM is a supported domain pack and opt-in. The `supported` wording follows sub-decision A.

## 4. Compatibility-preserving migration path

| Milestone | Change | Installer behavior | Reversible | Authority |
| --- | --- | --- | --- | --- |
| M0 | This record, and the corrections to it | None | Yes | Owner selection recorded |
| M1 | Wording and drift fixes: the `supported` definition (A), the entrypoint statement (B), the front-door list, the count of 52, the release scope text, the registry grouping and header note (R5), the README note | None | Yes, by git revert | Owner ratifies the wording for A and B. The rest needs maintainer review. |
| M2 | Conditional wording for E-1 and E-2 (R1, R2), the E-3 fallback and E-4 requirement (R3), and the profile contract | None | Yes | Owner accepts the fallback rules and the profile contract |
| M3 | Selector on `setup-skills` (`--profile entrypoint|full`, `--include product-management`), installation availability reporting, and the profile validator. The default stays all 52. | Adds options and output lines; the no-flag installed set is unchanged | Yes, by reverting the option | Implemented in PR #684 (merged `b89dcbab`) under owner decisions E, G and H |
| M4 | The default becomes the dependency-complete profile. The full set stays available by name. The release note announces the change one release ahead. | Scripted default installs receive fewer Skills. Existing installed trees are not touched. | Yes, by reverting the default | Not implemented. Owner decision D: reconsider for the first suitable release after an M3-bearing release has announced the change, through a separate rollout decision. |

**Not in this path:** removing any PM Skill. That requires an owner-authored ADR superseding ADR 0028 first. Disposition 2 does not include it.

**Compatibility guarantees:**

- No milestone deletes an installed Skill. `copy_skill` replaces a same-named tree only under `--force` (`src/sensemaking_skills/setup_skills.py` lines 181-191). The installer deletes nothing it does not package.
- Divergent installed trees still require `--force`, unchanged.
- Before M4, every command produces today's output.
- A user who installed all 52 keeps them after M4. Re-running a default install does not remove PM trees.
- The wheel is unchanged in every milestone. `setup.py` lines 29-35 still package all of `skills/`. Any selector filters at install time, not at packaging time.

**Ordering constraint.** M4 must not come before M2. A reduced default that still names an absent PM Skill as available would leave dangling references.

**Remaining dependency after M2.** Conditional installation requirements (E-3, E-4) are stated in text. Nothing at runtime yet checks whether the required Skill is installed. The `availability.requires_installed_skill` field exists in `skill-registry.yaml`. Whether the runtime already honours it is unverified and should be checked before M3.

## 5. Downstream reconciliation register

Class: DOC (documentation), CONTRACT (release contract), SKILL (Skill instruction), REG (registry data), CODE (installer). Owner input refers to section 6.

| # | Touchpoint | Current state | Required change | Class | Milestone | Owner input |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | `release-v1.0.yaml` line 7 | Scope says "mechanically qualified engineering Skills", while 27 PM Skills sit in `supported` | Scope names the PM domain pack as repository-qualified and opt-in | CONTRACT | M1 | A |
| 2 | `docs/release-v1.0-contract.md` | Does not define `supported`, and does not state the entrypoint promise | Define `supported` as repository-level, state native-harness support as not claimed, add a bounded entrypoint statement | CONTRACT | M1 | A, B |
| 3 | `release-v1.0.yaml` line 89 (`internal`) | Lists `using-sensemaking` as internal | No change to the tier. The entrypoint statement sits in the contract doc, so the artifact tier and the public promise stay separate. | CONTRACT | M1 | B |
| 4 | `docs/public-surface-v1.0.md` lines 96-99 | The front door lists `strategic-sensemaking-loop` | Remove it from the front door. ADR 0034 line 54 makes it an internal continuation. | DOC | M1 | None |
| 5 | `docs/skill-catalogue.md` line 7 | "ships 51 Skills" | 52 | DOC | M1 | None |
| 6 | `docs/skill-catalogue.md` section 5 table | Lists `to-issues` under PM | Remove it. The sentence about it needs rewriting too. | DOC | M1 | None |
| 7 | `docs/skill-catalogue.md` section 5 intro | "shipped for explicit product-management work" | Align with the opt-in description | DOC | M3 | None |
| 8 | `README.md`, "The installed product includes" list | No PM item | Add a note that the PM domain pack is supported and repository-qualified, and that opt-in selection is planned | DOC | M1 | None |
| 9 | `GETTING_STARTED.md` line 74 | Already states that setup is optional and never a prerequisite | No change | None | None | None |
| 10 | `GETTING_STARTED.md` install commands | No selector | Document the selector | DOC | M3 | None |
| 11 | `docs/strategic-candidate-directions.md` line 810 | "opt-in surfaces". Non-authoritative. | No change. Note only. | None | None | None |
| 12 | `skill-registry.yaml` ecosystems | `using-sensemaking` absent from every ecosystem; `to-prd` sits in `drafting` | R5: add the entrypoint to `core`, move `to-prd` to `product` | REG | M1 | None |
| 13 | `skill-registry.yaml` header | No explanation of `deprecated` on PM entries | Add a header note that the status refers to legacy invocation metadata, not Skill support | REG | M1 | None |
| 14 | `skill-registry.yaml` unshipped identities (`prd`, `triage`, `tdd`, `ui-brief`, `ui-flow`, `ui-screen-spec`) | Already marked `proposed` or `deprecated` with notes | No change. A test asserts the capability entries for `triage` and `tdd`. | None | None | None |
| 15 | Compatibility-only workflows naming unshipped or PM identities (E-5) | Not eligible for current recommendation | No change (R4) | None | None | None |
| 16 | `skill-registry.yaml` PM status notes (E-9) | Historical pointers | No change | None | None | None |
| 17 | `using-sensemaking/SKILL.md` line 430 and `adaptive-skill-composition-v1.md` line 23 | `pre-mortem` named as owner, with no fallback | R1 | SKILL | M2 | Accept the fallback |
| 18 | `using-sensemaking/references/experiment-economy-v1.md` lines 65-69 | `experiment-design` named as owner, with no fallback | R2 | SKILL | M2 | Accept the fallback |
| 19 | `full-local-sensemaking` conditional step and `docs-implementation-workflow` step 2, in both workflow-registry copies | E-3 and E-4 | R3: fallback text and conditional requirement | REG | M2 | Accept the requirement |
| 20 | Workflow-registry copies | The packaged copy lacks three compatibility-only workflows | R6, deferred to the profile contract | REG | M3 | None |
| 21 | `scripts/validate-repo.py` | Not checked for how it treats registry status values | Check before M1 merges registry edits | DOC | M1 | None |
| 22 | `src/sensemaking_skills/setup_skills.py` lines 124-132 and 316-325 | Installs every packaged Skill. No selector. | Add the selector | CODE | M3 | None |
| 23 | `src/sensemaking_skills/cli.py` lines 387-470 | `setup-skills` has no selector option | Add the selector | CODE | M3 | None |
| 24 | `setup.py` lines 29-35 | Packages all of `skills/` | No change | None | None | None |
| 25 | ADRs 0028, 0029, 0031, 0034 | Unchanged | No change. Optional: an owner-authored ADR clarifying ADR 0029's reading of PM. | None | None | Optional |
| 26 | `skill-manifests/pm/`, `domain-packs/product-management.yaml`, the six `validate-pm-*` scripts, the capability migration matrix | Unchanged | No change | None | None | None |

## 6. Open questions

Status after M3. Owner decisions are recorded in [distribution-owner-decision.md](distribution-owner-decision.md) section 8.

- **C, decided.** `to-prd` stays in the PM add-on, and `docs-implementation-workflow` requires it explicitly. Implemented in the workflow text and the M3 availability check.
- **R2, implemented in M2 under the owner's direction to preserve fallbacks.** No separate acceptance of the experiment-design fallback is recorded.
- **D, decided in part.** M4 is not part of M3 or RC5. The rollout decision, meaning which release announces the change, remains open.
- **E, decided.** `--profile entrypoint|full` and `--include product-management`. Implemented in M3.
- **F, not addressed by the owner.** `to-issues` is excluded from the entrypoint profile and included under `full`. It is not part of the PM add-on. Low priority.
- **G and H, decided.** Liveness preserved. `coding-agent-native-campaign` excluded from `entrypoint`, available under `full`.

## 7. Verification and limits

- **Method.** Static reading at `39718ecb`. Named owners, path references and workflow steps were extracted by script. `skill-registry.yaml`, `workflow-registry.yaml` and `workflow-liveness.yaml` were parsed as YAML. The scan script lives in the session scratchpad and is not committed.
- **Prose review.** Prose mentions of PM names were reviewed for the PM Skills. They were not reviewed line by line for all 25 non-PM Skills.
- **Tests.** Tests that read the registries and documents were read for the assertions they make. They were not run. Under the current construction policy, local unit tests are not run; that result is `NOT_RUN`.
- **Not observed:** host discovery, invocation, and usage.
- **Not compared:** installed user-level Skill copies on the author's machine.

## 8. Relation to S5

S5 asks whether retained repository knowledge changes later decisions. This reconciliation does not depend on S5 and does not claim it. Native-harness evidence, if sub-decision A(ii) were chosen, would be a separate qualification.
