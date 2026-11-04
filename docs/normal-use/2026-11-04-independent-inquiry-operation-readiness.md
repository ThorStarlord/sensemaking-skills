# Independent Inquiry Operation Qualification — Stage 0 Readiness and Case Selection

**Date:** 2026-11-04.  
**Status:** **STAGE 0 PARTIALLY COMPLETE — CASE INPUTS GROUNDED; FRESH-AGENT EXECUTION BLOCKED IN THIS HOST.** No inquiry operation is provisionally qualified, failed, or empirically assessed by this readiness record.  
**Source of the qualification request:** owner-supplied *Sensemaking — Independent Inquiry Operation Qualification Plan* (2026-11-04, **proposed/not yet executed**); this is a bounded **execution-readiness addendum**, not an accepted Skill contract, a new stage pipeline, an experimentation policy, or a replacement for the owner's original text.  
**Inspected Sensemaking source baseline:** `ThorStarlord/sensemaking-skills` `main@206c4cd267033c7d0cce955fbe370d093a5abfa0` (PR #722 merge).  
**Target claim:** **Practical repeatability of each separately bounded Sensemaking inquiry responsibility in genuinely fresh coding-agent sessions**, with evaluated next-step recommendations. NOT universal generality, superiority to a capable ordinary agent, causal graph advantage, multi-stage autonomy or validated product desire.

## 1. Readiness verdict

The [existing inquiry-process reconciliation](../explorations/2026-11-03-inquiry-process-reconciliation.md) distinguishes six modes: **Priority Framing, Divergent Exploration, Coverage Assessment, Convergent Evaluation, Focused Depth Exploration, Portfolio Reassessment**. It treats them as **adaptive responsibilities**, not a mandatory pipeline. [Product strategy](../product-strategy.md) and accepted ADRs 0029/0031/0034 still determine product purpose, evidence limits and authority. The owner-supplied plan explicitly prioritizes **Divergent Exploration** and **Focused Depth Exploration** for the first observations; historical [Exploration Atlas](../explorations/README.md) reports must not count as fresh qualifications.

**Actual environment inspection:** the present agent has connected GitHub read/write/review tools and can read the installed `using-sensemaking` Skill. A local inspection of **this container**, however, found `git` but no available `codex`, `claude` or `opencode` executable. The current connected tools do **not** expose an action to launch genuinely independent coding-agent conversations. This does **not** imply that those CLIs are absent on the owner's Windows machine or other runtimes; their availability there is **NOT_ASSESSED**. GitHub access by itself is not a new independent-agent session. Running the same model twice in this conversation or generating hypothetical transcripts would not satisfy the plan's independence criterion.

**Decision:** preserve source-pinned candidate cases and a short operating contract, then **STOP at the executable-session boundary**. Actual Round A runs, independent reviewer judgments, Round B and process integration are **NOT_RUN/BLOCKED** pending a real fresh-session host. This is an honest capability boundary, **not** a failed Sensemaking operation, and not reason to build test infrastructure or rewrite guidance.

## 2. First two operations: authentic, source-pinned candidate cases

Case questions below are **proposed invitations**, not detailed reasoning scripts or predicted answers. Each runner must read the actual repository sources at the pinned revision; the source links are read-only evidence. The case must not supply an earlier conclusion as an answer. **Case selection is not execution**.

| Proposed case | Operation and target baseline | Bounded question for a fresh session | Why useful / contamination check |
| --- | --- | --- | --- |
| **DE-A, Round A** | **Divergent Exploration** — [Atlas Midgard](https://github.com/ThorStarlord/atlas-midgard/tree/2b3556e47daa6110d01c045432e23bf4e041ba49), `main@2b3556e47daa6110d01c045432e23bf4e041ba49` | *What materially different player experiences might become possible from Atlas's existing relationship among authored character identity, character-anchored buildcraft, and region/Hearth support, without changing its accepted product identity?* | [Buildcraft source](https://github.com/ThorStarlord/atlas-midgard/blob/2b3556e47daa6110d01c045432e23bf4e041ba49/docs/systems/transformative-buildcraft.md) separates canonical design from implemented runtime; [product thesis](https://github.com/ThorStarlord/atlas-midgard/blob/2b3556e47daa6110d01c045432e23bf4e041ba49/docs/vision/product-thesis.md) and [regional continuity](https://github.com/ThorStarlord/atlas-midgard/blob/2b3556e47daa6110d01c045432e23bf4e041ba49/docs/decisions/living-continuity-network-model.md) set boundaries. **Exclude** the already answered exact Atlas guest/host *belonging without owning* creative question from [PR #722](../explorations/2026-11-03-cross-repository-creative-discovery-atlas-midgard.md). |
| **DE-B, conditional Round B** | **Divergent Exploration** — [Auteur](https://github.com/ThorStarlord/auteur/tree/8036dac6e9f66f06d2e8369b3e4ea48670f11a38), `main@8036dac6e9f66f06d2e8369b3e4ea48670f11a38` | *What potentially distinct author-facing experiences could emerge from Auteur's complete agent-generated narrative architecture and author-governed revision, beyond already implemented workflow and presentation conventions?* | [Current status](https://github.com/ThorStarlord/auteur/blob/8036dac6e9f66f06d2e8369b3e4ea48670f11a38/STATUS.md), [narrative architecture design](https://github.com/ThorStarlord/auteur/blob/8036dac6e9f66f06d2e8369b3e4ea48670f11a38/docs/architecture/detailed-narrative-architecture-v1.md) and [Story Lens UX](https://github.com/ThorStarlord/auteur/blob/8036dac6e9f66f06d2e8369b3e4ea48670f11a38/docs/design/2026-09-24-story-lens-first-screen-ux.md) distinguish accepted/implemented experiences from speculation. Authorship is a genuinely different beneficiary/domain from an ARPG; check whether the question duplicates an already completed internal design exploration before launch. |
| **FD-A, Round A** | **Focused Depth Exploration** — [Metamorfose Edutech](https://github.com/ThorStarlord/metamorfose-edutech/tree/570f25ec0eafc6335524719abf764d1a7119835f), `main@570f25ec0eafc6335524719abf764d1a7119835f` | *What direct, second-order, systemic, beneficial and harmful consequences follow from treating a developmental play opportunity as valuable while **not** treating it as a measured mastery claim, when educators must make informed follow-up decisions?* | [Accepted skills/opportunity distinction](https://github.com/ThorStarlord/metamorfose-edutech/blob/570f25ec0eafc6335524719abf764d1a7119835f/docs/human/current/decisions/games/ADR-2026-09-10-measured-skill-vs-developmental-opportunity.md) and [Pedagogical Control Plane](https://github.com/ThorStarlord/metamorfose-edutech/blob/570f25ec0eafc6335524719abf764d1a7119835f/docs/human/current/architecture/pedagogical-control-plane-v0.1.md) already distinguish pedagogical intention, observations, interpretation and educator authority. An honest result may partly RESTATE existing consequences; qualification measures defensible depth, **not** mandatory discovery. **No real children, student records, or private school data**. |
| **FD-B, conditional Round B** | **Focused Depth Exploration** — [Auteur](https://github.com/ThorStarlord/auteur/tree/8036dac6e9f66f06d2e8369b3e4ea48670f11a38), `main@8036dac6e9f66f06d2e8369b3e4ea48670f11a38` | *If the derived narrative-architecture guidance changes while an author's accepted Story Identity and provenance remain authoritative, what consequences follow for interpretation, revision, trust and author autonomy?* | [Current status](https://github.com/ThorStarlord/auteur/blob/8036dac6e9f66f06d2e8369b3e4ea48670f11a38/STATUS.md) describes current guidance-freshness boundaries; [Detailed Narrative Architecture](https://github.com/ThorStarlord/auteur/blob/8036dac6e9f66f06d2e8369b3e4ea48670f11a38/docs/architecture/detailed-narrative-architecture-v1.md) distinguishes authoritative history and derived interpretation. A changed-premise negative finding can pass, provided it is source-faithful and not a reproduction of an answer supplied in the invocation. |

**Source currentness:** these are observed main revisions **at Stage 0**, not promises that the live repos will remain unchanged. A qualification runner must either pin/check out the above refs or declare a new source revision before beginning. The **installed Skill bytes / installer profile / host/model configuration are not verified here**. The fresh runner and reviewer must capture them as part of each actual attempt; the repository SHA does not prove which installed Skill an external host loaded.

**Variation:** DE-A is game design and DE-B is narrative authoring; FD-A is pedagogy/evidence and FD-B is author-facing narrative judgment. This intentionally tests **operations**, not the same exact inquiry repeated, and avoids simply copying archived Sensemaking answers. Round B is **conditional on satisfactory and informative Round A results**, not a scheduled obligation.

## 3. Short neutral invocation contract

One operation per new agent conversation; choose only its case question, target, Skill entrypoint and source revision. Use ordinary access to product docs, implementation, installed Skills and Git history. Do not give a stage-by-stage reasoning script, prior finished solution, previous run's transcript, hidden model hints, or expected conclusion.

Suggested **neutral case invocation** (for each selected case):

> Use the installed `using-sensemaking` Skill and repository evidence at the specified source revision. Perform **only [OPERATION]** concerning **[QUESTION]** in **[TARGET REPOSITORY]**. Independently recover the authoritative source context. Produce one meaningful, source-grounded result; distinguish established facts, prior ideas, hypotheses, unknowns, and authority limits; explain why this operation is complete and recommend a next warranted inquiry only if useful. **Do not perform the next operation or implement speculative findings.**

Do not insert case-specific intended answers or the existing reviewer's novelty expectations into the agent-facing prompt. The aphoristic guidance in the owner-supplied plan is **evaluation intent**, not an answer key. The runner may add only necessary technical access/return instructions, not an intellectual solution.

## 4. Independent observation and review contract

**A fresh observation requires:** (a) new conversation/context, no prior attempt's answer, (b) exact source revision and installed Skill version, (c) normal source access, (d) recording agent/host/tool availability and source reads as inspectable, (e) a completed single-operation output and stopping behavior, and (f) no silent source mutation between trials. Separate worktrees are optional if immutable checkout access is sufficient.

**Reviewer:** a different reviewer from the producing agent, with relevant original files and near-predecessor ideas available; no exact-answer benchmark. Independently inspect pivotal source claims and authority. Human owner judgment is especially appropriate when new artistic/pedagogical desirability is claimed; it does not by itself make the session an independent model run.

**Two independent verdict axes per completed run:**

1. **Operation result:** source grounding, operation fidelity, intellectual substance, novelty/uncertainty, authority integrity and completion decision → `SUFFICIENT / INSUFFICIENT / INCONCLUSIVE` with reasons.
2. **Next-step recommendation:** unresolved question, basis in evidence, correct next operation (or warranted stop), executable specificity, alternatives, no unauthorized continuation → `SUFFICIENT / INSUFFICIENT / NOT_APPLICABLE` with reasons.

**Critical defects:** fabricated consequential evidence, invented owner mandate, unsupported new-goal certainty, treating graph omission as real absence, confusing inquiry preference with permission to build, silently executing the next operation, claiming unobserved trials, or ignoring decisive contradictory sources. A well-formatted report alone is not evidence of success.

**Operation-level repeatability:** only after **two completed fresh, suitably different cases**, reviewed independently without unresolved critical defects, may one say `PROVISIONALLY QUALIFIED IN TESTED CONTEXTS`. One successful Round A is **not** repeatability. Another discriminating case is warranted only if it could change that verdict. Historical prior reports can inform the reviewer but count **zero** new trials.

**Repair:** if an observed critical defect is real, identify its cause (guidance/source access/prompt/agent/reviewer/authority), make at most the smallest warranted correction, preserve the failed record, and repeat in a fresh session with the changed version identified. Do not amend all Skills preemptively or add a new execution runtime.

## 5. Readiness matrix — evidence only

| Operation | Fresh completed observations in this program | Independent review | Operation repeatability | Next-step recommendation quality |
| --- | --- | --- | --- | --- |
| Priority Framing | **0** | NOT_RUN | NOT_RUN | NOT_ASSESSED |
| Divergent Exploration | **0** | NOT_RUN | **BLOCKED / NOT_RUN** | NOT_ASSESSED |
| Coverage Assessment | **0** | NOT_RUN | NOT_RUN | NOT_ASSESSED |
| Convergent Evaluation | **0** | NOT_RUN | NOT_RUN | NOT_ASSESSED |
| Focused Depth Exploration | **0** | NOT_RUN | **BLOCKED / NOT_RUN** | NOT_ASSESSED |
| Portfolio Reassessment | **0** | NOT_RUN | NOT_RUN | NOT_ASSESSED |

**No empirical or independent-agent claim is supported by this readiness artifact.** The existing [operational-qualification first-use case](operational-qualification-001.md) and [pre-registration](operational-qualification-001-preregistration.md) illustrate durable evidence conventions but are different questions and historical baselines; their outputs are **not** new operation passes. The repository's [qualification-evidence receipts](../qualification-evidence.md) verify structural frozen packages, not the intellectual quality or origin of a new fresh agent session.

## 6. Next warranted responsibility and stop

1. **Outside this host:** identify an actual fresh-session runner (local Codex / Claude Code / OpenCode or other coding-agent host), its precise installed `using-sensemaking` source/version, and an independent source-aware reviewer. This requires actual tool/environment availability, **not** a speculative workflow.
2. Verify the chosen case input's exact source revision, ensure its answer is not supplied as an existing report, and pre-record a short two-axis reviewer rubric.
3. Run **DE-A and FD-A as two separate fresh agent sessions**, one per operation; retain their raw outputs and inspectable run traces where available. **These runs have not occurred.**
4. Independently review each before choosing a different Round B case; a material defect can warrant one narrowly targeted correction and fresh replacement.
5. Defer cases for the remaining four operations, the twelve-observation planning ceiling, human-supervised integration and autonomous orchestration until real outcome evidence warrants them.

**STOP at Stage 0 in this host.** Do not fabricate subagent independence, execute more inquiry modes within this same context, run synthetic pass/fail scripts, open a separate evaluation infrastructure project, rewrite the governing original exploration archive, modify any target repository, promote candidate product goals, or claim successful qualification/integration. Only this readiness document may be committed to the Sensemaking repository as **preparatory evidence**, not a qualification receipt.
