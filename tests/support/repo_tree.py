"""Repository-tree scans that tolerate concurrent build output.

Parallel test workers build wheels in the repository root. A wheel build writes
staging directories under build/ and removes them when it finishes. A
Path.rglob() scan can list such a directory and then find it gone, which raises
FileNotFoundError and fails an unrelated test.

os.walk() reports the same disappearance through onerror. The handler here
skips only a directory that has vanished. Every other error is re-raised,
including PermissionError. CPython's rglob() silently skips directories it
cannot read, so the forbidden-file check was weaker than it looked.
"""

from __future__ import annotations

import os
from collections.abc import Iterator
from pathlib import Path


def _raise_unless_vanished(error: OSError) -> None:
    if not isinstance(error, FileNotFoundError):
        raise error


def iter_tree(root: Path) -> Iterator[Path]:
    """Yield every directory and file under root, as root.rglob("*") does.

    Symbolic links are not followed, matching rglob().
    """
    if not root.is_dir():
        raise NotADirectoryError(f"repository tree root is not a directory: {root}")
    for dirpath, dirnames, filenames in os.walk(root, onerror=_raise_unless_vanished):
        base = Path(dirpath)
        for name in dirnames + filenames:
            yield base / name


def find_named(root: Path, name: str) -> list[Path]:
    """Every entry under root named name, ignoring case.

    rglob() matches case-insensitively on Windows. Matching everywhere keeps the
    forbidden-name check at least as strict on every platform.
    """
    wanted = name.lower()
    return [path for path in iter_tree(root) if path.name.lower() == wanted]


def read_text_if_present(
    path: Path, *, encoding: str = "utf-8", errors: str = "strict"
) -> str | None:
    """Return the text of path, or None if a concurrent build removed it.

    Only FileNotFoundError counts as removal. Other failures propagate.
    """
    try:
        return path.read_text(encoding=encoding, errors=errors)
    except FileNotFoundError:
        return None
