# Repository Grounding Plan

**Status:** owner-directed plan (2026-10-12); Phase 0 not started  
**Direction and rationale:** [`research/repository-grounding-direction-2026-10.md`](research/repository-grounding-direction-2026-10.md)  
**Level-4 authority:** `docs/product-strategy.md` changes only through Phase 0
below, per `docs/product-thesis-revision.md`.

## 1. Goal

Make full delegation practical by giving the coding agent the knowledge about a
target repository that it cannot recover from the code, and by turning every
owner answer into durable context so the same question is never asked twice.

**Outcome that counts as success:** on a real target repository, an agent with
the Grounding Pack completes real tasks with fewer owner questions and less
rework than the same agent without it, and owner questions per task go down
over successive tasks.

## 2. Non-goals

- No repository ontology of code structure (module lists, class taxonomies,
  file maps). The agent derives these on demand.
- No new runtime, router, planner, scoring, or evaluation harness.
- No validator unless a named consumer reads the field it checks (see
  `CLAUDE.md`, "A validator rule must trace to a real consumer").
- No new plan documents between phases. Each phase produces a working change
  or a short result note, not another plan.
- No change to merge, release, or publication authority. Those stay reserved.

## 3. The Grounding Pack

Four files, stored in the **target** repository (default location
`.sensemaking/`; an existing `CONTEXT.md` / `docs/adr/` / `CLAUDE.md` is reused
instead of duplicated).

| File | Holds | Budget |
| --- | --- | --- |
| `intent.md` | Users, the job the product does, current goals, **non-goals**, open owner decisions, answered owner questions | 800 words |
| `context.md` | Domain terms and what they mean in this repo; terms that are easy to confuse | 800 words |
| `invariants.md` | Rules that must stay true, especially ones the code does not enforce; known traps with the incident that taught them | 600 words |
| `decisions/NNNN-*.md` | One short record per decision: choice, rejected alternatives, why | 250 words each |

**Provenance rule.** Every line in `context.md` and `invariants.md`, and every
factual claim in `intent.md`, ends with one tag:

- `[code: path]` or `[test: path]` - checkable against the repository;
- `[owner: date or link]` - an owner decision; authoritative for intent;
- `[hypothesis]` - the agent's inference; must not be treated as fact.

**Inclusion rule.** A line belongs in the pack only if an agent could not
recover it from the code in a few minutes. If it can be enforced by a test,
type, or lint rule, write that instead and cite it.

**Budgets are hard limits.** When a file is over budget, cut or merge lines;
do not add files.

## 4. Phases

### Phase 0 - Ratify the direction (owner)

Work:

1. Record a Level-4 revision in `docs/product-strategy.md`:
   - section 1 (purpose): add that the main lever is target-repo grounding;
   - section 9 (hypotheses): add "A Grounding Pack reduces owner questions and
     rework versus a direct agent" as *Not established*;
   - section 10 (success measures): add owner questions per task and rework
     per task.
2. Add ADR 0030 "Target-repository Grounding Pack" recording the format in
   section 3, the provenance rule, and that the Brief stays for compatibility.
3. Owner chooses the first target repository. Candidates:
   `ThorStarlord/React_incremental_game_prototype` (used in Trial 001, has
   Build Validation CI) or `auteur` (already probed in
   `integration-run-auteur.yaml`). Selection criteria: real ongoing work, CI
   that runs, and the owner can answer intent questions.

Exit: ADR 0030 merged; strategy updated; target named.

### Phase 1 - Template and skill change (this repo)

Work:

1. Add `templates/grounding-pack/` with the four files, each with a header
   stating its budget, the inclusion rule, and the provenance tags.
2. Add a "Build or refresh the Grounding Pack" section to
   `skills/repo-sensemaker/SKILL.md` (at most 600 words):
   - read the existing pack first; if absent, create it from the template;
   - fill `context.md` and `invariants.md` from code, tests, commit history,
     and existing docs, tagging every line;
   - write candidate intent as `[hypothesis]` and list it under
     "open owner decisions" instead of inventing it;
   - never restate what grep can find.
3. Add the **question ratchet** to `skills/using-sensemaking/SKILL.md` (at most
   200 words): before asking the owner, check `intent.md` and `decisions/`;
   after the owner answers, record the answer with `[owner: date]` in the same
   change.
4. Add a line to `skills/using-sensemaking/SKILL.md` "Default doctrine": read
   the target repo's Grounding Pack before task work when it exists.
5. Run the full test suite; confirm no artifact-contract or field-agreement
   test changes, since no new machine fields are introduced.

Exit: template exists; both skills updated; tests pass on the same set as
`main`.

### Phase 2 - Build the first pack (target repo)

Work:

1. A fresh agent session with the updated skills builds the pack for the
   chosen target repository in one pull request to that repository.
