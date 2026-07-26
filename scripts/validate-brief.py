import os
import sys
import re
import json
import argparse
from datetime import datetime, timezone
from typing import TypedDict, Any

import yaml

from _validator_utils import format_error, extract_sections, load_weakness_types, load_workflow_registry

# Stable error codes
BRIEF_FILE_NOT_FOUND = "BRIEF_FILE_NOT_FOUND"
MISSING_EVIDENCE_EXCERPTS = "MISSING_EVIDENCE_EXCERPTS"
EVIDENCE_EXCERPT_FIELD = "EVIDENCE_EXCERPT_FIELD"
HALLUCINATED_FILE = "HALLUCINATED_FILE"
INVALID_LINE_FORMAT = "INVALID_LINE_FORMAT"
PARSING_ERROR = "PARSING_ERROR"
MISSING_WORKFLOW_ID = "MISSING_WORKFLOW_ID"
HALLUCINATED_WORKFLOW_ID = "HALLUCINATED_WORKFLOW_ID"
MISSING_HANDOFF_BLOCK = "MISSING_HANDOFF_BLOCK"
REGISTRY_NOT_FOUND = "REGISTRY_NOT_FOUND"
NO_LOGIC_TRACE = "NO_LOGIC_TRACE"
NO_EVIDENCE_FILE_CITATIONS = "NO_EVIDENCE_FILE_CITATIONS"

# Structured weakness-type contract (issue #80). UNKNOWN_WEAKNESS_TYPE (the old
# blocking case-insensitive prose-substring check) is retired -- it wrongly
# rejected a legitimate brief in PR #78 because taxonomy is required metadata,
# not a structural blocker (D2/D3/D4 in the ratified owner decision package).
WEAKNESS_TYPE_MISSING = "WEAKNESS_TYPE_MISSING"
WEAKNESS_TYPE_UNKNOWN = "WEAKNESS_TYPE_UNKNOWN"
WEAKNESS_TYPE_OTHER_NO_EXPLANATION = "WEAKNESS_TYPE_OTHER_NO_EXPLANATION"
WEAKNESS_TYPE_MALFORMED = "WEAKNESS_TYPE_MALFORMED"
WEAKNESS_TYPE_PROSE_MISMATCH = "WEAKNESS_TYPE_PROSE_MISMATCH"
HIGH_RISK_CLAIM_NEEDS_SUBSTANTIVE_AUDIT = "HIGH_RISK_CLAIM_NEEDS_SUBSTANTIVE_AUDIT"

# Deterministic evidence-quote grounding (issue #80).
EVIDENCE_QUOTE_NOT_FOUND = "EVIDENCE_QUOTE_NOT_FOUND"

FILE_CITATION_RE = re.compile(
    r"`?[\w./\\-]+\.(?:md|py|yaml|yml|toml|txt)(?::\d+)?`?",
    re.IGNORECASE,
)

# High-risk weakness-type categories requiring a substantive human audit
# before final approval (D5). This warning never proves an audit happened
# and never judges correctness -- it only flags that one is required.
HIGH_RISK_WEAKNESS_TYPES = {"Safety Gaps", "Ghost Features"}

# Fixed, documented window (in lines) searched around a cited line range when
# grounding an evidence_excerpts quote. Narrow and deterministic by design --
# no semantic/paraphrase matching, no whole-repo fallback search.
QUOTE_GROUNDING_WINDOW = 3


class ValidationError(TypedDict, total=False):
    """Structured validation error with all metadata for JSON output."""
    error_id: str  # e.g., repository_sensemaking_brief.primary_fog_type.missing_field
    error_type: str  # missing_field, unknown_value, semantic_conflict, logic_error, type_error
    field: str | None
    current_value: Any
    message: str
    suggested_fixes: list[str]
    reference: str
    severity: str  # "error" (blocking, default) or "warning" (non-blocking)


