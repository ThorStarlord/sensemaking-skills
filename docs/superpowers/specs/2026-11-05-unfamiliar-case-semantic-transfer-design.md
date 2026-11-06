# Independent Semantic Transfer — Unfamiliar Atlas Case

**Status:** Revised 2026-11-05 to a normal-use-first method. Planning only: this revision performed no agent observation, changed no model, and does not qualify Sensemaking. The [first-use result](../../normal-use/2026-11-05-ontology-author-reader-first-use.md) (`PARTIAL`) is unchanged. **Procedure:** [revised execution procedure](../plans/2026-11-05-unfamiliar-case-semantic-transfer.md).

**Why revised.** The first version made distinct host sessions, source-occluded reading and a five-axis pass gate mandatory for any judgement of Sensemaking's value. Those arrangements answer narrow questions about continuity, representation and causal attribution. They do not answer the product question, which is whether retained knowledge helps a coding agent in ordinary repository work. This version makes ordinary work the default evidence and keeps the earlier arrangements as optional diagnostics. The governing rule is [Experiment Economy & Proportional Rigor](../../../skills/using-sensemaking/references/experiment-economy-v1.md): use the lowest-cost evidence strong enough for the decision and the claim actually being made.

## 1. Three claims, evaluated separately

| Claim | Question | Evidence that fits | Controls warranted by default |
| --- | --- | --- | --- |
| **A. Practical usefulness** | Can retained knowledge help a coding agent understand, challenge or improve a real repository during ordinary engineering work? | Normal-use episodes (section 3) | None beyond honest observation. Normal context, existing documents, earlier agent work, installed Skills, repository history and imperfect sources are the environment the product must serve. |
| **B. Knowledge continuity** | Can an agent recover and use knowledge that earlier work persisted, when it lacks that work's conversation? | A genuinely later session that records what it retrieved and from where | No inherited transcript, scratchpad or answer-bearing memory from the earlier work. Normal repository and source access stay available. [ADR 0031](../../adr/0031-persistent-semantic-stewardship.md) asks for this evidence from genuinely separate episodes. |
| **C. Ontology-specific causal contribution** | Does typed, source-linked knowledge improve outcomes beyond what a capable agent achieves with ordinary documentation, retrieval and reasoning? | A matched comparison with pre-stated outcomes, adjudication and replication | Research-grade controls: matched conditions, condition isolation, pre-specified or blinded adjudication. Warranted only by a decision that needs this attribution. |

A result for one claim does not establish another. A successful pre-source paraphrase does not show usefulness (A). A normal-use episode does not show that knowledge carried across sessions (B) or caused an outcome (C).

## 2. Assumptions reassessed

| # | Assumption in the first version | Disposition | Reason |
| --- | --- | --- | --- |
| 1 | Distinct author, reader and reviewer sessions are always necessary | Rejected as a default | Needed for claim B and for contested fidelity adjudication. Not needed to judge usefulness, where the realistic agent is the one doing the work. |
| 2 | Reading source before interpreting stored knowledge is undesirable | Rejected | Checking a record against its source is part of ordinary use. Only the representation diagnostic (D-REP) asks for a source-free first pass. |
| 3 | Independent semantic paraphrase is an adequate proxy for engineering usefulness | Rejected | A paraphrase tests comprehension of a record. Usefulness appears in decisions, rejected alternatives, corrections and outcomes, which ADR 0031 names as its success conditions. |
| 4 | Imperfect repository conditions are methodological contamination | Rejected as a default | Competing documents, history and installed Skills are operating context. Contamination matters only when it makes a specific inference unreliable ([Experiment Economy](../../../skills/using-sensemaking/references/experiment-economy-v1.md) section 7). |
| 5 | More isolation always yields more valuable evidence | Rejected | Isolation lowers realism and adds setup and interpretation cost. Cleaner evidence about an unrealistic setting can be less decision-relevant (Experiment Economy section 6). |
| 6 | An unresolved question automatically warrants another experiment | Rejected | A warranted experiment needs a decision that its plausible outcomes would change (Experiment Economy section 2). |
| 7 | A successful mechanical or semantic-transfer observation establishes better engineering judgment | Rejected | Mechanical validity is not semantic truth. One paraphrase pass is not engineering benefit. One case supports only that case. |

