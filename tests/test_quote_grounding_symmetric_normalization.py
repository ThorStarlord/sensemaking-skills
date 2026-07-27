"""Regression tests for symmetric multiline quote-grounding normalization.

Background (Evidence 0015, experiments/evidence/0015-stage1-auteur-controlled-
learning-attempt/): a Stage 1 auteur-repo run reported four false
EVIDENCE_QUOTE_NOT_FOUND errors (excerpts 0, 1, 2, 4) for quotes that were, on
manual inspection, genuinely present at their cited source ranges. Read-only
investigation established:

  - CRLF handling was NOT the cause (disproven).
  - _normalize_for_grounding() was applied ASYMMETRICALLY: the quote was
    normalized as one multiline string (embedded "\\n<indent>" survived,
    collapsed only to "\\n "), while the source window was normalized
    line-by-line with each line individually .strip()ped before rejoining
    (indentation removed entirely). A logically identical multiline quote
    and source therefore normalized to different strings whenever a
    continuation line carried leading indentation.
  - All four failing excerpts are multiline; the two excerpts that passed
    (3, 5) are single-line, which is why they never hit the asymmetry (no
    embedded newline to normalize differently on either side).
  - Evidence 0013 uses a different, unrelated producer-transcription
    mechanism and is out of scope here; it is not touched or reclassified
    by this change.

Fix: scripts/validate-brief.py's _normalize_for_grounding() now splits ANY
input (quote or single source line) into lines, collapses horizontal
whitespace and strips each line individually, then rejoins with "\\n". The
same function, called the same way, is used for both the quote and each
source-window line, so a multiline quote and its logically equivalent source
excerpt always normalize identically regardless of continuation-line
indentation.

This is exact-text (line-stripped) matching, not semantic/fuzzy matching:
non-whitespace content still must match exactly, and the +/-3-line grounding
window, ambiguity detection, and deterministic tie-break are unchanged (see
tests/test_weakness_type_and_quote_contract.py::TestEvidenceQuoteGrounding
for pre-existing coverage of those, left intact by this change).
"""

import importlib.util
import os
import sys
import tempfile
import unittest

SCRIPTS_DIR = os.path.join(os.path.dirname(__file__), "..", "scripts")
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, SCRIPTS_DIR)

_spec = importlib.util.spec_from_file_location(
    "validate_brief", os.path.join(SCRIPTS_DIR, "validate-brief.py")
)
vb = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(vb)


def _by_code(errors, code):
    return [e for e in errors if e["message"].startswith(f"{code}:")]


def _write_tmp(content: str) -> str:
    fd, path = tempfile.mkstemp(suffix=".md")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(content)
    return path


def _brief_citing(lines: str, quote: str, file_name: str = "example.py") -> str:
    """Build a minimal brief citing ``quote`` at ``lines`` in ``file_name``.

    ``quote`` is the RAW quote text (real newlines allowed); this function
    performs the YAML double-quoted-scalar escaping itself (backslash,
    double-quote, then newline -> literal ``\\n``), in that order.
    """
    escaped = quote.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")
    return (
        "# Brief\n\n## 6. Weakest boundary\nZero Validation: fixture.\n\n"
        "## 7. Evidence\n- {f} cited.\n\nLogic trace: {f} "
        "supports this fixture's weakest-boundary claim.\n\n"
        "## 8. Evidence excerpts\n```yaml\nevidence_excerpts:\n"
        "  - file: {f}\n    lines: {lines}\n    quote: \"{quote}\"\n"
        "    supports_claim: \"demonstrates grounding\"\n```\n\n"
        "## 13. Machine-readable handoff\n```yaml\n"
        "primary_fog_type: architecture_fog\n"
        "evidence:\n  - \"{f}: cited for grounding\"\n"
        "recommended_workflow_id: full-local-sensemaking\n"
        "weakest_boundary: fixture\nweakness_type: Zero Validation\n"
        "required_inputs:\n  - repository_sensemaking_brief\n```\n"
    ).format(f=file_name, lines=lines, quote=escaped)


