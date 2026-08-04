"""Safe leaf-name validation for immutable attempt artifacts (Phase 4, #120).

Every caller-supplied name that reaches the filesystem through the
accounting runtime (produced-artifact filenames, raw-output extensions) is
frozen to one narrow lowercase ASCII leaf-name grammar. This closes path
traversal, separator injection, drive-qualified and UNC paths, Windows
ADS/colon syntax, trailing-dot/space aliasing, hidden names, and empty
names, so no caller-supplied name can resolve outside the exact attempt
directory or alias an existing file.

The grammar is the frozen contract:

    ^[a-z0-9][a-z0-9._-]*$     (starts with lowercase alphanumeric)
    no ".." substring anywhere
    no trailing "." or " "
    length 1..128 characters
    no Windows reserved-device stem (con, prn, aux, nul, com1-9, lpt1-9,
    with or without an extension)

Under this grammar a name is always a single path leaf: it contains no
separators (`/`, `\\`), no colon (`:`), no whitespace, no wildcards, and
cannot be `.` or `..`. The Windows reserved-device rejection closes the
DOS-device aliasing class (`con.md`, `nul`, `com1.log`, ...), whose names
resolve to devices rather than files on Windows and could block or raise
raw OSErrors inside the locked artifact-write path. Ordinary look-alike
names (`console.md`, `com0.md`, `com10.md`, `con-file.md`, ...) remain
valid.
"""

import re

from .failure_codes import (
    ARTIFACT_FILENAME_INVALID,
    RAW_OUTPUT_EXTENSION_INVALID,
    CampaignAccountingError,
)

#: Maximum final leaf-name length (characters). Exactly 128 is accepted;
#: 129 is rejected. Applied to the final filesystem leaf -- for raw output,
#: to the composed ``raw-output.<extension>`` name.
MAX_LEAF_NAME_LENGTH = 128

_LEAF_NAME_RE = re.compile(r"^[a-z0-9][a-z0-9._-]*$")

#: Windows reserved DOS-device stems (lowercase; uppercase already fails
#: the lowercase grammar). The stem is the portion before the first dot,
#: so both bare and extension-bearing forms are caught.
_WINDOWS_DEVICE_STEMS = frozenset(
    ["con", "prn", "aux", "nul"]
    + [f"com{i}" for i in range(1, 10)]
    + [f"lpt{i}" for i in range(1, 10)]
)


def validate_artifact_leaf_name(
    name: str,
    *,
    label: str,
    failure_code: str,
) -> None:
    """Raise ``CampaignAccountingError(failure_code)`` unless ``name`` is a
    frozen lowercase ASCII leaf name.

    ``label`` names the artifact kind in the deterministic detail string;
    ``failure_code`` distinguishes produced-artifact filenames from
    raw-output extensions.

    All rejections are purely lexical: they run before any ``resolve()``,
    ``exists()``, ``read_bytes()``, ``open()``, or campaign-state access,
    and no platform-specific exception (``OSError``, ``TimeoutError``) can
    escape as the public validation result.
    """
    if not isinstance(name, str) or name == "":
        raise CampaignAccountingError(
            failure_code,
            f"{label}: name must be a non-empty string, got {name!r}",
        )
    if _LEAF_NAME_RE.fullmatch(name) is None:
        raise CampaignAccountingError(
            failure_code,
            f"{label}: {name!r} is not a valid lowercase ASCII leaf name "
            "(must match ^[a-z0-9][a-z0-9._-]*$)",
        )
    if ".." in name:
        raise CampaignAccountingError(
            failure_code,
            f"{label}: {name!r} contains a '..' sequence and is rejected",
        )
    if name.endswith((".", " ")):
        raise CampaignAccountingError(
            failure_code,
            f"{label}: {name!r} ends with a trailing dot or space and is "
            "rejected (filesystem aliasing)",
        )
    if len(name) > MAX_LEAF_NAME_LENGTH:
        raise CampaignAccountingError(
            failure_code,
            f"{label}: {name!r} is {len(name)} characters long; the maximum "
            f"leaf-name length is {MAX_LEAF_NAME_LENGTH}",
        )
    stem = name.split(".", 1)[0]
    if stem in _WINDOWS_DEVICE_STEMS:
        raise CampaignAccountingError(
            failure_code,
            f"{label}: {name!r} uses the Windows reserved device stem "
            f"'{stem}' and is rejected",
        )


def validate_produced_artifact_filename(name: str) -> None:
    """Validate a produced-artifact leaf name (``ARTIFACT_FILENAME_INVALID``)."""
    validate_artifact_leaf_name(
        name, label="produced artifact filename", failure_code=ARTIFACT_FILENAME_INVALID
    )


def validate_raw_output_extension(extension: str) -> None:
    """Validate a raw-output extension fragment.

    The extension is composed into ``raw-output.<extension>`` and the whole
    leaf name is checked under the same grammar
    (``RAW_OUTPUT_EXTENSION_INVALID``).
    """
    composed = f"raw-output.{extension}" if extension else "raw-output."
    validate_artifact_leaf_name(
        composed, label="raw-output extension", failure_code=RAW_OUTPUT_EXTENSION_INVALID
    )
