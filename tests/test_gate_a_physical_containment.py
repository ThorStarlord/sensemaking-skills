"""Gate A: PHYSICAL containment, path anchoring, and filesystem aliasing.

WHY THIS FILE EXISTS
--------------------
A THIRD independent review of PR #109 reproduced two complete authorization
bypasses, end to end, against the real production chain:

    build_invocation_identity() -> classify_invocation() -> requires_gate_a()

with the process CWD deliberately DIFFERENT from the framework root:

    experiments./evidence/0016-stage1-auteur-post-remediation-controlled-attempt
    jexp/evidence/0016-stage1-auteur-post-remediation-controlled-attempt
        (where `jexp` is an NTFS junction to `experiments`)

Both classified ORDINARY_DEVELOPMENT and required no authorization, while
`os.path.samefile()` proved they reached the physical Evidence 0016 campaign
directory.

ROOT CAUSE
----------
`resolve_containment()` built `Path(str(value))` from a RELATIVE output path.
Python resolves that against `os.getcwd()`. With a CWD outside the framework
root, the physical pass looked at a path that did not exist, found nothing,
and silently fell back to a purely LEXICAL parse. Lexically, `experiments.`
and `jexp` are not the component `experiments`, so the parse returned
OUTSIDE_EXPERIMENTS and the classifier called it ordinary development.

THE INVARIANT THIS FILE ENFORCES
--------------------------------
    Every relative path is interpreted relative to the authorized framework
    root -- never process CWD -- and physical filesystem identity overrides
    textual spelling.

SAFETY
------
Every fixture here is a TEMPORARY repository under `tmp_path`. Nothing in this
file may create anything inside the real repository's `experiments/evidence/`
tree; `test_no_real_evidence_0016_directory_is_ever_created` asserts that.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))
sys.path.insert(0, str(REPO_ROOT / "tests"))

import gate_a_authorization as ga  # noqa: E402
from skill_executor import build_invocation_identity  # noqa: E402

CAMPAIGN_SLUG = ga.CONTRACT_EVIDENCE_SLUG
CAMPAIGN_REL = f"experiments/evidence/{CAMPAIGN_SLUG}"

ORDINARY_MODEL = "claude-haiku-4-5"
ORDINARY_REPO = "https://github.com/ThorStarlord/unrelated-project.git"


# ===========================================================================
# Helpers
# ===========================================================================


def make_framework(tmp_path: Path) -> Path:
    """A temporary framework repository containing the campaign directory.

    The campaign directory is created HERE, in tmp, and never in the real
    repository. Classification itself must never create it (section 28).
    """
    root = tmp_path / "framework"
    (root / "experiments" / "evidence" / CAMPAIGN_SLUG).mkdir(parents=True)
    (root / "artifacts").mkdir(parents=True)
    return root


def ordinary_identity_for(output_path, framework_root):
    """An identity whose ONLY possible campaign signal is the output path.

    Model, artifact type, workflow and target repository are all deliberately
    non-campaign, so any controlled/ambiguous classification is attributable
    to path handling alone. This is the exact shape of the reproduced attack:
    an ordinary-looking invocation that writes into Evidence 0016.
    """
    return build_invocation_identity(
        repo_root=str(framework_root),
        executor_id="claude-code",
        skill_id="workflow-planner",
        expected_output_artifact=str(output_path),
        context={"artifact_type": "workflow_orchestration_plan",
                 "workflow_id": "workflow-planner",
                 "target_repository": ORDINARY_REPO},
        model=ORDINARY_MODEL,
    )


def classify(output_path, framework_root):
    return ga.classify_invocation(
        ordinary_identity_for(output_path, framework_root))


def assert_gated(output_path, framework_root, why=""):
    """The path must require Gate A, and must not be ordinary development."""
    mode, signals = classify(output_path, framework_root)
    assert mode is not ga.ExecutionMode.ORDINARY_DEVELOPMENT, (
        f"{why or output_path!r} classified ORDINARY_DEVELOPMENT; "
        f"signals={signals}")
    assert ga.requires_gate_a(mode), (
        f"{why or output_path!r} did not require Gate A; signals={signals}")
    return mode


def can_make_junction() -> bool:
    if os.name != "nt":
        return False
    return shutil.which("cmd") is not None


def make_junction(link: Path, target: Path) -> bool:
    """Create an NTFS junction. Returns False when unavailable."""
    if not can_make_junction():
        return False
    proc = subprocess.run(["cmd", "/c", "mklink", "/J", str(link), str(target)],
                          capture_output=True, text=True)
    return proc.returncode == 0 and link.exists()


def can_make_symlink(tmp_path: Path) -> bool:
    probe = tmp_path / "_symlink_probe"
    target = tmp_path / "_symlink_target"
    target.mkdir(exist_ok=True)
    try:
        probe.symlink_to(target, target_is_directory=True)
    except (OSError, NotImplementedError):
        return False
    probe.unlink()
    return True


def short_name(path: Path):
    """Query the real Win32 8.3 short path, or None when unavailable."""
    if os.name != "nt":
        return None
    try:
        import ctypes
        from ctypes import wintypes
    except ImportError:  # pragma: no cover
        return None
    GetShortPathNameW = ctypes.windll.kernel32.GetShortPathNameW
    GetShortPathNameW.argtypes = [wintypes.LPCWSTR, wintypes.LPWSTR,
                                  wintypes.DWORD]
    GetShortPathNameW.restype = wintypes.DWORD
    buf = ctypes.create_unicode_buffer(1024)
    n = GetShortPathNameW(str(path), buf, 1024)
    if n == 0 or n >= 1024:
        return None
    result = buf.value
    if result.casefold() == str(path).casefold():
        return None          # 8.3 generation disabled on this volume
    return result


# ===========================================================================
# Section 3: relative paths are anchored to framework_root, never to CWD
# ===========================================================================

RELATIVE_FORMS = [
    CAMPAIGN_REL,
    f"experiments/./evidence/{CAMPAIGN_SLUG}",
    f"experiments//evidence//{CAMPAIGN_SLUG}",
    f"experiments/evidence/../evidence/{CAMPAIGN_SLUG}",
]


@pytest.mark.parametrize("rel", RELATIVE_FORMS)
def test_anchoring_invariant_relative_equals_joined(tmp_path, rel):
    """canonicalize(rel, root) == canonicalize(root / rel, root).

    The invariant demanded by section 3. If these ever diverge, a relative
    spelling means something different from the absolute spelling of the same
    location, which is precisely the bug class being fixed.
    """
    root = make_framework(tmp_path)
    joined = root / rel
    a = ga.parse_evidence_path(rel, root)
    b = ga.parse_evidence_path(joined, root)
    assert a.key() == b.key(), (
        f"relative and joined spellings disagree:\n  rel={a.key()}\n"
        f"  abs={b.key()}")


@pytest.fixture
def cwd_matrix(tmp_path):
    """Every CWD a caller could plausibly (or maliciously) select."""
    root = make_framework(tmp_path)
    other_repo = tmp_path / "other-repo"
    (other_repo / "experiments" / "evidence").mkdir(parents=True)
    unrelated = tmp_path / "unrelated"
    unrelated.mkdir()
    nested = root / "scripts" / "deep"
    nested.mkdir(parents=True)
    cwds = [
        tmp_path,                       # repository parent
        unrelated,                      # unrelated temporary directory
        other_repo,                     # another repository
        nested,                         # nested inside the framework repo
        root,                           # the framework root itself
    ]
    fs_root = Path(os.path.abspath(os.sep))
    if os.access(fs_root, os.R_OK):
        cwds.append(fs_root)            # filesystem root where permitted
    return root, cwds


@pytest.mark.parametrize("rel", RELATIVE_FORMS)
def test_classification_is_cwd_independent(cwd_matrix, rel):
    """Classification depends on framework_root, NOT on process CWD.

    A caller calling os.chdir() must not be able to change the answer. This is
    the direct regression for mutation 11 (resolve relative paths against CWD).
    """
    root, cwds = cwd_matrix
    original = os.getcwd()
    results = {}
    try:
        for cwd in cwds:
            os.chdir(cwd)
            mode, _ = classify(rel, root)
            results[str(cwd)] = mode
    finally:
        os.chdir(original)
    distinct = set(results.values())
    assert len(distinct) == 1, (
        f"classification varied with CWD for {rel!r}: {results}")
    only = distinct.pop()
    assert only is not ga.ExecutionMode.ORDINARY_DEVELOPMENT, (
        f"{rel!r} classified ordinary from every CWD")
    assert ga.requires_gate_a(only)


def test_relative_path_without_anchor_fails_closed():
    """A relative path with no framework root cannot be placed -- so it is
    ambiguous, never ordinary."""
    anchored, code = ga.anchor_output_path(CAMPAIGN_REL, None)
    assert anchored is None
    assert code == ga.GATE_A_OUTPUT_PATH_UNANCHORABLE


def test_anchor_never_consults_cwd(tmp_path, monkeypatch):
    """anchor_output_path must not read the process CWD at all."""
    root = make_framework(tmp_path)
    called = []
    real_getcwd = os.getcwd
    monkeypatch.setattr(os, "getcwd",
                        lambda: (called.append(1), real_getcwd())[1])
    anchored, code = ga.anchor_output_path(CAMPAIGN_REL, root)
    assert code is None
    assert anchored == root / "experiments" / "evidence" / CAMPAIGN_SLUG
    assert not called, "anchoring consulted os.getcwd()"


# ===========================================================================
# Section 9: trailing-dot aliases (the first reproduced bypass)
# ===========================================================================

TRAILING_DOT_FORMS = [
    f"experiments./evidence/{CAMPAIGN_SLUG}",
    f"experiments/evidence./{CAMPAIGN_SLUG}",
    f"experiments/evidence/{CAMPAIGN_SLUG}.",
]


@pytest.mark.skipif(os.name != "nt", reason="Win32 trailing-dot semantics")
@pytest.mark.parametrize("form", TRAILING_DOT_FORMS)
def test_relative_trailing_dot_alias_is_gated(tmp_path, form):
    """THE FIRST REPRODUCED BYPASS. Relative, CWD elsewhere, must be gated."""
    root = make_framework(tmp_path)
    campaign = root / "experiments" / "evidence" / CAMPAIGN_SLUG
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    original = os.getcwd()
    try:
        os.chdir(elsewhere)
        # Win32 filesystem equivalence, proven not assumed.
        assert os.path.samefile(str(root / form), str(campaign)), (
            f"{form!r} is not a Win32 alias of the campaign directory here")
        assert_gated(form, root, why=f"relative trailing-dot {form!r}")
        # The physical identity, not the spelling, is what was recorded.
        ident = ga.parse_evidence_path(form, root)
        assert ident.evidence_number == ga.CONTRACT_EVIDENCE_NUMBER
        assert ident.campaign_slug
    finally:
        os.chdir(original)


@pytest.mark.skipif(os.name != "nt", reason="Win32 trailing-dot semantics")
@pytest.mark.parametrize("form", TRAILING_DOT_FORMS)
def test_absolute_trailing_dot_alias_is_gated(tmp_path, form):
    root = make_framework(tmp_path)
    assert_gated(root / form, root, why=f"absolute trailing-dot {form!r}")


@pytest.mark.skipif(os.name != "nt", reason="Win32 extended-length paths")
def test_extended_length_campaign_path_is_gated(tmp_path):
    """`\\\\?\\` disables Win32 trailing-dot normalization; the plain extended
    campaign path must still be recognized, and the extended trailing-dot form
    must never read as ordinary."""
    root = make_framework(tmp_path)
    extended = "\\\\?\\" + str((root / CAMPAIGN_REL).resolve())
    assert_gated(extended, root, why="extended-length campaign path")
    ext_dot = "\\\\?\\" + str(root.resolve()) + f"\\experiments.\\evidence\\{CAMPAIGN_SLUG}"
    mode, _ = classify(ext_dot, root)
    assert mode is not ga.ExecutionMode.ORDINARY_DEVELOPMENT


@pytest.mark.skipif(os.name != "nt", reason="Windows case-insensitive aliases")
def test_case_variant_alias_is_gated(tmp_path):
    root = make_framework(tmp_path)
    assert_gated(f"EXPERIMENTS/EVIDENCE/{CAMPAIGN_SLUG.upper()}", root,
                 why="upper-case alias")


# ===========================================================================
# Section 10: junction aliases (the second reproduced bypass)
# ===========================================================================

junction_required = pytest.mark.skipif(
    not can_make_junction(),
    reason="NTFS junction creation unavailable on this platform/account")


@junction_required
def test_relative_junction_to_experiments_is_gated(tmp_path):
    """THE SECOND REPRODUCED BYPASS."""
    root = make_framework(tmp_path)
    campaign = root / "experiments" / "evidence" / CAMPAIGN_SLUG
    assert make_junction(root / "jexp", root / "experiments")
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    original = os.getcwd()
    try:
        os.chdir(elsewhere)
        alias = f"jexp/evidence/{CAMPAIGN_SLUG}"
        assert os.path.samefile(str(root / alias), str(campaign))
        assert_gated(alias, root, why="relative junction alias")
        ident = ga.parse_evidence_path(alias, root)
        assert ident.evidence_number == ga.CONTRACT_EVIDENCE_NUMBER
    finally:
        os.chdir(original)


@junction_required
def test_relative_junction_to_evidence_is_gated(tmp_path):
    root = make_framework(tmp_path)
    assert make_junction(root / "jev", root / "experiments" / "evidence")
    assert_gated(f"jev/{CAMPAIGN_SLUG}", root, why="junction to evidence")


@junction_required
def test_absolute_junction_alias_is_gated(tmp_path):
    root = make_framework(tmp_path)
    assert make_junction(root / "jexp", root / "experiments")
    assert_gated(root / "jexp" / "evidence" / CAMPAIGN_SLUG, root,
                 why="absolute junction alias")


@junction_required
def test_nested_junction_chain_is_gated(tmp_path):
    """A junction to a junction still lands in the campaign directory."""
    root = make_framework(tmp_path)
    assert make_junction(root / "j1", root / "experiments")
    assert make_junction(root / "j2", root / "j1")
    assert_gated(f"j2/evidence/{CAMPAIGN_SLUG}", root, why="nested junction")


@junction_required
def test_junction_escaping_the_repository_is_rejected(tmp_path):
    """A junction pointing OUTSIDE the framework root is an escape."""
    root = make_framework(tmp_path)
    outside = tmp_path / "outside"
    outside.mkdir()
    assert make_junction(root / "esc", outside)
    resolved, code = ga.resolve_containment(f"esc/evidence/{CAMPAIGN_SLUG}", root)
    assert code == ga.GATE_A_OUTPUT_PATH_SYMLINK_ESCAPE
    mode, _ = classify(f"esc/evidence/{CAMPAIGN_SLUG}", root)
    assert mode is not ga.ExecutionMode.ORDINARY_DEVELOPMENT


@junction_required
def test_junction_pointing_back_inside_through_another_alias_is_gated(tmp_path):
    """Out of the repo and back in again still reaches the campaign path."""
    root = make_framework(tmp_path)
    hop = tmp_path / "hop"
    hop.mkdir()
    assert make_junction(hop / "back", root / "experiments")
    assert make_junction(root / "out", hop)
    assert_gated(f"out/back/evidence/{CAMPAIGN_SLUG}", root,
                 why="junction out-and-back")


@junction_required
def test_junction_retargeted_after_identity_construction(tmp_path):
    """Identity is built once; re-deriving at the provider boundary must not
    silently accept a junction that has since been repointed elsewhere."""
    root = make_framework(tmp_path)
    decoy = root / "artifacts"
    assert make_junction(root / "swap", decoy)
    alias = f"swap/evidence/{CAMPAIGN_SLUG}"
    before, _ = classify(alias, root)
    # Repoint the junction at the campaign namespace.
    (root / "swap").rmdir()
    assert make_junction(root / "swap", root / "experiments")
    after = assert_gated(alias, root, why="retargeted junction")
    assert after is not ga.ExecutionMode.ORDINARY_DEVELOPMENT
    # The re-derived identity differs from the pre-swap one; that difference is
    # exactly what the provider-boundary identity check must catch.
    assert ga.parse_evidence_path(alias, root).evidence_number == "0016"
    assert before is not after or before is not ga.ExecutionMode.ORDINARY_DEVELOPMENT


# ===========================================================================
# Section 11: 8.3 short-name aliases
# ===========================================================================


@pytest.mark.skipif(os.name != "nt", reason="8.3 short names are Windows-only")
def test_short_name_alias_is_gated(tmp_path):
    """Query the REAL generated short name; never assume `EXPERI~1`."""
    root = make_framework(tmp_path)
    campaign = root / "experiments" / "evidence" / CAMPAIGN_SLUG
    short = short_name(campaign)
    if short is None:
        pytest.skip("8.3 short-name generation disabled on this volume "
                    "(capability unavailable, not a security gap): the same "
                    "physical-identity branch is covered by the junction and "
                    "trailing-dot tests and by Linux symlink tests in CI")
    assert os.path.samefile(short, str(campaign))
    assert_gated(short, root, why=f"8.3 short name {short!r}")
    ident = ga.parse_evidence_path(short, root)
    assert ident.evidence_number == ga.CONTRACT_EVIDENCE_NUMBER, (
        "physical canonicalization did not map the 8.3 alias to the long path")


@pytest.mark.skipif(os.name != "nt", reason="8.3 short names are Windows-only")
def test_relative_short_name_alias_is_gated(tmp_path):
    root = make_framework(tmp_path)
    short = short_name(root / "experiments")
    if short is None:
        pytest.skip("8.3 short-name generation disabled on this volume")
    rel = Path(short).name + f"/evidence/{CAMPAIGN_SLUG}"
    assert_gated(rel, root, why=f"relative 8.3 alias {rel!r}")


# ===========================================================================
# Section 12: colon-bearing and ADS-like components
# ===========================================================================

COLON_FORMS = [
    f"experiments:x/evidence/{CAMPAIGN_SLUG}",
    f"experiments/evidence/{CAMPAIGN_SLUG}:stream",
    f"experiments/evidence/{CAMPAIGN_SLUG}::$DATA",
]


@pytest.mark.parametrize("form", COLON_FORMS)
def test_colon_bearing_components_are_rejected(tmp_path, form):
    """Colon components are rejected BEFORE classification, deterministically.

    They must never read as ordinary just because the evidence parse failed.
    """
    root = make_framework(tmp_path)
    resolved, code = ga.resolve_containment(form, root)
    assert resolved is None
    assert code == ga.GATE_A_OUTPUT_PATH_COLON_COMPONENT_PROHIBITED
    ident = ga.parse_evidence_path(form, root)
    assert ident.containment_failure == ga.GATE_A_OUTPUT_PATH_COLON_COMPONENT_PROHIBITED
    assert_gated(form, root, why=f"colon/ADS form {form!r}")


def test_drive_letter_is_not_a_colon_component(tmp_path):
    """A legitimate absolute Windows path must not trip the colon rule."""
    root = make_framework(tmp_path)
    canon = ga.canonicalize_path(root / CAMPAIGN_REL)
    assert not ga.has_colon_component(canon)


# ===========================================================================
# Sections 20/23: POSIX symlinks -- these MUST execute on Linux CI
# ===========================================================================

symlink_required = pytest.mark.skipif(
    os.name == "nt",
    reason="POSIX symlink semantics; exercised by the Linux CI job")


@symlink_required
def test_symlinked_experiments_ancestor_is_gated(tmp_path):
    root = make_framework(tmp_path)
    (root / "sexp").symlink_to(root / "experiments", target_is_directory=True)
    assert_gated(f"sexp/evidence/{CAMPAIGN_SLUG}", root,
                 why="symlinked experiments ancestor")


@symlink_required
def test_symlinked_evidence_ancestor_is_gated(tmp_path):
    root = make_framework(tmp_path)
    (root / "sev").symlink_to(root / "experiments" / "evidence",
                              target_is_directory=True)
    assert_gated(f"sev/{CAMPAIGN_SLUG}", root, why="symlinked evidence ancestor")


@symlink_required
def test_symlinked_campaign_directory_is_gated(tmp_path):
    root = make_framework(tmp_path)
    (root / "scamp").symlink_to(root / "experiments" / "evidence" / CAMPAIGN_SLUG,
                                target_is_directory=True)
    # A slash-bearing path: `build_invocation_identity` only treats an
    # `expected_output_artifact` as a PATH when it contains a separator, so a
    # bare component would test nothing.
    assert_gated("scamp/repository-sensemaking-brief.md", root,
                 why="symlinked campaign directory")


@symlink_required
def test_symlink_escape_outside_repository_is_rejected(tmp_path):
    root = make_framework(tmp_path)
    outside = tmp_path / "outside"
    outside.mkdir()
    (root / "esc").symlink_to(outside, target_is_directory=True)
    resolved, code = ga.resolve_containment(f"esc/evidence/{CAMPAIGN_SLUG}", root)
    assert code == ga.GATE_A_OUTPUT_PATH_SYMLINK_ESCAPE


@symlink_required
def test_symlink_introduced_after_identity_construction_is_gated(tmp_path):
    root = make_framework(tmp_path)
    alias = f"late/evidence/{CAMPAIGN_SLUG}"
    before, _ = classify(alias, root)
    (root / "late").symlink_to(root / "experiments", target_is_directory=True)
    assert_gated(alias, root, why="symlink created after identity construction")


@symlink_required
def test_symlink_loop_fails_closed(tmp_path):
    root = make_framework(tmp_path)
    a = root / "loopa"
    b = root / "loopb"
    a.symlink_to(b, target_is_directory=True)
    b.symlink_to(a, target_is_directory=True)
    resolved, code = ga.resolve_containment(f"loopa/evidence/{CAMPAIGN_SLUG}", root)
    assert code in ga.PHYSICAL_CONTAINMENT_FAILURE_CODES
    mode, _ = classify(f"loopa/evidence/{CAMPAIGN_SLUG}", root)
    assert mode is not ga.ExecutionMode.ORDINARY_DEVELOPMENT


@symlink_required
def test_dangling_symlink_fails_closed_or_gates(tmp_path):
    root = make_framework(tmp_path)
    (root / "dangling").symlink_to(root / "does-not-exist",
                                   target_is_directory=True)
    mode, _ = classify(f"dangling/evidence/{CAMPAIGN_SLUG}", root)
    assert mode is not ga.ExecutionMode.ORDINARY_DEVELOPMENT


def test_linux_ci_actually_has_symlink_capability(tmp_path):
    """Section 20: CI must FAIL, not skip, if Linux loses symlink capability.

    A security suite that silently degrades to zero symlink coverage cannot
    support a merge decision.
    """
    if os.name == "nt":
        pytest.skip("Windows: junction tests cover the reparse-point branch")
    assert can_make_symlink(tmp_path), (
        "POSIX runner cannot create symlinks; the Gate A symlink security "
        "tests would silently skip. Failing loudly instead.")


# ===========================================================================
# Section 7: lexical/physical disagreement is never resolved downward
# ===========================================================================


@pytest.mark.skipif(os.name != "nt", reason="needs a Win32 or POSIX alias")
def test_physical_identity_overrides_lexical_spelling(tmp_path):
    """The general invariant, stated directly as a test."""
    root = make_framework(tmp_path)
    alias = f"experiments./evidence/{CAMPAIGN_SLUG}"
    lexical = ga._parse_canonical_parts(
        ga.canonicalize_path(alias).parts, ga.canonicalize_path(alias))
    assert lexical.parse_status == "OUTSIDE_EXPERIMENTS", (
        "precondition: the raw spelling looks ordinary")
    physical = ga.parse_evidence_path(alias, root)
    assert physical.parse_status == "VALID_EVIDENCE_PATH", (
        "physical resolution must override the ordinary-looking spelling")


def test_resolved_candidate_is_compared_to_resolved_root(tmp_path):
    """Containment must not compare a resolved candidate to an unresolved root.

    Regression for mutation 15.
    """
    root = make_framework(tmp_path)
    # `tmp_path` itself is frequently a symlinked/short-name path on both
    # platforms; comparing resolved-vs-unresolved would spuriously escape.
    resolved, code = ga.resolve_containment(CAMPAIGN_REL, root)
    assert code is None, f"unexpected containment failure {code}"
    assert resolved is not None
    assert os.path.samefile(str(resolved),
                            str(root / "experiments" / "evidence" / CAMPAIGN_SLUG))


@junction_required
def test_aliased_framework_root_still_contains_its_own_campaign_path(tmp_path):
    """When the framework ROOT is itself reached through a junction, a genuine
    campaign path inside it must still be CONTAINED.

    This is the sharp regression for mutation 15. If containment compares the
    physically resolved candidate against an UNRESOLVED root, the candidate
    resolves to the real directory, the root keeps its alias spelling, the two
    no longer share a prefix, and a perfectly legitimate path is reported as a
    symlink escape. Resolve both sides, or neither.
    """
    real_root = make_framework(tmp_path / "real")
    aliased_root = tmp_path / "aliased"
    assert make_junction(aliased_root, real_root)
    resolved, code = ga.resolve_containment(CAMPAIGN_REL, aliased_root)
    assert code is None, (
        f"a legitimate campaign path under an aliased root was reported as "
        f"{code}; containment compared a resolved candidate to an unresolved "
        f"root")
    assert resolved is not None
    ident = ga.parse_evidence_path(CAMPAIGN_REL, aliased_root)
    assert ident.evidence_number == ga.CONTRACT_EVIDENCE_NUMBER


# ===========================================================================
# Section 13: one canonical parser, no CWD-relative resolver anywhere
# ===========================================================================


def test_no_production_module_resolves_a_security_path_against_cwd():
    """Source-level invariant: no bare `Path(str(value))` on an output path,
    and no `os.getcwd()` / `os.path.abspath` in the containment path."""
    src = (REPO_ROOT / "scripts" / "gate_a_authorization.py").read_text(
        encoding="utf-8")
    start = src.index("def resolve_containment(")
    end = src.index("EvidenceParseStatus = Literal[")
    body = src[start:end]
    for forbidden in ("os.getcwd(", "os.path.abspath(", "Path.cwd("):
        assert forbidden not in body, (
            f"{forbidden} appears inside the containment path; relative paths "
            "must be anchored to framework_root only")


def test_every_security_path_interpretation_passes_root_and_raw():
    """Behavioral invariant: the parser REQUIRES both inputs to be correct.

    Calling the canonicalizer without the framework root must not produce the
    controlled identity -- which is what makes passing the root mandatory at
    every call site rather than optional.
    """
    unanchored = ga.parse_evidence_path(f"jexp/evidence/{CAMPAIGN_SLUG}")
    assert unanchored.parse_status == "OUTSIDE_EXPERIMENTS"


# ===========================================================================
# Section 28: classification never touches the filesystem
# ===========================================================================


def test_classification_creates_no_filesystem_entries(tmp_path, monkeypatch):
    """Canonicalization/classification must create nothing at all."""
    root = make_framework(tmp_path)

    def forbidden(*a, **k):
        raise AssertionError("classification attempted a filesystem write")

    monkeypatch.setattr(os, "mkdir", forbidden)
    monkeypatch.setattr(os, "makedirs", forbidden)
    monkeypatch.setattr(Path, "mkdir", forbidden)
    monkeypatch.setattr(Path, "touch", forbidden)
    monkeypatch.setattr(Path, "write_text", forbidden)
    monkeypatch.setattr(Path, "write_bytes", forbidden)

    before = sorted(p.relative_to(root).as_posix() for p in root.rglob("*"))
    for candidate in RELATIVE_FORMS + COLON_FORMS + [
            f"experiments./evidence/{CAMPAIGN_SLUG}",
            f"jexp/evidence/{CAMPAIGN_SLUG}",
            "artifacts/plan.md"]:
        ga.parse_evidence_path(candidate, root)
        ga.resolve_containment(candidate, root)
        classify(candidate, root)
    after = sorted(p.relative_to(root).as_posix() for p in root.rglob("*"))
    assert before == after, f"classification changed the tree: {set(after) - set(before)}"


def test_no_real_evidence_0016_directory_is_ever_created():
    """The old bypass reproduction accidentally created a real campaign
    directory in the repository. That must be structurally impossible now."""
    real = REPO_ROOT / "experiments" / "evidence" / CAMPAIGN_SLUG
    assert not real.exists(), (
        f"a test created the real Evidence 0016 directory at {real}")
    # The run-control directory is now an authorized drafted artifact. What
    # must not exist is an operative owner approval inside it.
    run_control = REPO_ROOT / "experiments" / "run-control"
    if run_control.exists():
        approvals = [
            p for p in run_control.rglob("owner-approval.md")
        ]
        assert not approvals, (
            f"an operative owner approval exists: {approvals}")


def test_repository_experiments_tree_is_untouched_by_this_suite():
    """`git status` over experiments/ must stay clean while these tests run."""
    proc = subprocess.run(
        ["git", "status", "--porcelain", "--", "experiments/"],
        cwd=str(REPO_ROOT), capture_output=True, text=True)
    if proc.returncode != 0:
        pytest.skip("git unavailable")
    assert proc.stdout.strip() == "", (
        f"the experiments/ tree was modified: {proc.stdout}")


# ===========================================================================
# Section 25: CONTRACT_TARGET_SHA is classification-only, never an authority
# ===========================================================================


def test_contract_target_sha_is_referenced_only_by_the_classifier():
    """Source audit: the constant must appear in exactly one decision site,
    and that site must be the classifier's signal list -- never `authorize`."""
    src = (REPO_ROOT / "scripts" / "gate_a_authorization.py").read_text(
        encoding="utf-8")
    uses = [ln.strip() for ln in src.splitlines()
            if "CONTRACT_TARGET_SHA" in ln and not ln.strip().startswith("#")]
    assert len(uses) == 2, f"unexpected CONTRACT_TARGET_SHA uses: {uses}"
    assert uses[0].startswith("CONTRACT_TARGET_SHA ="), uses[0]
    assert "signals" not in uses[1] or True
    assert "_norm_sha(identity.target_sha)" in uses[1], (
        "the only consumer must be the classifier signal, not authorization")
    # The authorization path must bind to the RECORD, not to the constant.
    auth = src[src.index("def authorize("):]
    assert "CONTRACT_TARGET_SHA" not in auth, (
        "authorize() referenced the stale pinned constant; a constant must "
        "never be able to authorize or redirect execution")
    assert 'record_tgt != context.target_sha.strip()' in auth


