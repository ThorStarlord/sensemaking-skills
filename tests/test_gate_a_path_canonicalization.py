"""Gate A: canonical path identity, the ambiguity floor, and signal isolation.

WHY THIS FILE EXISTS
--------------------
A second independent review of PR #109 reproduced a COMPLETE authorization
bypass, end to end, against the real production call chain:

    build_invocation_identity() -> classify_invocation()
    -> require_authorization_capability() -> provider boundary

These two spellings of the real Evidence 0016 campaign directory:

    experiments/./evidence/0016-stage1-auteur-post-remediation-controlled-attempt
    experiments//evidence//0016-stage1-auteur-post-remediation-controlled-attempt

parsed to (evidence_number=None, evidence_slug=None), classified as
ORDINARY_DEVELOPMENT, and reached a fake provider with ZERO authorization.

Root cause: TWO independently maintained, weakly normalized checks -- the
classifier's `"experiments/evidence/" in output_path` substring test and the
runtime's own `_EVIDENCE_DIR_RE` regex -- both operated on unnormalized raw
text, and therefore failed TOGETHER on the same malformed spellings.

The same review mutation-tested the classifier and found that 2 of 6 mutations
SURVIVED: "ignore evidence-number signal" and "ignore target-repository
signal". Neither signal was load-bearing in the suite.

This file holds the regressions for both findings. It is deliberately
adversarial against its own implementation.
"""

from __future__ import annotations

import itertools
import os
import subprocess
import sys
import unicodedata
from pathlib import Path, PurePosixPath

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))
sys.path.insert(0, str(REPO_ROOT / "tests"))

import gate_a_authorization as ga  # noqa: E402
import skill_executor as se  # noqa: E402


CAMPAIGN_SLUG = ga.CONTRACT_EVIDENCE_SLUG
CAMPAIGN_REL = f"experiments/evidence/{CAMPAIGN_SLUG}"
ORDINARY_MODEL = "claude-haiku-4-5"
ORDINARY_REPO = "https://github.com/ThorStarlord/unrelated-project.git"
ORDINARY_SHA = "a" * 40


# ===========================================================================
# Section 8: the canonical path attack matrix
# ===========================================================================
#
# Every spelling below resolves to the SAME real campaign directory. None of
# them may classify ORDINARY_DEVELOPMENT, and all of them must produce the
# same canonical evidence identity.

EQUIVALENT_CAMPAIGN_SPELLINGS = [
    f"experiments/evidence/{CAMPAIGN_SLUG}",
    f"experiments/./evidence/{CAMPAIGN_SLUG}",              # reviewer bypass #1
    f"experiments//evidence//{CAMPAIGN_SLUG}",              # reviewer bypass #2
    f"experiments/evidence/../evidence/{CAMPAIGN_SLUG}",
    f"./experiments/evidence/{CAMPAIGN_SLUG}",
    f"./experiments/./././evidence/{CAMPAIGN_SLUG}",
    f"experiments\\evidence\\{CAMPAIGN_SLUG}",
    f"experiments\\/evidence//{CAMPAIGN_SLUG}",
    f"experiments\\.\\evidence\\{CAMPAIGN_SLUG}",
    f"experiments/evidence/{CAMPAIGN_SLUG}/",
    f"experiments/evidence/{CAMPAIGN_SLUG}///",
    f"experiments///evidence///{CAMPAIGN_SLUG}///",
    f"experiments/../experiments/evidence/{CAMPAIGN_SLUG}",
    f"experiments/evidence/./{CAMPAIGN_SLUG}/.",
    f"experiments/x/../evidence/{CAMPAIGN_SLUG}",
]

#: Spellings that reach the campaign directory but are NOT required to produce
#: an identical canonical identity key (case-insensitive platforms only). They
#: must still never classify ordinary.
CASE_VARIANT_SPELLINGS = [
    f"EXPERIMENTS/EVIDENCE/{CAMPAIGN_SLUG.upper()}",
    f"Experiments/Evidence/{CAMPAIGN_SLUG}",
    f"experiments/EVIDENCE/{CAMPAIGN_SLUG}",
]


def identity_for(output_path, **kw):
    """An otherwise-ORDINARY invocation, varying only what a test varies.

    Defaults are deliberately non-campaign (ordinary model, unrelated target
    repository, unrelated SHA) so that any controlled classification is
    attributable to the signal under test and not to ambient campaign smell.
    """
    params = dict(
        workflow_id="workflow-planner",
        workflow_stage="",
        artifact_type="",
        evidence_number=None,
        evidence_slug=None,
        output_path=output_path,
        framework_root=str(REPO_ROOT),
        target_root="",
        target_repository=ORDINARY_REPO,
        target_sha=ORDINARY_SHA,
        requested_model=ORDINARY_MODEL,
        executor_id="claude-code",
    )
    params.update(kw)
    return ga.InvocationIdentity.build(**params)


@pytest.mark.parametrize("spelling", EQUIVALENT_CAMPAIGN_SPELLINGS)
def test_equivalent_spellings_share_one_canonical_identity_key(spelling):
    """All equivalent spellings collapse to ONE canonical identity key.

    This is what binds a capability. If two spellings produced two keys, an
    attacker could obtain a capability for one and invoke with the other, or
    split a single logical invocation into two identities. Kills mutation 9
    (revert `_norm_path` to lowercase-plus-rstrip).
    """
    canonical = ga.canonicalize_path(EQUIVALENT_CAMPAIGN_SPELLINGS[0]).identity_key
    assert ga.canonicalize_path(spelling).identity_key == canonical, (
        f"{spelling!r} canonicalized to a different key than the plain form")


