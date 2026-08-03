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

import yaml
from yaml import (
    AliasToken,
    AnchorToken,
    DirectiveToken,
    ScalarToken,
    TagToken,
)

__all__ = [
    "TwoLaneYamlError",
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

    # Explicit-key '?' indicator: heuristic, line-anchored detection. Aliases,
    # anchors, and tags are already rejected above; a bare '?' introducing a
    # mapping key is a source-form construct this profile does not support.
    for line in source_text.splitlines():
        stripped = line.strip()
        if stripped == "?" or stripped.startswith("? "):
            raise TwoLaneYamlError(
                "EXPLICIT_KEY_FORBIDDEN",
                "explicit '?' key syntax is forbidden",
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
            value = float(raw)
        else:
            value = int(raw)
        if isinstance(value, float) and value == 0.0:
            import math

            if math.copysign(1.0, value) < 0:
                raise TwoLaneYamlError("NEGATIVE_ZERO_FORBIDDEN", "-0 is forbidden")
        return value

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
