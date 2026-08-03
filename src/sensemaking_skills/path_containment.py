"""Shared, pure path-containment primitives.

Extracted verbatim (no logic changes) from ``scripts/gate_a_authorization.py``
so both Gate A (Lane B / ADR 0022) and the campaign-validation package
(Lane A / ADR 0023 Phase 2) reuse ONE containment implementation rather
than defining two independent, potentially-diverging ones. ADR 0023 section
15 explicitly requires reusing the existing ``framework_root`` /
``target_root`` / ``artifact_root`` topology rather than inventing a
parallel resolution mechanism; ADR 0022's own containment code is that
existing, already-reviewed implementation.

``scripts/gate_a_authorization.py`` imports every name below (a genuine
re-export, not a re-implementation) so ``gate_a_authorization.canonicalize_path
is path_containment.canonicalize_path`` holds by construction --
see ``tests/test_path_containment_extraction_characterization.py`` for the
identity proof and the behavioral characterization battery captured before
this extraction.

This module has ZERO import-time dependency on ``scripts/`` or ``docs/`` --
it is a normal, installable package module, importable from a wheel with no
access to the repository checkout (unlike a prior revision of the
campaign-validation adapter, which loaded ``gate_a_authorization.py`` by
filesystem path -- that approach broke for an installed wheel and is no
longer used).
"""

from __future__ import annotations

import os
import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path, PurePath, PurePosixPath
from typing import Optional

__all__ = [
    "GATE_A_OUTPUT_PATH_ESCAPE",
    "GATE_A_OUTPUT_PATH_AMBIGUOUS",
    "GATE_A_OUTPUT_PATH_SYMLINK_ESCAPE",
    "GATE_A_OUTPUT_PATH_PHYSICAL_RESOLUTION_FAILED",
    "GATE_A_OUTPUT_PATH_REPARSE_POINT_AMBIGUOUS",
    "GATE_A_OUTPUT_PATH_OUTSIDE_FRAMEWORK_ROOT",
    "GATE_A_OUTPUT_PATH_ALIAS_MISMATCH",
    "GATE_A_OUTPUT_PATH_UNANCHORABLE",
    "GATE_A_OUTPUT_PATH_COLON_COMPONENT_PROHIBITED",
    "PHYSICAL_CONTAINMENT_FAILURE_CODES",
    "CanonicalPath",
    "canonicalize_path",
    "has_colon_component",
    "anchor_output_path",
    "resolve_containment",
]

GATE_A_OUTPUT_PATH_ESCAPE = "GATE_A_OUTPUT_PATH_ESCAPE"
GATE_A_OUTPUT_PATH_AMBIGUOUS = "GATE_A_OUTPUT_PATH_AMBIGUOUS"
GATE_A_OUTPUT_PATH_SYMLINK_ESCAPE = "GATE_A_OUTPUT_PATH_SYMLINK_ESCAPE"

# -- third-review physical-containment failure codes -------------------------
# Each of these means "we could not establish where this path physically
# lands". None of them may ever degrade to ordinary development.
GATE_A_OUTPUT_PATH_PHYSICAL_RESOLUTION_FAILED = (
    "GATE_A_OUTPUT_PATH_PHYSICAL_RESOLUTION_FAILED")
GATE_A_OUTPUT_PATH_REPARSE_POINT_AMBIGUOUS = (
    "GATE_A_OUTPUT_PATH_REPARSE_POINT_AMBIGUOUS")
GATE_A_OUTPUT_PATH_OUTSIDE_FRAMEWORK_ROOT = (
    "GATE_A_OUTPUT_PATH_OUTSIDE_FRAMEWORK_ROOT")
GATE_A_OUTPUT_PATH_ALIAS_MISMATCH = "GATE_A_OUTPUT_PATH_ALIAS_MISMATCH"
GATE_A_OUTPUT_PATH_UNANCHORABLE = "GATE_A_OUTPUT_PATH_UNANCHORABLE"
GATE_A_OUTPUT_PATH_COLON_COMPONENT_PROHIBITED = (
    "GATE_A_OUTPUT_PATH_COLON_COMPONENT_PROHIBITED")

