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
  schema_version: prototype-1
  domain:
    - product | architecture | ui | docs | integration
    # NOT a new taxonomy: these are the same base concepts as the canonical
    # primary_fog_type enum (docs/canonical-vocabulary.yaml), deliberately
    # reusing its vocabulary rather than inventing a second one (earlier
    # ledger reasoning, still correct: "fog taxonomy already approximates
    # this; reconcile the first taxonomy before adding a second").
    # The behavioral value this adds over primary_fog_type: `domain` is a
    # LIST. primary_fog_type must stay single-valued because routing
    # (ADR 0018) needs exactly one value to key off of -- but a
    # consequential_boundary is frequently NOT single-domain (P4's finding
    # was simultaneously product AND architecture: which surface is
    # canonical is a product question; how the two diverged is an
    # architecture question). Forcing that into one primary_fog_type value
    # already loses information today. `domain` doesn't fix routing (out
    # of scope, unchanged) -- it lets the brief say what primary_fog_type
    # structurally cannot.
  discovery_confidence:
    level: low | medium | high
    why_bounded: "..."
    # Formalizes the "Confidence and why bounded" prose pattern already
    # used downstream of repo-sensemaker (see
    # experiments/solution-interaction-s1-v1/owner-synthesis-v1.md section 8)
    # -- extending an existing habit, not inventing a new one. Answers a
    # DIFFERENT question than `uncertainty.source`: source asks "why is the
    # boundary I found unresolved?"; discovery_confidence asks "how sure am
    # I that I found the RIGHT boundary at all?" A repo whose real problem
    # is buried in runtime behavior or an external system may still produce
    # a structurally pristine brief around the wrong boundary -- this field
    # exists so that case is distinguishable from a genuinely
    # well-grounded finding, not to add another taxonomy.
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
  evidence_status_notes:
    # OPTIONAL. Per-excerpt confidence annotation, keyed to Section 8's
    # canonical evidence_excerpts by (file, lines) -- NOT a new field on
    # evidence_excerpts itself. Section 8's four required fields (file,
    # lines, quote, supports_claim) are ADR 0016-governed and untouched;
    # this is a parallel, vNext-only list. Deliberately NOT top-level
    # (earlier ledger reasoning, still correct: status belongs to a claim,
    # not to the brief as a whole -- different excerpts in the same brief
    # legitimately carry different confidence).
    - file: "..."
      lines: "..."
      status: observed | derived | interpretation | hypothesis
      # observed: directly read in the cited file/lines.
      # derived: a deterministic computation over observed evidence (e.g.
      #   this prototype's evidence scripts -- a duplicate-authority match,
      #   a version-drift diff).
      # interpretation: a semantic judgment about what observed/derived
      #   evidence means (e.g. "this pattern indicates X").
      # hypothesis: not yet confirmed; would need a probe (ties to
      #   uncertainty.source: empirical) to become observed/derived.
  evidence_note: >
    Three distinct evidence questions, not one ranking:

    (1) CITATION TRUST -- which source file to believe when two files
    disagree about a fact. Unchanged, canonical:
    code/tests > contracts/registries > accepted ADRs > canonical docs >
    open issues/proposed ADRs > historical status docs > untracked drafts.
    This prototype does not touch that hierarchy.

    (2) DESCRIPTIVE vs. NORMATIVE -- not a ranking, two different axes.
    Descriptive evidence (code, tests, runtime behavior, config) answers
    "what actually exists/happens?" Normative evidence (explicit owner
    decisions, Accepted ADRs, ratified contracts) answers "what is
    supposed to be true?" When they agree, cite either. When they
    DISAGREE (an Accepted ADR says B, the code does A), the correct
    consequential_boundary finding is "implementation has drifted from
    ratified intent" -- not "code wins because it's higher on the
    citation list." Report the disagreement as drift; do not collapse it
    into one ranking.

    (3) HISTORICAL/EMPIRICAL -- what happened in previous experiments or
    revisions (e.g. experiments/*/learning-v1.md, prior PRs, git history).
    This is neither a citation-trust question nor a descriptive/normative
    question -- it's evidence about trajectory and precedent, useful for
    discovery_confidence and for recognizing recurring patterns (e.g. "the
    same drift class has appeared twice before"), but it does not by
    itself establish current descriptive OR normative truth. A thing that
    was true in a past experiment is historical evidence that it might
    still be true now, not proof that it is.
```

### Field status (evidence level, per the assumption ledger)

| Field | Evidence level |
|---|---|
| `consequential_boundary` | Supported by P4 (n=1) |
| `uncertainty.source` | Supported by S1 (n=1, agent-selected target) |
| `owner_intent_state` | Exploratory — direct response to "never silently invent owner preference," not yet tested in an interaction |
| `domain` (list) | Exploratory — reuses canonical vocabulary, not a new taxonomy; multi-valuedness motivated by P4's actual finding spanning product+architecture |
| `discovery_confidence` | Exploratory — formalizes an existing prose pattern (S1 owner-synthesis section 8), no case yet where the *field* (vs. the prose habit) changed behavior |
| `evidence_status_notes` (per-excerpt) | Exploratory — added per this task's authorization; not yet exercised against a real disagreement between excerpts of different confidence |

None of this is claimed as validated. See
[the assumption ledger](../../docs/prototypes/repo-sensemaker-vnext.md) for
what would change that.