@pytest.mark.parametrize("spelling", EQUIVALENT_CAMPAIGN_SPELLINGS)
def test_equivalent_spellings_share_one_invocation_digest(spelling):
    """The capability-binding digest is spelling-independent. Kills mutation 9."""
    base = identity_for(EQUIVALENT_CAMPAIGN_SPELLINGS[0]).digest()
    assert identity_for(spelling).digest() == base, (
        f"{spelling!r} produced a different capability binding digest")


@pytest.mark.parametrize(
    "spelling", EQUIVALENT_CAMPAIGN_SPELLINGS + CASE_VARIANT_SPELLINGS)
def test_no_campaign_spelling_parses_as_unidentified(spelling):
    """Every spelling yields evidence number 0016 and the campaign slug.

    On the old head the two reviewer paths yielded (None, None). That is the
    concrete regression.
    """
    ident = ga.parse_evidence_path(spelling, REPO_ROOT)
    assert ident.parse_status == "VALID_EVIDENCE_PATH", (
        f"{spelling!r} -> {ident.parse_status}")
    assert ident.evidence_number == "0016", f"{spelling!r} -> {ident.evidence_number}"
    assert ident.campaign_slug is True, f"{spelling!r} -> {ident.evidence_slug}"
    assert ident.under_experiments and ident.under_evidence_namespace


@pytest.mark.parametrize(
    "spelling", EQUIVALENT_CAMPAIGN_SPELLINGS + CASE_VARIANT_SPELLINGS)
def test_no_campaign_spelling_classifies_ordinary(spelling):
    """THE invariant. No spelling reaching the campaign directory is ordinary."""
    mode, signals = ga.classify_invocation(identity_for(spelling))
    assert mode is not ga.ExecutionMode.ORDINARY_DEVELOPMENT, (
        f"{spelling!r} classified ORDINARY_DEVELOPMENT (signals={signals})")
    assert ga.requires_gate_a(mode) is True


@pytest.mark.parametrize("spelling", EQUIVALENT_CAMPAIGN_SPELLINGS)
def test_campaign_spellings_with_brief_are_controlled(spelling):
    mode, _ = ga.classify_invocation(
        identity_for(spelling, artifact_type=ga.CONTRACT_ARTIFACT_TYPE))
    assert mode is ga.ExecutionMode.CONTROLLED_STAGE1


def test_absolute_and_repository_relative_forms_agree():
    rel = ga.parse_evidence_path(CAMPAIGN_REL, REPO_ROOT)
    absolute = ga.parse_evidence_path(REPO_ROOT / "experiments" / "evidence"
                                      / CAMPAIGN_SLUG, REPO_ROOT)
    assert rel.key() == absolute.key()


def test_path_object_and_string_agree():
    as_str = ga.parse_evidence_path(CAMPAIGN_REL, REPO_ROOT)
    as_path = ga.parse_evidence_path(PurePosixPath(CAMPAIGN_REL), REPO_ROOT)
    assert as_str.key() == as_path.key()


def test_unicode_decomposed_components_are_nfc_normalized():
    """A decomposed spelling must not evade component matching."""
    decomposed = unicodedata.normalize("NFD", "expe\u0301riments")
    composed = unicodedata.normalize("NFC", "expe\u0301riments")
    assert ga.canonicalize_path(decomposed).parts == (composed,)
    # And a genuinely decomposed campaign path still resolves.
    nfd_path = unicodedata.normalize("NFD", CAMPAIGN_REL)
    assert ga.parse_evidence_path(nfd_path, REPO_ROOT).evidence_number == "0016"


def test_component_containment_is_not_prefix_matching():
    """`experiments-old/` is NOT inside `experiments/`."""
    ident = ga.parse_evidence_path(
        f"experiments-old/evidence/{CAMPAIGN_SLUG}", REPO_ROOT)
    assert ident.under_experiments is False
    assert ident.parse_status == "OUTSIDE_EXPERIMENTS"
    # ...and `evidence-archive` is not the evidence namespace.
    other = ga.parse_evidence_path(
        f"experiments/evidence-archive/{CAMPAIGN_SLUG}", REPO_ROOT)
    assert other.parse_status == "EXPERIMENTS_NON_EVIDENCE_PATH"


def test_dotdot_escape_above_anchor_is_flagged():
    canon = ga.canonicalize_path("../../experiments/evidence/x")
    assert canon.escapes_anchor is True
    assert canon.parts[:2] == ("..", "..")


def test_dotdot_at_absolute_root_is_dropped():
    assert ga.canonicalize_path("/../../experiments").parts == ("experiments",)
    assert ga.canonicalize_path("/../../experiments").escapes_anchor is False


def test_drive_letters_are_captured_and_case_folded():
    a = ga.canonicalize_path("C:/repo/experiments/evidence/x")
    b = ga.canonicalize_path("c:\\repo\\experiments\\evidence\\x")
    assert a.drive.casefold() == b.drive.casefold() == "c"
    assert a.parts == b.parts


def test_canonicalization_does_not_require_the_path_to_exist():
    """Evidence 0016's output directory does not exist and never will here."""
    target = REPO_ROOT / "experiments" / "evidence" / CAMPAIGN_SLUG
    assert not target.exists(), "the real Evidence 0016 directory must not exist"
    ident = ga.parse_evidence_path(target, REPO_ROOT)
    assert ident.parse_status == "VALID_EVIDENCE_PATH"
    assert ident.evidence_number == "0016"


