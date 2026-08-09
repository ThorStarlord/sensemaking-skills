# Repository Sensemaking Brief

## 1. Repository goal
What this repo appears to be trying to accomplish.

## 2. Current shape
Main folders, files, skills, workflows, examples, and references.

## 3. Strong signals
What is already working or conceptually strong.

## 4. Missing pieces
What is absent, incomplete, or implied but not implemented.

## 5. Improvement opportunities
Useful refinements that are not urgent blockers.

## 6. Weakest boundary
The most ambiguous, unproven, unsafe, or unenforced part of the repo.

**You MUST classify the boundary using one of the recognized weakness types** (see
[Weakness Types](weakness-types.md)): `Vocabulary Drift`, `Contract Mismatch`,
`Ghost Features`, `Safety Gaps`, `Implicit Dependencies`, `Zero Validation`, or
`Orphaned Examples`. State it explicitly on its own line:

`**Weakness type:** <one of the recognized types>`

Example: `**Weakness type:** Zero Validation`

**This weakness-type enum is a completely different vocabulary from the
fog-type classification in Section 6.5 below.** Do not answer this question
with a fog-type value (e.g. `architecture_fog`) -- only the seven weakness
types listed above are valid here.

---

## 6.5. Problem classification (fog type)
Classify the primary type of uncertainty or problem:
- **product_fog**: Vague user needs, unclear feature requirements, undocumented workflows
- **ui_fog**: Navigation complexity, screen design issues, interaction patterns unclear
- **docs_fog**: Missing documentation, unclear specifications, knowledge gaps
- **architecture_fog**: Code structure problems, design issues, unclear boundaries (default if unclear)

This classification determines which implementation workflow will be used downstream.

## 7. Evidence
File-level evidence supporting the diagnosis (cites specific files and line ranges,
e.g. `scripts/validate-brief.py:46`).

**Output mode:** choose and signal the citation mode per [evidence-rules.md](evidence-rules.md)
("Citation Format: Two Output Modes"):

```markdown
<!-- mode: investigative | durable -->
```

- **investigative** (default, human readers): file paths **with line numbers**, e.g. `src/auth/login.ts:42-58`.
- **durable** (downstream skills that validate/transform evidence): file paths **only, no line numbers**, grep-verifiable claims.

If unsure, default to `investigative` -- a downstream skill can transform
investigative evidence into durable form, but the reverse is not possible
without re-running the analysis.

**This section's own prose must contain at least one literal file-path
citation** (e.g. `scripts/validate-brief.py:46`), even though Section 8
(evidence excerpts) and Section 13 (machine-readable `evidence:` list) also
carry structured citations. The validator checks Section 7's prose
independently -- citations that appear only in Sections 8/13 do not satisfy
this requirement.

Minimal valid example:

> `scripts/validate-brief.py:259` shows the Evidence-section check runs
> independently of the evidence_excerpts block in Section 8, which is why a
> citation must also appear here in Section 7's own prose.

**Logic trace (required):** Show the diagnostic reasoning that connects the cited
evidence to the weakest boundary — i.e., the chain from observed signals to your
conclusion. Begin this paragraph with the literal words "Logic trace:".

**State currency and claim provenance (required):** Keep observed evidence,
documented claims, inference, and owner-supplied judgment/context
distinguishable. Decision-changing current-state claims must explicitly
distinguish verified current state from merely documented state: when verified,
cite the probe used (e.g. git history, working-tree state, test runs, recent
reviews); when not verified, clearly identify the claim as documented but not
independently verified. Never treat documented state as automatically current.

## 8. Evidence excerpts
Each excerpt's `lines` field is a single line or a range. Use either the `Lx` /
`Lx-Ly` form (e.g. `L18`, `L25-L30`) or bare numbers (e.g. `18`, `25-30`) — both
are accepted. Every excerpt must include all four fields: `file`, `lines`,
`quote`, `supports_claim`.

