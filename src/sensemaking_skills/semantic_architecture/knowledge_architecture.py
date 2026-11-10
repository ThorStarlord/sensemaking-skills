"""Path-scoped architecture and ontology queries over reviewed knowledge (ADR 0033).

Pure functions over the claim and relation payloads already read from an
indexed revision. They retrieve explicitly declared links only. A path that no
component covers is reported NOT ASSESSED, never as "no rules apply".
"""

from __future__ import annotations

import re
from typing import Any, Iterable, Mapping

from .knowledge import _valid_repo_path, is_path_scope

OPERATIONS = frozenset({"rules-for", "term", "orientation-summary", "context-for"})
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


HISTORY_KINDS = frozenset({"incident", "lesson", "observation"})
INACTIVE_STATUSES = frozenset({"superseded", "contested", "invalidated"})
CONTEXT_NOTE = (
    "Explicit links only: an item appears because a reviewed relation or a declared path "
    "scope names it, never because its name or a neighbouring file looks similar. Relevance "
    "does not establish semantic truth or action authority. A linked alternative "
    "is not automatically endorsed or rejected."
)
CONSTRAINT_KINDS = frozenset({"invariant", "constraint"})
_EMPTY_CATEGORY_NOTES = {
    "contracts": "No explicitly linked contract is recorded for the owning components. "
                 "Absence here is not evidence that no contract applies.",
    "constraints": "No explicitly linked invariant or constraint is recorded for the owners, "
                   "rules or linked decisions. Constraints may exist outside the indexed "
                   "revision; this is not a clearance.",
    "decisions": "No explicitly linked decision is recorded for the owners or rules. "
                 "Decisions may exist outside the indexed revision.",
    "alternatives": "No alternative is explicitly linked to a decision in this "
                    "bounded task context; other viable options may exist.",
    "history": "No explicitly linked incident, lesson or observation is recorded. "
               "Prior occurrences may exist outside the indexed revision.",
    "verification_refs": "No linked verification record is recorded. Tests may exist in the "
                         "repository and were not assessed here.",
}


def is_repository_file_path(value: str) -> bool:
    """Validate path syntax only, without checking whether a file exists."""
    return _valid_repo_path(value, glob=False) and not value.endswith("/")


def _context_item(cid: str, claim: Mapping[str, Any], matched_by: set[str]) -> dict:
    return {
        "claim_id": cid, "kind": claim["kind"], "statement": claim["statement"],
        "epistemic_status": claim.get("epistemic_status"),
        "authority_kind": claim.get("authority_kind"),
        "authority_ref": claim.get("authority_ref"),
        "evidence_refs": claim.get("evidence_refs", []),
        "matched_by": sorted(matched_by),
    }


def _test_evidence_verifications(claims: Mapping[str, dict], path: str) -> dict[str, list[str]]:
    """Verification records that explicitly name this file as authority or evidence.

    A reviewed verification claim whose ``authority_ref`` is the file, or whose
    ``evidence_refs`` cite it as ``file:<path>``, is verification context for it.
    This is provenance, never ownership: no component is created, and claim kinds
    other than verification that merely cite the file do not qualify.
    """
    file_ref = f"file:{path}"
    found: dict[str, list[str]] = {}
    for cid, claim in claims.items():
        if claim.get("kind") != "verification":
            continue
        reasons = []
        if claim.get("authority_ref") == path:
            reasons.append("authority_ref: this file is the authority of this verification claim")
        if file_ref in claim.get("evidence_refs", []):
            reasons.append("evidence_ref: this file is cited in this verification claim's evidence")
        if reasons:
            found[cid] = reasons
    return found


