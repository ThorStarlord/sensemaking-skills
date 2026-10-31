# PM distribution: core profile, opt-in behavior and migration path

**Status:** planning record. It changes no behavior. Companion to [distribution-owner-decision.md](distribution-owner-decision.md), which records Disposition 2.

**Baseline:** `origin/main` `39718ecb`. Every line reference below is to that revision. Bare Skill paths such as `using-sensemaking/SKILL.md` are relative to `skills/`.

## 1. Scope

**In scope:** the definitions the owner decision needs before any installer change. These are the dependency-complete core profile, PM opt-in behavior, a phased migration path, and a register of downstream touchpoints.

**Out of scope:** installer code, Skill edits, registry edits, release-contract edits, ADR changes, Skill removal and release publication. Each is a later increment with its own authority.

## 2. Dependency-complete core profile

### 2.1 Membership

The core profile is the **25 non-PM Skills** in the release tier. Those are the front door (1), the supported engineering Skills (11) and the internal Skills (13). Its PM complement is the 27 Skills in `skill-manifests/pm/`. Together they make 52.

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
| `strategic-sensemaking-loop` | internal | Controller row for cross-session continuation; path reference from `using-sensemaking` |
| `workflow-planner` | internal | Contracts and registries that core Skills read by path |
| `problem-framer` | internal | Controller row for problem framing |
| `unknowns-mapper` | internal | Controller row for unknowns that block a decision |
| `sensemaking-docs-reconciler` | internal | Controller row for docs and implementation that disagree; `docs-contract-reconciliation` workflow |
| `handoff` | internal | Steps in most core workflows |
| `docs-aligner` | internal | `docs-architecture` workflow |
| `to-issues` | internal | `architecture-implementation-workflow`; the `repo-sensemaker` evidence rules |
| `skill-maintainer` | internal | `skill-maintenance-loop`, `skill-evaluation-workflow` |
| `usage-researcher` | internal | `skill-evaluation-workflow` |
| `setup-sensemaking-skills` | internal | `setup-sensemaking-repo` workflow |
| `coding-agent-native-campaign` | internal | Classification only. No Skill names it. Runtime code and `scripts/README.md` refer to it. |

### 2.2 Edges from the core into PM

The closure check found four dependencies that must be resolved before the default changes. It also found soft mentions that need no change.

| Edge | Location | Kind | Required resolution |
| --- | --- | --- | --- |
| E-1 `pre-mortem` | `using-sensemaking/SKILL.md` line 430; `using-sensemaking/references/adaptive-skill-composition-v1.md` line 23 | Named owner for adversarial challenge, with no fallback | R1 |
| E-2 `experiment-design` | `using-sensemaking/references/experiment-economy-v1.md` lines 65-69 | Named owner once experiment warrant exists, with no fallback | R2 |
| E-3 `discovery` | `full-local-sensemaking` workflow, one step | Workflow step | R3 |
| E-4 `to-prd` | `implementation-workflow`, `experimental-autonomous-sprint`, `docs-implementation-workflow`, `architecture-implementation-workflow`, and the product workflows | Workflow step | R3 |

**Soft mentions, not dependencies, so no change is needed:**

- `repo-sensemaker/references/evidence-rules.md` line 50 names `to-prd` as an example downstream consumer.
- `repo-sensemaker/SKILL.md` line 173 uses "discovery/research" as a phrase.
- The status notes in `skill-registry.yaml` (lines 169-347) name PM paths as historical pointers.
- PM Skills use the word "handoff" for the artifact concept, not for the `handoff` Skill.

**Unshipped references,** independent of the distribution decision. Eight workflows name Skills that do not ship: `prd`, `triage`, `tdd`, `ui-brief`, `ui-flow` and `ui-screen-spec`. These are defects today. They must be fixed in any disposition.

### 2.3 Required resolutions

