# Task S1 — Investigation-First, Clarify-If-Needed Interaction Probe (charter, frozen)

experiment_type: solution_interaction (S-series, case 1)
record: charter-v1
recorded_at: 2026-08-08 20:17 -03:00 (before any target-specific investigation)
status: FROZEN
owner: ThorStarlord
scope: experiments/solution-interaction-s1-v1/
target_selection: AGENT_SELECTED_TARGET (owner weakened the gate twice: owner-originated
  -> agent-suggested/owner-confirmed -> agent-selected. Owner instruction: choose one
  repo/question from shallow pre-investigation evidence; freeze choice + rationale
  before any deep investigation; ask no further target-selection questions.)

## Purpose

Test the leading solution hypothesis for the repo-sensemaker product interaction:

> "The default interaction should be investigation-first. The agent should
> autonomously gather and synthesize repository evidence, identify the
> consequential decision boundary, and recommend directly when the evidence is
> sufficient. When the remaining uncertainty is both decision-changing and
> dependent on owner intent, the agent should ask the smallest high-information
> question needed to resolve it, then recommend."

Solution discovery only. Do not modify repo-sensemaker or the target repository
beyond the evidence package below (home-repo convention, same as P1/P2).

## Phase 0 — Frozen identities

- Target repository: **sensemaking-skills** (home repository,
  H:\GithubRepositories\sensemaking-skills, origin
  https://github.com/ThorStarlord/sensemaking-skills.git) @ SHA
  `27aa2442e5395f8793023882d5ed5e94861755e4`
- Target working-tree state at freeze: `M src/sensemaking_skills.egg-info/PKG-INFO`
  (unrelated), `?? .reasonix/`, `?? experiments/product-interaction-p4-v1/`
  (unrelated; P4 evidence not yet committed). Frozen identity is the committed SHA.
- Canonical sensemaking-skills repository SHA: `27aa2442e5395f8793023882d5ed5e94861755e4`
  (target == canonical repo for this home-repo case, same as P1/P2).
- Canonical repo-sensemaker SKILL.md path: `skills/repo-sensemaker/SKILL.md`
- Canonical repo-sensemaker identity: git blob SHA
  `a5cb5dd71fd75adeb879780b9dc47020cecd5ab3` (verified identical to the identity
  frozen in P3 and P4; not modified).
- Exact owner question (agent-selected, frozen verbatim):
  **"Should the next engineering work focus on interaction design or on
  standalone-contract cleanup (the four infrastructure gaps)?"**
  - "interaction design" = the S1-class product-interaction work for
    repo-sensemaker (investigation-first / clarify-if-needed interaction).
  - "standalone-contract cleanup" = the four infrastructure gaps in
    00-user-intent.md: evidence rules dual-mode rendering, execution mode,
    skill-hygiene validator, artifact contracts for PM/engineering.
- Execution mode: agent-native, one-shot, read-only canonical repo-sensemaker
  interaction performed in a fresh subagent context (no prior S1 context
  contamination; the subagent has no knowledge of this session beyond the
  frozen brief it is given).
- Timestamp: 2026-08-08.

Only the current canonical repo-sensemaker is used, exactly once. Not used:
hardening candidates, stale installed copies, modified prompts, P1-P4 variants,
or a prompt tuned to force a desired S1 outcome.

## Target selection rationale (recorded before deep investigation)

Candidates were proposed from a deliberately shallow scan (repo identity, rough
activity, broad architecture, obvious current work areas; no deep diagnosis).
Prior-probe exposure was then checked against P-series records:

1. **renpy_mcp_server — rejected.** P4 already probed it and concluded
   "determine which implementation is the canonical product surface",
   recording the exact high-information owner-intent question. The proposed
   S1 question is P4's own recommendation; the owner already reviewed that
   synthesis. Would pre-solve S1's Phase 3 and pollute the POST judgment.
2. **auteur — rejected.** P3 (auteur @ 374abb4...) already concluded "complete
   the Cartographer pilot v2 behavioral evaluation before any new feature
   slice" — the proposed Cartographer question is P3's exact recommendation.
   Pre-solved.
3. **sensemaking-skills — selected.** P1/P2 probed this repo only with the
   generic "what engineering work would create the most value next?" question.
   The specific live decision — the four infrastructure gaps (00-user-intent.md,
   never implemented) vs. the interaction-design thread — has never been
   probed. It is the owner's most active product repository, the decision is
   genuinely live (the owner is choosing between these threads right now), and
   the residual uncertainty is owner-intent (strategic priority), which
   exercises the clarify-if-needed path S1 is designed to test.

Selection preceded any target-specific investigation. No candidate was
deep-inspected before selection.

## Claim limitation (weakened gate)

S1 used an AGENT_SELECTED_TARGET. The proportional claim is:

> "Given an agent-selected plausible repository decision, the investigation-
> first / clarify-if-needed interaction was tested for usefulness, grounding,
> owner burden, and intent handling."

S1 does NOT claim it tested an authentic owner-owned live decision and does
NOT measure owner demand.

## Phase 1 — Minimal assisted context

Record: assisted-context-v1.md (ASSISTED_CONTEXT label; no PRE questionnaire,
no PRE->POST delta claim; NO CLEAR PRE INCLINATION unless legitimately known).

## Phase 2 — One canonical investigation

Exactly ONE read-only canonical repo-sensemaker investigation of the target,
in a fresh subagent context. Output: repo-sensemaker-investigation-v1.md
(full Repository Sensemaking Brief per the canonical template). The subagent
also returns a Phase-3 input (uncertainty classification + counterfactual
test) in its final answer, NOT inside the artifact.

## Phase 3 — Decide whether to ask the owner

At most ONE owner question, only if:
- the remaining uncertainty is owner-intent (not evidence-resolvable), AND
- the counterfactual holds ("if the owner answered differently, the
  engineering recommendation would materially change").

If one question is asked, freeze it in clarification-v1.md BEFORE asking.
If one question is insufficient: record it, do not ask a second question.

## Phase 4 — Owner-facing synthesis

owner-synthesis-v1.md (compact, 11 required elements), substantially shorter
than the investigation.

## Phase 5 — Canonical validation (once)

Run `scripts/validate-brief.py --json` once on repo-sensemaker-investigation-v1.md;
record complete result in validation-result-v1.json. No repair to force a
pass; no rerun; no validator modification. Success/failure is not the S1
product outcome.

## Phase 6 — Owner POST

Seven lightweight questions (Q1-Q7) recorded faithfully in owner-post-v1.md.

## Phase 7 — Learning

learning-v1.md: disposition PROMISING / MIXED / NOT_PROMISING / MISLEADING;
CLARIFICATION_BEHAVIOR; OWNER_BURDEN; INTENT_PRESERVATION; GROUNDING; the
seven most-important-learning questions; final report.

## Artifacts

experiments/solution-interaction-s1-v1/: charter-v1.md, assisted-context-v1.md,
repo-sensemaker-investigation-v1.md, clarification-v1.md (only if a question is
asked), owner-synthesis-v1.md, owner-post-v1.md, learning-v1.md,
validation-result-v1.json (canonical validation runs).

No numeric scorecards, schemas, campaign machinery, automated evaluators,
authorization frameworks, benchmark harnesses, or A/B/C infrastructure.

## Hard stop / prohibited actions

S1 does NOT authorize implementation. Do NOT: modify repo-sensemaker;
implement clarification logic; build owner-context systems or dialogue state
machines; change validator behavior; reopen P-series; start P5 or S2;
implement the engineering recommendation; modify the target repository beyond
this evidence package; start packaging/distribution or PyPI work; modify
EXP-0002; merge unrelated branches; create infrastructure because S1 suggests
it might be useful. If S1 exposes a promising product change: RECORD IT. DO
NOT IMPLEMENT IT.