def context_for(
    claims: Mapping[str, dict], relations: Iterable[dict], *, path: str, limit: int,
) -> tuple[dict, list[str], list[str]]:
    """Task context for one repository file, each item tied to the explicit link behind it.

    Ownership and path-scoped rules come from rules_for. Contracts, constraints,
    decisions, history, verification and recorded alternatives enter only through
    explicit relations from an owning component, an applicable rule, or a linked
    decision. Constraints are invariant or constraint claims reached by
    constrained_by. Bounded second hops recover decision -> derived_from ->
    observation, directly linked decision -> references/contradicts -> alternative
    records, and linked decision -> constrained_by -> constraint. Returns the context
    and the claim and relation IDs grounding the visible, bounded result, both
    in deterministic order. Category totals may include omitted records.

    A file that no component owns can also reach verification records that name it
    as authority or evidence, and the components those records verify. Both are
    relevance, never ownership, and are reported as such.
    """
    edges = list(relations)
    base = rules_for(claims, edges, path=path, limit=len(claims) + len(edges) + 1)
    owners = set(base["owning_components"])
    rule_ids = {rule["claim_id"] for rule in base["applicable_rules"]}
    layer_ids = set(base["layers"]) | set(base["bounded_contexts"])
    # Verification relevance applies only to a file no component owns, so owned paths
    # keep their existing response. A component verified by such a record anchors its
    # decisions, constraints and history; it never becomes an owner of contracts or rules.
    test_verifications = {} if owners else _test_evidence_verifications(claims, path)
    base_anchors = owners | rule_ids
    buckets: dict[str, dict[str, set[str]]] = {
        "contracts": {}, "constraints": {}, "decisions": {}, "alternatives": {},
        "history": {}, "verification_refs": {},
    }
    # Retain link provenance by category item. A per-category limit may omit an
    # item, so its edges must not displace evidence for items actually returned.
    link_relation_ids: dict[str, dict[str, set[str]]] = {name: {} for name in buckets}
    structural_relation_ids: set[str] = set()

    def link(bucket: str, target: str, rel: Mapping[str, Any], via: str = "") -> None:
        text = f"{via}relation {rel['subject']} {rel['predicate']} {rel['object']}"
        buckets[bucket].setdefault(target, set()).add(text)
        link_relation_ids[bucket].setdefault(target, set()).add(rel["id"])

    # The verification bucket has two sources: file matches, and tested_by links from
    # owners and applicable rules. Only owners and rules expand to their verification
    # records; a verified component adds its decisions, constraints and history, not
    # every test of it. Built before the verified-component derivation below, because
    # that derivation must read the bucket's displayed selection.
    for cid, reasons in test_verifications.items():
        buckets["verification_refs"][cid] = set(reasons)
    for rel in edges:
        if (rel["predicate"] == "tested_by" and rel["subject"] in base_anchors
                and claims.get(rel["object"], {}).get("kind") == "verification"):
            link("verification_refs", rel["object"], rel)
    # A verified component is returned only with a supporting verification record that
    # this response displays: the first `limit` of the whole verification bucket in
    # deterministic order. A rule-added record can sort before a file match and displace
    # it, so visibility comes from that displayed selection, not from file matches alone.
    # Components supported only by hidden records are counted as omitted, never returned.
    displayed_verifications = set(sorted(buckets["verification_refs"])[:limit])
    verified_all: set[str] = set()
    supported_text: dict[str, set[str]] = {}
    supported_rel_ids: dict[str, set[str]] = {}
    for rel in edges:
        if (rel["predicate"] == "tested_by" and rel["object"] in test_verifications
                and claims.get(rel["subject"], {}).get("kind") == "component"):
            verified_all.add(rel["subject"])
            if rel["object"] in displayed_verifications:
                supported_text.setdefault(rel["subject"], set()).add(
                    f"relation {rel['id']}: {rel['subject']} tested_by {rel['object']} "
                    "(this component is verified by the file's verification record; not ownership)")
                supported_rel_ids.setdefault(rel["subject"], set()).add(rel["id"])
    verified_components = sorted(supported_text)[:limit]
    verified_text = {cid: supported_text[cid] for cid in verified_components}
    verified_rel_ids = {cid: supported_rel_ids[cid] for cid in verified_components}
    anchors = base_anchors | set(verified_components)

    for rel in edges:
        s, p, o = rel["subject"], rel["predicate"], rel["object"]
        s_kind, o_kind = claims.get(s, {}).get("kind"), claims.get(o, {}).get("kind")
        if p == "exposes" and s in owners and o_kind == "contract":
            link("contracts", o, rel)
        elif p == "flows_to" and (s in owners or o in owners):
            carried = rel.get("attributes", {}).get("carries")
            if claims.get(carried, {}).get("kind") == "contract":
                link("contracts", carried, rel)
        elif p == "decided_by" and (s in anchors or o in anchors):
            target = o if s in anchors else s
            if claims.get(target, {}).get("kind") == "decision":
                link("decisions", target, rel)
        elif p == "constrained_by" and s in anchors and o_kind in CONSTRAINT_KINDS:
            link("constraints", o, rel)
        elif p in {"references", "learned_from", "contradicts"}:
            if s in anchors and o_kind in HISTORY_KINDS:
                link("history", o, rel)
            elif o in anchors and s_kind in HISTORY_KINDS:
                link("history", s, rel)
        elif p == "belongs_to" and s in owners and o in layer_ids:
            structural_relation_ids.add(rel["id"])
        elif p == "applies_to" and s in rule_ids and o in owners | layer_ids:
            structural_relation_ids.add(rel["id"])
    for rel in edges:
        s, p, o = rel["subject"], rel["predicate"], rel["object"]
        if (p == "derived_from" and s in buckets["decisions"]
                and claims.get(o, {}).get("kind") in HISTORY_KINDS):
            link("history", o, rel, via="second hop through linked decision: ")
        elif p in {"references", "contradicts"}:
            if s in buckets["decisions"] and claims.get(o, {}).get("kind") == "alternative":
                link("alternatives", o, rel, via="second hop through linked decision: ")
            elif o in buckets["decisions"] and claims.get(s, {}).get("kind") == "alternative":
                link("alternatives", s, rel, via="second hop through linked decision: ")
        elif (p == "constrained_by" and s in buckets["decisions"]
                and claims.get(o, {}).get("kind") in CONSTRAINT_KINDS):
            link("constraints", o, rel, via="second hop through linked decision: ")

    def items(bucket: str) -> list[dict]:
        return [_context_item(cid, claims[cid], buckets[bucket][cid]) for cid in sorted(buckets[bucket])]

    contracts, decisions = items("contracts"), items("decisions")
    constraints = items("constraints")
    alternatives = items("alternatives")
    history, verification = items("history"), items("verification_refs")
    lists = {"contracts": contracts, "constraints": constraints, "decisions": decisions,
             "alternatives": alternatives, "history": history,
             "verification_refs": verification}
    verified_list = [_context_item(cid, claims[cid], verified_text[cid]) for cid in verified_components]
    totals = {
        "owning_components": len(owners), "architecture_rules": len(rule_ids),
        "layers": len(base["layers"]), "bounded_contexts": len(base["bounded_contexts"]),
        "verified_components": len(verified_all),
        **{name: len(group) for name, group in lists.items()},
    }
    omitted = {name: max(0, total - limit) for name, total in totals.items()}
    # Every verified component not returned counts, including components supported
    # only by an omitted verification record; the limit arithmetic would undercount.
    omitted["verified_components"] = len(verified_all) - len(verified_list)
    truncated = any(omitted.values())

    gaps: list[dict] = []
    if not owners:
        gaps.append({"category": "ownership", "status": "NOT_ASSESSED", "note": NOT_ASSESSED_NOTE})
    elif len(owners) > 1:
        shown = min(len(owners), limit)
        gaps.append({"category": "ownership", "status": "AMBIGUOUS",
                     "note": f"{len(owners)} reviewed components declare this path; "
                             f"{shown} shown, {len(owners) - shown} omitted by limit."})
    if test_verifications:
        gaps.append({"category": "verification_relevance", "status": "NOT_AN_OWNER",
                     "note": f"No component owns this file. {len(test_verifications)} verification "
                             "record(s) name it as authority or evidence; those links show relevance only. "
                             "They do not establish ownership, architectural dependency or runtime behaviour."})
        if not verified_all:
            gaps.append({"category": "verified_components", "status": "NOT_ASSESSED",
                         "note": "No component records a tested_by relation to the verification "
                                 "record(s) above, so no verified component context is available."})
        elif len(verified_all) > len(verified_list):
            gaps.append({"category": "verified_components", "status": "TRUNCATED",
                         "note": f"{len(verified_all) - len(verified_list)} verified component(s) are "
                                 "not returned: beyond the limit, or supported only by verification "
                                 "record(s) the limit omitted. Their decisions, constraints and history "
                                 "are not expanded."})
    if not rule_ids:
        gaps.append({"category": "architecture_rules", "status": "NOT_ASSESSED",
                     "note": "No rule matched this path by declared scope or graph link. "
                             "This is not evidence that no rule applies."})
    for name, group in lists.items():
        if not group:
            note = (_EMPTY_CATEGORY_NOTES[name] if anchors else
                    "Cannot assess: no owning component or applicable rule anchors this path.")
            gaps.append({"category": name, "status": "NOT_ASSESSED", "note": note})
    # Include owner and layer claims as well as the expanded linked categories:
    # a hypothetical owner or constraint is not an established obligation.
    considered_ids = owners | layer_ids | rule_ids | set(verified_components) | {
        item["claim_id"] for group in lists.values() for item in group
    }
    inactive = sorted(cid for cid in considered_ids
                      if claims[cid].get("epistemic_status") in INACTIVE_STATUSES)
    if inactive:
        gaps.append({"category": "epistemic_status", "status": "EPISTEMIC_CAVEAT",
                     "note": f"{len(inactive)} contextual record(s) are superseded, contested or "
                             f"invalidated: {', '.join(inactive[:8])}. "
                             "They are not current obligations."})
    hypothetical = sorted(cid for cid in considered_ids
                          if claims[cid].get("epistemic_status") == "hypothetical")
    if hypothetical:
        gaps.append({"category": "epistemic_status", "status": "HYPOTHETICAL_CAVEAT",
                     "note": f"{len(hypothetical)} contextual record(s) are hypothetical: "
                             f"{', '.join(hypothetical[:8])}. "
                             "These are unconfirmed possibilities, not established architectural obligations."})
    if truncated:
        gaps.append({"category": "limits", "status": "TRUNCATED",
                     "note": f"Categories above the limit of {limit} are cut; see omitted counts."})

    owner_list = sorted(owners)[:limit]
    layer_list = base["layers"][:limit]
    context_list = base["bounded_contexts"][:limit]
    rule_list = base["applicable_rules"][:limit]
    context = {
        "target_path": path,
        "ownership": {
            "coverage_status": base["coverage_status"], "components": owner_list,
            "ambiguous": base["ownership_ambiguous"],
            "layers": layer_list, "bounded_contexts": context_list,
        },
        "architecture_rules": rule_list,
        "contracts": contracts[:limit], "constraints": constraints[:limit],
        "decisions": decisions[:limit],
        "alternatives": alternatives[:limit],
        "history": history[:limit], "verification_refs": verification[:limit],
        "verified_components": verified_list[:limit],
        "knowledge_gaps": gaps, "omitted": omitted, "truncated": truncated,
        "note": CONTEXT_NOTE,
    }
    returned: set[str] = {*owner_list, *layer_list, *context_list, *(r["claim_id"] for r in rule_list)}
    for group in (contracts, constraints, decisions, alternatives, history, verification):
        returned.update(item["claim_id"] for item in group[:limit])
    returned.update(item["claim_id"] for item in verified_list[:limit])

    # The global relation envelope should describe visible context, not entries
    # omitted by the independent category limits. Keep every link for a shown
    # item, including labelled second hops and flows_to-carried contracts.
    selected_relations = {
        rid for name in lists for item in context[name]
        for rid in link_relation_ids[name].get(item["claim_id"], ())
    }
    selected_relations.update(rid for item in verified_list[:limit]
                              for rid in verified_rel_ids.get(item["claim_id"], ()))
    selected_relations.update(
        rel["id"] for rel in edges
        if rel["id"] in structural_relation_ids
        and rel["subject"] in returned and rel["object"] in returned
    )
    return context, sorted(returned), sorted(selected_relations)


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
    """Only explicit reviewed ownership locates component code; citations are not ownership."""
    paths = set(claim.get("attributes", {}).get("owned_paths", []))
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
    assessed_scope_files: set[str] = set()
    edges = list(relations)
    manifest_modules: set[str] | None = None
    stable_modules: set[str] | None = None
    if "release-v1.0.yaml" in tracked:
        try:
            import yaml

            release = yaml.safe_load(read_source("release-v1.0.yaml")) or {}
            manifest_modules = set(release.get("package_boundary", {}).get("source_only_modules", []))
            stable_modules = set(release.get("public_surface", {}).get("stable_python_modules", []))
        except (ValueError, KeyError, TypeError, yaml.YAMLError) as exc:
            not_assessed.append(f"release manifest could not be read: {exc}")
    for rule_id, rule in sorted(claims.items()):
        if rule["kind"] != "architecture_rule":
            continue
        attrs = rule.get("attributes", {})
        reasons: list[str] = []
        in_scope = _rule_scoped_files(rule_id, rule, claims, edges, tracked)
        python_files = sorted(p for p in in_scope if p.endswith(".py"))
        if attrs.get("rule_type") == "dependency_direction":
            assessed_scope_files.update(python_files)
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
            owned = _component_files(claim)
            if not owned:
                reasons.append(f"target {target} has no explicit owned_paths")
            dest.update(owned)
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
    if stable_modules is not None:
        for module in sorted(stable_modules):
            stem = "src/" + module.replace(".", "/")
            stable_files = {p for p in tracked if p.endswith(".py") and (
                p == stem + ".py" or p.startswith(stem + "/")
            )}
            if not stable_files:
                not_assessed.append(f"stable manifest module has no tracked Python source: {module}")
            for uncovered in sorted(stable_files - assessed_scope_files):
                not_assessed.append(f"stable module not covered by a dependency rule: {uncovered}")
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
