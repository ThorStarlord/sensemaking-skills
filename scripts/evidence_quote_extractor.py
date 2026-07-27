r"""
Deterministic evidence-quote extraction (issue #89).

Problem this closes: Evidence 0013 (experiments/evidence/0013-stage1-auteur-
run-model-enforcement/) found the MODEL was the verbatim-copy boundary for
`evidence_excerpts[].quote` in repository_sensemaking_brief.md, and a real
controlled Stage 1 run produced three real fidelity failures while
transcribing quotes: a Unicode em dash normalized to `--`, leading
indentation dropped, and Markdown bold/backtick formatting altered.

Fix: the model only supplies `file` + `lines` (a line range) + rationale.
This module is the sole runtime component that reads the cited source file
and extracts the exact quote text -- byte-for-byte (after the documented
CRLF/encoding policy below), never paraphrased, never re-typed by a model.
scripts/brief_skeleton.py's reconcile() calls this for every evidence
excerpt and overwrites the `quote` field with its result; validate-brief.py
then re-derives the same extraction independently and checks the stored
quote against it (see EVIDENCE_QUOTE_NOT_FOUND / _quote_found_near in
scripts/validate-brief.py) -- this module does not weaken that check, it
makes the *stored* quote trustworthy so the check has something honest to
verify.

Safety contract:
  - Only repository-relative paths are accepted. Absolute paths (POSIX
    `/...` or Windows drive-letter `C:\...`) and any ".." traversal
    component are rejected before the filesystem is ever touched.
  - The resolved path is symlink-resolved (os.path.realpath) and proven to
    remain under the authorized root via os.path.commonpath -- the same
    technique scripts/skill_executor.py's canonicalize_path/is_within_root
    use for artifact-write confinement (issue #43), reused here rather than
    reinvented, for the read side.
  - This module never writes to the authorized root or anywhere else. It is
    read-only by construction.
  - Missing files, non-UTF-8/undecodable files, and invalid line ranges
    (zero/negative, reversed, out of bounds) are rejected with a
    QuoteExtractionError -- never silently degraded to an empty or partial
    quote.

Encoding / line-ending policy (documented, not implicit):
  - Files are read as UTF-8 (strict). A file that cannot be decoded as
    UTF-8 is rejected, not guessed at with another codec.
  - CRLF and lone-CR line endings are normalized to LF before splitting
    into lines, matching validate-brief.py's own `_quote_found_near`
    normalization. This means a CRLF source file and an LF source file with
    the same logical line content produce byte-identical extracted quotes;
    the source's line-ending convention is not part of the quote contract.
  - Multi-line quotes are joined with a canonical "\n" (never "\r\n"),
    regardless of the source file's own line endings.
  - Leading indentation, trailing spaces that are part of a line, Unicode
    code points, Markdown formatting characters, and blank lines within the
    cited range are preserved verbatim -- no trimming, no whitespace
    collapsing, no normalization beyond the CRLF policy above. (Validator-
    side comparison may still apply its own whitespace-tolerant matching;
    that is a separate, already-existing concern in validate-brief.py and
    is unaffected by this module.)
"""

from __future__ import annotations

import os
from dataclasses import dataclass


class QuoteExtractionError(Exception):
    """Raised when deterministic quote extraction cannot complete.

    Callers (brief_skeleton.reconcile) MUST NOT catch this and silently fall
    back to an unverified model-supplied quote -- that would reintroduce the
    exact defect issue #89 closes. The documented behavior is to fail
    loudly: either propagate this exception, or (as brief_skeleton.reconcile
    does) record an unambiguous failure sentinel that the validator is
    guaranteed to reject.
    """


@dataclass(frozen=True)
class ExtractedQuote:
    quote: str
    file: str
    line_start: int
    line_end: int


def _canonicalize(path: str) -> str:
    """Same technique as scripts/skill_executor.py's canonicalize_path:
    absolute, symlink-resolved, case-normalized, so distinct spellings of
    the same on-disk location compare equal and traversal via ".." or a
    symlinked ancestor cannot escape detection.
    """
    resolved = os.path.realpath(os.path.abspath(os.path.normpath(path)))
    return os.path.normcase(resolved)


def _is_within_root(path: str, root: str) -> bool:
    """Same technique as scripts/skill_executor.py's is_within_root: proven
    containment via os.path.commonpath on canonicalized inputs, not a
    string-prefix check (which a ".." or symlinked-ancestor escape would
    defeat).
    """
    try:
        return os.path.commonpath([path, root]) == root
    except ValueError:
        # Different drives on Windows, or otherwise not comparable.
        return False