class ValidationResult(TypedDict):
    """Complete validation result with metadata."""
    valid: bool
    artifact_id: str
    artifact_path: str
    validator: str
    errors: list[ValidationError]
    validation_timestamp: str


def _code_error(
    code: str,
    message: str,
    field: str | None = None,
    severity: str = "error",
) -> "ValidationError":
    """Build a ValidationError whose message is prefixed with a stable error code.

    Used for the structural/content checks below (logic trace, evidence
    citations, weakness type, excerpt fields, hallucinated files/workflow
    IDs) which report a fixed vocabulary of codes rather than simple field
    presence.

    ``severity`` defaults to "error" (blocking, invalidates the artifact).
    Pass ``severity="warning"`` for required-but-non-blocking metadata (e.g.
    the weakness-type taxonomy, per D2) -- warnings never flip ``valid`` to
    False and never cause a non-zero validator exit code.
    """
    return {
        "error_type": "logic_error",
        "field": field,
        "current_value": None,
        "message": f"{code}: {message}",
        "suggested_fixes": [],
        "reference": "skills/workflow-planner/references/artifact-contracts.yaml",
        "severity": severity,
    }


def _is_blocking(error: "ValidationError") -> bool:
    """True if this error should invalidate the artifact / cause non-zero exit.

    Missing ``severity`` (e.g. the Phase-1 required-field checks below, which
    predate this field) defaults to "error" -- fully backward compatible.
    """
    return error.get("severity", "error") == "error"


def _is_large_artifact(content: str) -> bool:
    """Heuristic: artifacts >= 100 lines are 'large' and get relaxed validation.

    Large artifacts (like repository_sensemaking_brief at ~350 lines) reliably
    contain all substantive content but organize it under their own section
    headings rather than the rigid contract names. The content is validated by
    downstream consumers semantically, so structural formatting checks become
    guidance-level warnings.
    """
    return content.count("\n") + 1 >= 100


def _parse_artifact_data(content: str) -> dict[str, Any] | None:
    """Try to extract machine-readable artifact data from YAML blocks.

    Returns dict if found, None otherwise.
    """
    # Look for machine-readable handoff YAML
    handoff_match = re.search(
        r"## 13\. Machine-readable handoff\s+```yaml\s+(.*?)\s+```",
        content,
        re.DOTALL | re.IGNORECASE,
    )

    if not handoff_match:
        # Try last YAML block for large artifacts
        yaml_blocks = re.findall(r"```yaml\s+(.*?)\s+```", content, re.DOTALL)
        if yaml_blocks:
            try:
                return yaml.safe_load(yaml_blocks[-1])
            except Exception:
                return None
        return None

    try:
        return yaml.safe_load(handoff_match.group(1))
    except Exception:
        return None


def _normalize_for_grounding(text: str) -> str:
    """Narrow, documented normalization for quote grounding.

    Only two transforms, both deliberately conservative to avoid false
    positives: (1) normalize line endings, (2) collapse runs of horizontal
    whitespace to a single space. No paraphrase/semantic matching.
    """
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[^\S\n]+", " ", text)
    return text.strip()


def _parse_line_range(lines_value: str) -> tuple[int, int] | None:
    """Parse an 'Lx', 'Lx-Ly', '18', or '25-30' style lines value."""
    match = re.match(r"^L?(\d+)(?:-L?(\d+))?$", lines_value.strip())
    if not match:
        return None
    start = int(match.group(1))
    end = int(match.group(2)) if match.group(2) else start
    if end < start:
        start, end = end, start
    return start, end


