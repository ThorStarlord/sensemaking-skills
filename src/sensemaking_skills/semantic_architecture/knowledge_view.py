"""Read-only, source-qualified projection of an indexed semantic neighborhood.

This module does not infer semantic premises, prove causation, or authorize actions.
It creates a bounded presentation over an existing exact-revision knowledge query.
A local browser may display the same envelope without becoming a knowledge store.
"""

from __future__ import annotations

import json
from importlib import resources
from typing import Any

from .knowledge import ID_PATTERN, SHA_PATTERN

_VIEW_VERSION = 1
_ESTABLISHMENT = frozenset({
    "SOURCE_DECLARED", "MECHANICAL", "AGENT_INFERRED", "SCENARIO", "UNKNOWN",
})
_ROLES = frozenset({
    "NECESSARY", "SUPPORTING", "DEFEATER", "CONTEXT_ONLY",
    "UNKNOWN", "SCENARIO_ONLY",
})


def _text(value: Any, *, name: str, max_chars: int = 1200, allow_empty: bool = False) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{name} must be text")
    if len(value) > max_chars or (not allow_empty and not value.strip()):
        raise ValueError(f"{name} is empty or exceeds {max_chars} characters")
    return value


def _identity(value: Any, *, name: str) -> str:
    result = _text(value, name=name, max_chars=128)
    if ID_PATTERN.fullmatch(result) is None:
        raise ValueError(f"{name} must be a stable claim/relation identifier")
    return result


def _revision(value: Any, *, name: str) -> str:
    result = _text(value, name=name, max_chars=40)
    if SHA_PATTERN.fullmatch(result) is None:
        raise ValueError(f"{name} must be an exact 40-character Git SHA")
    return result


def _source_refs(value: Any, *, name: str, cap: int = 50) -> list[str]:
    if not isinstance(value, (list, tuple)) or len(value) > cap:
        raise ValueError(f"{name} must be a bounded list of source references")
    return [_text(ref, name=name, max_chars=1500) for ref in value]


def _establishment(record: dict[str, Any]) -> str:
    if record.get("derivation") == "mechanical" or record.get("authority_kind") == "mechanical":
        return "MECHANICAL"
    if record.get("derivation") == "lexical":
        return "UNKNOWN"
    return "SOURCE_DECLARED"


def _node(record: dict[str, Any]) -> dict[str, Any]:
    statement = _text(record.get("statement"), name="claim statement", max_chars=12000)
    return {
        "id": _identity(record.get("id"), name="claim id"),
        "kind": _text(record.get("kind"), name="claim kind", max_chars=80),
        "label": statement[:600] + ("..." if len(statement) > 600 else ""),
        "epistemic_status": _text(record.get("epistemic_status"), name="claim status", max_chars=80),
        "authority_kind": _text(record.get("authority_kind"), name="claim authority", max_chars=80),
        "authority_ref": _text(record.get("authority_ref", "not assessed"), name="claim authority_ref", max_chars=1500),
        "establishment": _establishment(record),
        "source_ref": _text(record.get("source_ref"), name="claim source", max_chars=1500),
        "evidence_refs": _source_refs(record.get("evidence_refs"), name="claim evidence"),
    }


def _edge(record: dict[str, Any]) -> dict[str, Any]:
    predicate = _text(record.get("predicate"), name="relation predicate", max_chars=80)
    return {
        "id": _identity(record.get("id"), name="relation id"),
        "subject": _identity(record.get("subject"), name="relation subject"),
        "object": _identity(record.get("object"), name="relation object"),
        "predicate": predicate,
        # Navigation links never establish a necessary premise.
        "role": "CONTEXT_ONLY" if predicate in {"references", "contained_in"} else "UNKNOWN",
        "establishment": _establishment(record),
        "epistemic_status": _text(record.get("epistemic_status"), name="relation status", max_chars=80),
        "source_ref": _text(record.get("source_ref"), name="relation source", max_chars=1500),
        "evidence_refs": _source_refs(record.get("evidence_refs"), name="relation evidence"),
        "scenario_only": False,
    }


