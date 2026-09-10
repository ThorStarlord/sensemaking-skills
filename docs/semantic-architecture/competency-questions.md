# Competency Questions

**Status:** Canonical scope tests for the semantic architecture  
**Rule:** ontology concepts should be added because they help answer demonstrated competency questions, not because they are merely available software-engineering vocabulary.

## How to use this document

Each question represents a class of reasoning Sensemaking should eventually support consistently. A question does not imply that its answer must be deterministic. The implementation should classify which parts are mechanically observable, which are semantic judgments, and which require owner or external authority.

A proposed ontology concept should identify the competency question(s) it enables.

## A. Intent, scope, and authority

**CQ-001** — What explicit user goal or mission governs the current analysis?

**CQ-002** — Which requirements and constraints are explicit, and which are merely inferred?

**CQ-003** — Which success conditions have been stated, and what evidence would establish each condition?

**CQ-004** — Which part of the repository is in authorized scope for reading, analysis, or mutation?

**CQ-005** — What action authority currently exists, and what authority would be required for the next consequential action?

**CQ-006** — Does a current recommendation exceed the authority under which the evidence was gathered?

## B. Repository identity and currentness

**CQ-007** — Which exact repository state does a material claim describe?

**CQ-008** — Is the current worktree the same state that produced the evidence being relied upon?

**CQ-009** — Which observations came from tracked files, untracked files, generated output, external sources, or historical commits?

**CQ-010** — Has repository drift made an earlier diagnosis stale or only partially applicable?

**CQ-011** — Can a later agent reconstruct the target identity and currentness boundary without the prior chat session?

## C. Repository structure

**CQ-012** — What packages, modules, source files, tests, configurations, schemas, workflows, and documentation constitute the relevant subsystem?

**CQ-013** — Which source units export or expose interfaces consumed elsewhere?

**CQ-014** — Which source units import, call, configure, persist to, generate, or otherwise depend on other units?

**CQ-015** — Which files are implementation, tests, configuration, documentation, generated artifacts, fixtures, or build definitions?

**CQ-016** — Which structural relationships are directly observed and which are inferred from naming or organization?

**CQ-017** — Which code elements jointly realize one higher-level software capability?

## D. Software architecture and boundaries

**CQ-018** — What components and architectural boundaries are explicit in ratified documentation or code structure?

**CQ-019** — Which components belong to which layers or subsystems?

**CQ-020** — Which dependencies cross an architectural boundary?

**CQ-021** — Does an observed dependency conform to, bypass, or contradict a stated contract?

**CQ-022** — Which interfaces mediate dependencies and which dependencies reach directly into another component's implementation?

**CQ-023** — Where is ownership of a responsibility duplicated, fragmented, or ambiguous?

**CQ-024** — Which architectural relationships are intended, transitional, accidental, or currently uncertain?

**CQ-025** — Does a proposed repair reduce the identified architectural contradiction or merely move it?

## E. Behavior and contracts

**CQ-026** — Where is a claimed behavior implemented?

**CQ-027** — Which interface, test, schema, specification, documentation, or external contract defines expected behavior?

**CQ-028** — Which tests provide evidence for a behavioral claim, and what scope do those tests actually cover?

**CQ-029** — Does a passing test establish the entire claimed behavior or only a narrower condition?

**CQ-030** — Does runtime or integration evidence contradict what static code or documentation appears to imply?

**CQ-031** — Which behavior is relied upon by downstream components even if no explicit contract declares it?

## F. Evidence and epistemic status

**CQ-032** — What exact evidence supports a material claim?

**CQ-033** — Is a claim mechanically observed, deterministically derived, agent-inferred, hypothesized, or human-ratified?

**CQ-034** — What counter-evidence exists for the current claim?

**CQ-035** — Is the evidence source complete enough to justify an absence claim?

**CQ-036** — Which claims depend only on stale, partial, or weak evidence?

**CQ-037** — Which claims are mutually contradictory, and are the contradictions caused by time, scope, source authority, or genuine inconsistency?

**CQ-038** — Which conclusion was produced by a validated artifact, and what does that validation mechanically establish versus leave semantic?

**CQ-039** — Which exact evidence bytes and repository snapshot were used when a decision was authored?

**CQ-040** — Has a later artifact superseded, reconciled, or merely added evidence to an earlier claim?

## G. Uncertainty and investigation

**CQ-041** — What credible uncertainty could change the next action, scope, authority path, or stop/continue decision?