def _quote_found_near(file_path: str, lines_value: str, quote: str) -> tuple[bool, str]:
    """Check whether ``quote`` exists within a fixed window around the cited
    line range in ``file_path``.

    Deterministic only: exact (post-normalization) substring match within a
    documented +/- QUOTE_GROUNDING_WINDOW-line window around the cited range.
    No semantic/paraphrase matching, no whole-repository fallback search.

    Returns (found, detail_message). ``detail_message`` always states the
    actual window searched so a human can verify the match location.
    """
    rng = _parse_line_range(lines_value)
    try:
        with open(file_path, encoding="utf-8") as f:
            file_lines = f.read().replace("\r\n", "\n").replace("\r", "\n").split("\n")
    except Exception as e:
        return False, f"(could not read file: {e})"

    if rng is None:
        return False, "(cited line range could not be parsed)"

    start, end = rng
    total = len(file_lines)
    win_start = max(1, start - QUOTE_GROUNDING_WINDOW)
    win_end = min(total, end + QUOTE_GROUNDING_WINDOW)
    if win_start > total:
        return False, f"(cited line range {start}-{end} is out of bounds; file has {total} lines)"

    window_text = "\n".join(file_lines[win_start - 1:win_end])
    norm_window = _normalize_for_grounding(window_text)
    norm_quote = _normalize_for_grounding(quote)

    if not norm_quote:
        return False, "(quote is empty after normalization)"

    if norm_quote in norm_window:
        return True, f"(matched within lines {win_start}-{win_end})"
    return False, f"(searched lines {win_start}-{win_end}, no match)"


