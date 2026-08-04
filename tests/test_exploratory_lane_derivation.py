"""Phase 3 (#119): lane-derivation matrix for the provider boundary.

The four-lane model (ORDINARY / CANONICAL / EXPLORATORY / AMBIGUOUS) is
derived from the ACTUAL invocation (identity + declared exploratory
identity), never from a capability, a boolean, an environment variable, or
a caller-supplied string of any other kind.

Rules under test (task brief sections 2-4, 9):

- CONTROLLED_STAGE1 always maps to CANONICAL; a declared exploratory
  identity can never override a canonical signal.
- ORDINARY_DEVELOPMENT maps to ORDINARY only when NO exploratory claim is
  made; an exploratory claim on an ordinary-classified invocation is
  mixed evidence and maps to AMBIGUOUS.
- AMBIGUOUS maps to EXPLORATORY only when the ambiguity is exactly the
  experiments-namespace floor, the declared exploratory identity is
  well-formed, and the output path is inside
  ``experiments/campaigns/<declared campaign_id>/``. Everything else
  stays AMBIGUOUS (fails closed; requires a canonical AuthorizedInvocation).
"""

from __future__ import annotations

import sys
import uuid
from pathlib import Path

import pytest

REPO_ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT_DIR / "scripts"))

import gate_a_authorization as ga  # noqa: E402

FRAMEWORK_ROOT = "C:/phase3-tests/example-repo"

VALID_ATTEMPT_ID = "a1b2c3d4-e5f6-4789-8abc-def012345678"
VALID_CONFIGURATION_ID = "1111111111111111111111111111111111111111111111111111111111111111"
CAMPAIGN_ID = "EXP-0001-alpha"


def _campaign_output_path() -> str:
    return f"{FRAMEWORK_ROOT}/experiments/campaigns/{CAMPAIGN_ID}/attempts/attempt-1.md"


def _ordinary_output_path() -> str:
    return f"{FRAMEWORK_ROOT}/artifacts/brief.md"


def _evidence_output_path() -> str:
    return f"{FRAMEWORK_ROOT}/experiments/evidence/0016-sensemaking/summary.md"


def _experiments_non_campaign_path() -> str:
    return f"{FRAMEWORK_ROOT}/experiments/scratch/notes.md"


def _declared(campaign_id=CAMPAIGN_ID, classification="EXPLORATORY_NOT_CANONICAL_EVIDENCE",
              attempt_id=VALID_ATTEMPT_ID, configuration_id=VALID_CONFIGURATION_ID):
    return ga.DeclaredExploratory(
        campaign_id=campaign_id,
        classification=classification,
        attempt_id=attempt_id,
        configuration_id=configuration_id,
    )


def _identity(*, output_path, declared_controlled_mode=None):
    return ga.InvocationIdentity.build(
        workflow_id="phase3-test-workflow",
        workflow_stage="stage-3",
        artifact_type="attempt_result",
        output_path=output_path,
        framework_root=FRAMEWORK_ROOT,
        target_repository="https://example.invalid/example-owner/example-target.git",
        target_sha="000000000000000000000000000000000000beef",
        requested_model="example-model-identifier",
        executor_id="test-executor",
        declared_controlled_mode=declared_controlled_mode,
    )


# ---------------------------------------------------------------------------
# Lane constants
# ---------------------------------------------------------------------------


def test_lane_constants_are_four_distinct_strings():
    lanes = {ga.LANE_ORDINARY, ga.LANE_CANONICAL, ga.LANE_EXPLORATORY, ga.LANE_AMBIGUOUS}
    assert len(lanes) == 4
    assert ga.LANE_ORDINARY == "ORDINARY"
    assert ga.LANE_CANONICAL == "CANONICAL"
    assert ga.LANE_EXPLORATORY == "EXPLORATORY"
    assert ga.LANE_AMBIGUOUS == "AMBIGUOUS"


# ---------------------------------------------------------------------------
# EXPLORATORY: the happy, exact conditions
# ---------------------------------------------------------------------------


def test_campaign_output_with_well_formed_declaration_is_exploratory():
    identity = _identity(output_path=_campaign_output_path())
    lane, signals = ga.derive_authorization_lane(identity, _declared())
    assert lane == ga.LANE_EXPLORATORY
    assert "output_under_experiments_namespace" in signals