class TestNormalizeForGroundingSymmetry(unittest.TestCase):
    """Unit-level proof the normalization function itself is now symmetric."""

    def test_multiline_indented_quote_and_source_line_normalize_identically(self):
        # Minimal reproduction: a multiline quote whose second line is
        # indented, checked against source lines carrying the same
        # indentation. Pre-fix, normalizing the quote as one blob preserved
        # "\n " (one space) for the continuation line, while normalizing the
        # source line-by-line stripped it entirely -- so the two never
        # matched.
        quote = "\n".join(["first line", "    indented continuation"])
        source_lines = ["first line", "    indented continuation"]

        norm_quote = vb._normalize_for_grounding(quote)
        norm_source = "\n".join(vb._normalize_for_grounding(line) for line in source_lines)

        self.assertEqual(norm_quote, norm_source)
        self.assertEqual(norm_quote, "first line\nindented continuation")

    def test_asymmetry_reproduction_would_have_failed_pre_fix(self):
        # Demonstrates the exact old failure mode as a standalone assertion:
        # the old "normalize quote as a whole blob, but strip source lines
        # individually" combination produced different strings for
        # logically identical text.
        import re

        def old_blob_normalize(text: str) -> str:
            text = text.replace("\r\n", "\n").replace("\r", "\n")
            text = re.sub(r"[^\S\n]+", " ", text)
            return text.strip()

        quote = "\n".join(["first line", "    indented continuation"])
        source_lines = ["first line", "    indented continuation"]

        old_norm_quote = old_blob_normalize(quote)
        old_norm_source = "\n".join(old_blob_normalize(line) for line in source_lines)
        self.assertNotEqual(old_norm_quote, old_norm_source)  # the historical bug

        new_norm_quote = vb._normalize_for_grounding(quote)
        new_norm_source = "\n".join(vb._normalize_for_grounding(line) for line in source_lines)
        self.assertEqual(new_norm_quote, new_norm_source)

    def test_tabs_and_spaces_both_collapse_under_horizontal_whitespace_contract(self):
        quote = "\n".join(["first line", "\t\tindented with tabs"])
        source_lines = ["first line", "    indented with tabs"]
        norm_quote = vb._normalize_for_grounding(quote)
        norm_source = "\n".join(vb._normalize_for_grounding(line) for line in source_lines)
        self.assertEqual(norm_quote, norm_source)

    def test_different_non_whitespace_characters_still_differ(self):
        norm_a = vb._normalize_for_grounding("\n".join(["first line", "    indented continuation"]))
        norm_b = vb._normalize_for_grounding("\n".join(["first line", "    INDENTED CONTINUATION"]))
        self.assertNotEqual(norm_a, norm_b)


