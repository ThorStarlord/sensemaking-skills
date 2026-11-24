# Campaign Realization Assessment v1

**Status:** additive Campaign companion. It preserves the immutable
`extensions.capability_outcome` binding and appends agent-authored,
evidence-linked condition assessments under
`extensions.capability_outcome_realization`. It adds no aggregate completion
score, readiness verdict, planner or second truth system.

## Purpose

A bound capability outcome names the original realization conditions. Those
conditions do not stay self-explanatory as work proceeds: some accumulate
evidence, some remain partial, and some are contradicted. A later agent needs
to see all three without rewriting the original commitment:

```text
original conditions  -> immutable binding
current evidence     -> latest append-only assessment
remaining work       -> the agent's reading of partial, absent, contradicted
                        or unassessed conditions; no derived verdict
```

The assessment is a claim about evidence, not a claim that a condition is
satisfied. `EVIDENCE_PRESENT` means evidence was found, not that the condition
is complete. The binding continues to report `realization: not_established`.

## Write

```bash
sensemaking-skills campaign capability-outcome assess \
  --workspace /path/to/campaign \
  --repo . \
  --assessment assessment.json \
  --decision "Why this assessment is warranted" \
  --json
```

The command:

- refuses a Campaign without a bound capability outcome;
- requires `possibility_id` to match the binding;
- requires the exact 40-character source revision and validates it in `--repo`;
- requires exactly one entry for every binding condition, with no duplicates or
  omissions;
- validates every `file:` evidence path as tracked at that source revision and
  every `commit:` evidence ref as an exact local commit;
- appends the assessment with a same-state lifecycle transition, preserving the
  active responsibility and the binding;
- never changes `binding.realization`, `binding.remaining_conditions`,
  `binding.assumptions` or any prior assessment.

### Input

```json
{
  "possibility_id": "poss:goal-family-construction-bridge",
  "source_revision": "0e64430c83ca861b8e9ac2eaf5c842464c6891b3",
  "conditions": [
    {
      "condition_index": 1,
      "status": "EVIDENCE_PRESENT",
      "evidence_refs": ["file:docs/normal-use/example.md", "commit:..."],
      "basis": "What was inspected and what it shows."
    },
    {
      "condition_index": 2,
      "status": "PARTIAL_EVIDENCE",
      "evidence_refs": ["file:docs/normal-use/example.md"],
      "basis": "One observation only; the condition is not generally established."
    }
  ]
}
```

Allowed statuses:

| Status | Meaning |
| --- | --- |
| `EVIDENCE_PRESENT` | Evidence exists at the cited revision. It does not by itself establish satisfaction. |
| `PARTIAL_EVIDENCE` | Some relevant evidence exists, but coverage or applicability is incomplete. |
| `NO_EVIDENCE` | The condition was checked and no supporting evidence was found; the basis records the check. |
| `CONTRADICTING_EVIDENCE` | Evidence against the condition was found; the basis records it. |
| `NOT_ASSESSED` | The condition was not checked in this assessment; absence is not a failure. |

`EVIDENCE_PRESENT`, `PARTIAL_EVIDENCE` and `CONTRADICTING_EVIDENCE` require at
least one validated evidence ref. Every entry requires a non-empty basis.
Unknown fields are rejected so a free-form completion verdict cannot be
smuggled into the record.

## Read

`campaign working-context` and `campaign resume-profile` project the latest
assessment beside the binding:

- `working` and `audit` return the full latest assessment, including each
  condition's original text, status, evidence refs and basis;
- `minimal` returns the assessment id, source revision, count by status and the
  immutable binding realization;
- `audit` also returns the append-only assessment history.

`campaign capability-outcome bridge` adds:

- the latest assessment and its condition status counts;
- `realization_assessment_staleness` compared with the queried
  `indexed_ref`;
- `knowledge_realization` comparing the possibility's authored
  `assessed_ref` with the queried `indexed_ref`;
- caveats `REALIZATION_ASSESSMENT_NOT_PRESENT`,
  `REALIZATION_ASSESSMENT_STALE` and `KNOWLEDGE_REALIZATION_STALE` when
  applicable;
- the capability and component `claim_ceiling` and `scope` already authored in
  reviewed knowledge, so guidance-only and code-backed components are not
  flattened into one flag.

## Boundaries

```text
assessment             != completion
EVIDENCE_PRESENT       != condition satisfied
latest assessment      != readiness verdict
condition status count != score
source revision match  != evidence currentness
```

The assessment is agent-authored. Evidence refs are pointers; the agent that
reads them still decides applicability, sufficiency and the next responsibility.
The immutable binding remains the authority for the original commitment. A
different governing outcome requires a new Campaign.
