# Repository Sensemaking Brief (vNext prototype)

**PROTOTYPE — prototype/repo-sensemaker-vnext.** Sections 1-14 below are
**byte-identical in structure** to the canonical
[Repository Sensemaking Brief](../../repo-sensemaker/references/repo-analysis-template.md)
and remain fully valid against `scripts/validate-brief.py` — this prototype
does not redefine any ADR-governed field. Section 15 is new, additive, and
read by nothing canonical. A brief built from this template is a normal,
valid `repository_sensemaking_brief` artifact *plus* an experimental
appendix.

---

## 1. Repository goal
## 2. Current shape
## 3. Strong signals
## 4. Missing pieces
## 5. Improvement opportunities
## 6. Weakest boundary

*(Sections 1-6: unchanged from canonical. See the canonical template for
full guidance text — not reproduced here to avoid a second copy of the same
prose drifting out of sync.)*

**Prototype note on Section 6:** if the consequential boundary identified in
Section 15 is a *legitimate unresolved choice* rather than a demonstrated
weakness, Section 6 may say so plainly (e.g. "no defect identified; see
Section 15 for the unresolved decision") instead of forcing a weakness-type
classification here. Section 13's `weakness_type` field still accepts
absence as a non-blocking warning today (D2) — this prototype does not
change that validator behavior, it only stops treating the warning as
something to suppress by inventing a label.

## 6.5. Problem classification (fog type)
## 7. Evidence
## 8. Evidence excerpts
## 9. Why this boundary matters
## 10. Candidate next steps
## 11. Recommended next step
## 12. Recommended workflow
## 13. Machine-readable handoff

*(Sections 6.5-13: unchanged from canonical, including the exact YAML
fence `validate-brief.py` parses. Do not add vNext fields inside this
block — they belong in Section 15's separate fence.)*

## 14. Ready-to-copy prompt

*(Unchanged from canonical.)*

---

## 15. Analysis vNext (PROTOTYPE — not read by any canonical validator)

This section exists to test three hypotheses concretely, not to declare them
settled:

1. Does separating *consequential boundary* from *weakest boundary* produce
   a truthful brief in cases where nothing is actually broken? (Evidence:
   P4 — two parallel implementations, no defect, no canonical way to say so.)
2. Does classifying *why* the boundary is unresolved change what a
   downstream reader should do next? (Evidence: S1 — repository-evidence vs.
   owner-intent uncertainty routed to different next actions.)
3. Can `owner_intent_state` prevent this skill from silently inventing an
   owner preference when intent is thin or absent?

```yaml
analysis_vnext:
  schema_version: prototype-0
  consequential_boundary:
    description: "..."
    rationale: "..."
    is_demonstrated_weakness: true | false
    # If true, Section 13's weakness_type must be one of the 7 registered
    # types (unchanged canonical rule). If false, Section 13's
    # weakness_type may be omitted (already non-blocking per D2) --
    # this prototype adds no new sentinel value, per the assumption
    # ledger's explicit rejection of "weakness_type: none" as a canonical
    # change (see docs/prototypes/repo-sensemaker-vnext.md, A-05).
  uncertainty:
    source: repository_evidence | empirical | owner_intent | external_environment
    question: "..."
    # The unresolved question itself, regardless of source -- every source
    # has one (e.g. empirical: "does Cartographer's behavior actually meet
    # the intended quality bar?"; repository_evidence: "which of these two
    # implementations does the production path actually invoke?"). This
    # field does NOT decide who the question is "for" -- that's what
    # `source` is for. Only when source is owner_intent does the caller
    # (repo-sensemaker's interaction layer) convert this into something to
    # ask the owner, and only then does neutral phrasing apply.
    #
    # Deliberately no `recommended_next_information_action` field here
    # (removed -- see assumption ledger A-03/A-06): it would be a stored,
    # model-authored duplicate of a pure function of `source`
    # (repository_evidence->investigate, empirical->probe,
    # owner_intent->ask_owner, external_environment->inspect_external),
    # creating a class of bug where the two fields silently disagree (e.g.
    # source: owner_intent + action: probe). The mapping lives once, in
    # repo-sensemaker's SKILL.md workflow diagram, derived at read time.
  owner_intent_state:
    known: "what was already established, verbatim or summarized"
    unresolved: "what remains unknown, if anything"
    status: sufficient | thin | blocking_unknown
    # blocking_unknown means this skill could not produce a confident
    # consequential_boundary without owner input it does not have --
    # the caller (interaction layer) must decide whether to ask, this
    # skill must not guess.
  evidence_note: >
    Citation-level trust (which SOURCE FILE to believe when two files
    disagree about a fact) still follows the existing, unchanged
    evidence-authority hierarchy (code/tests > contracts/registries >
    accepted ADRs > canonical docs > open issues/proposed ADRs > historical
    status docs > untracked drafts) -- this prototype does not touch that.
    But that hierarchy answers a citation question, not a conflict
    question, and this block's reasoning needs the latter: descriptive
    evidence (code, tests, runtime behavior, config -- "what actually
    exists/happens") and normative evidence (explicit owner decisions,
    Accepted ADRs, ratified contracts -- "what is supposed to be true") are
    not the same axis, and one is not simply higher-ranked than the other.
    When they agree, cite either. When they DISAGREE (an Accepted ADR says
    B, the code does A), the correct consequential_boundary finding is
    "implementation has drifted from ratified intent" -- not "code wins
    because it's higher on the citation list." Report the disagreement as
    drift; do not collapse it into one ranking.
```

### Field status (evidence level, per the assumption ledger)

| Field | Evidence level |
|---|---|
| `consequential_boundary` | Supported by P4 (n=1) |
| `uncertainty.source` | Supported by S1 (n=1, agent-selected target) |
| `owner_intent_state` | Exploratory — direct response to "never silently invent owner preference," not yet tested in an interaction |

None of this is claimed as validated. See
[the assumption ledger](../../docs/prototypes/repo-sensemaker-vnext.md) for
what would change that.