def validate_brief(
    artifact_path: str,
    repo_root: str = ".",
    target_repo: str | None = None,
) -> list[ValidationError]:
    """Validate a repository sensemaking brief and return structured errors.

    Args:
        artifact_path: Path to the brief .md file.
        repo_root: Root of the sensemaking-skills framework repo (used for
            resolving artifact-contracts, weakness-types, and workflow registry).
        target_repo: Root of the repository the brief is ABOUT. Cited evidence
            files are resolved against this root when provided. Falls back to
            repo_root when not given (preserves single-repo behavior exactly).

    Returns a list of ValidationError dicts. Empty list means validation passed.
    """
    errors: list[ValidationError] = []
    # Citation existence checks resolve against target_repo (the repo the brief
    # is about) when supplied; otherwise fall back to repo_root, preserving
    # existing single-repo/internal-proof behavior byte-for-byte.
    citation_root = target_repo if target_repo else repo_root

    if not os.path.exists(artifact_path):
        errors.append({
            "error_type": "missing_field",
            "field": "artifact",
            "current_value": None,
            "message": f"Brief file not found: {artifact_path}",
            "suggested_fixes": [f"Ensure brief exists at: {artifact_path}"],
            "reference": "skills/workflow-planner/references/artifact-contracts.yaml"
        })
        return errors

    with open(artifact_path, encoding="utf-8") as f:
        content = f.read()

    sections = extract_sections(content, normalize_hyphens=False)
    weakness_types = load_weakness_types(repo_root)
    large = _is_large_artifact(content)
    artifact_data = _parse_artifact_data(content)

    # --- PHASE 1 REQUIRED FIELD CHECKS ---
    # Check for required machine fields per artifact-contracts.yaml
    # Required: artifact_id, primary_fog_type, evidence, recommended_workflow_id, created_at, immutable

    if artifact_data:
        # Check primary_fog_type
        if "primary_fog_type" not in artifact_data:
            errors.append({
                "error_id": "repository_sensemaking_brief.primary_fog_type.missing_field",
                "error_type": "missing_field",
                "field": "primary_fog_type",
                "current_value": None,
                "message": "Required field 'primary_fog_type' is missing.",
                "suggested_fixes": [
                    "Add primary_fog_type: product_fog",
                    "Add primary_fog_type: ui_fog",
                    "Add primary_fog_type: docs_fog",
                    "Add primary_fog_type: architecture_fog"
                ],
                "reference": "skills/workflow-planner/references/artifact-contracts.yaml"
            })
        else:
            # Validate the value is an allowed fog type
            fog_type = artifact_data.get("primary_fog_type")
            allowed_fog_types = ["product_fog", "ui_fog", "docs_fog", "architecture_fog"]
            if fog_type not in allowed_fog_types:
                errors.append({
                    "error_id": "repository_sensemaking_brief.primary_fog_type.unknown_value",
                    "error_type": "unknown_value",
                    "field": "primary_fog_type",
                    "current_value": fog_type,
                    "message": f"Field 'primary_fog_type' has value '{fog_type}', which is not recognized.",
                    "suggested_fixes": [f"Change to: primary_fog_type: {ft}" for ft in allowed_fog_types],
                    "reference": "docs/adr/0007-soft-context-routing.md"
                })

        # Check evidence (should be non-empty list)
        if "evidence" not in artifact_data:
            errors.append({
                "error_id": "repository_sensemaking_brief.evidence.missing_field",
                "error_type": "missing_field",
                "field": "evidence",
                "current_value": None,
                "message": "Required field 'evidence' is missing.",
                "suggested_fixes": [
                    "Add evidence as a list of file-level citations",
                    "Example: evidence: ['README.md (lines 5-12): vague feature requirements', ...]"
                ],
                "reference": "skills/workflow-planner/references/artifact-contracts.yaml"
            })
        else:
            evidence = artifact_data.get("evidence")
            if not isinstance(evidence, list):
                errors.append({
                    "error_id": "repository_sensemaking_brief.evidence.type_error",
                    "error_type": "type_error",
                    "field": "evidence",
                    "current_value": evidence,
                    "message": f"Field 'evidence' should be a list, but got {type(evidence).__name__}.",
                    "suggested_fixes": ["Convert evidence to an array of strings"],
                    "reference": "skills/workflow-planner/references/artifact-contracts.yaml"
                })
            elif len(evidence) == 0:
                errors.append({
                    "error_id": "repository_sensemaking_brief.evidence.logic_error",
                    "error_type": "logic_error",
                    "field": "evidence",
                    "current_value": [],
                    "message": "Evidence list is empty. Cannot verify fog type classification is grounded in analysis.",
                    "suggested_fixes": [
                        "Add file-level evidence (e.g., 'README.md: feature list is vague')",
                        "Add architectural evidence (e.g., 'tight coupling in data layer')"
                    ],
                    "reference": "docs/adr/0003-artifact-composition-pattern.md"
                })

        # Check recommended_workflow_id
        if "recommended_workflow_id" not in artifact_data:
            if not large:  # Large artifacts can skip this
                errors.append({
                    "error_id": "repository_sensemaking_brief.recommended_workflow_id.missing_field",
                    "error_type": "missing_field",
                    "field": "recommended_workflow_id",
                    "current_value": None,
                    "message": "Required field 'recommended_workflow_id' is missing.",
                    "suggested_fixes": [
                        "Add recommended_workflow_id: product-implementation-workflow",
                        "Add recommended_workflow_id: ui-implementation-workflow",
                        "Add recommended_workflow_id: docs-implementation-workflow",
                        "Add recommended_workflow_id: architecture-implementation-workflow"
                    ],
                    "reference": "skills/workflow-planner/references/artifact-contracts.yaml"
                })
        else:
            workflow_id = artifact_data.get("recommended_workflow_id")
            registry = load_workflow_registry(repo_root)
            if registry is not None:
                valid_ids = {w["id"] for w in registry.get("workflows", [])}
                if workflow_id not in valid_ids:
                    errors.append({
                        "error_id": "repository_sensemaking_brief.recommended_workflow_id.unknown_value",
                        "error_type": "unknown_value",
                        "field": "recommended_workflow_id",
                        "current_value": workflow_id,
                        "message": f"HALLUCINATED_WORKFLOW_ID: Recommended workflow ID '{workflow_id}' not found in registry.",
                        "suggested_fixes": [
                            "Check available workflows in workflow-registry.yaml",
                            "Ensure workflow ID matches exactly (case-sensitive)"
                        ],
                        "reference": "skills/workflow-planner/references/artifact-contracts.yaml"
                    })

    # --- STRUCTURAL / CONTENT CHECKS ---

    # 1. Logic trace reasoning marker
    if "logic trace" not in content.lower():
        errors.append(_code_error(NO_LOGIC_TRACE, "Brief does not include a logic trace showing diagnostic reasoning."))

    # 2. File-level citations in the Evidence section
    evidence_section = sections.get("evidence", "")
    if evidence_section and not FILE_CITATION_RE.search(evidence_section):
        errors.append(_code_error(NO_EVIDENCE_FILE_CITATIONS, "Evidence section has no file-level citations (e.g., path/to/file.py:42)."))

    # 3. Structured weakness_type field (Section 13 machine YAML). Taxonomy is
    #    required metadata but non-blocking (D2): missing/unrecognized/prose-
    #    mismatched values are warnings only, never invalidate the brief.
    #    Only a malformed field (wrong YAML type) is blocking, since that is a
    #    structural defect rather than a taxonomy-completeness gap. Enum is
    #    sourced from weakness_types (load_weakness_types()), the same loader
    #    scripts/skill_executor.py's get_allowed_weakness_types() uses, so the
    #    two can never independently drift.
    weakest_boundary = sections.get("weakest boundary", "")
    if artifact_data is not None:
        # A present-but-empty key (e.g. an untouched "weakness_type:  # ..."
        # skeleton placeholder, which YAML parses as None) is treated the
        # same as an absent key -- both are "not yet supplied", a warning,
        # not a structural defect. Only a genuinely wrong YAML *type* (list,
        # int, bool, ...) is WEAKNESS_TYPE_MALFORMED.
        if "weakness_type" not in artifact_data or artifact_data.get("weakness_type") is None:
            errors.append(_code_error(
                WEAKNESS_TYPE_MISSING,
                "Section 13 has no structured 'weakness_type' field. This does not "
                "invalidate the brief, but the taxonomy is required metadata -- "
                f"add one. Known types: {', '.join(weakness_types)}, Other.",
                field="weakness_type",
                severity="warning",
            ))
        else:
            weakness_type = artifact_data.get("weakness_type")
            if not isinstance(weakness_type, str):
                errors.append(_code_error(
                    WEAKNESS_TYPE_MALFORMED,
                    f"'weakness_type' must be a string, got {type(weakness_type).__name__}: {weakness_type!r}",
                    field="weakness_type",
                    severity="error",
                ))
            else:
                allowed_weakness_types = set(weakness_types) | {"Other"}
                if weakness_type == "Other":
                    explanation = artifact_data.get("weakness_type_explanation")
                    if not explanation or not str(explanation).strip():
                        errors.append(_code_error(
                            WEAKNESS_TYPE_OTHER_NO_EXPLANATION,
                            "weakness_type is 'Other' but 'weakness_type_explanation' is "
                            "missing or empty (D4). This does not invalidate the brief "
                            "structurally, but final human approval must not be granted "
                            "until an explanation is added.",
                            field="weakness_type_explanation",
                            severity="warning",
                        ))
                elif weakness_type not in allowed_weakness_types:
                    errors.append(_code_error(
                        WEAKNESS_TYPE_UNKNOWN,
                        f"'weakness_type' value '{weakness_type}' is not a recognized "
                        f"taxonomy term. Known types: {', '.join(weakness_types)}, Other.",
                        field="weakness_type",
                        severity="warning",
                    ))

                if weakness_type in HIGH_RISK_WEAKNESS_TYPES:
                    errors.append(_code_error(
                        HIGH_RISK_CLAIM_NEEDS_SUBSTANTIVE_AUDIT,
                        f"weakness_type is '{weakness_type}', a high-risk claim category "
                        "(D5) requiring a substantive human audit before final approval. "
                        "This warning does not confirm an audit occurred and does not "
                        "judge correctness -- it only flags that one is required.",
                        field="weakness_type",
                        severity="warning",
                    ))

                if weakest_boundary and weakness_type.lower() not in weakest_boundary.lower():
                    errors.append(_code_error(
                        WEAKNESS_TYPE_PROSE_MISMATCH,
                        f"Structured weakness_type ('{weakness_type}') does not appear in "
                        "the Section 6 'Weakest boundary' prose. Prose may legitimately "
                        "add nuance or name an additional term -- the structured field is "
                        "authoritative for anything machine-facing; this is informational "
                        "only.",
                        field="weakness_type",
                        severity="warning",
                    ))

    # 4. evidence_excerpts YAML block: presence + per-excerpt field checks
    evidence_match = re.search(r"```yaml\s+(evidence_excerpts:.*?)\s+```", content, re.DOTALL | re.IGNORECASE)
    if not evidence_match:
        evidence_match = re.search(r"```yaml\s+(- file:.*?)\s+```", content, re.DOTALL)

    if not evidence_match and large:
        pass  # Large briefs often present evidence in a markdown table instead.
    elif not evidence_match:
        errors.append(_code_error(MISSING_EVIDENCE_EXCERPTS, "Missing or malformed YAML block for evidence_excerpts."))
    else:
        try:
            data = yaml.safe_load(evidence_match.group(1))
            if isinstance(data, dict):
                excerpts = data.get("evidence_excerpts", [])
            elif isinstance(data, list):
                excerpts = data
            else:
                errors.append(_code_error(PARSING_ERROR, "evidence_excerpts block must be a list or dict containing 'evidence_excerpts'."))
                excerpts = []

            if not excerpts:
                errors.append(_code_error(EVIDENCE_EXCERPT_FIELD, "Evidence excerpts list is empty."))

            for i, exc in enumerate(excerpts):
                for field in ["file", "lines", "quote", "supports_claim"]:
                    if field not in exc:
                        errors.append(_code_error(EVIDENCE_EXCERPT_FIELD, f"Excerpt[{i}] missing required field: {field}"))

                file_path = exc.get("file")
                if file_path:
                    if file_path.startswith("file:///"):
                        errors.append(_code_error(HALLUCINATED_FILE, f"Excerpt[{i}] uses absolute file:/// path: {file_path}"))
                    else:
                        full_path = os.path.join(citation_root, file_path)
                        if not os.path.exists(full_path):
                            errors.append(_code_error(HALLUCINATED_FILE, f"Excerpt[{i}] references non-existent file: {file_path}"))

                lines = exc.get("lines")
                # Accept both the Lx / Lx-Ly form and bare line numbers (18, 25-30).
                lines_valid = lines is not None and re.match(r"^L?\d+(?:-L?\d+)?$", str(lines).strip())
                if lines is not None and not lines_valid:
                    errors.append(_code_error(
                        INVALID_LINE_FORMAT,
                        f"Excerpt[{i}] has invalid lines format: {lines} "
                        f"(expected a line number or range, e.g. L18, 18, L25-L30, or 25-30)",
                    ))

                # Deterministic quote grounding (issue #80): the cited quote
                # must actually exist at (or within a small fixed window
                # around) the cited file/line location. Only runs when the
                # file exists and the line syntax is valid, so this never
                # duplicates HALLUCINATED_FILE / INVALID_LINE_FORMAT.
                quote = exc.get("quote")
                if (
                    file_path
                    and not file_path.startswith("file:///")
                    and lines_valid
                    and quote
                ):
                    full_path = os.path.join(citation_root, file_path)
                    if os.path.exists(full_path):
                        found, detail = _quote_found_near(full_path, str(lines), str(quote))
                        if not found:
                            errors.append(_code_error(
                                EVIDENCE_QUOTE_NOT_FOUND,
                                f"Excerpt[{i}] quote not found in {file_path} {detail}. "
                                "The quote must exist verbatim (after line-ending "
                                "normalization and optional horizontal-whitespace "
                                f"collapsing) within {QUOTE_GROUNDING_WINDOW} lines of "
                                f"the cited range '{lines}'.",
                            ))
        except Exception as e:
            errors.append(_code_error(PARSING_ERROR, f"Failed to parse evidence YAML: {e}"))

    # 5. handoff / workflow ID (legacy Section 13 block; artifact_data already covers
    # the Phase-1 recommended_workflow_id check above for the current schema, this
    # covers the large-artifact fallback path and hallucinated-ID detection)
    if artifact_data is not None:
        workflow_id = artifact_data.get("recommended_workflow_id")
        if not workflow_id and not large:
            errors.append(_code_error(MISSING_WORKFLOW_ID, "Handoff missing 'recommended_workflow_id'."))
    elif not large:
        errors.append(_code_error(MISSING_HANDOFF_BLOCK, "Missing 'Machine-readable handoff' YAML block."))

    return errors


