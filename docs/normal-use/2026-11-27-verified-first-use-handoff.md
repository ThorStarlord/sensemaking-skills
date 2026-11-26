# Verified first-use handoff (2026-11-27)

**Status:** substantive product possibility developed and realized; external-premise
reconsideration observed.
**Source baseline:** `cdbd399551bd80a24213e3f3d476dccac20b61d5`.
**Possibility synthesis:** `cf57ed488c5c2d1589409bc641632980d522e205`.
**Implementation:** `deecf6a0b60615bf9d73a87ed49343f4d8444003`.

## 1. The observed beneficiary gap

The public `analyze` command was the only advertised repository-analysis verb,
but it only printed harness-specific instructions. It told every user to use
Claude Code, named repository-relative Skill paths that may not exist in an
installed wheel, and promised artifacts without creating them. `analyze` was
listed in `release-v1.0.yaml` as a stable public command, while
`sensemaking-skills release audit` still reported the release authority valid.

The real first-use path was different: install, run `setup-skills`, then invoke
the `using-sensemaking` Skill. Nothing bridged installation to that Skill, and
the install record could be stale without the user knowing.

## 2. Possibility development

A new possibility, `poss:verified-first-use-handoff`, was authored through the
existing synthesis producer. It states that a first-time owner or agent can run
one harness-neutral command that verifies the installed entrypoint Skill,
prepares a handoff artifact for a target repository, and hands off to the single
Skill entrypoint without pretending the CLI analyzes semantics.

Developed elements:

- **Beneficiary:** a first-time repository owner or coding agent.
- **Value hypothesis:** a verified handoff reduces failed installation-to-Skill
  transitions and stale-Skill load, helping a first-time agent reach a
  source-grounded answer faster.
- **Assumptions:** the agent owns semantic control; later sessions consult
  retained knowledge; users may start from CLI help or the first-use guide.
- **Alternatives:** remove the public command; docs-only instructions; a full
  CLI analyzer. The full analyzer would duplicate the Skill and imply semantic
  authority the CLI does not have.
- **Realization condition:** an installed Skill is found and verified, a target
  handoff is written, and a first-time agent can use it without reconstructing
  paths or installation state.
- **Revisit condition:** an independent first-time user reports whether the
  handoff reached a source-grounded answer, or the handoff implementation
  changes: `file:src/sensemaking_skills/first_use.py` or
  `file:src/sensemaking_skills/cli.py`.

## 3. Realization

`semantic handoff` (CLI `sensemaking-skills handoff`) now:

- discovers an installed `using-sensemaking` Skill across the declared harness
  roots, or accepts `--skill-path`;
- fails closed if no copy exists or multiple copies are ambiguous without
  `--harness`, `--scope` or `--skill-path`;
- compares the installed tree with the packaged/source Skill and the install
  record, reporting `CURRENT_WITH_PACKAGE_SOURCE`, `CURRENT_AS_INSTALLED`,
  `DIFFERS_FROM_PACKAGE_SOURCE`, `LOCAL_CHANGES_OR_STALE` or `UNRECORDED`;
- inventories the target repository's top-level paths, entry documents,
  manifests and `.sensemaking/knowledge` presence without reading file
  contents;
- writes `handoff.json` and `handoff.md` with actual paths and a prompt-only
  agent instruction;
- reports `analysis_performed: false`, `semantic_truth_established: false` and
  `action_authorized: false`.

`analyze` remains a compatibility alias with the same options. The Version 1.0
command surface is preserved; `handoff` is additive.

## 4. Authentic use

Run on this repository with `--skill-path skills/using-sensemaking` relative to
the source checkout:

- `currency: CURRENT_WITH_PACKAGE_SOURCE`;
- target inventory included `README.md`, `GETTING_STARTED.md`, `STATUS.md`,
  `AGENTS.md`, `CLAUDE.md`, `CONTEXT.md`, the product strategy and the docs
  entry point;
