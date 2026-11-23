"""Read-only construction bridge for a Campaign's bound capability outcome.

The bridge joins the agent-authored ``extensions.capability_outcome`` record to
the explicitly declared ``requires_capability`` and ``implemented_by`` routes
for the same possibility at one committed repository revision. It removes the
manual cross-reference between Campaign state and the reviewed knowledge index;
it does not select the possibility, inspect component code, establish
implementation, sufficiency or readiness, or recommend an increment.
"""

from __future__ import annotations

import sqlite3
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from .campaign_knowledge_context import CampaignKnowledgeError, select_campaign_target
from .campaigns import CampaignWorkspaceError
from .campaigns.execution import CampaignExecutionService
from .campaigns.target_snapshot import repository_identity
from .workspace_knowledge import run_workspace_query

CAPABILITY_OUTCOME_BRIDGE = "CAPABILITY_OUTCOME_BRIDGE"
ROUTE_ALIGNMENT_ALIGNED = "ALIGNED"
ROUTE_ALIGNMENT_MISMATCHED = "MISMATCHED"
ROUTE_ALIGNMENT_NOT_ASSESSED = "NOT_ASSESSED"

_EXPLICIT_LIMIT = (
    "The capability-outcome bridge joins an agent-authored Campaign binding to "
    "documentary required-capability routes at one committed revision. It does "
    "not select or rank an increment, inspect component code, establish "
    "implementation, sufficiency, readiness or semantic truth, and it does not "
    "authorize action."
)


def build_capability_bridge(
    *,
    workspace: str | Path,
    repo: str | Path,
    ref: str,
    target_alias: str | None = None,
) -> dict[str, Any]:
    """Project one Campaign's bound outcome beside its declared capability routes.

    The Campaign state remains the authority for the bound outcome, responsibility
    and authority. The knowledge query supplies only the exact-revision
    possibilities, capabilities, components and relations authored in the
    checkout. Neither source is verified by this join.
    """

    context = CampaignExecutionService(workspace).working_context()
    outcome = context.get("capability_outcome")
    if not isinstance(outcome, dict):
        raise CampaignKnowledgeError(
            "the Campaign has no bound capability outcome; bind one with "
            "'campaign capability-outcome bind' before projecting its bridge"
        )
    possibility_id = str(outcome.get("possibility_id") or "").strip()
    if not possibility_id:
        raise CampaignKnowledgeError(
            "the bound capability outcome has no possibility_id"
        )

    route_query = _route_query(repo, ref, possibility_id)
    ecology = route_query["possibility_ecology"]
    focus = ecology.get("focus")
    if not isinstance(focus, dict) or focus.get("claim_id") != possibility_id:
        raise CampaignKnowledgeError(
            f"the queried knowledge did not return the bound possibility {possibility_id!r}"
        )

    routes = tuple(ecology.get("required_capability_routes") or ())
    alignment = _route_alignment(outcome.get("required_capabilities") or (), routes)
    source_alignment = _source_alignment(outcome.get("source_refs") or (), focus)
    target_binding = _target_binding(
        context.get("targets") or (), target_alias, Path(repo)
    )
    workspace_context = route_query.get("workspace_context") or {}
    workspace_index = route_query.get("workspace_index") or {}
    route_truncated = bool(
        ecology.get("required_capability_omitted")
        or any(
            (route.get("implementation_component_omitted") or 0)
            for route in routes
        )
    )

    return {
        "ok": True,
        "code": CAPABILITY_OUTCOME_BRIDGE,
        "campaign_id": context.get("campaign_id"),
        "capability_outcome": outcome,
        "target_binding": target_binding,
        "source_identity": {
            "repository": route_query.get("repository"),
            "repository_identity_source": workspace_index.get(
                "repository_identity_source"
            ),
            "repository_label_verified": workspace_index.get(
                "repository_label_verified"
            ),
            "requested_ref": ref,
            "indexed_ref": workspace_index.get("indexed_ref"),
            "index_state": workspace_index.get("index_state"),
            "source_scope": route_query.get("source_scope"),
            "workspace_context": workspace_context,
        },
        "bridge": {
            "possibility_id": possibility_id,
            "focus": focus,
            "realization": focus.get("realization"),
            "required_capability_routes": list(routes),
            "required_capability_total": ecology.get("required_capability_total"),
            "required_capability_omitted": ecology.get("required_capability_omitted"),
            "required_capability_link_not_assessed": ecology.get(
                "required_capability_link_not_assessed"
            ),
            "route_alignment": alignment,
            "source_alignment": source_alignment,
            "route_truncated": route_truncated,
        },
        "caveats": _caveats(
            target_binding=target_binding,
            workspace_context=workspace_context,
            alignment=alignment,
            source_alignment=source_alignment,
            ecology=ecology,
            route_truncated=route_truncated,
        ),
        "selection_performed": False,
        "recommendation_performed": False,
        "semantic_truth_established": False,
        "action_authorized": False,
        "implementation_verified": False,
        "explicit_limit": _EXPLICIT_LIMIT,
    }