class TestMultilineQuoteGroundingEndToEnd(unittest.TestCase):
    """End-to-end validate_brief() coverage using the minimal repro shape."""

    def setUp(self):
        self._tmpdir = tempfile.TemporaryDirectory()
        self.target_repo = self._tmpdir.name

    def tearDown(self):
        self._tmpdir.cleanup()

    def _write_source(self, name: str, content: str, newline: str = "\n"):
        text = content.replace("\n", newline)
        with open(os.path.join(self.target_repo, name), "wb") as f:
            f.write(text.encode("utf-8"))

    def test_exact_indented_multiline_quote_matches(self):
        source = "\n".join(["first line", "    indented continuation", "last line"]) + "\n"
        self._write_source("indented.py", source)
        quote = "\n".join(["first line", "    indented continuation"])
        content = _brief_citing("1-2", quote, "indented.py")
        path = _write_tmp(content)
        try:
            errors = vb.validate_brief(path, REPO_ROOT, target_repo=self.target_repo)
            self.assertEqual(_by_code(errors, vb.EVIDENCE_QUOTE_NOT_FOUND), [])
        finally:
            os.remove(path)

    def test_genuinely_different_multiline_text_still_rejected(self):
        source = "\n".join(["first line", "    indented continuation", "last line"]) + "\n"
        self._write_source("indented.py", source)
        quote = "\n".join(["first line", "    a completely different continuation"])
        content = _brief_citing("1-2", quote, "indented.py")
        path = _write_tmp(content)
        try:
            errors = vb.validate_brief(path, REPO_ROOT, target_repo=self.target_repo)
            matches = _by_code(errors, vb.EVIDENCE_QUOTE_NOT_FOUND)
            self.assertEqual(len(matches), 1)
            self.assertEqual(matches[0]["severity"], "error")
        finally:
            os.remove(path)

    def test_line_ending_matrix_all_equivalent(self):
        # source LF/quote text, source CRLF/quote text: both must produce
        # the same (passing) result, and a quote containing raw CRLF must
        # behave the same as one containing raw LF.
        lf_quote = "\n".join(["first line", "    indented continuation"])
        crlf_quote = "\r\n".join(["first line", "    indented continuation"])
        source_text = "\n".join(["first line", "    indented continuation", "last line"]) + "\n"

        for source_newline in ("\n", "\r\n"):
            for quote_variant in (lf_quote, crlf_quote):
                with self.subTest(source_newline=repr(source_newline), quote=repr(quote_variant)):
                    self._write_source("matrix.py", source_text, newline=source_newline)
                    content = _brief_citing("1-2", quote_variant, "matrix.py")
                    path = _write_tmp(content)
                    try:
                        errors = vb.validate_brief(path, REPO_ROOT, target_repo=self.target_repo)
                        self.assertEqual(_by_code(errors, vb.EVIDENCE_QUOTE_NOT_FOUND), [])
                    finally:
                        os.remove(path)

    def test_normalize_for_grounding_crlf_quote_matches_lf_quote(self):
        # Direct unit check: a quote containing raw CRLF vs raw LF normalizes
        # identically (CRLF remains disproven as a distinct axis of failure;
        # this asserts it explicitly rather than relying on inference).
        lf_quote = "\n".join(["first line", "    indented continuation"])
        crlf_quote = "\r\n".join(["first line", "    indented continuation"])
        self.assertEqual(
            vb._normalize_for_grounding(lf_quote),
            vb._normalize_for_grounding(crlf_quote),
        )

    def test_single_line_quote_behavior_unchanged(self):
        self._write_source("single.py", "alpha\nbeta   gamma\ndelta\n")
        content = _brief_citing("2", "beta gamma", "single.py")
        path = _write_tmp(content)
        try:
            errors = vb.validate_brief(path, REPO_ROOT, target_repo=self.target_repo)
            self.assertEqual(_by_code(errors, vb.EVIDENCE_QUOTE_NOT_FOUND), [])
            self.assertEqual(_by_code(errors, vb.EVIDENCE_QUOTE_WINDOW_MATCH), [])
        finally:
            os.remove(path)


