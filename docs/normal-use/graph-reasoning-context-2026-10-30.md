# Graph reasoning: controller and Steward decision context

## Question and decision

For the owner's graph-reasoning plan, should the controller or RECALL guidance
be extended to make knowledge activation mandatory, and what governs changes
to those two surfaces? This is a real decision in WP-1 and WP-3, not an
independent qualification. At `74384f2aaf96d7b73403be3617187f5aa349b6b9`,
the controller already triggers narrow RECALL when retained knowledge could
change a bounded decision; the Steward reference selects existing queries,
requires original-source checks, allows direct authored-record fallback and
keeps routine edits lightweight. A mandatory consultation stage would conflict
with that adaptive boundary. **No Skill instruction change is warranted by
this case.** Whether agents actually follow the guidance in fresh hosts remains
unassessed.

## Retrieval and source checks

The CLI was run from this checkout's `src` through Python, not the older
editable installation on PATH. A clean source-pinned index outside the checkout
was built at `74384f2aaf96d7b73403be3617187f5aa349b6b9`. It included Git
path containment; its 677 claims and 666 relations include mechanical records,
not just the authored graph. The active HEAD matched, and no changes were
unindexed at the queries below.

- `context-for` with paths `skills/using-sensemaking/SKILL.md` and
  `skills/repository-semantic-steward/references/recall.md` returned the
  broad `skills/**` artifact-path rule and historical linked observations.
  For **each** path, ownership, contracts, decisions and alternatives were
  `NOT_ASSESSED`; neither context was truncated. The rule did not answer this
  decision and the gaps did not establish absence of a governing decision.
- Literal `search` for `retrieval`, `recall` and `ontology-first` returned
  `decision:ontology-first-adaptive-sensemaking`. The original ADR 0034 and
  the two Skill sources establish the controller/Steward division; ADR 0029
  establishes the agent-owned control boundary. The decision record's
  qualification note, however, described the cloud pair as interrupted.
  The cited operational qualification report states the cloud pair was
  recovered and completed; the separate local pair stayed interrupted. Its
  verdict is narrow reuse on one assumption and possibility, not comparative
  superiority.

This retrieval affected the decision: it exposed the missing access path and
directed source inspection to ADR 0034, which ruled out treating the Steward
as another controller. It did not establish complete decision coverage.

## Relational verdict

**Claim:** ADR 0034 governs the `using-sensemaking` entrypoint and composes
the Steward under agent-owned control, at the inspected revision. Direction:
positive.

- **Declared:** guidance and accepted product decision, ADR 0034 decisions B,
  C, E and G, plus the two Skill files. The agent, not deterministic machinery,
  selects responsibility.
- **Implemented:** the two checked Skill documents express those roles; this
  is guidance, not a runtime promise.
- **Exercised:** this session manually read and applied those instructions; it
  did not observe native Skill invocation. General adherence is not assessed.
- **Graph:** the decision was recorded and searchable; the two path contexts
  lacked owner-to-decision links at the indexed revision.
- **Assessment:** `HOLDS` for the declared role division; the path-specific
  graph coverage was incomplete. Residue: `none` for this bounded claim.
  The controller chooses the response; RELATE does not authorize it.
- **Knowledge:** add only the source-supported path anchors and `decided_by`
  links; revise the stale qualification note. Existing `context-for` is the
  consumer, so no retrieval code or ontology construct is proposed.

The negative claim that these paths have no governing decision would be
`OVERSTATED`: the graph miss is contradicted by ADR 0034 and the Skill text.
This does not establish that all relevant decisions, alternatives or
dependencies have been modeled. ADRs 0032 and 0033 remain proposed; mechanical
proposal validation and later retrieval are not semantic truth or independent
proof of agent benefit.
