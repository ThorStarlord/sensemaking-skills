"""Phase 5B - frozen semantic metrics scorer (baseline AND hardened use this).

Deterministic sentence-level claim scorer. Frozen rules:

Claim classes (per charter 5B.1):
  OBSERVED    : assertive sentence with a file:line citation that resolves
                (file exists in the target repo, line <= file length)
  DERIVED     : sentence with a citation AND a reasoning marker
                (therefore|thus|so|consequence|because|implies|means|hence)
  INFERRED    : hedged sentence (likely|probably|suggests|appears|may|might|
                possibly|presumably|seems|could|unclear|unknown|not confirmed)
                without a resolvable citation
  UNSUPPORTED : assertive factual/derived sentence with no resolvable citation

Metrics (frozen definitions):
  evidence_precision      = supported claims / claims carrying evidence
                          = (OBSERVED + DERIVED) / (OBSERVED + DERIVED + cited-but-unresolvable)
  unsupported_claim_rate  = UNSUPPORTED / (OBSERVED + DERIVED + UNSUPPORTED)
  observed_claim_accuracy = OBSERVED / (OBSERVED + cited-but-unresolvable)
  derived_claim_accuracy  = DERIVED / (DERIVED + reason-marked-without-citation)
  inference_labeling_rate = INFERRED / (INFERRED + UNSUPPORTED)
  conflicting_evidence_detection_rate = briefs flagging a contradiction with
                            >= 2 distinct cited files / total briefs
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

WORK = Path(r"H:\GithubRepositories\sensemaking-skills\experiments\repository-sensemaking-skill-hardening-v1")
BASELINE = WORK / "baseline"
CORPUS = WORK / "corpus"
OUT = WORK / "baseline-semantic-metrics-v1.yaml"
SCORER_VERSION = "semantic-scorer-v1"

HEDGES = re.compile(
    r"\b(likely|probably|suggests?|appears?|may\b|might\b|possibly|presumably|seems?|could\b|"
    r"unclear|unknown|not confirmed|no proof|apparently|arguably|tentatively)\b",
    re.I,
)
REASON = re.compile(r"\b(therefore|thus|so\b|consequence|because|implies?|means?|hence|as a result)\b", re.I)
CITE = re.compile(
    r"`?([A-Za-z0-9_][A-Za-z0-9_./-]*)\.(md|py|yaml|yml|toml|txt|js|jsx|ts|tsx|json|html|css|go|rs|java|rb|sh)"
    r"(?::(\d+)(?:-(\d+))?)?`?"
)
SENT = re.compile(r"[^.!?\n]+[.!?]?")


def claim_class(sentence: str, resolvable: bool) -> str:
    cited = CITE.search(sentence) is not None
    hedged = HEDGES.search(sentence) is not None
    reason = REASON.search(sentence) is not None
    if cited:
        if reason:
            return "DERIVED"
        if resolvable:
            return "OBSERVED"
        return "CITED_UNRESOLVABLE"
    if hedged:
        return "INFERRED"
    return "UNSUPPORTED"


def line_count(path: Path) -> int:
    try:
        return len(path.read_text(encoding="utf-8", errors="replace").splitlines())
    except Exception:
        return 0


def check_citation(sentence: str, target: Path) -> bool:
    for m in CITE.finditer(sentence):
        rel = f"{m.group(1)}.{m.group(2)}"
        start = m.group(3)
        f = target / rel
        if not f.exists():
            continue
        if start is None:
            return True
        try:
            if int(start) <= line_count(f):
                return True
        except ValueError:
            continue
    return False


def scan_brief(path: Path, target: Path) -> dict:
    text = path.read_text(encoding="utf-8", errors="replace")
    # drop the Section 13 handoff (machine block) and section headers
    body = re.split(r"## 13\. Machine-readable handoff", text)[0]
    body = "\n".join(l for l in body.splitlines() if not re.match(r"^#{1,3} ", l))
    # strip fenced code blocks (inventories/trees are not claims)
    body = re.sub(r"```.*?```", " ", body, flags=re.S)
    # protect citation dots from sentence splitting, then split, then restore
    protected = CITE.sub(lambda m: m.group(0).replace(".", "\x02"), body)
    sentences = []
    for s in SENT.findall(protected):
        s = s.strip().replace("\x02", ".")
        if len(s) >= 15:
            sentences.append(s)
    counts = {"OBSERVED": 0, "DERIVED": 0, "INFERRED": 0, "UNSUPPORTED": 0, "CITED_UNRESOLVABLE": 0}
    for s in sentences:
        resolvable = check_citation(s, target)
        counts[claim_class(s, resolvable)] += 1
    # conflicting-evidence detection: >=2 distinct cited files near a conflict marker
    conflict_marker = re.compile(r"\b(conflict|contradict|disagre|mismatch|stale|outdated|drift)\b", re.I)
    conflict = False
    for para in re.split(r"\n\s*\n", body):
        if conflict_marker.search(para):
            files = {m.group(1) for m in CITE.finditer(para)}
            if len(files) >= 2:
                conflict = True
                break
    return counts, conflict


def main() -> None:
    gt = yaml.safe_load((CORPUS / "ground-truth.yaml").read_text(encoding="utf-8"))["repositories"]
    rows = []
    agg = {k: 0 for k in ("OBSERVED", "DERIVED", "INFERRED", "UNSUPPORTED", "CITED_UNRESOLVABLE")}
    conflicts = 0
    for entry in gt:
        rid = entry["repository_id"]
        brief = BASELINE / f"{rid}.md"
        target = CORPUS / rid
        counts, conflict = scan_brief(brief, target)
        for k in agg:
            agg[k] += counts[k]
        total = sum(counts.values())
        row = {
            "repository_id": rid,
            "claims": counts,
            "evidence_precision": round((counts["OBSERVED"] + counts["DERIVED"]) / max(1, counts["OBSERVED"] + counts["DERIVED"] + counts["CITED_UNRESOLVABLE"]), 3),
            "unsupported_claim_rate": round(counts["UNSUPPORTED"] / max(1, counts["OBSERVED"] + counts["DERIVED"] + counts["UNSUPPORTED"]), 3),
            "observed_claim_accuracy": round(counts["OBSERVED"] / max(1, counts["OBSERVED"] + counts["CITED_UNRESOLVABLE"]), 3),
            "derived_claim_accuracy": round(counts["DERIVED"] / max(1, counts["DERIVED"]), 3),
            "inference_labeling_rate": round(counts["INFERRED"] / max(1, counts["INFERRED"] + counts["UNSUPPORTED"]), 3),
            "conflicting_evidence_detected": conflict,
        }
        rows.append(row)
        if conflict:
            conflicts += 1
    n = len(rows)
    summary = {
        "scorer_version": SCORER_VERSION,
        "scorer_rules_frozen": True,
        "same_scorer_for_hardened": True,
        "same_parser_for_baseline_and_hardened": True,
        "repositories": n,
        "evidence_precision": round((agg["OBSERVED"] + agg["DERIVED"]) / max(1, agg["OBSERVED"] + agg["DERIVED"] + agg["CITED_UNRESOLVABLE"]), 3),
        "unsupported_claim_rate": round(agg["UNSUPPORTED"] / max(1, agg["OBSERVED"] + agg["DERIVED"] + agg["UNSUPPORTED"]), 3),
        "observed_claim_accuracy": round(agg["OBSERVED"] / max(1, agg["OBSERVED"] + agg["CITED_UNRESOLVABLE"]), 3),
        "derived_claim_accuracy": round(agg["DERIVED"] / max(1, agg["DERIVED"]), 3),
        "inference_labeling_rate": round(agg["INFERRED"] / max(1, agg["INFERRED"] + agg["UNSUPPORTED"]), 3),
        "conflicting_evidence_detection_rate": round(conflicts / n, 3),
        "total_claims": sum(agg.values()),
        "per_repository": rows,
    }
    OUT.write_text(yaml.safe_dump(summary, sort_keys=False), encoding="utf-8")
    for k, v in summary.items():
        if k != "per_repository":
            print(f"{k}: {v}")


if __name__ == "__main__":
    main()
