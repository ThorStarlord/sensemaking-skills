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


def _file_refs(claim: Mapping[str, Any]) -> list[str]:
    return [ref[len("file:"):] for ref in claim.get("evidence_refs", []) if ref.startswith("file:")]


def _components_for_path(claims: Mapping[str, dict], path: str) -> list[str]:
    owners = []
    for claim_id, claim in claims.items():
        if claim["kind"] != "component":
            continue
        for ref in _file_refs(claim):
            if ref == path or (ref.endswith("/") and path.startswith(ref)) or _scope_matches(ref, path):
                owners.append(claim_id)
                break
    return sorted(owners)


def _rule_applies(rule: Mapping[str, Any], path: str, owners: set[str]) -> list[str]:
    reasons = []
    for scope in rule["attributes"].get("applies_to", []):
        if _scope_matches(scope, path):
            reasons.append(f"path scope {scope}")
        elif not is_path_scope(scope) and scope in owners:
            reasons.append(f"component {scope}")
    return reasons


def rules_for(
    claims: Mapping[str, dict], relations: Iterable[dict], *, path: str, limit: int,
) -> dict:
    """Which declared component, layer, rules and tests apply to an edit at `path`."""
    rel_list = list(relations)
    owners = _components_for_path(claims, path)
    owner_set = set(owners)
    applicable = []
    for claim_id, claim in sorted(claims.items()):
        if claim["kind"] != "architecture_rule":
            continue
        reasons = _rule_applies(claim, path, owner_set)
        if reasons:
            applicable.append({"claim_id": claim_id, "rule_type": claim["attributes"].get("rule_type"),
                               "severity": claim["attributes"].get("severity"), "matched_by": reasons,
                               "statement": claim["statement"]})
    layers = sorted({rel["object"] for rel in rel_list
                     if rel["predicate"] == "belongs_to" and rel["subject"] in owner_set
                     and claims.get(rel["object"], {}).get("kind") == "layer"})
    contexts = sorted({rel["object"] for rel in rel_list
                       if rel["predicate"] == "belongs_to" and rel["subject"] in owner_set
                       and claims.get(rel["object"], {}).get("kind") == "bounded_context"})
    tests = sorted({rel["object"] for rel in rel_list
                    if rel["predicate"] == "tested_by" and rel["subject"] in owner_set})
    status = "COVERED" if owners else "NOT_ASSESSED"
    return {
        "path": path,
        "coverage_status": status,
        "owning_components": owners[:limit],
        "layers": layers[:limit],
        "bounded_contexts": contexts[:limit],
        "applicable_rules": applicable[:limit],
        "tests": tests[:limit],
        "truncated": len(applicable) > limit or len(owners) > limit or len(tests) > limit,
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
            forbidden_files.update(ref[5:] for ref in owner.get("evidence_refs", []) if ref.startswith("file:"))
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
                if any(target_file == f or target_file.startswith(f.rstrip("/") + "/") for f in forbidden_files):
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
