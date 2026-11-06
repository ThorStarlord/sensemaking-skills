# Evidence-Grounded Abductive & Divergent Reasoning — Competency/Fit v1

**Date:** 2026-11-06  
**Status:** documentary competency assessment / source reconstruction; not a tested agent-ability benchmark, runtime qualification or evidence of a missing parsed ontology feature.  
**Source baseline:** `ThorStarlord/sensemaking-skills@c6a9562b07b948aa07b7bb68e8bdeb1f37cb8f52`.  
**Sources:** [Layered Ontology](ontology.md), [epistemics](relations-and-epistemics.md), [Reasoning Model](reasoning-model.md), [Divergent Exploration](divergent-exploration-ontology.md), [prospective reasoning](prospective-reasoning-ontology.md), [Cognitive Orientation](cognitive-orientation-crosswalk-v1.md), [connected inquiry](connected-prospective-inquiry-ontology.md), [source cases](evidence-grounded-abductive-divergent-reference-cases-v1.md).

## 1. Decision: is a new ontology or machine contract necessary?

**Result:** the existing ontology supports the **five requested distinctions in source-addressable prose and the existing Claim/Hypothesis/Provenance structure**. There is **no demonstrated loss of a necessary meaning under the current Level-2 conceptual representation**. A new parsed claim kind, graph predicate, sidecar file, mandatory proof tree, explanation reasoner or knowledge-store migration would currently be speculative.

**There is, however, a *methodological/documentary integration gap*.** The current divergent guide is explicit about questions, frames and meaningful alternatives, and the epistemic model is explicit about grounding each claim, but there was no single conditional portable method requiring explanation-specific contrast: *same explandum, different explanatory mechanisms, evidence for/against each, outcome-sensitive discriminator, and revision without false convergence*. A dedicated **conceptual composition with an agent-facing guide** fills that smaller gap while reusing existing meanings. It is not a new semantic authority or separate Skill.

This is an assessment of expressibility and guidance, **not** an observation that ordinary agents failed every competency or that this composition improves creative outcomes.

## 2. Five requested capabilities: fit and remaining distinction

| Requested capability | Existing semantic support | Concrete representational test | Disposition |
| --- | --- | --- | --- |
| Multiple competing explanations of the **same observation** | `Observation`, `Hypothesis`, `InquiryQuestion`, `ExploratoryJudgment` | Case A records A.O1 with A.H1/H2/H3 without treating those as separate observed events. | **EXPRESSIBLE**; portable explanatory-contrast guidance needed. |
| Evidence supporting/challenging **each** explanation | `EvidenceSource`, `CounterEvidence`, `Claim`, epistemic status + currentness | Case A attributes framing evidence to H1 and the partial-status read to H2, refusing exclusive causal proof; Case B preserves an independent critic's limited judgment. | **EXPRESSIBLE**; method must forbid citation-only support and unobserved negatives. |
| Assumptions changing an explanation's plausibility | `Assumption`, `ExplorationFrame`, `Hypothesis`, provenance/temporal status | Case A's proposed new-run discriminator separates complete-context availability from unknown historical cause; Case C contrasts fixed-vs-changed desired end. | **EXPRESSIBLE**; condition sensitivity needs explicit application. |
| Revision of explanations and *discriminating evidence* | `InquiryQuestion`, `TransformationAccount`, `ExploratoryJudgment`, revisions and provenance | Case A.Q1 names an observation whose outcomes would narrow hypotheses; Case B documents later rule change without retroactive overwrite. | **EXPRESSIBLE** as documentary question and revision; no automatic observation selector exists or is currently warranted. |
| New product possibilities from explanation | `CandidateExpression`, `PossibilityLandscape`, `ProductPossibility`, `TransformationAccount` | Case C distinguishes changed narrative end (C1) from changed mechanism (C4); Case D illustrates justified no-broadening. | **EXPRESSIBLE**; creative interpretation is still speculative, not proven user value. |

**Decision-changing distinction:** a mere list of alternative interpretations is not an *explanatory contrast* unless the agent also identifies what common evidence is being explained and how observations would affect the candidates. Existing semantics permit that record; current portable methodology does not consistently call it out.

## 3. Local competency questions (not automatic validation fields)