- **R1, composition row for adversarial challenge (E-1).** Keep `architectural-review` as the core owner. Mark `pre-mortem` as an optional specialist that applies when the PM profile is installed. Edit both locations, `SKILL.md` line 430 and `adaptive-skill-composition-v1.md` line 23.
- **R2, experiment-design fallback (E-2).** When experiment warrant exists and `experiment-design` is absent, the controller applies the design criteria already stated in `experiment-economy-v1.md`. Those criteria are decision discrimination, total cost, minimum sufficient rigor, controls, stop conditions and claim ceiling. The result records its claim ceiling. `experiment-design` applies when installed.
- **R3, workflow steps that name PM Skills (E-3, E-4).** Gate each PM step behind the PM profile. Five of the ten affected workflows are core-named, so this changes engineering workflows. Owner sub-decision C in section 6 chooses between gating and moving `to-prd` into core.
- **R4, unshipped references.** Remove or replace the eight workflow references and fix the registry entries (section 5, rows 13-15). This is needed under every disposition. `prd` already carries a deprecated status note that points to `to-prd`.
- **R5, registry grouping.** The `core` ecosystem should list the 25 core Skills. `using-sensemaking` and `coding-agent-native-campaign` are currently missing from every ecosystem. `to-prd` should move from `drafting` to `product`, matching its release tier.
- **R6, two workflow-registry copies.** Choose one source of truth and sync the packaged copy. The packaged copy is the one the loader reads by default. It has 20 workflows where the skills copy has 23. This must happen before M3.

### 2.4 Closure rule for a later check

Walk the named owners, path references and workflow steps from each core member. A walk that reaches a PM Skill passes only if the edge is listed in section 2.2 and its resolution (R1-R3) is in place. This document specifies the check. It does not build it.

## 3. PM opt-in behavior

**Membership.** The 27 PM Skill trees, the same set as the release tier's PM entries and `skill-manifests/pm/`.

**Closure.** The PM set needs no engineering Skill beyond the core.

- All 27 PM manifests declare empty `consumes`, so no PM artifact depends on an engineering artifact.
- Five PM Skills reach `using-sensemaking` by path, for `references/experiment-economy-v1.md`. They are `discovery`, `experiment-design`, `hypothesis`, `lean-canvas` and `pricing`. The `using-sensemaking` Skill is in the core in every profile, so this edge is always satisfied.
- `to-prd`'s reference template names `to-issues` as prose. `to-issues` is core, so that is satisfied too.

**Selector (proposed; the name is not final).** `setup-skills --domain product-management` adds the 27 PM trees. It never removes a tree. A PM tree already present is treated by the existing `copy_skill` states, so re-running it is idempotent.

**Default.** Before M4, the default remains all 52 Skills, which is today's behavior. From M4, the default is the core profile.

**When PM is absent.** The controller must not name an absent PM Skill as available. If a PM specialist would be warranted, the controller records the gap, for example `specialist not installed`, and uses the core fallback (R1, R2). It reports `NOT_ASSESSED` where no fallback exists. This is a proposed behavior, not one already stated.

**Workflows.** Product-named workflows, and any workflow step that names a PM Skill, run only when the PM profile is present (R3).

**Visibility.** Installation, not harness visibility, makes PM opt-in. Host discovery was not observed, so the docs must say that a PM Skill is opt-in by installation. They must not promise what a harness will list.

**Release wording.** PM is a supported domain pack that is opt-in. The `supported` wording follows sub-decision A.

## 4. Compatibility-preserving migration path