def _route_query(
    repo: str | Path, ref: str, possibility_id: str
) -> dict[str, Any]:
    """Run the existing zero-setup possibility-ecology query at one revision."""
    try:
        payload = run_workspace_query(
            repo=repo,
            ref=ref,
            operation="possibility-ecology",
            subject=possibility_id,
        )
    except (ValueError, OSError, UnicodeError, sqlite3.Error) as exc:
        raise CampaignKnowledgeError(
            f"required-capability routes could not be queried: {exc}"
        ) from exc
    ecology = payload.get("possibility_ecology")
    if not isinstance(ecology, dict):
        raise CampaignKnowledgeError(
            "the knowledge query returned no possibility ecology projection"
        )
    if ecology.get("focus_kind") != "opportunity":
        raise CampaignKnowledgeError(
            f"the bound claim {possibility_id!r} is not an opportunity; "
            "the bridge joins opportunity required-capability routes only"
        )
    return payload


def _target_binding(
    targets: Sequence[Mapping[str, Any]],
    target_alias: str | None,
    repo: Path,
) -> dict[str, Any]:
    """Verify the queried checkout against a bound Campaign target when one exists."""
    if not targets:
        if target_alias is not None:
            raise CampaignKnowledgeError(
                "--target-alias was supplied, but this Campaign has no bound target"
            )
        return {
            "assessment": ROUTE_ALIGNMENT_NOT_ASSESSED,
            "target_alias": None,
            "detail": (
                "This Campaign has no bound target; the queried repository is an "
                "explicit knowledge source, not a verified Campaign target."
            ),
        }
    target = select_campaign_target(targets, target_alias)
    try:
        identity_source, repository_id = repository_identity(repo)
    except (CampaignWorkspaceError, OSError, UnicodeError) as exc:
        raise CampaignKnowledgeError(
            f"the knowledge checkout identity could not be verified: {exc}"
        ) from exc
    if repository_id != target.get("repository_id"):
        raise CampaignKnowledgeError(
            f"the knowledge checkout is not the repository bound to Campaign target "
            f"{target['alias']!r}; refusing to attribute its routes to this Campaign"
        )
    return {
        "assessment": "MATCH",
        "target_alias": target["alias"],
        "repository_id_match": True,
        "repository_identity_source": identity_source,
        "target_head_sha": target.get("head_sha"),
    }


def _route_alignment(
    declared: Sequence[str], routes: Sequence[Mapping[str, Any]]
) -> dict[str, Any]:
    """Mechanically compare the Campaign's capability IDs with declared route IDs."""
    declared_ids = list(dict.fromkeys(str(item) for item in declared if str(item)))
    route_ids = [
        str(route["capability_claim_id"])
        for route in routes
        if route.get("capability_claim_id")
    ]
    declared_set = set(declared_ids)
    route_set = set(route_ids)
    matched = [item for item in declared_ids if item in route_set]
    campaign_only = [item for item in declared_ids if item not in route_set]
    knowledge_only = [item for item in route_ids if item not in declared_set]

    if not declared_ids and not route_ids:
        assessment = ROUTE_ALIGNMENT_NOT_ASSESSED
        detail = "Neither the Campaign binding nor the repository declares a required capability."
    elif campaign_only or knowledge_only:
        assessment = ROUTE_ALIGNMENT_MISMATCHED
        detail = (
            "The Campaign binding and the repository's declared requires_capability "
            "edges do not name the same capability set; the difference is reported, "
            "not repaired or ranked."
        )
    else:
        assessment = ROUTE_ALIGNMENT_ALIGNED
        detail = "The Campaign binding and the repository declare the same capability set."
    return {
        "assessment": assessment,
        "matched": matched,
        "campaign_only": campaign_only,
        "knowledge_only": knowledge_only,
        "campaign_required_capability_count": len(declared_ids),
        "declared_route_count": len(route_ids),
        "detail": detail,
    }