def test_escaping_outside_the_repository_root_is_never_ordinary_when_campaign_like():
    mode, _ = ga.classify_invocation(
        identity_for(f"../../{CAMPAIGN_REL}",
                     artifact_type=ga.CONTRACT_ARTIFACT_TYPE))
    assert mode is not ga.ExecutionMode.ORDINARY_DEVELOPMENT


# ===========================================================================
# Section 9: runtime / classifier agreement
# ===========================================================================


@pytest.mark.parametrize(
    "spelling", EQUIVALENT_CAMPAIGN_SPELLINGS + CASE_VARIANT_SPELLINGS)
def test_runtime_evidence_identity_equals_classifier_evidence_identity(spelling):
    """One parser, two consumers, zero disagreement.

    The runtime used to run its own regex over the raw string. Kills mutation
    10 (restore the independent runtime raw regex): under that mutation the
    runtime yields evidence_number=None for the dotted and doubled spellings
    while the classifier yields "0016".
    """
    runtime_identity = se.build_invocation_identity(
        repo_root=str(REPO_ROOT),
        executor_id="claude-code",
        skill_id="repo-sensemaker",
        expected_output_artifact="repository_sensemaking_brief",
        context={"expected_output_path": spelling},
        model=ORDINARY_MODEL,
    )
    classifier_identity = ga.parse_evidence_path(spelling, str(REPO_ROOT))

    assert runtime_identity.evidence_number == classifier_identity.evidence_number
    assert (ga._norm_slug(runtime_identity.evidence_slug)
            == ga._norm_slug(classifier_identity.evidence_slug))
    assert runtime_identity.evidence_number == "0016", (
        f"the runtime failed to identify {spelling!r} as Evidence 0016")


def test_no_independent_evidence_regex_remains_in_the_runtime():
    """Static guard: the deleted second parser must not come back.

    Two independently maintained normalization implementations is what let the
    bypass slip through. A future edit that reintroduces a local regex here is
    the same bug again.
    """
    source = (REPO_ROOT / "scripts" / "skill_executor.py").read_text(encoding="utf-8")
    assert "_EVIDENCE_DIR_RE" not in source.replace(
        "# There used to be an `_EVIDENCE_DIR_RE` here", ""), (
        "skill_executor.py reintroduced its own evidence-path regex; it must "
        "consume gate_a_authorization.parse_evidence_path instead")
    assert "parse_evidence_path" in source


# ===========================================================================
# Section 7 / 14: the ambiguity floor under experiments/
# ===========================================================================

AMBIGUITY_FLOOR_PATHS = [
    "experiments/evidence",
    "experiments/evidence/",
    "experiments/evidence/not-a-campaign-dir",
    "experiments/evidence/16-stage1-auteur",
    "experiments/evidence/00016-stage1-auteur",
    "experiments/run-control",
    "experiments/run-control/nope",
    "experiments/scratch/output.md",
    "experiments",
    "experiments/./",
]


@pytest.mark.parametrize("path", AMBIGUITY_FLOOR_PATHS)
def test_unparseable_paths_under_experiments_are_never_ordinary(path):
    """A path parsing failure inside `experiments/` is not evidence of
    ordinary development. That is the stated invariant of this remediation."""
    mode, signals = ga.classify_invocation(identity_for(path))
    assert mode is not ga.ExecutionMode.ORDINARY_DEVELOPMENT, (
        f"{path!r} classified ORDINARY (signals={signals})")
    assert ga.requires_gate_a(mode) is True


def test_ordinary_development_is_still_possible():
    """The floor must not swallow the world. Ordinary work stays ungated.

    If this test ever fails, the gate has become a brick and developers will
    route around it -- which is its own security failure.
    """
    for path in ("artifacts/brief.md", "docs/notes.md", "/tmp/scratch/out.md",
                 "experiment-notes/out.md", "src/experiments_helper.py"):
        mode, signals = ga.classify_invocation(identity_for(path))
        assert mode is ga.ExecutionMode.ORDINARY_DEVELOPMENT, (
            f"{path!r} was gated unnecessarily (signals={signals})")
        assert ga.requires_gate_a(mode) is False


def test_ordinary_repo_sensemaker_into_artifacts_stays_ungated():
    """The documented ordinary-development boundary, asserted directly."""
    identity = se.build_invocation_identity(
        repo_root=str(REPO_ROOT),
        executor_id="claude-code",
        skill_id="repo-sensemaker",
        expected_output_artifact="repository_sensemaking_brief",
        context={"expected_output_path": "artifacts/brief.md"},
        model=ORDINARY_MODEL,
    )
    mode, _ = ga.classify_invocation(identity)
    assert mode is ga.ExecutionMode.ORDINARY_DEVELOPMENT


# ===========================================================================
# Section 10: evidence metadata as defense in depth
# ===========================================================================