def build_graph_exploration_view(
    query: dict[str, Any], *, question: str, focus_ref: str,
    max_nodes: int = 80, max_edges: int = 160,
) -> dict[str, Any]:
    """Project explicit query records, never deriving semantic edge closure.

    The input should come from query_knowledge against one exact indexed snapshot.
    Omission counts cover *visible query records* only. Query-level truncation is
    separately and visibly preserved because unknown source omissions cannot
    truthfully be counted as zero.
    """
    if not isinstance(query, dict):
        raise ValueError("expected one exact-revision knowledge query")
    if query.get("semantic_truth_established") is not False or query.get("action_authorized") is not False:
        raise ValueError("query may not claim semantic truth or action authority")
    repository = _text(query.get("repository"), name="repository", max_chars=200)
    ref = _revision(query.get("target_ref"), name="target_ref")
    focus = _identity(focus_ref, name="focus_ref")
    _text(question, name="question", max_chars=400)
    if not isinstance(max_nodes, int) or isinstance(max_nodes, bool) or not 1 <= max_nodes <= 250:
        raise ValueError("max_nodes must be 1..250")
    if not isinstance(max_edges, int) or isinstance(max_edges, bool) or not 0 <= max_edges <= 250:
        raise ValueError("max_edges must be 0..250")
    raw_nodes = query.get("claims")
    raw_edges = query.get("relations")
    if not isinstance(raw_nodes, list) or not isinstance(raw_edges, list):
        raise ValueError("query claims/relations must be lists")
    if len(raw_nodes) > 250 or len(raw_edges) > 250:
        raise ValueError("query exceeds supported bounded envelope")
    if any(not isinstance(x, dict) for x in [*raw_nodes, *raw_edges]):
        raise ValueError("query records must be objects")
    nodes = [_node(x) for x in raw_nodes]
    relations = [_edge(x) for x in raw_edges]
    all_ids = [x["id"] for x in nodes]
    if len(all_ids) != len(set(all_ids)):
        raise ValueError("duplicate claim IDs in source query")
    if len({x["id"] for x in relations}) != len(relations):
        raise ValueError("duplicate relation IDs in source query")
    if focus not in all_ids:
        raise ValueError("focus_ref is absent from the bounded query; inspect a smaller neighborhood")
    nodes.sort(key=lambda x: (x["id"] != focus, x["id"]))
    selected_nodes = nodes[:max_nodes]
    visible_ids = {x["id"] for x in selected_nodes}
    relations.sort(key=lambda x: x["id"])
    visible_edges = [
        x for x in relations
        if x["subject"] in visible_ids and x["object"] in visible_ids
    ][:max_edges]
    source_truncated = query.get("truncated") is True
    omitted_nodes = len(nodes) - len(selected_nodes)
    omitted_edges = len(relations) - len(visible_edges)
    notices: list[str] = []
    if source_truncated:
        notices.append("Underlying knowledge query was truncated; counts below exclude unknown source omissions.")
    if omitted_nodes or omitted_edges:
        notices.append("Local display caps or unavailable endpoint records omit some returned items.")
    if not visible_edges:
        notices.append("No explicit edges are visible in this bounded view; absence is NOT_ASSESSED.")
    source_scope = query.get("source_scope", [])
    limits = query.get("explicit_limits", [])
    if not isinstance(source_scope, list) or not isinstance(limits, list):
        raise ValueError("source_scope and explicit_limits must be lists")
    view = {
        "view_version": _VIEW_VERSION,
        "repository": repository,
        "target_ref": ref,
        "indexed_ref": ref,
        "assessed_ref": None,
        "question": question.strip(),
        "focus_ref": focus,
        "provenance": "INDEXED_QUERY",
        "source_scope": _source_refs(source_scope, name="source scope", cap=100),
        "explicit_limits": _source_refs(limits, name="query limitations", cap=100),
        "nodes": selected_nodes,
        "edges": visible_edges,
        "comparisons": [],
        "scenarios": [],
        "coverage": {
            "omitted_nodes": omitted_nodes,
            "omitted_edges": omitted_edges,
            "source_truncated": source_truncated,
            "truncated": source_truncated or bool(omitted_nodes or omitted_edges),
            "unassessed": notices,
        },
        "semantic_truth_established": False,
        "action_authorized": False,
    }
    validate_graph_exploration_view(view)
    return view


