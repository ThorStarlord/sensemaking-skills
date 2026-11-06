# Evidence-Grounded Abductive Inquiry v1 — Conditional Portable Agent Method

**Load when:** a source-grounded observation, apparent contradiction, unexpected output, failure, or strategic/product finding admits **materially different explanations**, and discriminating among them could change what to understand, investigate, explore or do next. Also useful when an agent would otherwise treat one attractive explanation as a fact and generate product ideas from it.

**Skip when:** the task is a clear, directly authorized local fix with adequate verified cause; the question is pure divergent exploration without a material explanatory conflict (use `divergent-exploration-v1.md`); or deeper causes would not change a meaningful decision. The active `using-sensemaking` agent retains responsibility and authority; this is not a standalone Skill, autonomous reasoner, mandatory procedure, graph parser or test gate.

**Result:** a bounded, attributed explanation contrast; source-qualified candidate hypotheses, supporting/counterevidence and assumptions; a useful discriminator or justified unresolved/stop; and *optional* changed inquiry questions/product expressions. A single explanation or a "no useful rival" conclusion can be correct when the evidence genuinely warrants it.

**Portable:** no `.sensemaking/`, framework checkout, ontology index, CLI, repository-specific ADRs or host-specific commands are required. Consult original sources in the current target. These instructions summarize the relevant [conceptual ontology](https://github.com/ThorStarlord/sensemaking-skills/blob/main/docs/semantic-architecture/evidence-grounded-abductive-divergent-ontology-v1.md); reading that external document is not a prerequisite.

## 1. Orient to the intellectual operation

Name the target, actual question, authorized scope and source boundary. Separate:

- **Observed explandum:** what is directly recorded or reproduced, by what source and at which revision?
- **Explanatory uncertainty:** why/how could it happen? Which mechanism is not yet observed or proved?
- **Divergent question:** what materially different end, beneficiary, experience or possibility could be worth exploring *if* an account were plausible?
- **Decision hinge:** would learning more about the cause change the correct next step? If not, avoid turning routine discovery into an investigation.

Use the needed operation, not a fixed Abduct -> Diverge -> Rank -> Build pipeline. A question may be explanatory only, divergent only, both, or already decided. A missing graph edge is a gap in inspected representation, not proof of absent product behavior.

## 2. Contrast rival explanations of the *same observation*

For consequential uncertainty, preserve the **same explanandum** across candidate explanations rather than moving each candidate to a different problem. Create only as many meaningfully distinct hypotheses as sources and decision require. For each:

- explain a plausible mechanism or assumption;
- cite exact supporting **observations** and their relevant source revisions;
- identify counterevidence, contradictory claims, and observations that are *neutral* or not assessed;
- state conditions under which the account could hold or fail;
- distinguish source observation from authored interpretation or newly proposed cause.

An inferred mechanism, even when attractive, remains a Hypothesis until evidence warrants a stronger statement. Two hypotheses can both be partially true; a contrast is not proof of exclusivity. A single source can be consistent with several hypotheses, and citation count does not rank explanations.

Example from one repository's *reported* historical episode: an agent analyzed the invoked Skill rather than the requested whole repository. "It confused method and target" and "the available status read was incomplete" are possible contributing explanations; the report observed both the wrong declared scope and a partial read but did **not** identify an exclusive cause. This example is guidance, not a fact about the user's current target.

## 3. Form one decision-relevant discriminator when useful

A valuable **discriminating question** is more specific than "get more data". It names:

- which hypotheses, source interpretations or premises it could separate;
- the **observable** outcome or source that would be inspected;
- what plausible different observations would do to each hypothesis (support, weaken, narrow or leave unresolved);
- the smallest sufficient real read/probe and the authority to perform it;
- why further inquiry would change the next decision.

If the same result is predicted by all candidates, the probe is not discriminating. A proposed test is not a performed test, a mechanistic explanation, a promise of a positive result or evidence of a causal intervention. When no useful authorized discriminator is available, preserve **UNRESOLVED** rather than inventing a winner. Use [Inquiry / Experiment Economy] discipline if a real controlled experiment is contemplated; ordinary source inspection is usually cheaper.

## 4. Reconsider premises and revisions without rewriting history

Ask whether a changed **premise**, inspected source, scope/horizon, observed behavior or owner purpose changes the actual claim:

- **Same evidence, narrower explanation:** qualify the originally overbroad hypothesis, preserving its old wording/assessed revision.
- **New evidence against a hypothesis:** record the counterevidence and correction; do not erase the earlier account.
- **Changed situation or goal:** distinguish historical applicability from an actual change in facts or owner direction.
- **No decision-relevant new evidence:** record a bounded unchanged/unresolved result; do not force a revision.

Preserve the original cited source and assessed snapshot separately from the date of the current evaluation. Do not treat the most recent document as semantic authority merely because it is newer.

## 5. Open *different* possibilities only when explanation changes the question

A source-grounded explanation may reveal a different beneficiary, desired end, user experience, structural mechanism or adjacent question. Use [Divergent Exploration](divergent-exploration-v1.md) if the inquiry now turns on question/frame changes or incomplete expressions; use [Creative Prospective Discovery](creative-prospective-discovery-v1.md) if it turns on product/architecture novelty.

When an expression matters, record a **short attributed transformation account**, not hidden chain of thought:

> Source/revision + observed or hypothesized relation -> changed premise/meaning -> new question or provisional expression -> nearest existing possibility and difference -> uncertainty and authority boundary.

Ask whether the change is an **explanatory hypothesis**, a **different desired end**, a **different mechanism for an existing end**, or simply **new wording**. Novelty requires a bounded comparison corpus. An explanation is not automatically a new `poss:` record, architecture proposal, adopted strategy or authorized build.

## 6. Regulate and stop

Watch for four errors: fitting every datum to a preferred cause, counting multiple names for one mechanism as rivals, mistaking a graph omission for reality, and converting a provisional creative end into owner intent. When these errors could change the inquiry, challenge the current frame, inspect an original source, seek a genuinely discriminating observation, or stop for an epistemic/authority boundary. Do **not** conduct an endless investigation because uncertainty remains in principle.

Useful completion may be:
- **Explained within source limits:** one or more hypotheses well supported under declared conditions, with remaining uncertainties.
- **Unresolved with useful discriminator:** the next observable check and its expected discriminating effect are identified; actual execution is separately warranted.
- **Unresolved without worthwhile next probe:** further evidence is unavailable, excessive or not decision-changing.
- **Productive divergence:** a new question or source-linked candidate expression exists, still provisional.
- **No new expression / no change:** the original question remains sufficient; decline unnecessary creativity.

Keep evidence status, actual source exposure, producer/assessor and inability to prove a causal creative advantage explicit.

## Optional compact output pattern

Use proportionate prose, a short table or this structure when relationships would otherwise be lost:

```text
Target / source boundary:
Explandum (observed vs inferred):
H1 / H2 (and other materially plausible accounts):
Grounds for/against each, including unassessed:
Assumption that changes the contrast:
Discriminating question (not run unless actually executed):
Changed question or possibility, if any:
Historical predecessor / current disposition:
Uncertainty, authority, stop:
```

This pattern is **not** a registered artifact, machine-readable schema, mandatory output, private cognition trace or scoring protocol. In ordinary source-grounded work, a few careful sentences may be sufficient.

## Evidence ceiling and ownership

Authored explanation accounts establish **what an agent says and cites**, not the internal cognitive cause of its output. A documentation link can show the guide exists, not that a fresh host loaded it. A well-differentiated response is not evidence that this methodology outperforms source-only reasoning. Maintain the target's own governing authority, source currentness, data boundaries and consent requirements. The active agent controls warrant, continuation and authorized work; explanations or possibility records never grant permissions.

**Leave conditional consequence depth, convergent evaluation, strategic adoption and implementation to their separately warranted owners.**
