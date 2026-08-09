"""
PROTOTYPE (prototype/repo-sensemaker-vnext) -- not wired into validate-repo.py,
CI, or any canonical validator.

Operationalizes S1's own finding: "README 0.2.1 vs pyproject 0.2.2 version
drift" (experiments/solution-interaction-s1-v1/owner-synthesis-v1.md,
section 6, "minor and non-decision-changing"). That was found by a human/
agent reading both files by hand. This makes the specific comparison
(pyproject.toml's declared version vs. version-like strings mentioned in
README.md) mechanically repeatable.

Deliberately narrow: this does NOT compare pyproject.toml's version against
package.json's version. Those are legitimately independent (Python package
version vs. npm tooling version) -- naively flagging every version-shaped
string mismatch across every manifest would produce a false positive on
this repo right now (pyproject 0.2.2 vs package.json 4.1.0, which were
never meant to track each other). The S1 pattern specifically compares the
SAME conceptual version (the package's own version) as declared in its
canonical source (pyproject.toml) against how it's *mentioned* elsewhere
(README prose) -- a narrower, well-evidenced claim beats a broad, noisy one.

Usage:
    python scripts/prototype_version_drift_scan.py --repo-root .
"""

import argparse
import os
import re

VERSION_RE = re.compile(r"\b(\d+\.\d+\.\d+)\b")


def extract_pyproject_version(repo_root):
    """Return the version declared in [project] version = "X.Y.Z", or None
    if pyproject.toml doesn't exist or has no such line."""
    path = os.path.join(repo_root, "pyproject.toml")
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as f:
        for line in f:
            m = re.match(r'^\s*version\s*=\s*"([^"]+)"', line)
            if m:
                return m.group(1)
    return None


def find_readme_version_mentions(repo_root):
    """Return a list of (line_number, version_string) for every
    dotted-triple version number mentioned in README.md. Does not attempt
    to judge which mention is "the" version -- multiple mentions,
    including ones that don't refer to the package's own version (e.g. a
    dependency's version), are possible; the caller decides relevance."""
    path = os.path.join(repo_root, "README.md")
    if not os.path.exists(path):
        return []
    mentions = []
    with open(path, encoding="utf-8") as f:
        for i, line in enumerate(f, start=1):
            for m in VERSION_RE.finditer(line):
                mentions.append((i, m.group(1)))
    return mentions


def detect_readme_pyproject_version_drift(repo_root):
    """Compare pyproject.toml's declared version against every version-like
    string mentioned in README.md.

    Returns a dict:
        pyproject_version: str | None
        readme_mentions: [(line_number, version_string), ...]
        drifted_mentions: [(line_number, version_string), ...] -- README
            mentions that differ from pyproject_version. Empty if
            pyproject_version is None (nothing to compare against) or if
            README has no version mentions.
    """
    pyproject_version = extract_pyproject_version(repo_root)
    mentions = find_readme_version_mentions(repo_root)

    drifted = []
    if pyproject_version is not None:
        drifted = [(ln, v) for ln, v in mentions if v != pyproject_version]

    return {
        "pyproject_version": pyproject_version,
        "readme_mentions": mentions,
        "drifted_mentions": drifted,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    args = parser.parse_args(argv)

    result = detect_readme_pyproject_version_drift(args.repo_root)
    print(f"pyproject.toml version: {result['pyproject_version']}")
    print(f"README.md version mentions: {len(result['readme_mentions'])}")
    for ln, v in result["readme_mentions"]:
        marker = " <-- DRIFT" if (ln, v) in result["drifted_mentions"] else ""
        print(f"  README.md:{ln}: {v}{marker}")

    if result["drifted_mentions"]:
        print(
            f"\n{len(result['drifted_mentions'])} README mention(s) disagree "
            f"with pyproject.toml's declared version "
            f"({result['pyproject_version']})."
        )
        return 1
    print("\nNo drift between README.md mentions and pyproject.toml.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
