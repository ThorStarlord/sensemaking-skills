# Inquiry method reflection: multiple divergent passes and durable documentation

**Status:** non-authoritative methodological reflection. It does not change `using-sensemaking`, the Strategic Exploration Funnel, repository policy, runtime architecture, or authority requirements.
**Origin:** owner-supplied discussion summarized 2026-11-02, concerning one prompt per inquiry mode, repeated Divergent Explorations, qualitative diminishing returns, and cumulative documentation. This is a *reasoned interpretation*, not a verbatim reproduction of the attached conversation.
**Source-reviewed context:** [ADR 0034](../adr/0034-ontology-first-adaptive-sensemaking.md), [prospective reasoning ontology](../semantic-architecture/prospective-reasoning-ontology.md), [Strategic Exploration Funnel](../../skills/strategic-repository-analysis/references/strategic-exploration-funnel-v1.md), [Creative Prospective Discovery](../../skills/strategic-repository-analysis/references/creative-prospective-discovery-v1.md), [Idea Library](../idea-library.md).
**Navigation:** [exploration atlas](README.md), [generative-depth record](2026-11-02-generative-depth-repository-knowledge.md), [divergent record](2026-11-02-divergent-repository-knowledge.md).

## 1. User argument reconstructed

The submitted argument favors **slow, explicit, inspectable reasoning while the inquiry methodology itself is developing**. It makes the following distinctions:

- A single monolithic prompt may blend divergence, convergence and depth before the possibility space has grown.
- Separate passes clarify which reasoning objective a given exploration serves; an agent may coordinate them later without executing all reasoning modes simultaneously.
- One prompt per reasoning objective **does not imply** one prompt per strategic stage or human approval after every pass.
- Repeated Divergent Exploration should use changing lenses (broad coverage, neglected regions, assumption inversion, analogy, fresh independent exploration), not repeat the same prompt unchanged.
- Choosing the next area for **exploratory coverage** is not Convergent Evaluation of which product idea to implement.
- Diminishing returns concern genuinely *new conceptual dimensions*, not raw candidate quantity.
- Documentation separates exploration records, curated possibilities and authoritative decisions.
- Creative outcome and inquiry-method quality should be observed **separately**.

These are substantive method arguments, not an already selected new product process.

## 2. Merits of the argument

**Preserves divergence.** The user can notice when candidates are prematurely dismissed or when depth analysis quietly turns into preference selection. Distinct inquiries make intellectual boundaries visible.

**Enables cumulative creative work.** A later exploration can refer to precise earlier candidate ideas, overlaps and unanswered questions. It need not rebuild everything from conversational memory.

**Preserves agent autonomy.** A single delegated instruction can contain multiple explicit, distinct inquiries while retaining agent-owned semantic control. Human review is necessary only where authority is actually reserved or the owner chooses to supervise.

**Makes method learning legible.** A productive candidate and a strong inquiry method are different claims. A poorly structured pass can find a useful idea by luck; a carefully performed pass can correctly find little novelty.

**Works with current architecture.** [Prospective reasoning ontology](../semantic-architecture/prospective-reasoning-ontology.md) already distinguishes activity operation, domain, and DIVERGENT/CONVERGENT plus BREADTH/DEPTH orientation. Thus “separate modes” need not introduce a new runtime phase machine.

## 3. Limitations and important refinements

**Inspectability is not guaranteed by prompt count.** A long, single agent answer can still contain independently documented passes; two separately issued prompts can still be contaminated by premature convergence. The relevant unit is a *clearly bounded inquiry with inspectable output*, not a message count.

**Stage separation is contextual, not universal.** ADR 0034 deliberately enables adaptive composition and revisiting earlier reasoning. Ordinary bounded work must not be forced through manual divergence cycles.

**No mandatory number of passes.** The supplied A/B/C/D/E examples are alternative creative lenses, not a five-pass gate, quota or mature process contract.

**A shrinking novelty count can mislead.** One genuinely new experiential dimension can be substantial; many differently phrased candidates can be repeats. Qualitative coverage, original sources, novelty distinctions and remaining conceptual blind spots matter more than bar charts or scores.

**Autonomous coordination could still hide mode mixing.** Delegating several inquiries at once can be efficient, but the reports must preserve which operations produced which conclusions. Nothing here establishes a reliable autonomous exploration orchestrator.

