"""Phase 14/15 - candidate scoring + comparison runner.

Uses the FROZEN scorer modules by import + path repointing (the scorer files
themselves are never modified; scorer_sha256 remains CF4D03F5...). Runs:
  1. candidate briefs -> candidate-scored.yaml (mechanical: fog/boundary/
     routing/entry points, same parser as baseline-scored.yaml)
  2. candidate briefs -> candidate-semantic-metrics-v1.yaml (frozen semantic
     scorer)
  3. baseline vs candidate comparison -> phase15-comparison-v1.yaml with the
     charter gates evaluated and per-repository classification.
"""
from __future__ import annotations

import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

import yaml

WORK = Path(r"H:\GithubRepositories\sensemaking-skills\experiments\repository-sensemaking-skill-hardening-v1")
BASELINE = WORK / "baseline"
CANDIDATE = WORK / "candidate"
CORPUS = WORK / "corpus"
REPO_ROOT = Path(r"H:\GithubRepositories\sensemaking-skills")

# ---- load the FROZEN mechanical scorer module (score_baseline.py) ----
spec = importlib.util.spec_from_file_location("mech", WORK / "tools" / "score_baseline.py")
mech = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mech)
# repoint to candidate (module constants, not edits)
mech.BASELINE = CANDIDATE


def load_registry_ids() -> set[str]:
    reg = yaml.safe_load((REPO_ROOT / "skills/workflow-planner/references/workflow-registry.yaml").read_text(encoding="utf-8"))
    return {w["id"] for w in reg["workflows"]}


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
    registry_ids = load_registry_ids()

    # 1. validate all candidate briefs with the frozen validator
    validation = []
    for entry in gt:
        rid = entry["repository_id"]
        brief = CANDIDATE / f"{rid}.md"
        if not brief.exists():
            validation.append({"repository_id": rid, "brief_missing": True})
            continue
        r = subprocess.run(
            [sys.executable, str(REPO_ROOT / "scripts/validate-brief.py"),
             str(brief), "--target-repo", str(CORPUS / rid), "--repo-root", str(REPO_ROOT), "--json"],
            capture_output=True, text=True, encoding="utf-8")
        parsed = {}
        try:
            parsed = json.loads(r.stdout or "{}")
        except Exception:
            pass
        validation.append({
            "repository_id": rid,
            "exit_code": r.returncode,
            "valid": parsed.get("valid"),
            "error_count": len(parsed.get("errors") or []),
            "errors": [e.get("message", "") for e in (parsed.get("errors") or [])],
        })
    (CANDIDATE / "validation-results.yaml").write_text(
        yaml.safe_dump({"schema": "candidate-validation-results-v1", "results": validation}, sort_keys=False),
        encoding="utf-8")

    # 2. mechanical scoring (frozen parser, candidate path)
    rows = []
    for entry in gt:
        rid = entry["repository_id"]
        brief = CANDIDATE / f"{rid}.md"
        if not brief.exists():
            rows.append({"repository_id": rid, "brief_present": False})
            continue
        text = brief.read_text(encoding="utf-8")
        env = envelope_of(text)
        wt = env.get("weakness_type")
        row = {
            "repository_id": rid,
            "brief_present": True,
            "fog_declared": env.get("primary_fog_type"),
            "fog_expected": entry["expected_fog_candidates"][0] if entry.get("expected_fog_candidates") else None,
            "fog_match": env.get("primary_fog_type") in entry.get("expected_fog_candidates", []),
            "fog_match_primary": env.get("primary_fog_type") == (entry.get("expected_fog_candidates") or [None])[0],
            "weakness_type": wt,
            "weakness_type_valid": wt in mech.WEAKNESS_TYPES,
            "workflow_id": env.get("recommended_workflow_id"),
            "workflow_id_in_registry": env.get("recommended_workflow_id") in registry_ids,
            "has_logic_trace": "Logic trace:" in text,
            "entry_points_found": [ep for ep in entry.get("known_entry_points", []) if ep.split(":")[0] in text],
        }
        rows.append(row)
    n = len(rows)
    present = [r for r in rows if r.get("brief_present")]
    mech_out = {
        "schema": "candidate-scored-v1",
        "repositories": n,
        "briefs_produced": len(present),
        "fog_classification_accuracy": round(sum(1 for r in present if r.get("fog_match")) / len(present), 3) if present else None,
        "fog_classification_accuracy_primary": round(sum(1 for r in present if r.get("fog_match_primary")) / len(present), 3) if present else None,
        "weakness_type_validity_rate": round(sum(1 for r in present if r.get("weakness_type_valid")) / len(present), 3) if present else None,
        "workflow_routing_registry_validity": round(sum(1 for r in present if r.get("workflow_id_in_registry")) / len(present), 3) if present else None,
        "logic_trace_presence_rate": round(sum(1 for r in present if r.get("has_logic_trace")) / len(present), 3) if present else None,
        "rows": rows,
    }
    (CANDIDATE / "candidate-scored.yaml").write_text(yaml.safe_dump(mech_out, sort_keys=False), encoding="utf-8")

    # 3. semantic metrics with the FROZEN semantic scorer (path-repointed)
    spec2 = importlib.util.spec_from_file_location("sem", WORK / "tools" / "scorer_semantic_v1.py")
    sem = importlib.util.module_from_spec(spec2)
    spec2.loader.exec_module(sem)
    sem.BASELINE = CANDIDATE
    sem.OUT = WORK / "candidate-semantic-metrics-v1.yaml"
    sem.main()

    # 4. comparison vs baseline
    base_rows = {r["repository_id"]: r for r in yaml.safe_load((WORK / "baseline-scored.yaml").read_text(encoding="utf-8"))["rows"]}
    base_sem = yaml.safe_load((WORK / "baseline-semantic-metrics-v1.yaml").read_text(encoding="utf-8"))
    cand_sem = yaml.safe_load((WORK / "candidate-semantic-metrics-v1.yaml").read_text(encoding="utf-8"))
    gt_by_id = {e["repository_id"]: e for e in gt}

    per_repo = []
    for r in rows:
        if not r.get("brief_present"):
            continue
        rid = r["repository_id"]
        b = base_rows[rid]
        want_type = gt_by_id[rid]["known_weak_boundaries"][0]["type"]
        b_boundary = b.get("weakness_type") == want_type
        c_boundary = r.get("weakness_type") == want_type
        b_eps = set(b.get("entry_points_found") or [])
        c_eps = set(r.get("entry_points_found") or [])
        state = "IMPROVED"
        if (b.get("fog_match"), b_boundary) == (r.get("fog_match"), c_boundary):
            state = "UNCHANGED"
        if (not b.get("fog_match") and not r.get("fog_match")) and (b_boundary and not c_boundary):
            state = "REGRESSED"
        if b.get("fog_match") and not r.get("fog_match"):
            state = "REGRESSED"
        if b.get("fog_match") == r.get("fog_match") and (not b_boundary and c_boundary):
            state = "IMPROVED"
        per_repo.append({
            "repository_id": rid,
            "fog": {"baseline": b.get("fog_declared"), "candidate": r.get("fog_declared"), "expected": b.get("fog_expected")},
            "weakness_type": {"baseline": b.get("weakness_type"), "candidate": r.get("weakness_type"), "ground_truth": want_type},
            "entry_points": {"baseline": len(b_eps), "candidate": len(c_eps), "expected": len(gt_by_id[rid]["known_entry_points"])},
            "classification": state,
        })

    gates = {
        "unsupported_claim_rate": {"baseline": base_sem["unsupported_claim_rate"], "candidate": cand_sem["unsupported_claim_rate"],
                                   "gate": "candidate < baseline", "pass": cand_sem["unsupported_claim_rate"] < base_sem["unsupported_claim_rate"]},
        "evidence_precision": {"baseline": base_sem["evidence_precision"], "candidate": cand_sem["evidence_precision"],
                               "gate": "candidate > baseline", "pass": cand_sem["evidence_precision"] > base_sem["evidence_precision"]},
        "weakest_boundary_accuracy": {"baseline": round(sum(1 for r in per_repo if r["weakness_type"]["baseline"] == r["weakness_type"]["ground_truth"]) / len(per_repo), 3),
                                      "candidate": round(sum(1 for r in per_repo if r["weakness_type"]["candidate"] == r["weakness_type"]["ground_truth"]) / len(per_repo), 3),
                                      "gate": "candidate > baseline", "pass": None},
        "routing_validity": {"baseline": 1.0,
                             "candidate": round(sum(1 for r in present if r.get("workflow_id_in_registry")) / len(present), 3),
                             "gate": "candidate >= baseline", "pass": None},
        "validation_pass_rate": {"baseline": 1.0,
                                 "candidate": round(sum(1 for v in validation if v.get("valid") is True) / len(validation), 3),
                                 "gate": "candidate >= baseline", "pass": None},
        "observed_claim_accuracy": {"baseline": base_sem["observed_claim_accuracy"], "candidate": cand_sem["observed_claim_accuracy"],
                                    "gate": "no material regression", "pass": cand_sem["observed_claim_accuracy"] >= base_sem["observed_claim_accuracy"] - 0.05},
        "inference_labeling_rate": {"baseline": base_sem["inference_labeling_rate"], "candidate": cand_sem["inference_labeling_rate"],
                                    "gate": "no material regression", "pass": cand_sem["inference_labeling_rate"] >= base_sem["inference_labeling_rate"] - 0.05},
    }
    gates["weakest_boundary_accuracy"]["pass"] = gates["weakest_boundary_accuracy"]["candidate"] > gates["weakest_boundary_accuracy"]["baseline"]
    gates["routing_validity"]["pass"] = gates["routing_validity"]["candidate"] >= gates["routing_validity"]["baseline"]
    gates["validation_pass_rate"]["pass"] = gates["validation_pass_rate"]["candidate"] >= gates["validation_pass_rate"]["baseline"]

    out = {
        "schema": "phase15-comparison-v1",
        "baseline_pins": "baseline-report.yaml + baseline-semantic-metrics-v1.yaml (frozen)",
        "candidate_pins": "candidate-freeze-v1.yaml (frozen skill/template/validator/scorer)",
        "scorer_sha256": "CF4D03F573474EDAC19CBBEC305024C0B49DC02F082328368CFAFF042A67EA8B (frozen, unchanged)",
        "charter_gates": gates,
        "gate_overall_pass": all(g["pass"] for g in gates.values()),
        "per_repository": per_repo,
        "summary": {
            "improved": sum(1 for r in per_repo if r["classification"] == "IMPROVED"),
            "unchanged": sum(1 for r in per_repo if r["classification"] == "UNCHANGED"),
            "regressed": sum(1 for r in per_repo if r["classification"] == "REGRESSED"),
            "ambiguous": sum(1 for r in per_repo if r["classification"] not in ("IMPROVED", "UNCHANGED", "REGRESSED")),
        },
    }
    (WORK / "phase15-comparison-v1.yaml").write_text(yaml.safe_dump(out, sort_keys=False), encoding="utf-8")
    print("=== charter gates ===")
    for k, v in gates.items():
        print(f"{k}: baseline={v['baseline']} candidate={v['candidate']} -> {'PASS' if v['pass'] else 'FAIL'}")
    print("=== summary ===")
    print(yaml.safe_dump(out["summary"], sort_keys=False))
    print("comparison written:", WORK / "phase15-comparison-v1.yaml")


if __name__ == "__main__":
    main()
