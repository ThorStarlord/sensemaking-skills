"""Prepare a first-use or returning-engagement handoff to the installed Skill.

The handoff names paths, install-record facts and a target-repository inventory.
It does not analyze repository semantics, select work or authorize action. The
active agent still invokes the installed ``using-sensemaking`` entrypoint.
"""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from . import __version__
from .code_provenance import code_provenance_lines
from .reentry_context import continuity_inventory, selected_receipts
from .harness_adapters import CANONICAL_HARNESS_TARGETS, get_harness_adapter
from .semantic_architecture.worktree_context import guarded_git_text
from .setup_skills import (
    INSTALL_RECORD_NAME,
    SkillsSetupError,
    _CommittedSkillHistory,
    _git_tree_id,
    _skill_tree_fingerprint,
    _tree_digest,
    get_package_skills_dir,
    load_install_record,
)

ENTRY_SKILL = "using-sensemaking"
HANDOFF_ARTIFACT_ID = "sensemaking_first_use_handoff"
HANDOFF_SCHEMA_VERSION = 1
_MAX_TOP_LEVEL = 40

_ENTRY_DOCUMENTS = (
    "AGENTS.md",
    "CLAUDE.md",
    "CONTEXT.md",
    "README.md",
    "STATUS.md",
    "GETTING_STARTED.md",
    "docs/README.md",
    "docs/product-strategy.md",
)
_MANIFESTS = (
    "pyproject.toml",
    "setup.py",
    "setup.cfg",
    "package.json",
    "requirements.txt",
    "Cargo.toml",
    "go.mod",
    "Makefile",
    "justfile",
)
_LIMITS = (
    "The handoff projects paths, install metadata and selected receipt history; it does not analyze repository semantics.",
    "Installed-Skill currency compares the copied tree with package source or the install record; it does not show what a harness loaded or will load.",
    "Receipt validation checks representation and current path references, not semantic correctness, applicability or authority.",
    "Projected responsibility verification results are authored historical claims; handoff does not rerun checks or establish current verification.",
    "Continuity inventories describe the working tree, not a committed snapshot or a complete strategic model.",
    "Detached proposal and historical JSON inventories are path hints, not validation, review state, relevance or unresolved work. No proposal contents are read.",
    "The generated prompt must be executed by a capable agent with repository access and its own authority.",
    "A stale or unrecorded Skill may differ from the package; resolve the actual source before consequential use.",
    "No semantic truth, decision authority or action authorization is established.",
)


def _candidate_roots(target: Path, harness: str | None) -> list[tuple[str, str, Path]]:
    adapters = (
        [get_harness_adapter(harness)]
        if harness is not None
        else [get_harness_adapter(name) for name in CANONICAL_HARNESS_TARGETS]
    )
    roots: list[tuple[str, str, Path]] = []
    seen: set[tuple[str, str]] = set()
    for adapter in adapters:
        for scope, root in (
            ("user", adapter.user_skills_dir()),
            ("project", adapter.project_skills_dir(target)),
        ):
            key = (scope, str(root.resolve()))
            if key in seen:
                continue
            seen.add(key)
            roots.append((adapter.id, scope, root))
    return roots


def _package_source() -> tuple[Path | None, dict[str, str] | None]:
    try:
        source = get_package_skills_dir() / ENTRY_SKILL
    except (OSError, ValueError, SkillsSetupError):
        return None, None
    if not (source / "SKILL.md").is_file():
        return None, None
    return source, _skill_tree_fingerprint(source)


def _currency(
    skill_dir: Path, recorded: dict[str, Any] | None,
) -> tuple[str, str, dict[str, str], dict[str, Any]]:
    fingerprint = _skill_tree_fingerprint(skill_dir)
    digest = _tree_digest(fingerprint)
    source_path, source_fingerprint = _package_source()
    matches_source = bool(source_fingerprint is not None and fingerprint == source_fingerprint)
    source = {
        "available": source_path is not None,
        "path": str(source_path) if source_path is not None else None,
        "matches": matches_source,
    }
    if matches_source:
        return "CURRENT_WITH_PACKAGE_SOURCE", digest, fingerprint, source
    if source_path is not None:
        return "DIFFERS_FROM_PACKAGE_SOURCE", digest, fingerprint, source
    if recorded is None:
        return "UNRECORDED", digest, fingerprint, source
    if recorded.get("tree_sha256") == digest:
        return "CURRENT_AS_INSTALLED", digest, fingerprint, source
    return "LOCAL_CHANGES_OR_STALE", digest, fingerprint, source


