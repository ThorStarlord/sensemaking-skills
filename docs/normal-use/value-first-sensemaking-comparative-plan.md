# Value-first Sensemaking: compact-vs-full comparative evaluation plan

**Status:** owner-requested evaluation plan; documentation-only; not an executed experiment or a shipped Skill change  
**Recorded:** 2026-10-11  
**Scope:** compare decision and product value before investing in further Sensemaking complexity  
**Canonical product boundary:** [ADR 0029](../adr/0029-current-product-boundary.md) and [product strategy](../product-strategy.md)  
**Related evidence:** [September 30 remeasurement](strategic-sensemaking-remeasure-2026-09-30.md), [autonomous terminal-mission corroboration](autonomous-terminal-mission-corroboration-plan.md), [Capability Scale Frontier](../research/capability-scale-frontier-v0.md)

## Decision to support

**Does adding Sensemaking guidance to a capable coding agent materially improve the
selection and delivery of a useful engineering outcome, relative to using that
agent directly, at an acceptable total cost? If so, what is the smallest
guidance surface that preserves the demonstrated improvement?**

The intended benefit is *building the right thing*, not merely producing
correctly validated artifacts for a possibly wrong responsibility. This
includes recognizing when the requested implementation is unnecessary,
finding a simpler path to the underlying user goal, choosing a useful
reversible prototype, and preserving the few consequential invariants that
the shortcut must not violate.

This is a **comparative product hypothesis**, not a new Level-4 product
mission, release gate, Skill, Campaign type, policy layer, score, or runtime.
It is not an instruction to retire existing specialized capabilities today.

## 1. Baseline: what is known and what is not

- The September 30 remeasurement used 18 **read-only** episodes: three per
  arm on each of Pydantic, Jellyfin, and AION. It found **zero clearly
  Skill-favorable tasks** against the pre-registered threshold. Pydantic
  favored the control, Jellyfin tied, and AION was weakly Skill-favorable.
  This warrants the existing **simplify-hard** posture; it does **not**
  demonstrate a measured universal productivity loss, prove a broken
  mechanism, or quantify a two-minute-versus-twenty-minute delay.
- At the October 11 source checkpoint, `skills/using-sensemaking/SKILL.md`
  is approximately 6,334 words. Prompt length is a plausible source of
  attention dilution, repetitive meta-deliberation, and false escalation,
  **not a proven causal explanation** for the earlier results.
- The repository has many specialist Skills and historical documents, but
  file count alone does not establish what an actual agent loads into its
  context. Distinguish source size, actually loaded bytes, invoked references,
  and observed behavior.
- The current Skill already advocates direct bounded work, optional
  Campaign use, experience-first previews, and reversible construction.
  **Having those instructions on paper is not evidence they work in use.**
