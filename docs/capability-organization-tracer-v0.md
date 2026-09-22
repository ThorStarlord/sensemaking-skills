# Capability & Organization Tracer v0

**Status:** owner-directed executable tracer; first-class product inspection surface, not an organizational runtime  
**Date:** 2026-09-22  
**Tracker:** Issue #459  
**Product boundary:** ADR 0029 remains authoritative

## 1. Objective

Capability & Organization Tracer v0 tests one concrete product hypothesis:

> Existing Skills can serve as a legible capability substrate for an explicit
> multi-role organization without turning Sensemaking into a scheduler,
> automatic router, or worker-management runtime.

The tracer deliberately makes Organization mechanically inspectable while
keeping semantic selection and execution ownership with the active agent and
existing execution surfaces.

## 2. Product surfaces

The shipped CLI adds:

~~~text
sensemaking-skills organization skill-profile
sensemaking-skills organization inspect
sensemaking-skills organization role
~~~

These commands are read-only.

They may:

- expose a small non-authoritative Skill-capability profile overlay;
- validate that explicitly bound roles cover their declared capability requirements;
- validate role and relationship references;
- expose inbound/outbound evidence relationships for one role;
- check canonical Skill existence when a repository root is supplied.

They may not:

- select a Skill;
- decide that an Organization Pattern is warranted;
- assign an actor to a role;
- allocate a worker;
- schedule or retry work;
- grant authority;
- execute repository work;
- infer semantic truth or objective closure.

## 3. Skill-capability projection

Tracer v0 ships a deliberately small explanatory overlay:

~~~text
using-sensemaking
  package role: governance
  capability families:
    responsibility_control
    episode_coordination

repo-sensemaker
  package role: situated_skill
  capability family:
    repository_diagnosis

repair-verifier
  package role: situated_skill
  capability families:
    bounded_verification
    evidence_reconciliation

output-reconciler
  package role: capability
  capability family:
    evidence_reconciliation
~~~

The overlay is not a Skill Contract Manifest extension.

Where a repository root is supplied, the CLI can additionally expose existing
Skill Manifest fields such as domain, responsibility, and repository-mutation
posture. The overlay does not override those contracts.

~~~text
capability facet visible
!= capability selected
!= responsibility warranted
!= execution authorized
~~~

## 4. Repository Change Cell v0

The first Organization Pattern is:

~~~text
                  Controller
                  /        \
          optional          \
          Analyst          Builder
             \               |
              \              v
               +--------> Verifier
                              |
                              v
                          Reconciler
                              |
                              v
                          Controller
~~~

### Controller

Responsibility:

- preserve owner objective and authority;
- select the warranted bounded responsibility;
- decide continue / stop / escalate from returned evidence.

Capability binding:

- using-sensemaking for responsibility control and episode coordination.

### Analyst — optional

Responsibility:

- diagnose repository state only when decision-changing uncertainty warrants it.

Capability binding:

- repo-sensemaker.

### Builder

Responsibility:

- implement only the already-selected bounded repository responsibility.

Binding:

- external executor providing repository_implementation.

The Builder is intentionally not represented as a fake Skill.

### Verifier

Responsibility:

- independently test the bounded completion claim and expose unsupported claims or residual failure.

Capability binding:

- repair-verifier.

### Reconciler

Responsibility:

- reconcile implementation/verification evidence with the prior responsibility and claims.

Capability binding:

- output-reconciler.

## 5. Relationship model

Tracer v0 supports only explicit descriptive relationships:

~~~text
delegates_to
returns_evidence_to
reviews
informs
~~~

The default cell uses explicit evidence-carrying edges.

Relationship existence does not imply that an actor was instantiated or that
the work was executed.

## 6. Existing execution boundary is reused

Sensemaking already has the correct external-execution primitive:

~~~text
already-selected responsibility
-> execution handoff
-> external worker / factory
-> returned result evidence
-> parent reassessment
~~~

Organization v0 therefore adds no worker runtime.

For a real delegated episode:

1. use Organization Pattern v0 to inspect the intended role/capability topology;
2. let the semantic controller select the actual responsibility;
3. use the existing Campaign execution handoff/result interface when durable external delegation is useful;
4. return worker evidence;
5. verify/reconcile;
6. let the controller decide continuation.

~~~text
Organization Pattern
!= Campaign

Organization Pattern
!= execution handoff

Organization Pattern
describes responsibility topology

Campaign/execution
preserves durable objective/responsibility/evidence state
~~~

## 7. Why the overlay remains separate from Skill Contract Manifest v1

The tracer needs to test whether package role and capability-family facets are
actually useful.

Encoding them directly into every Skill Contract Manifest before that test
would prematurely make research vocabulary part of a deterministic contract.

Therefore v0 uses a packaged, explicitly non-authoritative overlay.

Promotion into manifest/schema authority would require repeated normal-use
evidence that the facets solve a real discovery, maintenance, or coordination
problem that cannot be served adequately by a read-only projection.

## 8. Qualification

Product and release qualification cover:

- default Repository Change Cell mechanical validity;
- explicit external-executor Builder binding;
- profile/manifest projection for existing Skills;
- role evidence-edge inspection;
- fail-closed behavior when capability requirements are uncovered;
- installed wheel/sdist ability to run the default Organization inspection.

These checks establish representation and packaging behavior only.

They do not establish that multi-role execution outperforms a single capable
agent.

## 9. Promotion questions

The tracer should answer these from real use:

1. Do explicit roles prevent responsibility confusion?
2. Do capability-family facets make Skill selection easier to understand?
3. Does Builder/Verifier separation catch consequential errors?
4. Does evidence get lost or distorted between roles?
5. Does authority leak from Controller into Verifier/Reconciler?
6. Does the Organization add useful coordination, or only ceremony?
7. Does one actor frequently occupy multiple roles without loss?
8. Does topology repeatedly need to change mid-task?

Only repeated evidence should justify broader machinery.

## 10. Explicit non-goals

Do not infer from Tracer v0 that the product should add:

- a worker registry;
- a scheduler or queue;
- automatic role assignment;
- dynamic Organization generation;
- peer-message transport;
- automatic capability/Skill routing;
- persistent workforce state;
- retries or parallel-execution control;
- Campaign schema v3;
- autonomous merge/release/deployment/publication.

The next larger implementation is warranted only if executable normal use shows
that these are the limiting factor.

## 11. Core laws

~~~text
role != Skill
Skill != actor
capability available != capability selected
role binding != actor assignment
organization valid != organization warranted
organization selected != execution authorized
worker success != verifier success
verifier success != parent objective closure
coordination topology != worker runtime
~~~