**CQ-042** — Which uncertainty is currently decision-changing rather than merely interesting?

**CQ-043** — What evidence would resolve, narrow, or materially reframe that uncertainty?

**CQ-044** — Is an investigation collecting new decision-relevant evidence or repeating already sufficient work?

**CQ-045** — Did new evidence close one uncertainty while introducing another?

**CQ-046** — Is work blocked because evidence is unavailable, capability is unavailable, authority is missing, or the semantic question itself remains unresolved?

## H. Responsibility, capability, and work

**CQ-047** — What responsibility is warranted by the current evidence?

**CQ-048** — Which available capabilities declare compatibility with that responsibility?

**CQ-049** — Which capability was selected, by whom, and on what semantic rationale?

**CQ-050** — Does the selected capability require mutation or external authority beyond the current boundary?

**CQ-051** — What artifact or evidence should the capability produce if it succeeds mechanically?

**CQ-052** — What conditions distinguish completion of the responsibility from successful execution of the capability?

**CQ-053** — Was a responsibility deferred because it was unwarranted now, blocked, lower priority, or outside authority?

## I. Change and repair

**CQ-054** — What changed between two target snapshots?

**CQ-055** — Which software entities and relations were modified by the change?

**CQ-056** — Which original claim or uncertainty motivated the change?

**CQ-057** — What evidence demonstrates that the change addressed the targeted condition?

**CQ-058** — Did the change introduce new dependency, contract, quality, or documentation contradictions?

**CQ-059** — Does repository change establish only that bytes changed, or is there independent evidence that the intended repair succeeded?

**CQ-060** — Can a reviewer reconstruct the chain from problem evidence to change to validation to decision?

## J. Product-change reasoning

**CQ-061** — Is a proposed product change a net-new capability, extension, enhancement, integration, enabler, quality improvement, or simplification/removal?

**CQ-062** — Does the proposed change add, deepen, broaden, connect, simplify, harden, accelerate, scale, or enable product value?

**CQ-063** — Which existing product capability or user workflow does the change affect?

**CQ-064** — Does the change create mostly independent value, complementary value, multiplicative value, foundational value, or defensive value?

**CQ-065** — Is a proposed implementation actually one feature, several features realizing one capability, or an enabling investment beneath a larger initiative?

**CQ-066** — Does a proposed taxonomy label describe value creation, implementation mechanism, product surface, or maturity state, and are those axes being accidentally conflated?

## K. Documentation and semantic drift

**CQ-067** — Which document is authoritative for a given contract, product definition, decision, or historical explanation?

**CQ-068** — Does current implementation contradict current documentation, or are the two describing different scopes or times?

**CQ-069** — Are two Skills using the same canonical term with materially different meanings?

**CQ-070** — Has a legacy term survived after the underlying architecture changed?

**CQ-071** — Which ontology concept is merely descriptive vocabulary today, and which has an executable contract behind it?

**CQ-072** — Would formalizing a new concept remove repeated ambiguity or merely add vocabulary burden?

## L. Handoff, reconstruction, and termination

**CQ-073** — Can a fresh agent reconstruct the current goal, target state, active responsibility, uncertainty, authority, and evidence without prior conversation memory?

**CQ-074** — Which conclusions are current, superseded, contradicted, deferred, or unresolved at handoff time?

**CQ-075** — What continuation actions are mechanically available, and which are semantically warranted?

**CQ-076** — What evidence supports closure rather than continuation?

**CQ-077** — Is closure blocked by missing evidence, missing authority, an external dependency, or a genuine remaining responsibility?

**CQ-078** — Can the complete decision path be reconstructed from durable state without making historical decisions appear more certain than they were at the time?

## Initial priority set

The first implementation experiments should prioritize questions that already recur across existing Skills and Campaigns:

```text
CQ-007 repository currentness
CQ-017 capability realization
CQ-020 boundary-crossing dependency
CQ-021 contract contradiction
CQ-032 evidence for claim
CQ-033 epistemic status
CQ-037 contradiction
CQ-041 decision-changing uncertainty
CQ-047 warranted responsibility
CQ-054 target change
CQ-057 repair evidence
CQ-059 changed != succeeded
CQ-069 vocabulary drift
CQ-073 fresh-context reconstruction
```

These questions are intentionally cross-cutting. If the semantic model cannot improve consistency on these, expanding it further is not warranted.