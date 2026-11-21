# Divergent Exploration — First usable experiences for a Sensemaking-enhanced DeepSeek Harness

**Date:** 2026-11-06. **Operation:** Divergent Exploration. **Guiding question:** What could we do? **Outcome:** bounded Possibility Space.

**Status:** exploratory, non-authoritative candidate expressions. This is **not** a coverage assessment, ranking, selected MVP, product architecture change, strategic disposition, backlog, implementation plan or merge/deployment authorization.

**Inquiry identity:** DE-HARNESS-FIRST-2026-11-06. **Assessor / author:** ChatGPT working from explicitly provided user intent and directly inspected repository documentation. **Prior exposure:** the owner's Option C framing and exploration seeds were visible; this is not a blind independent discovery trial. **Novelty scope:** assessed only against sources named below; general originality and user value are NOT_ASSESSED.

## A. Exploration framing

### User problem and authority

The open question is not 'which agent architecture wins?' but **what valuable first usable experience an owner could delegate, what result they would actually receive, and what human attention would be needed before delivery**. Some experiences end with understanding, others with an option space, a proof or a PR, and some with continued authorized work. No experience is preselected.

Option C separates three *potential* layers: a coding-agent host/execution foundation (DeepSeek Harness is a candidate, not a commitment), ontology-grounded Sensemaking for reasoning and source-linked knowledge, and optional long-lived coordination. Existing work in the superagent prototype and Dark Factory supplies **evidence of adjacent mechanisms**, not permission to merge those architectures.

**Current authority boundary:** accepted Sensemaking ADR 0034 makes understanding/prospective reasoning a legitimate terminal output and leaves implementation downstream and separately authorized (S2). The established Sensemaking/Dark Factory agreement says Dark Factory owns the canonical **durable software-factory runtime**; Sensemaking must not grow a competing Goal/Frontier/Campaign controller (S4). Dark Factory's own ADRs distinguish Intent Authority, Current Warrant, Action Authority and Transition Authority (D3–D5). A DeepSeek execution host, if used, does not acquire protected permissions by virtue of its technical capability.

### Source snapshots and capability classification

All references below are immutable blob links from the inspected branch heads, **not a claim of live execution in this inquiry**:

| Repository | Inspected branch head | Grounded current reading |
| --- | --- | --- |
| Sensemaking Skills | main at 112463aa993174f87d99add569eeb9a531fdead8 | Ontology-grounded agent-native guidance, typed knowledge/query surfaces and retained exploration references exist; independent creative or longitudinal advantage is not demonstrated by the cited status records (S1–S5). |
| Official DeepSeek Harness | master at fcc0ad462172522aaf5c93a7b2e01f6b9f0b0159 | Developer-preview plugin-first runtime with Web/headless/SDK/ACP compositions, model/tool/session seams and subagent providers in source/docs (H1–H5); its safety notice explicitly says it is not audited or production-ready (H6). |
| dsh-superagent-prototype | main at 6337fc823ce20251c8de8085948165c81aaa701e | Research-prototype code/docs for GitHub/Feishu triggers, policy admission, Tickets/Mandates, worker Sessions and an attention-minimizing panel (P1–P5). Not an official DeepSeek product and not independently production-qualified here. |
| Dark Factory | main at 60d50c3ee555556223be6be7e26726c7cbef4f6b | Accepted canonical factory runtime, implemented Campaign/Goal-related capabilities and bounded historical E2E-6 serial fixture qualification; a later real-work Organic attempt is budget-exhausted/unqualified (D1–D7). Qualification does not transfer to a DeepSeek integration. |

**Source map**