def test_campaign_output_with_campaign_id_having_no_suffix_is_exploratory():
    identity = _identity(
        output_path=f"{FRAMEWORK_ROOT}/experiments/campaigns/EXP-0002/attempts/one.md"
    )
    lane, _ = ga.derive_authorization_lane(identity, _declared(campaign_id="EXP-0002"))
    assert lane == ga.LANE_EXPLORATORY


# ---------------------------------------------------------------------------
# AMBIGUOUS: every deviation stays fail-closed
# ---------------------------------------------------------------------------


def test_campaign_output_without_declaration_is_ambiguous():
    identity = _identity(output_path=_campaign_output_path())
    lane, _ = ga.derive_authorization_lane(identity, None)
    assert lane == ga.LANE_AMBIGUOUS


def test_campaign_output_with_malformed_campaign_id_is_ambiguous():
    identity = _identity(output_path=_campaign_output_path())
    assert ga.derive_authorization_lane(identity, _declared(campaign_id="EXP-X"))[0] == ga.LANE_AMBIGUOUS
    assert ga.derive_authorization_lane(identity, _declared(campaign_id=""))[0] == ga.LANE_AMBIGUOUS
    assert ga.derive_authorization_lane(identity, _declared(campaign_id="0016-brief"))[0] == ga.LANE_AMBIGUOUS


def test_campaign_output_with_wrong_classification_is_ambiguous():
    identity = _identity(output_path=_campaign_output_path())
    lane, _ = ga.derive_authorization_lane(identity, _declared(classification="CANONICAL_EVIDENCE"))
    assert lane == ga.LANE_AMBIGUOUS
    lane, _ = ga.derive_authorization_lane(identity, _declared(classification=""))
    assert lane == ga.LANE_AMBIGUOUS


def test_campaign_output_with_non_uuid_attempt_id_is_ambiguous():
    identity = _identity(output_path=_campaign_output_path())
    for bad in ("not-a-uuid", "", "00000000-0000-0000-0000-000000000000Z", str(uuid.uuid4()).upper()):
        lane, _ = ga.derive_authorization_lane(identity, _declared(attempt_id=bad))
        assert lane == ga.LANE_AMBIGUOUS


def test_campaign_output_with_malformed_configuration_id_is_ambiguous():
    identity = _identity(output_path=_campaign_output_path())
    for bad in ("", "abc", "1111111111111111111111111111111111111111111111111111111111111111ZZ",
                ("f" * 64).upper()):
        lane, _ = ga.derive_authorization_lane(identity, _declared(configuration_id=bad))
        assert lane == ga.LANE_AMBIGUOUS


def test_declared_campaign_mismatching_path_namespace_is_ambiguous():
    identity = _identity(output_path=_campaign_output_path())
    lane, _ = ga.derive_authorization_lane(identity, _declared(campaign_id="EXP-0002-other"))
    assert lane == ga.LANE_AMBIGUOUS


def test_declared_campaign_case_variant_of_path_namespace_is_ambiguous():
    identity = _identity(output_path=_campaign_output_path())
    lane, _ = ga.derive_authorization_lane(identity, _declared(campaign_id=CAMPAIGN_ID.lower()))
    assert lane == ga.LANE_AMBIGUOUS


def test_output_below_experiments_but_not_in_campaign_namespace_is_ambiguous():
    identity = _identity(output_path=_experiments_non_campaign_path())
    lane, _ = ga.derive_authorization_lane(identity, _declared())
    assert lane == ga.LANE_AMBIGUOUS


def test_output_in_evidence_namespace_is_ambiguous_never_exploratory():
    identity = _identity(output_path=_evidence_output_path())
    lane, _ = ga.derive_authorization_lane(identity, _declared())
    assert lane == ga.LANE_AMBIGUOUS


def test_output_outside_experiments_with_declaration_is_ambiguous_not_ordinary():
    identity = _identity(output_path=_ordinary_output_path())
    lane, _ = ga.derive_authorization_lane(identity, _declared())
    assert lane == ga.LANE_AMBIGUOUS


