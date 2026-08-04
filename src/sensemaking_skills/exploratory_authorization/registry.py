"""Process-local issuer registry for exploratory capabilities.

The registry is the ONLY liveness authority: an object that is not a live
issuance of this registry is dead, regardless of what attributes it
carries. Transitions are single-state-machine, guarded by one lock:

    ISSUED -> CONSUMING -> CONSUMED   (normal consumption)
    ISSUED/CONSUMING/CONSUMED -> DEAD (burn: drift, expiry, provider failure)

Consumption is atomic in two stages:

- ``begin_consume`` performs the ISSUED -> CONSUMING transition under the
  lock; exactly one caller wins, everyone else observes the current state
  (and maps it to a failure code).
- ``complete_consume`` / ``fail_consume`` finalize CONSUMING after the
  binding validation and (test-only) critical-section hook.
"""

from __future__ import annotations

import threading
from enum import Enum
from typing import Optional


class CapabilityState(Enum):
    ISSUED = "issued"
    CONSUMING = "consuming"
    CONSUMED = "consumed"
    DEAD = "dead"


class ExploratoryCapabilityRegistry:
    """One process-local registry; duplicate attempt ids are rejected."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._states: dict[str, CapabilityState] = {}
        self._attempt_ids: set[str] = set()

    def issue(self, capability_id: str, attempt_id: str) -> bool:
        """Register a new issuance. Returns False if the attempt id is
        already issued in this process (duplicate)."""
        with self._lock:
            if attempt_id in self._attempt_ids:
                return False
            self._attempt_ids.add(attempt_id)
            self._states[capability_id] = CapabilityState.ISSUED
            return True

    def state(self, capability_id: str) -> Optional[CapabilityState]:
        with self._lock:
            return self._states.get(capability_id)

    def is_live(self, capability_id: Optional[str]) -> bool:
        if capability_id is None:
            return False
        return self.state(capability_id) is CapabilityState.ISSUED

    def is_spent(self, capability_id: Optional[str]) -> bool:
        if capability_id is None:
            return False
        state = self.state(capability_id)
        return state in (CapabilityState.CONSUMED, CapabilityState.DEAD)

    def begin_consume(self, capability_id: str) -> CapabilityState:
        """Atomically claim ISSUED -> CONSUMING. Returns the observed state
        (ISSUED if this caller won, anything else if they lost)."""
        with self._lock:
            state = self._states.get(capability_id)
            if state is CapabilityState.ISSUED:
                self._states[capability_id] = CapabilityState.CONSUMING
            return self._states.get(capability_id)

    def complete_consume(self, capability_id: str) -> None:
        with self._lock:
            self._states[capability_id] = CapabilityState.CONSUMED

    def fail_consume(self, capability_id: str) -> None:
        with self._lock:
            self._states[capability_id] = CapabilityState.DEAD

    def burn(self, capability_id: str) -> None:
        """Any state -> DEAD. Permanently spent, unrecoverable."""
        with self._lock:
            self._states[capability_id] = CapabilityState.DEAD

    def reset(self) -> None:
        """Test-only: wipe all issuances (fresh process-local state)."""
        with self._lock:
            self._states.clear()
            self._attempt_ids.clear()


#: The process-local singleton. Capabilities bind to whichever registry
#: issued them; forged objects consult nothing and are dead.
_registry = ExploratoryCapabilityRegistry()


def get_exploratory_registry() -> ExploratoryCapabilityRegistry:
    return _registry


def reset_exploratory_registry() -> None:
    """Test-only: reset the process-local registry to empty."""
    _registry.reset()
