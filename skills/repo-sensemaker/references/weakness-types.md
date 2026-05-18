# Weakness Types in Repositories

When identifying the **Weakest Boundary**, look for these common types:

1. **Vocabulary Drift**: Terms used in the README don't match the code or directory structure.
2. **Contract Mismatch**: Files claim to be one format (e.g., `.yaml`) but are actually another (e.g., Markdown).
3. **Ghost Features**: Functionality mentioned in documentation that has no corresponding implementation.
4. **Safety Gaps**: Autonomous workflows that lack mandatory human-approval gates.
5. **Implicit Dependencies**: Skills or scripts that depend on files or paths not explicitly defined or validated.
6. **Zero Validation**: Core logic or structure that has no automated check (e.g., no `validate-repo.py` or equivalent).
7. **Orphaned Examples**: Examples that are outdated or don't follow current templates.
8. **Incomplete Refactoring with Divergence Risk** (NEW): Two coexisting data access patterns (old + new) that can diverge because:
   - New pattern has low coverage (<80%) and is partially implemented
   - No consistency tests verify both patterns produce identical results
   - No deprecation plan documents migration timeline
   - Developers don't know which pattern to use for new code
   - **Example**: Finance system with both direct Supabase queries and DAL wrapper functions, but only 40% migrated to DAL and no tests comparing both paths.
   - **Risk**: Silent divergence - both systems appear to work, but data could diverge without warning.
   - **Detection**: Search for coexisting patterns, measure DAL coverage, check for consistency tests, look for deprecation roadmap.