| ID | Question a future reader should be able to answer | Current documentary fit | Case |
| --- | --- | --- | --- |
| EAD-01 | Which exact source-scoped event/claim is the explanandum, rather than an interpretation? | Existing Observation / Claim / EvidenceSource | A.O1 |
| EAD-02 | What rival explanations are genuinely different *under the same question*? | Existing Hypothesis + attributed contrast | A.H1/H2/H3 |
| EAD-03 | What evidence supports one explanation without proving it exclusively? | EvidenceSource + source-specific interpretation | A.E1 |
| EAD-04 | What challenge/counterevidence or absence-of-assessment limits another? | CounterEvidence / epistemic UNRESOLVED / NOT_ASSESSED distinction | A.E1, D |
| EAD-05 | Which premise is hypothetical versus observed or owner-ratified? | Assumption / RatifiedIntent / epistemic status | A.H2, C |
| EAD-06 | What observation would *discriminate* the hypotheses and how would outcomes differ? | InquiryQuestion + scoped conditional account | A.Q1, B.Q1 |
| EAD-07 | How do we preserve the historical explanation when evidence changes it? | TransformationAccount + authored predecessor and revisions | B history |
| EAD-08 | What is still unresolved after a discriminator is proposed but not run? | InquiryQuestion / UNRESOLVED + provenance | A.Q1 |
| EAD-09 | What alternative question opens from an explanatory hypothesis without becoming an accepted goal? | InquiryQuestion / CandidateExpression | A.T1 |
| EAD-10 | Is the new expression a changed desired end, changed mechanism, or mere restatement? | ExplorationFrame / CandidateExpression / ExploratoryJudgment | C, B |
| EAD-11 | Can divergence and explanation stop independently with bounded scope? | ExplorationInquiry + attributed judgment and stop rationale | D |
| EAD-12 | Can a later independent agent reproduce semantic application without the author telling it the answer? | **NOT ESTABLISHED** by documentary semantics | None |
| EAD-13 | Is there a causal or comparative improvement over source-only reasoning? | **NOT ESTABLISHED** and would need a different evidence design | None |

For EAD-01..11, "fit" means **a reader can reconstruct the distinction from authored records and source links**. It does not mean the active agent will discover, verify or spontaneously perform it. EAD-12/13 explicitly require outside evidence that this module does not supply.

## 4. Alternative implementations considered

| Alternative | Value | Why selected/not selected |
| --- | --- | --- |
| Do nothing; rely on existing references | Zero maintenance and all meanings are in principle expressible | Misses the *real* portable explanatory-contrast discipline and makes the user reassemble several guides. |
| **Compose a documentary conceptual ontology plus conditional reference** | Makes rival evidence, assumption sensitivity, discriminator and creative hinge discoverable without changing protected schemas | **SELECTED**: source-appropriate, bounded, maintainable and compatible. |
| Add new first-class `ExplanationSet`, `Discriminator`, `abductsTo` graph predicate and query CLI | Could eventually aid machine-queryable comparisons | **NOT WARRANTED NOW**: no observed producer/consumer loss under existing prose/Claim/Hypothesis; identity, migration, false confidence and conformance costs are unearned. |
| Add a universal abductive agent/reasoner or compulsory multi-stage chain | Mechanically visible transitions | **REJECTED**: violates agent-native semantic controller and risks mistaking generated form for explanatory truth. |

## 5. Scoped proof/qualification matrix

| Claim | Source evidence available now | Ceiling |
| --- | --- | --- |
| Ontological expressibility | Conceptual mapping and cases A–D | **DOCUMENTARY FIT**, not machine parsing test |
| Actual historical source behavior | Build Loop owner-supplied case; Auteur two dated evaluation documents | **SOURCE-REPORTED** events, not independently rerun here |
| Ability to retain this explanation | New readable source documentation on a Git branch/merged revision when integrated | **PROVENANCE OF AUTHORED CONTENT**, not true explanation |
| Host can load the optional reference | Reference path and conditional agent-facing entry when merged | **SOURCE/DISTRIBUTION CONFIGURATION ONLY**; not host load evidence |
| Independent abductive reasoning | No distinct fresh coding-agent run with uncued source task | **NOT RUN** |
| Improvement relative to ordinary source-only reasoning | No matched comparison or human evaluation | **NOT ASSESSED** |
| New product value from creative hypotheses | Auteur C1–C4 are hypotheses, not observed author preference | **NOT ASSESSED** |

The current construction-phase `CLAUDE.md` directs **source/diff review, no locally added/manual unit or synthetic evidence tests, and truthful NOT_RUN**. Hosted CI is unmodified; its exact-head results, if observed, establish only their checked scopes.

## 6. Expansion and stopping criteria

Reopen schema evolution **only** if an actual producer/consumer demonstrates an answer or distinction that cannot be reconstructed from existing typed Claims, Hypotheses, provenance, references, authored transformations and source reports. Supply exact failing question, competing representations, stable identity, relation endpoints, migrations, backwards compatibility, real consumers and owner/schema authorization under [Steward schema evolution](../../skills/repository-semantic-steward/references/schema-evolution.md).

Reopen agent guidance if a normal use with a legitimately loaded reference demonstrates a material confusion (for example, citation-only explanation, incorrect rivalry, or claimed proof after an unexecuted discriminator). Do not infer that from a single same-author document.

**V1 decision:** integrate the conceptual profile and conditional portable method; preserve `NO_NEW_MACHINE_SCHEMA / NO_NEW_KNOWLEDGE_PACK / NO_NEW_CONTROLLER`. An independently valuable qualification inquiry may follow when a suitable real host and decision hinge exist, but it is not automatically a completion gate.