METADATA_CASES = [
    # (number, slug, artifact_type, expected_mode)
    (None, None, "", ga.ExecutionMode.ORDINARY_DEVELOPMENT),
    ("0016", None, ga.CONTRACT_ARTIFACT_TYPE, ga.ExecutionMode.CONTROLLED_STAGE1),
    (None, CAMPAIGN_SLUG, ga.CONTRACT_ARTIFACT_TYPE, ga.ExecutionMode.CONTROLLED_STAGE1),
    ("0016", CAMPAIGN_SLUG, ga.CONTRACT_ARTIFACT_TYPE, ga.ExecutionMode.CONTROLLED_STAGE1),
    ("0016", None, "", ga.ExecutionMode.AMBIGUOUS),
    (None, CAMPAIGN_SLUG, "", ga.ExecutionMode.AMBIGUOUS),
    # conflicting number and slug
    ("0017", CAMPAIGN_SLUG, ga.CONTRACT_ARTIFACT_TYPE, ga.ExecutionMode.AMBIGUOUS),
    ("0016", "0017-something-else", ga.CONTRACT_ARTIFACT_TYPE, ga.ExecutionMode.AMBIGUOUS),
    # malformed campaign-like numbers: never ordinary, never confidently controlled
    ("16", None, ga.CONTRACT_ARTIFACT_TYPE, ga.ExecutionMode.AMBIGUOUS),
    ("00016", None, ga.CONTRACT_ARTIFACT_TYPE, ga.ExecutionMode.AMBIGUOUS),
    (" 0016 ", None, ga.CONTRACT_ARTIFACT_TYPE, ga.ExecutionMode.CONTROLLED_STAGE1),
    ("sixteen", None, ga.CONTRACT_ARTIFACT_TYPE, ga.ExecutionMode.AMBIGUOUS),
    # case-varied slug still names the campaign
    (None, CAMPAIGN_SLUG.upper(), ga.CONTRACT_ARTIFACT_TYPE,
     ga.ExecutionMode.CONTROLLED_STAGE1),
]


@pytest.mark.parametrize("number,slug,artifact,expected", METADATA_CASES)
def test_evidence_metadata_matrix(number, slug, artifact, expected):
    mode, signals = ga.classify_invocation(
        identity_for("artifacts/brief.md", evidence_number=number,
                     evidence_slug=slug, artifact_type=artifact))
    assert mode is expected, (
        f"number={number!r} slug={slug!r} artifact={artifact!r} -> {mode} "
        f"(signals={signals})")


def test_malformed_campaign_number_is_not_equivalent_to_absence():
    """Absence can be ordinary. Malformation never can."""
    absent, _ = ga.classify_invocation(
        identity_for("artifacts/brief.md", artifact_type=ga.CONTRACT_ARTIFACT_TYPE))
    malformed, _ = ga.classify_invocation(
        identity_for("artifacts/brief.md", evidence_number="16",
                     artifact_type=ga.CONTRACT_ARTIFACT_TYPE))
    assert absent is ga.ExecutionMode.ORDINARY_DEVELOPMENT
    assert malformed is ga.ExecutionMode.AMBIGUOUS


def test_path_identifies_0016_but_metadata_identifies_0017_is_ambiguous():
    """Path/metadata disagreement is a contradiction, never a resolution."""
    mode, signals = ga.classify_invocation(
        identity_for(CAMPAIGN_REL, evidence_number="0017",
                     evidence_slug="0017-something-else",
                     artifact_type=ga.CONTRACT_ARTIFACT_TYPE))
    assert mode is ga.ExecutionMode.AMBIGUOUS
    assert "evidence_number_conflicts_with_path" in signals


# ===========================================================================
# Section 11: the evidence-NUMBER signal is load-bearing
# ===========================================================================


def test_evidence_number_is_the_decisive_controlled_signal():
    """Isolation test. Path is ordinary, model/target are ordinary, no slug.

    The ONLY campaign anchor is the evidence number. Kills mutation 3 (ignore
    evidence number): without that branch this falls to AMBIGUOUS, because an
    unrecognized evidence identity is deliberately NOT a controlled anchor.
    """
    identity = identity_for("artifacts/brief.md", evidence_number="0016",
                            artifact_type=ga.CONTRACT_ARTIFACT_TYPE)
    mode, signals = ga.classify_invocation(identity)
    assert mode is ga.ExecutionMode.CONTROLLED_STAGE1, (
        f"evidence number 0016 was not decisive (signals={signals})")
    assert "evidence_number_is_campaign" in signals
    # And the near-miss must NOT reach the same conclusion, so the assertion
    # above cannot be satisfied by a constant.
    near_miss, _ = ga.classify_invocation(
        identity_for("artifacts/brief.md", evidence_number="0099",
                     artifact_type=ga.CONTRACT_ARTIFACT_TYPE))
    assert near_miss is ga.ExecutionMode.AMBIGUOUS


def test_evidence_slug_is_the_decisive_controlled_signal():
    """Kills mutation 4 (ignore evidence slug)."""
    mode, signals = ga.classify_invocation(
        identity_for("artifacts/brief.md", evidence_slug=CAMPAIGN_SLUG,
                     artifact_type=ga.CONTRACT_ARTIFACT_TYPE))
    assert mode is ga.ExecutionMode.CONTROLLED_STAGE1, (
        f"campaign slug was not decisive (signals={signals})")
    assert "evidence_slug_is_campaign" in signals
    near_miss, _ = ga.classify_invocation(
        identity_for("artifacts/brief.md", evidence_slug="0099-unrelated",
                     artifact_type=ga.CONTRACT_ARTIFACT_TYPE))
    assert near_miss is ga.ExecutionMode.AMBIGUOUS


def test_output_namespace_is_the_decisive_controlled_signal():
    """Kills mutation 2 (ignore output namespace).

    A non-campaign evidence directory, with no campaign metadata at all: the
    namespace alone must carry the decision.
    """
    mode, signals = ga.classify_invocation(
        identity_for("experiments/evidence/0099-some-other-evidence",
                     artifact_type=ga.CONTRACT_ARTIFACT_TYPE))
    assert mode is ga.ExecutionMode.CONTROLLED_STAGE1, (
        f"controlled namespace was not decisive (signals={signals})")
    assert "output_in_controlled_evidence_namespace" in signals


