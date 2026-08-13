"""Tests for validate-brief.py's collision-direction evidence rule (issue #171).

evidence-rules Rule 7 (Collision Dedup Direction): when a brief RECOMMENDS
renumbering/deduplicating a colliding ID (ADR number, artifact id, workflow
id), it must carry the direction decision (reference counts per candidate,
prior dedup intent, grep incl. handoffs) in Section 13's machine field
`collision_dedup_direction`. A brief that merely QUOTES target text
containing "renumber" is not a recommendation and is not flagged.
"""

import importlib.util
import os
import sys
import tempfile
import unittest

SCRIPTS_DIR = os.path.join(os.path.dirname(__file__), "..", "scripts")
sys.path.insert(0, SCRIPTS_DIR)

_spec = importlib.util.spec_from_file_location(
    "validate_brief", os.path.join(SCRIPTS_DIR, "validate-brief.py"))
vb = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(vb)

REPO_ROOT = os.path.dirname(os.path.dirname(__file__))
COLLISION_DIRECTION_EVIDENCE_REQUIRED = vb.COLLISION_DIRECTION_EVIDENCE_REQUIRED

_HANDOFF_WITHOUT_FIELD = """## 13. Machine-readable handoff

```yaml
artifact_id: repository_sensemaking_brief
schema_version: 1
primary_fog_type: docs_fog
evidence:
  - "docs/adr/013-a.md and docs/adr/013-b.md both declare ADR 013"
recommended_workflow_id: docs-contract-reconciliation
created_at: "2026-08-13T00:00:00Z"
immutable: true
```
"""

_HANDOFF_WITH_FIELD = _HANDOFF_WITHOUT_FIELD.replace(
    'recommended_workflow_id: docs-contract-reconciliation',
    'collision_dedup_direction: "keep 013 on universe-to-series (9 references); '
    'series-graph has 0; grep incl. handoffs done"\n'
    'recommended_workflow_id: docs-contract-reconciliation',
)


def _write_brief(rec_steps: str, handoff: str, quote_only: str = "") -> str:
    body = (
        "# Repository Sensemaking Brief\n\n"
        "## 1. Repository goal\n\nTarget repo.\n\n"
        "## 6. Weakest boundary\n\nVocabulary Drift.\n\n"
        "Logic trace: the code is verified and healthy, so the weakest "
        "boundary is the documentation layer.\n\n"
        "## 7. Evidence\n\n"
        "`docs/adr/013-a.md` and `docs/adr/013-b.md` both declare ADR 013.\n\n"
        "## 10. Candidate next steps\n\n" + rec_steps + "\n\n"
        + handoff + "\n"
    )
    if quote_only:
        body += "## 8. Evidence excerpts\n\n```yaml\n" + quote_only + "\n```\n"
    fd, path = tempfile.mkstemp(suffix=".md")
    os.close(fd)
    with open(path, "w", encoding="utf-8") as f:
        f.write(body)
    return path


class TestCollisionDirectionEvidence(unittest.TestCase):
    def tearDown(self):
        pass

    def test_renumber_recommendation_without_direction_is_blocking(self):
        path = _write_brief(
            "Renumber the second ADR 013 to 018 and update references.",
            _HANDOFF_WITHOUT_FIELD,
        )
        try:
            errors = vb.validate_brief(path, REPO_ROOT)
            codes = [e.get("message", "") for e in errors]
            self.assertTrue(
                any(COLLISION_DIRECTION_EVIDENCE_REQUIRED in m for m in codes),
                f"expected {COLLISION_DIRECTION_EVIDENCE_REQUIRED} in {codes}",
            )
        finally:
            os.unlink(path)

    def test_renumber_recommendation_with_direction_passes(self):
        path = _write_brief(
            "Renumber the second ADR 013 to 018 and update references.",
            _HANDOFF_WITH_FIELD,
        )
        try:
            errors = vb.validate_brief(path, REPO_ROOT)
            self.assertFalse(
                any(COLLISION_DIRECTION_EVIDENCE_REQUIRED in e.get("message", "")
                    for e in errors),
            )
        finally:
            os.unlink(path)

    def test_quote_only_mention_is_not_a_recommendation(self):
        # "renumber" appears only inside a quoted evidence excerpt of the
        # TARGET's text; the actionable sections never recommend it.
        path = _write_brief(
            "Refresh the stale HANDOFF against measured state.",
            _HANDOFF_WITHOUT_FIELD,
            quote_only=(
                "evidence_excerpts:\n"
                '  - file: docs/adr/013-b.md\n'
                '    lines: L1\n'
                '    quote: "# ADR 013: Universe-to-Series renumber intent"\n'
                '    supports_claim: "quoted target text only"'
            ),
        )
        try:
            errors = vb.validate_brief(path, REPO_ROOT)
            self.assertFalse(
                any(COLLISION_DIRECTION_EVIDENCE_REQUIRED in e.get("message", "")
                    for e in errors),
            )
        finally:
            os.unlink(path)


if __name__ == "__main__":
    unittest.main()
