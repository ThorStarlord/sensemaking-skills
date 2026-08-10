"""Tests for validate-brief.py's handling of Section 15
("Extended analysis") ratified per ADR 0024.

Every field in this block is classified "model, constrained" (ADR 0024,
per ADR 0015's taxonomy) but is entirely optional and non-blocking
(warning severity only, never error). These tests prove: (a) absence
causes zero errors/warnings, (b) presence with valid values causes zero
errors/warnings, (c) presence with invalid enum/type values produces a
WARNING, never an error (the artifact must still validate overall),
(d) a malformed block degrades to a warning, not a crash, (e) the
pre-ratification "(candidate)" heading spelling is still tolerated.
"""

import importlib.util
import os
import sys
import tempfile
import unittest

SCRIPTS_DIR = os.path.join(os.path.dirname(__file__), "..", "scripts")
sys.path.insert(0, SCRIPTS_DIR)

_spec = importlib.util.spec_from_file_location(
    "validate_brief", os.path.join(SCRIPTS_DIR, "validate-brief.py")
)
validate_brief_module = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(validate_brief_module)
validate_brief = validate_brief_module.validate_brief
_is_blocking = validate_brief_module._is_blocking

REPO_ROOT = os.path.dirname(os.path.dirname(__file__))

_BASE_VALID_BODY = """# Repository Sensemaking Brief

## 1. Repository goal
Test repo.

## 6. Weakest boundary
**Weakness type:** Zero Validation

## 7. Evidence
<!-- mode: investigative -->
scripts/validate-brief.py:1 shows this.

Logic trace: this connects evidence to the conclusion.

## 8. Evidence excerpts
```yaml
evidence_excerpts:
  - file: scripts/validate-brief.py
    lines: L1
    quote: "import os"
    supports_claim: "file exists"
```

## 13. Machine-readable handoff

```yaml
artifact_id: repository_sensemaking_brief
schema_version: 1
primary_fog_type: architecture_fog
evidence:
  - "scripts/validate-brief.py:1: exists"
recommended_workflow_id: architecture-implementation-workflow
weakness_type: Zero Validation
created_at: "2026-08-09T00:00:00Z"
immutable: true
```
"""


def _write_tmp(content: str) -> str:
    fd, path = tempfile.mkstemp(suffix=".md")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(content)
    return path


def _validate(content: str) -> list:
    path = _write_tmp(content)
    try:
        return validate_brief(path, REPO_ROOT)
    finally:
        os.remove(path)


class TestExtendedAnalysisAbsent(unittest.TestCase):
    def test_no_section_15_produces_no_extended_analysis_errors(self):
        errors = _validate(_BASE_VALID_BODY)
        codes = [e["message"] for e in errors]
        self.assertFalse(
            any("EXTENDED_ANALYSIS" in c for c in codes),
            f"unexpected EXTENDED_ANALYSIS codes with no Section 15 present: {codes}",
        )


class TestExtendedAnalysisValid(unittest.TestCase):
    def test_valid_section_15_produces_no_warnings(self):
        content = _BASE_VALID_BODY + """
## 15. Extended analysis

```yaml
extended_analysis:
  schema_version: 1
  domain:
    - product
    - architecture
  consequential_boundary:
    description: "desc"
    rationale: "rationale"
    is_demonstrated_weakness: true
  uncertainty:
    source: owner_intent
    question: "which track first?"
  owner_intent_state:
    known: "prior preference noted"
    status: thin
```
"""
        errors = _validate(content)
        codes = [e["message"] for e in errors if "EXTENDED_ANALYSIS" in e["message"]]
        self.assertEqual(codes, [])


class TestExtendedAnalysisInvalidValuesAreWarningsOnly(unittest.TestCase):
    def test_unknown_uncertainty_source_is_a_warning(self):
        content = _BASE_VALID_BODY + """
## 15. Extended analysis

```yaml
extended_analysis:
  uncertainty:
    source: something_made_up
    question: "q"
```
"""
        errors = _validate(content)
        matches = [e for e in errors if "EXTENDED_ANALYSIS_UNCERTAINTY_SOURCE" in e["message"]]
        self.assertEqual(len(matches), 1)
        self.assertFalse(_is_blocking(matches[0]))

    def test_unknown_owner_intent_status_is_a_warning(self):
        content = _BASE_VALID_BODY + """
## 15. Extended analysis

```yaml
extended_analysis:
  owner_intent_state:
    known: "x"
    status: extremely_confident
```
"""
        errors = _validate(content)
        matches = [e for e in errors if "EXTENDED_ANALYSIS_OWNER_INTENT_STATUS" in e["message"]]
        self.assertEqual(len(matches), 1)
        self.assertFalse(_is_blocking(matches[0]))

    def test_non_boolean_is_demonstrated_weakness_is_a_warning(self):
        content = _BASE_VALID_BODY + """
## 15. Extended analysis

```yaml
extended_analysis:
  consequential_boundary:
    is_demonstrated_weakness: "yes"
```
"""
        errors = _validate(content)
        matches = [e for e in errors if "EXTENDED_ANALYSIS_IS_DEMONSTRATED_WEAKNESS_TYPE" in e["message"]]
        self.assertEqual(len(matches), 1)
        self.assertFalse(_is_blocking(matches[0]))

    def test_malformed_yaml_degrades_to_warning_not_crash(self):
        content = _BASE_VALID_BODY + """
## 15. Extended analysis

```yaml
extended_analysis:
  domain: [unclosed
```
"""
        # Must not raise. Base artifact is otherwise valid, so the only
        # blocking-severity errors (if any) must come from elsewhere, not
        # from this malformed optional block.
        errors = _validate(content)
        matches = [e for e in errors if "EXTENDED_ANALYSIS_MALFORMED" in e["message"]]
        self.assertEqual(len(matches), 1)
        self.assertFalse(_is_blocking(matches[0]))

    def test_overall_artifact_still_valid_with_invalid_extended_analysis(self):
        # The whole point of "optional/non-blocking": an otherwise-valid
        # brief must not fail overall validation just because Section 15
        # contains garbage.
        content = _BASE_VALID_BODY + """
## 15. Extended analysis

```yaml
extended_analysis:
  uncertainty:
    source: nonsense
  owner_intent_state:
    status: nonsense
```
"""
        errors = _validate(content)
        blocking = [e for e in errors if _is_blocking(e)]
        self.assertEqual(blocking, [], f"expected no blocking errors, got {blocking}")

    def test_legacy_candidate_heading_spelling_still_tolerated(self):
        # ADR 0024: the validator accepts the pre-ratification "(candidate)"
        # heading so already-written artifacts revalidate unchanged.
        content = _BASE_VALID_BODY + """
## 15. Extended analysis (candidate)

```yaml
extended_analysis:
  schema_version: candidate-1
  domain:
    - architecture
```
"""
        errors = _validate(content)
        codes = [e["message"] for e in errors if "EXTENDED_ANALYSIS" in e["message"]]
        self.assertEqual(codes, [], f"legacy heading produced EXTENDED_ANALYSIS codes: {codes}")


if __name__ == "__main__":
    unittest.main()