def _skill_candidate(
    harness: str, scope: str, root: Path, *, explicit: bool = False,
) -> dict[str, Any] | None:
    skill_dir = root / ENTRY_SKILL
    skill_md = skill_dir / "SKILL.md"
    if not skill_dir.is_dir() or not skill_md.is_file():
        return None
    records, record_problem = load_install_record(root)
    recorded = records.get(ENTRY_SKILL)
    currency, digest, _, source = _currency(skill_dir, recorded)
    version_mismatch = bool(
        recorded
        and recorded.get("package_version")
        and recorded.get("package_version") != __version__
    )
    return {
        "entry_skill": ENTRY_SKILL,
        "harness": harness,
        "scope": scope,
        "explicit": explicit,
        "root": str(root),
        "skill_dir": str(skill_dir),
        "skill_md": str(skill_md),
        "record_path": str(root / INSTALL_RECORD_NAME),
        "record_problem": record_problem,
        "recorded": recorded,
        "currency": currency,
        "tree_sha256": digest,
        "source_comparison": source,
        "version_mismatch": version_mismatch,
        "recorded_tree_matches": bool(recorded and recorded.get("tree_sha256") == digest),
        "loaded_skill_identity": "NOT_OBSERVED",
    }


def _select_skill(
    target: Path, *, harness: str | None, scope: str, skill_path: Path | None,
) -> dict[str, Any]:
    if skill_path is not None:
        candidate_path = skill_path.expanduser().resolve()
        if candidate_path.is_file():
            skill_dir = candidate_path.parent
        else:
            skill_dir = candidate_path
        if skill_dir.name == ENTRY_SKILL and (skill_dir / "SKILL.md").is_file():
            root = skill_dir.parent
            candidate = _skill_candidate("explicit", "explicit", root, explicit=True)
            if candidate is not None:
                return candidate
        raise ValueError(
            "skill path must identify the installed using-sensemaking Skill directory "
            "or its SKILL.md file"
        )
    candidates = [
        candidate
        for harness_id, candidate_scope, root in _candidate_roots(target, harness)
        if (candidate := _skill_candidate(harness_id, candidate_scope, root)) is not None
        and (scope == "any" or candidate_scope == scope)
    ]
    if not candidates:
        raise ValueError(
            "no installed using-sensemaking Skill found. Run "
            "`sensemaking-skills setup-skills --target <harness>` first, or pass "
            "--skill-path."
        )
    if len(candidates) > 1:
        listing = "; ".join(
            f"{item['harness']}:{item['scope']}={item['skill_dir']}"
            for item in candidates
        )
        raise ValueError(
            "multiple installed using-sensemaking copies found: "
            f"{listing}. Pass --harness, --scope or --skill-path to select one."
        )
    return candidates[0]


def _git_facts(target: Path) -> dict[str, Any]:
    if not (target / ".git").exists():
        return {"is_git": False, "head": None, "branch": None, "error": None}
    try:
        head = guarded_git_text(target, "rev-parse", "HEAD").strip()
        branch = guarded_git_text(target, "rev-parse", "--abbrev-ref", "HEAD").strip()
        return {"is_git": True, "head": head, "branch": branch, "error": None}
    except (ValueError, OSError) as exc:
        return {"is_git": True, "head": None, "branch": None, "error": str(exc)[:240]}