- Trial 001 supports a bounded autonomous engineering target with
  loaded-Skill attribution limits. Trial 002/002R is still target-unpinned
  in [Issue #515](https://github.com/ThorStarlord/sensemaking-skills/issues/515).
  Neither result supplies the missing construction-enabled comparison.
- Real software changes are often cheap enough to prototype, but
  integration, migration, security, persistence, recovery, review, and
  ongoing maintenance can dominate generation cost. Deleting a branch
  cannot reverse a destructive production action.

**Question not yet answered:** is the marginal value absent, hidden by a
large default prompt, specific to higher-consequence decisions, or simply
unmeasured because prior comparisons were read-only?

## 2. Value-first operating hypothesis

A useful agent should normally:

1. Infer the human outcome and distinguish it from the implementation the
   user first proposed; challenge that proposed implementation **only when**
   a concrete alternative could materially improve the outcome.
2. Consider the smallest practical solution, including doing nothing,
   a configuration change, a bounded repair, an existing feature, a
   disposable prototype, or a larger build when actually necessary.
3. Prefer cheap, authorized, reversible construction as evidence when it
   is more informative and lower total cost than further speculative
   planning; interact with prototypes when experience is the unresolved
   question.
4. Identify and protect the **material** invariants: e.g. no user-data loss,
   real permissions, migration safety, security, or a reserved merge or
   deployment boundary. Do not confuse a locally passing test with the
   desired product outcome.
5. Ship/complete useful bounded work, learn from the result, and stop when
   additional analysis cannot change the decision.

Avoid the two extremes:

- **Process theater:** verbose levels, warrants, ledgers, documents,
  speculative tests, or escalation that do not change a consequential
  decision or protect a real invariant.
- **Speed theater:** assuming code generation is free, dismissing real
  integration risk, trusting running code over all documented intent,
  or discarding protection because a prototype is easy to write.

These are evaluation hypotheses. Do not reinterpret this plan as proof that
a particular instruction length or shortcut is always optimal.

## 3. Three comparison arms

| Arm | Agent guidance | What it tests |
| --- | --- | --- |
| **A — Direct agent** | Normal repository/tool instructions and the same user goal, **without Sensemaking** | Competent baseline; no invented procedural handicap |
| **B — Compact Sensemaking** | A separate approximately 300–500-word **experimental** instruction, retaining essential authority and trust boundaries | Whether a small set of value-first heuristics beats A and reduces unnecessary ceremony |
| **C — Current full Sensemaking** | The exact versioned, verified current `using-sensemaking` instructions, with the same on-demand access normally available in the intended harness | Whether deeper guidance provides incremental value over A and B |

The 300–500-word range is an **initial design constraint**, not a presumed
optimum or a mandatory permanent limit. Do not cut away meaningful behavior
solely to meet a word count. Measure total **actually loaded** instructions
rather than counting repository files that the agent never read.

All three arms receive the same task-specific facts, repository state,
resources, model/runtime class, tool permissions, time/budget envelope, and
ordinary safety requirements. The intervention is guidance, not a secretly
different engineering task.

### Candidate compact intervention — draft only

The following is a **starting point to edit and freeze for an actual
comparison**, not a shipped replacement or an instruction automatically
active in current user sessions:

> You are a coding agent responsible for the user's useful repository outcome,
> not for producing planning artifacts. First identify the user's underlying
> goal, the current repository reality, and any constraints that could make
> the obvious implementation wrong. If the path is clear and local, execute it
> directly without ceremony.
>
> When the requested feature or next task may solve the wrong problem, briefly
> compare the plausible alternatives: do nothing, reuse existing capability,
> configuration, small patch, reversible prototype, or larger design. Prefer
> the simplest approach that demonstrably satisfies the need, not the one with
> the smallest code diff at any cost. Raise alternatives only when they could
> change the decision.
>
> Prefer inexpensive, reversible construction and firsthand inspection over
> elaborate speculative planning when the build can provide sufficient
> evidence. Preserve data, security, persistence, correct authority, and other
> real system invariants proportionately to risk. Production actions and
> irreversible migrations require stronger checks; branch deletion does not
> undo external side effects.
>
> Complete bounded useful work within granted authority; avoid unrelated
> cleanup, invented deliverables, premature owner escalation, and documentation
> that nobody needs to continue. If the task spans fresh contexts, preserve
> only the progress, evidence, next responsibility, and stop conditions needed
> for safe continuation. Verify the actual user-relevant behavior, state
> uncertainty honestly, and distinguish implemented, tested, merged, and
> deployed.
>
> Ask for owner decisions only when repository evidence cannot resolve a
> genuinely reserved choice. Otherwise choose the warranted next action and
> continue. Stop when the outcome is reached or a real authority, risk, or
> external-evidence boundary prevents progress.

Before running, edit the draft only to remove ambiguity and freeze one exact
version. Do not iterative-tune it against the held-out comparator outcome.

## 4. Select tasks that expose actual product judgment

### Initial case: a real value-selection dilemma

Choose **one authentic current repository need** with a real user outcome,
more than one credible intervention, and a useful observable result. An ideal
case is a requested large feature whose underlying need might instead be met
by an existing capability, configuration, local repair, or small prototype.
The simple alternative need not be correct: discovering that it is inadequate
is also legitimate evidence.

Admission conditions:

- The request is genuinely authorized and not already materially delivered
  by an in-flight PR or existing feature.
- Current source, owner intent, and acceptance criteria can be established
  without manufacturing a fake problem or planting conflicting docs.
- Both a minimal and a more extensive solution remain credible **before**
  seeing the agent outputs; neither is seeded as the expected correct answer.
- A reviewer can inspect actual behavior or a user-relevant artifact, not
  merely the quality of the agent's prose.
- The target is reversible or safely isolated, with consequential trust
  boundaries specified.
- The evaluator can recognize justified **no-build**, small-build, and
  large-build outcomes. A "two-line fix" is not always the right answer.

Do **not** recycle an already active Auteur/Metamorfose implementation issue
to manufacture fresh Trial 002 admission. Choose from live authorized work;
if no case qualifies, record **NO ADMITTED CASE** and continue ordinary work.

### Follow-on case: real construction, not only analysis

If the initial case yields a decision-changing signal or leaves a meaningful
unknown, use one authentic bounded feature requiring actual integration
across relevant surfaces and objective checks. It should create a useful
artifact, not merely a strategic report. Preserve independent review of
usability/acceptance where applicable.

A later long-horizon case may test fresh-context continuation or autonomous
responsibility selection, but **more complexity is not itself a success
criterion**. Add an axis only if the existing evidence leaves that capability
both useful and unproven.

## 5. Execution protocol (when an independent runner exists)

**Preflight — no run without a valid baseline**

1. Capture the current Sensemaking `main` commit and target repository base
   SHA. Verify the full Skill actually loaded by the runner; hosted installs
   require platform-specific version verification. Record whether native
   discovery is verified, an exact manual load, or unknown. Do not label
   stale/unverified instruction bytes as the tested version.
2. Freeze the compact candidate text, the original owner request, target
   acceptance observations, allowed actions, budgets, and protected
   transitions. Specify which alternatives were plausible at admission.
3. Create isolated workspaces and independent agent contexts for A, B, C.
   Do not carry earlier arm outcomes, critiques, or sealed expected choices
   into another arm. Same Git base, harness class, model version, tools,
   credentials scope, and allowed authority; record deviations.
4. Confirm the runner can actually edit, execute, and verify the target.
   A GitHub read/write connector without an independent runnable coding
   agent is **not** a construction-enabled comparator. If unavailable,
   stop at a documented setup limitation; do not replay prompts and
   claim an independent trial.
5. Predefine the evaluator and minimum evidence. Prefer a reviewer who
   did not author the variants, blinded to arm labels when practical.
   The target owner may provide genuine product feedback. Do not treat the
   evaluated agent's self-report as independent verification.

**Run — preserve the useful artifact**

6. Give each arm the same task and constraints, changing only the intended
   guidance. Let ordinary engineering competence and existing project
   instructions remain available to all arms.
7. Preserve commits/diffs, runnable result, relevant test outputs,
   genuine interaction or owner feedback, tool-call record, material
   deviations, time/tokens/cost where measurable, interruptions,
   false escalations, and any authority or safety violations. Keep
   branches separate; do not merge competing experiment outputs as a
   side effect.
8. Review the *artifact and chosen solution*, not just documentation
   quality. When two approaches both work, compare whether the added
   control guidance justified its attention and operational cost.
9. Explicitly classify an external blocker or no-run as **NOT TESTED**,
   not a capability failure or a success. A preview that boots proves
   inspectability, not user preference or product fitness.

**Reconcile — do not overclaim**

10. Compare A vs B, A vs C, and B vs C. Preserve the smallest
    decision-relevant qualitative finding. Attribute only where variant
    identity, execution conditions, and artifacts permit it.
11. If a clear failure is found, isolate its mechanism: verbosity,
    premature escalation, unnecessary research, stale Skill loading,
    false confidence, missed alternatives, context continuity, missing
    tools, or an actual user-need mismatch. Do not invent a new subsystem.
12. Apply the decision rules below. Record exceptions and uncertainty;
    a single case supports only a bounded conclusion.

## 6. Evidence that should influence the decision

| Question | Observable evidence | Anti-pattern to catch |
| --- | --- | --- |
| **Right outcome?** | User need met, credible alternative considered, artifact works in relevant interaction | Beautiful or well-tested wrong feature |
| **Minimal sufficient intervention?** | Existing capability reused or solution proportional to need | Building a new abstraction because it is easy |
| **Agency and completion?** | Independent action without unnecessary owner routing; real stop boundary | Escalating a repository-answerable question |
| **Cost of deciding and building?** | Measured elapsed/tool/token use when available; material rework and avoidable steps | Claiming a timing benefit without a measurement |
| **Trustworthiness?** | Tests/inspection matched to risk; user data and actual permissions protected | Treating green CI or branch rollback as a guarantee |
| **Continuity, when tested?** | Fresh context recovers the goal, next responsibility, and limits without the old chat | Large ledger replaces actual progress |
| **Guidance fidelity?** | Verified loaded bytes/variant and controlled differences | Attributing current Skill behavior to a stale hosted copy |

Use qualitative evidence and actual observations; no synthetic 8-axis
leaderboard, arbitrary weighted score, rigid case quota, or automatic winner
selection. Success on a small case cannot establish broad autonomous
competence. A task may correctly end with **no code changed**.

## 7. Implementation milestones and exit criteria

### M0 — Prepare a comparison without changing the shipped Skill

- Use this plan and existing Issue #218 for naturally occurring evidence;
  do not create a new tracker or evaluation runtime just to administer it.
- Verify the concrete source/harness parity procedure for the chosen
  runner; use `scripts/probe_skill_distribution.py` for file-based installs
  and actual installation/update controls for hosted Skills.
- Refine the compact intervention to one frozen text artifact in the
  evaluation workspace, **not** a replacement `SKILL.md` in the shipped
  Skill tree. Record exact bytes/hash and any optionally invoked references.
- **Exit:** one reproducible variant description; no claim about quality.

### M1 — One product-choice comparison at modest scale

- Admit one live authentic dilemma; freeze the goal and acceptance evidence.
- Run A/B/C in independent environments if available.
- Inspect selected approaches, working artifacts or justified non-build,
  unnecessary escalation, missed alternatives, and total effort.
- **Exit:** an honest three-arm comparison or an explicit **NOT TESTED**
  blocker with no synthetic substitute.

### M2 — Bounded construction-enabled comparison

- Proceed only if M1 leaves a consequential uncertainty that real
  construction can answer.
- Use an authentic integrated feature with meaningful acceptance checks.
- Again compare the real artifacts and outcomes, not the amount of procedure.
- **Exit:** supported/contradicted/inconclusive findings scoped to this
  repository and task class. No general superiority claim.

### M3 — Adjacent complexity, only if warranted

- If marginal value appears tied to continuation, test one actual
  fresh-context break (D) with durable source state.
- If tied to selecting the right responsibility, test an unpinned
  highest-leverage choice (A/C/E). If tied to protected transitions,
  test authority (F) only where separately granted.
- Use the [Capability Scale Frontier](../research/capability-scale-frontier-v0.md)
  as descriptive vocabulary, **not** a requirement to fill eight cells.
- **Exit:** one tested adjacent boundary or a justified decision not to scale.

### M4 — Product decision and smallest follow-through

- **A beats B and C:** do not force broad Skill loading; narrow the
  use case, retire/restrict the default, or retain specialist capabilities
  only where independently useful. Preserve uncertainties.
- **B improves on A; C adds no marginal benefit:** favor a short default
  with selectively loaded references. Design and qualify migration
  separately; do not delete shipped surfaces on one episode.
- **C improves on both:** identify which guidance made the difference,
  then attempt to retain that mechanism with less default overhead.
- **Mixed/domain-specific outcomes:** make the guidance opt-in or
  context-dependent without inventing a deterministic router.
- **No genuine comparator or no decision-changing result:** stop
  experimentation, continue real authorized engineering, and do not
  manufacture additional cases.

**Exit:** a concise decision tied to actual evidence, retained limitations,
the next useful intervention (if any), and a clear authority path for
changing a shipped Skill. Any product-boundary or major Level-4 revision
must follow the existing owner-ratification process.

## 8. Relationship to existing roadmap and authority

This **does not replace or reclassify** the
[Trial 002/002R ladder](autonomous-terminal-mission-corroboration-plan.md).
That ladder diagnoses heterogeneity, continuation, autonomous target
selection, and protected-transition behavior. This plan tests the
**incremental product value of guidance** against a direct agent.
They answer different questions:

```text
Skill executes a difficult mission
!= Skill improves the result versus direct agent

guidance described in docs
!= guidance delivered to the actual harness

mechanically valid implementation
!= right user-facing product

low code-generation cost
!= zero integration or irreversible-action cost
```

Do not pool a fresh-context-resume experiment with the initial A/B/C
comparison as though the interventions were identical. A real eligible
mission may inform both lanes **only with separate claim ceilings**.
Issue #515 remains the specific Trial 002 admission authority.
Issue #255's independent-harness stop is a real external limit;
this plan does not wish it away.

**Authorized now:** document the comparative hypothesis, retain this
plan, and continue normal engineering. **Not performed by this
document:** a runner setup, new compact shipped Skill, real three-arm
trial, changes to ADR 0029, new release evidence, merges, or product
effectiveness claims. Future implementation should select the smallest
bounded next step when the required real task and execution surface
exist.

## 9. Stop conditions and maintenance

Stop and report the boundary when no admitted real task exists,
loaded Skill identity cannot support the intended attribution,
independent execution is unavailable, material risk cannot be bounded,
or results no longer change a product decision. Ordinary work should
not wait for the evaluation program.

Update this one plan rather than creating a new family of competing
protocols. Record actual episodes in existing normal-use surfaces only
when they occur. Avoid fixed word-count dogma, artificial "correct"
two-line solutions, elaborate synthetic task matrices, and automatic
Skill selection machinery.

**Governing principle:** maximize useful decision quality and user
value **per unit of process**, subject to real engineering, evidence,
and authority invariants.