**Historical documentation is not creative proof.** Preserving ideas makes them findable, but does not establish that a later independent agent retrieved, critically used or improved an outcome because of them. Existing R6/S5 limitations remain as stated in [STATUS](../../STATUS.md).

**Knowledge growth may anchor future passes.** A candidate library can narrow imagination. A later agent may explore independently before consulting the atlas, then use it to detect relationships and possible restatements.

## 4. Optional lenses for multiple exploratory passes

The following are *examples*, not prescribed sequence or minimum coverage:

| Inquiry lens | Creative aim | What to keep separate |
| --- | --- | --- |
| Broad divergence | Map candidate user experiences, mechanisms and product identities | Avoid ranking or converting to a construction path |
| Negative-space exploration | Search important dimensions omitted from earlier passes | Missing record is `NOT_ASSESSED`, not evidence of absence |
| Assumption inversion | Explore futures that require explicit counterfactual premises | Counterfactual status vs current ratified commitments |
| Cross-domain analogy | Recombine useful mechanisms or analogy failures | Source scope and target-repository authority |
| Independent fresh interpretation | Generate ideas without beginning from the current idea catalogue | Later similarity/novelty comparison vs unconstrained guessing |
| Unresolved-question exploration | Produce new questions from previous decisions and surprising tensions | A question is not an accepted user goal |
| Developer-experience exploration | Imagine user interactions rather than new graph storage | Desired product outcome vs an implementation design |

A later session can open another lens, repeat one with a genuinely different question, or explore a different dimension entirely.

## 5. What diminishing returns can and cannot mean

A useful qualitative reflection asks:

- Are additional passes exposing previously unrepresented **conceptual dimensions or product outcomes**?
- Are several pass outputs mainly renamings or small variants of earlier records?
- Would a different lens plausibly reveal a meaningful region currently unexamined?
- Did retained earlier knowledge enable new combinations, or did it merely reproduce known ideas?
- Are unresolved important questions still opening materially different futures?

These questions help describe coverage; they are **not** an algorithm, score or automatic transition trigger. In particular, a local decrease in originality does not grant permission to enter Convergent Evaluation, select an architecture or reopen Level 3.

## 6. Documentation model

**Exploration records** remain attributable, chronological and epistemically explicit. They retain the actual inquiry focus, sources, alternatives, variants and unresolved dimensions.

**The [exploration atlas](README.md)** is a changeable navigation view over them. It can group related concepts and point at overlaps without declaring a preferred direction.

**The [Idea Library](../idea-library.md)** selectively preserves distinct, source-reviewed ProductPossibilities with stable `poss:` identities when a separate reconciliation warrants it. Speculative local IDs are not automatically promoted.

**Decision and governing documents** separately record owner and agent decisions under the applicable authority. They are not edited merely because an exploration is interesting.

For newly authored passes, lightweight useful fields may include: inquiry question and orientation, source revision and original evidence, speculative vs observed statements, distinctive candidates and relations, overlap with earlier passes, open dimensions and a clear non-selection statement. These are *documentation suggestions*, not a new schema or validator contract.

## 7. Two kinds of learning: do not conflate them

| Inquiry outcome | Question to preserve | Claim not implied |
| --- | --- | --- |
| Product/creative learning | What new user experience, capability or product meaning was imagined? | The idea is valuable, novel in the world or should be built |
| Methodological learning | Which lens, question or separation made a discovery possible or exposed repetition? | The method is generally reliable, superior or qualified across independent agents |

For example, an idea about a temporal-echo game mechanic is a **hypothetical product possibility**. A reflection that a prohibited-behavior lens generated the idea is a **method observation in this conversation**, not evidence that the lens performs reliably across sessions.

## 8. Open methodology questions (not selected process changes)

- When is an independent pre-recall exploration useful, and when does it waste attention or repeat source work?
- Can one multi-pass delegation preserve mode separation as clearly as separate owner-initiated inquiries?
- Which documents should later agents read first to avoid being anchored yet still benefit from history?
- What form of cross-pass conceptual links is sufficient without creating a new schema?
- How can one distinguish a novel product *goal* from a novel description of an existing possibility?
- What evidence would eventually show that one pass made a later pass more creative, rather than merely more familiar with earlier words?

**Status of the maturity-stage discussion:** “explicit passes -> assisted coordination -> adaptive orchestration” is a way of thinking about method evolution, **not** a three-phase roadmap, product commitment, required workflow or argument for new orchestration machinery.

**End state:** useful process reflection, no new mandatory controller logic, no automatic convergence, no authorization to build.