def validate_graph_exploration_view(view: dict[str, Any]) -> dict[str, Any]:
    """Validate presentation integrity, not original evidence or inference truth.

    Accepts both deterministic indexed projections and explicitly curated,
    attributed source-only examples. It does not promote either to authority.
    """
    if not isinstance(view, dict) or type(view.get("view_version")) is not int or view["view_version"] != 1:
        raise ValueError("unsupported graph view version")
    _text(view.get("repository"), name="repository", max_chars=200)
    ref = _revision(view.get("target_ref"), name="target_ref")
    if view.get("indexed_ref") is not None and _revision(view["indexed_ref"], name="indexed_ref") != ref:
        raise ValueError("indexed_ref cannot be a different repository snapshot")
    if view.get("assessed_ref") is not None:
        _revision(view["assessed_ref"], name="assessed_ref")
    if view.get("semantic_truth_established") is not False or view.get("action_authorized") is not False:
        raise ValueError("graph view cannot establish semantic truth or authority")
    _text(view.get("question"), name="question", max_chars=400)
    focus = _identity(view.get("focus_ref"), name="focus_ref")
    nodes, edges = view.get("nodes"), view.get("edges")
    if not isinstance(nodes, list) or not isinstance(edges, list) or len(nodes) > 250 or len(edges) > 250:
        raise ValueError("graph view contains invalid or unbounded nodes/edges")
    ids: set[str] = set()
    for node in nodes:
        if not isinstance(node, dict):
            raise ValueError("graph node must be an object")
        nid = _identity(node.get("id"), name="node id")
        if nid in ids:
            raise ValueError("duplicate graph node ID")
        ids.add(nid)
        for field in ("kind", "label", "epistemic_status", "authority_kind", "source_ref"):
            _text(node.get(field), name=f"node {field}", max_chars=1500)
        if node.get("establishment") not in _ESTABLISHMENT:
            raise ValueError("invalid node establishment")
        _source_refs(node.get("evidence_refs"), name="node evidence")
    if focus not in ids:
        raise ValueError("graph focus node not present")
    edge_ids: set[str] = set()
    for edge in edges:
        if not isinstance(edge, dict):
            raise ValueError("graph edge must be an object")
        eid = _identity(edge.get("id"), name="edge id")
        if eid in edge_ids:
            raise ValueError("duplicate graph edge ID")
        edge_ids.add(eid)
        if _identity(edge.get("subject"), name="edge subject") not in ids or _identity(edge.get("object"), name="edge object") not in ids:
            raise ValueError("graph edge endpoint missing in visible graph")
        for field in ("predicate", "epistemic_status", "source_ref"):
            _text(edge.get(field), name=f"edge {field}", max_chars=1500)
        if edge.get("role") not in _ROLES or edge.get("establishment") not in _ESTABLISHMENT:
            raise ValueError("unsupported edge role or establishment")
        if type(edge.get("scenario_only")) is not bool:
            raise ValueError("scenario_only must be boolean")
        if edge["scenario_only"] and edge["establishment"] != "SCENARIO":
            raise ValueError("scenario-only edges must remain hypothetical")
        _source_refs(edge.get("evidence_refs"), name="edge evidence")
    coverage = view.get("coverage")
    if not isinstance(coverage, dict):
        raise ValueError("graph view requires coverage")
    for key in ("omitted_nodes", "omitted_edges"):
        value = coverage.get(key)
        if type(value) is not int or value < 0:
            raise ValueError(f"coverage {key} must be a nonnegative integer")
    for key in ("truncated", "source_truncated"):
        if type(coverage.get(key)) is not bool:
            raise ValueError(f"coverage {key} must be boolean")
    if (coverage["omitted_nodes"] or coverage["omitted_edges"] or coverage["source_truncated"]) and not coverage["truncated"]:
        raise ValueError("omissions or source truncation must be disclosed")
    _source_refs(coverage.get("unassessed"), name="coverage unassessed", cap=100)
    for field in ("source_scope", "explicit_limits"):
        _source_refs(view.get(field, []), name=field, cap=100)
    if view.get("comparisons", []) and not isinstance(view.get("comparisons"), list):
        raise ValueError("comparisons must be a list")
    if view.get("scenarios", []) and not isinstance(view.get("scenarios"), list):
        raise ValueError("scenarios must be a list")
    return view


def render_graph_view_html(view: dict[str, Any]) -> str:
    """Render an offline, self-contained HTML companion with inert embedded JSON.

    The browser can only select and draft a new message; it never mutates the
    authoritative graph, runs tool commands or treats scenarios as ratified.
    """
    validate_graph_exploration_view(view)
    template = resources.files("sensemaking_skills.semantic_architecture").joinpath(
        "view_assets", "graph_view.html"
    ).read_text(encoding="utf-8")
    marker = "__SENSEMAKING_GRAPH_VIEW_JSON__"
    if template.count(marker) != 1:
        raise ValueError("graph viewer template requires exactly one data placeholder")
    # JSON parser restores escaped source text, but HTML parser never sees a
    # literal script-close tag or executable user-provided markup.
    data = json.dumps(view, ensure_ascii=True, sort_keys=True, separators=(",", ":"))
    data = data.replace("&", r"\u0026").replace("<", r"\u003c").replace(">", r"\u003e")
    return template.replace(marker, data)