- `handoff.json` and `handoff.md` were written;
- the prompt named the actual Skill path, target path, output directory and
  question;
- `analysis_performed`, `semantic_truth_established` and `action_authorized`
  were all `false`.

The first run against the user-level generic install reported
`LOCAL_CHANGES_OR_STALE` even though the copied content was current, because
the install record's tree digest was older than an out-of-band sync. The
implementation now compares the installed tree with the packaged/source Skill
first, and reports `CURRENT_WITH_PACKAGE_SOURCE` when they match. The stale
record remains visible; it no longer produces a false stale warning.

The compatibility alias `analyze` produced the same handoff and printed a
stderr note that it does not analyze semantics. A missing `--skill-path` failed
closed.

## 5. External-premise reconsideration

Review from the synthesis commit `cf57ed48` to the implementation commit
`deecf6a0`, using `workspace-review-context --include-candidates`:

- `poss:verified-first-use-handoff` -> `FIRED`
  - `file:src/sensemaking_skills/first_use.py` -> `CHANGED_PATH`
  - `file:src/sensemaking_skills/cli.py` -> `CHANGED_PATH`
- 11 other authored conditions remained `NOT_ASSESSED`
- coverage `PARTIAL`; no automatic disposition change

This is the first structured reconsideration firing on an external product
premise rather than on the reconsideration evaluator itself. The firing
confirmed that the implementation changed the files named by the condition. It
did not by itself prove that the handoff improves a first-time agent's answer.

## 6. Fresh-context first use

A fresh-context consumer received the generated handoff prompt and the target
question: "How does the review context relate changed paths to reviewed
knowledge?" It manually read the installed `using-sensemaking` `SKILL.md`,
followed its source-grounded method, and returned a 300-600 word answer with
source paths. The answer correctly described BASE-only knowledge, changed path
names, per-path fingerprint overlap, whole-diff overlap and the optional
candidate/reconsideration surfaces.

Observed friction:

- the handoff paths were sufficient to start, but the prompt named no entry
  documents or source entry points;
- "review context" was ambiguous and had to be resolved from the CLI/docs;
- the handoff's JSON contained the target HEAD, but the prompt did not pin it;
- the consumer was read-only and therefore did not create the session receipt
  the Skill normally asks for;
- the consumer read the Skill file manually; it did not establish host-native
  Skill loading.

The prompt now includes the target revision, entry documents, manifests,
top-level paths, an instruction to resolve ambiguous product terms from the
named sources, and a write-scope reminder. The implementation remains
`PARTIALLY_IMPLEMENTED`: one same-agent fresh context is not independent user
benefit or a controlled comparison.

## 7. Product versus model

**Product:** harness-root discovery, install-record and package-source
comparison, fail-closed ambiguity handling, bounded target inventory,
path-validated handoff files and a compatibility alias.

**Model:** selected the first-use gap, authored the possibility, implemented
the bridge, interpreted the fired condition and kept the realization partial
pending independent use. The CLI did not analyze the repository or decide what
the agent should do.

## 8. Claim ceiling

| Level | Status |
| --- | --- |
| Functional handoff command and compatibility alias | Observed |
| Verified installed-Skill currency comparison | Observed on this host |
| Handoff written with real target/Skill paths | Observed |
| External-premise structured condition fired | Observed |
| Fresh-context first-use answer | OBSERVED (one same-agent fresh context) |
| Host-native Skill loading | NOT ASSESSED |
| Independent user benefit or answer-quality improvement | NOT ESTABLISHED |
| Comparative cognitive benefit | NOT ESTABLISHED |
| Longitudinal development | NOT ESTABLISHED |

## 9. Continuation

The possibility remains `PARTIALLY_IMPLEMENTED` until a first-time agent uses
the handoff on a real task and the result is observed. Do not expand the
command into a semantic analyzer or remove the compatibility surface. The next
warranted use is a fresh-context consumer with the generated handoff; if the
consumer succeeds without the handoff, record that the bridge was unnecessary
for that user.
