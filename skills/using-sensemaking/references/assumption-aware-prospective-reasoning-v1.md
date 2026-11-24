# Assumption-Aware Prospective Reasoning v1

**Status:** optional agent-facing procedure. It composes the existing
possibility ecology and a read-only contrast operation. It does not generate
possibilities, infer assumptions, rank scenarios, select a direction or
authorize construction.

## When to use

Use this procedure when a consequential product or construction decision may be
bounded by unexamined assumptions: the current option set feels complete, the
same candidates keep returning, or a direction depends on a premise that has
not been checked.

Skip it for narrow local work, a decision whose assumptions are already stable,
or a mere request to list possibilities.

```text
assumption visible     != assumption true
assumption negated     != assumption false
shared assumption      != recommendation to combine
unassessed             != absent
scenario contrast      != selection or ranking
```

## Procedure

1. **Anchor the governing outcome.** State the product goal and the actual
   implementation or consumer behavior at stake. Use the current source, not
   only the possibility record.
2. **Retrieve the authored ecology.**
   ```bash
   sensemaking-skills semantic workspace-query --repo . --ref HEAD \
     --operation possibility-ecology --subject <goal-or-opportunity-id> --json
   ```
   Inspect each candidate's dimensions, relationships, assumptions, required
   capabilities and any `relationship_omitted` count. A truncated relationship
   projection is `PARTIAL`, not complete.
3. **Build the assumption index.** Assumptions are authored `references` with
   `conceptual_relation` `assumes` or `sharesAssumptionWith`. Inspect the
   original claim, evidence and counterevidence for any assumption that could
   change the choice. Other premises remain `NOT_ASSESSED`.
4. **Author a small scenario set.** Start with `base`. For each assumption that
   could change the option set, author a scenario that negates it. Keep the
   scenario set small enough to interpret; do not enumerate every combination.
   ```json
   {
     "scenarios": [
       {"id": "base", "negated": [], "held": []},
       {"id": "no-cross-episode",
        "negated": ["hyp:cross-episode-synthesis-recurs"]}
     ]
   }
   ```
5. **Run the contrast.**
   ```bash
   sensemaking-skills semantic possibility contrast --repo . --ref HEAD \
     --subject <goal-or-opportunity-id> \
     --scenarios scenarios.json --json
   ```
6. **Read the result carefully.**
   - `AFFECTED`: the candidate visibly assumes a negated assumption.
   - `UNAFFECTED`: the candidate has visible assumptions, none negated.
   - `NOT_ASSESSED`: no visible assumption relation; this is not evidence that
     the candidate has no assumptions.
   - `PARTIAL`: the one-hop relation projection was truncated; use `explain` on
     that claim before relying on an absence.
   - `candidate_omitted` / `descendant_candidate_omitted`: candidates were cut by
     the query limit and were not contrasted. The scenario result is partial even
     when every visible candidate has complete relationship coverage.
   - `conflicts`: a visible candidate contradicts a held claim. `held` is used
     only for this conflict check and otherwise does not change a candidate's
     `AFFECTED`/`UNAFFECTED` classification; a conflict is a question, not a
     recommendation.
   - `shared_assumptions`: candidates sharing an assumption but lacking a direct
     relation are questions for the agent, not an endorsed combination.
7. **Interpret.** Ask:
   - Which candidate survives only under an assumption the evidence weakens?
   - Which candidate is unassessed because its premises were never authored?
   - Does a shared assumption expose a materially different combination?
   - Is the candidate set too thin for the governing goal?
8. **Decide.** Continue, reframe, author a new candidate through the existing
   `semantic possibility record` producer, or stop. The agent owns the
   selection. A justified `NO_MODEL_CHANGE` is valid.
9. **Reconcile.** Record only consequential evidence. Do not treat a scenario
   contrast as proof that an assumption is true or false, or as proof that a
   new direction is valuable.

## Minimal command sequence

```bash
# 1. see the authored ecology and its assumption relations
sensemaking-skills semantic workspace-query --repo . --ref HEAD \
  --operation possibility-ecology --subject goal:compounding-product-knowledge --json

# 2. author scenarios.json, then contrast
sensemaking-skills semantic possibility contrast --repo . --ref HEAD \
  --subject goal:compounding-product-knowledge \
  --scenarios scenarios.json --json

# 3. if a genuinely new candidate survives, retain it as a hypothesis
sensemaking-skills semantic possibility record --repo . \
  --episode artifacts/history/<episode>.json \
  --output .sensemaking/knowledge/<proposal>.json
```

The producer validates provenance and writes an unreviewed proposal. Ordinary
Git review remains. It does not promote the candidate to strategy.

## Failure modes

- **Negation-as-evidence:** a scenario says what would change if an assumption
  were false; it does not show that it is false.
- **Scenario theater:** many scenarios can create the appearance of rigor
  without a decision-changing contrast.
- **Combination endorsement:** shared assumptions are prompts to inspect an
  unrepresented combination, not a recommendation to build it.
- **Omission blindness:** a candidate with partial relationship coverage may
  have assumptions outside the view.
- **Confirmation scenarios:** author scenarios before looking for a preferred
  answer; include the base case and a scenario that could defeat the current
  preference.
- **Ranking by proxy:** the operation returns no score, ranking or next action.

## Evidence ceiling

The command establishes that authored assumption relations and an
agent-authored scenario were projected at one committed revision. It does not
establish that the assumptions are correct, that the scenario is exhaustive,
that a candidate is valuable, or that the contrast improved the decision.
Those remain agent judgment and, where claimed, separate qualification.