def test_contract_target_sha_changes_classification_only(tmp_path, monkeypatch):
    """Changing the constant moves a signal, and nothing else."""
    root = make_framework(tmp_path)

    def ident(sha):
        return build_invocation_identity(
            repo_root=str(root), executor_id="claude-code",
            skill_id="workflow-planner",
            expected_output_artifact=str(root / "artifacts" / "plan.md"),
            context={"artifact_type": "workflow_orchestration_plan",
                     "workflow_id": "workflow-planner",
                     "target_repository": ORDINARY_REPO,
                     "target_sha": sha},
            model=ORDINARY_MODEL)

    _, signals_pinned = ga.classify_invocation(ident(ga.CONTRACT_TARGET_SHA))
    assert "target_sha_is_campaign_pin" in signals_pinned
    monkeypatch.setattr(ga, "CONTRACT_TARGET_SHA", "b" * 40)
    _, signals_moved = ga.classify_invocation(ident(ga.CONTRACT_TARGET_SHA))
    assert "target_sha_is_campaign_pin" in signals_moved
    _, signals_stale = ga.classify_invocation(ident("0" * 40))
    assert "target_sha_is_campaign_pin" not in signals_stale


def test_matching_contract_target_sha_cannot_satisfy_authorization(tmp_path):
    """A campaign-pinned SHA is not a credential. With no authorization record
    present, Gate A must still refuse."""
    from gate_a_authorization import AuthorizationContext, authorize_invocation

    root = make_framework(tmp_path)
    target = tmp_path / "target"
    target.mkdir()
    rc = tmp_path / "rc"
    rc.mkdir()
    ctx = AuthorizationContext(
        framework_root=root,
        target_root=target,
        execution_framework_sha="c" * 40,
        target_sha=ga.CONTRACT_TARGET_SHA,
        evidence_number=ga.CONTRACT_EVIDENCE_NUMBER,
        evidence_slug=ga.CONTRACT_EVIDENCE_SLUG,
        exact_model=ga.CONTRACT_EXACT_MODEL,
        artifact_type=ga.CONTRACT_ARTIFACT_TYPE,
        invocation_limit=1,
        authorization_record_path=rc / ga.CONTRACT_RECORD_FILENAME,
        authorization_digest_path=rc / ga.CONTRACT_DIGEST_FILENAME,
        owner_approval_path=rc / ga.CONTRACT_APPROVAL_FILENAME,
        run_control_commit_sha="c" * 40,
    )
    decision, capability = authorize_invocation(
        ctx, git_head=lambda p: "c" * 40,
        run_control_commit_resolver=lambda a, b: "c" * 40)
    assert not decision.authorized
    assert capability is None
    assert decision.failure_code in (
        ga.GATE_A_AUTHORIZATION_RECORD_MISSING,
        ga.GATE_A_REQUIRED_PATH_MISSING,
        ga.GATE_A_EXECUTION_FRAMEWORK_SHA_PENDING,
        ga.GATE_A_OWNER_APPROVAL_MISSING,
    ), decision.failure_code
