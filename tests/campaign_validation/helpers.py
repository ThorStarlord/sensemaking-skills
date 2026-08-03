"""Test-only helper: render a Python value as Two-Lane YAML Profile v1 source.

This is NOT a production parser/dumper -- it exists purely so tests can
build valid Two-Lane v1 fixture documents from plain Python dict/list
literals without hand-writing YAML strings for every case. Every string
value is quoted; every mapping key is emitted unquoted plain ASCII;
booleans/None/numbers are emitted unquoted, matching exactly what
``parse_two_lane_yaml`` accepts.
"""

from __future__ import annotations

import copy
from typing import Any


def _quote(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")
    return f'"{escaped}"'


def _render_scalar(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return repr(value) if isinstance(value, float) else str(value)
    if isinstance(value, str):
        return _quote(value)
    raise TypeError(f"not a scalar: {value!r}")


def dump_two_lane_yaml(value: Any, indent: int = 0) -> str:
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
                inner = dump_two_lane_yaml(item, indent + 1).lstrip()
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


def to_bytes(value: Any) -> bytes:
    return dump_two_lane_yaml(value).encode("utf-8")


def clone(value: Any) -> Any:
    return copy.deepcopy(value)
