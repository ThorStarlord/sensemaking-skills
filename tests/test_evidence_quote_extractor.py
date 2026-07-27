"""Tests for scripts/evidence_quote_extractor.py (issue #89).

Covers the deterministic quote-extraction safety/fidelity contract:
path-authority (absolute paths, traversal, escape), missing/undecodable
files, invalid line ranges, and fidelity of extracted text (Unicode
punctuation, indentation, tabs, Markdown formatting, CRLF/LF, blank lines,
multiline joins, first/last line, single-line ranges).

No real model/network call. No repository outside tests/fixtures is
written to (this module is read-only by construction).
"""

import os
import sys
import tempfile
import unittest

SCRIPTS_DIR = os.path.join(os.path.dirname(__file__), "..", "scripts")
sys.path.insert(0, SCRIPTS_DIR)

import evidence_quote_extractor as qe  # noqa: E402

FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures", "evidence-0013")
REPO_ROOT = os.path.dirname(os.path.dirname(__file__))


class TmpRootMixin:
    def setUp(self):
        self._tmpdir = tempfile.TemporaryDirectory()
        self.root = self._tmpdir.name

    def tearDown(self):
        self._tmpdir.cleanup()

    def write(self, relpath: str, content: str, newline: str = "\n") -> str:
        full = os.path.join(self.root, relpath)
        os.makedirs(os.path.dirname(full) or self.root, exist_ok=True)
        with open(full, "w", encoding="utf-8", newline="") as f:
            f.write(content.replace("\n", newline))
        return full


class TestPathAuthority(TmpRootMixin, unittest.TestCase):
    def test_rejects_absolute_posix_path(self):
        with self.assertRaises(qe.QuoteExtractionError):
            qe.resolve_repo_relative_path("/etc/passwd", self.root)

    def test_rejects_absolute_windows_path(self):
        with self.assertRaises(qe.QuoteExtractionError):
            qe.resolve_repo_relative_path("C:\\Windows\\system.ini", self.root)

    def test_rejects_dotdot_traversal(self):
        with self.assertRaises(qe.QuoteExtractionError):
            qe.resolve_repo_relative_path("../../etc/passwd", self.root)

    def test_rejects_embedded_dotdot(self):
        with self.assertRaises(qe.QuoteExtractionError):
            qe.resolve_repo_relative_path("sub/../../escape.txt", self.root)

    def test_rejects_empty_path(self):
        with self.assertRaises(qe.QuoteExtractionError):
            qe.resolve_repo_relative_path("", self.root)

    def test_rejects_none_path(self):
        with self.assertRaises(qe.QuoteExtractionError):
            qe.resolve_repo_relative_path(None, self.root)

    def test_accepts_plain_relative_path(self):
        self.write("a/b.py", "x = 1\n")
        resolved = qe.resolve_repo_relative_path("a/b.py", self.root)
        self.assertTrue(os.path.isfile(resolved))

    def test_symlink_escape_rejected_when_supported(self):
        target_outside = tempfile.TemporaryDirectory()
        try:
            secret = os.path.join(target_outside.name, "secret.txt")
            with open(secret, "w", encoding="utf-8") as f:
                f.write("secret\n")
            link_path = os.path.join(self.root, "escape_link")
            try:
                os.symlink(target_outside.name, link_path, target_is_directory=True)
            except (OSError, NotImplementedError):
                self.skipTest("symlinks not supported/permitted on this platform (Windows)")
            with self.assertRaises(qe.QuoteExtractionError):
                qe.resolve_repo_relative_path("escape_link/secret.txt", self.root)
        finally:
            target_outside.cleanup()


class TestExtractionErrors(TmpRootMixin, unittest.TestCase):
    def test_missing_file_rejected(self):
        with self.assertRaises(qe.QuoteExtractionError):
            qe.extract_quote("does_not_exist.py", 1, 1, self.root)

    def test_undecodable_file_rejected(self):
        full = os.path.join(self.root, "binary.dat")
        with open(full, "wb") as f:
            f.write(b"\xff\xfe\x00\x01binary")
        with self.assertRaises(qe.QuoteExtractionError):
            qe.extract_quote("binary.dat", 1, 1, self.root)

    def test_zero_line_rejected(self):
        self.write("f.py", "a\nb\nc\n")
        with self.assertRaises(qe.QuoteExtractionError):
            qe.extract_quote("f.py", 0, 1, self.root)

    def test_negative_line_rejected(self):
        self.write("f.py", "a\nb\nc\n")
        with self.assertRaises(qe.QuoteExtractionError):
            qe.extract_quote("f.py", -1, 1, self.root)

    def test_reversed_range_rejected(self):
        self.write("f.py", "a\nb\nc\n")
        with self.assertRaises(qe.QuoteExtractionError):
            qe.extract_quote("f.py", 3, 1, self.root)

    def test_out_of_bounds_rejected(self):
        self.write("f.py", "a\nb\nc\n")
        with self.assertRaises(qe.QuoteExtractionError):
            qe.extract_quote("f.py", 1, 100, self.root)

    def test_non_integer_lines_rejected(self):
        self.write("f.py", "a\nb\nc\n")
        with self.assertRaises(qe.QuoteExtractionError):
            qe.extract_quote("f.py", "abc", "def", self.root)


