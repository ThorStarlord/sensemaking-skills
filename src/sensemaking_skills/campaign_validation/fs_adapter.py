"""Filesystem / artifact-root trust boundary adapter.

Campaign validation reuses the existing artifact-root trust model rather
than building a second, incompatible path system (ADR 0023 section 15). This
module is a narrow adapter around ``scripts/gate_a_authorization.py``'s
pure, filesystem-touching-but-behavior-frozen containment primitives
(``canonicalize_path``, ``resolve_containment``) -- it imports them
unmodified; **no line of ``gate_a_authorization.py`` is edited by this
package**, so every existing Gate A test remains byte-for-byte unaffected.

``resolve_containment`` already implements: lexical normalization, physical
resolution against a pinned root (never the process CWD), symlink/reparse
point escape detection, and cross-platform (Windows/Linux) containment --
exactly the properties this adapter needs. Reimplementing that logic here
would risk a second, subtly-divergent containment mechanism; this module
instead depends on it directly.
"""

from __future__ import annotations

import importlib.util
import sys
import threading
from pathlib import Path
from typing import Optional

from .failure_codes import CAMPAIGN_FAILURE_CODES  # noqa: F401  (re-export point)

_GATE_A_MODULE_NAME = "sensemaking_skills._gate_a_authorization_impl"
_lock = threading.Lock()
_gate_a_module = None


def _load_gate_a_module():
    """Load ``scripts/gate_a_authorization.py`` by file path (no sys.path mutation).

    Loaded once, lazily, and cached. Using ``importlib.util.spec_from_file_location``
    (rather than ``sys.path.insert`` + ``import``, the pattern used by Gate A's
    own tests) avoids adding ``scripts/`` to ``sys.path`` for the lifetime of
    the process, which would otherwise risk shadowing unrelated modules.
    """
    global _gate_a_module
    with _lock:
        if _gate_a_module is not None:
            return _gate_a_module
        repo_root = Path(__file__).resolve().parents[3]
        module_path = repo_root / "scripts" / "gate_a_authorization.py"
        spec = importlib.util.spec_from_file_location(_GATE_A_MODULE_NAME, module_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[_GATE_A_MODULE_NAME] = module
        spec.loader.exec_module(module)
        _gate_a_module = module
        return module


class ArtifactRootError(ValueError):
    def __init__(self, code: str, message: str):
        super().__init__(f"{code}: {message}")
        self.code = code
        self.message = message


def resolve_under_root(relative_or_absolute: str, artifact_root: str) -> Path:
    """Resolve a candidate path strictly beneath ``artifact_root``.

    Fails closed with a ``CAMPAIGN_PATH_ESCAPE`` or
    ``CAMPAIGN_SYMLINK_CONTAINMENT_VIOLATION`` ``ArtifactRootError`` on any
    lexical or physical escape, and with ``CAMPAIGN_FILESYSTEM_ERROR`` on any
    other filesystem failure. Returns the resolved, contained absolute path
    on success.
    """
    ga = _load_gate_a_module()
    try:
        resolved, failure = ga.resolve_containment(relative_or_absolute, artifact_root)
    except Exception as exc:  # pragma: no cover - defensive, Gate A already fails closed
        raise ArtifactRootError("CAMPAIGN_FILESYSTEM_ERROR", str(exc)) from exc

    if failure == ga.GATE_A_OUTPUT_PATH_SYMLINK_ESCAPE or failure == getattr(
        ga, "GATE_A_OUTPUT_PATH_REPARSE_POINT_AMBIGUOUS", object()
    ):
        raise ArtifactRootError(
            "CAMPAIGN_SYMLINK_CONTAINMENT_VIOLATION",
            f"path escapes artifact root via symlink/reparse point: {failure}",
        )
    if failure == getattr(ga, "GATE_A_OUTPUT_PATH_COLON_COMPONENT_PROHIBITED", object()):
        raise ArtifactRootError(
            "CAMPAIGN_PATH_ESCAPE", f"path contains a forbidden colon component: {failure}"
        )
    if failure is not None:
        raise ArtifactRootError("CAMPAIGN_PATH_ESCAPE", f"path escapes artifact root: {failure}")
    if resolved is None:
        raise ArtifactRootError("CAMPAIGN_PATH_ESCAPE", "path could not be resolved under root")

    # resolve_containment permits an absolute-and-outside path to pass through
    # silently (it returns (resolved, None) for legitimate absolute paths
    # outside the root, treating that as "ordinary development" in Gate A's
    # domain). Campaign validation's contract is stricter: every candidate
    # MUST be contained. Enforce that explicitly here rather than depending on
    # Gate A callers' broader tolerance.
    canon_resolved = ga.canonicalize_path(resolved)
    canon_root = ga.canonicalize_path(Path(str(artifact_root)).resolve(strict=False))
    if canon_resolved.relative_to_root(canon_root) is None:
        raise ArtifactRootError("CAMPAIGN_PATH_ESCAPE", "resolved path is outside artifact root")

    return resolved


def read_utf8_bytes(path: Path) -> Optional[bytes]:
    """Read raw UTF-8 bytes deliberately. Returns None if the file is missing.

    Any other OSError is re-raised as ``ArtifactRootError``
    (``CAMPAIGN_FILESYSTEM_ERROR``) so callers never see an uncaught OSError.
    """
    try:
        if not path.is_file():
            return None
        return path.read_bytes()
    except OSError as exc:
        raise ArtifactRootError("CAMPAIGN_FILESYSTEM_ERROR", str(exc)) from exc
