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
        "match_quality": "exact_id" if any(cid.split(":", 1)[-1].lower() == needle for cid in matches) else "statement_substring",
        "multiple_matches": len(matches) > 1,
        "matched_claims": matches[:limit],
        "synonyms": synonyms[:limit],
        "distinct_from": distinct[:limit],
        "coverage_status": "COVERED" if matches else "NOT_ASSESSED",
        "note": None if matches else "NOT ASSESSED: no reviewed definition matches this term.",
        "truncated": any(len(items) > limit for items in (matches, synonyms, distinct)),
    }


def orientation_summary(claims: Mapping[str, dict], relations: Iterable[dict], *, max_lines: int = 200) -> dict:
    """A bounded map of layers, components, contexts and rules, with what was cut."""
    rel_list = list(relations)
    by_kind: dict[str, list[str]] = {}
    for cid, claim in sorted(claims.items()):
        by_kind.setdefault(claim["kind"], []).append(cid)
    lines: list[str] = []
    for kind in ("layer", "bounded_context", "component", "architecture_rule", "contract"):
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


def _module_namespace(path: str) -> list[str]:
    """Resolve source-relative modules for Python's relative import syntax."""
    local = path.removeprefix("src/").removesuffix(".py").split("/")
    return local[:-1] if local[-1] != "__init__" else local[:-1]


def _python_imports_with_issues(source: str, module_of_file: str) -> tuple[list[str], list[str]]:
    """Return statically resolvable imports and parser/dynamic-import limitations."""
    import ast

    try:
        tree = ast.parse(source)
    except SyntaxError as exc:
        return [], [f"Python syntax error at line {exc.lineno}; imports not assessed"]
    found: list[str] = []
    issues: list[str] = []
    namespace = _module_namespace(module_of_file)
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            found.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            if node.level:
                up = node.level - 1
                if up >= len(namespace):
                    issues.append(f"unresolvable relative import at line {node.lineno}")
                    continue
                base = namespace[:len(namespace) - up]
                if node.module:
                    base += node.module.split(".")
                module = ".".join(base)
            else:
                module = node.module or ""
            if module:
                found.append(module)
                found.extend(module + "." + name.name for name in node.names if name.name != "*")
            else:
                issues.append(f"unresolvable import-from at line {node.lineno}")
        elif isinstance(node, ast.Call) and isinstance(node.func, (ast.Name, ast.Attribute)):
            is_import = (
                isinstance(node.func, ast.Name) and node.func.id == "__import__"
            ) or (
                isinstance(node.func, ast.Attribute) and node.func.attr == "import_module"
                and isinstance(node.func.value, ast.Name) and node.func.value.id == "importlib"
            )
            if is_import:
                if node.args and isinstance(node.args[0], ast.Constant) and isinstance(node.args[0].value, str):
                    found.append(node.args[0].value)
                else:
                    issues.append(f"dynamic import target unknown at line {node.lineno}")
    return sorted(set(found)), issues


def _python_imports(source: str, module_of_file: str) -> list[str]:
    """Compatibility reader: import syntax only, without assessment metadata."""
    return _python_imports_with_issues(source, module_of_file)[0]


def _component_files(claim: Mapping[str, Any]) -> set[str]:
    """Explicit owned paths plus source-supported package roots for checker targeting."""
    paths = set(claim.get("attributes", {}).get("owned_paths", []))
    paths.update(ref[5:] for ref in claim.get("evidence_refs", []) if ref.startswith("file:"))
    return {p.rsplit("/", 1)[0] + "/" if p.endswith("/__init__.py") else p for p in paths}


def _matches_file(target: str, scopes: Iterable[str]) -> bool:
    return any(target == p or (p.endswith("/") and target.startswith(p)) for p in scopes)


def _rule_scoped_files(rule_id: str, rule: Mapping[str, Any], claims: Mapping[str, dict],
                       relations: Iterable[dict], tracked: set[str]) -> set[str]:
    scopes = rule["attributes"].get("applies_to", [])
    files = {p for p in tracked if any(_scope_matches(scope, p) for scope in scopes)}
    targets = {r["object"] for r in relations if r["predicate"] == "applies_to" and r["subject"] == rule_id}
    for target in targets:
        if claims.get(target, {}).get("kind") == "component":
            for p in claims[target].get("attributes", {}).get("owned_paths", []):
                if p in tracked:
                    files.add(p)
        elif claims.get(target, {}).get("kind") in {"layer", "bounded_context"}:
            members = {r["subject"] for r in relations if r["predicate"] == "belongs_to" and r["object"] == target}
            for cid in members:
                for p in claims.get(cid, {}).get("attributes", {}).get("owned_paths", []):
                    if p in tracked:
                        files.add(p)
    return files


