"""Classifier mutation harness (issue #108, second independent review).

A test suite that passes proves nothing about the tests. This harness breaks
the production classifier in ten specific, security-relevant ways and asserts
that the targeted suite NOTICES each time. A mutation that SURVIVES is a hole
in the tests, not a curiosity.

It is committed deliberately so an independent reviewer can re-run it rather
than take a report on trust:

    python tests/mutation_harness.py            # all ten
    python tests/mutation_harness.py ignore_evidence_number

Each mutation edits a production file in place, runs the targeted suites, and
restores the original bytes in a `finally` block. It never leaves the tree
modified, and it never touches authorization artifacts, Evidence 0015,
Evidence 0016, or any real provider.

HISTORY. On the pre-remediation head (888759b1) mutations 3 and 5 --
"ignore evidence number" and "ignore target repository" -- both SURVIVED: the
suite stayed fully green with the signal deleted, so neither signal was
load-bearing. Mutations 9 and 10 could not even be expressed, because the
canonical parser and the shared evidence-path parser did not exist yet.
"""

from __future__ import annotations

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
]

# Re-derivation happens at TWO layers: the fail-fast check in `invoke_skill`
# and the consuming check at the provider boundary in `_invoke_skill_async`.
# A mutation that removes only one is masked by the other, so this mutation
# removes BOTH -- otherwise it would not actually test what it claims to.
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
    "        ident = parse_evidence_path(output)\n"
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
    "        ident = parse_evidence_path(output)\n"
    "        if False:"
)

#: name -> [(file, old_text, new_text), ...]
MUTATIONS = {
    # 1. The whole classifier gives up and calls everything ordinary.
    "always_ordinary": [(
        GA,
        "    if identity is None:",
        "    if True:\n        return ExecutionMode.ORDINARY_DEVELOPMENT, ()\n"
        "    if identity is None:")],
    # 2. The canonical output namespace stops being a signal.
    "ignore_output_namespace": [(
        GA,
        '    if ident.parse_status in ("VALID_EVIDENCE_PATH", "AMBIGUOUS_EVIDENCE_PATH"):',
        "    if False:")],
    # 3. SURVIVED on the old head.
    "ignore_evidence_number": [(
        GA,
        "    if _norm_evidence_number(identity.evidence_number) == CONTRACT_EVIDENCE_NUMBER:",
        "    if False:")],
    # 4.
    "ignore_evidence_slug": [(
        GA,
        "    if _norm_slug(identity.evidence_slug) == CONTRACT_EVIDENCE_SLUG.casefold():",
        "    if False:")],
    # 5. SURVIVED on the old head.
    "ignore_target_repository": [(
        GA,
        "    if _norm_repo_url(identity.target_repository) == _NORM_CONTRACT_TARGET_REPOSITORY:",
        "    if False:")],
    # 6.
    "ignore_target_sha": [(
        GA,
        "    if _norm_sha(identity.target_sha) and _norm_sha(identity.target_sha) "
        "== _norm_sha(CONTRACT_TARGET_SHA):",
        "    if False:")],
    # 7. The ambiguity floor is silently downgraded.
    "ambiguous_becomes_ordinary": [(
        GA,
        "        return ExecutionMode.AMBIGUOUS, frozen_signals",
        "        return ExecutionMode.ORDINARY_DEVELOPMENT, frozen_signals")],
    # 8. The provider boundary trusts construction-time identity.
    "skip_provider_boundary_rederivation": [
        (SE, _REDERIVE_OLD_ASYNC, _REDERIVE_NEW_ASYNC),
        (SE, _REDERIVE_OLD_SYNC, _REDERIVE_NEW_SYNC)],
    # 9. The exact pre-remediation normalizer, restored.
    "revert_norm_path_weak": [(
        GA,
        "        return canonicalize_path(value).identity_key",
        '        return str(value).replace("\\\\", "/").rstrip("/")')],
    # 10. The deleted second parser, restored.
    "restore_runtime_raw_regex": [(SE, _RUNTIME_OLD, _RUNTIME_NEW)],
}


def run(names):
    results = {}
    for name in names:
        originals = {}
        ok = True
        for path, old, new in MUTATIONS[name]:
            src = path.read_text(encoding="utf-8")
            originals.setdefault(path, src)
            if old not in src:
                print(f"[{name}] ANCHOR NOT FOUND in {path.name}")
                ok = False
                break
            path.write_text(src.replace(old, new, 1), encoding="utf-8", newline="")
        if not ok:
            for path, src in originals.items():
                path.write_text(src, encoding="utf-8", newline="")
            results[name] = ("ANCHOR_ERROR", "")
            continue
        try:
            proc = subprocess.run(
                [sys.executable, "-m", "pytest", *TESTS, "-q", "-x", "-p", "no:cacheprovider",
                 # Outside the repository: a mutation run must never dirty the
                 # working tree it is mutating.
                 "--basetemp=" + str(Path(tempfile.gettempdir())
                                     / "gate-a-mutation-tmp")],
                cwd=ROOT, capture_output=True, text=True,
            )
            out = proc.stdout.strip().splitlines()
            killer = next((ln.split(" ")[1] for ln in out
                           if ln.startswith("FAILED ")), "")
            results[name] = ("KILLED" if proc.returncode != 0 else "SURVIVED",
                             killer or (out[-1] if out else ""))
        finally:
            for path, src in originals.items():
                path.write_text(src, encoding="utf-8", newline="")
    return results


def main() -> int:
    names = sys.argv[1:] or list(MUTATIONS)
    unknown = [n for n in names if n not in MUTATIONS]
    if unknown:
        print(f"unknown mutation(s): {unknown}")
        return 2
    results = run(names)
    print("\n=== CLASSIFIER MUTATION MATRIX ===")
    for i, (name, (verdict, tail)) in enumerate(results.items(), 1):
        print(f"{i:2d}. {name:38s} {verdict:12s} {tail}")
    bad = [n for n, (v, _) in results.items() if v != "KILLED"]
    print(f"\nNOT KILLED: {bad or 'none'}")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