def _target_inventory(target: Path, continuity: dict[str, Any]) -> dict[str, Any]:
    top_level: list[dict[str, str]] = []
    for item in sorted(target.iterdir(), key=lambda path: path.name):
        if item.name == ".git":
            continue
        if len(top_level) >= _MAX_TOP_LEVEL:
            break
        kind = "symlink" if item.is_symlink() else ("dir" if item.is_dir() else "file")
        top_level.append({"name": item.name, "kind": kind})
    knowledge = continuity["knowledge_files"]
    return {
        "top_level": top_level,
        "top_level_truncated": len(top_level) >= _MAX_TOP_LEVEL,
        "entry_documents": [
            name for name in _ENTRY_DOCUMENTS if (target / name).is_file()
        ],
        "manifests": [name for name in _MANIFESTS if (target / name).is_file()],
        "sensemaking_knowledge_present": knowledge["directory_status"] == "OBSERVED",
        "sensemaking_knowledge_file_count": knowledge["total"],
        "sensemaking_knowledge_directory_status": knowledge["directory_status"],
    }


def _committed_skill_comparison(skill: dict[str, Any], expected: str) -> str:
    """Compare the selected Skill to the requested commit's existing Git tree.

    Reuse setup-skills' tree comparison (regular non-executable Skill files).
    No history traversal, network access, installation, or loaded-byte claim.
    """
    source = skill["source_comparison"].get("path")
    skill_dir = Path(skill["skill_dir"])
    roots = [Path(source).parent] if source else []
    if skill_dir.parent.name == "skills" and skill_dir.parent not in roots:
        roots.append(skill_dir.parent)
    for root in roots:
        history = _CommittedSkillHistory.for_source(root)
        if history is None:
            continue
        try:
            commit = guarded_git_text(history.repo_root, "rev-parse", "--verify",
                                      expected + "^{commit}").strip()
            if commit != expected:
                continue
            tree = guarded_git_text(history.repo_root, "rev-parse", "--verify",
                                    expected + ":skills/" + ENTRY_SKILL).strip()
            exact = _git_tree_id(skill_dir, history.hash_name, lf_only=False)
            if exact == tree:
                return "MATCHES_COMMITTED_TREE"
            if _git_tree_id(skill_dir, history.hash_name, lf_only=True) == tree:
                return "LINE_ENDINGS_ONLY"
            return "DIFFERS_FROM_COMMITTED_TREE"
        except (ValueError, OSError, RuntimeError):
            continue
    return "NOT_AVAILABLE"


def _source_expectation(skill: dict[str, Any], expected: str | None) -> dict[str, Any]:
    """Keep requested commit, installed bytes and recorded provenance distinct."""
    recorded = skill.get("recorded") or {}
    recorded_commit = recorded.get("source_commit") if skill["recorded_tree_matches"] else None
    if not isinstance(recorded_commit, str) or not re.fullmatch(
            r"[0-9a-f]{40}|[0-9a-f]{64}", recorded_commit):
        recorded_commit = None
    comparison = _committed_skill_comparison(skill, expected) if expected else "NOT_REQUESTED"
    if expected is None:
        status = "NOT_REQUESTED"
    elif comparison != "NOT_AVAILABLE":
        status = comparison
    elif recorded_commit == expected:
        status = "MATCHES_INSTALL_RECORD"
    elif recorded_commit:
        status = "DIFFERS_FROM_INSTALL_RECORD"
    else:
        status = "NOT_ESTABLISHED"
    return {"expected_source_ref": expected, "status": status,
            "committed_tree_comparison": comparison,
            "scope": "ENTRY_SKILL_TREE_ONLY",
            "matching_tree_recorded_source_commit": recorded_commit,
            "loaded_skill_identity": "NOT_OBSERVED"}