**Retained:** the exact-commit retrieval check, which is cheap and decision-relevant whenever a record is cited; source verification as a normal step; labelling any prompted reading as prompted; a selection rule recorded before outcomes are seen; independent review when a fidelity verdict is contested; keeping negative observations.

**Changed:** the five-axis gate becomes a checklist of which evidence a claim needs, not a universal pass requirement. A case's originality matters only to a diagnostic that depends on prior non-exposure. Normal use of knowledge that already exists is the product working, not contamination.

**Withdrawn as mandatory:** source-occluded reading for every case; isolated scratchpads and distinct host identities for normal-use episodes; `NOT_RUN/BLOCKED` for a normal-use episode merely because the available host shares a parent session.

## 3. Normal-use method

Preferred loop:

```text
real repository goal
-> ordinary agent work (normal context, Skills, sources, history)
-> observed use of retained knowledge, when the agent judges it useful
-> source-grounded reasoning and decision
-> evidence reconciliation
-> warranted next responsibility
```

Rules:

- **Real goal.** The goal is an owner request or an engineering responsibility the agent actually faces. A question asked only to test the knowledge is a diagnostic prompt, not an episode.
- **Free use.** The agent may read sources, search and inspect history, reject retained knowledge that is wrong, reconsider earlier decisions, decide that existing evidence is enough, or skip retrieval for a simple task. Avoiding unnecessary retrieval is not a failure. The method must not require knowledge to be used in order to show that it is used.
- **Selection rule first.** Record why this repository and task were chosen before the outcome is known.
- **Reconcile.** Retain, revise or reject the knowledge the work touched. `NO_MODEL_CHANGE` is a valid result.

Earlier same-agent records of this kind already exist, for example [ontology-first entry on Atlas](../../normal-use/ontology-first-entry-atlas-001.md) and [creative prospective discovery](../../normal-use/2026-11-02-creative-prospective-discovery.md). Both state that they are not independent trials, and that limit still applies to them.

## 4. Bounded episode observation

An episode needs a short note, not a score. The note records what the claim needs from these dimensions:

- **Relevance:** whether retained knowledge surfaced something material to the actual responsibility, with the record IDs or queries used.
- **Grounding:** whether the agent separated authoritative sources, observations, inference and uncertainty, with the sources it opened.
- **Interpretation:** whether it read recorded relations without inventing stronger dependencies, for example treating a `references` edge as necessary support.
- **Reconciliation:** whether it found and corrected conflicts with current repository reality.
- **Decision contribution:** whether knowledge changed a choice, explanation, alternative or selected responsibility. Cite the artifact where the effect appears (decision note, diff, report).
- **Outcome:** whether the engineering result was useful and verified, with NOT_RUN items named.
- **Cost:** retrieval, maintenance and procedural overhead relative to benefit.
- **Negatives:** irrelevant retrieval, outdated or misleading records, knowledge that was ignored, and unnecessary overhead. Keep them.

Attribution rules:

- Retrieval is not use, and use is not benefit. Credit knowledge with an effect only where an artifact or the agent's reasoning shows it.
- Keep observed effects (commands, diffs, reports) separate from the agent's retrospective account.
- Name the ceiling: one task, one agent, host and model, one repository revision.
- No numeric scores, episode quotas or mandatory counterfactuals. A counterfactual (the same task without retained knowledge) is worth its cost only when the decision depends on attribution, which normally means claim C.

## 5. Optional diagnostics

A diagnostic runs only when its named trigger holds. Each gives a minimal arrangement. None is a default.

**D-CONT: cross-session continuity (claim B).**
- Trigger: a decision or owner claim depends on whether persisted knowledge can stand in for missing conversation.
- Arrangement: a later session that is genuinely new (a new host session, or a fresh agent without the earlier transcript, scratchpad or answer-bearing memory), with normal repository and source access. It records its retrieval trace.
- Note: once a continuity claim is actually being made, ordinary later sessions can supply this evidence without a dedicated run, provided they meet the arrangement above.
- If inherited context contains the answer, record the result with that ceiling. Do not count it as continuity.

**D-REP: representation sufficiency (a narrow question inside claims A and B).**
- Trigger: a schema, record-format or authoring-guidance decision depends on whether records can be interpreted without their sources.
- Arrangement: a reader given only the retrieved records gives an account of explicit claims, relations, provenance and uncertainty. In a separate step it then checks the original sources. The result is labelled `PROMPTED_REPRESENTATION`. Any source read before the first account invalidates that account as representation evidence.