def validation_result_to_json(
    artifact_path: str,
    errors: list[ValidationError],
) -> str:
    """Convert validation result to JSON format with multi-error schema.

    ``valid`` is False only if a blocking (severity="error", the default)
    entry is present. Non-blocking warnings (e.g. WEAKNESS_TYPE_* taxonomy
    codes) never flip ``valid`` to False (D2).
    """
    result: ValidationResult = {
        "valid": not any(_is_blocking(e) for e in errors),
        "artifact_id": "repository_sensemaking_brief",
        "artifact_path": os.path.abspath(artifact_path),
        "validator": "validate-brief.py",
        "errors": errors,
        "validation_timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    }

    return json.dumps(result, indent=2, default=str)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Specialized validator for repository sensemaking brief.")
    parser.add_argument("artifact_path", nargs="?", help="Path to the brief .md file")
    parser.add_argument("--repo-root", default=".", help="Root of the repository for file checks")
    parser.add_argument(
        "--target-repo",
        default=None,
        help=(
            "Root of the repository the brief is ABOUT, if different from "
            "--repo-root (external-repository runs). Evidence citations are "
            "resolved against this root when provided; falls back to --repo-root."
        ),
    )
    parser.add_argument("--json", action="store_true", help="Output JSON format")
    parser.add_argument("--list-codes", action="store_true", help="List all error codes and exit")
    args = parser.parse_args(argv)

    if args.list_codes:
        codes = [
            BRIEF_FILE_NOT_FOUND,
            PARSING_ERROR,
            MISSING_EVIDENCE_EXCERPTS,
            EVIDENCE_EXCERPT_FIELD,
            HALLUCINATED_FILE,
            INVALID_LINE_FORMAT,
            MISSING_WORKFLOW_ID,
            HALLUCINATED_WORKFLOW_ID,
            MISSING_HANDOFF_BLOCK,
            REGISTRY_NOT_FOUND,
            NO_LOGIC_TRACE,
            NO_EVIDENCE_FILE_CITATIONS,
            WEAKNESS_TYPE_MISSING,
            WEAKNESS_TYPE_UNKNOWN,
            WEAKNESS_TYPE_OTHER_NO_EXPLANATION,
            WEAKNESS_TYPE_MALFORMED,
            WEAKNESS_TYPE_PROSE_MISMATCH,
            HIGH_RISK_CLAIM_NEEDS_SUBSTANTIVE_AUDIT,
            EVIDENCE_QUOTE_NOT_FOUND,
        ]
        print("Stable error codes for brief validation:")
        for code in codes:
            print(f"  {code}")
        return 0

    if not args.artifact_path:
        parser.print_usage()
        return 1

    errors = validate_brief(args.artifact_path, args.repo_root, args.target_repo)
    blocking = [e for e in errors if _is_blocking(e)]

    if args.json:
        print(validation_result_to_json(args.artifact_path, errors))
        return 0 if not blocking else 1
    else:
        # Legacy prose output for backward compatibility
        if errors:
            for error in errors:
                error_type = error.get("error_type", "unknown")
                field = error.get("field", "")
                message = error.get("message", "")
                label = "ERROR" if _is_blocking(error) else "WARNING"
                print(f"{label} [{error_type}] {field}: {message}")
        if blocking:
            return 1
        print("Brief verification passed! All required fields are present and valid.")
        return 0


if __name__ == "__main__":
    sys.exit(main())