def _prompt(
    skill: dict[str, Any], target: Path, output: Path, question: str | None,
    *, git: dict[str, Any], inventory: dict[str, Any],
    continuity: dict[str, Any], source_expectation: dict[str, Any],
) -> str:
    asked = (question or "").strip() or (
        "Perform a bounded repository orientation and identify the most "
        "consequential open question worth pursuing."
    )
    lines = [
        f"Use the installed Sensemaking entrypoint Skill at {skill['skill_md']}.",
        "Verify actual loaded Skill identity where the host exposes it; otherwise disclose unknown.",
        f"Target repository: {target}",
    ]
    if git.get("head"):
        lines.append(f"Target HEAD (working-tree overlay not indexed): {git['head']}")
    if source_expectation["expected_source_ref"]:
        lines.append(f"Requested Skill source: {source_expectation['expected_source_ref']}")
        lines.append(f"Entry-Skill comparison only: {source_expectation['status']}")
    lines.extend([
        f"Output directory: {output}",
        f"Question: {asked}",
        "",
    ])
    entry_documents = inventory.get("entry_documents") or []
    if entry_documents:
        lines.append("Start with these entry documents: " + ", ".join(entry_documents))
    manifests = inventory.get("manifests") or []
    if manifests:
        lines.append("Manifests: " + ", ".join(manifests))
    top_level = [
        item["name"] for item in (inventory.get("top_level") or [])
        if item.get("kind") in {"dir", "file"}
    ][:12]
    if top_level:
        lines.append("Top-level paths: " + ", ".join(top_level))
    lines.extend([
        "",
        "Follow the Skill's source-grounded workflow. Read the original sources;",
        "distinguish observed evidence, inferences, hypotheses and unresolved",
        "questions. If the question uses an ambiguous product term, resolve it",
        "from the named sources before broad exploration. Write only within the",
        "output directory or another location you are authorized to modify.",
        "Do not modify unrelated repositories. Do not claim semantic truth,",
        "decision authority or actions beyond what is authorized.",
    ])
    ci = continuity["inventory"]
    has_speculative_paths = bool(
        ci["detached_proposal_files"]["total"] or ci["historical_json_records"]["total"]
    )
    if (continuity["selected_receipts"] or ci["receipt_files"]["total"]
            or ci["knowledge_files"]["total"] or has_speculative_paths):
        lines.extend([
            "",
            f"Returning engagement: inspect the continuity section of {output / 'handoff.json'}.",
            "Read relevant original receipts and reviewed knowledge, recheck their",
            "currentness, then re-warrant the strategic direction and responsibility.",
            "A valid prior receipt is historical evidence, not today's instructions",
            "or permission. Invalid/unavailable receipts require source recovery;",
            "do not silently treat them as absent or rewrite immutable history.",
            "Use the receipt's evidence refs and unresolved blockers; verify them in",
            "current sources. A valid receipt may be irrelevant, incomplete or stale.",
            "Distinguish the receipt validator status from authored responsibility",
            "validation commands and PASS, FAIL or NOT_RUN results. Inspect their",
            "original evidence and current applicability; handoff does not rerun them.",
            "If a consequential selection or stop depends on prior completion, compare",
            "the authored goal, actual responsibilities, stop rationale and claim ceiling",
            "against today's delegation. A completed local increment is not mission closure.",
            "When available, use the existing semantic workspace-query search for",
            "the current question (source-pinned lexical candidates, not relevance proof),",
            "and product-outline or method context only when decision-relevant.",
        ])
    if ci["receipt_files"].get("path_selection") == "LEXICOGRAPHIC_ENDS":
        lines.extend([
            "",
            "Receipt path hints show both filename-order ends within the path budget;",
            "middle paths are omitted. Filename order is not chronology of updates,",
            "relevance, strategic precedence or authority. Enumerate the directory",
            "directly if the relevant path is missing; select receipts explicitly.",
        ])
    if has_speculative_paths:
        lines.extend([
            "",
            "The continuity inventory also lists detached proposal paths and historical",
            "JSON records separately from the knowledge directory. Inspect only records",
            "relevant to the current choice; a historical JSON file may be a synthesis",
            "input, an already integrated draft or unrelated evidence. A filename does",
            "not establish review status, unresolved work or authority. Compare original",
            "evidence and current reviewed knowledge before reusing a candidate.",
            "If an actual detached pack warrants review, use the existing read-only",
            "knowledge-proposal-check with an explicit new --destination, then follow",
            "the ordinary authorized review and clean-commit build contract. Do not",
            "automatically copy, promote, execute or select a candidate.",
        ])
    lines.extend([
        "For explicitly sustained development, load the long-horizon strategic",
        "development reference; establish or reuse adequate semantic knowledge",
        "and explicit knowledge-edit authority. Keep clear isolated work light.",
    ])
    if source_expectation["status"] not in {
        "NOT_REQUESTED", "MATCHES_INSTALL_RECORD", "MATCHES_COMMITTED_TREE",
    }:
        lines.extend([
            "",
            "The requested Skill source identity is not established for this copy.",
            "Resolve the intended source against actual installed/loaded content",
            "before consequential use. An explicit pinned source load is an option;",
            "do not replace a shared installation without authorization.",
        ])
    if skill["currency"] not in {
        "CURRENT_AS_INSTALLED", "CURRENT_WITH_PACKAGE_SOURCE",
    }:
        lines.extend([
            "",
            f"Note: the installed Skill is reported as {skill['currency']}. "
            "Verify the selected copy and use setup-skills with its actual harness "
            "and scope, or explicitly load the intended source. Review divergent "
            "content before updating; do not modify another active installation.",
        ])
    return "\n".join(lines)


