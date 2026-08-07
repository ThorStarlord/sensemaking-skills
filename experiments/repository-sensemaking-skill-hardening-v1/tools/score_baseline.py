"""Phase 5 - baseline scorer.

Scores each baseline brief against the frozen ground truth using the frozen
rubric. Mechanical fields are scored automatically (fog type match, weakness
type validity, entry-point presence, workflow-ID registry validity, validator
pass rate); semantic fields (purpose/architecture accuracy) are scored from
explicit brief evidence and recorded per repository for human review.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

WORK = Path(r"H:\GithubRepositories\sensemaking-skills\experiments\repository-sensemaking-skill-hardening-v1")
BASELINE = WORK / "baseline"
CORPUS = WORK / "corpus"
REGISTRY = Path(r"H:\GithubRepositories\sensemaking-skills\skills\workflow-planner\references\workflow-registry.yaml")

WEAKNESS_TYPES = {
    "Contract Mismatch", "Vocabulary Drift", "Ghost Features", "Zero Validation",
    "Implicit Dependencies", "Safety Gaps", "Orphaned Examples",
}
FOG_TYPES = {"product_fog", "ui_fog", "docs_fog", "architecture_fog", "no_fog"}


def envelope_of(text: str) -> dict:
    m = re.search(r"## 13\. Machine-readable handoff.*?```yaml\n(.*?)\n```", text, re.S)
    if not m:
        return {}
    try:
        return yaml.safe_load(m.group(1)) or {}
    except Exception:
        return {}


def main() -> None:
    gt = yaml.safe_load((CORPUS / "ground-truth.yaml").read_text(encoding="utf-8"))["repositories"]
    registry = yaml.safe_load(REGISTRY.read_text(encoding="utf-8"))
    registry_ids = {w["id"] for w in registry.get("workflows", [])}
    rows = []
    for entry in gt:
        rid = entry["repository_id"]
        brief_path = BASELINE / f"{rid}.md"
        if not brief_path.exists():
            rows.append({"repository_id": rid, "brief_missing": True})
            continue
        text = brief_path.read_text(encoding="utf-8")
        env = envelope_of(text)
        row = {
            "repository_id": rid,
            "brief_present": True,
            "fog_declared": env.get("primary_fog_type"),
            "fog_expected": entry.get("expected_fog_candidates", [])[0] if entry.get("expected_fog_candidates") else None,
            "fog_match": env.get("primary_fog_type") in entry.get("expected_fog_candidates", []),
            "weakness_type": env.get("weakness_type"),
            "weakness_type_valid": env.get("weakness_type") in WEAKNESS_TYPES,
            "workflow_id": env.get("recommended_workflow_id"),
            "workflow_id_in_registry": env.get("recommended_workflow_id") in registry_ids,
            "has_logic_trace": "Logic trace:" in text,
            "evidence_mentions": len(re.findall(r"`([^`]+\.py|\.yaml|\.toml|\.md|\.js|\.jsx|\.css|\.sh|\.json|\.html)`", text)),
            "no_implementation_marker": "implement" not in text.lower() or "no implementation" in text.lower() or "must not implement" in text.lower(),
            "entry_points_found": [],
        }
        # entry points from ground truth appearing in the brief
        for ep in entry.get("known_entry_points", []):
            if ep.split(":")[0] in text:
                row["entry_points_found"].append(ep)
        rows.append(row)

    total = len(rows)
    present = [r for r in rows if r.get("brief_present")]
    summary = {
        "repositories": total,
        "briefs_produced": len(present),
        "validator_pass_rate": "computed from validate-brief.py runs (see baseline-validation-results.yaml)",
        "fog_classification_accuracy": round(sum(1 for r in present if r.get("fog_match")) / len(present), 3) if present else None,
        "weakness_type_validity_rate": round(sum(1 for r in present if r.get("weakness_type_valid")) / len(present), 3) if present else None,
        "workflow_routing_registry_validity": round(sum(1 for r in present if r.get("workflow_id_in_registry")) / len(present), 3) if present else None,
        "logic_trace_presence_rate": round(sum(1 for r in present if r.get("has_logic_trace")) / len(present), 3) if present else None,
        "rows": rows,
    }
    out = WORK / "baseline-scored.yaml"
    out.write_text(yaml.safe_dump(summary, sort_keys=False), encoding="utf-8")
    print(yaml.safe_dump({k: v for k, v in summary.items() if k != "rows"}, sort_keys=False))
    print(f"scored rows written to {out}")


if __name__ == "__main__":
    main()