2. The owner reviews **only** `intent.md` and the open-decisions list, and
   answers or corrects them. Other files are reviewed by spot-checking ten
   tagged lines against the cited paths.
3. Record a short result note (at most one page) in
   `docs/normal-use/grounding-pack-build-001.md`: time to build, words per
   file, share of lines by tag, spot-check failures, owner corrections.

Exit: pack merged in the target repo; spot-check failure rate under 10%;
result note merged here.

Stop if: the pack cannot stay within budget without dropping lines the owner
considers essential (the format is wrong; revise section 3 before continuing).

### Phase 3 - Use it on real work (target repo)

Work:

1. Take the next 6 to 10 real tasks from the target repository's backlog,
   chosen by the owner before seeing results. Mix sizes: at least two that
   touch more than one module.
2. Alternate arms by task order (odd: agent with pack; even: same agent and
   model, pack hidden by working from a branch without `.sensemaking/`). Both
   arms keep normal repository access and CI.
3. For each task, record in a single table in
   `docs/normal-use/grounding-pack-use-001.md`:
   - owner questions asked;
   - questions that the pack already answered (ratchet misses);
   - rework: follow-up commits after the first "done" claim, and CI failures;
   - invariant violations found in review;
   - owner preference between the two results, where both exist;
   - pack lines added or corrected during the task.
4. The ratchet stays on in the pack arm: answered questions go into
   `intent.md` immediately.

Exit: table complete for all chosen tasks.

Decision rules (applied in Phase 4):

- **Adopt** if the pack arm has fewer owner questions and no more rework, and
  the owner does not prefer the no-pack results overall.
- **Revise format** if the pack arm asks fewer questions but has equal or more
  rework (the pack may hold the wrong content).
- **Stop the direction** if there is no difference in questions or rework;
  record the result and return to the Level-4 strategy.

### Phase 4 - Decide and simplify (this repo)

Work, if Phase 3 says **Adopt**:

1. Shrink `skills/using-sensemaking/SKILL.md` to a core of at most 1,500
   words: goal and authority, read the pack, the question ratchet, resolve
   the nearest decision-changing uncertainty, verify against real behavior,
   when to stop. Move the rest to `references/` as optional reading.
2. Shrink `skills/repo-sensemaker/SKILL.md` to at most 1,500 words centered on
   building and refreshing the pack. Keep the Brief path for compatibility
   until a separate decision retires it; do not delete contract fields that
   tests or validators still read.
3. Update `docs/product-strategy.md` section 9 with the measured result and
   its limits (one target repository, small N).
4. Stop adding inward-facing status documents for work that does not change
   behavior. `STATUS.md` keeps one line per integrated change.

Exit: skill word counts within budget; tests pass; strategy updated.

### Phase 5 - Second target and maintenance (target repos)

Work:

1. Repeat Phases 2 and 3 on a second, different repository to check the
   format transfers.
2. Keep packs current: any pull request that changes behavior covered by a
   pack line updates that line in the same pull request.
3. Only if stale citations are observed in practice: add a small script that
   checks every `[code: path]` and `[test: path]` target exists. Its consumer
   is the agent reading the pack; it must not check anything else.

Exit: second result note; observed staleness rate recorded.

## 5. Measures

| Measure | Source | Direction |
| --- | --- | --- |
| Owner questions per task | Phase 3 table | Down, and lower in the pack arm |
| Ratchet misses (asked although recorded) | Phase 3 table | Zero |
| Rework commits and CI failures after "done" | Target PR history | Not higher in the pack arm |
| Invariant violations found in review | Owner review | Lower in the pack arm |
| Pack size and tag mix | Pack files | Within budget; `[hypothesis]` share falls over time |
| Process-guidance words loaded per session | Skill word counts | Down after Phase 4 |

Validator pass rates are not a success measure for this plan.

## 6. Risks

| Risk | Mitigation |
| --- | --- |
| The pack grows into another documentation pile | Hard word budgets; inclusion rule; cut before adding files |
| Agent-written guesses get treated as facts | Provenance tags; `[hypothesis]` lines cannot justify an action alone |
| Pack goes stale | Update in the same PR as the change; Phase 5 citation check only if staleness is observed |
| Small N in Phase 3 overstates the result | Report counts, not percentages; claim limited to the tested repos |
| Planning replaces doing | No new plan documents between phases; each phase ends in a change or a one-page result |
| Owner availability limits intent capture | Owner reviews only `intent.md` and open decisions; everything else is agent-maintained |

## 7. Owner decisions needed

1. Approve the Level-4 change and ADR 0030 (Phase 0).
2. Choose the first target repository and the task list for Phase 3.
3. Answer the open intent questions in the first pack (Phase 2).
4. Apply the Phase 3 decision rule (Phase 4).
