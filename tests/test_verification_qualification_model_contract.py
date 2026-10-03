from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODEL = ROOT / "docs" / "verification-and-qualification-model.md"
MAINTAINER = ROOT / "docs" / "maintainer-guide-v1.0.md"
QUALIFICATION = ROOT / "docs" / "product-management" / "qualification-levels.md"
OPERATIONS = ROOT / "docs" / "operations-runbook.md"
FAQ = ROOT / "docs" / "FAQ.md"
CONTEXT = ROOT / "CONTEXT.md"


def test_verification_and_qualification_model_declares_orthogonal_axes():
    text = MODEL.read_text(encoding="utf-8")

    for required in (
        "test class",
        "mechanical validation stage",
        "semantic/control level",
        "qualification state",
        "validator passed != semantic truth",
        "test passed != qualification",
    ):
        assert required in text


def test_mechanical_validation_stops_before_semantic_truth():
    text = MODEL.read_text(encoding="utf-8")

    for stage in (
        "V0 — Syntax",
        "V1 — Shape",
        "V2 — Contract / conformance",
        "V3 — Identity / provenance / currentness",
        "V4 — Evidence integrity",
        "V5 — Admission / transition integrity",
    ):
        assert stage in text

    assert "V0-V5 PASS" in text
    assert "!= semantic correctness" in text
    assert "S1 — Evidence supports claim" in text
    assert "S2 — Claim warrants decision" in text
    assert "S3 — Observed outcome supports effectiveness claim" in text


def test_level_word_is_reserved_for_current_control_model():
    text = MODEL.read_text(encoding="utf-8")
    maintainer = MAINTAINER.read_text(encoding="utf-8")

    assert "The word **Level** is reserved for the current Four-Level Control Model." in text
    assert "Older retained documents use the phrase" in text
    assert "Level-3 validators" in text
    assert "do not introduce new" in maintainer
    assert "Level-N validator" in maintainer


def test_claim_ceiling_covers_all_canonical_test_classes():
    text = MODEL.read_text(encoding="utf-8")

    for test_class in (
        "UNIT",
        "CONTRACT",
        "INTEGRATION",
        "ACCEPTANCE",
        "ROBUSTNESS",
        "PERFORMANCE",
        "RELEASE_INTEGRITY",
        "QUALIFICATION_VERIFIER",
        "EXTERNAL_EVIDENCE",
    ):
        assert f"**{test_class}**" in text


def test_qualification_doc_links_back_to_cross_axis_model():
    text = QUALIFICATION.read_text(encoding="utf-8")

    assert "../verification-and-qualification-model.md" in text
    assert "not a synonym for test result, validation depth, or Four-Level Control scope" in text
    assert "does not by itself advance empirical maturity" in text

def test_model_is_discoverable_from_current_operator_and_context_surfaces():
    operations = OPERATIONS.read_text(encoding="utf-8")
    context = CONTEXT.read_text(encoding="utf-8")

    assert "verification-and-qualification-model.md" in operations
    assert "verification-and-qualification-model.md" in context


def test_consequential_results_have_a_reporting_discipline():
    model = MODEL.read_text(encoding="utf-8")
    operations = OPERATIONS.read_text(encoding="utf-8")

    for field in (
        "test class:",
        "validation stage:",
        "semantic status:",
        "qualification effect:",
        "evidence identity:",
        "claim ceiling:",
    ):
        assert field in model
        assert field in operations


def test_faq_explains_the_four_assurance_axes():
    text = FAQ.read_text(encoding="utf-8")

    assert "test class" in text
    assert "validation stage" in text
    assert "control level" in text
    assert "qualification state" in text
    assert "They are deliberately not one ladder." in text

