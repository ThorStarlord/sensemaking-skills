"""Filesystem / artifact-root trust boundary adapter.

Campaign validation reuses the existing artifact-root trust model rather
than building a second, incompatible path system (ADR 0023 section 15).
This module is a narrow adapter around ``sensemaking_skills.path_containment``
-- the shared, pure containment primitives extracted (unmodified) from
``scripts/gate_a_authorization.py`` and now reused by both Gate A and this
package (see ``tests/test_path_containment_extraction_characterization.py``
for the extraction's non-regression proof).

This module is a normal package import: it does **not** load
``scripts/gate_a_authorization.py`` by filesystem path at runtime. A prior
revision did that (via ``importlib.util.spec_from_file_location``), which
worked from a repository checkout but silently could not work from an
installed wheel with no access to ``scripts/`` -- there is no such
directory once the package is installed. Importing
``sensemaking_skills.path_containment`` instead is a normal, packaged
dependency that works identically from a checkout or an installed wheel.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from sensemaking_skills import path_containment as pc

from .failure_codes import CAMPAIGN_FAILURE_CODES  # noqa: F401  (re-export point)


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
    try:
        resolved, failure = pc.resolve_containment(relative_or_absolute, artifact_root)
    except Exception as exc:  # pragma: no cover - defensive, Gate A already fails closed
        raise ArtifactRootError("CAMPAIGN_FILESYSTEM_ERROR", str(exc)) from exc

    if failure in (pc.GATE_A_OUTPUT_PATH_SYMLINK_ESCAPE,
                   pc.GATE_A_OUTPUT_PATH_REPARSE_POINT_AMBIGUOUS):
        raise ArtifactRootError(
            "CAMPAIGN_SYMLINK_CONTAINMENT_VIOLATION",
            f"path escapes artifact root via symlink/reparse point: {failure}",
        )
    if failure == pc.GATE_A_OUTPUT_PATH_COLON_COMPONENT_PROHIBITED:
        raise ArtifactRootError(
            "CAMPAIGN_PATH_ESCAPE", f"path contains a forbidden colon component: {failure}"
        )
    if failure is not None:
        raise ArtifactRootError("CAMPAIGN_PATH_ESCAPE", f"path escapes artifact root: {failure}")
    if resolved is None:
        raise ArtifactRootError("CAMPAIGN_PATH_ESCAPE", "path could not be resolved under root")

    # resolve_containment permits an absolute-and-outside path to pass through
    # silently (it returns (resolved, None) for a plain lexical escape with
    # no symlink involved -- Gate A's own docstring calls that "ordinary
    # development writing elsewhere"). Campaign validation's contract is
    # stricter: every candidate MUST be contained, regardless of mechanism.
    # Enforce that explicitly here rather than depending on Gate A callers'
    # broader tolerance -- see path_containment.resolve_containment's
    # docstring note addressed specifically to this caller.
    try:
        real_root = Path(str(artifact_root)).resolve(strict=False)
    except OSError as exc:
        raise ArtifactRootError("CAMPAIGN_FILESYSTEM_ERROR", str(exc)) from exc
    canon_resolved = pc.canonicalize_path(resolved)
    canon_root = pc.canonicalize_path(real_root)
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