#: Every code meaning "physical containment could not be established". None of
#: these may ever be treated as evidence of ordinary development.
PHYSICAL_CONTAINMENT_FAILURE_CODES = frozenset({
    GATE_A_OUTPUT_PATH_AMBIGUOUS,
    GATE_A_OUTPUT_PATH_SYMLINK_ESCAPE,
    GATE_A_OUTPUT_PATH_PHYSICAL_RESOLUTION_FAILED,
    GATE_A_OUTPUT_PATH_REPARSE_POINT_AMBIGUOUS,
    GATE_A_OUTPUT_PATH_OUTSIDE_FRAMEWORK_ROOT,
    GATE_A_OUTPUT_PATH_ALIAS_MISMATCH,
    GATE_A_OUTPUT_PATH_UNANCHORABLE,
    GATE_A_OUTPUT_PATH_COLON_COMPONENT_PROHIBITED,
})

_DRIVE_RE = re.compile(r"^([A-Za-z]):$")


@dataclass(frozen=True)
class CanonicalPath:
    """One canonical representation of a path. Built by `canonicalize_path`.

    Attributes
    ----------
    raw:
        The original input, stringified. Kept for diagnostics ONLY. Nothing in
        this module may make a security decision from `raw`.
    drive:
        Drive letter without the colon (``"C"``), or ``""``.
    is_absolute:
        Whether the input was rooted.
    parts:
        Canonical, case-preserving, NFC-normalized path components after `.`
        removal, separator collapsing and safe `..` resolution.
    escapes_anchor:
        True when unresolved leading `..` components remain, i.e. the path
        refers to something above its own anchor.
    """

    raw: str
    drive: str
    is_absolute: bool
    parts: tuple[str, ...]
    escapes_anchor: bool

    @property
    def lexical(self) -> PurePosixPath:
        """Canonical lexical form as a POSIX pure path."""
        prefix = ""
        if self.drive:
            prefix += f"{self.drive}:"
        if self.is_absolute:
            prefix += "/"
        return PurePosixPath(prefix + "/".join(self.parts))

    @property
    def identity_key(self) -> str:
        """The stable, case-preserving string stored on `InvocationIdentity`.

        This is what the capability digest binds to. Two spellings of the same
        path produce the SAME identity key; that is the property that stops an
        attacker from obtaining a capability for one spelling and using it for
        another, or from splitting one logical invocation into two identities.
        """
        return str(self.lexical)

    @property
    def match_parts(self) -> tuple[str, ...]:
        """Components folded for case-insensitive, NFC-stable comparison."""
        return tuple(p.casefold() for p in self.parts)

    def relative_to_root(self, root: "CanonicalPath") -> Optional[PurePosixPath]:
        """Repository-relative POSIX path, or None if not contained in `root`.

        Containment is decided on whole components, never on string prefixes,
        so `experiments-old/` is not "inside" `experiments/`.
        """
        if root is None or not root.parts and not root.is_absolute:
            return None
        if self.drive.casefold() != root.drive.casefold():
            return None
        if self.is_absolute != root.is_absolute:
            return None
        rp = root.match_parts
        if self.match_parts[:len(rp)] != rp:
            return None
        return PurePosixPath("/".join(self.parts[len(rp):]) or ".")