class TestFidelity(TmpRootMixin, unittest.TestCase):
    def test_em_dash_preserved(self):
        self.write("s.py", '"""Decision workspace service \u2014 compose real project state."""\n')
        result = qe.extract_quote("s.py", 1, 1, self.root)
        self.assertIn("\u2014", result.quote)
        self.assertNotIn("--", result.quote)

    def test_leading_indentation_preserved(self):
        self.write("f.py", "def f():\n    x = 1\n    return x\n")
        result = qe.extract_quote("f.py", 2, 2, self.root)
        self.assertEqual(result.quote, "    x = 1")

    def test_tabs_preserved(self):
        self.write("f.py", "def f():\n\tx = 1\n")
        result = qe.extract_quote("f.py", 2, 2, self.root)
        self.assertEqual(result.quote, "\tx = 1")

    def test_markdown_bold_and_backticks_preserved(self):
        self.write("CHANGELOG.md", "# Changelog\n\n- **`auteur decision status`**: shows state\n")
        result = qe.extract_quote("CHANGELOG.md", 3, 3, self.root)
        self.assertEqual(result.quote, "- **`auteur decision status`**: shows state")

    def test_multiline_with_blank_line_in_range(self):
        self.write("f.py", "a\nb\n\nd\n")
        result = qe.extract_quote("f.py", 1, 4, self.root)
        self.assertEqual(result.quote, "a\nb\n\nd")

    def test_multiline_joined_with_lf(self):
        self.write("f.py", "line1\nline2\nline3\n")
        result = qe.extract_quote("f.py", 1, 3, self.root)
        self.assertNotIn("\r", result.quote)
        self.assertEqual(result.quote, "line1\nline2\nline3")

    def test_crlf_source_extraction(self):
        self.write("f.py", "line1\nline2\nline3\n", newline="\r\n")
        result = qe.extract_quote("f.py", 2, 2, self.root)
        self.assertEqual(result.quote, "line2")
        self.assertNotIn("\r", result.quote)

    def test_lf_source_extraction(self):
        self.write("f.py", "line1\nline2\nline3\n", newline="\n")
        result = qe.extract_quote("f.py", 2, 2, self.root)
        self.assertEqual(result.quote, "line2")

    def test_first_line_of_file(self):
        self.write("f.py", "first\nsecond\nthird\n")
        result = qe.extract_quote("f.py", 1, 1, self.root)
        self.assertEqual(result.quote, "first")

    def test_last_line_of_file(self):
        self.write("f.py", "first\nsecond\nthird\n")
        result = qe.extract_quote("f.py", 3, 3, self.root)
        self.assertEqual(result.quote, "third")

    def test_single_line_range(self):
        self.write("f.py", "only one line of interest\nother\n")
        result = qe.extract_quote("f.py", 1, 1, self.root)
        self.assertEqual(result.quote, "only one line of interest")

    def test_trailing_spaces_preserved(self):
        self.write("f.py", "x = 1   \ny = 2\n")
        result = qe.extract_quote("f.py", 1, 1, self.root)
        self.assertEqual(result.quote, "x = 1   ")

    def test_unicode_code_points_preserved(self):
        self.write("f.py", "s = \"\u00e9\u00e8\u4e2d\u6587\"\n")
        result = qe.extract_quote("f.py", 1, 1, self.root)
        self.assertIn("\u4e2d\u6587", result.quote)


class TestFrameworkVsTargetRoot(TmpRootMixin, unittest.TestCase):
    """Framework root vs target root must be distinguishable -- extraction
    against one root must not silently fall through to the other."""

    def test_extraction_scoped_to_given_root_only(self):
        other = tempfile.TemporaryDirectory()
        try:
            with open(os.path.join(other.name, "only_in_other.py"), "w", encoding="utf-8") as f:
                f.write("secret = 1\n")
            with self.assertRaises(qe.QuoteExtractionError):
                qe.extract_quote("only_in_other.py", 1, 1, self.root)
            result = qe.extract_quote("only_in_other.py", 1, 1, other.name)
            self.assertEqual(result.quote, "secret = 1")
        finally:
            other.cleanup()

    def test_no_target_file_written(self):
        self.write("f.py", "a\nb\n")
        before = os.listdir(self.root)
        qe.extract_quote("f.py", 1, 1, self.root)
        after = os.listdir(self.root)
        self.assertEqual(before, after)


class TestParseLinesValue(unittest.TestCase):
    def test_bare_single_number(self):
        self.assertEqual(qe.parse_lines_value("18"), (18, 18))

    def test_bare_range(self):
        self.assertEqual(qe.parse_lines_value("25-30"), (25, 30))

    def test_l_prefixed_single(self):
        self.assertEqual(qe.parse_lines_value("L18"), (18, 18))

    def test_l_prefixed_range(self):
        self.assertEqual(qe.parse_lines_value("L25-L30"), (25, 30))

    def test_invalid_format_rejected(self):
        with self.assertRaises(qe.QuoteExtractionError):
            qe.parse_lines_value("not-a-range")


class TestEvidence0013Reconstruction(unittest.TestCase):
    """Reconstructs Evidence 0013's three real fidelity failures against
    fixture copies (tests/fixtures/evidence-0013/), never against the
    evidence directory itself, to prove exact-text extraction where the
    model's hand-transcription previously failed.
    """

    def test_em_dash_docstring_extracted_exactly(self):
        result = qe.extract_quote("service_py_snippet.py", 1, 1, FIXTURES_DIR)
        self.assertEqual(
            result.quote,
            '"""Decision workspace service \u2014 compose real project state from subsystems."""',
        )

    def test_indented_cli_parser_line_extracted_exactly(self):
        result = qe.extract_quote("cli_parser_snippet.py", 2, 2, FIXTURES_DIR)
        self.assertEqual(result.quote, '    decision_parser = subparsers.add_parser(')

    def test_changelog_bold_backtick_line_extracted_exactly(self):
        result = qe.extract_quote("CHANGELOG_snippet.md", 7, 7, FIXTURES_DIR)
        self.assertEqual(
            result.quote,
            "- **`auteur decision status`**: show the current decision workspace state \u2014 including pending items.",
        )


if __name__ == "__main__":
    unittest.main()
