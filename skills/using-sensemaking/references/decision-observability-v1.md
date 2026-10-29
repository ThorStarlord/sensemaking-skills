# Decision Observability (v1)

**Purpose:** When a user requests maximum decision transparency, make the
active agent's consequential reasoning-control choices inspectable while it
applies `using-sensemaking`. This is optional diagnostic guidance for the same
agent-owned controller, not a router, mandatory pipeline, authority grant, or
claim to reveal private internal reasoning.

**Load when:** a user asks for maximum decision transparency, a detailed
Skill-selection audit, or equivalent scrutiny of reasoning-control choices.
**Skip when:** ordinary proportional explanation is sufficient.

## Evidence and activation

Ordinary consequential repository-level use includes the substantive final
justification in `ontology-first-entry-v1.md` section 6 and the existing compact
receipt; no detailed execution audit is required. In maximum transparency,
record a contemporaneous, user-visible rationale *before* each consequential
selection, reconsideration, or stop, and reassess after consequential results.
Do not narrate every routine file read, force a choice among irrelevant Skills,
or invoke all specialists.
Depth is determined by what a reader needs to challenge the decision, not an
arbitrary word limit.

Keep three kinds of evidence distinct:

1. **Contemporaneous rationale:** the agent's declared basis, alternatives and
   expectations, recorded before action. It is self-report, not proof of the
   model's hidden causal computation.
2. **Observed execution:** host events, tool calls and results, insofar as the
   host exposes them. A planned invocation is not an observed invocation.
3. **Retrospective interpretation or causal probe:** later assessment of the
   trace, including missed opportunities or interventions. Label it as such;
   a rationale alone cannot establish causality.

Maximum transparency may itself affect the behavior being observed. A matched
baseline without the diagnostic instruction is needed to investigate that effect;
never claim equivalence, non-interference or causation from one trace.

## Decision lifecycle

Give each consequential decision a session-local identifier (`D-001`, etc.).
Before acting, record:

- the user's goal, current responsibility and scope/authority constraints;
- the source-linked evidence available then, assumptions and the nearest
  decision-changing uncertainty;
- relevant alternative responsibilities and specialist Skills actually
  considered, the selection or skip and the reasons for each material choice;
- the expected contribution and what evidence would change the choice.

After acting, append the actual mechanism and outcome, source/version when
known, relevant context supplied, observable event or artifact references,
errors and coverage limitations. Distinguish an instruction load from an
executed native call. Report what the result established, supported, challenged
or left unknown, whether it met the expectation, and the controller's resulting
choice to continue, reconsider, select or stop. The specialist's output is
input to the controller, not a decision delegated to the specialist.

Do not invent timestamps, references, arguments, events or prior deliberation.
If the host does not expose an event, mark it unavailable or unobserved. A
manual load followed by applying guidance is not a native invocation; a native
load does not prove the specialist completed its responsibility. A failed
native invocation and a subsequent manual fallback are separate events.

## Specialist classifications

Use these labels for individual evidence-backed events or conclusions, not as
exclusive lifecycle states. A Skill may be selected, fail, and later have its
instructions loaded manually. Identify the decision and evidence for each.

| Label | Supported meaning |
| --- | --- |
| `INVOKED_NATIVE` | A host-native Skill invocation was observed; completion needs separate evidence. |
| `INSTRUCTIONS_LOADED` | The specialist's `SKILL.md` was read manually; record whether its procedure was applied. |
| `SELECTED_INVOCATION_FAILED` | Selection was recorded and an attempted invocation failed; disclose the failure. |
| `CONSIDERED_SKIPPED` | A candidate and reason for not invoking it were recorded before the action. |
| `UNAVAILABLE` | The required Skill or host capability was actually found unavailable; identify the limitation. |
| `NOT_DOCUMENTED` | The record does not establish whether the Skill was considered; this proves neither rejection nor failure. |

A retrospective missed opportunity is a later interpretation, not a
`CONSIDERED_SKIPPED` event. Do not assign motives to undocumented omissions.

## Final audit and coverage

Provide the same substantive repository-level decision justification as ordinary
use: explain how the evidence, credible alternatives and consequences support
the recommendation, what could overturn it and where its authority ends. Do not
replace that synthesis with a chronology or longer procedural narration. A
focused task still explains only its actual scope; it does not require a new
repository-wide exploration.

Also produce a reviewable chronology of the documented decisions; a specialist
selection audit using the classifications above; expected versus observed
contributions and controller reassessments; retrospective missed opportunities;
and a stop rationale. Identify source and event references, known gaps and the
limits on each finding. Assess domain and architecture coverage, retained
knowledge and currentness, possibility breadth, alternatives, consequences,
governing decisions and authority, to the extent relevant to the user's task.
State significant unexamined areas and why they do or do not affect the outcome;
continue investigating when a gap can change an authorized conclusion.

When architecture is the question, distinguish evidence bearing on agent-native
composition (A), mechanical execution of an agent-selected Skill (A2), and
runtime-directed selection (B). A single host failure does not establish a need
for A2 or B. An explanation cannot prove its own cause or comparative benefit.

## Capture, confidentiality and continuity

The host's actual event stream, if available, is separate from the narrative.
Reference only events accessible to the reviewer; say when logs are unavailable,
partial, truncated or ephemeral. Prefer file paths, revisions and bounded
summaries over reproducing source, prompts, credentials, private data or tool
outputs. Follow target permissions and data-handling rules. Redact or omit
sensitive material before persistence or sharing, without implying a redacted
trace is complete. Do not loosen permissions to obtain evidence.

Keep extended Markdown in session output, or in a reviewable artifact only when
writing it is authorized. The normal session receipt remains compact; where a
report has been legitimately persisted in the repository, a responsibility may
point to it using the existing `artifact_refs` field. A working-tree-only audit
may disappear with the checkout; disclose its actual persistence. Neither a
receipt nor an audit authorizes Git, publication, implementation or access.
