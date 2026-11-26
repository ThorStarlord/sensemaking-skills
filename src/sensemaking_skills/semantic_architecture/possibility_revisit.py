"""Evaluate authored possibility revisit conditions during a committed review.

A ``revisit_when`` value may embed explicit references:

- ``file:path/to/file``
- ``claim:kind:identifier``
- ``symbol:path/to/file.py#name``

This module evaluates only those explicit references. It does not interpret the
surrounding prose, infer semantic consequence, rank possibilities, revive a
candidate or authorize work. A fired reference is a reconsideration prompt.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Iterable

from .source_relationships import build_source_review_comparison
from .worktree_context import guarded_git_text

_MAX_REFS = 8
_MAX_LIMIT = 50
_REF = re.compile(r"(?<![A-Za-z0-9_])(?P<kind>claim|file|symbol):(?P<value>[^\s,;)\]\}]+)")
_CLAIM = re.compile(r"[a-z][a-z0-9_-]*:[A-Za-z0-9._-]+\Z")
_SYMBOL = re.compile(r"[A-Za-z_][A-Za-z0-9_]*\Z")
_LINE_SUFFIX = re.compile(r":line:\d+\Z")
_LIMITS = (
    "Only explicit file:, claim: and symbol: references inside revisit_when are evaluated; surrounding prose is NOT INTERPRETED.",
    "A fired reference is a reconsideration prompt, not evidence that the possibility is stale, invalid or selected again.",
    "Claim comparison is a normalized record diff at the two revisions plus authority/evidence path changes; it does not establish semantic consequence.",
    "Symbol comparison is the existing source-level behavior surface, not runtime behavior, test evidence or semantic equivalence.",
    "Claim and symbol comparison read committed BASE/TARGET knowledge and source; uncommitted knowledge changes are NOT ASSESSED.",
    "Conditions with no structured reference, missing claims, unsupported symbol paths or unavailable comparisons remain NOT_ASSESSED.",
    "This surface does not rank possibilities, revive candidates, update records or authorize work.",
)


def _normalized_path(value: str) -> str | None:
    value = _LINE_SUFFIX.sub("", value).rstrip(".")
    value = value.removeprefix("./")
    if (
        not value
        or value.startswith(("/", "\\", "-"))
        or ":" in value
        or "\\" in value
    ):
        return None
    parts = value.split("/")
    if any(part in ("", ".", "..") for part in parts):
        return None
    return value


def parse_revisit_condition(condition: str) -> dict[str, Any]:
    """Return explicit references and the surrounding text for one condition."""

    refs: list[dict[str, str]] = []
    seen: set[tuple[str, str]] = set()
    unparsed: list[str] = []
    for match in _REF.finditer(condition):
        kind = match.group("kind")
        raw = match.group("value").rstrip(".")
        value: str | None = None
        if kind == "file":
            value = _normalized_path(raw)
        elif kind == "claim":
            value = raw if _CLAIM.fullmatch(raw) else None
        elif kind == "symbol":
            path, separator, name = raw.partition("#")
            if separator and _SYMBOL.fullmatch(name):
                normalized = _normalized_path(path)
                if normalized is not None and normalized.endswith(".py"):
                    value = f"{normalized}#{name}"
        if value is None:
            unparsed.append(match.group(0))
            continue
        key = (kind, value)
        if key in seen:
            continue
        seen.add(key)
        if len(refs) < _MAX_REFS:
            refs.append({"kind": kind, "value": value, "raw": match.group(0)})
        else:
            unparsed.append(match.group(0))
    stripped = _REF.sub("", condition).strip()
    return {
        "refs": refs,
        "unparsed_refs": unparsed,
        "unstructured_text": stripped or None,
        "truncated": len(refs) >= _MAX_REFS and bool(unparsed),
    }


def _claims_at_commit(root: Path, sha: str) -> dict[str, dict[str, Any]]:
    names = guarded_git_text(
        root, "ls-tree", "-r", "-z", "--name-only", sha, "--", ".sensemaking/knowledge"
    ).split("\x00")
    claims: dict[str, dict[str, Any]] = {}
    for name in filter(None, names):
        if not name.endswith(".json"):
            continue
        raw = guarded_git_text(root, "show", f"{sha}:{name}")
        try:
            data = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise ValueError(f"knowledge file is not valid JSON at {sha}: {name}") from exc
        for record in data.get("claims", []) if isinstance(data, dict) else []:
            identifier = record.get("id")
            if not isinstance(identifier, str) or not identifier:
                raise ValueError(f"knowledge file has an invalid claim id at {sha}: {name}")
            if identifier in claims:
                raise ValueError(f"duplicate authored claim id at {sha}: {identifier}")
            claims[identifier] = record
    return claims


def _claim_file_refs(claim: dict[str, Any]) -> set[str]:
    refs: set[str] = set()
    authority = claim.get("authority_ref")
    if isinstance(authority, str) and not authority.startswith(("http:", "https:")):
        path = _normalized_path(authority)
        if path is not None:
            refs.add(path)
    for item in claim.get("evidence_refs", []) or []:
        if isinstance(item, str) and item.startswith("file:"):
            path = _normalized_path(item[5:])
            if path is not None:
                refs.add(path)
    return refs


def _normalized_claim(claim: dict[str, Any] | None) -> str | None:
    if claim is None:
        return None
    return json.dumps(claim, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def _evaluate_ref(
    ref: dict[str, str], *, root: Path, base_sha: str, target_sha: str,
    changed_paths: frozenset[str], base_claims: dict[str, dict[str, Any]],
    target_claims: dict[str, dict[str, Any]], symbol_cache: dict[tuple[str, str], dict[str, Any]],
) -> dict[str, Any]:
    kind = ref["kind"]
    value = ref["value"]
    result: dict[str, Any] = {
        "kind": kind,
        "value": value,
        "status": "NOT_ASSESSED",
        "reason": None,
        "evidence_refs": [],
        "detail": None,
    }
    if kind == "file":
        path = _normalized_path(value.removeprefix("file:"))
        if path is None:
            result["reason"] = "INVALID_FILE_REF"
            return result
        result["evidence_refs"] = [f"file:{path}"]
        if path in changed_paths:
            result["status"] = "FIRED"
            result["reason"] = "CHANGED_PATH"
        else:
            result["status"] = "NO_MATCH"
            result["reason"] = "PATH_UNCHANGED"
        return result
    if kind == "claim":
        value = value.removeprefix("claim:")
        base = base_claims.get(value)
        target = target_claims.get(value)
        result["value"] = value
        result["evidence_refs"] = [f"claim:{value}"]
        if base is None and target is None:
            result["reason"] = "CLAIM_MISSING"
            return result
        if _normalized_claim(base) != _normalized_claim(target):
            result["status"] = "FIRED"
            result["reason"] = "CLAIM_CHANGED"
            return result
        files = _claim_file_refs(base or {}) | _claim_file_refs(target or {})
        matched = sorted(files & changed_paths)
        if matched:
            result["status"] = "FIRED"
            result["reason"] = "CLAIM_EVIDENCE_CHANGED"
            result["evidence_refs"] = [f"file:{path}" for path in matched[:8]]
            return result
        result["status"] = "NO_MATCH"
        result["reason"] = "CLAIM_UNCHANGED"
        return result
    if kind == "symbol":
        path, _, name = value.removeprefix("symbol:").partition("#")
        if not path.endswith(".py") or not _SYMBOL.fullmatch(name):
            result["reason"] = "UNSUPPORTED_SYMBOL_REF"
            return result
        key = (path, name)
        if key not in symbol_cache:
            try:
                symbol_cache[key] = build_source_review_comparison(
                    root, base_sha, target_sha, path, limit=25, symbol=name,
                )
            except (ValueError, OSError, UnicodeError) as exc:
                symbol_cache[key] = {"_error": str(exc)}
        comparison = symbol_cache[key]
        if "_error" in comparison:
            result["reason"] = "COMPARISON_UNAVAILABLE"
            result["detail"] = str(comparison["_error"])[:300]
            return result
        behavior = comparison.get("symbol_behavior_comparison") or {}
        result["evidence_refs"] = [f"file:{path}", f"symbol:{path}#{name}"]
        if behavior.get("presence") != "BOTH":
            result["reason"] = "SYMBOL_NOT_VISIBLE_BOTH"
            return result
        if not str(comparison.get("comparison_status", "")).startswith("COMPLETE"):
            result["reason"] = "COMPARISON_PARTIAL"
            result["detail"] = str(comparison.get("comparison_status"))
            return result
        if comparison.get("truncated"):
            result["reason"] = "COMPARISON_TRUNCATED"
            return result
        changed_fields = list(behavior.get("changed_fields") or [])
        source_changed = bool(behavior.get("source_changed"))
        if changed_fields or source_changed:
            result["status"] = "FIRED"
            result["reason"] = "SYMBOL_BEHAVIOR_CHANGED"
            result["detail"] = {
                "changed_fields": changed_fields,
                "source_changed": source_changed,
            }
            return result
        result["status"] = "NO_MATCH"
        result["reason"] = "SYMBOL_UNCHANGED"
        return result
    result["reason"] = "UNSUPPORTED_REF"
    return result


def build_candidate_reconsiderations(
    root: Path, base_sha: str, target_sha: str, changed_paths: Iterable[str],
    *, limit: int = 25,
) -> dict[str, Any]:
    """Evaluate structured revisit conditions for authored opportunities."""

    if not 1 <= limit <= 100:
        raise ValueError("candidate reconsideration limit must be 1..100")
    effective_limit = min(limit, _MAX_LIMIT)
    changed = frozenset(
        path for path in (_normalized_path(str(item)) for item in changed_paths)
        if path is not None
    )
    base_claims = _claims_at_commit(root, base_sha)
    target_claims = _claims_at_commit(root, target_sha)
    symbol_cache: dict[tuple[str, str], dict[str, Any]] = {}
    evaluations: list[dict[str, Any]] = []
    unconditioned = 0
    for claim_id in sorted(base_claims):
        claim = base_claims[claim_id]
        if claim.get("kind") != "opportunity":
            continue
        attributes = claim.get("attributes") or {}
        condition = attributes.get("revisit_when")
        if not isinstance(condition, str) or not condition.strip():
            unconditioned += 1
            continue
        parsed = parse_revisit_condition(condition)
        refs = [
            _evaluate_ref(
                ref, root=root, base_sha=base_sha, target_sha=target_sha,
                changed_paths=changed, base_claims=base_claims,
                target_claims=target_claims, symbol_cache=symbol_cache,
            )
            for ref in parsed["refs"]
        ]
        fired = [ref for ref in refs if ref["status"] == "FIRED"]
        not_assessed = [ref for ref in refs if ref["status"] == "NOT_ASSESSED"]
        if fired:
            assessment = "FIRED"
        elif not_assessed or not refs or parsed["unparsed_refs"]:
            assessment = "NOT_ASSESSED"
        else:
            assessment = "NO_MATCH"
        realization = ((attributes.get("dimensions") or {}).get("realization") or {}).get("value")
        evaluations.append({
            "claim_id": claim_id,
            "statement": str(claim.get("statement", ""))[:500],
            "epistemic_status": claim.get("epistemic_status"),
            "realization": realization,
            "value_hypothesis": attributes.get("value_hypothesis"),
            "revisit_when": condition,
            "structured_refs": refs,
            "unstructured_text": parsed["unstructured_text"],
            "unparsed_refs": parsed["unparsed_refs"],
            "assessment": assessment,
            "reasons": sorted({
                *(ref["reason"] for ref in refs if ref.get("reason")),
                *(["UNPARSED_REFERENCE"] if parsed["unparsed_refs"] else []),
            }),
            "consumer_note": (
                "A fired reference is a reconsideration prompt; inspect the changed "
                "evidence and the authored condition before updating the possibility."
            ),
            "truncated": parsed["truncated"],
        })
    order = {"FIRED": 0, "NO_MATCH": 1, "NOT_ASSESSED": 2}
    evaluations.sort(key=lambda item: (order[item["assessment"]], item["claim_id"]))
    returned = evaluations[:effective_limit]
    omitted = evaluations[effective_limit:]
    counts = {
        "opportunities_total": sum(1 for claim in base_claims.values() if claim.get("kind") == "opportunity"),
        "with_condition": len(evaluations),
        "unconditioned": unconditioned,
        "fired": sum(1 for item in evaluations if item["assessment"] == "FIRED"),
        "no_match": sum(1 for item in evaluations if item["assessment"] == "NO_MATCH"),
        "not_assessed": sum(1 for item in evaluations if item["assessment"] == "NOT_ASSESSED"),
        "returned": len(returned),
        "omitted": len(omitted),
        "omitted_fired": sum(1 for item in omitted if item["assessment"] == "FIRED"),
    }
    truncated = bool(omitted) or any(item["truncated"] for item in returned)
    coverage = "PARTIAL" if truncated or counts["not_assessed"] else "COMPLETE_FOR_STRUCTURED_REFS"
    return {
        "scope": "all authored opportunity claims with a revisit_when at BASE",
        "change_paths_total": len(changed),
        "candidates": returned,
        "counts": counts,
        "selection_order": ["FIRED", "NO_MATCH", "NOT_ASSESSED"],
        "coverage_status": coverage,
        "truncated": truncated,
        "explicit_limits": list(_LIMITS),
    }