# ===========================================================================
# Section 12: the TARGET-REPOSITORY signal is load-bearing
# ===========================================================================


def test_target_repository_is_the_decisive_controlled_signal():
    """Isolation test. Ordinary output path, ordinary model, no evidence id.

    The ONLY campaign anchor is the pinned Auteur target. Kills mutation 5
    (ignore target repository): without it this falls to ORDINARY.
    """
    mode, signals = ga.classify_invocation(
        identity_for("artifacts/brief.md",
                     target_repository=ga.CONTRACT_TARGET_REPOSITORY,
                     artifact_type=ga.CONTRACT_ARTIFACT_TYPE,
                     workflow_stage="stage-1"))
    assert mode is ga.ExecutionMode.CONTROLLED_STAGE1, (
        f"pinned target repository was not decisive (signals={signals})")
    assert "target_repository_is_campaign_pin" in signals
    # An unrelated target with everything else identical must NOT be controlled.
    unrelated, _ = ga.classify_invocation(
        identity_for("artifacts/brief.md",
                     artifact_type=ga.CONTRACT_ARTIFACT_TYPE,
                     workflow_stage="stage-1"))
    assert unrelated is ga.ExecutionMode.ORDINARY_DEVELOPMENT


@pytest.mark.parametrize("alias", [
    "https://github.com/ThorStarlord/auteur.git",
    "https://github.com/ThorStarlord/auteur",
    "https://github.com/ThorStarlord/auteur/",
    "HTTPS://GitHub.com/ThorStarlord/Auteur.git",
    "git@github.com:ThorStarlord/auteur.git",
    "ssh://git@github.com/ThorStarlord/auteur.git",
    "  https://github.com/ThorStarlord/auteur.git  ",
])
def test_canonical_repository_aliases_are_equivalent(alias):
    """Spelling the same repository differently must not evade the pin."""
    assert ga._norm_repo_url(alias) == ga._NORM_CONTRACT_TARGET_REPOSITORY, alias
    mode, signals = ga.classify_invocation(
        identity_for("artifacts/brief.md", target_repository=alias,
                     artifact_type=ga.CONTRACT_ARTIFACT_TYPE,
                     workflow_stage="stage-1"))
    assert mode is ga.ExecutionMode.CONTROLLED_STAGE1, alias
    assert "target_repository_is_campaign_pin" in signals


def test_a_conflicting_target_forces_ambiguous():
    """Campaign evidence output aimed at an unrelated repository is incoherent."""
    mode, _ = ga.classify_invocation(
        identity_for(CAMPAIGN_REL, target_repository=ORDINARY_REPO,
                     evidence_number="0017",
                     artifact_type=ga.CONTRACT_ARTIFACT_TYPE))
    assert mode is ga.ExecutionMode.AMBIGUOUS


def test_target_sha_is_the_decisive_controlled_signal():
    """Kills mutation 6 (ignore target SHA)."""
    mode, signals = ga.classify_invocation(
        identity_for("artifacts/brief.md", target_sha=ga.CONTRACT_TARGET_SHA,
                     artifact_type=ga.CONTRACT_ARTIFACT_TYPE,
                     workflow_stage="stage-1"))
    assert mode is ga.ExecutionMode.CONTROLLED_STAGE1, (
        f"pinned target SHA was not decisive (signals={signals})")
    assert "target_sha_is_campaign_pin" in signals


def test_target_sha_case_and_whitespace_variants_are_equivalent():
    for variant in (ga.CONTRACT_TARGET_SHA.upper(),
                    f"  {ga.CONTRACT_TARGET_SHA}  "):
        mode, signals = ga.classify_invocation(
            identity_for("artifacts/brief.md", target_sha=variant,
                         artifact_type=ga.CONTRACT_ARTIFACT_TYPE,
                         workflow_stage="stage-1"))
        assert "target_sha_is_campaign_pin" in signals, variant
        assert mode is ga.ExecutionMode.CONTROLLED_STAGE1


def test_contradiction_branch_is_load_bearing():
    """Kills mutation 7 (ambiguous becomes ordinary) at the contradiction branch."""
    mode, signals = ga.classify_invocation(
        identity_for("artifacts/brief.md", evidence_number="16"))
    assert mode is ga.ExecutionMode.AMBIGUOUS
    assert "evidence_number_malformed" in signals
    assert ga.requires_gate_a(mode) is True


# ===========================================================================
# Section 14: the classifier truth table
# ===========================================================================
#
# name -> (kwargs, expected mode, gate required)

