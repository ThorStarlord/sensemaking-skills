"""Test-only helper: render a Python value as Two-Lane YAML Profile v1 source.

This module delegates to the production serializer
``sensemaking_skills.campaign_validation.yaml_profile.dump_two_lane_yaml``;
it exists so tests can keep importing the familiar ``to_bytes`` helper.
"""

from __future__ import annotations

import copy
from typing import Any

from sensemaking_skills.campaign_validation.yaml_profile import (
    dump_two_lane_yaml,
)


def to_bytes(value: Any) -> bytes:
    return dump_two_lane_yaml(value).encode("utf-8")


def clone(value: Any) -> Any:
    return copy.deepcopy(value)