def _source_alignment(
    campaign_refs: Sequence[str], focus: Mapping[str, Any]
) -> dict[str, Any]:
    """Report whether the binding and the indexed possibility cite a shared path.

    A shared path is a documentary join, not proof that the binding is correct or
    that either record is semantically current.
    """
    campaign = [str(item) for item in campaign_refs]
    focus_refs: list[str] = []
    for key in ("source_ref", "authority_ref"):
        value = focus.get(key)
        if isinstance(value, str) and value:
            focus_refs.append(value)
    focus_refs.extend(str(item) for item in (focus.get("evidence_refs") or ()))

    def normalize(value: str) -> str:
        return value[len("file:"):] if value.startswith("file:") else value

    overlap = sorted(
        {normalize(item) for item in campaign}
        & {normalize(item) for item in focus_refs}
    )
    return {
        "campaign_source_refs": campaign,
        "focus_source_ref": focus.get("source_ref"),
        "focus_authority_ref": focus.get("authority_ref"),
        "overlap": overlap,
        "assessment": "MATCH" if overlap else ROUTE_ALIGNMENT_NOT_ASSESSED,
        "detail": (
            "At least one cited source path is shared; this is a documentary join, "
            "not verification."
            if overlap
            else "No cited source path is shared; this is not by itself evidence that the binding is wrong."
        ),
        "semantic_truth_established": False,
    }


def _caveats(
    *,
    target_binding: Mapping[str, Any],
    workspace_context: Mapping[str, Any],
    alignment: Mapping[str, Any],
    source_alignment: Mapping[str, Any],
    ecology: Mapping[str, Any],
    route_truncated: bool,
) -> list[dict[str, str]]:
    caveats: list[dict[str, str]] = []
    if target_binding.get("assessment") == ROUTE_ALIGNMENT_NOT_ASSESSED:
        caveats.append({
            "code": "TARGET_NOT_BOUND",
            "detail": str(target_binding.get("detail") or ""),
        })
    if not workspace_context.get("head_matches_indexed_ref"):
        caveats.append({
            "code": "HISTORICAL_CHECKOUT_HEAD",
            "detail": (
                "The active checkout is not at the indexed revision; re-inspect "
                "the original sources before relying on these routes."
            ),
        })
    if not workspace_context.get("worktree_clean"):
        caveats.append({
            "code": "UNINDEXED_WORKTREE_CHANGES",
            "detail": (
                "Uncommitted or untracked changes are not indexed; the bridge "
                "describes committed bytes only."
            ),
        })
    if alignment.get("assessment") == ROUTE_ALIGNMENT_MISMATCHED:
        caveats.append({
            "code": "ROUTE_ALIGNMENT_MISMATCH",
            "detail": str(alignment.get("detail") or ""),
        })
    if source_alignment.get("assessment") != "MATCH":
        caveats.append({
            "code": "SOURCE_REF_NOT_JOINED",
            "detail": str(source_alignment.get("detail") or ""),
        })
    if ecology.get("required_capability_link_not_assessed"):
        caveats.append({
            "code": "REQUIRED_CAPABILITY_ROUTES_NOT_ASSESSED",
            "detail": (
                "The selected possibility declares no required-capability route; "
                "absence is NOT_ASSESSED, not evidence that no capability applies."
            ),
        })
    if route_truncated:
        caveats.append({
            "code": "ROUTES_TRUNCATED",
            "detail": (
                "The bounded route projection omitted capabilities or implementation "
                "components; see the total and omission counts."
            ),
        })
    caveats.append({
        "code": "DOCUMENTARY_ROUTES",
        "detail": (
            "Routes join explicit authored relations; no component code was "
            "inspected and implementation_verified remains false."
        ),
    })
    caveats.append({
        "code": "INSPECT_ORIGINAL_SOURCE",
        "detail": (
            "Read the cited possibility, capability and component sources before "
            "relying on the bridge."
        ),
    })
    return caveats