def canonicalize_path(value) -> CanonicalPath:
    """THE canonicalization primitive. Lexical, total, filesystem-free.

    Accepts ``str``, ``os.PathLike``, ``Path``, ``PurePosixPath`` or ``None``.
    Never raises, never touches the filesystem, and never requires the path to
    exist -- Evidence 0016's output directory does not exist and must still be
    classifiable.
    """
    if value is None:
        return CanonicalPath(raw="", drive="", is_absolute=False, parts=(),
                             escapes_anchor=False)
    raw = str(value)
    text = unicodedata.normalize("NFC", raw)
    text = text.replace("\\", "/")

    drive = ""
    m = _DRIVE_RE.match(text[:2])
    if m:
        drive = m.group(1)
        text = text[2:]

    is_absolute = text.startswith("/")

    parts: list[str] = []
    escapes = False
    for segment in text.split("/"):
        if segment == "" or segment == ".":
            # Repeated separators produce empty segments; `.` is a no-op.
            # Collapsing BOTH is precisely what the old normalizer failed to
            # do, and is what the reproduced bypass depended on.
            continue
        if segment == "..":
            if parts and parts[-1] != "..":
                parts.pop()
            elif is_absolute or drive:
                # A filesystem root has no parent; `/..` is `/`.
                continue
            else:
                parts.append("..")
                escapes = True
            continue
        parts.append(segment)

    return CanonicalPath(
        raw=raw,
        drive=drive,
        is_absolute=is_absolute,
        parts=tuple(parts),
        escapes_anchor=escapes,
    )


def has_colon_component(canon: CanonicalPath) -> bool:
    """True when any path COMPONENT carries a colon.

    On Windows a colon inside a component is NTFS alternate-data-stream or
    drive-relative syntax (``experiments:x``, ``dir:stream``, ``dir::$DATA``).
    Those forms do not mean what their spelling suggests and Win32 resolves
    them inconsistently, so Gate A rejects them outright rather than letting a
    failed evidence parse read as ordinary development. The drive prefix is
    stripped by `canonicalize_path` before `parts` is built, so a legitimate
    ``C:\\...`` never trips this.
    """
    return any(":" in p for p in canon.parts)


def anchor_output_path(value, framework_root) -> tuple[Optional[Path], Optional[str]]:
    """THE anchoring primitive. Returns ``(anchored_absolute_path, failure)``.

    A relative output path is interpreted as ``framework_root / value`` and
    NEVER against:

      * process CWD;
      * test-runner CWD;
      * a caller-selected CWD;
      * the current script directory;
      * environment variables.

    This is the third-review root cause: `resolve_containment` used to build
    ``Path(str(value))``, which Python resolves against `os.getcwd()`. With a
    CWD outside the framework root, every relative alias of the campaign
    directory missed the physical pass entirely and fell back to a lexical
    parse that reported ORDINARY_DEVELOPMENT. A caller running `os.chdir()`
    must not be able to change a classification.
    """
    canon = canonicalize_path(value)
    if canon.is_absolute or canon.drive:
        return Path(str(value)), None
    if framework_root in (None, ""):
        # A relative path with no authoritative anchor cannot be placed. That
        # is ambiguity, never ordinariness.
        return None, GATE_A_OUTPUT_PATH_UNANCHORABLE
    return Path(str(framework_root)).joinpath(*canon.parts) if canon.parts \
        else Path(str(framework_root)), None