| ID | Exact-revision source | What it warrants |
| --- | --- | --- |
| S1 | [README.md](https://github.com/ThorStarlord/sensemaking-skills/blob/112463aa993174f87d99add569eeb9a531fdead8/README.md) | Product identity, implemented semantic plane, and unproven cross-session benefit |
| S2 | [docs/adr/0034-ontology-first-adaptive-sensemaking.md](https://github.com/ThorStarlord/sensemaking-skills/blob/112463aa993174f87d99add569eeb9a531fdead8/docs/adr/0034-ontology-first-adaptive-sensemaking.md) | Accepted ontology-first identity, one agent-native semantic controller, implementation optional |
| S3 | [skills/strategic-repository-analysis/references/divergent-exploration-v1.md](https://github.com/ThorStarlord/sensemaking-skills/blob/112463aa993174f87d99add569eeb9a531fdead8/skills/strategic-repository-analysis/references/divergent-exploration-v1.md) | Divergent inquiry, possibility identity, attribution, source scope, and stopping guidance |
| S4 | [docs/dark-factory-autonomy-boundary.md](https://github.com/ThorStarlord/sensemaking-skills/blob/112463aa993174f87d99add569eeb9a531fdead8/docs/dark-factory-autonomy-boundary.md) | Sensemaking versus Dark Factory canonical runtime ownership |
| S5 | [STATUS.md](https://github.com/ThorStarlord/sensemaking-skills/blob/112463aa993174f87d99add569eeb9a531fdead8/STATUS.md) | Source-implemented knowledge and bounded qualification; evidence ceilings |
| S6 | [skills/strategic-repository-analysis/references/strategic-exploration-funnel-v1.md](https://github.com/ThorStarlord/sensemaking-skills/blob/112463aa993174f87d99add569eeb9a531fdead8/skills/strategic-repository-analysis/references/strategic-exploration-funnel-v1.md) | Exploration-only permission to stop before Level-3 convergence |
| S7 | [docs/decision-orchestration-boundary.md](https://github.com/ThorStarlord/sensemaking-skills/blob/112463aa993174f87d99add569eeb9a531fdead8/docs/decision-orchestration-boundary.md) | Semantic work selection versus execution coordination |
| H1 | [README.md](https://github.com/deepseek-ai/deepseek-harness/blob/fcc0ad462172522aaf5c93a7b2e01f6b9f0b0159/README.md) | Official DeepSeek Harness and developer-preview notice |
| H2 | [docs/architecture.md](https://github.com/deepseek-ai/deepseek-harness/blob/fcc0ad462172522aaf5c93a7b2e01f6b9f0b0159/docs/architecture.md) | Plugin architecture, model/tool/session seams, Web/headless/SDK/ACP profiles |
| H3 | [packages/bundle/headless/README.md](https://github.com/deepseek-ai/deepseek-harness/blob/fcc0ad462172522aaf5c93a7b2e01f6b9f0b0159/packages/bundle/headless/README.md) | One-shot task and optional session-id continuation; no persistent worker implied |
| H4 | [docs/subsystems/persistence.md](https://github.com/deepseek-ai/deepseek-harness/blob/fcc0ad462172522aaf5c93a7b2e01f6b9f0b0159/docs/subsystems/persistence.md) | Durable session log interface, JSONL backend, restore constraints |
| H5 | [packages/subagent/README.md](https://github.com/deepseek-ai/deepseek-harness/blob/fcc0ad462172522aaf5c93a7b2e01f6b9f0b0159/packages/subagent/README.md) | In-process and external child-agent backends |
| H6 | [SAFETY.md](https://github.com/deepseek-ai/deepseek-harness/blob/fcc0ad462172522aaf5c93a7b2e01f6b9f0b0159/SAFETY.md) | Unaudited preview; limitations of sandbox and approval controls |
| P1 | [README.md](https://github.com/ThorStarlord/dsh-superagent-prototype/blob/6337fc823ce20251c8de8085948165c81aaa701e/README.md) | Research-prototype disclaimer, single-repository GitHub/Feishu agent use |
| P2 | [docs/001-domain.md](https://github.com/ThorStarlord/dsh-superagent-prototype/blob/6337fc823ce20251c8de8085948165c81aaa701e/docs/001-domain.md) | Trigger, Eval, Mandate, Ticket, Assignment, Subscription conceptual lifecycle |
| P3 | [docs/002-authorization.md](https://github.com/ThorStarlord/dsh-superagent-prototype/blob/6337fc823ce20251c8de8085948165c81aaa701e/docs/002-authorization.md) | Admission policy and context-versus-authority distinction |
| P4 | [docs/003-execution.md](https://github.com/ThorStarlord/dsh-superagent-prototype/blob/6337fc823ce20251c8de8085948165c81aaa701e/docs/003-execution.md) | Session/worker assignment, concurrency, setup and reporting |
| P5 | [docs/007-architecture.md](https://github.com/ThorStarlord/dsh-superagent-prototype/blob/6337fc823ce20251c8de8085948165c81aaa701e/docs/007-architecture.md) | Engine, Store, Runtime and adapter code-map |
| D1 | [README.md](https://github.com/ThorStarlord/dark-factory/blob/60d50c3ee555556223be6be7e26726c7cbef4f6b/README.md) | Factory product identity, implementation-status summary and qualification caveats |
| D2 | [docs/adr/0001-canonical-successor-product.md](https://github.com/ThorStarlord/dark-factory/blob/60d50c3ee555556223be6be7e26726c7cbef4f6b/docs/adr/0001-canonical-successor-product.md) | Accepted canonical successor product; migration by deliberate evaluation |
| D3 | [docs/adr/0002-intent-authority-model.md](https://github.com/ThorStarlord/dark-factory/blob/60d50c3ee555556223be6be7e26726c7cbef4f6b/docs/adr/0002-intent-authority-model.md) | Intent, current warrant, action and transition authorities |
| D4 | [docs/adr/0003-sensemaking-archon-boundary.md](https://github.com/ThorStarlord/dark-factory/blob/60d50c3ee555556223be6be7e26726c7cbef4f6b/docs/adr/0003-sensemaking-archon-boundary.md) | Exactly one semantic responsibility selector within the factory |
| D5 | [docs/adr/0007-post-v0-authority-and-release-boundary.md](https://github.com/ThorStarlord/dark-factory/blob/60d50c3ee555556223be6be7e26726c7cbef4f6b/docs/adr/0007-post-v0-authority-and-release-boundary.md) | Distinct Campaign, merge, deployment and rollback grants |
| D6 | [docs/architecture/delegated-autonomy-operating-model.md](https://github.com/ThorStarlord/dark-factory/blob/60d50c3ee555556223be6be7e26726c7cbef4f6b/docs/architecture/delegated-autonomy-operating-model.md) | Qualified single-fixture serial continuation and its limits |
| D7 | [STATUS.md](https://github.com/ThorStarlord/dark-factory/blob/60d50c3ee555556223be6be7e26726c7cbef4f6b/STATUS.md) | Organic workload budget-exhaustion stop and unqualified real target |

**Knowledge versus demonstration:** published docs and checked-in modules can establish declared architecture and implemented source surfaces. They do **not** prove that Sensemaking is loaded correctly under official DeepSeek Harness, that DeepSeek has been qualified as a Dark Factory executor, that the superagent is safe to deploy, or that any candidate below improves user outcomes. These integrations are hypothetical and require later inquiry.

### Dimensions deliberately varied

| Dimension | Contrasting possibilities |
| --- | --- |
| Beneficiary | Repository newcomer; individual developer; product owner; architecture reviewer; teammate; autonomous operator |
| User hands over | URL/checkout; hypothesis; ambiguous intent; specific issue; failure; abandoned project; backlog; Goal and authority envelope |
| Promised result | Explanation; decision lineage; possibility landscape; impact map; knowledge delta; evidence verdict; demo; PR; recovery; terminal Goal |
| Timescale | One command; interactive episode; revisited sessions; unattended long-lived work |
| Human relationship | Read-only without interruption; owner answers a discriminating question; reviewer accepts result; on-exception protected approval |
| Agency | No action; observe/interpret; propose; bounded write; repeated sanctioned work |
| Semantic memory | Original source only; compact selected context; Git-reviewed knowledge; historical decision re-entry |
| Host/coordination | Existing coding agent; DeepSeek headless; interactive profile; optional subagents; superagent ticket host; Dark Factory durable runtime |
| Scope | Single component; repository; cross-repository relation; team request stream |
| Trust boundary | Local read-only; sandboxed test/edit; PR publication; protected merge; production integration |

The families below group user promises, **not implementation components or candidate rankings**. The same runtime feature can serve distinct experiences; sharing a technical mechanism does not make the user ends identical.

## B. Possibility families

| Family | Underlying user experience | Core difference | Expressions |
| --- | --- | --- | --- |
| A | **Source-grounded truth on demand** | The deliverable is a trustworthy account of repository reality, not changed software. | P01–P03 |
| B | **Possible futures and prospective consequences** | The deliverable changes how product or architecture choices can be understood before acting. | P04–P07 |
| C | **Reusable understanding and human comprehension** | The product makes relevant knowledge recoverable or learnable beyond one answer. | P08–P09 |
| D | **Bounded engineering and disciplined probes** | The deliverable is a bounded code change, repaired failure, or hypothesis-testing evidence. | P10–P13 |
| E | **Warranted work selection and revival** | The product identifies the right continuation from partially specified or stale work. | P14–P15 |
| F | **Durable delegated work and attention management** | The product remains responsible across time, either for a software Goal or for team requests. | P16–P17 |
| G | **Multiple repositories and contested interpretations** | The deliverable preserves relations or disagreements that one local perspective would miss. | P18–P19 |

No arbitrary count quota was used: entries were retained where the delegated input, outcome, human relationship or substantive autonomy promise changes. Variations such as 'two subagents rather than one', 'GUI rather than terminal', or 'a hook that saves a paragraph' are **configurations**, not separate expressions unless they change the delivered user experience.

## C. Possibility catalog

Each expression is a prospective hypothesis by this inquiry's author. Its ten fields describe the intended experience; source codes give the *seed/constraint*, never proof of current integrated delivery.

### P01 — Repository cartographer

**Family:** A — Source-grounded truth on demand. **Grounding seeds:** S1–S3, S5, H2–H4. **Status:** proposed experience, not an integrated capability claim.

1. **User intention:** Understand a repository quickly without learning its internal vocabulary first.
2. **Delegated input:** A repository URL or checkout plus a request for purpose, architecture, constraints and present capabilities.
3. **Autonomous responsibility:** Inspect governing documents and relevant sources, reconcile conflicting descriptions and mark unknowns; make no changes.
4. **Tangible outcome:** A source-linked architectural and product map distinguishing established behavior, intent and gaps.
5. **Human involvement:** Only if a genuinely owner-reserved question cannot be answered from sources; no approval needed for read-only inspection.
6. **Role of Sensemaking:** Organize domain/capability/constraint relationships and distinguish authority from historical claims.
7. **Role of the runtime:** Any host with repository reads and document output; a one-shot headless runtime or an existing coding agent may suffice.
8. **Coordination needs:** One ordinary session; no persistent worker, hooks or factory.
9. **Distinctiveness:** Makes repository reality legible rather than deciding a future or producing code.
10. **Uncertainty:** Can coverage of a large unfamiliar codebase be sufficiently faithful without heavyweight indexing?

### P02 — Completion-claim auditor

**Family:** A — Source-grounded truth on demand. **Grounding seeds:** S1–S3, S5, H2–H4. **Status:** proposed experience, not an integrated capability claim.

1. **User intention:** Know whether a stated implementation or readiness claim is actually supported.
2. **Delegated input:** A PR, test result, release claim or statement such as 'the feature is finished' with its target revision.
3. **Autonomous responsibility:** Trace the claim to code, tests, receipts and missing acceptance; expose discrepancies without repairing them.
4. **Tangible outcome:** A verdict with supported, disputed and unexamined claims, exact evidence and the remaining proof boundary.
5. **Human involvement:** A person decides whether the claim is sufficient for acceptance or whether later verification is authorized.
6. **Role of Sensemaking:** Separates claims, evidence, confidence limits, authority and findings; avoids converting test success into product truth.
7. **Role of the runtime:** Read-only Git, test-log and source access; running tests is optional and separately authorized.
8. **Coordination needs:** Usually one session, with optional evidence-gathering subagents.
9. **Distinctiveness:** The value is trustworthy assurance, not an architectural map or a patch.
10. **Uncertainty:** What claims need live environments or independent user observation beyond available receipts?

### P03 — Decision-lineage re-entry

**Family:** A — Source-grounded truth on demand. **Grounding seeds:** S1–S3, S5, H2–H4. **Status:** proposed experience, not an integrated capability claim.

1. **User intention:** Resume understanding after months or after a different agent worked on the project.
2. **Delegated input:** A repository, its historical decisions or retained knowledge, and a question about what changed and why.
3. **Autonomous responsibility:** Compare current revision with cited historical choices and reconstruct supersession, unresolved tensions and source provenance.
4. **Tangible outcome:** A 'where we left off' packet with current decision anchors, invalidated assumptions and open questions.
5. **Human involvement:** Human involvement only where historical provenance is missing or a former owner preference is ambiguous.
6. **Role of Sensemaking:** Uses semantic relationships to reconstruct rationale across artifacts, not merely summarize recent commits.
7. **Role of the runtime:** Repository and history reads; may use existing exact-revision query commands, but no new service is essential.
8. **Coordination needs:** One session that consumes durable existing records; no resident agent needed.
9. **Distinctiveness:** Returns narrative continuity for a returning decision-maker rather than continuously maintaining a graph.
10. **Uncertainty:** Will older decisions be reachable, and can it avoid treating stale conclusions as current authority?

### P04 — Ambiguous-intent possibility studio

**Family:** B — Possible futures and prospective consequences. **Grounding seeds:** S2–S3, S5–S7, H2. **Status:** proposed experience, not an integrated capability claim.

1. **User intention:** Discover materially different products or user experiences before knowing what to build.
2. **Delegated input:** An incomplete goal, target repository and any nonnegotiable product identity or constraints.
3. **Autonomous responsibility:** Generate alternate beneficiaries, desired ends, assumptions and mechanisms; preserve distinct frames and incomplete questions.
4. **Tangible outcome:** A provenance-aware possibility landscape and conceptual interaction sketches, explicitly without ranking.
5. **Human involvement:** Ask only if exploration would otherwise fabricate a governing product constraint; selection belongs to a later stage.
6. **Role of Sensemaking:** Divergent Exploration supplies question/frame identity, novelty-basis caution and source-grounded reinterpretation.
7. **Role of the runtime:** Any conversational harness with source inspection and artifact writing; no runtime extension needed.
8. **Coordination needs:** One session, optionally several independent viewpoints to broaden frames.
9. **Distinctiveness:** Its output is new possible meanings of the user's intention, not code or an option score.
10. **Uncertainty:** Does the method actually create qualitatively new possibilities rather than plausible restatements?

### P05 — Latent product-goal scout

**Family:** B — Possible futures and prospective consequences. **Grounding seeds:** S2–S3, S5–S7, H2. **Status:** proposed experience, not an integrated capability claim.

1. **User intention:** Find valuable goals nobody explicitly requested but which the product's history makes plausible.
2. **Delegated input:** A repository plus decisions, constraints, contradictions, failed attempts and knowledge history.
3. **Autonomous responsibility:** Inspect underused relationships and tensions; reframe them into hypothetical new user ends without self-authorizing work.
4. **Tangible outcome:** An opportunity hypothesis dossier connecting each potential goal to the source tension that inspired it.
5. **Human involvement:** Owner later decides whether any newly imagined product goal is desirable or permissible.
6. **Role of Sensemaking:** Knowledge continuity and prospective reasoning are the generative inputs, not a guarantee of originality.
7. **Role of the runtime:** Read/query tools and an agent able to explore source-linked relations; no durable execution controller required.
8. **Coordination needs:** One analytical episode, possibly separate perspective passes.
9. **Distinctiveness:** Starts from repository evidence and uncovers unasked goals; unlike P04, the user need not supply the aspiration.
10. **Uncertainty:** Novelty, actual user demand and retained-knowledge causal benefit are presently unproven.

### P06 — Change-consequence atlas

**Family:** B — Possible futures and prospective consequences. **Grounding seeds:** S2–S3, S5–S7, H2. **Status:** proposed experience, not an integrated capability claim.

1. **User intention:** Understand potential architectural and product consequences before making a proposed change.
2. **Delegated input:** A particular change proposal, governing constraints and source revision.
3. **Autonomous responsibility:** Trace component/contract/dependency relations, develop plausible downstream consequences and label speculative links.
4. **Tangible outcome:** A source-linked impact and counterfactual map with uncertainty and affected product experiences.
5. **Human involvement:** Human decides which consequences matter and whether any change should be commissioned.
6. **Role of Sensemaking:** Supplies typed dependencies, assumptions, consequence chains and explicit uncertainty.
7. **Role of the runtime:** Repository source reads; graph query can help but simulation infrastructure is not assumed.
8. **Coordination needs:** Single session; optional isolated investigation where evidence is disputed.
9. **Distinctiveness:** Tests a specific counterfactual future rather than generating unconstrained product directions.
10. **Uncertainty:** Can consequences be usefully inferred without live probes and without overstating causal certainty?

### P07 — Architectural transformation prospectus

**Family:** B — Possible futures and prospective consequences. **Grounding seeds:** S2–S3, S5–S7, H2. **Status:** proposed experience, not an integrated capability claim.

1. **User intention:** Explore how an existing architecture could change while preserving the accepted product intent.
2. **Delegated input:** A migration aspiration such as 'separate execution from semantics' plus repository sources.
3. **Autonomous responsibility:** Map invariants, alternative boundaries, reversible constraints and incompatible assumptions; stop before architecture choice.
4. **Tangible outcome:** Several coherent transformation concepts, preserved constraints and questions that would discriminate them.
5. **Human involvement:** Architecture ownership, product-thesis revision and implementation authorization are reserved for the correct decision process.
6. **Role of Sensemaking:** Recovers historical decisions and differentiates observed coupling from actual architectural obligation.
7. **Role of the runtime:** Code/source navigation only for proposal; a migration implementation host is not required.
8. **Coordination needs:** One session or multiple bounded specialist analyses, with the active semantic owner reconciling.
9. **Distinctiveness:** Its deliverable is a changeable architectural option space, not a bugfix or selected target design.
10. **Uncertainty:** Which dependencies are hard invariants, and how much external interoperability evidence is absent?

### P08 — Living semantic steward

**Family:** C — Reusable understanding and human comprehension. **Grounding seeds:** S1–S3, S5, H4. **Status:** proposed experience, not an integrated capability claim.

1. **User intention:** Keep a useful, current model of the repository as the code and decisions evolve.
2. **Delegated input:** An existing repository and permission to update reviewed knowledge records when meaningful changes occur.
3. **Autonomous responsibility:** Notice source-backed changes, propose knowledge deltas, preserve provenance and flag conflicting or outdated links.
4. **Tangible outcome:** Reviewable knowledge-record diffs and exact-revision re-entry queries, not necessarily implementation PRs.
5. **Human involvement:** Human review where source authority or interpretation is contested; ordinary authored additions follow granted scope.
6. **Role of Sensemaking:** Persistent, typed product memory is the central output and supports later reasoning.
7. **Role of the runtime:** Read/write repository plus existing knowledge tools; scheduled runs are optional, not proof of required resident workers.
8. **Coordination needs:** Repeated independent sessions with Git-carried knowledge; durable ticket machinery is not a prerequisite.
9. **Distinctiveness:** Maintains the model itself; P03 consumes historical meaning without promising active stewardship.
10. **Uncertainty:** Will maintenance overhead, stale links and graph noise outweigh later reuse benefit?

### P09 — Interactive repository mentor

**Family:** C — Reusable understanding and human comprehension. **Grounding seeds:** S1–S3, S5, H4. **Status:** proposed experience, not an integrated capability claim.

1. **User intention:** Learn an unfamiliar architecture or acquire working fluency without reading every document.
2. **Delegated input:** A repository and the learner's current question or chosen component.
3. **Autonomous responsibility:** Explain concepts in task-relevant order, offer source-backed examples and adapt follow-up questions.
4. **Tangible outcome:** A guided conversation, navigable concept path and a small set of verified source pointers.
5. **Human involvement:** Learner chooses where to drill deeper; no approval for read-only teaching.
6. **Role of Sensemaking:** Semantic relationships and source provenance make explanations less arbitrary and easier to check.
7. **Role of the runtime:** Conversational UI or terminal with repository reads; neither hooks nor a factory loop is necessary.
8. **Coordination needs:** One interactive session; retained learner progress is optional and distinct from product knowledge.
9. **Distinctiveness:** The beneficiary is the human learning the system, not an agent building or deciding for them.
10. **Uncertainty:** Can it measure actual comprehension and avoid misleading explanations when knowledge is incomplete?

### P10 — Source-grounded PR executor

**Family:** D — Bounded engineering and disciplined probes. **Grounding seeds:** S2, S7, H2–H3, H6, D3–D4. **Status:** proposed experience, not an integrated capability claim.

1. **User intention:** Turn one sufficiently authorized coding request into a reviewable change.
2. **Delegated input:** A bounded issue, acceptance conditions, repository and action/transition limits.
3. **Autonomous responsibility:** Understand relevant sources, implement the change, run proportionate checks, reconcile claims and open a PR where permitted.
4. **Tangible outcome:** A focused patch or pull request with evidence and explicit limitations.
5. **Human involvement:** Human intervenes for product ambiguity, unavailable credentials or reserved merge/deploy authority.
6. **Role of Sensemaking:** Selects bounded work, brings prior constraints to the task and interprets tests without overclaiming.
7. **Role of the runtime:** Filesystem edits, terminal, test tools and Git/PR access; could run as one DeepSeek or alternative host session.
8. **Coordination needs:** One session can be sufficient; a small subagent is optional, not defining.
9. **Distinctiveness:** Its promise is one bounded code outcome, unlike P11's end-to-end product experience.
10. **Uncertainty:** Does a selected host preserve exact permissions, tool behavior and artifact identity across the task?

### P11 — Complete feature experience finisher

**Family:** D — Bounded engineering and disciplined probes. **Grounding seeds:** S2, S7, H2–H3, H6, D3–D4. **Status:** proposed experience, not an integrated capability claim.

1. **User intention:** Receive a finished, coherent user workflow instead of isolated code changes.
2. **Delegated input:** A feature-level user outcome, target repository and explicit acceptance boundaries.
3. **Autonomous responsibility:** Inspect every necessary UI, state, API, persistence, permission and documentation surface; implement warranted connected changes.
4. **Tangible outcome:** A demonstrable vertical feature with test/acceptance evidence and an honest incomplete-boundary report.
5. **Human involvement:** Owner input for genuinely unstated product meaning or protected external transitions; no automatic 'complete' from green CI.
6. **Role of Sensemaking:** Connects product intention, contracts and source-level consequences so hidden adjacent requirements are less likely to be missed.
7. **Role of the runtime:** A robust coding host with local validation; staging or browser acceptance may require separate environment access.
8. **Coordination needs:** May fit one long session or staged bounded sessions; factory persistence is not inherent to the promise.
9. **Distinctiveness:** The deliverable is a user-experience slice with cross-surface coherence, not merely a PR touching code.
10. **Uncertainty:** Which acceptance conditions demand real users, backend state or privileged deployment?

### P12 — Defect-recovery custodian

**Family:** D — Bounded engineering and disciplined probes. **Grounding seeds:** S2, S7, H2–H3, H6, D3–D4. **Status:** proposed experience, not an integrated capability claim.

1. **User intention:** Restore a failing workflow without mistaking a symptom for its root cause.
2. **Delegated input:** A failing CI run, regression, incident description or incomplete repair, plus the repository revision.
3. **Autonomous responsibility:** Reproduce where safe, distinguish environment/provider failures from code faults, attempt an authorized local repair or stop with diagnosis.
4. **Tangible outcome:** A verified repair candidate or a bounded recovery dossier identifying the real blocker.
5. **Human involvement:** Human approval for dangerous rollback, secrets, data modification or unsupported production effects.
6. **Role of Sensemaking:** Uses source/incident history and finding-specific verification to prevent false repair closure.
7. **Role of the runtime:** Terminal and logs for local cases; operations integrations only when separately granted.
8. **Coordination needs:** Can be one session; retry and restart may benefit from durable execution records, not necessarily factory control.
9. **Distinctiveness:** Begins with a failure and permits a justified no-fix finding, unlike ordinary feature delivery.
10. **Uncertainty:** Can the observable environment discriminate transient infrastructure faults from a source regression?

### P13 — Falsifiable-assumption probe

**Family:** D — Bounded engineering and disciplined probes. **Grounding seeds:** S2, S7, H2–H3, H6, D3–D4. **Status:** proposed experience, not an integrated capability claim.

1. **User intention:** Reduce uncertainty about a proposed design before committing a production feature.
2. **Delegated input:** A consequential claim or assumption, source baseline and acceptable experiment boundary.
3. **Autonomous responsibility:** Choose a minimal permitted diagnostic or disposable prototype and record observations without promoting it to product code.
4. **Tangible outcome:** A small evidence report, canary or disposable branch demonstrating what was and was not learned.
5. **Human involvement:** Human grants any execution or external effects beyond the diagnostic envelope; later adoption is a separate decision.
6. **Role of Sensemaking:** Names the precise warrant gap, alternative explanations and observation limits.
7. **Role of the runtime:** Could use local shell/tests or a disposable sandbox; no persistent service or automatic PR is needed.
8. **Coordination needs:** Usually one session; independent checks only where they materially strengthen the inference.
9. **Distinctiveness:** Produces decision-changing evidence, not an implemented product feature or an option ranking.
10. **Uncertainty:** Would direct source inspection be cheaper and sufficient, making the probe unnecessary?

### P14 — Warranted backlog continuation

**Family:** E — Warranted work selection and revival. **Grounding seeds:** S2, S7, D3, H3. **Status:** proposed experience, not an integrated capability claim.

1. **User intention:** Avoid blindly doing the next stale or low-value backlog item.
2. **Delegated input:** A repository and an existing backlog, issue collection or partial implementation history.
3. **Autonomous responsibility:** Reconcile backlog entries with current sources and owner authorization, classify superseded work and perform one warranted bounded item if action is authorized.
4. **Tangible outcome:** A current work disposition plus either a qualified PR or a source-backed reason to refrain.
5. **Human involvement:** Owner involvement when prioritization is genuinely preference-dependent or a protected transition is reached.
6. **Role of Sensemaking:** Separates historical intent from current warrant and grounds candidate selection in repo reality.
7. **Role of the runtime:** Issue/Git tools and ordinary coding tools for optional execution; no dedicated factory necessary for one episode.
8. **Coordination needs:** Single session or independently repeated sessions; not automatically a Campaign chain.
9. **Distinctiveness:** Its key value is selecting or declining current work, unlike P10 where the work item is already chosen.
10. **Uncertainty:** Can selection be grounded without silently inventing a new product priority?

### P15 — Dormant-project revival

**Family:** E — Warranted work selection and revival. **Grounding seeds:** S2, S7, D3, H3. **Status:** proposed experience, not an integrated capability claim.

1. **User intention:** Recover a partially abandoned product whose actual state and boot path are unknown.
2. **Delegated input:** An old repository, last known intention, incomplete branches and permission to inspect or safely restore a local environment.
3. **Autonomous responsibility:** Establish the real state, disentangle legacy branches, recover a runnable local path if authorized and mark what remains lost.
4. **Tangible outcome:** A resurrection dossier and, where feasible, a bootable local demo or non-destructive repair PR.
5. **Human involvement:** Human approval for destructive cleanup, secret replacement, data migrations or a changed product thesis.
6. **Role of Sensemaking:** Reconstructs historical rationale, current capability, invalid assumptions and whether restoration is warranted.
7. **Role of the runtime:** Git history, environment diagnostics, package tools, optional container; no factory controller is inherently needed.
8. **Coordination needs:** May span several bounded sessions, with durable notes if source recovery becomes lengthy.
9. **Distinctiveness:** The user seeks operational re-entry into an abandoned product, not merely a prioritized queue.
10. **Uncertainty:** What cannot be recreated due to missing credentials, data, dependencies or external services?

### P16 — Bounded milestone delegate

**Family:** F — Durable delegated work and attention management. **Grounding seeds:** S4, D1–D7, P1–P5, H2–H5. **Status:** proposed experience, not an integrated capability claim.

1. **User intention:** Delegate a software outcome larger than one change and return only when the Goal is done or a true exception arises.
2. **Delegated input:** An explicit target Goal, repository, scope, authority envelope, resource budget and protected-transition rules.
3. **Autonomous responsibility:** Reassess current state, select and complete successive warranted Campaigns, reconcile their evidence, and stop correctly.
4. **Tangible outcome:** A qualified terminal Goal state, integrated work where authorized, or an explicit blocked/exception record.
5. **Human involvement:** Only reserved product decisions, merge/release/deploy grants, budget or external constraints interrupt.
6. **Role of Sensemaking:** Interprets current Goal and returned evidence; semantic judgment must remain singular inside the factory.
7. **Role of the runtime:** A suitable bounded executor could hypothetically be DeepSeek Harness, but Dark Factory is already the canonical durable factory runtime.
8. **Coordination needs:** Durable Goal/Frontier/Campaign coordination is essential; parallel subagents are not essential.
9. **Distinctiveness:** Owns an evolving terminal outcome across cycles, not one Ticket or PR.
10. **Uncertainty:** Can a DeepSeek executor adapter respect Dark Factory's current contract without duplicating Campaign truth?

### P17 — Team attention concierge

**Family:** F — Durable delegated work and attention management. **Grounding seeds:** S4, D1–D7, P1–P5, H2–H5. **Status:** proposed experience, not an integrated capability claim.

1. **User intention:** Request help through existing team discussions and receive results without constant status chatter.
2. **Delegated input:** Authorized GitHub/Feishu events, written admission rules and a single-repo team communication boundary.
3. **Autonomous responsibility:** Admit eligible requests, create work tickets, assign workers, preserve follow-up ownership and report only useful outcomes or questions.
4. **Tangible outcome:** Replies in original threads, reviewable PRs and a panel of items requiring human attention.
5. **Human involvement:** Human handles genuinely blocked tickets, decisions and protected actions; unread conversations grant no authority.
6. **Role of Sensemaking:** Provides source-grounded work judgment inside each authorized ticket, without replacing the existing admission/mandate controller.
7. **Role of the runtime:** A host with persistent event intake, routing, sessions and authorized workers; the superagent prototype offers a research example.
8. **Coordination needs:** Long-lived ticket/service coordination may be useful, but this is not necessarily Goal-level factory control.
9. **Distinctiveness:** The promise is low-attention teamwork and communication continuity, not closed-loop delivery of a software milestone.
10. **Uncertainty:** How can ticket Eval and Dark Factory semantic continuation coexist without overlapping authority?

### P18 — Cross-repository contract interpreter

**Family:** G — Multiple repositories and contested interpretations. **Grounding seeds:** S2–S3, S7, D2–D5, H5. **Status:** proposed experience, not an integrated capability claim.

1. **User intention:** Understand and possibly align dependencies spanning several repositories without losing ownership boundaries.
2. **Delegated input:** Two or more explicitly named repositories, desired interoperability and each repository's authority scope.
3. **Autonomous responsibility:** Map interface contracts, trace implications on both sides and preserve separate ownership and unresolved compatibility claims.
4. **Tangible outcome:** A cross-repo compatibility/negotiation dossier, optionally later informing separate authorized PRs.
5. **Human involvement:** Human owners resolve contract changes spanning products; external writes remain separate authorizations.
6. **Role of Sensemaking:** Preserves typed dependency, provenance, scope and competing product intents across repositories.
7. **Role of the runtime:** Multiple source checkouts and comparison tools; execution coordination is optional for an analysis-only experience.
8. **Coordination needs:** May need specialist sessions, but need not be a multi-repository factory Campaign.
9. **Distinctiveness:** Value comes from keeping two source-of-truth systems coherent, not understanding one codebase in isolation.
10. **Uncertainty:** Who owns cross-repo contract decisions and how are incompatible revisions/permissions represented?

### P19 — Contested-perspective council

**Family:** G — Multiple repositories and contested interpretations. **Grounding seeds:** S2–S3, S7, D2–D5, H5. **Status:** proposed experience, not an integrated capability claim.

1. **User intention:** Expose important disagreements that one apparently confident coding agent may smooth over.
2. **Delegated input:** A disputed architecture, risk claim or product question, with evidence and explicit lenses to examine.
3. **Autonomous responsibility:** Generate independently attributable readings, challenge assumptions and reconcile which disputes are evidential versus owner choices.
4. **Tangible outcome:** A disagreement map with source-backed positions, unknowns and decision questions—not an automatic winner.
5. **Human involvement:** A human or separate authorized process adjudicates protected preferences; no forced consensus.
6. **Role of Sensemaking:** Grounds competing perspectives in shared sources while retaining differences in interpretation and uncertainty.
7. **Role of the runtime:** Any host that can run independent contextual passes; subagent support may help but is not a prerequisite.
8. **Coordination needs:** Independent sessions or subagents can preserve separateness; simply adding agents without viewpoint diversity is not this possibility.
9. **Distinctiveness:** The output is auditable intellectual plurality, not more throughput or another implementation worker.
10. **Uncertainty:** Are supposedly independent perspectives actually correlated by prompts, shared context and model bias?

## D. Representative contrasting interaction sketches

Conceptual delegations only; arrows describe **user experience**, not implementation state machines.

| Expression | User delegates → System works → System delivers → Human involvement |
| --- | --- |
| P01 | 'Here is this repository' → source-grounded interpretation → architecture/goal map → none unless source authority is indeterminate |
| P05 | 'Find what we have not considered' → tensions in historical knowledge → hypothetical new product goals with provenance → owner decides whether any goal matters later |
| P10 | 'Implement this bounded issue' → inspect, edit, verify and reconcile within authority → reviewable PR → human handles reserved merge/product decision |
| P13 | 'Continue the backlog responsibly' → revalidate current work instead of assuming oldest first → current disposition and, if permitted, one completed item → owner handles genuinely preference-dependent priority |
| P16 | 'Achieve this authorized milestone' → successive warranted Campaigns and exact-state reassessment → terminal Goal, evidence or blocked state → human only at genuine authority/exception boundaries |
| P17 | 'Help us through existing threads' → admit policy-eligible requests, route workers, retain Ticket context → replies/PRs/exception panel → team responds only to decisions or usable results |
| P18 | 'Compare these two dependent repos' → map reciprocal contracts and ownership → compatibility dossier → product owners decide cross-repo authority |
| P19 | 'Show why experts disagree' → retain independently attributed interpretations → contestable disagreement map → human adjudicates preferences or asks for more inquiry |

## E. Unexplored dimensions and plausible later divergent lenses

These are **open territory**, not findings that the corresponding capability is absent or bad.

- **Who counts as the user?** Solo developer, product owner, engineering team, nontechnical stakeholder, user-facing maintainers, or an agent acting for another agent could generate different promises.
- **What if the most useful first version has no custom harness?** Existing coding agent + portable Sensemaking guide + Git-reviewed artifact could deliver P01/P04/P06. A no-hooks/no-resident-worker frame deserves comparison without pretending it has been tested here.
- **What if semantic memory is optional or deliberately short-lived?** Source-only reconstruction, selective retention, temporary private reasoning, owner-approved forgetting and exportable handoff represent distinct trust and usability assumptions.
- **What if the owner cannot or does not want to grant write access?** Read-only, offline, source-auditing and local canary experiences might become the whole product rather than partial implementations.
- **What if the relevant value is *not* software?** Repository-driven pedagogy, governance deliberation and cross-team contract literacy may have different beneficiaries and success evidence.
- **What if actions occur in untrusted or regulated environments?** Threat models, confidential repository handling, artifact redaction and verifiable least-privilege execution may produce new interaction families. DeepSeek's safety warning makes this material, but no security review was conducted.
- **What if hardware, tokens, API limits or background-job interruption dominate?** Cost-aware bounded autonomy and graceful partial-result delivery may materially change the promised experience.
- **What if the host is changed?** Codex, Claude Code, OpenCode, DeepSeek or a CLI-only substrate could realize different experience subsets; no host-comparison qualification was run.
- **What if human authority is collective or asynchronous?** Multi-owner consent, competing product mandates and team discussion capture need inquiry beyond single-owner task delegation.
- **What if the application spans repositories, services and deploy environments?** Cross-repo identity and production effects remain outside a demonstrated first experience here.
- **What if generative exploration is systematically mediocre?** Blind novelty and source-only-versus-memory comparison would test the suspected reasoning limitation; generating plausible text is not proof of product opportunity discovery.

Potential later lenses: counterfactual absence of the runtime; no-write/no-network; returning user after six months; novice onboarding; multi-owner governance; emergency recovery; untrusted code; reduced-budget operation; source-only skeptic; and a team member who cares primarily about low notification noise. They are invitations for another divergent round, not mandatory passes.

## F. Architectural tensions — retained without resolution

| Tension | What the inspected sources establish | Unresolved question (no decision made) |
| --- | --- | --- |
| Single-agent vs multi-agent | Official DeepSeek offers child-agent backends (H5); Sensemaking retains one active semantic controller (S2, S7). | When would independent viewpoints yield meaningfully better outcomes, rather than overhead or conflicting judgments? |
| One-off task vs durable delegation | Headless offers one invocation and optional session continuation (H3); Dark Factory owns durable Goal/Campaign continuation (S4, D6). | Which experiences require factory state, which need only a source artifact, and which justify a Ticket service? |
| Session memory vs semantic knowledge vs factory truth | DeepSeek persists session events (H4), Sensemaking has reviewed product knowledge (S1–S5), Dark Factory owns Campaign evidence/authority (D2–D6). | How can all three coexist without duplicate competing canonical records or unbounded prompt injection? |
| Autonomous action vs protected authority | Dark Factory separates warrant/action/transition grants (D3–D5); superagent uses Mandates (P2–P3); DeepSeek approval is not audited isolation (H6). | How should a proposed adapter carry exact rights without silently inventing or weakening any of them? |
| Runtime extensibility vs complexity | DeepSeek Cordis supports replaceable plugins, and multiple profiles (H2). | Is a custom plugin needed at all, and how would breaking preview changes affect maintenance? |
| DeepSeek integration vs Dark Factory ownership | Dark Factory is accepted as canonical factory successor (S4, D2); the superagent prototype separately has Ticket-level coordination (P1–P5). | Could DeepSeek serve only as a bounded executor, or a social front door, without creating a second factory runtime? |
| Event-driven intake vs semantic responsibility | Superagent Eval decides admission/Tickets; Sensemaking decides warranted engineering responsibility (P2–P3, S7). | Where is the exact translation boundary when a Ticket contains a product-level Goal? |
| Historical knowledge vs fresh source | Sensemaking source-reentry evidence is bounded (S5) and original source remains authoritative. | How is stale or incomplete graph material prevented from biasing the agent more than actual source reality? |
| User attention vs richer explanation | The superagent prototype explicitly optimizes for low attention (P1); exploratory and audit outputs may need elaborate attribution. | Who receives a compact result, a full record, or one human action, and with what consent? |
| Model flexibility vs capability claims | DeepSeek Harness has a model-adapter seam (H2); no cross-provider comparison was performed. | Which experiences depend on model quality versus host mechanics versus Sensemaking guidance? |
| Local safety vs operational power | DeepSeek safety says sandbox/approval controls are not sufficient by themselves (H6). | How could any write-capable or unattended mode be qualified for a particular environment without overclaiming production safety? |
| Exploration vs production state | S3/S6 require standalone divergence to stop before convergence or construction; D3 protects runtime work authority. | How are hypothetical expressions retained so no automatic backlog or Campaign is created from them? |

A possible architecture diagram would be a premature design decision at this stage. These questions deliberately preserve several allocations of responsibility for later investigation.

## G. Coverage Assessment handoff (assessment not performed)

**Distinct families retained:** A source-grounded truth; B possible futures/architectural consequences; C living understanding/human learning; D bounded engineering and probes; E warranted work/revival; F durable delegation/team attention; G cross-repository coordination and contested perspectives.

**Provisional differentiation basis:** Each entry names a different desired result or delegation/interrupt contract. Nearby pairs that warrant later scrutiny include P03 versus P08 (consume history vs steward it), P04 versus P05 (given intention vs source-discovered new goal), P06 versus P07 (consequence prediction vs alternative boundaries), P10 versus P11 (one change vs complete workflow), P14 versus P15 (current backlog warrant vs operational resurrection), and P16 versus P17 (Goal-level Campaigns vs team Ticket/attention management).

**Remaining coverage uncertainty:** Originality is scoped to the inspected corpus; no fresh participant trials, model comparison, real DeepSeek-to-Sensemaking adapter exercise, DeepSeek-as-Dark-Factory-executor test, threat modeling, cross-repo live qualification, or quantified human-attention benefit were performed. Missing beneficiaries and offline/least-privilege frames could still change the landscape. The set is intentionally not asserted exhaustive.

**Questions for the future Coverage Assessment only (not answered here):**

1. Do any entries merely rename the same user end, or can their tangible outcomes and authority contracts be differentiated?
2. Which beneficiary, outcome, timescale, or autonomy mode is still missing from the explored space?
3. Did the catalog over-index on engineering delivery despite Sensemaking's ontology-first identity?
4. Are the “no custom harness”, “no persistent worker” and “no code change” counterframes adequately represented?
5. Would one more independent divergent round plausibly alter the *families*, or only produce cosmetic variants?
6. Which source claims are still only documentary or research-prototype evidence and need later verification before any option evaluation?
7. What owner-reserved boundary must remain explicit if an option is later selected?

**Completion / stop:** A bounded possibility landscape with contrasting user promises, constraints, source pointers, conceptual interactions and unresolved gaps has been recorded. Continuing directly into consolidation, ranking, MVP selection, architecture, implementation, a new controller, or another Skill would exceed this authorized Divergent Exploration. No design adoption or runtime integration is claimed.

---

**Governing non-identities:** Possibility ≠ capability. Source document ≠ runtime qualification. Session persistence ≠ semantic knowledge. A successful worker ≠ completed Goal. Exploration ≠ permission to act.
