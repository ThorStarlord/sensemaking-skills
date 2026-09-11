# The Sensemaking Campaign

**Status:** Canonical Level-2 durable product model  
**Scope:** Durable product definition; version-independent  
**Current implementation roadmap:** [`productization-v0.3.md`](productization-v0.3.md)

## 1. Purpose

A **Sensemaking Campaign** is a durable engineering decision process carried across coding-agent sessions.

It exists to make a long-running engineering effort reconstructible from repository evidence, explicit decisions, authority, validated artifacts, and append-preserving history rather than from hidden conversation memory.

The Campaign is the central **durable Level-2 abstraction** around which Sensemaking Skills' persistence, provenance, handoff, and reconstruction machinery is productized. It is **not** the universal entry point for every Sensemaking task.

The active agent can apply Sensemaking's control doctrine, use a diagnostic Skill such as `repo-sensemaker`, or perform narrow bounded work without creating Campaign state when continuation complexity does not warrant it. Campaign primarily earns its cost when repository-specific decision context must survive time, sessions, agents, machines, or handoffs.

It does not replace the active coding agent's judgment. It makes that judgment explicit, bounded, durable, inspectable, and recoverable when durability is useful.

## 2. Product thesis

Sensemaking Skills is an **agent-native engineering sensemaking and control layer for software-engineering agents**.

The active coding agent owns semantic control. When durable Level-2 state is warranted, Sensemaking provides a deterministic substrate around that control loop:

- repository evidence;
- typed campaign state;
- explicit responsibilities and uncertainty;
- validated artifacts and evidence references;
- capability availability;
- authority boundaries;
- transition history;
- deterministic validation and reconstruction;
- reconciliation and repair verification;
- durable handoff across fresh agent contexts.

The product therefore aims to make an existing coding agent reason and continue work more reliably. It does **not** aim to replace that agent with a centralized autonomous orchestrator, and it does not require Campaign state merely because Sensemaking is being used.

## 3. Campaign definition

Conceptually, a Campaign contains:

```text
Campaign
├── Goal / user intent
├── Repository snapshot / target identity
├── Current uncertainty
├── Active responsibility
├── Available capabilities
├── Authority
├── Evidence
├── Produced artifacts
├── Transition history
├── Deferred responsibilities
└── Terminal / continuation state
```

The exact persisted representation may evolve, but these concepts define the durable product-level object being carried across sessions.

## 4. When Campaign is warranted and its canonical lifecycle

Campaign use is a semantic agent decision, not a size threshold or automatic mode. The Persona & Adaptive Guidance Model v0 distinguishes:

```text
decision complexity
-> may warrant stronger repository sensemaking

consequentiality
-> may warrant stronger evidence / validation / reconciliation

continuation complexity
-> primarily determines the value of durable Campaign state
```

Therefore:

```text
repository sensemaking warranted != Campaign required
high consequentiality != Campaign required
large task != Campaign required
```

When the agent decides durable Campaign state is warranted, the normal Campaign lifecycle is:

```text
Campaign warranted / initialized
→ repository sensemaking when needed
→ consequential uncertainty identified
→ agent determines warranted responsibility
→ agent inspects bounded available capabilities
→ authority is made explicit
→ bounded work is performed
→ artifact / evidence is produced
→ deterministic validation / reconciliation runs when warranted
→ agent authors a campaign decision
→ durable transition is recorded
→ continue / hand off / stop
```

The Campaign records the decision process. It does not silently infer or substitute for the semantic steps in that process.

## 5. Semantic-control boundary

The permanent control boundary is:

```text
Agent:
  Is Campaign durability useful for this work?
  What does the evidence mean?
  Which uncertainty is consequential?
  Which responsibility is warranted?
  Which available capability should be selected?
  Does the result justify continuation, deferral, or closure?

Deterministic machinery:
  Is the representation structurally valid?
  Is state persisted safely?
  Does referenced evidence exist and satisfy its mechanical admission contract?
  Does authority metadata permit the claimed action?
  Is the transition structurally reconstructible?
  What durable evidence, provenance, and history exist?
```

Therefore:

```text
validator passed != semantic conclusion is true
capability exists != capability should be selected
capability available != execution authorized
recommendation != execution authority
Campaign available != Campaign warranted
```

And critically:

```text
Campaign Controller
!= semantic router
```

The Campaign layer records and enforces contracts. **The agent still decides.**

## 6. Responsibility, capability, and authority

Sensemaking permanently distinguishes three questions:

```text
warranted responsibility
        !=
available capability
        !=
authorized capability
```

### Warranted responsibility

