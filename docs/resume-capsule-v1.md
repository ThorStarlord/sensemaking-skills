# Resume Capsule v1

**Status:** repository-only productization contract  
**Command:** `sensemaking-skills campaign resume-context`  
**Campaign schema:** unchanged (v2)  
**Semantic authority:** unchanged

Resume Capsule v1 makes durable Campaign continuation easier to consume without adding semantic summarization or a recommended next action.

## Projections

The existing full projection remains the default:

```bash
sensemaking-skills campaign resume-context \
  --workspace /path/to/campaign \
  --json
```

A smaller deterministic projection is available with:

```bash
sensemaking-skills campaign resume-context \
  --workspace /path/to/campaign \
  --compact \
  --recent-transitions 3 \
  --json
```

Compact mode preserves stable Campaign identity, mission/current state, authority/terminal state, target digest identity, bounded active responsibility/uncertainty fields, counts, bounded recent transition summaries, handoff presence, and semantic-companion integrity/count metadata. It omits larger full collections whose exact contents remain available through the default projection and `campaign inspect`.

## Optional mechanical preflight

Resume Capsule may include a bounded Campaign Preflight v0 summary:

```bash
sensemaking-skills campaign resume-context \
  --workspace /path/to/campaign \
  --compact \
  --include-preflight \
  --json
```

A failed preflight is surfaced as durable/mechanical context. It does not convert `resume-context` into a proceed/stop gate and does not select a repair.

## Explicit limits

```text
compact projection != semantic summary
preflight included != action recommendation
reference integrity != semantic truth
fresh-context reconstruction != reproduced hidden reasoning
resume context != authority to execute
```

No LLM-generated summarization, evidence ranking, hidden chain-of-thought capture, automatic responsibility selection, or Campaign schema migration is introduced by v1.

## Qualification boundary

Full/compact shape, bounded transition history, preflight embedding, and non-recommendation behavior are repository/hermetic contracts and can be qualified by tests and exact-head CI. Existing native-harness/product-value evidence ceilings remain unchanged.
