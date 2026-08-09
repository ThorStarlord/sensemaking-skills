"""
Regression tests for validate-brief.py's fog-vocabulary handling
(Construction Slice 2).

Before this fix, `allowed_fog_types` in validate-brief.py was a hard-coded
list of 4 values (product_fog, ui_fog, docs_fog, architecture_fog), while
docs/canonical-vocabulary.yaml and artifact-contracts.yaml's routing_fields
both declare 5 canonical fog types, including integration_fog. A brief that
correctly used the 5th canonical value was rejected with
primary_fog_type.unknown_value -- an enforced contradiction, not just a
documentation gap.

recommended_workflow_id and weakness_type already load their allowed values
from their registries (see load_workflow_registry / load_weakness_types in
_validator_utils.py); this brings primary_fog_type in line with that
existing, already-correct pattern via load_canonical_vocabulary().
"""

import importlib.util
import os
import sys

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SCRIPTS_DIR = os.path.join(REPO_ROOT, "scripts")
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

if "validate_brief" in sys.modules:
    vb = sys.modules["validate_brief"]
else:
    _spec = importlib.util.spec_from_file_location(
        "validate_brief", os.path.join(SCRIPTS_DIR, "validate-brief.py")
    )
    vb = importlib.util.module_from_spec(_spec)
    sys.modules["validate_brief"] = vb
    _spec.loader.exec_module(vb)

FIXTURES = os.path.join(REPO_ROOT, "tests", "fixtures", "validate-brief")


def _fog_type_errors(artifact_path):
    errors = vb.validate_brief(artifact_path, repo_root=REPO_ROOT)
    return [e for e in errors if e.get("field") == "primary_fog_type"]


def test_integration_fog_is_accepted():
    """integration_fog is canonical (docs/canonical-vocabulary.yaml,
    artifact-contracts.yaml routing_fields) and must not be rejected."""
    path = os.path.join(FIXTURES, "valid", "integration-fog-brief.md")
    errors = _fog_type_errors(path)
    assert errors == [], errors


def test_all_five_canonical_fog_types_are_accepted(tmp_path):
    """Every canonical fog type must round-trip through the validator, not
    just the 4 that were previously hard-coded."""
    template = open(
        os.path.join(FIXTURES, "valid", "integration-fog-brief.md"), encoding="utf-8"
    ).read()
    from _validator_utils import load_canonical_vocabulary
    vocab = load_canonical_vocabulary(REPO_ROOT)
    canonical_ids = [ft["id"] for ft in vocab["fog_types"]]
    assert len(canonical_ids) >= 5, canonical_ids  # sanity: registry itself has 5+

    for fog_id in canonical_ids:
        content = template.replace("primary_fog_type: integration_fog", f"primary_fog_type: {fog_id}")
        fixture_path = tmp_path / f"brief-{fog_id}.md"
        fixture_path.write_text(content, encoding="utf-8")
        errors = _fog_type_errors(str(fixture_path))
        assert errors == [], f"{fog_id}: {errors}"


def test_noncanonical_fog_type_is_still_rejected(tmp_path):
    """A fog type that is NOT in the canonical registry must still be
    rejected -- the fix must not turn validation into a no-op."""
    template = open(
        os.path.join(FIXTURES, "valid", "integration-fog-brief.md"), encoding="utf-8"
    ).read()
    content = template.replace("primary_fog_type: integration_fog", "primary_fog_type: not_a_real_fog_type")
    fixture_path = tmp_path / "brief-bad-fog.md"
    fixture_path.write_text(content, encoding="utf-8")

    errors = _fog_type_errors(str(fixture_path))
    assert any(e.get("error_type") == "unknown_value" for e in errors), errors