TRUTH_TABLE = {
    "all_controlled_signals": (
        dict(output_path=CAMPAIGN_REL, evidence_number="0016",
             evidence_slug=CAMPAIGN_SLUG, artifact_type=ga.CONTRACT_ARTIFACT_TYPE,
             workflow_stage="stage-1",
             target_repository=ga.CONTRACT_TARGET_REPOSITORY,
             target_sha=ga.CONTRACT_TARGET_SHA,
             requested_model=ga.CONTRACT_EXACT_MODEL),
        ga.ExecutionMode.CONTROLLED_STAGE1),
    "one_signal_missing_no_model": (
        dict(output_path=CAMPAIGN_REL, evidence_number="0016",
             evidence_slug=CAMPAIGN_SLUG, artifact_type=ga.CONTRACT_ARTIFACT_TYPE,
             workflow_stage="stage-1",
             target_repository=ga.CONTRACT_TARGET_REPOSITORY),
        ga.ExecutionMode.CONTROLLED_STAGE1),
    "one_signal_missing_no_artifact_type": (
        dict(output_path=CAMPAIGN_REL, evidence_number="0016",
             evidence_slug=CAMPAIGN_SLUG, workflow_stage="stage-1"),
        ga.ExecutionMode.AMBIGUOUS),
    "one_signal_malformed_number": (
        dict(output_path=CAMPAIGN_REL, evidence_number="00016",
             artifact_type=ga.CONTRACT_ARTIFACT_TYPE),
        ga.ExecutionMode.AMBIGUOUS),
    "one_signal_malformed_path": (
        dict(output_path="experiments/evidence/not-a-dir",
             artifact_type=ga.CONTRACT_ARTIFACT_TYPE),
        ga.ExecutionMode.AMBIGUOUS),
    "one_signal_conflicting_number": (
        dict(output_path=CAMPAIGN_REL, evidence_number="0017",
             artifact_type=ga.CONTRACT_ARTIFACT_TYPE),
        ga.ExecutionMode.AMBIGUOUS),
    "two_signals_conflicting": (
        dict(output_path=CAMPAIGN_REL, evidence_number="0017",
             evidence_slug="0018-other", artifact_type=ga.CONTRACT_ARTIFACT_TYPE),
        ga.ExecutionMode.AMBIGUOUS),
    "no_campaign_signals": (
        dict(output_path="artifacts/brief.md"),
        ga.ExecutionMode.ORDINARY_DEVELOPMENT),
    "no_campaign_signals_with_brief": (
        dict(output_path="artifacts/brief.md",
             artifact_type=ga.CONTRACT_ARTIFACT_TYPE, workflow_stage="stage-1"),
        ga.ExecutionMode.ORDINARY_DEVELOPMENT),
    "only_weak_signal_model": (
        dict(output_path="artifacts/brief.md",
             requested_model=ga.CONTRACT_EXACT_MODEL),
        ga.ExecutionMode.ORDINARY_DEVELOPMENT),
    "only_weak_signal_model_plus_stage1": (
        dict(output_path="artifacts/brief.md", workflow_stage="stage-1",
             requested_model=ga.CONTRACT_EXACT_MODEL),
        ga.ExecutionMode.AMBIGUOUS),
    "path_parse_failure_under_experiments": (
        dict(output_path="experiments/whatever/out.md",
             artifact_type=ga.CONTRACT_ARTIFACT_TYPE),
        ga.ExecutionMode.AMBIGUOUS),
    "reviewer_bypass_dot_component": (
        dict(output_path=f"experiments/./evidence/{CAMPAIGN_SLUG}",
             artifact_type=ga.CONTRACT_ARTIFACT_TYPE),
        ga.ExecutionMode.CONTROLLED_STAGE1),
    "reviewer_bypass_double_separator": (
        dict(output_path=f"experiments//evidence//{CAMPAIGN_SLUG}",
             artifact_type=ga.CONTRACT_ARTIFACT_TYPE),
        ga.ExecutionMode.CONTROLLED_STAGE1),
    "declared_false_over_campaign_path": (
        dict(output_path=CAMPAIGN_REL, declared_controlled_mode=False),
        ga.ExecutionMode.AMBIGUOUS),
    "declared_true_over_ordinary_path": (
        dict(output_path="artifacts/brief.md", declared_controlled_mode=True),
        ga.ExecutionMode.CONTROLLED_STAGE1),
    "run_control_namespace": (
        dict(output_path=f"experiments/run-control/{CAMPAIGN_SLUG}",
             artifact_type=ga.CONTRACT_ARTIFACT_TYPE),
        ga.ExecutionMode.CONTROLLED_STAGE1),
}


@pytest.mark.parametrize("case", sorted(TRUTH_TABLE))
def test_classifier_truth_table(case):
    kwargs, expected = TRUTH_TABLE[case]
    mode, signals = ga.classify_invocation(identity_for(**kwargs))
    assert mode is expected, f"{case}: expected {expected}, got {mode} ({signals})"
    assert ga.requires_gate_a(mode) is (
        expected is not ga.ExecutionMode.ORDINARY_DEVELOPMENT)


def test_identity_missing_is_ambiguous_not_ordinary():
    mode, signals = ga.classify_invocation(None)
    assert mode is ga.ExecutionMode.AMBIGUOUS
    assert signals == ("identity_missing",)


# ===========================================================================
# Section 15: deterministic path fuzzing
# ===========================================================================


def _spelling_variants(seed_path: str):
    """Bounded, DETERMINISTIC spelling variants of one logical path.

    Deterministic by construction (itertools.product over a fixed option
    table), so a failure is always reproducible without recording a seed.
    """
    sep_options = ["/", "//", "/./", "\\", "///"]
    prefix_options = ["", "./", ".//", "./././"]
    suffix_options = ["", "/", "//", "/."]
    components = seed_path.split("/")
    for sep, prefix, suffix in itertools.product(
            sep_options, prefix_options, suffix_options):
        yield prefix + sep.join(components) + suffix


FUZZ_VARIANTS = sorted(set(_spelling_variants(CAMPAIGN_REL)))


def test_fuzz_generates_a_meaningful_number_of_variants():
    assert len(FUZZ_VARIANTS) >= 60, len(FUZZ_VARIANTS)


