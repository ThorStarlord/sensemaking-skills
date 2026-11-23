# Method-context provenance completeness and the recognition boundary (2026-11-22)

**Status:** normal-use observation plus a contained correction. **Source baseline:** `91dfc13bd5cd695d9b94dd54c25664cbefe0317b`. **Correction commit:** `c812a72578d998688d12a756e7711a7cd4f1742f`. This is not independent later-agent qualification, a controlled comparison or evidence of cognitive benefit. Issues #872 and #874 remain open.

## 1. Historical evidence: what L1 and L2 establish

The 2026-11-19 [cognitive capability assessment](../../research/cognitive-capability-assessment-20261119.md) records two behavioral observations.

**L1.** A fresh subagent (D2) read `docs/normal-use/2026-11-17-construction-vs-qualification-selection-lesson.md` before its first Sensemaking query, and the related lesson ranked first in its later search. It then rejected Issues #859, #872 and #874 as an "owner-gated qualification track, not a construction increment". No intermediate text or tool call shows the lesson's conditional applicability check. The record establishes pre-decision exposure without a visible check; it does **not** show that the lesson was ignored, that a different decision would have been better, or that the behavior recurs.

**L2.** D2 and D3 both read the lesson source, but D3 reported applying the two-gate check while D2 did not. D2 was choosing among several candidates; D3 was answering a single-item evidence question. The pair is not a controlled comparison. Task framing is a plausible explanation, not an established cause, and two instances do not establish a rate.

The records also show that D2's issue read was body-only, while the owner amendment was present in the lesson's own source. Evidence access was therefore sufficient for the distinction; the missing element was its use.

## 2. Current consumer check

At `91dfc13b`, the current optional consumer was exercised with the D2-like question:

```bash
semantic method context \
  --question "Should I choose a useful construction increment now or wait for independent qualification evidence?" \
  --repo . --ref HEAD --json
```

It returned both current method lessons, each with its authored scope, conditions, claim ceiling, counterevidence, original outcome, `source_records` and later records. The selection consumer (`workspace-query --operation product-outline --method-question ...`) returned the same candidates and kept `applicability_to_present_task: NOT_ESTABLISHED`. The 2026-11-17 presentation defect (L5) is no longer current; search output leads with the statement.

The current consumer therefore supports discovery and source inspection. It does not perform recognition, applicability judgment or method selection; those remain agent-owned by design.

## 3. Confirmed completeness defects

### 3.1 Empty visible records under truncation

`method_adaptation.py` computed:

```python
(not neighbors["truncated"] and all(...)) if records else True
```

The conditional expression returned `True` for an empty record set even when the one-hop `explain` neighborhood was truncated. `explain` slices claims and relations to its limit and sets `truncated` when either exceeds it.

A disposable repository with one method lesson and 251 outgoing `references` relations (252 claims, 251 relations) was queried through the real `semantic method context` CLI. Before the correction, the candidate returned `related_records_complete: true` with zero `source_records` and zero `later_related_records`, although the `explain` neighborhood was truncated. This contradicts the documented contract that an omitted source makes the flag false.

After the correction, the same query returns `related_records_complete: false`. The real current lessons, whose neighborhoods are not truncated, remain `true`.

### 3.2 Dropped non-observation/lesson `learned_from` sources

The consumer kept an outgoing `learned_from` target only when its indexed kind was `observation` or `lesson`. Real reviewed lessons include `learned_from` edges to `incident` records, `decision` records and one unindexed `adr:` target. A future method lesson derived from an incident would have shown no source while still reporting complete provenance.

A disposable repository with a method lesson `learned_from` an incident was queried through the real CLI. After the correction, `source_records` contains the incident with `source_read_status: INDEXED_RECORD` and the candidate reports complete. Outgoing `references` remain source records only when they name an observation or prior lesson; other references are not source records. An unindexed target remains visible with `NOT_ASSESSED`, making completeness false rather than silently dropping it.

## 4. What the correction changes, and what it does not

**Changes**

- `related_records_complete` is false whenever the `explain` neighborhood is truncated or any listed later/source record is not indexed.
- Every outgoing `learned_from` target is visible as a source record, regardless of kind.
- Unindexed sources remain visible as `NOT_ASSESSED`.
- The consumer contract and hosted checks state the empty-set and truncation semantics.

**Does not change**

- Candidate discovery, ranking or applicability judgment.
- The method lessons, their scope or authority.
- Any automatic method selection, mandatory checklist or reflection stage.
- The historical L1/L2 observations or their evidence ceiling.

## 5. Diagnosis: substrate truthfulness versus recognition

The current evidence does not support a current discovery, timing or source-availability defect:

- The D2-like question retrieves the relevant lesson.
- D2 had the lesson's source text before its decision.
- The current consumer exposes source records and later observations, including D2 and D3.

The nearest evidenced limitation is **recognition/applicability judgment**, with **host invocation** and **observation limitation** as competing explanations. D2's private reasoning is not reconstructed; the absence of a visible check is not proof that no judgment occurred. The framing difference between D2 and D3 remains an untested hypothesis. A source-grounded rejection of a lesson remains a valid outcome.

The completeness defects were real substrate-truthfulness defects: they could tell an agent that provenance was complete when it was not. Fixing them improves the evidence available for judgment. It does not demonstrate that an agent will now make a better method choice.

## 6. Evidence ceiling

| Level | Status |
| --- | --- |
| Current consumer discovery and source-record disclosure | Observed through the real CLI |
| Empty-truncated and incident-source branches | Verified through disposable real CLI probes |
| Real current method candidates unaffected | Observed |
| Agent reads the corrected field and changes a decision | Not observed |
| Independent later-agent use | Not established |
| Decision influence, comparative benefit or longitudinal development | Not established |
| #872 / #874 | Open |

No new method lesson, method selector, applicability checklist or mandatory reflection is warranted by this evidence. The next useful evidence is an authentic later agent facing a consequential method choice with the current consumer available, not another representational layer.
