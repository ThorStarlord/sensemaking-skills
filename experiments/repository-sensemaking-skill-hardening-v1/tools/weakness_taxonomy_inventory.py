"""Commit 3 - GAP-6 taxonomy inventory over the 25 corpus weaknesses.

Classifies every ground-truth weak boundary against the seven canonical
types, records the chosen mapping and fit, and decides outcome A vs B.
"""
from __future__ import annotations

from pathlib import Path

import yaml

WORK = Path(r"H:\GithubRepositories\sensemaking-skills\experiments\repository-sensemaking-skill-hardening-v1")
CORPUS = WORK / "corpus"

CANONICAL = {
    "Vocabulary Drift", "Contract Mismatch", "Ghost Features", "Safety Gaps",
    "Implicit Dependencies", "Zero Validation", "Orphaned Examples",
}

# mapping guidance per corpus weakness -> canonical type + fit note
FIT_NOTES = {
    "Zero Validation": ("Zero Validation", "exact fit - canonical type 6"),
    "Contract Mismatch": ("Contract Mismatch", "exact fit - canonical type 2"),
    "Implicit Dependencies": ("Implicit Dependencies", "exact fit - canonical type 5"),
    "Ghost Features": ("Ghost Features", "exact fit - canonical type 3; D5 high-risk (substantive audit)"),
    "Vocabulary Drift": ("Vocabulary Drift", "exact fit - canonical type 1"),
    "Safety Gaps": ("Safety Gaps", "partial fit: canonical definition is autonomous-workflow human gates; app-code use requires prose justification (plugin-architecture)"),
    "Orphaned Examples": ("Orphaned Examples", "exact fit - canonical type 7"),
}


def main() -> None:
    gt = yaml.safe_load((CORPUS / "ground-truth.yaml").read_text(encoding="utf-8"))["repositories"]
    scored = yaml.safe_load((WORK / "baseline-scored.yaml").read_text(encoding="utf-8"))["rows"]
    brief_type = {r["repository_id"]: r["weakness_type"] for r in scored}

    rows = []
    types_used = {}
    for entry in gt:
        rid = entry["repository_id"]
        gt_type = entry["known_weak_boundaries"][0]["type"]
        canonical, note = FIT_NOTES.get(gt_type, (gt_type, "not in canonical set - needs mapping"))
        types_used[canonical] = types_used.get(canonical, 0) + 1
        rows.append({
            "repository_id": rid,
            "ground_truth_type": gt_type,
            "canonical_type": canonical,
            "fit": note,
            "baseline_brief_type": brief_type.get(rid),
        })

    canonical_fit = sum(1 for r in rows if r["canonical_type"] in CANONICAL)
    decision = "A" if canonical_fit == len(rows) else "B"
    out = {
        "schema": "weakness-taxonomy-inventory-v1",
        "phase": "commit-3",
        "decision": f"Outcome {decision}",
        "decision_rationale": (
            "Outcome A: all 25 corpus weaknesses map to canonical types; keep the "
            "seven types, document mapping guidance in SKILL.md, and use Other only "
            "with explanation. No schema/validator/consumer changes needed, so no "
            "compatibility risk."
            if decision == "A"
            else "Outcome B: extension required - schemas/validators/consumers must be updated."
        ),
        "canonical_types_used": types_used,
        "repositories": rows,
    }
    out_path = WORK / "weakness-taxonomy-inventory-v1.yaml"
    out_path.write_text(yaml.safe_dump(out, sort_keys=False), encoding="utf-8")
    print(f"decision: Outcome {decision} ({canonical_fit}/{len(rows)} map to canonical types)")
    print(f"inventory written: {out_path}")


if __name__ == "__main__":
    main()