**D-FID: authoring fidelity (reliability of a record).**
- Trigger: a record's claims are disputed, high-consequence, or proposed for reviewed status.
- Arrangement: a reviewer that did not author the record checks material claims against the source at the exact revision, and classifies support, scope and missing nuance. A distinct host session is preferred when the verdict is contested. Mechanical proposal checks stay separate from this review.

**D-CAUSAL: causal or comparative attribution (claim C).**
- Trigger: the owner must decide whether the ontology adds value beyond source-only work or ordinary documentation.
- Arrangement: matched tasks under both conditions, with outcomes and adjudication criteria fixed before running, condition isolation and replication. This is research-grade. This revision supplies no design for it.

## 6. The Atlas companion Shared Memory case

The case remains a candidate, not a compulsory fixture or an answer key. It is worth using only if an owner or a real engineering responsibility needs the question answered; then it is an episode under section 3. If a diagnostic uses it, the selection is recorded before any observation. PR 768 recorded that the case lies outside the six inspected Atlas knowledge packs at the pinned revision. This revision did not work in Atlas and does not re-verify that. The neutral question may stay as written:

> In Atlas, how should companion Shared Memory relate to Saga History and durable player progression, and what is supported by the current repository versus specified or not assessed?

## 7. Relation to the first-use result

The [first-use readout](../../normal-use/2026-11-05-ontology-author-reader-first-use.md) remains as recorded (`PARTIAL`). Under this method its two failing axes read as follows. Author fidelity found one false as-built clause and one inherited overstatement. The first answer missed both, and the source check on the second pass caught them. That is a candidate defect, not a verdict on usefulness. Reader interpretation before source checking was not observed because the neutral question did not request a representation pass. That gap matters only if D-REP is warranted. The viewer defect that run exposed was repaired in [PR #767](https://github.com/ThorStarlord/sensemaking-skills/pull/767) and is not part of this method's result.

## 8. Warrant for an isolated run now

Applying the Experiment Warrant Gate ([Experiment Economy](../../../skills/using-sensemaking/references/experiment-economy-v1.md) section 2):

- **Unresolved decision:** whether the semantic-knowledge path should keep investing in authored records. ADR 0031 and `STATUS.md` leave this open until there is evidence of practical value.
- **Discriminating outcome:** a pre-source paraphrase result, pass or fail, would not change that decision. Its only consequence is a representation guidance adjustment, which is cheap, reversible and observable in ordinary use.
- **Cheaper route:** ordinary episodes (section 3) address the decision directly, at lower cost.
- **Precedent:** the one pre-registered pair so far, [operational qualification 001](../../normal-use/operational-qualification-001.md), gave a weak, unreplicated reuse signal (see `STATUS.md`). That is a reason to keep controlled comparisons tied to a real decision, not a reason against normal use.

**Conclusion:** no isolated unfamiliar-case run is warranted now.

## 9. What this revision does not establish

- It is a methodological revision. It is not empirical qualification of Sensemaking, and it does not show practical usefulness, continuity or causal benefit.
- It relaxes isolation for claim A. That raises the risk that a favourable episode is credited to knowledge it does not show. The attribution rules in section 4 limit this but do not remove it.
- Claims B and C remain untested. ADR 0031's condition of genuinely separate later episodes is still open.
- Self-report can flatter a tool. The observation rules narrow that without eliminating it.

## 10. Product identity

The ontology helps coding agents retain, retrieve, challenge, reconstruct and apply accumulated repository understanding ([ADR 0031](../../adr/0031-persistent-semantic-stewardship.md), [ADR 0034](../../adr/0034-ontology-first-adaptive-sensemaking.md)). It is not a semantic truth oracle, not the primary authority for product decisions, and not a substitute for current source inspection. Its value shows in warranted reasoning and useful outcomes. It does not show in the number of records retrieved or the fidelity of isolated paraphrases.

## 11. Next responsibility

**`NO_FURTHER_INQUIRY`** for the isolated unfamiliar-case run (section 8).

The next ordinary responsibility is to take up any authentic repository task that retained knowledge bears on, work it normally, and record an episode under section 4. No diagnostic is currently warranted. If a continuity claim is later made, a genuinely separate session can supply D-CONT evidence at that point.