| Milestone | Change | Installer behavior | Reversible | Authority |
| --- | --- | --- | --- | --- |
| M0 | This branch: records only | None | Yes | Owner decision recorded |
| M1 | Wording and drift fixes: the `supported` definition (A), the entrypoint promise (B), front-door lists, the count of 52, the unshipped references (R4), registry grouping (R5), README omission | None | Yes, by git revert | Owner ratifies the wording for A and B. The drift fixes need maintainer review only. |
| M2 | Skill-instruction edits R1 and R2, the workflow gating R3, the copy sync R6, and the closure check specified in 2.4 | None | Yes | Owner accepts the fallback rules (R2) and sub-decision C |
| M3 | Selector `--domain` on `setup-skills`. The default stays all 52. Tests assert the installed set with and without the selector. | Adds an option; the default is unchanged | Yes, by reverting the option | A separate engineering increment. The owner approves that the default stays unchanged. |
| M4 | The default becomes the core profile. `--domain all` restores 52. The release note announces the change one release ahead. | Scripted default installs receive fewer Skills. Existing installed trees are not touched. | Yes, by reverting the default | A separate owner decision on timing |

**Not in this path:** removing any PM Skill. That requires an owner-authored ADR superseding ADR 0028 first. Disposition 2 does not include it.

**Compatibility guarantees:**

- No milestone deletes an installed Skill. `copy_skill` replaces a same-named tree only under `--force` (`src/sensemaking_skills/setup_skills.py` lines 181-191). The installer deletes nothing it does not package.
- Divergent installed trees still require `--force`, unchanged.
- Before M4, every command produces today's output.
- A user who installed all 52 keeps them after M4. Re-running the default install does not remove PM trees.
- The wheel is unchanged in every milestone. `setup.py` lines 29-35 still package all of `skills/`. The selector filters at install time, not at packaging time.

**Ordering constraint.** M4 must not come before M2. A core-only default that still names PM Skills would leave dangling references.

## 5. Downstream reconciliation register

Class: DOC (documentation), CONTRACT (release or registry contract), SKILL (Skill instruction), REG (registry data), CODE (installer). Owner input refers to section 6.

| # | Touchpoint | Current state | Required change | Class | Milestone | Owner input |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | `release-v1.0.yaml` line 7 | Scope says "mechanically qualified engineering Skills", while 27 PM Skills sit in `supported` | Scope names the PM domain pack as supported and opt-in | CONTRACT | M1 | A |
| 2 | `release-v1.0.yaml` line 89 (`internal`) | Lists `using-sensemaking` as internal | Add the entrypoint classification | CONTRACT | M1 | B |
| 3 | `docs/release-v1.0-contract.md` | Does not define `supported` as repository-level | Define it, and state native-harness support as not claimed | CONTRACT | M1 | A, B |
| 4 | `docs/public-surface-v1.0.md` lines 96-99 | Front door lists `strategic-sensemaking-loop` | Keep the front door to `using-sensemaking`, per ADR 0034 | DOC | M1 | Confirm |
| 5 | `docs/skill-catalogue.md` line 7 | "ships 51 Skills" | 52 | DOC | M1 | None |
| 6 | `docs/skill-catalogue.md` lines 87-104 | The PM table lists `to-issues` | Remove `to-issues` from the PM table. It is core. | DOC | M1 | F |
| 7 | `docs/skill-catalogue.md` section 5 intro | "shipped for explicit product-management work" | Align with the opt-in definition in section 3 | DOC | M3 | None |
| 8 | `README.md` line 171 ("installed product includes") | No PM item | Add the PM domain pack as opt-in | DOC | M1 | None |
| 9 | `README.md` line 439 | Mentions the "completed Product Management migration" | Keep. Clarify that it is a domain pack. | DOC | M1 | None |
| 10 | `GETTING_STARTED.md` install commands | No selector | Document `--domain` | DOC | M3 | None |
| 11 | `docs/strategic-candidate-directions.md` line 810 | "opt-in surfaces". Non-authoritative. | No change. Note only. | DOC | None | None |
| 12 | `skill-registry.yaml` ecosystems (from line 4) | Core omits `using-sensemaking` and `coding-agent-native-campaign`; `to-prd` sits in `drafting` | R5 | REG | M1 | None |
| 13 | `skill-registry.yaml` (`prd` at line 225, and `triage`, `tdd`, `ui-brief`, `ui-flow`, `ui-screen-spec`) | Entries for unshipped Skills. `prd` is deprecated. | Remove the entries, or mark them not shipped | REG | M1 | None |
| 14 | `src/sensemaking_skills/defaults/capability-registry.yaml` lines 470 and 482 | Entries for `triage` and `tdd`, which do not ship | Remove or mark them | REG | M1 | None |
| 15 | Workflow registries, 8 workflows | Name unshipped Skills | Fix or remove the references (R4) | REG | M1 | None |
| 16 | Workflow registries, two copies | 23 workflows versus 20 in the packaged copy | R6: one source of truth, synced | REG | M2 | None |
| 17 | `using-sensemaking/SKILL.md` line 430; `adaptive-skill-composition-v1.md` line 23 | `pre-mortem` named as owner, with no fallback | R1 | SKILL | M2 | Accept the fallback |
| 18 | `using-sensemaking/references/experiment-economy-v1.md` lines 65-69 | `experiment-design` named as owner, with no fallback | R2 | SKILL | M2 | Accept the fallback |
| 19 | Workflow steps naming `to-prd` or `discovery` (10 workflows) | Core-named workflows depend on PM Skills | R3 | REG | M2 | C |
| 20 | `scripts/validate-repo.py` | Not checked. Whether it validates registry ids against the shipped set is unknown. | Check before M1 | DOC | M1 | None |
| 21 | `src/sensemaking_skills/setup_skills.py` lines 124-132 and 316-325 | Installs every packaged Skill. No selector. | Add `--domain` | CODE | M3 | None |
| 22 | `src/sensemaking_skills/cli.py` lines 387-470 | `setup-skills` has no domain option | Add `--domain` | CODE | M3 | None |
| 23 | `setup.py` lines 29-35 | Packages all of `skills/` | No change | None | None | None |
| 24 | ADRs 0028, 0029, 0031, 0034 | Unchanged | No change. Optional: an owner-authored ADR clarifying ADR 0029's PM reading. | None | None | Optional |
| 25 | `skill-manifests/pm/`, `domain-packs/product-management.yaml`, the six `validate-pm-*` scripts, the capability migration matrix | Unchanged | No change | None | None | None |