def resolve_containment(value, root) -> tuple[Optional[Path], Optional[str]]:
    """PHYSICAL containment check. Returns ``(resolved_or_None, failure_code)``.

    Explicit sequence -- path INTERPRETATION is separated from filesystem
    RESOLUTION, and interpretation always happens first:

      1. validate input type;
      2. select the authoritative anchor (`framework_root`);
      3. build the anchored absolute path;
      4. lexical normalization;
      5. identify the nearest existing ancestor;
      6. physically resolve that ancestor;
      7. append the unresolved suffix;
      8. evaluate containment against the PHYSICALLY RESOLVED framework root;
      9. produce the canonical repository-relative identity.

    The final component is allowed not to exist -- an output directory that has
    not been created yet is normal, and requiring existence would make
    classification depend on whether the attacker had already made the
    directory. This function never creates anything.

    Fails closed. Any OSError (permission denied, broken reparse point, symlink
    loop, inaccessible ancestor, unsupported path form) yields an explicit
    failure code. There is no "no physical signal, carry on lexically" branch:
    that branch was the bypass.

    NOTE for campaign-validation callers: a plain LEXICAL escape with no
    symlink/reparse point involved (e.g. an anchored path built from a
    literal ``../x`` that was outside the root from the start, without any
    filesystem redirection) intentionally returns ``(resolved, None)`` here
    -- Gate A treats that as "ordinary development writing elsewhere," not
    an error condition of this primitive. A caller that requires STRICT
    containment (reject-if-outside-root regardless of mechanism) must check
    ``canonicalize_path(resolved).relative_to_root(canonicalize_path(root))``
    itself after calling this function -- see
    ``sensemaking_skills.campaign_validation.fs_adapter.resolve_under_root``.
    """
    # 1. validate input type
    if value in (None, ""):
        return None, None
    if not isinstance(value, (str, os.PathLike, PurePath)):
        return None, GATE_A_OUTPUT_PATH_PHYSICAL_RESOLUTION_FAILED
    if root in (None, ""):
        return None, None

    canon = canonicalize_path(value)
    # Colon-bearing components are rejected BEFORE any filesystem contact.
    if has_colon_component(canon):
        return None, GATE_A_OUTPUT_PATH_COLON_COMPONENT_PROHIBITED

    try:
        # 2/3. anchor to the framework root -- never to CWD.
        anchored, anchor_failure = anchor_output_path(value, root)
        if anchor_failure:
            return None, anchor_failure

        # 6. resolve the framework root itself, with the same semantics, so
        #    step 8 never compares a resolved candidate to an unresolved root.
        try:
            real_root = Path(str(root)).resolve(strict=False)
        except OSError:
            return None, GATE_A_OUTPUT_PATH_PHYSICAL_RESOLUTION_FAILED

        # 5. nearest existing ancestor
        existing = anchored
        unresolved: list[str] = []
        guard = 0
        try:
            while (not existing.exists() and existing.parent != existing
                   and guard < 256):
                # `Path.exists()` follows links and SWALLOWS the OSError, so a
                # symlink loop and a dangling symlink both report False --
                # indistinguishable from "this output directory has not been
                # created yet". Treating them as not-yet-created let a
                # component that physically EXISTS but cannot be resolved slide
                # through as ordinary development. `os.path.lexists()` sees the
                # link itself: if the entry is there but unresolvable, we do not
                # know where it lands, and that is ambiguity, not absence.
                if os.path.lexists(existing):
                    return None, GATE_A_OUTPUT_PATH_REPARSE_POINT_AMBIGUOUS
                unresolved.append(existing.name)
                existing = existing.parent
                guard += 1
        except OSError:
            return None, GATE_A_OUTPUT_PATH_PHYSICAL_RESOLUTION_FAILED
        if guard >= 256:
            return None, GATE_A_OUTPUT_PATH_REPARSE_POINT_AMBIGUOUS

        # 6. physically resolve it (follows junctions, symlinks, 8.3 names,
        #    trailing-dot/space Win32 normalization and case aliases).
        try:
            resolved_ancestor = existing.resolve(strict=False)
        except OSError:
            return None, GATE_A_OUTPUT_PATH_REPARSE_POINT_AMBIGUOUS
        if not resolved_ancestor.is_absolute():
            # Resolution that did not produce an absolute path tells us
            # nothing about physical location.
            return None, GATE_A_OUTPUT_PATH_PHYSICAL_RESOLUTION_FAILED

        # 7. append the unresolved suffix
        resolved = resolved_ancestor.joinpath(*reversed(unresolved))

        # 8. component-aware containment against the resolved root
        canon_res = canonicalize_path(resolved)
        canon_root = canonicalize_path(real_root)
        rel = canon_res.relative_to_root(canon_root)
        if rel is None:
            # An ANCHORED path that resolves outside the root escaped through a
            # reparse point. A path that was absolute and outside to begin with
            # is ordinary development writing elsewhere.
            lex_rel = canonicalize_path(anchored).relative_to_root(canon_root)
            if lex_rel is not None:
                return resolved, GATE_A_OUTPUT_PATH_SYMLINK_ESCAPE
        return resolved, None
    except (OSError, ValueError):
        return None, GATE_A_OUTPUT_PATH_PHYSICAL_RESOLUTION_FAILED
