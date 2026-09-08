# Campaign capability registry

**Status:** P6 product contract  
**Scope:** read-only capability metadata inspection for an already-warranted, agent-classified responsibility

## Purpose

P6 fills the capability-inspection step in the Sensemaking Campaign without moving semantic control into Python.

The boundary is:

```text
active responsibility
        ↓
active coding agent supplies responsibility classification
        ↓
strict capability metadata lookup
        ↓
deterministically ordered, unranked candidates
        ↓
agent chooses one / none / ordinary work
```

The permanent invariant remains:

```text
warranted responsibility
!= capability availability
!= execution authority
```

## Product surface

P6 adds:

```text
sensemaking-skills campaign capabilities \
  --workspace /path/to/CMP-0001 \
  --responsibility-type architecture_review \
  --json
```

`--responsibility-type` is deliberately supplied by the active coding agent. P6 does not infer it from the responsibility statement, evidence, artifact fields, mission, workflow metadata, or prior transition history.

The command requires an active durable responsibility so capability inspection remains contextual to a Campaign rather than becoming a detached semantic router.

## Catalog source

The installed package carries:

```text
src/sensemaking_skills/defaults/capability-registry.yaml
```

This is a small Campaign-specific metadata overlay. It declares facts that the current Skill/workflow catalogs do not already encode in the shape required by `campaign_semantics`:

- accepted responsibility types;
- input/output artifact contracts;
- completion conditions;
- capability kind;
- repository-mutation behavior;
- required authority classification;
- availability classification/reason;
- whether completion returns control to the campaign agent.

It does not copy complete Skill instructions or workflow definitions.

P6 loads these declarations into the existing semantic contracts:

- `Capability`;
- `RegisteredCapability`;
- `CapabilityRegistry`;
- `AvailabilityStatus`.

No second capability domain model is introduced.

## Workflow identity and liveness

Entries whose `kind` is `workflow` are mechanically cross-checked against the packaged workflow registry and liveness overlay.

The relevant distinction is:

```text
workflow registered
!= workflow currently live
```

A workflow whose effective liveness is `compatibility_only` remains identifiable but is forced to:

```text
availability: unavailable
```

with a reason explaining that current selection/execution is prohibited.

P6 never resurrects compatibility-only workflows merely because they remain in the durable catalog.

## Agent-native Skill availability

P6 does not pretend that the deterministic Campaign process can discover whether a Skill is actually installed in Claude Code, Codex, OpenCode, or another harness.

Current agent-native Skill entries therefore use:

```text
availability: external
```

unless their durable catalog status is already known to be unavailable (for example proposed/deprecated identities retained only for provenance).

Harness-specific discovery belongs to P10. This prevents:

```text
registered Skill
⇒ installed Skill
```

from becoming a false inference.

## Authority semantics

Each candidate exposes a **required authority classification** separately from the authority on the active responsibility.

For example, a response can honestly contain:

```text
responsibility_authority: authorized_autonomously
candidate.required_authority: owner_authorization_required
```

This is not an error and does not mean owner authorization has occurred. It means only that the candidate declares a stricter execution boundary than the responsibility currently carries.

P6 must never emit a derived field such as:

```text
authorized: true
```

without separate durable authorization evidence.

## JSON surface

A successful response has the shape:

```json
{
  "ok": true,
  "code": "CAMPAIGN_CAPABILITIES",
  "campaign_id": "CMP-0001",
  "responsibility_id": "R-ARCH-001",
  "responsibility_type": "architecture_review",
  "responsibility_authority": "authorized_autonomously",
  "candidate_count": 1,
  "candidates": [
    {
      "id": "architectural-review",
      "kind": "skill",
      "accepted_responsibility_types": ["architecture_review"],
      "input_artifact": "repository_sensemaking_brief",
      "output_artifact": "architectural_review_recommendation",
      "completion_conditions": ["..."],
      "mutates_repository": false,
      "required_authority": "authorized_autonomously",
      "availability": "external",
      "availability_reason": "...",
      "returns_control": true
    }
  ]
}
```

Candidate order is deterministic by capability ID. It is not a ranking.

## Honest empty results

An agent-classified responsibility type with no declared compatible capability is a successful inspection result:

```json
{
  "code": "CAMPAIGN_CAPABILITIES",
  "candidate_count": 0,
  "candidates": []
}
```

This represents an honest state such as:

```text
RESPONSIBILITY_WARRANTED
CAPABILITY_UNAVAILABLE
```

The deterministic layer does not convert the empty result into a hidden fallback, recommendation, or ordinary-coding selection.

## Strict catalog validation

The catalog loader fails closed on structural defects including:

- unsupported schema version;
- unknown top-level or capability fields;
- duplicate capability IDs;
- malformed list/string/boolean fields;
- unknown authority values;
- unknown availability values;
- workflow capability IDs absent from the workflow catalog;
- unknown workflow liveness values.

An invalid packaged catalog is reported as `CAPABILITY_CATALOG_ERROR`; it is not silently partially loaded.

## Explicit non-goals

P6 does **not**:

- infer responsibility type from prose;
- interpret repository evidence;
- rank candidates;
- emit a score, best candidate, or recommendation;
- select a capability;
- invoke a capability;
- treat catalog membership as runtime availability;
- treat availability as execution authorization;
- create or consume owner authorization evidence;
- automatically chain workflows;
- revive compatibility-only, proposed, or deprecated capability identities;
- implement harness-specific installation detection (P10);
- change the active responsibility or campaign state.

Therefore:

```text
Campaign Controller
!= semantic router

CapabilityRegistry
= inspectable catalog
!= selector
```

## Qualification expectations

A qualified P6 candidate must prove at least:

1. the packaged capability catalog loads outside repository-semantic reasoning;
2. real Skill and workflow identities are present;
3. the agent must explicitly supply responsibility classification;
4. candidates are deterministic and unranked;
5. unknown responsibility types return an honest empty set;
6. proposed/deprecated identities are not available;
7. compatibility-only workflows are mechanically unavailable;
8. responsibility authority and capability-required authority remain separate;
9. catalog corruption fails closed;
10. the command requires an active responsibility;
11. JSON contains no recommendation/rank/score/selection field;
12. installed-wheel packaging contains the catalog and supports capability inspection without a source checkout.