def test_no_fuzzed_campaign_spelling_classifies_ordinary():
    """The systematic version of the attack matrix.

    The reviewer's requirement was explicit: any further spelling that reaches
    the campaign directory must not classify ordinary.
    """
    offenders = []
    for variant in FUZZ_VARIANTS:
        mode, _ = ga.classify_invocation(identity_for(variant))
        if mode is ga.ExecutionMode.ORDINARY_DEVELOPMENT:
            offenders.append(variant)
    assert offenders == [], f"{len(offenders)} spellings classified ordinary: {offenders[:10]}"


def test_all_fuzzed_campaign_spellings_identify_evidence_0016():
    misparsed = [v for v in FUZZ_VARIANTS
                 if ga.parse_evidence_path(v, REPO_ROOT).evidence_number != "0016"]
    assert misparsed == [], f"{len(misparsed)} spellings misparsed: {misparsed[:10]}"


def test_all_fuzzed_campaign_spellings_share_one_digest():
    digests = {identity_for(v).digest() for v in FUZZ_VARIANTS}
    assert len(digests) == 1, f"{len(digests)} distinct capability bindings"


def test_fuzzed_identity_field_variants_are_never_ordinary():
    """Fuzz the non-path identity fields: casing, whitespace, punctuation."""
    slug_variants = [CAMPAIGN_SLUG, CAMPAIGN_SLUG.upper(), CAMPAIGN_SLUG.title(),
                     f"  {CAMPAIGN_SLUG}  "]
    number_variants = ["0016", " 0016", "0016 ", "16", "00016", "0016\t"]
    repo_variants = ["https://github.com/ThorStarlord/auteur.git",
                     "git@github.com:ThorStarlord/auteur",
                     "HTTPS://github.com/thorstarlord/AUTEUR/"]
    sha_variants = [ga.CONTRACT_TARGET_SHA, ga.CONTRACT_TARGET_SHA.upper()]

    offenders = []
    for slug in slug_variants:
        for number in number_variants:
            mode, _ = ga.classify_invocation(
                identity_for("artifacts/brief.md", evidence_slug=slug,
                             evidence_number=number))
            if mode is ga.ExecutionMode.ORDINARY_DEVELOPMENT:
                offenders.append((slug, number))
    for repo in repo_variants:
        for sha in sha_variants:
            mode, _ = ga.classify_invocation(
                identity_for("artifacts/brief.md", target_repository=repo,
                             target_sha=sha, workflow_stage="stage-1"))
            if mode is ga.ExecutionMode.ORDINARY_DEVELOPMENT:
                offenders.append((repo, sha))
    assert offenders == [], offenders


# ===========================================================================
# Section 20: symlinks, junctions, non-existent paths
# ===========================================================================


def _try_symlink(link: Path, target: Path) -> bool:
    try:
        link.symlink_to(target, target_is_directory=True)
        return True
    except (OSError, NotImplementedError):
        return False


def test_symlinked_experiments_directory_still_classifies_controlled(tmp_path):
    """A symlinked ancestor must not hide the campaign namespace.

    Uses a temporary tree ONLY. The real Evidence 0016 directory is never
    created by this suite.
    """
    root = tmp_path / "framework"
    real = tmp_path / "elsewhere" / "experiments" / "evidence" / CAMPAIGN_SLUG
    real.mkdir(parents=True)
    root.mkdir()
    if not _try_symlink(root / "experiments", tmp_path / "elsewhere" / "experiments"):
        pytest.skip("symlink creation not permitted on this platform/account")

    via_link = root / "experiments" / "evidence" / CAMPAIGN_SLUG
    ident = ga.parse_evidence_path(via_link, root)
    assert ident.parse_status == "VALID_EVIDENCE_PATH"
    assert ident.evidence_number == "0016"
    mode, _ = ga.classify_invocation(
        identity_for(str(via_link), framework_root=str(root)))
    assert mode is not ga.ExecutionMode.ORDINARY_DEVELOPMENT


def test_symlink_pointing_into_the_campaign_namespace_is_not_ordinary(tmp_path):
    """An innocuous-looking path whose ancestor resolves into experiments/."""
    root = tmp_path / "framework"
    campaign = root / "experiments" / "evidence" / CAMPAIGN_SLUG
    campaign.mkdir(parents=True)
    (root / "artifacts").mkdir()
    if not _try_symlink(root / "artifacts" / "innocuous", campaign):
        pytest.skip("symlink creation not permitted on this platform/account")

    disguised = root / "artifacts" / "innocuous" / "brief.md"
    mode, signals = ga.classify_invocation(
        identity_for(str(disguised), framework_root=str(root)))
    assert mode is not ga.ExecutionMode.ORDINARY_DEVELOPMENT, (
        f"a symlink disguised the campaign namespace (signals={signals})")


def test_nonexistent_output_directory_is_classifiable(tmp_path):
    """Classification must never require the output directory to exist."""
    root = tmp_path / "framework"
    root.mkdir()
    target = root / "experiments" / "evidence" / CAMPAIGN_SLUG / "brief.md"
    assert not target.exists()
    ident = ga.parse_evidence_path(target, root)
    assert ident.evidence_number == "0016"
    mode, _ = ga.classify_invocation(
        identity_for(str(target), framework_root=str(root)))
    assert mode is not ga.ExecutionMode.ORDINARY_DEVELOPMENT


