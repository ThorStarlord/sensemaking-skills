"""Path-scoped architecture and ontology queries over reviewed knowledge (ADR 0033).

Pure functions over the claim and relation payloads already read from an
indexed revision. They retrieve explicitly declared links only. A path that no
component covers is reported NOT ASSESSED, never as "no rules apply".
"""

from __future__ import annotations

import re
from typing import Any, Iterable, Mapping

from .knowledge import is_path_scope

OPERATIONS = frozenset({"rules-for", "term", "orientation-summary"})
NOT_ASSESSED_NOTE = (
    "NOT ASSESSED: no declared component covers this path. Absence here is not evidence "
    "that no rule applies; inspect the code and governing documents before editing."
)


def glob_to_regex(glob: str) -> re.Pattern[str]:
    """Repository-relative glob: `**` crosses directories, `*` and `?` do not."""
    out: list[str] = []
    index = 0
    while index < len(glob):
        char = glob[index]
        if glob.startswith("**/", index):
            out.append("(?:.*/)?")
            index += 3
            continue
        if glob.startswith("**", index):
            out.append(".*")
            index += 2
            continue
        if char == "*":
            out.append("[^/]*")
        elif char == "?":
            out.append("[^/]")
        else:
            out.append(re.escape(char))
        index += 1
    return re.compile("^" + "".join(out) + "$")


def _scope_matches(scope: str, path: str) -> bool:
    if is_path_scope(scope):
        return bool(glob_to_regex(scope).match(path))
    return False


def _components_for_path(claims: Mapping[str, dict], path: str) -> list[str]:
    """A citation is provenance, not ownership."""
    return sorted(cid for cid, claim in claims.items()
                  if claim["kind"] == "component"
                  and path in claim.get("attributes", {}).get("owned_paths", []))


def _rule_applies(rule_id: str, rule: Mapping[str, Any], path: str,
                  targets: set[str], relations: Iterable[dict]) -> list[str]:
    reasons = [f"path scope {scope}" for scope in rule["attributes"].get("applies_to", [])
               if _scope_matches(scope, path)]
    reasons.extend(f"declared graph target {rel['object']}" for rel in relations
                   if rel["predicate"] == "applies_to" and rel["subject"] == rule_id
                   and rel["object"] in targets)
    return sorted(set(reasons))


def rules_for(claims: Mapping[str, dict], relations: Iterable[dict], *, path: str, limit: int) -> dict:
    """Retrieve declared architecture guidance while preserving its evidence limits."""
    edges = list(relations)
    owners = _components_for_path(claims, path)
    owner_set = set(owners)
    layers = sorted({r["object"] for r in edges if r["predicate"] == "belongs_to"
                     and r["subject"] in owner_set and claims.get(r["object"], {}).get("kind") == "layer"})
    contexts = sorted({r["object"] for r in edges if r["predicate"] == "belongs_to"
                       and r["subject"] in owner_set and claims.get(r["object"], {}).get("kind") == "bounded_context"})
    tests = sorted({r["object"] for r in edges if r["predicate"] == "tested_by" and r["subject"] in owner_set})
    targets = owner_set | set(layers) | set(contexts)
    applicable = []
    for cid, claim in sorted(claims.items()):
        if claim["kind"] != "architecture_rule":
            continue
        reasons = _rule_applies(cid, claim, path, targets, edges)
        if reasons:
            applicable.append({
                "claim_id": cid, "rule_type": claim["attributes"].get("rule_type"),
                "severity": claim["attributes"].get("severity"),
                "epistemic_status": claim.get("epistemic_status"),
                "authority_kind": claim.get("authority_kind"),
                "authority_ref": claim.get("authority_ref"),
                "evidence_refs": claim.get("evidence_refs", []),
                "matched_by": reasons, "statement": claim["statement"],
            })
    return {
        "path": path, "coverage_status": "COVERED" if owners else "NOT_ASSESSED",
        "ownership_ambiguous": len(owners) > 1,
        "owning_components": owners[:limit],
        "layers": layers[:limit], "bounded_contexts": contexts[:limit],
        "applicable_rules": applicable[:limit], "tests": tests[:limit],
        "truncated": any(len(a) > limit for a in (owners, layers, contexts, applicable, tests)),
        "note": None if owners else NOT_ASSESSED_NOTE,
    }


