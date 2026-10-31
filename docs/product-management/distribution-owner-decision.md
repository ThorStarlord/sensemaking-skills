# Product Management distribution: owner decision

**Status:** owner-selected 2026-10-31 `[owner: 2026-10-31]`. This is an owner decision record, not an ADR. It amends no accepted ADR and changes no installer, release contract, manifest or Skill. It removes nothing.

**Baseline:** `origin/main` `39718ecb`.

**Companion:** [distribution-reconciliation.md](distribution-reconciliation.md) defines the dependency-complete core profile, PM opt-in behavior, a compatibility-preserving migration path and the downstream touchpoint register.

**Source:** the private decision packet of 2026-10-31 (a Claude Docs document, not shared). Its evidence and limits are carried forward in section 5.

## 1. Decision

The owner selected **Disposition 2**:

> Retain Product Management as a supported, specialized, opt-in domain while making ontology-grounded repository understanding the default Sensemaking experience.

The owner also stated these points, which bind the reconciliation:

- ADR 0028 remains accepted. This decision governs how PM is distributed and made visible, relative to ADRs 0029, 0031 and 0034. It does not retire PM capabilities.
- It is not removing Product Management. It gives PM an appropriate place in the product.
- It is not mechanical qualification and not native-harness qualification. It is a precisely bounded support promise.
- A focused default is the more coherent expression of the product's identity. ADR 0034 B says ordinary users need to know only `using-sensemaking` (`docs/adr/0034-ontology-first-adaptive-sensemaking.md`, line 26).

Not decided here: installer defaults, Skill removal and release publication. Each follows as a separately authorized increment, sequenced in the companion.

## 2. Sub-decision A: what "supported" promises

**Owner ruling:** distinguish two levels, and never let one stand in for the other.

| Level | Meaning | Evidence it needs | Claimed now |
| --- | --- | --- | --- |
| Repository-level mechanical support | The Skill has a manifest declaring its responsibility, outputs and repository mutation, and repository validators check it. | Manifest, validators, migration matrix | Yes, for the 38 Skills in the release tier's `supported` list |
| Native-harness support | The Skill is discovered and invoked in a named harness (Claude Code, Codex or OpenCode) and is shown useful there. | Preserved evidence from an actual supported harness (ADR 0028, line 72) | No |

Manifest-backed qualification does not establish actual invocation or usefulness in Claude Code, Codex or OpenCode.

**Consequence for wording.** `docs/release-v1.0-contract.md` should define `supported` as repository-level mechanical support and state that native-harness support is not claimed. Under ADR 0028's ladder, the 27 PM Skills are `REPOSITORY_QUALIFIED`, with native and portability qualification pending.

## 3. Sub-decision B: a public promise for `using-sensemaking`

**Owner ruling:** `using-sensemaking` should carry an explicit, bounded public-entrypoint promise. That promise is not native-harness qualification. It is not forced into an artifact-oriented support tier until the contract is reconciled.

**Proposed bounded scope**, for the owner to confirm in the wording step:

- **Promised:** `using-sensemaking` is the single public entrypoint for repository understanding. It states a procedure, composition rules and stop conditions, and it composes specialists under the active agent's judgment.
- **Not promised:** host discovery; native invocation in any harness; the quality or truth of any specialist's output; automatic selection by machinery, which ADR 0029 excludes.
- **Classification:** the Skill produces no single artifact, so the release contract needs a non-artifact entrypoint classification. The exact field is a wording decision for the contract step.

## 4. What this record does not decide

- Installer behavior. The selector and default membership are specified in the companion. Changing the default is a separate owner decision, milestone M4.
- Whether an ADR should record the distribution change. If the owner wants ADR-form authority, the owner authors that ADR.
- Three open questions, listed in companion section 6: how engineering workflows that name `to-prd` or `discovery` are gated; whether to accept the controller fallback for experiment design; and the profile and flag names.

## 5. Evidence and limits carried from the packet

Carried forward unchanged:

- Static reading of `origin/main` `39718ecb`. The remote head was confirmed with `git ls-remote`. Nothing was fetched into the primary checkout.
- No tests or validators were run. Read-only scope and the current construction policy both apply.
- No host evidence. What a host lists or invokes was not observed for any Skill.
- No usage data and no user counts.
- PM content quality was not assessed beyond manifests, the migration matrix and validator names.
- ADR wording was read as text. Where an interpretation matters, it is labelled. ADR 0029 admits PM only through its generic lines on bounded capability discovery and optional Campaign durability. That reading is an interpretation, and the owner should confirm it.
- Installed user-level Skill copies on the author's machine were not compared.
- The recommendation rests on identity and claim policy, not observed harm. If the owner treats broad default availability as a feature, disposition 1 with the consistency fixes is the honest alternative.

Corrections and additions found while preparing this record. The packet did not contain these:

- **Six** registry ids name unshipped Skills, not five: `prd`, `triage`, `tdd`, `ui-brief`, `ui-flow` and `ui-screen-spec`. `prd` is marked `status: deprecated` in `skills/workflow-planner/references/skill-registry.yaml` (line 225).
- Two capability-registry entries name unshipped Skills: `triage` (`src/sensemaking_skills/defaults/capability-registry.yaml`, line 470) and `tdd` (line 482).
- Eight of 23 workflows in `skills/workflow-planner/references/workflow-registry.yaml` name an unshipped Skill.
- The two copies of the workflow registry differ. The skills copy has 23 workflows. The packaged copy at `src/sensemaking_skills/defaults/` has 20 and lacks `artifact-reconciliation`, `architecture-implementation-workflow` and `architectural-review-planning-workflow`. The loader reads the packaged copy (`src/sensemaking_skills/registry.py`, lines 88-100).
- The skill registry's ecosystems omit `using-sensemaking` and `coding-agent-native-campaign`. It also places `to-prd`, a PM Skill under the release tier, in the `drafting` group.
- The catalogue's section 5 PM table lists `to-issues`. That Skill is internal, and it has no PM manifest.
- `docs/skill-catalogue.md` line 7 says the repository ships 51 Skills. Its 52 Skills are the count the release tier uses.

## 6. Relation to S5

S5 asks whether retained repository knowledge changes later decisions. This decision does not depend on S5 evidence and does not claim it. If sub-decision A(ii), native-harness support, were ever chosen, native-harness evidence would be a separate qualification, not S5.

## 7. Persistence and authority

- This record and the companion are committed on branch `claude/pm-distribution-disposition-2`, in the worktree `H:/GithubRepositories/smk-pm-distribution`. They are local. Nothing is pushed, and no pull request is open.
- This supersedes the packet's persistence statement, which said nothing was in the repository. The packet itself remains private.
- Installer code, Skill files, registries, the release contract and ADRs are unchanged on this branch.