What kind of work does the current evidence justify doing next?

This is a semantic judgment owned by the active coding agent.

### Available capability

Does the current environment expose a Skill, tool, workflow, or ordinary engineering capability that claims it can perform the warranted responsibility?

Availability is inspectable product state. It does not rank candidates and does not select one for the agent.

### Authorized capability

Even if a capability is available, may it be used for the claimed action under the current authority boundary?

Authorization is distinct from recommendation and availability.

Valid campaign outcomes may therefore include:

```text
RESPONSIBILITY_WARRANTED
CAPABILITY_UNAVAILABLE
```

or:

```text
CAPABILITY_AVAILABLE
OWNER_AUTHORITY_REQUIRED
```

Those are honest states, not routing failures to be hidden.

## 7. Durable campaign state

The durable campaign layer exists so a fresh process or agent can reconstruct the current decision state without relying on prior chat context.

Current product implementations use typed campaign contracts such as:

- `CampaignState`;
- `Responsibility`;
- `Uncertainty`;
- `Authority`;
- dependencies;
- `TransitionRecord`;
- `CampaignPolicy`;
- `CampaignHandoff`;
- `CampaignTrace`;
- capability availability.

These records are structural. They make decisions reconstructible; they do not judge whether those decisions were semantically wise.

## 8. Artifact and evidence model

Artifacts and evidence are first-class parts of the Campaign because a durable decision must be able to answer **what supported it**.

The intended trust chain is:

```text
agent / Skill produces artifact
        ↓
exact artifact bytes
        ↓
canonical validator boundary
        ↓
validated artifact admission
        ↓
durable campaign evidence
        ↓
agent-authored decision
        ↓
TransitionRecord
```

The following are deliberately different:

```text
file exists
!= validated artifact
!= admitted campaign evidence
!= semantic decision
```

A mechanical validator may establish that an artifact satisfies a contract. It does not establish that the artifact's semantic conclusion is true.

Longer-term lineage should make it possible to answer:

```text
Which repository state was examined?
Which Skill or capability produced this artifact?
Which exact artifact bytes were validated?
Which validator admitted them?
Which evidence supported this decision?
Which transition consumed that evidence?
What later artifact superseded or reconciled it?
```

## 9. Handoff and resumability

Durable handoff is a defining Campaign property, not merely a convenience command.

A fresh coding-agent context should be able to reconstruct the active campaign from:

- durable campaign state;
- transition history;
- current handoff state;
- referenced canonical artifacts and evidence;
- explicit responsibility and authority;
- allowed continuation boundaries and stop conditions where recorded.

It should **not** require the prior conversation transcript as hidden input.

The target experience is:

```text
Agent A works
→ campaign state and evidence become durable
→ handoff is generated
→ Agent A context ends
→ Agent B resumes from the campaign
→ reconstruction validates
→ agent B continues from the same explicit decision state
```

This is especially important for long-running engineering work where agent contexts are disposable but the engineering decision process must not be.

## 10. Product architecture

The product architecture is intentionally agent-native and progressively durable:

```text
                    USER
                      │
                      ▼
                 Coding Agent
              semantic controller
                      │
          ┌───────────┴───────────┐
          │                       │
          ▼                       ▼
  Repository sensemaking     Ordinary bounded work
   when decision-complex        when locally clear
          │                       │
          └───────────┬───────────┘
                      ▼
          explicit responsibility / evidence
                      │
             agent asks whether durable
             continuation is warranted
                      │
          ┌───────────┴───────────┐
          │                       │
          ▼                       ▼
     no Campaign needed      Campaign warranted
          │                       │
          │                       ▼
          │                CampaignService
          │                       │
          │                       ▼
          │                 CampaignStore
          │                       │
          │                       ▼
          │                campaign_semantics
          │                       │
          └───────────┬───────────┘
                      ▼
             continue / handoff / stop
```

Skills and harness integrations sit around this control layer as bounded capabilities. They do not move semantic control into the deterministic campaign runtime.

## 11. Golden-path product experience

When Campaign durability is warranted, the Campaign product should support a coherent journey resembling:

```text
campaign init
→ agent performs repository sensemaking when needed
→ campaign ingest <validated artifact> when useful
→ agent records warranted responsibility + authority
→ agent selects/uses a bounded capability
→ work evidence is recorded
→ agent authors advance / defer / close decision
→ campaign transition is committed
→ campaign handoff when continuation crosses context
→ fresh-agent resume
```

For ordinary Sensemaking before this point, see `../GETTING_STARTED.md` and `../skills/using-sensemaking/SKILL.md`. Campaign Golden Paths compose existing durable surfaces; they are not a universal Sensemaking workflow.

