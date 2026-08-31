"""Throwaway FULL spike #3: genre_pipeline subsystem."""
layers = {"L0 Ontology": 3, "L1 Identity": 5, "L2 Structure": 4, "L3 Realization": 3, "L4 Expression": 2}
files = {"runtime.py": "orchestration across layers", "identity.py": "compile_story_identity (L1)", "models.py": "GenrePipelineSpec", "registry.py": "genre packs registry", "validation.py": "L1 contract validation"}
edges = [("runtime.py","compile_story_identity","L1 compilation"), ("runtime.py","GenreSessionStore","cross-layer orchestration"), ("registry.py","genre_packs","L0 Ontology vocabularies")]
cost = {"lines": 35, "files_read": 5, "time_min": 14}
partial = "architecture_fog -> docs-aligner"
full = "architecture_fog CONFIRMED, narrowed: genre_pipeline is cross-cutting orchestration, not layer-owned; registry (L0) + runtime (orchestration) correctly separated per narrative-architecture.md cross-cutting note. No layer violation. Same workflow, scope = genre_pipeline orchestration boundary."
changed = False
print("GENRE_PIPELINE FULL nodes", sum(layers.values())+len(files), "edges", len(edges), "cost", cost)
print("PARTIAL:", partial)
print("FULL:", full)
print("Changed?", changed)
