"""Throwaway FULL spike #2: structure subsystem."""
layers = {"L0 Ontology": 3, "L1 Identity": 4, "L2 Structure": 8, "L3 Realization": 5, "L4 Expression": 2}
files = {"analyzer.py": "L2 diagnostics (run_all_diagnostics)", "proposal_models.py": "L2 plans", "bible_audit.py": "cross-layer validation", "diagnostics.py": "StructureDiagnostic", "state.py": "L2/L3 state"}
edges = [("analyzer.py","StoryBlueprint+StoryBible","diagnoses L1/L2/L3"), ("bible_audit.py","audit_bible_locations","validates realization vs structure"), ("proposal_models.py","StructureProposal","L2 thread/arc plans")]
cost = {"lines": 38, "files_read": 5, "time_min": 15}
partial = "architecture_fog -> docs-aligner (whole-repo)"
full = "architecture_fog CONFIRMED, narrowed: structure analyzer is well-bounded L2 diagnostics with explicit fail-closed rules (diagnostics.py). Churn c996f84 is additive F3, not systemic drift. Same workflow, scope narrowed to structure L2 proposal/diagnostic contract."
changed = False
print("STRUCTURE FULL nodes", sum(layers.values())+len(files), "edges", len(edges), "cost", cost)
print("PARTIAL:", partial)
print("FULL:", full)
print("Changed?", changed)