`file` and `lines` are what matter — give the exact path and the smallest
line range that contains the cited text. Do not invent a path or a range you
have not actually read. **Do not hand-transcribe the `quote` text yourself:**
the runtime overwrites `quote` with the exact verbatim text it reads from
`file`/`lines` before validation runs (issue #89) — the model is no longer
the verbatim-copy boundary, because hand-transcription has been observed to
silently mangle Unicode punctuation (e.g. em dashes), drop leading
indentation, and alter Markdown formatting (bold/backticks). Write a short
placeholder for `quote` (e.g. `"see file/lines"`) rather than retyping the
source text.

```yaml
evidence_excerpts:
  - file: path/to/file.ext
    lines: L10-L15
    quote: "see file/lines"
    supports_claim: "..."
```

## 9. Why this boundary matters
What breaks if this remains weak.

## 10. Candidate next steps
2–5 possible next moves.

## 11. Recommended next step
The smallest concrete action with highest leverage.

If the recommended step depends on a current-state claim, cite the probe that
verified it, or state explicitly that the claim is documented but not
independently verified.

## 12. Recommended workflow
One workflow candidate from the official `workflow-registry.yaml`. Do not invent workflow IDs.

## 13. Machine-readable handoff

```yaml
artifact_id: repository_sensemaking_brief
schema_version: 1
source_intent_ref: artifacts/01-orchestration-run/00-user-intent.md
user_implied_fog_type: product_fog | ui_fog | docs_fog | architecture_fog | unknown
primary_fog_type: product_fog | ui_fog | docs_fog | architecture_fog | mixed | unknown
diagnosis_conflict: true | false
escalation_recommended: true | false
evidence:
  - "path/to/file.ext (lines L10-L15): short citation supporting the diagnosis"
  - "path/to/other_file.ext: short citation supporting the diagnosis"
recommended_workflow_id: # MUST match an ID in workflow-registry.yaml
recommended_execution_mode: plan_only | guided_execution
weakest_boundary:
weakness_type: # one of the 7 registered types in weakness-types.md, or "Other"
weakness_type_explanation: null # required non-empty string ONLY when weakness_type is "Other"; otherwise null
required_inputs:
  - user_intent
  - repository_state
created_at: "2026-05-19T16:00:00Z"
immutable: true
```

`weakness_type` is required metadata but non-blocking (D2): a missing or
unrecognized value is a validator warning, not an error, and never
invalidates the brief. It must match the `**Weakness type:**` line stated in
Section 6's prose. If none of the 7 registered types fit, use `Other` and
give a non-empty `weakness_type_explanation` — omitting the explanation for
`Other` is also a non-blocking warning, but it must be resolved before a
human grants final approval.

All required fields (Stage 1 intent-aware fields, standard routing fields, and
top-level fields required by `artifact-contracts.yaml`) MUST appear in that
**single** fenced yaml block above. Do not split them across multiple yaml
blocks — only the first yaml fence immediately following this heading is
parsed by `validate-brief.py`.

`evidence` is a required field: a list of short file-level citation strings
(the machine-readable counterpart to the prose in Section 7 / the excerpts in
Section 8). It is distinct from `evidence_excerpts` (structured excerpt
objects) — both are expected, under their own names.

### Complete Example
```yaml
artifact_id: repository_sensemaking_brief
schema_version: 1
source_intent_ref: artifacts/01-orchestration-run/00-user-intent.md
user_implied_fog_type: product_fog
primary_fog_type: product_fog
diagnosis_conflict: false
escalation_recommended: false
evidence:
  - "README.md (lines 5-12): feature requirements are vague, no user context"
  - "docs/ARCHITECTURE.md: does not exist"
recommended_workflow_id: product-implementation-workflow  # must be a top-level id from workflow-registry.yaml
recommended_execution_mode: guided_execution
weakest_boundary: Zero Validation
weakness_type: Zero Validation  # must be one of the 7 weakness types (weakness-types.md) or "Other", NOT a fog-type value
weakness_type_explanation: null
required_inputs:
  - user_intent
  - repository_state
created_at: "2026-05-19T16:00:00Z"
immutable: true
```

## 14. Ready-to-copy prompt
Prompt for `workflow-planner` or another downstream skill.
