"""Level 2 cross-artifact semantic alignment validator.

Checks that the problem_frame "Object Under Pressure" aligns with the
repo_sensemaking_brief "Weakest Boundary" — ensuring the system doesn't
diagnose a different boundary than the one framed.

Usage:
    python scripts/validate-alignment.py <frame_path> [--brief <brief_path>] [--repo-root PATH]
    python scripts/validate-alignment.py --list-codes
"""

import os
import sys
import re
import argparse

from _validator_utils import format_error

# Stable error codes
MISSING_FILE = "MISSING_FILE"
MISSING_SECTION = "MISSING_SECTION"
NO_TERM_OVERLAP = "NO_TERM_OVERLAP"
FILE_REF_MISMATCH = "FILE_REF_MISMATCH"
BOUNDARY_DRIFT = "BOUNDARY_DRIFT"

HEADING_RE = re.compile(r"^##\s+(?:\d+\.\s*)?(?P<name>.+?)\s*$", re.MULTILINE)
FILE_REF_RE = re.compile(r"`?[\w./\\-]+\.(?:md|py|yaml|yml|toml|txt)`?", re.IGNORECASE)


def _extract_sections(content: str) -> dict[str, str]:
    sections = {}
    matches = list(HEADING_RE.finditer(content))
    for idx, match in enumerate(matches):
        start = match.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(content)
        name = match.group("name").strip().lower().replace("-", " ")
        sections[name] = content[start:end].strip()
    return sections


def _extract_nouns(text: str) -> set[str]:
    words = re.findall(r"[a-zA-Z_]{4,}", text)
    stopwords = {"this", "that", "with", "from", "what", "will", "must", "have",
                 "been", "were", "does", "done", "when", "then", "than", "also",
                 "into", "over", "such", "each", "which", "their", "there", "about",
                 "would", "could", "should", "after", "before", "between", "without",
                 "being", "while", "where", "other", "these", "those", "shall"}
    return {w.lower() for w in words if w.lower() not in stopwords and len(w) > 3}


def validate_alignment(frame_path: str, brief_path: str | None = None, repo_root: str = ".") -> list[str]:
    errors: list[str] = []

    if not os.path.exists(frame_path):
        errors.append(format_error(MISSING_FILE, f"Problem frame not found: {frame_path}"))
        return errors

    with open(frame_path, encoding="utf-8") as f:
        frame_content = f.read()

    frame_sections = _extract_sections(frame_content)
    object_under_pressure = frame_sections.get("object under pressure", "")

    if not object_under_pressure:
        errors.append(format_error(MISSING_SECTION, "Problem frame missing 'Object Under Pressure' section"))

    if not brief_path:
        return errors

    if not os.path.exists(brief_path):
        errors.append(format_error(MISSING_FILE, f"Brief not found: {brief_path}"))
        return errors

    with open(brief_path, encoding="utf-8") as f:
        brief_content = f.read()

    brief_sections = _extract_sections(brief_content)
    weakest_boundary = brief_sections.get("weakest boundary", "")
    evidence = brief_sections.get("evidence", "")

    if not weakest_boundary:
        errors.append(format_error(MISSING_SECTION, "Brief missing 'Weakest Boundary' section"))

    if not object_under_pressure or not weakest_boundary:
        return errors

    # 1. Term overlap
    frame_terms = _extract_nouns(object_under_pressure)
    brief_terms = _extract_nouns(weakest_boundary)

    if frame_terms and brief_terms:
        overlap = frame_terms & brief_terms
        if not overlap:
            errors.append(format_error(NO_TERM_OVERLAP,
                f"No shared key terms between Object Under Pressure and Weakest Boundary. "
                f"Frame terms: {sorted(frame_terms)[:10]}. Brief terms: {sorted(brief_terms)[:10]}."))
        elif len(overlap) < 2:
            errors.append(format_error(BOUNDARY_DRIFT,
                f"Weak overlap ({len(overlap)} term(s): {overlap}). "
                f"Object Under Pressure and Weakest Boundary may be discussing different aspects."))

    # 2. File reference alignment
    frame_files = set(FILE_REF_RE.findall(object_under_pressure))
    if frame_files and evidence:
        if not FILE_REF_RE.search(evidence):
            errors.append(format_error(FILE_REF_MISMATCH,
                "Object Under Pressure references files but Evidence section has no file citations"))
        elif not any(ref in evidence for ref in frame_files):
            errors.append(format_error(FILE_REF_MISMATCH,
                f"Files in Object Under Pressure ({sorted(frame_files)}) not cited in Evidence section"))

    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate semantic alignment between problem_frame and sensemaking brief.")
    parser.add_argument("artifact_path", nargs="?", help="Path to problem_frame .md file (positional)")
    parser.add_argument("--frame", help="Path to problem_frame .md file")
    parser.add_argument("--brief", help="Path to repository_sensemaking_brief .md file")
    parser.add_argument("--repo-root", default=".", help="Root directory of the repository")
    parser.add_argument("--list-codes", action="store_true", help="List all error codes and exit")
    args = parser.parse_args(argv)

    if args.list_codes:
        codes = [MISSING_FILE, MISSING_SECTION, NO_TERM_OVERLAP, FILE_REF_MISMATCH, BOUNDARY_DRIFT]
        print("Stable error codes for alignment validation:")
        for c in codes:
            print(f"  {c}")
        return 0

    frame_path = args.frame or args.artifact_path
    if not frame_path:
        parser.print_usage()
        return 1

    errs = validate_alignment(frame_path, args.brief, args.repo_root)
    if errs:
        for e in errs:
            print(f"ERROR {e}")
        return 1

    print("Alignment validation passed!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
