"""Gate A mutation harness (issue #108).

A test suite that passes proves nothing about the tests. This harness breaks
the production classifier and the physical-containment path in fifteen
specific, security-relevant ways and asserts that TARGETED tests notice each
time. A mutation that SURVIVES is a hole in the tests, not a curiosity.

    python tests/mutation_harness.py            # all fifteen
    python tests/mutation_harness.py ignore_evidence_number

THIRD-REVIEW REDESIGN
---------------------
The previous harness counted a mutation as KILLED whenever the suite exited
non-zero. It never checked that the suite was GREEN to begin with, and it
never checked WHICH test failed. The focused baseline was in fact red (9
failures), so every "kill" was potentially vacuous: an unrelated pre-existing
failure produced the same non-zero exit as a real detection.

This harness now enforces the protocol demanded by the third review:

    1. restore pristine proposed-head source
    2. run the targeted baseline suite
    3. REQUIRE exit code 0 -- otherwise abort with BASELINE_RED and count
       nothing as killed
    4. apply exactly one mutation
    5. run the targeted suite
    6. require at least one EXPECTED test to fail
    7. record the failing tests
    8. restore pristine source
    9. re-verify restoration (bytes identical, baseline green again)

A mutation is KILLED only when the baseline was green, the mutation applied
cleanly, and at least one test named in that mutation's `expects` list failed.
A mutation that only breaks some unrelated test is reported
KILLED_BY_WRONG_TEST, which is a coverage defect, not a pass.

SAFETY. Mutations edit production files in place and restore them in a
`finally` block. Nothing here touches authorization artifacts, Evidence 0015,
Evidence 0016, run-control, or any real provider. Test temp files are written
outside the repository.

HISTORY. On the pre-remediation head (888759b1) mutations 3 and 5 SURVIVED.
Mutations 9 and 10 could not be expressed at all. Mutations 11-15 target the
CWD-anchoring defect found by the third review.
"""

from __future__ import annotations

import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GA = ROOT / "scripts" / "gate_a_authorization.py"
SE = ROOT / "scripts" / "skill_executor.py"

TESTS = [
    "tests/test_gate_a_authorization_consumer.py",
    "tests/test_gate_a_invocation_boundary.py",
    "tests/test_gate_a_trust_boundary.py",
    "tests/test_gate_a_path_canonicalization.py",
    "tests/test_gate_a_physical_containment.py",
]

BASETEMP = Path(tempfile.gettempdir()) / "gate-a-mutation-tmp"

# Re-derivation happens at TWO layers: the fail-fast check in `invoke_skill`
# and the consuming check at the provider boundary in `_invoke_skill_async`.
# A mutation that removes only one is masked by the other.
_REDERIVE_OLD_ASYNC = (
    "        actual_identity = self._actual_identity(\n"
    "            skill_id, expected_output_path, context\n"
    "        )"
)
_REDERIVE_NEW_ASYNC = "        actual_identity = self._invocation_identity  # MUTATED"

_REDERIVE_OLD_SYNC = (
    "                identity=self._actual_identity(\n"
    "                    skill_id, expected_output_artifact, context\n"
    "                ),"
)
_REDERIVE_NEW_SYNC = "                identity=self._invocation_identity,  # MUTATED"

_RUNTIME_OLD = (
    "        ident = parse_evidence_path(output, repo_root)\n"
    "        if ident.evidence_number:"
)
_RUNTIME_NEW = (
    "        import re as _re\n"
    "        _m = _re.search("
    "r'experiments[\\\\/](?:evidence|run-control)[\\\\/](\\d{4})-([A-Za-z0-9._-]+)',"
    " str(output))\n"
    "        if _m:\n"
    "            evidence_number = evidence_number or _m.group(1)\n"
    "            evidence_slug = evidence_slug or f'{_m.group(1)}-{_m.group(2)}'\n"
    "        ident = parse_evidence_path(output, repo_root)\n"
    "        if False:"
)

# -- physical-containment anchors (mutations 11-15) --------------------------

_ANCHOR_OLD = (
    "    if framework_root in (None, \"\"):\n"
    "        # A relative path with no authoritative anchor cannot be placed. That\n"
    "        # is ambiguity, never ordinariness.\n"
    "        return None, GATE_A_OUTPUT_PATH_UNANCHORABLE\n"
    "    return Path(str(framework_root)).joinpath(*canon.parts) if canon.parts \\\n"
    "        else Path(str(framework_root)), None"
)
_ANCHOR_CWD = (
    "    return Path(str(value)), None  # MUTATED: resolve against process CWD"
)

_SKIP_REL_OLD = "    canon = canonicalize_path(value)\n    # Colon-bearing components are rejected BEFORE any filesystem contact."
_SKIP_REL_NEW = (
    "    canon = canonicalize_path(value)\n"
    "    if not (canon.is_absolute or canon.drive):\n"
    "        return None, None  # MUTATED: skip physical resolution for relatives\n"
    "    # Colon-bearing components are rejected BEFORE any filesystem contact."
)