def test_declared_stage1_brief_signal_on_campaign_output_is_ambiguous():
    identity = _identity(output_path=_campaign_output_path())
    identity = ga.InvocationIdentity.build(
        workflow_id="phase3-test-workflow",
        workflow_stage="stage-1",
        artifact_type=ga.CONTRACT_ARTIFACT_TYPE,
        output_path=_campaign_output_path(),
        framework_root=FRAMEWORK_ROOT,
        target_repository="https://example.invalid/example-owner/example-target.git",
        target_sha="000000000000000000000000000000000000beef",
        requested_model="example-model-identifier",
        executor_id="test-executor",
    )
    lane, _ = ga.derive_authorization_lane(identity, _declared())
    assert lane == ga.LANE_AMBIGUOUS


def test_declared_controlled_mode_false_on_campaign_output_is_ambiguous():
    identity = _identity(output_path=_campaign_output_path(), declared_controlled_mode=False)
    lane, _ = ga.derive_authorization_lane(identity, _declared())
    assert lane == ga.LANE_AMBIGUOUS


def test_evidence_number_metadata_on_campaign_output_is_ambiguous():
    identity = ga.InvocationIdentity.build(
        workflow_id="phase3-test-workflow",
        workflow_stage="stage-3",
        artifact_type="attempt_result",
        evidence_number="0042",
        output_path=_campaign_output_path(),
        framework_root=FRAMEWORK_ROOT,
        target_repository="https://example.invalid/example-owner/example-target.git",
        target_sha="000000000000000000000000000000000000beef",
        requested_model="example-model-identifier",
        executor_id="test-executor",
    )
    lane, _ = ga.derive_authorization_lane(identity, _declared())
    assert lane == ga.LANE_AMBIGUOUS


def test_containment_failure_on_campaign_output_is_ambiguous():
    identity = _identity(output_path=f"C:/elsewhere/experiments/campaigns/{CAMPAIGN_ID}/x.md")
    lane, _ = ga.derive_authorization_lane(identity, _declared())
    assert lane == ga.LANE_AMBIGUOUS


def test_no_identity_is_ambiguous_even_with_declaration():
    lane, _ = ga.derive_authorization_lane(None, _declared())
    assert lane == ga.LANE_AMBIGUOUS


# ---------------------------------------------------------------------------
# CANONICAL: canonical signals always win
# ---------------------------------------------------------------------------


def test_declared_controlled_mode_true_is_canonical_even_with_exploratory_claim():
    identity = _identity(output_path=_campaign_output_path(), declared_controlled_mode=True)
    lane, _ = ga.derive_authorization_lane(identity, _declared())
    assert lane == ga.LANE_CANONICAL


def test_declared_controlled_mode_true_on_evidence_output_is_canonical():
    identity = _identity(output_path=_evidence_output_path(), declared_controlled_mode=True)
    lane, _ = ga.derive_authorization_lane(identity, _declared())
    assert lane == ga.LANE_CANONICAL


def test_evidence_output_without_declaration_is_canonical_when_strong_signals():
    identity = ga.InvocationIdentity.build(
        workflow_id="phase3-test-workflow",
        workflow_stage="stage-1",
        artifact_type=ga.CONTRACT_ARTIFACT_TYPE,
        output_path=_evidence_output_path(),
        framework_root=FRAMEWORK_ROOT,
        target_repository="https://example.invalid/example-owner/example-target.git",
        target_sha="000000000000000000000000000000000000beef",
        requested_model="example-model-identifier",
        executor_id="test-executor",
    )
    lane, _ = ga.derive_authorization_lane(identity, None)
    assert lane == ga.LANE_CANONICAL


# ---------------------------------------------------------------------------
# ORDINARY: no claims, no controlled signals
# ---------------------------------------------------------------------------


def test_plain_ordinary_output_is_ordinary():
    identity = _identity(output_path=_ordinary_output_path())
    lane, _ = ga.derive_authorization_lane(identity, None)
    assert lane == ga.LANE_ORDINARY


def test_ordinary_lane_does_not_require_authorization():
    identity = _identity(output_path=_ordinary_output_path())
    lane, _ = ga.derive_authorization_lane(identity, None)
    assert ga.requires_gate_a(ga.ExecutionMode.ORDINARY_DEVELOPMENT) is False
    assert lane == ga.LANE_ORDINARY