def _render_markdown(payload: dict[str, Any]) -> str:
    skill = payload["installed_skill"]
    target = payload["target"]
    inventory = target["inventory"]
    lines = [
        "# Sensemaking first-use handoff",
        "",
        f"Generated: {payload['generated_at']}",
        "",
        "## Target",
        "",
        f"- Path: `{target['path']}`",
        f"- Git: {'yes' if target['git']['is_git'] else 'no'}",
    ]
    if target["git"]["head"]:
        lines.append(f"- HEAD: `{target['git']['head']}`")
    if target["git"]["branch"]:
        lines.append(f"- Branch: `{target['git']['branch']}`")
    if target["git"]["error"]:
        lines.append(f"- Git note: {target['git']['error']}")
    lines.extend([
        "",
        "Entry documents: " + (
            ", ".join(f"`{name}`" for name in inventory["entry_documents"])
            or "none detected"
        ),
        "",
        "Manifests: " + (
            ", ".join(f"`{name}`" for name in inventory["manifests"])
            or "none detected"
        ),
        "",
        f"Sensemaking knowledge pack: {'present' if inventory['sensemaking_knowledge_present'] else 'absent'}",
        "",
        "## Installed Skill",
        "",
        f"- Path: `{skill['skill_md']}`",
        f"- Harness: `{skill['harness']}` ({skill['scope']})",
        f"- Currency: `{skill['currency']}`",
        f"- Package version: `{__version__}`",
    ])
    runtime = payload["generator_identity"]
    expectation = payload["source_expectation"]
    lines.extend([
        f"- CLI Python executable: `{runtime['python_executable']}`",
        *[f"- {line}" for line in runtime["code_provenance"]],
        f"- Requested Skill source: `{expectation['expected_source_ref'] or 'not specified'}`",
        f"- Requested-source comparison: `{expectation['status']}`",
        "- Loaded Skill identity: not observed by this CLI",
    ])
    recorded = skill.get("recorded") or {}
    if recorded.get("package_version"):
        lines.append(f"- Recorded package version: `{recorded['package_version']}`")
    if recorded.get("source_commit"):
        lines.append(f"- Recorded source commit: `{recorded['source_commit']}`")
    if skill.get("record_problem"):
        lines.append(f"- Install record note: {skill['record_problem']}")
    source = skill.get("source_comparison") or {}
    if source.get("available"):
        lines.append(
            f"- Package source comparison: {'matches' if source.get('matches') else 'differs'} "
            f"(`{source.get('path')}`)"
        )
    continuity = payload["continuity"]
    ci = continuity["inventory"]
    lines.extend([
        "",
        "## Returning-engagement evidence",
        "",
        "Working-tree paths (not a currentness or adequacy judgment):",
        f"- Knowledge-directory JSON: {ci['knowledge_files']['total']} files",
        f"- Detached proposal JSON: {ci['detached_proposal_files']['total']} files",
        f"- Historical JSON records: {ci['historical_json_records']['total']} files",
        "- Speculative-record review state: NOT_ASSESSED (paths only; not a pending-work list)",
        f"- Receipt files: {ci['receipt_files']['total']} files",
        "- Governing/strategic paths: " + (", ".join(ci["governing_paths"]) or "none detected"),
        "See handoff.json for bounded path lists and omissions.",
        "Explicit selected-receipt validation describes the current target, not historical truth.",
    ])
    if ci["receipt_files"].get("path_selection") == "LEXICOGRAPHIC_ENDS":
        lines.append(
            "- Receipt path hints: first and last 20 in filename order; "
            f"{ci['receipt_files']['omitted_count']} middle paths omitted. "
            "No relevance or chronology judgment."
        )
    for receipt in continuity["selected_receipts"]:
        lines.append(f"- Selected receipt: `{receipt['path']}` ({receipt['validation']})")
    lines.extend([
        "",
        "## How to use",
        "",
        "1. Open the target repository in your coding-agent harness.",
        "2. Make the installed Skill discoverable, or point the agent at the",
        "   `SKILL.md` path above.",
        "3. Give the agent the prompt below, or point it at this file.",
        "",
        "## Prompt",
        "",
        "```text",
        payload["prompt"],
        "```",
        "",
        "## Limits",
        "",
    ])
    lines.extend(f"- {limit}" for limit in payload["limits"])
    lines.append("")
    return "\n".join(lines)