## 6. Open owner questions

- **C.** Engineering workflows name `to-prd`: `implementation-workflow`, `experimental-autonomous-sprint`, `docs-implementation-workflow` and `architecture-implementation-workflow`. `full-local-sensemaking` names `discovery`. Either gate those PM steps behind the PM profile, or move `to-prd` into core as a stated exception. **Recommendation:** gate. Gating keeps Disposition 2 intact.
- **R2 acceptance.** Accept the controller fallback for experiment design. The alternative is to promote `experiment-design` into core. That is not recommended.
- **D.** The release in which M4 takes effect.
- **E.** Profile and flag names. **Recommendation:** `--domain product-management` for the PM domain, `--domain all` for the full set, and the core profile as the default after M4.
- **F.** Confirm that `to-issues` is core. This record classifies it as core: it is an internal engineering Skill, used by an engineering workflow. The catalogue's section 5 lists it under PM.

## 7. Verification and limits

- **Method.** Static reading at `39718ecb`. Named owners and path references were extracted by a script over `skills/`. `skill-registry.yaml` and `workflow-registry.yaml` were parsed as YAML, and the counts were recomputed from them. The scan script is in the session scratchpad and is not committed.
- **Prose review.** Prose mentions of PM names were reviewed by hand for the PM Skills. They were not reviewed for every line of all 25 core Skills.
- **Not run:** tests, validators and the installer. Under the current construction policy, no local unit or synthetic tests were run; the result is `NOT_RUN`.
- **Not observed:** host discovery, invocation, and usage.
- **Not compared:** the installed user-level Skill copies on the author's machine.

## 8. Relation to S5

S5 asks whether retained repository knowledge changes later decisions. This reconciliation does not depend on S5 and does not claim it. Native-harness evidence, if sub-decision A(ii) were chosen, would be a separate qualification.
