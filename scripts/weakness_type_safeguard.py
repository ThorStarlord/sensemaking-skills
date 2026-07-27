r"""
Section-aware, duplicate-key-safe weakness_type safeguard (issue #90).

Problem this closes: Evidence 0013
(experiments/evidence/0013-stage1-auteur-run-model-enforcement/) found the
package's Part 7 safeguard script (a document-wide regex,
``re.search(r"```yaml\n(.*?)\n```", text, re.DOTALL)``) grabbed the WRONG
yaml fence -- the generated brief's Section 8 contained a malformed doubled
```yaml fence (an inner ```yaml opened without closing the outer one), and
because the regex is non-greedy and searches the WHOLE document, it matched
that first (malformed) fence instead of the real Section 13 handoff block,
and reported "no weakness_type key found" even though Section 13's real
handoff block had exactly one `weakness_type` key.

The regex also could not reliably catch duplicate `weakness_type` keys in
the first place: ordinary `yaml.safe_load` silently applies last-value-wins
on duplicate mapping keys, so even a document-wide search that happened to
grab the right fence would never see the duplication if the fence itself
had it.

Fix, two independent parts:
  1. Structural, section-scoped parsing: locate the "## 13." heading (the
     artifact-contracts.yaml-declared home of the machine-readable handoff
     block, per skills/workflow-planner/references/artifact-contracts.yaml
     and repository_sensemaking_brief's Section 13 contract), determine its
     boundaries (until the next heading of the same or higher level), and
     find the fenced ```yaml block WITHIN that section specifically --
     never the first fence in the whole document.
  2. Duplicate-key-safe YAML parsing: a custom yaml.SafeLoader subclass
     whose mapping constructor raises on a duplicate key instead of
     silently keeping the last value, scoped to the Section 13 block's own
     content (so a `weakness_type` key nested under e.g. a `metadata:` map
     elsewhere in the block is distinguished from the authoritative
     top-level key -- only the top-level key is counted).

Deliberately bounded scope: this is not a general Markdown parser. It only
implements what is needed to reliably find one named section's one fenced
yaml block and safely parse it -- nothing else.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass

import yaml

# --- Outcome taxonomy (issue #90) -------------------------------------------
#
# Every outcome is a distinct, machine-readable label. Several labels map to
# the same exit-code *group* (documented per-label below) -- the label is
# still always distinct so a caller parsing output text (not just the exit
# code) can tell them apart.

NO_AUTHORITATIVE_SECTION = "NO_AUTHORITATIVE_SECTION"        # exit 2
NO_AUTHORITATIVE_BLOCK = "NO_AUTHORITATIVE_BLOCK"             # exit 2
MALFORMED_FENCE = "MALFORMED_FENCE"                           # exit 3
ZERO_WEAKNESS_TYPE_KEYS = "ZERO_WEAKNESS_TYPE_KEYS"           # exit 2
EXACTLY_ONE_WEAKNESS_TYPE_KEY = "EXACTLY_ONE_WEAKNESS_TYPE_KEY"  # exit 0
DUPLICATE_WEAKNESS_TYPE_KEYS = "DUPLICATE_WEAKNESS_TYPE_KEYS"    # exit 1
YAML_PARSE_ERROR = "YAML_PARSE_ERROR"                          # exit 4

EXIT_CODE_BY_LABEL = {
    EXACTLY_ONE_WEAKNESS_TYPE_KEY: 0,
    DUPLICATE_WEAKNESS_TYPE_KEYS: 1,
    NO_AUTHORITATIVE_SECTION: 2,
    NO_AUTHORITATIVE_BLOCK: 2,
    ZERO_WEAKNESS_TYPE_KEYS: 2,
    MALFORMED_FENCE: 3,
    YAML_PARSE_ERROR: 4,
}

# The heading this safeguard treats as authoritative. Matches
# repository_sensemaking_brief's Section 13 heading exactly as written by
# scripts/brief_skeleton.py's build_skeleton() and
# skills/repo-sensemaker/references/repo-analysis-template.md.
DEFAULT_SECTION_HEADING_PREFIX = "## 13."

_HEADING_RE = re.compile(r"^(#{1,6})\s+\S")
_FENCE_OPEN_RE = re.compile(r"^```yaml\s*$")
_FENCE_CLOSE_RE = re.compile(r"^```\s*$")
_ANY_FENCE_MARKER_RE = re.compile(r"^```")


@dataclass(frozen=True)
class SafeguardResult:
    outcome: str
    detail: str
    weakness_type_value: object = None
    duplicate_count: int = 0

    @property
    def exit_code(self) -> int:
        return EXIT_CODE_BY_LABEL[self.outcome]


class DuplicateKeyError(Exception):
    """Raised by the dup-safe loader's mapping constructor. Not caught
    silently anywhere in this module -- callers must observe it (or the
    outcome it produces) rather than getting a last-value-wins mapping.
    """

    def __init__(self, key):
        self.key = key
        super().__init__(f"duplicate key at this mapping level: {key!r}")


class _DuplicateKeySafeLoader(yaml.SafeLoader):
    """A yaml.SafeLoader that raises DuplicateKeyError instead of silently
    keeping the last value when a mapping (at any level) has a repeated
    key. Plain yaml.safe_load can never observe this -- PyYAML's default
    mapping constructor does last-value-wins, which is exactly the gap
    Evidence 0013 identified: a document with two `weakness_type:` keys
    parses to a single value with the standard loader, so a duplicate-key
    safeguard built on yaml.safe_load can never actually detect the
    duplication it exists to catch.
    """


def _construct_mapping_no_duplicates(loader: yaml.SafeLoader, node, deep=False):
    mapping = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            raise DuplicateKeyError(key)
        value = loader.construct_object(value_node, deep=deep)
        mapping[key] = value
    return mapping


_DuplicateKeySafeLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    _construct_mapping_no_duplicates,
)


def _heading_level(line: str) -> int | None:
    m = _HEADING_RE.match(line.rstrip("\n"))
    if not m:
        return None
    return len(m.group(1))


def extract_section_body(text: str, heading_prefix: str) -> str | None:
    """Return the body of the first heading line whose stripped text starts
    with `heading_prefix` (e.g. "## 13."), i.e. everything after that
    heading line up to (not including) the next heading of the same or
    higher level. Returns None if no such heading exists.

    Heading detection is fence-aware: a line starting with "#" while inside
    a fenced code block (between an opening and closing ``` marker) is YAML
    comment syntax, not a Markdown heading, and must not be treated as a
    section boundary or as the target heading itself.
    """
    lines = text.splitlines()
    start_idx = None
    level = None
    in_fence = False
    for i, line in enumerate(lines):
        if _ANY_FENCE_MARKER_RE.match(line.rstrip()):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        lvl = _heading_level(line)
        if lvl is not None and line.strip().startswith(heading_prefix):
            start_idx = i + 1
            level = lvl
            break
    if start_idx is None:
        return None

    in_fence = False
    end_idx = len(lines)
    for j in range(start_idx, len(lines)):
        line = lines[j]
        if _ANY_FENCE_MARKER_RE.match(line.rstrip()):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        lvl = _heading_level(line)
        if lvl is not None and lvl <= level:
            end_idx = j
            break
    return "\n".join(lines[start_idx:end_idx])


def extract_single_yaml_fence(section_body: str) -> tuple[str | None, str | None]:
    """Find exactly one ```yaml ... ``` fenced block within `section_body`.

    Returns (block_content, None) on success, or (None, reason) where
    `reason` is one of "no_block" or "malformed". "malformed" covers:
    an opening ```yaml fence that is never closed; a second ```yaml-style
    opening marker encountered before the first one's closing fence
    (doubled/nested-looking opening fences -- the exact Evidence 0013
    failure mode); and more than one independent ```yaml ... ``` block
    found in the section (ambiguous -- which one is authoritative is not
    guessable, so this is reported rather than silently picking the
    first/last).
    """
    lines = section_body.splitlines()
    blocks: list[str] = []
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i].rstrip()
        if _FENCE_OPEN_RE.match(line):
            j = i + 1
            closed_at = None
            malformed = False
            while j < n:
                candidate = lines[j].rstrip()
                if _FENCE_CLOSE_RE.match(candidate):
                    closed_at = j
                    break
                if _ANY_FENCE_MARKER_RE.match(candidate):
                    # Another fence marker (e.g. a second ```yaml, or any
                    # other ``` variant) appeared before this block's own
                    # closing fence -- doubled/nested opening fence.
                    malformed = True
                    break
                j += 1
            if malformed:
                return None, "malformed"
            if closed_at is None:
                return None, "malformed"  # unterminated fence
            blocks.append("\n".join(lines[i + 1:closed_at]))
            i = closed_at + 1
        else:
            i += 1

    if not blocks:
        return None, "no_block"
    if len(blocks) > 1:
        return None, "malformed"  # multiple candidate blocks in one section
    return blocks[0], None


def _parse_dup_safe(yaml_text: str) -> tuple[dict | None, DuplicateKeyError | None, yaml.YAMLError | None]:
    try:
        data = yaml.load(yaml_text, Loader=_DuplicateKeySafeLoader)
    except DuplicateKeyError as e:
        return None, e, None
    except yaml.YAMLError as e:
        return None, None, e
    return data, None, None


def check(
    brief_text: str,
    section_heading_prefix: str = DEFAULT_SECTION_HEADING_PREFIX,
) -> SafeguardResult:
    """Deterministically classify a repository_sensemaking_brief's
    authoritative `weakness_type` field. See module docstring for the
    outcome taxonomy and why each check exists.
    """
    section_body = extract_section_body(brief_text, section_heading_prefix)
    if section_body is None:
        return SafeguardResult(
            NO_AUTHORITATIVE_SECTION,
            f"no heading found starting with {section_heading_prefix!r}",
        )

    block, reason = extract_single_yaml_fence(section_body)
    if reason == "no_block":
        return SafeguardResult(
            NO_AUTHORITATIVE_BLOCK,
            "authoritative section found but contains no ```yaml fenced block",
        )
    if reason == "malformed":
        return SafeguardResult(
            MALFORMED_FENCE,
            "authoritative section's ```yaml fence is malformed (unterminated, "
            "doubled/nested opening marker, or multiple candidate blocks) -- "
            "refusing to guess which content is authoritative",
        )

    data, dup_err, yaml_err = _parse_dup_safe(block)
    if dup_err is not None:
        if dup_err.key == "weakness_type":
            # Recover the raw occurrence count for the report, without
            # trusting a last-value-wins parse: count top-level
            # "weakness_type:" key lines directly in the fenced block text
            # (only lines with zero leading indentation, i.e. genuinely
            # top-level, not the nested-under-metadata case).
            count = sum(
                1 for line in block.splitlines()
                if re.match(r"^weakness_type\s*:", line)
            )
            return SafeguardResult(
                DUPLICATE_WEAKNESS_TYPE_KEYS,
                f"top-level 'weakness_type' key repeated {max(count, 2)} times "
                "in the authoritative Section 13 block -- HARD STOP",
                duplicate_count=max(count, 2),
            )
        return SafeguardResult(
            YAML_PARSE_ERROR,
            f"authoritative block has a duplicate key unrelated to "
            f"weakness_type ({dup_err.key!r}); refusing to parse it with a "
            f"last-value-wins loader",
        )
    if yaml_err is not None:
        return SafeguardResult(YAML_PARSE_ERROR, f"could not parse authoritative yaml block: {yaml_err}")

    if not isinstance(data, dict):
        return SafeguardResult(
            ZERO_WEAKNESS_TYPE_KEYS,
            "authoritative block did not parse to a mapping (top-level YAML "
            "type is not a dict)",
        )

    value = data.get("weakness_type")
    if "weakness_type" not in data or value is None:
        return SafeguardResult(
            ZERO_WEAKNESS_TYPE_KEYS,
            "no top-level 'weakness_type' key in the authoritative Section 13 block",
        )

    return SafeguardResult(
        EXACTLY_ONE_WEAKNESS_TYPE_KEY,
        f"exactly one top-level 'weakness_type' key found: {value!r}",
        weakness_type_value=value,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Section-aware, duplicate-key-safe weakness_type safeguard for "
                     "repository_sensemaking_brief.md (issue #90)."
    )
    parser.add_argument("brief_path", help="Path to the brief .md file")
    parser.add_argument(
        "--section-heading-prefix",
        default=DEFAULT_SECTION_HEADING_PREFIX,
        help=f"Heading-line prefix identifying the authoritative section "
             f"(default: {DEFAULT_SECTION_HEADING_PREFIX!r})",
    )
    args = parser.parse_args(argv)

    try:
        with open(args.brief_path, encoding="utf-8") as f:
            text = f.read()
    except OSError as e:
        print(f"YAML_PARSE_ERROR: could not read {args.brief_path!r}: {e}")
        return EXIT_CODE_BY_LABEL[YAML_PARSE_ERROR]

    result = check(text, args.section_heading_prefix)
    print(f"{result.outcome}: {result.detail}")
    return result.exit_code


if __name__ == "__main__":
    sys.exit(main())
