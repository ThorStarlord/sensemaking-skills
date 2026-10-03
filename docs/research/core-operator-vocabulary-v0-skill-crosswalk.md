# Core Operator Vocabulary v0 — 51-Skill Crosswalk

**Status:** research audit; non-authoritative  
**Date:** 2026-09-22  
**Source set:** the 51 canonical Skill packages under skills/*/SKILL.md on main at the audit baseline  
**Vocabulary:** [Core Operator Vocabulary v0](core-operator-vocabulary-v0.md)  
**Authority:** descriptive only; not routing metadata, not a Skill registry replacement, not a manifest extension, not a release gate

## 1. Audit question

> Can every current canonical Skill be described naturally with the twelve candidate core operators while preserving why the Skill remains a distinct situated responsibility or governance/control surface?

The candidate operator set is:

~~~text
OBSERVE
FRAME
DECOMPOSE
MODEL
GENERATE
COMPARE
EVALUATE
VERIFY
SELECT
RECONCILE
COMMUNICATE
COORDINATE
~~~

The audit is intentionally qualitative.

An operator listed for a Skill means the transformation is materially characteristic of that Skill's method. It does not mean every invocation must expose every listed operator explicitly.

## 2. Primary package-role vocabulary

The audit also uses a descriptive primary-role classification:

- **CAPABILITY** — reusable bounded competence that is relatively cross-domain;
- **SITUATED_SKILL** — capability specialized by domain/responsibility/artifact/evidence/stopping semantics;
- **COMPOSITION** — connects, resumes, transfers, or composes other capabilities;
- **ROLE** — packages a recurring organizational responsibility/actor posture;
- **GOVERNANCE** — protects authority, provenance, ratification, canonicality, or protected transitions.

Root Primitives and Cognitive Operators are not represented as primary Skill-package identities in the current canonical tree.

## 3. Complete crosswalk

| Skill | Primary role | Operator decomposition | Situated distinction preserved by |
| --- | --- | --- | --- |
| ab-test-analysis | SITUATED_SKILL | OBSERVE, COMPARE, EVALUATE, VERIFY, MODEL | controlled-experiment evidence, statistical/practical significance, test-results claim ceiling |
| acceptance-criteria | SITUATED_SKILL | FRAME, DECOMPOSE, MODEL, VERIFY | delivery-specification semantics, observable scenarios, no invented product rules |
| architectural-review | SITUATED_SKILL | OBSERVE, FRAME, COMPARE, EVALUATE, MODEL | repository architecture judgment, proposed-direction boundary, advisory verdict |
| battlecard | SITUATED_SKILL | OBSERVE, COMPARE, EVALUATE, MODEL, COMMUNICATE | commercial competitive context, dated claims, talk-track communication |
| change-impact-analysis | CAPABILITY | OBSERVE, FRAME, DECOMPOSE, MODEL, EVALUATE | bounded change target, affected-surface reasoning, no automatic follow-up authority |
| coding-agent-native-campaign | GOVERNANCE | FRAME, VERIFY, COORDINATE, RECONCILE | approval identity, authorization receipt, campaign envelope, execution authority |
| competitive-analysis | SITUATED_SKILL | OBSERVE, FRAME, COMPARE, EVALUATE, MODEL | market-understanding responsibility, current competitor evidence |
| customer-journey | SITUATED_SKILL | OBSERVE, DECOMPOSE, MODEL, EVALUATE | journey scope, customer evidence, touchpoint/stage representation |
| discovery | SITUATED_SKILL | FRAME, GENERATE, EVALUATE, MODEL | product problem discovery, learning questions, evidence-before-investment |
| docs-aligner | SITUATED_SKILL | OBSERVE, COMPARE, EVALUATE, RECONCILE, MODEL | code/docs alignment, bounded repository mutation, downstream review expectation |
| experiment-design | SITUATED_SKILL | FRAME, GENERATE, COMPARE, EVALUATE, MODEL | pre-existing experiment warrant, proportional rigor, experiment-plan boundary |
| external-evidence-packet | GOVERNANCE | OBSERVE, FRAME, VERIFY, MODEL, COMMUNICATE | external provenance/currentness, external evidence != repository truth |
| gtm | SITUATED_SKILL | FRAME, GENERATE, COMPARE, EVALUATE, MODEL, COMMUNICATE | commercial-strategy responsibility, channel/message/timeline planning, no external execution |
| handoff | COMPOSITION | MODEL, COMMUNICATE, COORDINATE | cross-Skill context preservation, no execution or authority expansion |
| hypothesis | SITUATED_SKILL | FRAME, GENERATE, MODEL, EVALUATE | falsifiable product bet, success/kill criteria, validation != evidence |
| ideal-customer-profile | SITUATED_SKILL | OBSERVE, COMPARE, EVALUATE, MODEL | customer-fit evidence, disqualifiers, commercial/customer context |
| interview-synthesis | SITUATED_SKILL | OBSERVE, DECOMPOSE, COMPARE, MODEL | interview-source traceability, JTBD/pattern synthesis, no invented respondents |
| launch-checklist | SITUATED_SKILL | OBSERVE, DECOMPOSE, COMPARE, EVALUATE, VERIFY, MODEL | launch-readiness evidence, cross-functional conditions, recommendation != launch authority |
| lean-canvas | SITUATED_SKILL | FRAME, DECOMPOSE, MODEL, EVALUATE | business-model hypothesis structure, evidence status, critical assumptions |
| measure-pmf | SITUATED_SKILL | OBSERVE, COMPARE, EVALUATE, VERIFY, MODEL | PMF evidence bundle, segment/time scope, not-measured/insufficient-evidence states |
| multi-repository-strategic-analysis | SITUATED_SKILL | OBSERVE, FRAME, DECOMPOSE, MODEL, GENERATE, COMPARE, EVALUATE | explicit repository set, Level-3 capability allocation, no automatic scope expansion |
| north-star | SITUATED_SKILL | FRAME, GENERATE, COMPARE, EVALUATE, SELECT, MODEL | product-strategy metric selection, proposed metric status, no causal proof |
| okr | SITUATED_SKILL | FRAME, DECOMPOSE, MODEL, EVALUATE | strategy-to-outcome operationalization, target/owner evidence, no fabricated progress |
| opportunity-tree | SITUATED_SKILL | FRAME, DECOMPOSE, MODEL, GENERATE, EVALUATE | outcome/opportunity/solution hierarchy, evidence-aware assumptions |
| output-reconciler | CAPABILITY | OBSERVE, DECOMPOSE, COMPARE, VERIFY, EVALUATE, RECONCILE, MODEL | work-claim versus durable-evidence verification, scoped claim status |
| owner-decision-capsule | GOVERNANCE | FRAME, MODEL, COMPARE, EVALUATE, COMMUNICATE | owner-reserved choice, option-set adequacy, SELECT intentionally not performed |
| persona | SITUATED_SKILL | OBSERVE, DECOMPOSE, MODEL, EVALUATE | customer-understanding responsibility, JTBD/persona evidence boundary |
| pre-mortem | SITUATED_SKILL | FRAME, GENERATE, COMPARE, EVALUATE, MODEL | imagined-failure method, risk/readiness responsibility, imagined != observed |
| pricing | SITUATED_SKILL | OBSERVE, FRAME, GENERATE, COMPARE, EVALUATE, MODEL | pricing/packaging economics and WTP evidence, recommendation != price change |
| prioritize | SITUATED_SKILL | FRAME, COMPARE, EVALUATE, SELECT, MODEL | product-initiative prioritization, optional RICE, ranking != commitment |
| problem-framer | CAPABILITY | FRAME, DECOMPOSE, MODEL, EVALUATE | cross-domain problem-under-problem framing, non-implementation boundary |
| release-notes | SITUATED_SKILL | OBSERVE, COMPARE, MODEL, COMMUNICATE | shipped/beta/planned evidence classification, drafting != publication |
| repair-verifier | SITUATED_SKILL | OBSERVE, COMPARE, VERIFY, EVALUATE, RECONCILE | like-for-like re-probe against prior findings, bounded closure only |
| repo-sensemaker | SITUATED_SKILL | OBSERVE, FRAME, DECOMPOSE, COMPARE, EVALUATE, MODEL | repository diagnosis, weakest consequential boundary, diagnosis != strategy |
| roadmap | SITUATED_SKILL | FRAME, DECOMPOSE, COMPARE, EVALUATE, SELECT, MODEL | product-strategy sequencing, proposal/commitment distinction |
| sensemaking-docs-reconciler | GOVERNANCE | OBSERVE, COMPARE, EVALUATE, RECONCILE, MODEL | canonical vocabulary/contracts, approval-sensitive contract mutation |
| setup-sensemaking-skills | CAPABILITY | OBSERVE, FRAME, DECOMPOSE, MODEL, COORDINATE | harness/repository bootstrap, explicit approval for writes |
| skill-maintainer | ROLE | OBSERVE, DECOMPOSE, COMPARE, EVALUATE, MODEL, COMMUNICATE | recurring Skill-architecture maintenance role, evidence-linked improvement proposals |
| stakeholder-update | SITUATED_SKILL | OBSERVE, COMPARE, EVALUATE, MODEL, COMMUNICATE | stakeholder communication, currentness/decision-request semantics, no sending |
| strategic-repository-analysis | SITUATED_SKILL | OBSERVE, FRAME, DECOMPOSE, MODEL, GENERATE, COMPARE, EVALUATE, SELECT | Level-3 strategic decision space, path semantics, selection only when warranted |
| strategic-repository-reconciliation | SITUATED_SKILL | OBSERVE, COMPARE, VERIFY, EVALUATE, SELECT, RECONCILE, MODEL | prior Level-3 analysis, returned evidence, explicit strategic effect |
| strategic-sensemaking-loop | COMPOSITION | OBSERVE, FRAME, EVALUATE, SELECT, RECONCILE, COORDINATE | episode resume/control surface, inherited authority, no master truth system |
| strategy | SITUATED_SKILL | FRAME, DECOMPOSE, MODEL, GENERATE, COMPARE, EVALUATE, SELECT | product-strategy choices/non-choices, proposed until ratified |
| thesis-review-packet | GOVERNANCE | FRAME, MODEL, COMPARE, EVALUATE, COMMUNICATE | Level-3 to Level-4 protected review boundary, ratification intentionally external |
| to-issues | SITUATED_SKILL | FRAME, DECOMPOSE, MODEL | PRD-to-implementation decomposition, scope preservation, planning not execution |
| to-prd | SITUATED_SKILL | FRAME, DECOMPOSE, MODEL, EVALUATE | canonical product specification, evidence/scope/approval preservation |
| unknowns-mapper | CAPABILITY | FRAME, DECOMPOSE, MODEL, EVALUATE | cross-domain epistemic known/unknown/assumption/risk map, research stop rules |
| usage-researcher | ROLE | OBSERVE, DECOMPOSE, COMPARE, EVALUATE, MODEL, COMMUNICATE | recurring behavioral-observer role, observation only, no Skill mutation |
| user-stories | SITUATED_SKILL | FRAME, DECOMPOSE, MODEL, EVALUATE | user-valued delivery slices, traceability/INVEST, no invented estimates |
| using-sensemaking | GOVERNANCE | OBSERVE, FRAME, EVALUATE, SELECT, RECONCILE, COORDINATE | agent-native responsibility-selection/control policy, warrant/authority/stopping laws |
| workflow-planner | COMPOSITION | OBSERVE, FRAME, COMPARE, EVALUATE, SELECT, MODEL, COORDINATE | workflow recommendation after responsibility selection, plan != execution authority |

## 4. Coverage disposition

All 51 canonical Skills fit the twelve-operator vocabulary without needing a thirteenth operator for useful explanatory coverage.

~~~text
canonical Skills checked: 51

primary package roles:
  CAPABILITY: 5
  SITUATED_SKILL: 35
  COMPOSITION: 3
  ROLE: 2
  GOVERNANCE: 6

ROOT_PRIMITIVE packages: 0
COGNITIVE_OPERATOR packages: 0

Skills requiring a thirteenth core operator: 0
Skills recommended for merge solely from operator overlap: 0
~~~

This does not mean every line of every Skill can be mechanically reduced to the listed operators. The audit asks whether the Skill's characteristic reasoning can be explained without inventing another core operator.

## 5. Repeated capability ancestry

The crosswalk exposes several recurring capability families.

### 5.1 Evidence-grounded comparative judgment

Common shape:

~~~text
MODEL
+ COMPARE
+ EVALUATE
+ optional SELECT
~~~

Examples:

- architectural-review;
- competitive-analysis;
- pricing;
- prioritize;
- north-star;
- strategic-repository-analysis;
- multi-repository-strategic-analysis.

Shared operators do not erase their different domains, evidence contracts, or selection authority.

### 5.2 Evidence reconciliation

Common shape:

~~~text
OBSERVE
+ COMPARE
+ VERIFY
+ EVALUATE
+ RECONCILE
~~~

Examples:

- output-reconciler;
- repair-verifier;
- sensemaking-docs-reconciler;
- strategic-repository-reconciliation.

Their prior-model semantics differ materially:

~~~text
work claim
repair finding
canonical docs/contracts
strategic analysis
~~~

So one generic reconciliation Skill is not warranted by this audit.

### 5.3 Decision-focused inquiry

Common shape:

~~~text
FRAME
+ GENERATE
+ EVALUATE
+ VERIFY
~~~

Examples:

- unknowns-mapper;
- discovery;
- hypothesis;
- experiment-design;
- ab-test-analysis.

The key situated distinction is what evidence is being sought and who owns experiment warrant.

### 5.4 Specification refinement

Common shape:

~~~text
FRAME
+ DECOMPOSE
+ MODEL
~~~

Examples:

~~~text
to-prd
  -> user-stories
  -> acceptance-criteria
  -> to-issues
~~~

This is a progressive increase in delivery resolution, not four synonyms.

### 5.5 Evidence-backed customer modeling

Common shape:

~~~text
OBSERVE
+ DECOMPOSE/COMPARE
+ MODEL
+ EVALUATE
~~~

Examples:

- interview-synthesis;
- persona;
- customer-journey;
- ideal-customer-profile.

The output representation and customer/commercial decision served by each Skill remain distinct.

### 5.6 Reserved-decision packaging

Common shape:

~~~text
FRAME
+ MODEL
+ COMPARE
+ EVALUATE
+ COMMUNICATE
~~~

Examples:

- owner-decision-capsule;
- thesis-review-packet.

Their cognitive shape overlaps strongly, but governance differs:

~~~text
owner-reserved premise
!=
Level-4 product-thesis ratification
~~~

This is strong evidence that shared capability ancestry does not imply shared authority.

### 5.7 Evidence-bounded communication

Common shape:

~~~text
OBSERVE
+ MODEL
+ COMMUNICATE
~~~

Examples:

- release-notes;
- stakeholder-update;
- battlecard;
- external-evidence-packet.

Each carries different evidence/currentness and publication/external-authority boundaries.

## 6. Why no thirteenth operator was admitted

Several candidate terms were tested conceptually but can be represented without expanding the kernel:

| Candidate term | Current decomposition |
| --- | --- |
| synthesize | OBSERVE + MODEL |
| classify | OBSERVE/COMPARE + MODEL |
| challenge | GENERATE + COMPARE + EVALUATE |
| explore alternatives | GENERATE; iterative search allocation remains Exploration Policy |
| forecast/simulate | MODEL + EVALUATE under assumptions |
| plan | FRAME + GENERATE + COMPARE + EVALUATE + SELECT + MODEL |
| specify | DECOMPOSE + MODEL |
| measure | OBSERVE + VERIFY/EVALUATE |
| stop | control-policy disposition, not cognitive operator |
| escalate | governance/control transition, not cognitive operator |
| authorize/ratify | authority act, not cognitive operator |
| mutate | execution/effect class, not cognitive operator |

A new operator should not be admitted merely because a useful verb exists.

## 7. Strongest negative finding

The audit found **operator reuse**, but almost no evidence that current Skill identities should be collapsed.

Examples:

~~~text
output-reconciler
and
repair-verifier

share:
  OBSERVE
  COMPARE
  VERIFY
  EVALUATE
  RECONCILE

but:
  work-claim verification
  !=
  repair closure against a prior diagnostic finding
~~~

Likewise:

~~~text
owner-decision-capsule
and
thesis-review-packet

share:
  FRAME
  MODEL
  COMPARE
  EVALUATE
  COMMUNICATE

but:
  OWNER_RESERVED
  !=
  LEVEL4_RESERVED
~~~

Therefore the audit supports:

> common capability ancestry

more strongly than:

> Skill consolidation.

## 8. Product boundary result

No repository construction follows automatically from this coverage.

The audit does not warrant:

- adding operator metadata to Skill Contract Manifests;
- adding an operator registry;
- adding deterministic Skill selection;
- reorganizing the Skill filesystem;
- adding one Skill per operator;
- merging current Skills;
- adding an operator-aware runtime;
- adding operator coverage to validation/release gates;
- changing Domain Pack authority.

The current descriptive projection is sufficient until normal use demonstrates a concrete decision-changing gap.

## 9. Reopen criteria

Re-run or revise this audit when one of these becomes true:

1. a new canonical Skill cannot be explained naturally using the current twelve operators;
2. repeated authoring/maintenance failures show that a shared capability contract would remove real duplication;
3. the same missing operator is repeatedly invented across unrelated Skills;
4. agents repeatedly misunderstand capability ancestry in ways that change responsibility selection;
5. normal use demonstrates that a read-only operator/capability projection would materially improve discovery or explanation;
6. existing governance or representation distinctions can no longer be expressed without overloading the operator vocabulary.

Until then:

~~~text
operator map
= explanatory research

operator map
!= product router
!= Skill contract
!= authority model
~~~