Human-readable and machine-readable Campaign surfaces should expose the same durable state without forcing an agent to scrape prose or infer hidden state from filenames.

## 12. Trust and reconstruction invariants

The Campaign should fail closed when durable history cannot explain current state.

Important product invariants include:

- campaign identity is stable across state, policy, handoff, transition, and trace records;
- transition history is append-preserving;
- current state must be reconstructible from durable history;
- evidence references must resolve to admitted or otherwise explicitly valid evidence under the current evidence contract;
- authority must be represented separately from recommendation or capability availability;
- stale or tampered state must not be silently accepted;
- interruption recovery must complete or reject already-committed deterministic intent without re-performing semantic reasoning;
- historical evidence is preserved rather than rewritten to make later states look inevitable.

## 13. Explicit non-goals

The Campaign product is deliberately **not** a license to build the following by default:

- centralized semantic routing;
- generic HTN planning;
- automatic Skill ranking;
- critic or voting swarms;
- self-modifying Skills;
- autonomous SkillOpt loops;
- a universal project-management engine;
- a campaign server/database/cloud backend without demonstrated need;
- a generic semantic truth validator;
- automatic external mutation authority;
- automatic Campaign selection from expertise/complexity/consequentiality scores;
- formal `LIGHT / STANDARD / HEAVY` Campaign modes without separate evidence and authority;
- cross-repository transaction/deployment coordination without demonstrated need.

These may be revisited only when concrete product pressure creates a consequential unresolved requirement.

SkillOpt-derived Skill-quality research and the boundary between that optional laboratory and the Campaign product are documented in [`research/skillopt-adaptation.md`](research/skillopt-adaptation.md). That record is provenance only; it does not add optimizer behavior or product authority to the Campaign.

## 14. Relationship to Skills and harnesses

Sensemaking Campaigns should work through existing coding-agent environments rather than requiring a proprietary autonomous runtime.

Harness adapters may install or expose:

- Skills;
- agent instructions;
- campaign continuation conventions;
- artifact locations;
- validation commands;
- handoff conventions;
- capability availability metadata.

Harness-specific details must remain outside the semantic core so the same Campaign model can survive changes in Claude Code, Codex, OpenCode, or other agent environments.

## 15. Product success properties

When Campaign durability is warranted, the Campaign model is successful when a real coding agent can:

```text
start
→ consume repository diagnosis when needed
→ record responsibility
→ bind authority
→ inspect available capability
→ perform bounded work
→ preserve validated evidence
→ record a durable transition
→ hand off
→ resume in a fresh context
→ continue or stop honestly
```

and when a reviewer can reconstruct **why the campaign is in its current state** from durable repository/campaign evidence rather than from private conversation history.

Campaign success is one part of Sensemaking product success; it does not imply every useful Sensemaking episode creates Campaign state.

## 16. Relationship to other repository documents

This document defines the durable **Campaign product model**.

Use the surrounding documents for different questions:

| Question | Source |
|---|---|
| How do I start using Sensemaking, including when Campaign is warranted? | [`../GETTING_STARTED.md`](../GETTING_STARTED.md) |
| How should a coding agent adapt scaffolding, rigor, and durability? | [`../skills/using-sensemaking/SKILL.md`](../skills/using-sensemaking/SKILL.md) and its `references/adaptive-guidance-v0.md` |
| What is a Sensemaking Campaign? | This document |
| What are we implementing for v0.3 right now? | [`productization-v0.3.md`](productization-v0.3.md) |
| What is the repository's current development frontier? | [`../STATUS.md`](../STATUS.md) |
| What does the typed campaign contract mean? | [`campaign-semantics.md`](campaign-semantics.md) and `src/sensemaking_skills/campaign_semantics/` |
| Who owns the top-level semantic control loop? | ADR 0013 |
| Current product boundary and routing/planning non-goals | [`ADR 0029`](adr/0029-current-product-boundary.md) |
| Where is the semantic-decision vs deterministic-orchestration boundary? | [`decision-orchestration-boundary.md`](decision-orchestration-boundary.md) |
| What is the current agent-native operating workflow? | [`agent-native-operating-workflow.md`](agent-native-operating-workflow.md) |
| Which SkillOpt ideas influenced Sensemaking, and which remain research/deferred? | [`research/skillopt-adaptation.md`](research/skillopt-adaptation.md) |

Versioned implementation plans may change. This product model should change only when the owner changes what a Sensemaking Campaign **is** or which architectural invariants define the product.