def check_rule_findings(
    claims: Mapping[str, dict], *, read_source, tracked: set[str], limit: int = 200,
    relations: Iterable[dict] = (),
) -> dict:
    """Warning-only Python dependency checker with explicit per-rule assessment.

    Unsupported rules, unresolved imports, non-Python scopes and parser errors
    never masquerade as zero-violation checks.
    """
    findings: list[dict] = []
    not_assessed: list[str] = []
    assessments: list[dict] = []
    edges = list(relations)
    manifest_modules: set[str] | None = None
    if "release-v1.0.yaml" in tracked:
        try:
            import yaml

            release = yaml.safe_load(read_source("release-v1.0.yaml")) or {}
            manifest_modules = set(release.get("package_boundary", {}).get("source_only_modules", []))
        except (ValueError, KeyError, TypeError, yaml.YAMLError) as exc:
            not_assessed.append(f"release manifest could not be read: {exc}")
    for rule_id, rule in sorted(claims.items()):
        if rule["kind"] != "architecture_rule":
            continue
        attrs = rule.get("attributes", {})
        reasons: list[str] = []
        in_scope = _rule_scoped_files(rule_id, rule, claims, edges, tracked)
        python_files = sorted(p for p in in_scope if p.endswith(".py"))
        if not in_scope:
            reasons.append("no tracked files match the declared scope")
        if len(python_files) != len(in_scope):
            reasons.append("non-Python files not evaluated")
        if attrs.get("rule_type") != "dependency_direction":
            reasons.append(f"rule type {attrs.get('rule_type')} has no executable checker")
            status = "NOT_ASSESSED"
            assessments.append({"rule_id": rule_id, "assessment_status": status, "files_examined": 0,
                                "scope_files_total": len(in_scope), "not_assessed_reasons": reasons})
            not_assessed.extend(f"{rule_id}: {reason}" for reason in reasons)
            continue
        forbidden = list(attrs.get("forbidden_targets") or [])
        allowed = list(attrs.get("allowed_targets") or [])
        forbidden_files: set[str] = set()
        allowed_files: set[str] = set()
        for target, dest in [(x, forbidden_files) for x in forbidden] + [(x, allowed_files) for x in allowed]:
            claim = claims.get(target)
            if claim is None:
                reasons.append(f"target {target} is not a claim")
                continue
            dest.update(_component_files(claim))
        if manifest_modules is not None and forbidden:
            recorded_packages = {p for p in forbidden_files if p.endswith("/")}
            expected_packages = {"src/" + module.replace(".", "/") + "/" for module in manifest_modules}
            if expected_packages and not expected_packages.issubset(recorded_packages):
                reasons.append("forbidden targets do not cover every source-only package in release manifest")
        if not python_files:
            reasons.append("no tracked Python file matches its scope")
        examined = 0
        for path in python_files:
            imported, parse_issues = _python_imports_with_issues(read_source(path), path)
            if parse_issues:
                reasons.extend(f"{path}: {issue}" for issue in parse_issues)
            if any("syntax error" in issue for issue in parse_issues):
                continue
            examined += 1
            for module in imported:
                target_file = _module_file(module, tracked)
                if target_file is None:
                    continue
                if _matches_file(target_file, forbidden_files):
                    findings.append({"rule_id": rule_id, "severity": attrs.get("severity"),
                                     "file": path, "imports": module, "resolves_to": target_file,
                                     "note": "Possible violation; import syntax only, for review."})
                if allowed and not _matches_file(target_file, allowed_files):
                    # Only judge modules that have reviewed owners; unmodeled
                    # source modules cannot prove an allowlist breach.
                    owners = [cid for cid, claim in claims.items() if claim["kind"] == "component"
                              and _matches_file(target_file, _component_files(claim))]
                    if owners:
                        findings.append({"rule_id": rule_id, "severity": attrs.get("severity"),
                                         "file": path, "imports": module, "resolves_to": target_file,
                                         "note": "Import of modeled component outside allowed_targets; for review."})
                    else:
                        reasons.append(f"{path}: imported {module} has no modeled target for allowlist")
        status = "NOT_ASSESSED" if examined == 0 else ("PARTIALLY_ASSESSED" if reasons else "ASSESSED")
        assessments.append({"rule_id": rule_id, "assessment_status": status,
                            "files_examined": examined, "scope_files_total": len(in_scope),
                            "not_assessed_reasons": sorted(set(reasons))})
        not_assessed.extend(f"{rule_id}: {reason}" for reason in sorted(set(reasons)))
    unique_findings: dict[tuple[str, str, str, str], dict] = {}
    for item in findings:
        key = (item["rule_id"], item["file"], item["resolves_to"], item["note"])
        unique_findings.setdefault(key, item)
    findings = list(unique_findings.values())
    return {
        "warning_only": True, "findings": findings[:limit], "findings_total": len(findings),
        "not_assessed": not_assessed, "rule_assessments": assessments,
        "rules_total": len(assessments),
        "truncated": len(findings) > limit,
        "limits": [
            "Python AST imports and literal import calls only; runtime coupling is NOT ASSESSED.",
            "Unmodeled code, unsupported rule types, and unresolved import syntax cannot establish compliance.",
            "Findings are evidence for review, not proof of a defect; this check never fails CI in v1.",
        ],
    }
