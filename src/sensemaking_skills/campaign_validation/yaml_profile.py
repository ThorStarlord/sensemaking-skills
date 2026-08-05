"""Two-Lane YAML Profile v1 parser (ADR 0023 section 10b).

Promotes the profile behavior proven in
``tests/test_two_lane_schema_contracts.py`` (documentation-level checks
only) into production code. This module is the single normative parser for
every digest-bearing Two-Lane v1 artifact; nothing else in this package may
use ``yaml.safe_load`` as a substitute.

Two layers, matching ADR 0023 section 10b exactly:

* **Layer A** -- source-token validation. Inspects the raw token stream
  (via ``yaml.scan``) *before* any composition happens, so it can reject
  anchors, aliases, tags, directives, multiple documents, and block/folded
  scalar styles even for input that would otherwise fail to compose.
* **Layer B** -- composed-node interpretation. Walks the composed node
  graph (via ``yaml.compose``) and builds the restricted JSON-compatible
  data model using the profile's own lexical scalar-resolution rules,
  never PyYAML's default (YAML-1.1-flavored) resolver.

Schema (field/type) validation is a separate, later stage (``schema_validation``
module) -- this module only establishes source-form and structural legality
plus the restricted JSON-compatible value.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

import math
from decimal import Decimal, InvalidOperation

import yaml
from yaml import (
    AliasToken,
    AnchorToken,
    DirectiveToken,
    KeyToken,
    ScalarToken,
    TagToken,
)

__all__ = [
    "TwoLaneYamlError",
    "dump_two_lane_yaml",
    "parse_two_lane_yaml",
]


class TwoLaneYamlError(ValueError):
    """Raised for any Two-Lane YAML Profile v1 violation.

    ``code`` is a short machine-stable reason token; ``message`` is a
    human-readable detail. Both are attributes so callers can build stable
    failure codes without parsing the exception string.
    """

    def __init__(self, code: str, message: str):
        super().__init__(f"{code}: {message}")
        self.code = code
        self.message = message


_MAPPING_KEY_RE = re.compile(r"^[a-z][a-z0-9_]*$")
_RESERVED_KEYS = frozenset({"true", "false", "null", "yes", "no", "on", "off"})

# RFC 8259 JSON-number grammar, used verbatim as the plain-scalar number test
# (ADR 0023 section 10b).
_JSON_NUMBER_RE = re.compile(r"^-?(0|[1-9][0-9]*)(\.[0-9]+)?([eE][+-]?[0-9]+)?$")


# ---------------------------------------------------------------------------
# Layer A: source-token validation
# ---------------------------------------------------------------------------

def _layer_a_validate_tokens(source_text: str) -> None:
    """Reject forbidden source-level constructs before any composition.

    Operates purely on the token stream produced by ``yaml.scan`` -- this
    runs even when the document could not be composed at all, which matters
    for e.g. an alias with no matching anchor (a composition-time error in
    PyYAML) -- Layer A must still independently identify the alias token
    itself, not rely on the downstream composer error to satisfy the
    assertion.
    """
    try:
        tokens = list(yaml.scan(source_text))
    except yaml.YAMLError as exc:
        raise TwoLaneYamlError("MALFORMED_YAML", str(exc)) from exc

    for tok in tokens:
        if isinstance(tok, KeyToken):
            # Explicit-key '?' indicator, detected at the token/source-position
            # level (not by scanning raw source lines): a KeyToken's
            # start_mark points at the '?' character itself only for an
            # EXPLICIT key ('? key' block form, or '{? key: value}' flow
            # form); for an ordinary simple key, PyYAML synthesizes the
            # KeyToken at the same position as the key scalar itself (no '?'
            # character precedes it there). Checking the literal source byte
            # at the token's own start position -- rather than line-anchored
            # text scanning -- means a '?' inside a quoted string value or a
            # comment is never misclassified as an explicit-key indicator.
            mark = tok.start_mark
            if mark.buffer is not None and 0 <= mark.pointer < len(mark.buffer) \
                    and mark.buffer[mark.pointer] == "?":
                raise TwoLaneYamlError(
                    "EXPLICIT_KEY_FORBIDDEN",
                    "explicit '?' key syntax is forbidden",
                )
        if isinstance(tok, AliasToken):
            raise TwoLaneYamlError("ALIAS_FORBIDDEN", "YAML aliases are forbidden")
        if isinstance(tok, AnchorToken):
            raise TwoLaneYamlError("ANCHOR_FORBIDDEN", "YAML anchors are forbidden")
        if isinstance(tok, TagToken):
            raise TwoLaneYamlError("TAG_FORBIDDEN", "explicit YAML tags are forbidden")
        if isinstance(tok, DirectiveToken):
            name = tok.name
            if name == "YAML":
                major_minor = tuple(str(part) for part in tok.value)
                if major_minor != ("1", "2"):
                    raise TwoLaneYamlError(
                        "YAML_VERSION_FORBIDDEN",
                        f"only %YAML 1.2 is permitted, got {major_minor}",
                    )
            else:
                # %TAG and any other directive.
                raise TwoLaneYamlError(
                    "DIRECTIVE_FORBIDDEN", f"unknown/forbidden directive {name!r}"
                )
        if isinstance(tok, ScalarToken):
            style = tok.style
            if style in ("|", ">"):
                raise TwoLaneYamlError(
                    "BLOCK_SCALAR_FORBIDDEN",
                    "literal/folded block scalars are forbidden",
                )
            if style in ("'", '"'):
                if tok.start_mark.line != tok.end_mark.line:
                    raise TwoLaneYamlError(
                        "MULTILINE_QUOTED_SCALAR_FORBIDDEN",
                        "physically multiline quoted strings are forbidden",
                    )


# ---------------------------------------------------------------------------
# Layer B: composed-node interpretation
# ---------------------------------------------------------------------------

class _NoImplicitResolver(yaml.SafeLoader):
    """A loader whose only purpose is composing nodes with no scalar
    resolution baked in -- Layer B does its own scalar interpretation, never
    PyYAML's YAML-1.1-flavored default resolver.
    """


# Remove every implicit resolver PyYAML's SafeLoader ships with (bool, int,
# float, timestamp, merge, null, ...). Explicit tags are already rejected in
# Layer A, so by the time Layer B runs, every scalar node is untagged
# (PyYAML's Resolver falls back to ``tag:yaml.org,2002:str`` when no
# implicit resolver matches and no explicit tag is present).
_NoImplicitResolver.yaml_implicit_resolvers = {}


def _compose(source_text: str) -> Any:
    try:
        nodes = list(yaml.compose_all(source_text, Loader=_NoImplicitResolver))
    except yaml.YAMLError as exc:
        raise TwoLaneYamlError("MALFORMED_YAML", str(exc)) from exc
    if len(nodes) > 1:
        raise TwoLaneYamlError(
            "MULTIPLE_DOCUMENTS_FORBIDDEN", "only one YAML document is permitted"
        )
    if not nodes or nodes[0] is None:
        raise TwoLaneYamlError("EMPTY_DOCUMENT", "document is empty")
    return nodes[0]


def _parse_exact_float(raw: str) -> float:
    """Parse a decimal/exponent JSON-number lexeme with exact Decimal analysis.

    ``float(raw)`` alone is not sufficient: Python's ``float()`` silently
    returns ``inf``/``0.0`` for lexemes whose exact decimal value overflows
    or underflows binary64, and it silently rounds a lexeme with more
    precision than binary64 can represent (e.g. ``0.10000000000000001``
    rounds to the same bits as ``0.1``) with no signal that anything was
    lost. This function instead parses the lexeme exactly as a ``Decimal``
    first, converts to ``float``, and rejects (fails closed) whenever that
    conversion is not value-preserving, per ADR 0023 section 10b's number
    domain rules.
    """
    try:
        exact = Decimal(raw)
    except InvalidOperation as exc:  # pragma: no cover - regex already restricts form
        raise TwoLaneYamlError("NUMERIC_PRECISION_UNSUPPORTED", str(exc)) from exc

    value = float(raw)

    if math.isinf(value):
        raise TwoLaneYamlError(
            "NUMERIC_OVERFLOW", f"{raw!r} overflows the binary64 domain"
        )
    if value == 0.0:
        if math.copysign(1.0, value) < 0:
            raise TwoLaneYamlError("NEGATIVE_ZERO_FORBIDDEN", "-0 is forbidden")
        if exact != 0:
            raise TwoLaneYamlError(
                "NUMERIC_UNDERFLOW", f"{raw!r} underflows to zero in binary64"
            )
        return value

    # Round-trip fidelity: the exact decimal lexeme must equal the exact
    # decimal value of the binary64 result (Python's `repr(float)` is the
    # shortest string that round-trips to that exact binary64 value). If
    # they differ, `raw` carried more precision than binary64/JCS can
    # preserve -- fail closed rather than silently rounding.
    if exact != Decimal(repr(value)):
        raise TwoLaneYamlError(
            "NUMERIC_PRECISION_UNSUPPORTED",
            f"{raw!r} cannot be represented exactly as a JCS/binary64 number",
        )
    return value


def _resolve_scalar(node: yaml.ScalarNode, *, is_key: bool) -> Any:
    style = node.style
    raw = node.value

    if style in ("'", '"'):
        return raw  # PyYAML already decoded escapes/quoting into `raw`.
    if style in ("|", ">"):  # pragma: no cover - Layer A already rejects this
        raise TwoLaneYamlError("BLOCK_SCALAR_FORBIDDEN", "block scalar forbidden")

    # Plain scalar: restricted resolution per ADR 0023 section 10b.
    if raw == "null":
        return None
    if raw == "true":
        return True
    if raw == "false":
        return False
    if _JSON_NUMBER_RE.match(raw):
        if "." in raw or "e" in raw or "E" in raw:
            return _parse_exact_float(raw)
        # Integer-lexeme scalar (no '.' or exponent in source): parsed as a
        # genuine Python ``int``, exactly, with no binary64 rounding --
        # arbitrary precision, so a value like 9007199254740992 round-trips
        # exactly here (a downstream safe-integer-range check is a distinct,
        # field-specific concern, not a parser concern). This int/float type
        # split is deliberately preserved rather than normalized away: it IS
        # the "scalar-source metadata" the integer-lexeme policy fields
        # (max_attempt_slots, etc.) need in order to reject a float-lexeme
        # value like ``5.0``/``5e0`` even though it is mathematically
        # integral. See ``validators.py::_require_integer_lexeme``.
        if raw == "-0":
            # The integer-lexeme grammar (`-?(0|[1-9][0-9]*)`, no leading
            # zeros permitted) has exactly one zero spelling, "0"; the only
            # way a negative sign reaches this branch on a zero-valued
            # lexeme is the literal string "-0" itself. `int("-0")` silently
            # collapses to ordinary `0`, discarding the sign -- reject at
            # the parser boundary instead, exactly like the float path
            # already does for `-0.0`/`-0e0`/etc., so a bare `-0` can never
            # reach ANY numeric field (policy integer fields,
            # `cost_ceiling.amount`, `execution_parameters` at any nesting
            # depth, or any other numeric field) as ordinary zero.
            raise TwoLaneYamlError("NEGATIVE_ZERO_FORBIDDEN", "-0 is forbidden")
        return int(raw)

    raise TwoLaneYamlError(
        "PLAIN_SCALAR_FORBIDDEN",
        f"unquoted plain scalar {raw!r} is not a permitted form "
        "(quote it if it is meant to be a string)",
    )


def _validate_key_grammar(key: str, *, open_subtree: bool) -> None:
    if not _MAPPING_KEY_RE.match(key):
        raise TwoLaneYamlError(
            "MAPPING_KEY_GRAMMAR_VIOLATION",
            f"mapping key {key!r} does not match ^[a-z][a-z0-9_]*$",
        )
    if key in _RESERVED_KEYS:
        raise TwoLaneYamlError(
            "RESERVED_KEY_FORBIDDEN", f"mapping key {key!r} is reserved"
        )


def _compose_value(node: yaml.Node, *, open_subtree: bool,
                    open_map_root_field: str | None) -> Any:
    if isinstance(node, yaml.ScalarNode):
        return _resolve_scalar(node, is_key=False)

    if isinstance(node, yaml.SequenceNode):
        return [
            _compose_value(item, open_subtree=open_subtree,
                            open_map_root_field=open_map_root_field)
            for item in node.value
        ]

    if isinstance(node, yaml.MappingNode):
        result: dict[str, Any] = {}
        seen: set[str] = set()
        for key_node, value_node in node.value:
            if not isinstance(key_node, yaml.ScalarNode):
                raise TwoLaneYamlError(
                    "COMPLEX_KEY_FORBIDDEN", "mapping keys must be plain scalars"
                )
            if key_node.style is not None:
                raise TwoLaneYamlError(
                    "QUOTED_KEY_FORBIDDEN", "mapping keys must be unquoted"
                )
            key = key_node.value
            _validate_key_grammar(key, open_subtree=open_subtree)
            if key in seen:
                raise TwoLaneYamlError(
                    "DUPLICATE_KEY_FORBIDDEN", f"duplicate mapping key {key!r}"
                )
            seen.add(key)

            child_open = open_subtree or (
                open_map_root_field is not None and key == open_map_root_field
            )
            result[key] = _compose_value(
                value_node,
                open_subtree=child_open,
                open_map_root_field=open_map_root_field if not child_open else None,
            )
        return result

    raise TwoLaneYamlError(
        "UNSUPPORTED_NODE_TYPE", f"unsupported node type {type(node).__name__}"
    )


def parse_two_lane_yaml(source_bytes: bytes, *,
                         open_map_root_field: str | None = None) -> Any:
    """Parse ``source_bytes`` under the Two-Lane YAML Profile v1.

    Args:
        source_bytes: Raw UTF-8 bytes of the YAML source (never a
            pre-decoded string -- callers must not paper over decode
            failures).
        open_map_root_field: The name of the sole top-level field whose
            value begins an open-map subtree (``execution_parameters`` for
            ``configuration-identity.schema.md``). ``None`` for schemas with
            no open-map field (campaign policy, campaign approval).

    Returns:
        A JSON-compatible value: ``dict``/``list``/``str``/``int``/
        ``float``/``bool``/``None``.

    Raises:
        TwoLaneYamlError: on any profile violation. ``.code`` gives a stable
            machine reason.
    """
    if not isinstance(source_bytes, (bytes, bytearray)):
        raise TwoLaneYamlError(
            "SOURCE_NOT_BYTES", "source must be raw bytes, not str"
        )
    try:
        source_text = source_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise TwoLaneYamlError("INVALID_UTF8", str(exc)) from exc

    if source_text.strip() == "":
        raise TwoLaneYamlError("EMPTY_DOCUMENT", "document is empty")

    _layer_a_validate_tokens(source_text)
    node = _compose(source_text)

    if not isinstance(node, yaml.MappingNode):
        raise TwoLaneYamlError(
            "ROOT_NOT_MAPPING", "top-level document must be a mapping"
        )

    return _compose_value(node, open_subtree=False,
                           open_map_root_field=open_map_root_field)


def _render_scalar(value: Any) -> str:
    """Render one scalar as Two-Lane YAML Profile v1 source.

    Every string is quoted (escaped); booleans/None/numbers are emitted
    unquoted. Mirrors exactly what ``parse_two_lane_yaml`` accepts.
    """
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return repr(value) if isinstance(value, float) else str(value)
    if isinstance(value, str):
        escaped = (
            value.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")
        )
        return f'"{escaped}"'
    raise TwoLaneYamlError(
        "NOT_A_SCALAR", f"cannot render non-scalar value {value!r} as YAML"
    )


def dump_two_lane_yaml(value: Any, indent: int = 0) -> str:
    """Render a JSON-compatible Python value as Two-Lane YAML Profile v1
    source text (the production counterpart of the test-only dumper).

    Every string value is quoted; mapping keys are emitted unquoted plain
    ASCII; booleans/None/numbers are emitted unquoted -- exactly what
    ``parse_two_lane_yaml`` accepts, so ``dump_two_lane_yaml(x)`` then
    ``parse_two_lane_yaml`` round-trips ``x``.
    """
    pad = "  " * indent
    if isinstance(value, dict):
        if not value:
            return pad + "{}\n"
        lines = []
        for k, v in value.items():
            if isinstance(v, dict) and v:
                lines.append(f"{pad}{k}:")
                lines.append(dump_two_lane_yaml(v, indent + 1).rstrip("\n"))
            elif isinstance(v, list) and v:
                lines.append(f"{pad}{k}:")
                lines.append(dump_two_lane_yaml(v, indent).rstrip("\n"))
            elif isinstance(v, dict):
                lines.append(f"{pad}{k}: {{}}")
            elif isinstance(v, list):
                lines.append(f"{pad}{k}: []")
            else:
                lines.append(f"{pad}{k}: {_render_scalar(v)}")
        return "\n".join(lines) + "\n"
    if isinstance(value, list):
        if not value:
            return pad + "[]\n"
        lines = []
        for item in value:
            if isinstance(item, dict):
                sub_lines = dump_two_lane_yaml(item, indent + 1).split("\n")
                first = sub_lines[0].strip()
                lines.append(f"{pad}- {first}")
                for extra in sub_lines[1:]:
                    if extra.strip():
                        lines.append(extra)
            elif isinstance(item, list):
                lines.append(f"{pad}-")
                lines.append(dump_two_lane_yaml(item, indent + 1).rstrip("\n"))
            else:
                lines.append(f"{pad}- {_render_scalar(item)}")
        return "\n".join(lines) + "\n"
    return pad + _render_scalar(value) + "\n"