class TestEvidence0015RegressionFixtures(unittest.TestCase):
    """Regression fixtures using the actual Evidence 0015 excerpt/source pairs.

    Source text below is copied verbatim (minimal relevant excerpt only)
    from the pinned auteur target commit
    b40db654e0df9e90074f7ad85b40d7362378e07d, read-only, for use as a static
    test fixture -- no live network clone is performed during ordinary test
    execution. Quotes are copied verbatim from
    experiments/evidence/0015-stage1-auteur-controlled-learning-attempt/raw/
    repository_sensemaking_brief.md Section 8 (excerpt indices 0, 1, 2, 3, 4,
    5 in citation order). Excerpts 0, 1, 2, 4 are multiline and were the ones
    that produced false EVIDENCE_QUOTE_NOT_FOUND; excerpts 3 and 5 are
    single-line and already passed pre-fix -- both groups must keep behaving
    correctly post-fix. Each fixture pads with blank lines so the cited
    line numbers match the real file's line numbers.
    """

    def setUp(self):
        self._tmpdir = tempfile.TemporaryDirectory()
        self.target_repo = self._tmpdir.name

    def tearDown(self):
        self._tmpdir.cleanup()

    def _write(self, rel_path: str, lines_before: int, body_lines: list[str]):
        full = os.path.join(self.target_repo, rel_path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        text = ("\n" * lines_before) + "\n".join(body_lines) + "\n"
        with open(full, "w", encoding="utf-8", newline="\n") as f:
            f.write(text)

    def test_excerpt_0_adr013_multiline_now_matches(self):
        # docs/adr/ADR-013-Universe-to-Series-Propagation.md, cited L40-L43,
        # source lines 37-46 (pinned auteur@b40db65).
        self._write(
            "docs/adr/ADR-013-Universe-to-Series-Propagation.md",
            36,
            [
                '   - Boolean conditions (e.g., "no character resurrection")',
                "   - Enumerated relationships (faction membership, alliance rules)",
                "",
                "2. **Natural-Language Principles** (advisory, non-blocking)",
                '   - Free-text guidance (e.g., "stories should explore intimacy within power dynamics")',
                "   - Thematic directions without computational enforcement",
                "   - Narrative values that inform but do not mechanically block",
                "",
                "3. **LLM-Assisted Interpretation** (optional, V1 non-blocking)",
                '   - Semantic similarity checks (e.g., "tone consistency across books")',
            ],
        )
        quote = "\n".join(
            [
                "2. **Natural-Language Principles** (advisory, non-blocking)",
                '   - Free-text guidance (e.g., "stories should explore intimacy within power dynamics")',
                "   - Thematic directions without computational enforcement",
                "   - Narrative values that inform but do not mechanically block",
            ]
        )
        content = _brief_citing(
            "L40-L43", quote, "docs/adr/ADR-013-Universe-to-Series-Propagation.md"
        )
        path = _write_tmp(content)
        try:
            errors = vb.validate_brief(path, REPO_ROOT, target_repo=self.target_repo)
            self.assertEqual(_by_code(errors, vb.EVIDENCE_QUOTE_NOT_FOUND), [])
        finally:
            os.remove(path)

    def test_excerpt_1_models_py_multiline_now_matches(self):
        # src/auteur/universe/models.py, cited L65-L67, source lines 62-70.
        self._write(
            "src/auteur/universe/models.py",
            61,
            [
                '    magic_system: str = Field(default="", min_length=0)',
                '    core_mythology: str = Field(default="", min_length=0)',
                "    timeline: TimelineProfile",
                "    forbidden_elements: list[str] = Field(default_factory=list)",
                "    required_elements: list[str] = Field(default_factory=list)",
                "    cross_story_constraints: list[CrossStoryConstraint] = Field(default_factory=list)",
                "    structured_constraints: list[StructuredConstraint] = Field(default_factory=list)",
                "",
                '    @model_validator(mode="after")',
            ],
        )
        quote = "\n".join(
            [
                "    forbidden_elements: list[str] = Field(default_factory=list)",
                "    required_elements: list[str] = Field(default_factory=list)",
                "    cross_story_constraints: list[CrossStoryConstraint] = Field(default_factory=list)",
            ]
        )
        content = _brief_citing("L65-L67", quote, "src/auteur/universe/models.py")
        path = _write_tmp(content)
        try:
            errors = vb.validate_brief(path, REPO_ROOT, target_repo=self.target_repo)
            self.assertEqual(_by_code(errors, vb.EVIDENCE_QUOTE_NOT_FOUND), [])
        finally:
            os.remove(path)

    def test_excerpt_2_compiler_py_multiline_now_matches(self):
        # src/auteur/universe/compiler.py, cited L18-L19, source lines 15-22.
        self._write(
            "src/auteur/universe/compiler.py",
            14,
            [
                "def compile_universe_constraints(universe: UniverseIdentity) -> CompiledUniverseConstraints:",
                '    """Compile UniverseIdentity into a form optimized for validator use.',
                "",
                "    This creates a flat list of constraints that Series/Book validators can",
                "    quickly check against without needing the full UniverseIdentity structure.",
                '    """',
                "    constraint_rules = [",
                '        f"{c.rule} (severity: {c.severity})"',
            ],
        )
        quote = "\n".join(
            [
                "    This creates a flat list of constraints that Series/Book validators can",
                "    quickly check against without needing the full UniverseIdentity structure.",
            ]
        )
        content = _brief_citing("L18-L19", quote, "src/auteur/universe/compiler.py")
        path = _write_tmp(content)
        try:
            errors = vb.validate_brief(path, REPO_ROOT, target_repo=self.target_repo)
            self.assertEqual(_by_code(errors, vb.EVIDENCE_QUOTE_NOT_FOUND), [])
        finally:
            os.remove(path)

    def test_excerpt_4_universe_integration_py_multiline_now_matches(self):
        # src/auteur/series/universe_integration.py, cited L27-L35, source
        # lines 24-38.
        self._write(
            "src/auteur/series/universe_integration.py",
            23,
            [
                '        """',
                "        diagnostics: list[ValidationDiagnostic] = []",
                "",
                "        for constraint in constraints:",
                "            if constraint.type == ConstraintType.GENRE_RULE:",
                "                diagnostics.extend(self._validate_genre_constraint(series, constraint))",
                "            elif constraint.type == ConstraintType.THEMATIC_INVARIANT:",
                "                diagnostics.extend(self._validate_thematic_constraint(series, constraint))",
                "            elif constraint.type == ConstraintType.CHARACTER_STATE:",
                "                diagnostics.extend(self._validate_character_constraint(series, constraint))",
                "            elif constraint.type == ConstraintType.RELATIONSHIP_RULE:",
                "                diagnostics.extend(self._validate_relationship_constraint(series, constraint))",
                "",
                "        return diagnostics",
                "",
            ],
        )
        quote = "\n".join(
            [
                "        for constraint in constraints:",
                "            if constraint.type == ConstraintType.GENRE_RULE:",
                "                diagnostics.extend(self._validate_genre_constraint(series, constraint))",
                "            elif constraint.type == ConstraintType.THEMATIC_INVARIANT:",
                "                diagnostics.extend(self._validate_thematic_constraint(series, constraint))",
                "            elif constraint.type == ConstraintType.CHARACTER_STATE:",
                "                diagnostics.extend(self._validate_character_constraint(series, constraint))",
                "            elif constraint.type == ConstraintType.RELATIONSHIP_RULE:",
                "                diagnostics.extend(self._validate_relationship_constraint(series, constraint))",
            ]
        )
        content = _brief_citing(
            "L27-L35", quote, "src/auteur/series/universe_integration.py"
        )
        path = _write_tmp(content)
        try:
            errors = vb.validate_brief(path, REPO_ROOT, target_repo=self.target_repo)
            self.assertEqual(_by_code(errors, vb.EVIDENCE_QUOTE_NOT_FOUND), [])
        finally:
            os.remove(path)

    def test_excerpt_3_handlers_py_single_line_still_passes(self):
        # src/auteur/series/handlers.py, cited L159, single-line quote --
        # already passed pre-fix; must still pass post-fix (no regression).
        self._write(
            "src/auteur/series/handlers.py",
            158,
            [
                "        diagnostics = validate_series_against_universe(series, universe, universe.structured_constraints)",
            ],
        )
        quote = "diagnostics = validate_series_against_universe(series, universe, universe.structured_constraints)"
        content = _brief_citing("L159", quote, "src/auteur/series/handlers.py")
        path = _write_tmp(content)
        try:
            errors = vb.validate_brief(path, REPO_ROOT, target_repo=self.target_repo)
            self.assertEqual(_by_code(errors, vb.EVIDENCE_QUOTE_NOT_FOUND), [])
        finally:
            os.remove(path)

    def test_excerpt_5_test_universe_py_single_line_still_passes(self):
        # tests/test_universe.py, cited L227, single-line quote -- already
        # passed pre-fix; must still pass post-fix (no regression).
        self._write(
            "tests/test_universe.py",
            226,
            ["    compiled = compile_universe_constraints(universe)"],
        )
        quote = "compiled = compile_universe_constraints(universe)"
        content = _brief_citing("L227", quote, "tests/test_universe.py")
        path = _write_tmp(content)
        try:
            errors = vb.validate_brief(path, REPO_ROOT, target_repo=self.target_repo)
            self.assertEqual(_by_code(errors, vb.EVIDENCE_QUOTE_NOT_FOUND), [])
        finally:
            os.remove(path)


if __name__ == "__main__":
    unittest.main()