def prepare_handoff(
    repo: str | Path,
    output: str | Path = "artifacts/sensemaking-handoff",
    *,
    question: str | None = None,
    harness: str | None = None,
    scope: str = "any",
    skill_path: str | Path | None = None,
    expected_source_ref: str | None = None,
    resume_from: tuple[str, ...] = (),
) -> dict[str, Any]:
    """Write a verified handoff and return its payload."""

    if expected_source_ref is not None and not re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", expected_source_ref):
        raise ValueError("expected source ref must be a full lowercase Git commit ID")
    if scope not in {"any", "user", "project"}:
        raise ValueError("scope must be any, user or project")
    target = Path(repo).expanduser().resolve()
    if not target.is_dir():
        raise ValueError(f"target repository is not a directory: {target}")
    output_dir = Path(output).expanduser().resolve()
    if output_dir.exists() and not output_dir.is_dir():
        raise ValueError(f"output path is not a directory: {output_dir}")
    skill = _select_skill(
        target,
        harness=harness,
        scope=scope,
        skill_path=Path(skill_path) if skill_path is not None else None,
    )
    continuity = {"inventory": continuity_inventory(target),
                  "selected_receipts": selected_receipts(target, resume_from)}
    output_dir.mkdir(parents=True, exist_ok=True)
    for name in ("handoff.json", "handoff.md"):
        destination = output_dir / name
        if destination.is_symlink() or (destination.exists() and not destination.is_file()):
            raise ValueError(f"handoff output is not a regular file: {destination}")
    payload: dict[str, Any] = {
        "artifact_id": HANDOFF_ARTIFACT_ID,
        "schema_version": HANDOFF_SCHEMA_VERSION,
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "generator_version": __version__,
        "generator_identity": {"python_executable": sys.executable, "code_provenance": code_provenance_lines()},
        "source_expectation": _source_expectation(skill, expected_source_ref),
        "continuity": continuity,
        "target": {
            "path": str(target),
            "git": _git_facts(target),
            "inventory": _target_inventory(target, continuity["inventory"]),
        },
        "installed_skill": skill,
        "output": {
            "directory": str(output_dir),
            "json": str(output_dir / "handoff.json"),
            "markdown": str(output_dir / "handoff.md"),
        },
        "question": (question or "").strip() or None,
        "analysis_performed": False,
        "semantic_truth_established": False,
        "action_authorized": False,
        "limits": list(_LIMITS),
    }
    payload["prompt"] = _prompt(
        skill, target, output_dir, question,
        git=payload["target"]["git"], inventory=payload["target"]["inventory"],
        continuity=continuity, source_expectation=payload["source_expectation"],
    )
    (output_dir / "handoff.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    (output_dir / "handoff.md").write_text(
        _render_markdown(payload), encoding="utf-8", newline="\n",
    )
    return payload
