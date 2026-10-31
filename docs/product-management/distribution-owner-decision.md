# Product Management distribution: owner decision

**Status:** owner selection of Disposition 2 recorded 2026-10-31. This is a decision record, not an ADR. It amends no accepted ADR and changes no installer, release contract, manifest or Skill. It removes nothing.

**Baseline:** `origin/main` `39718ecb`.

**Companion:** [distribution-reconciliation.md](distribution-reconciliation.md) covers the dependency analysis, the migration milestones and the touchpoint register.

**Source:** the owner's message of 2026-10-31 and the private decision packet of the same date (a Claude Docs document, not shared). The packet's evidence and limits are carried forward in section 5.

## 0. Authority levels

Each item below is labelled by who decided it. Only the first row is an explicit owner selection. Nothing here is a ratified ADR.

| Item | Level | Basis |
| --- | --- | --- |
| Disposition 2 is the intended product direction | Owner selection, explicit | Owner message, 2026-10-31 |
| Sub-decision A: support levels must be distinguished | Owner direction, explicit. The contract wording is not yet ratified. | Owner message |
| Sub-decision B: `using-sensemaking` gets a bounded public promise | Owner direction, explicit. The bounds are not yet ratified. | Owner message |
| "Not removing PM; giving it an appropriate place" | Owner statement | Owner message |
| Disposition 2 as the packet's recommendation | Agent recommendation, provisional | Packet |
| Bounded scope of the entrypoint promise; exact release wording | Agent proposal, pending owner ratification | Companion, section 3 |
| Candidate default profile; `--profile` and `--include` names | Agent proposal, pending owner decision | Companion, sections 2 and 6 |

## 1. Decision

The owner selected **Disposition 2**:

> Retain Product Management as a supported, specialized, opt-in domain while making ontology-grounded repository understanding the default Sensemaking experience.

The owner also stated these points. They guide the reconciliation but are not themselves ADR text:

- ADR 0028 remains accepted. This decision governs how PM is distributed and made visible, relative to ADRs 0029, 0031 and 0034. It does not retire PM capabilities.
- It is not removing Product Management. It gives PM an appropriate place in the product.
- It is not mechanical qualification and not native-harness qualification. It is a precisely bounded support promise.
- A focused default is the more coherent expression of the product's identity. ADR 0034 B says ordinary users need to know only `using-sensemaking` (`docs/adr/0034-ontology-first-adaptive-sensemaking.md`, line 26).

Not decided here: installer defaults, Skill removal and release publication. Each follows as a separately authorized increment.

## 2. Sub-decision A: what "supported" promises

**Owner direction:** distinguish repository-level mechanical support from native-harness support. Manifest-backed qualification does not establish actual invocation or usefulness in Claude Code, Codex or OpenCode.

| Level | Meaning | Evidence it needs | Claimed now |
| --- | --- | --- | --- |
| Repository-level mechanical support | The Skill has a manifest declaring its responsibility, outputs and repository mutation, and repository validators check it. | Manifest, validators, migration matrix | Yes, for the 38 Skills in the release tier's `supported` list |
| Native-harness support | The Skill is discovered and invoked in a named harness and shown useful there. | Preserved evidence from an actual supported harness (ADR 0028, line 72) | No |

**Consequence for wording (agent proposal).** The release contract should define `supported` as repository-level mechanical support and state that native-harness support is not claimed. Under ADR 0028's ladder, the 27 PM Skills are `REPOSITORY_QUALIFIED`, with native and portability qualification pending.

## 3. Sub-decision B: a public promise for `using-sensemaking`

**Owner direction:** `using-sensemaking` should carry an explicit, bounded public-entrypoint promise. That promise is not native-harness qualification, and it is not forced into an artifact-oriented support tier before the contract is reconciled.

**Proposed bounds (agent proposal, pending owner ratification):**

- **Promised:** `using-sensemaking` is the single public entrypoint for repository understanding. It states a procedure, composition rules and stop conditions, and it composes specialists under the active agent's judgment.
- **Not promised:** host discovery; native invocation in any harness; the quality or truth of any specialist's output; automatic selection by machinery, which ADR 0029 excludes.
- **Classification:** the Skill produces no single artifact, so the release contract needs a non-artifact entrypoint statement. The exact field is a wording decision for the contract step.

## 4. What this record does not decide

- Installer behavior. The profile contract is specified in the companion. Changing the default is a separate owner decision (milestone M4).
- Whether an ADR should record the distribution change. If the owner wants ADR-form authority, the owner authors that ADR.
- Open questions listed in companion section 6, including how engineering workflows that name `to-prd` are gated.

## 5. Evidence and limits carried from the packet

Carried forward:

- Static reading of `origin/main` `39718ecb`. The remote head was confirmed with `git ls-remote`. Nothing was fetched into the primary checkout.
- No tests or validators were run in the original analysis.
- No host evidence. What a host lists or invokes was not observed for any Skill.
- No usage data and no user counts.
- PM content quality was not assessed beyond manifests, the migration matrix and validator names.
- ADR wording was read as text. ADR 0029 admits PM only through its generic lines on bounded capability discovery and optional Campaign durability. That reading is an interpretation for the owner to confirm.
- Installed user-level Skill copies on the author's machine were not compared.
- The packet's recommendation rests on identity and claim policy, not observed harm. If the owner treats broad default availability as a feature, disposition 1 with the consistency fixes is the honest alternative.

Corrections found while preparing this record. The packet did not have these, or stated them loosely:

- **Six** registry identities name Skills that do not ship: `prd`, `triage`, `tdd`, `ui-brief`, `ui-flow` and `ui-screen-spec`. The packet said five. Each is already marked in `skills/workflow-planner/references/skill-registry.yaml` as `proposed` or `deprecated`, with a status note. They are therefore marked historical identities, not unmarked drift. Two capability-registry entries, `triage` and `tdd`, are asserted unavailable by `tests/campaign_validation/test_campaign_capabilities.py`.
- Eight workflows in the workflow registry name one of those identities. The ADR 0027 liveness overlay marks all eight `compatibility_only`, so none is currently eligible for recommendation.
- The skill registry marks 25 PM entries `status: deprecated`. Their notes say this refers to "wayfinder-era invocation metadata" and that the current implementation lives under `skills/`. The release tier calls the same Skills `supported`. The two words describe different things and need a glossary line.
- The two workflow-registry copies differ. The skills copy has 23 workflows and the packaged copy has 20. The loader always merges the packaged copy first and then merges the target repository's registry over it when one exists (`src/sensemaking_skills/registry.py`, `_load_package_defaults` and `_load_user_registry`).
- The skill registry's ecosystems omit `using-sensemaking` and `coding-agent-native-campaign`. It places `to-prd`, a PM Skill under the release tier, in the `drafting` group.
- The catalogue's section 5 PM table lists `to-issues`. That Skill is internal and has no PM manifest.
- `docs/skill-catalogue.md` line 7 says the repository ships 51 Skills. The release tier counts 52.

## 6. Relation to S5

S5 asks whether retained repository knowledge changes later decisions. This decision does not depend on S5 evidence and does not claim it. If sub-decision A(ii), native-harness support, were ever chosen, native-harness evidence would be a separate qualification.

## 7. Persistence and authority

- This record and the companion are committed on branch `claude/pm-distribution-disposition-2` and are part of the M0 pull request.
- The packet's persistence statement, which said nothing was in the repository, is superseded by this branch. The packet itself remains private.
- Installer code, Skill files, registries, the release contract and ADRs are unchanged by this record.