_IGNORE_REPARSE_OLD = "        resolved = resolved_ancestor.joinpath(*reversed(unresolved))"
_IGNORE_REPARSE_NEW = "        resolved = anchored  # MUTATED: ignore junction/reparse results"

_PREFER_PHYSICAL_OLD = "        if _control_rank(physical_identity) >= _control_rank(lexical_identity):"
_PREFER_PHYSICAL_NEW = "        if False:  # MUTATED: trust lexical identity on disagreement"

_ROOT_RESOLVED_OLD = "        canon_root = canonicalize_path(real_root)"
_ROOT_RESOLVED_NEW = "        canon_root = canonicalize_path(Path(str(root)))  # MUTATED: unresolved root"


#: name -> {"edits": [(file, old, new)], "expects": [test-name substrings]}
MUTATIONS = {
    # ---- classifier mutations 1-10 ----------------------------------------
    "always_ordinary": {
        "edits": [(
            GA,
            "    if identity is None:",
            "    if True:\n        return ExecutionMode.ORDINARY_DEVELOPMENT, ()\n"
            "    if identity is None:")],
        "expects": ["test_positive_exactly_one_fake_invocation",
                    "test_classification_is_cwd_independent",
                    "test_relative_trailing_dot_alias_is_gated"],
    },
    "ignore_output_namespace": {
        "edits": [(
            GA,
            '    if ident.parse_status in ("VALID_EVIDENCE_PATH", "AMBIGUOUS_EVIDENCE_PATH"):',
            "    if False:")],
        # The alias tests do NOT detect this one: an aliased campaign path still
        # yields `path_evidence_number_is_campaign`, which is strong on its own.
        # What detects it is the test that asserts the namespace signal alone is
        # sufficient to recognize a controlled Stage 1 run.
        "expects": ["test_controlled_stage1_is_recognized_without_any_declared_flag",
                    "namespace"],
    },
    "ignore_evidence_number": {
        "edits": [(
            GA,
            "    if _norm_evidence_number(identity.evidence_number) == CONTRACT_EVIDENCE_NUMBER:",
            "    if False:")],
        "expects": ["evidence_number"],
    },
    "ignore_evidence_slug": {
        "edits": [(
            GA,
            "    if _norm_slug(identity.evidence_slug) == CONTRACT_EVIDENCE_SLUG.casefold():",
            "    if False:")],
        "expects": ["evidence_slug"],
    },
    "ignore_target_repository": {
        "edits": [(
            GA,
            "    if _norm_repo_url(identity.target_repository) == _NORM_CONTRACT_TARGET_REPOSITORY:",
            "    if False:")],
        "expects": ["target_repository"],
    },
    "ignore_target_sha": {
        "edits": [(
            GA,
            "    if _norm_sha(identity.target_sha) and _norm_sha(identity.target_sha) "
            "== _norm_sha(CONTRACT_TARGET_SHA):",
            "    if False:")],
        "expects": ["target_sha"],
    },
    "ambiguous_becomes_ordinary": {
        "edits": [(
            GA,
            "        return ExecutionMode.AMBIGUOUS, frozen_signals",
            "        return ExecutionMode.ORDINARY_DEVELOPMENT, frozen_signals")],
        "expects": ["ambigu", "floor", "_is_gated", "cwd_independent"],
    },
    "skip_provider_boundary_rederivation": {
        "edits": [(SE, _REDERIVE_OLD_ASYNC, _REDERIVE_NEW_ASYNC),
                  (SE, _REDERIVE_OLD_SYNC, _REDERIVE_NEW_SYNC)],
        "expects": ["rederiv", "boundary", "identity"],
    },
    "revert_norm_path_weak": {
        "edits": [(
            GA,
            "        return canonicalize_path(value).identity_key",
            '        return str(value).replace("\\\\", "/").rstrip("/")')],
        "expects": ["canonical", "identity", "path"],
    },
    "restore_runtime_raw_regex": {
        "edits": [(SE, _RUNTIME_OLD, _RUNTIME_NEW)],
        "expects": ["parser", "regex", "identity", "canonical", "path"],
    },

    # ---- physical-resolution mutations 11-15 (third review) ---------------
    # 11. THE ACTUAL DEFECT: relative paths resolved against process CWD.
    "resolve_relative_against_cwd": {
        "edits": [(GA, _ANCHOR_OLD, _ANCHOR_CWD)],
        "expects": ["test_classification_is_cwd_independent",
                    "test_anchoring_invariant_relative_equals_joined",
                    "test_anchor_never_consults_cwd",
                    "test_relative_trailing_dot_alias_is_gated",
                    "test_relative_junction_to_experiments_is_gated"],
    },
    # 12. Physical resolution simply skipped for relative paths.
    "skip_physical_resolution_for_relative": {
        "edits": [(GA, _SKIP_REL_OLD, _SKIP_REL_NEW)],
        "expects": ["test_relative_trailing_dot_alias_is_gated",
                    "test_relative_junction_to_experiments_is_gated",
                    "test_classification_is_cwd_independent",
                    "test_resolved_candidate_is_compared_to_resolved_root"],
    },
    # 13. Junction/reparse resolution results discarded.
    "ignore_reparse_results": {
        "edits": [(GA, _IGNORE_REPARSE_OLD, _IGNORE_REPARSE_NEW)],
        "expects": ["junction", "trailing_dot", "short_name",
                    "symlink", "resolved_root"],
    },
    # 14. Lexical spelling trusted when it disagrees with physical identity.
    "trust_lexical_on_disagreement": {
        "edits": [(GA, _PREFER_PHYSICAL_OLD, _PREFER_PHYSICAL_NEW)],
        "expects": ["test_physical_identity_overrides_lexical_spelling",
                    "test_relative_trailing_dot_alias_is_gated",
                    "test_relative_junction_to_experiments_is_gated"],
    },
    # 15. Resolved candidate compared against an UNRESOLVED framework root.
    "compare_against_unresolved_root": {
        "edits": [(GA, _ROOT_RESOLVED_OLD, _ROOT_RESOLVED_NEW)],
        "expects": ["test_aliased_framework_root_still_contains_its_own_campaign_path",
                    "test_resolved_candidate_is_compared_to_resolved_root"],
    },
}