def term(claims: Mapping[str, dict], relations: Iterable[dict], *, name: str, limit: int) -> dict:
    """Definition, synonyms and confusable neighbours of a domain term."""
    needle = name.strip().lower()
    matches = [
        cid for cid, claim in sorted(claims.items())
        if claim["kind"] in {"domain_concept", "lifecycle_state", "invariant", "constraint"}
        and (cid.split(":", 1)[-1].lower() == needle or needle in claim["statement"].lower())
    ]
    rel_list = list(relations)
    synonyms = sorted({rel["subject"] if rel["object"] in matches else rel["object"]
                       for rel in rel_list if rel["predicate"] == "synonym_of"
                       and (rel["subject"] in matches or rel["object"] in matches)})
    distinct = sorted({rel["subject"] if rel["object"] in matches else rel["object"]
                       for rel in rel_list if rel["predicate"] == "distinct_from"
                       and (rel["subject"] in matches or rel["object"] in matches)})
    return {
        "term": name,
        "matched_claims": matches[:limit],
        "synonyms": synonyms[:limit],
        "distinct_from": distinct[:limit],
        "coverage_status": "COVERED" if matches else "NOT_ASSESSED",
        "note": None if matches else "NOT ASSESSED: no reviewed definition matches this term.",
        "truncated": len(matches) > limit,
    }


def orientation_summary(claims: Mapping[str, dict], relations: Iterable[dict], *, max_lines: int = 200) -> dict:
    """A bounded map of layers, components, contexts and rules, with what was cut."""
    rel_list = list(relations)
    by_kind: dict[str, list[str]] = {}
    for cid, claim in sorted(claims.items()):
        by_kind.setdefault(claim["kind"], []).append(cid)
    lines: list[str] = []
    for kind in ("layer", "bounded_context", "component", "architecture_rule", "contract", "external_system"):
        for cid in by_kind.get(kind, []):
            lines.append(f"{kind}: {cid}")
    for rel in rel_list:
        if rel["predicate"] in {"belongs_to", "applies_to", "flows_to", "exposes"}:
            lines.append(f"{rel['subject']} {rel['predicate']} {rel['object']}")
    cut = max(0, len(lines) - max_lines)
    return {
        "counts": {kind: len(ids) for kind, ids in sorted(by_kind.items())},
        "lines": lines[:max_lines],
        "lines_omitted": cut,
        "coverage_note": (
            "Only modeled constructs appear. A component absent here is NOT ASSESSED, not absent."
        ),
    }


# -- warning-only rule checker (Phase 3) -----------------------------------------

def _module_file(module: str, tracked: set[str]) -> str | None:
    """Map a dotted module under src/ or scripts/ to a tracked Python file, if any."""
    parts = module.split(".")
    for root in ("src/", ""):
        for end in (len(parts), len(parts) - 1):
            if end <= 0:
                continue
            candidate = root + "/".join(parts[:end]) + ".py"
            if candidate in tracked:
                return candidate
            package = root + "/".join(parts[:end]) + "/__init__.py"
            if package in tracked:
                return package
    return None


def _python_imports(source: str, module_of_file: str) -> list[str]:
    import ast

    try:
        tree = ast.parse(source)
    except SyntaxError:
        return []
    found: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            found.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
            found.append(node.module)
    return found


def check_rule_findings(
    claims: Mapping[str, dict], *, read_source, tracked: set[str], limit: int = 200,
) -> dict:
    """Report possible violations of dependency_direction rules. Warning-only.

    Import syntax is not architectural proof: a finding is evidence for review.
    Only Python sources are inspected; other scopes are NOT ASSESSED.
    """
    findings: list[dict] = []
    not_assessed: list[str] = []
    for rule_id, rule in sorted(claims.items()):
        if rule["kind"] != "architecture_rule" or rule["attributes"].get("rule_type") != "dependency_direction":
            continue
        forbidden = list(rule["attributes"].get("forbidden_targets") or [])
        forbidden_files: set[str] = set()
        for target in forbidden:
            owner = claims.get(target)
            if owner is None:
                not_assessed.append(f"{rule_id}: target {target} is not a claim")
                continue
            for ref in owner.get("evidence_refs", []):
                if not ref.startswith("file:"):
                    continue
                path = ref[5:]
                # A package's __init__.py claims its whole directory.
                forbidden_files.add(path.rsplit("/", 1)[0] + "/" if path.endswith("/__init__.py") else path)
        scope = rule["attributes"].get("applies_to", [])
        in_scope = sorted(p for p in tracked if p.endswith(".py") and any(
            glob_to_regex(s).match(p) for s in scope if is_path_scope(s)))
        if not in_scope:
            not_assessed.append(f"{rule_id}: no tracked Python file matches its scope")
        for path in in_scope:
            for module in _python_imports(read_source(path), path):
                target_file = _module_file(module, tracked)
                if target_file is None:
                    continue
                if any(target_file == f or (f.endswith("/") and target_file.startswith(f)) for f in forbidden_files):
                    findings.append({"rule_id": rule_id, "severity": rule["attributes"].get("severity"),
                                     "file": path, "imports": module, "resolves_to": target_file,
                                     "note": "Possible violation; import syntax only, for review."})
    return {
        "warning_only": True,
        "findings": findings[:limit],
        "findings_total": len(findings),
        "not_assessed": not_assessed,
        "limits": [
            "Python import syntax only; runtime coupling and architectural significance are NOT ASSESSED.",
            "Findings are evidence for review, not proof of a defect; this check never fails CI in v1.",
        ],
    }
