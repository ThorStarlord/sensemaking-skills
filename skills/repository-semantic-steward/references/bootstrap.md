# BOOTSTRAP — First-visit architectural understanding

## Purpose

Construct a useful architectural mental model that survives the coding agent's context, not a file catalog. Normal input includes contradictory documentation, missing architecture files, partial migrations, historic mistakes, active PR stacks and unknown components.

## Procedure

1. **Source identity:** Record repo, exact SHA and worktree state; read governing instructions and authorized owner goals. Current worktree may be dirty; use a separate clean worktree for index commands.
2. **Orientation:** Run `semantic knowledge-orient` against clean HEAD. Inspect missing document conventions, truncation and non-Python source coverage. Search manually beyond recognized paths where important.
3. **Product ontology:** Identify the product's domain nouns, types, rules, promises, non-goals, scope and semantic boundaries. Separate application domain concepts from repository knowledge types.
4. **Design and decisions:** Read current authoritative docs, ADRs and relevant history. Date and scope contradictory claims; newer files are not automatically stronger authority.
5. **Implementation model:** Trace meaningful capabilities to actual runtime owners, APIs, persistence, source paths and tests. Inspect JavaScript, SQL or other unsupported languages directly when needed; never infer runtime coupling from directories.
6. **Comparison and uncertainty:** Note discrepancies between declared architecture, tests and code. Keep unverified interpretations hypothetical/contested. Mark areas unassessed rather than invent missing edges.
7. **Reviewable knowledge:** Author source-grounded typed claims/relations in `.sensemaking/knowledge/*.json`, split by meaningful owner boundaries. Preserve current original sources instead of copying document passages wholesale.
8. **Publish and index:** Validate source refs and constraints in a clean snapshot after the proposed pack is committed; use the normal PR review path for consequential semantic conclusions. Build the SQLite snapshot externally at the new revision.
9. **Completeness record:** Summarize observed domains, unknowns, unsupported source formats, truncated selection and priority deepening opportunities. A useful wide overview does not require exhaustive code coverage.

## Suggested competency questions

- What is the repository for; which outcomes and non-goals govern it?
- Which domain concepts must not be conflated?
- Which components own a named user-visible capability and persistence boundary?
- What evidence establishes an actual dependency versus an inferred association?
- Which tests protect a declared invariant, and which claimed guarantees remain unverified?
- What are the important rejected alternatives, open decisions and architecture debt?
- What changed since the latest reviewed understanding?
- Could a fresh agent answer an unfamiliar cross-system engineering question from sources reachable through the model?

## Stop rule

Bootstrap once per materially new target or inadequate knowledge foundation, then enrich incrementally. Neither document count nor graph density is a completion metric. Finish with inspectable architectural value and an honest gap report.
10. **Architecture coverage map (schema_version 2):** model each top-level component and each ADR still in force, or list it explicitly as NOT ASSESSED. No minimum entry count is required. Add `layer`, `bounded_context` and `architecture_rule` records only where a real rule or distinction needs one, and give every rule a `rule_type`, `severity` and `applies_to` scope.
