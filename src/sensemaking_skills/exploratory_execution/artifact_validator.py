"""Campaign artifact validator for repository_sensemaking_brief (Phase 6).

The validator is FRAMEWORK-GOVERNED and byte-exact: it delegates to the
canonical pinned validator ``scripts/validate-brief.py`` (the SAME
authority the canonical lane uses), invoked from the pinned framework
checkout against the verified TARGET checkout. No validation logic is
duplicated here.

Flow:

1. extract the candidate artifact from the raw provider response
   (the full response text; the canonical validator locates the headings
   and the machine-readable handoff block itself);
2. write the artifact to a runtime-owned temp file;
3. run ``validate-brief.py <tmp> --repo-root <framework> --target-repo
   <target> --json`` (deterministic, pinned, subprocess);
4. classify every error code into structural / substantive /
   environmental and report counts in ``details``, so the execution
   report can emit structural and substantive pass rates separately
   (Issue #122);
5. return a ``ValidationOutcome`` that always preserves the extracted
   artifact content for the durable recorder.

A validator subprocess failure is an honest VALIDATION_FAILED (the raw
output is preserved and visible), never a silent pass.
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

from sensemaking_skills.campaign_accounting import ValidationOutcome

#: Error-code classification (Issue #122 structural vs substantive rates).
#: Environmental failures (missing brief file, missing registry) are the
#: runtime's fault, never the model's, and are reported separately.
STRUCTURAL_CODES = frozenset(
    {
        "PARSING_ERROR",
        "MALFORMED_HANDOFF_FENCE",
        "HANDOFF_YAML_PARSE_ERROR",
        "MISSING_HANDOFF_BLOCK",
        "MISSING_HANDOFF_SECTION",
        "MISSING_EVIDENCE_EXCERPTS",
        "EVIDENCE_EXCERPT_FIELD",
        "INVALID_LINE_FORMAT",
        "MISSING_WEAKNESS_TYPE",
        "DUPLICATE_WEAKNESS_TYPE_KEYS",
    }
)
SUBSTANTIVE_CODES = frozenset(
    {
        "NO_LOGIC_TRACE",
        "NO_EVIDENCE_FILE_CITATIONS",
        "HALLUCINATED_FILE",
        "EVIDENCE_QUOTE_NOT_FOUND",
        "EVIDENCE_QUOTE_WINDOW_MATCH",
        "MISSING_WORKFLOW_ID",
        "HALLUCINATED_WORKFLOW_ID",
        "WEAKNESS_TYPE_MISSING",
        "WEAKNESS_TYPE_UNKNOWN",
        "WEAKNESS_TYPE_OTHER_NO_EXPLANATION",
        "WEAKNESS_TYPE_MALFORMED",
        "WEAKNESS_TYPE_PROSE_MISMATCH",
        "HIGH_RISK_CLAIM_NEEDS_SUBSTANTIVE_AUDIT",
    }
)
# PROBE_REPORT_NOT_FOUND: the caller passed --probe-report <path> and that path
# does not exist. Like a missing brief file or registry, this is a runtime
# invocation problem (a bad same-episode probe-report path), never the model's
# fault -- classified environmental so structural/substantive rates stay clean.
ENVIRONMENTAL_CODES = frozenset(
    {"BRIEF_FILE_NOT_FOUND", "REGISTRY_NOT_FOUND", "PROBE_REPORT_NOT_FOUND"}
)


def _code_of(message: str) -> str:
    return message.split(":", 1)[0].strip()


class CampaignBriefValidator:
    """Validates a raw provider response as a repository_sensemaking_brief
    using the pinned canonical validator."""

    def __init__(
        self,
        *,
        framework_checkout: Path,
        target_checkout: Path,
        python: str | None = None,
    ) -> None:
        self._framework_checkout = Path(framework_checkout)
        self._target_checkout = Path(target_checkout)
        self._python = python or sys.executable

    def _validator_script(self) -> Path:
        script = self._framework_checkout / "scripts" / "validate-brief.py"
        if not script.is_file():
            raise RuntimeError(
                f"pinned framework checkout has no canonical validator at "
                f"{script}; refusing to validate without the pinned authority"
            )
        return script

    def __call__(self, raw: bytes) -> ValidationOutcome:
        artifact_text = raw.decode("utf-8", errors="replace")
        # A response with no YAML handoff block cannot be a brief; the
        # canonical validator would reject it, but fail fast with an honest
        # structural outcome (and still preserve the raw output).
        if "```yaml" not in artifact_text:
            return ValidationOutcome(
                passed=False,
                details={
                    "structural": {
                        "passed": 0,
                        "total": 1,
                        "errors": ["MISSING_HANDOFF_BLOCK"],
                    },
                    "substantive": {"passed": 0, "total": 0, "errors": []},
                    "environmental": [],
                    "validator": "validate-brief.py",
                },
                artifact_content=artifact_text,
                artifact_filename="produced-artifact.md",
            )

        script = self._validator_script()
        try:
            with tempfile.NamedTemporaryFile(
                "w", suffix=".md", encoding="utf-8", delete=False
            ) as f:
                f.write(artifact_text)
                tmp_path = f.name
            try:
                result = subprocess.run(
                    [
                        self._python,
                        str(script),
                        tmp_path,
                        "--repo-root",
                        str(self._framework_checkout),
                        "--target-repo",
                        str(self._target_checkout),
                        "--json",
                    ],
                    capture_output=True,
                    text=True,
                    timeout=300,
                    check=False,
                )
                verdict = json.loads(result.stdout or "{}")
            finally:
                Path(tmp_path).unlink(missing_ok=True)
        except Exception as exc:  # noqa: BLE001 - validator crash -> honest failure, never pass
            return ValidationOutcome(
                passed=False,
                details={
                    "structural": {"passed": 0, "total": 0, "errors": []},
                    "substantive": {"passed": 0, "total": 0, "errors": []},
                    "environmental": [f"VALIDATOR_RUNTIME_FAILURE: {exc}"],
                    "validator": "validate-brief.py",
                },
                artifact_content=artifact_text,
                artifact_filename="produced-artifact.md",
            )

        errors = verdict.get("errors") or []
        codes = [_code_of(str(e.get("message", ""))) for e in errors]
        structural = [
            c for c in codes if c in STRUCTURAL_CODES
        ]
        substantive = [c for c in codes if c in SUBSTANTIVE_CODES]
        environmental = [
            c for c in codes if c in ENVIRONMENTAL_CODES
        ]
        valid = bool(verdict.get("valid", False))
        details: dict[str, Any] = {
            "structural": {
                "passed": 0 if structural else 1,
                "total": 1,
                "errors": structural,
            },
            "substantive": {
                "passed": 0 if substantive else 1,
                "total": 1,
                "errors": substantive,
            },
            "environmental": environmental,
            "validator": "validate-brief.py",
            "validator_exit": result.returncode,
        }
        return ValidationOutcome(
            passed=bool(valid and not environmental),
            details=details,
            artifact_content=artifact_text,
            artifact_filename="produced-artifact.md",
        )
