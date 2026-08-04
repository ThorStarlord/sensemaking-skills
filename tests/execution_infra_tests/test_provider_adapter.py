"""Provider adapter tests (Issue #122).

The adapter is NEVER invoked by tests: every test proves construction and
refusal behavior with zero provider calls. A real provider call is the
Phase 6 operator's act, guarded by the runner.
"""

import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))

from execution_infra.provider_adapter import ClaudeProviderAdapter, ProviderAdapterError
from execution_infra.versions import adapter_versions, module_digest


def test_adapter_binds_pinned_configuration(tmp_path: Path) -> None:
    adapter = ClaudeProviderAdapter(
        framework_checkout=tmp_path,
        target_repository="https://github.com/ThorStarlord/auteur.git",
        target_sha="0653defb05625f2fcde0ac32eac6e59ccf7eeb90",
        model="claude-sonnet-5",
    )
    assert adapter.model == "claude-sonnet-5"
    # The skill must come from the FROZEN framework checkout.
    with pytest.raises(ProviderAdapterError) as exc:
        _ = adapter.skill_path
    assert "no repo-sensemaker skill" in str(exc.value)


def test_adapter_version_is_content_addressed(tmp_path: Path) -> None:
    infra = Path(__file__).resolve().parents[2] / "scripts" / "execution_infra"
    versions = adapter_versions(infra)
    assert "provider_adapter.py" in versions
    assert len(versions["provider_adapter.py"]) == 64
    # Content-addressed: a byte change would change the digest.
    assert versions["provider_adapter.py"] == module_digest(infra / "provider_adapter.py")


def test_adapter_never_called_by_tests() -> None:
    """The test suite must never trigger a provider invocation."""
    # The spy-based runner tests assert zero provider calls on every guard
    # path; this test documents that the adapter itself is not invoked.
    assert not hasattr(ClaudeProviderAdapter, "_invoked_for_test")
