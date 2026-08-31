"""Throwaway FULL prototype spike: detailed architecture graph for auteur author_decisions.

Purpose: measure cost vs benefit of building FULL vs PARTIAL (narrative-architecture.md + 2 ADRs)
for H1. Not a formal schema — throwaway to answer: does FULL change next warranted responsibility?
"""

layers = {
    "L0 Ontology": ["concepts", "relationships", "vocabularies"],
    "L1 Identity": ["StoryIdentity", "AuthorDecision.models: UnresolvedChoice", "genre/medium/scope"],
    "L2 Structure": ["StoryBlueprint", "threads/arcs/beats", "setup/payoff"],
    "L3 Realization": ["consequences.py: ConsequenceRefs", "context.py: ResolvedBinding", "scenes/events"],
    "L4 Expression": ["prose/voice/dialogue"],
}

scopes = ["Universe", "Series", "Book", "Chapter", "Scene"]

author_decisions_files = {
    "models.py": {"layer": "L1 Identity", "depends": ["decision.models.UnresolvedChoice"], " churn": "high"},
    "context.py": {"layer": "L3 Realization (projection M2)", "depends": ["StoryIdentity", "StoryBlueprint", "models.AuthorDecision"], "churn": "high"},
    "consequences.py": {"layer": "L3 Realization (M2 consumer)", "depends": ["models.AuthorDecision", "context.ResolvedBinding"], "churn": "high"},
    "report.py": {"layer": "L3 Realization", "depends": ["consequences.ConsequenceRefs"], "churn": "low"},
}

adrs = {
    "ADR 004": "Story Identity Schema",
    "ADR 010": "Genre Overrides/Consequence Classification",
    "ADR 014": "Agentic Editing Mode V1",
    "ADR 015": "Relationship Map Round-trip",
}

edges = [
    ("models.py", "L1 Identity", "defines AuthorDecision"),
    ("context.py", "L1+L2", "resolves refs against Identity+Blueprint (fail-closed)"),
    ("consequences.py", "L3", "consumes context, reports structural consequences per alternative"),
    ("consequences.py", "ADR 010", "one_of vs choose_k_of_n classification"),
    ("context.py", "ADR 015", "explicit relates_to only mechanism"),
]

cost = {
    "lines": 42,
    "files_read": ["docs/narrative-architecture.md", "src/auteur/author_decisions/models.py", "context.py", "consequences.py", "docs/adr/004,010,015"],
    "time_minutes": 18,
}

partial_decision = "architecture_fog: docs sprawl (296/109 historical) + churn in author_decisions -> recommend docs-aligner + to-prd"
full_decision = "architecture_fog CONFIRMED but narrowed: churn is contained in L1->L3 fail-closed projection (context.py) and M2 consumer (consequences.py), not systemic Layer 0/2 drift. Same workflow (docs-aligner) but scope narrowed to author_decisions M2 contract, not whole repo."

benefit_changed = False

print("FULL GRAPH NODES:", sum(len(v) for v in layers.values()) + len(scopes) + len(author_decisions_files))
print("EDGES:", len(edges))
print("COST lines:", cost["lines"], "files:", len(cost["files_read"]), "time min:", cost["time_minutes"])
print("PARTIAL decision:", partial_decision)
print("FULL decision:", full_decision)
print("Did FULL change next warranted responsibility?", benefit_changed)
print("Conclusion: For this slice, FULL cost 18min/42 lines for 0 decision change — PARTIAL sufficient.")
