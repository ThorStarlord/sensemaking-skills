"""Responsibility-to-capability metadata without semantic routing."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable, Optional

from .models import Authority, Capability


class AvailabilityStatus(str, Enum):
    AVAILABLE = "available"
    UNAVAILABLE = "unavailable"
    EXTERNAL = "external"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class RegisteredCapability:
    capability: Capability
    kind: str
    mutates_repository: bool
    authority: Authority
    availability: AvailabilityStatus
    returns_control: bool = True
    availability_reason: str = ""


@dataclass(frozen=True)
class RegistryDiagnostic:
    code: str
    detail: str


class CapabilityRegistry:
    """A catalog the agent may inspect; it never chooses for the agent."""

    def __init__(self, capabilities: Iterable[RegisteredCapability] = ()):
        self._items = {item.capability.id: item for item in capabilities}

    def register(self, item: RegisteredCapability) -> None:
        self._items[item.capability.id] = item

    def get(self, capability_id: str) -> Optional[RegisteredCapability]:
        return self._items.get(capability_id)

    def candidates(self, responsibility_type: str) -> tuple[RegisteredCapability, ...]:
        return tuple(item for item in self._items.values()
                     if responsibility_type in item.capability.accepted_responsibility_types)

    def validate_reference(self, capability_id: Optional[str], executable: bool = False) -> tuple[RegistryDiagnostic, ...]:
        if capability_id is None:
            return ()
        item = self.get(capability_id)
        if item is None:
            return (RegistryDiagnostic("UNKNOWN_CAPABILITY", f"capability {capability_id!r} is not registered"),)
        diagnostics = []
        if not item.capability.output_artifact:
            diagnostics.append(RegistryDiagnostic("MISSING_OUTPUT_ARTIFACT", f"capability {capability_id!r} has no output contract"))
        if item.kind == "workflow" and not item.returns_control:
            diagnostics.append(RegistryDiagnostic("WORKFLOW_MISSING_RETURN_CONTROL", f"workflow {capability_id!r} must return control to the campaign agent"))
        if executable and item.availability is not AvailabilityStatus.AVAILABLE:
            diagnostics.append(RegistryDiagnostic("CAPABILITY_NOT_AVAILABLE", f"capability {capability_id!r} is {item.availability.value}"))
        return tuple(diagnostics)

    def ids(self) -> tuple[str, ...]:
        return tuple(sorted(self._items))