def resolve_repo_relative_path(relative_path: str | None, root: str) -> str:
    r"""Resolve a model-supplied path against `root`, rejecting anything that
    is not a plain repository-relative path contained within `root`.

    Rejects (raises QuoteExtractionError):
      - None / empty path
      - POSIX-absolute paths (r"/etc/passwd")
      - Windows-absolute paths (r"C:\Windows\...", r"\\server\share\...")
      - any ".." path component (parent-directory traversal)
      - a path that, once resolved (including through symlinks), lands
        outside `root`
    """
    if relative_path is None:
        raise QuoteExtractionError("no path supplied")
    rel = str(relative_path).strip()
    if not rel:
        raise QuoteExtractionError("empty path supplied")

    normalized = rel.replace("\\", "/")

    if normalized.startswith("/"):
        raise QuoteExtractionError(f"absolute paths are not allowed: {relative_path!r}")
    if len(normalized) >= 2 and normalized[1] == ":":
        raise QuoteExtractionError(f"absolute paths are not allowed: {relative_path!r}")
    if normalized.startswith("//") or normalized.startswith("file:"):
        raise QuoteExtractionError(f"absolute/URI paths are not allowed: {relative_path!r}")

    parts = [p for p in normalized.split("/") if p not in ("", ".")]
    if ".." in parts:
        raise QuoteExtractionError(f"parent-directory traversal is not allowed: {relative_path!r}")

    root_c = _canonicalize(root)
    candidate = os.path.join(root, *parts) if parts else root
    candidate_c = _canonicalize(candidate)

    if not _is_within_root(candidate_c, root_c):
        raise QuoteExtractionError(
            f"resolved path escapes the authorized root: {relative_path!r} -> {candidate_c}"
        )
    return candidate_c


def _read_source_lines(resolved_path: str, relative_path: str) -> list[str]:
    if not os.path.isfile(resolved_path):
        raise QuoteExtractionError(f"file not found: {relative_path!r}")
    try:
        with open(resolved_path, "rb") as f:
            raw = f.read()
    except OSError as e:
        raise QuoteExtractionError(f"could not read file {relative_path!r}: {e}")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as e:
        raise QuoteExtractionError(f"file is not valid UTF-8 text: {relative_path!r}: {e}")

    # CRLF / lone-CR normalization (documented policy, see module docstring).
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = normalized.split("\n")
    # A trailing newline produces one extra "" entry from split() that does
    # not correspond to a real source line; drop it so line numbers line up
    # with what a human/editor would call "line N".
    if lines and lines[-1] == "" and normalized.endswith("\n"):
        lines = lines[:-1]
    return lines


def extract_quote(relative_path: str, line_start: int, line_end: int, root: str) -> ExtractedQuote:
    """Deterministically extract the verbatim text of lines [line_start,
    line_end] (1-indexed, inclusive) from `relative_path` resolved against
    `root`.

    Raises QuoteExtractionError for any of: unsafe path, missing file,
    undecodable file, non-integer/zero/negative/reversed/out-of-bounds line
    range. Never returns a partial or best-effort result.
    """
    resolved = resolve_repo_relative_path(relative_path, root)
    lines = _read_source_lines(resolved, relative_path)
    total = len(lines)

    try:
        start = int(line_start)
        end = int(line_end)
    except (TypeError, ValueError):
        raise QuoteExtractionError(
            f"line_start/line_end must be integers, got {line_start!r}/{line_end!r}"
        )

    if start <= 0 or end <= 0:
        raise QuoteExtractionError(f"line numbers must be >= 1, got {start}-{end}")
    if end < start:
        raise QuoteExtractionError(f"line range is reversed: {start}-{end}")
    if start > total or end > total:
        raise QuoteExtractionError(
            f"line range {start}-{end} is out of bounds; file has {total} lines"
        )

    quoted = lines[start - 1:end]
    return ExtractedQuote(quote="\n".join(quoted), file=str(relative_path), line_start=start, line_end=end)


_LINES_RE_1 = None  # placeholder for lazy import avoidance; see parse_lines_value


def parse_lines_value(lines_value: str) -> tuple[int, int]:
    """Parse the brief's 'lines' field ('L18', 'L25-L30', '18', '25-30')
    into a (start, end) tuple. Mirrors scripts/validate-brief.py's
    `_parse_line_range` accepted grammar so the model's existing 'lines'
    field format continues to work unchanged.
    """
    import re

    match = re.match(r"^L?(\d+)(?:-L?(\d+))?$", str(lines_value).strip())
    if not match:
        raise QuoteExtractionError(f"could not parse line range: {lines_value!r}")
    start = int(match.group(1))
    end = int(match.group(2)) if match.group(2) else start
    return (start, end)
