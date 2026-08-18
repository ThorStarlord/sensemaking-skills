from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SKILL = ROOT / "skills" / "repo-sensemaker" / "SKILL.md"
CONTRACT = (
    ROOT
    / "skills"
    / "repo-sensemaker"
    / "references"
    / "connector-native-probe.md"
)


def test_repo_sensemaker_selects_probe_backend_by_authorized_surface() -> None:
    skill = SKILL.read_text(encoding="utf-8")

    assert "state-currency probe" in skill.lower()
    assert "github_connector_exact_sha_v1" in skill
    assert "references/connector-native-probe.md" in skill
    assert "python scripts/probe-repo.py --repo-root <target-repo>" in skill
    assert "No third implicit probe path" in skill


def test_connector_native_probe_is_exact_sha_and_fail_closed() -> None:
    contract = CONTRACT.read_text(encoding="utf-8")

    required_phrases = (
        "github_connector_exact_sha_v1",
        "exact target SHA",
        "GitHub-supplied blob SHA",
        "No local target checkout is required or implied",
        "No mutable branch tip may substitute for the exact target SHA",
        "No unavailable metric may be fabricated",
        "verification_gap.vg",
        "context_entropy.ce",
        "fixtures_coverage.coverage",
        "churn",
        "escalation_recommended: true",
    )
    for phrase in required_phrases:
        assert phrase in contract


def test_connector_native_probe_separates_snapshot_from_live_metadata() -> None:
    contract = CONTRACT.read_text(encoding="utf-8")

    assert "exact-SHA tree/file/blob observations" in contract
    assert "live GitHub metadata" in contract
    assert "verified only at its observation time" in contract
    assert "unmeasured on this surface" in contract