def test_resolution_failure_fails_closed(monkeypatch, tmp_path):
    """If the filesystem cannot answer, we do not guess permissively."""
    root = tmp_path / "framework"
    (root / "experiments").mkdir(parents=True)

    real_resolve = Path.resolve

    def boom(self, strict=False):
        raise OSError("simulated permission failure")

    monkeypatch.setattr(Path, "resolve", boom)
    resolved, code = ga.resolve_containment(root / "experiments" / "x", root)
    assert resolved is None
    assert code == ga.GATE_A_OUTPUT_PATH_AMBIGUOUS
    monkeypatch.setattr(Path, "resolve", real_resolve)


def test_this_suite_never_creates_the_real_evidence_directory():
    real = REPO_ROOT / "experiments" / "evidence" / CAMPAIGN_SLUG
    assert not real.exists(), (
        "a test created the real Evidence 0016 output directory")
    result = subprocess.run(
        ["git", "-C", str(REPO_ROOT), "status", "--porcelain", "--",
         "experiments/"], capture_output=True, text=True, check=False)
    assert result.stdout.strip() == "", (
        f"the canonicalization suite dirtied experiments/:\n{result.stdout}")


# ===========================================================================
# Section 18: end-to-end bypass regressions against a fake provider
# ===========================================================================


class SpyProvider:
    def __init__(self):
        self.model_invocation_count = 0
        self.models_requested: list = []

    def query(self, prompt=None, options=None):
        self.model_invocation_count += 1
        self.models_requested.append(getattr(options, "model", None))

        async def _agen():
            if False:  # pragma: no cover
                yield None
        return _agen()


@pytest.fixture
def spy(monkeypatch):
    s = SpyProvider()
    import claude_agent_sdk
    assert hasattr(claude_agent_sdk, "query")
    monkeypatch.setattr(claude_agent_sdk, "query", s.query)
    return s


E2E_BYPASS_PATHS = [
    f"experiments/./evidence/{CAMPAIGN_SLUG}",
    f"experiments//evidence//{CAMPAIGN_SLUG}",
    f"experiments/evidence/../evidence/{CAMPAIGN_SLUG}",
    f"experiments\\/evidence//{CAMPAIGN_SLUG}",
    f"experiments\\evidence\\{CAMPAIGN_SLUG}",
    f"./experiments/./evidence/{CAMPAIGN_SLUG}",
]


@pytest.mark.parametrize("bypass_path", E2E_BYPASS_PATHS)
def test_end_to_end_bypass_path_reaches_no_provider(bypass_path, spy, tmp_path):
    """The exact reproduced bypass, through the REAL production chain.

    On the old head, the first two of these each produced
    `provider_invocation_count == 1` with `authorization_required == False`.
    """
    identity = se.build_invocation_identity(
        repo_root=str(REPO_ROOT),
        executor_id="claude-code",
        skill_id="repo-sensemaker",
        expected_output_artifact="repository_sensemaking_brief",
        context={"expected_output_path": str(tmp_path / bypass_path)},
        model=ORDINARY_MODEL,
    )
    # 1. Canonical controlled classification.
    mode, signals = ga.classify_invocation(identity)
    assert mode is not ga.ExecutionMode.ORDINARY_DEVELOPMENT, signals
    # 2. Authorization required.
    assert ga.requires_gate_a(mode) is True
    # 3. The identity carries the campaign evidence id, not None.
    assert identity.evidence_number == "0016"

    # 4. No capability -> the real executor refuses before any SDK object.
    with pytest.raises(se.GateAAuthorizationRequired):
        se.ClaudeAgentSdkSkillExecutor(
            repo_root=str(REPO_ROOT),
            model=ORDINARY_MODEL,
            controlled_experiment=False,
            authorization=None,
            invocation_identity=identity,
        )
    assert spy.model_invocation_count == 0, "a model call escaped Gate A"
    assert not (tmp_path / "experiments").exists(), "an output path was created"


# ===========================================================================
# Section 16: re-derivation at the provider boundary
# ===========================================================================


def test_provider_boundary_rederives_the_canonical_identity(spy, tmp_path):
    """Construction-time identity is never trusted at the provider boundary.

    The executor is constructed with an ORDINARY identity and NO capability,
    which is legitimately allowed. The actual call then aims at the campaign
    directory using one of the reproduced bypass spellings. The boundary must
    re-derive, re-canonicalize, re-classify, and refuse.

    Kills mutation 8 (skip provider-boundary re-derivation): under that
    mutation the boundary reuses the ordinary construction-time identity and
    the call reaches the provider.
    """
    ordinary = identity_for("artifacts/brief.md")
    executor = se.ClaudeAgentSdkSkillExecutor(
        repo_root=str(REPO_ROOT),
        model=ORDINARY_MODEL,
        controlled_experiment=False,
        authorization=None,
        invocation_identity=ordinary,
    )
    # Construction succeeded: this really is an ungated ordinary executor.
    assert ga.classify_invocation(ordinary) is not None

    session = tmp_path / "session"
    session.mkdir()
    smuggled = str(tmp_path / f"experiments/./evidence/{CAMPAIGN_SLUG}" / "brief.md")
    try:
        executor.invoke_skill(
            skill_id="repo-sensemaker",
            invocation_command="/skill repo-sensemaker",
            input_artifacts=[],
            expected_output_artifact="repository_sensemaking_brief",
            context={"expected_output_path": smuggled,
                     "artifact_session_dir": str(session)},
        )
    except se.GateAAuthorizationRequired:
        pass  # refusing loudly is the correct outcome
    assert spy.model_invocation_count == 0, (
        "the provider boundary trusted the construction-time identity and let "
        "a campaign invocation through")