_FAILED_RE = re.compile(r"^FAILED\s+(\S+)", re.M)


def _run_suite() -> tuple[int, list[str], str]:
    proc = subprocess.run(
        [sys.executable, "-m", "pytest", *TESTS, "-q", "--tb=no",
         "-p", "no:cacheprovider", "--basetemp=" + str(BASETEMP)],
        cwd=ROOT, capture_output=True, text=True)
    failed = _FAILED_RE.findall(proc.stdout)
    tail = (proc.stdout.strip().splitlines() or [""])[-1]
    return proc.returncode, failed, tail


def _matches(failed: list[str], expects: list[str]) -> list[str]:
    hits = []
    for node in failed:
        low = node.lower()
        if any(e.lower() in low for e in expects):
            hits.append(node)
    return hits


def run(names):
    # ---- steps 1-3: pristine source, green baseline, or abort -------------
    pristine = {GA: GA.read_text(encoding="utf-8"),
                SE: SE.read_text(encoding="utf-8")}
    print("[baseline] running targeted suite on pristine source ...")
    code, failed, tail = _run_suite()
    if code != 0:
        print(f"[baseline] BASELINE_RED: {tail}")
        for node in failed:
            print(f"           {node}")
        return None, {"baseline": tail, "failed": failed}
    print(f"[baseline] GREEN: {tail}")

    results = {}
    for name in names:
        spec = MUTATIONS[name]
        originals = {}
        ok = True
        # ---- step 4: apply exactly one mutation ---------------------------
        for path, old, new in spec["edits"]:
            src = path.read_text(encoding="utf-8")
            originals.setdefault(path, src)
            if old not in src:
                print(f"[{name}] ANCHOR NOT FOUND in {path.name}")
                ok = False
                break
            path.write_text(src.replace(old, new, 1), encoding="utf-8",
                            newline="")
        if not ok:
            for path, src in originals.items():
                path.write_text(src, encoding="utf-8", newline="")
            results[name] = ("ANCHOR_ERROR", [], "")
            continue
        try:
            # ---- steps 5-7: run, require an EXPECTED failure --------------
            mcode, mfailed, mtail = _run_suite()
            if mcode == 0:
                verdict = "SURVIVED"
                hits = []
            else:
                hits = _matches(mfailed, spec["expects"])
                verdict = "KILLED" if hits else "KILLED_BY_WRONG_TEST"
            results[name] = (verdict, hits or mfailed, mtail)
        finally:
            # ---- step 8: restore ------------------------------------------
            for path, src in originals.items():
                path.write_text(src, encoding="utf-8", newline="")

    # ---- step 9: verify restoration ---------------------------------------
    restored = all(p.read_text(encoding="utf-8") == s
                   for p, s in pristine.items())
    print(f"\n[restore] source bytes identical to pristine: {restored}")
    rcode, _, rtail = _run_suite()
    print(f"[restore] baseline re-run: {'GREEN' if rcode == 0 else 'RED'} ({rtail})")
    return results, {"restored": restored, "baseline_after": rtail,
                     "baseline_after_green": rcode == 0}


def main() -> int:
    names = sys.argv[1:] or list(MUTATIONS)
    unknown = [n for n in names if n not in MUTATIONS]
    if unknown:
        print(f"unknown mutation(s): {unknown}")
        return 2
    results, meta = run(names)
    if results is None:
        print("\n=== MUTATION TESTING ABORTED: BASELINE_RED ===")
        print("No mutation may be counted as killed against a red baseline.")
        return 3
    print("\n=== GATE A MUTATION MATRIX ===")
    for i, (name, (verdict, nodes, tail)) in enumerate(results.items(), 1):
        first = nodes[0] if nodes else tail
        print(f"{i:2d}. {name:42s} {verdict:20s} {first}")
    bad = [n for n, (v, _, _) in results.items() if v != "KILLED"]
    print(f"\nNOT KILLED: {bad or 'none'}")
    if not meta.get("restored") or not meta.get("baseline_after_green"):
        print("RESTORATION FAILED -- working tree may be dirty")
        return 4
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
