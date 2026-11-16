"""Old-versus-final comparison on one clean fixture (scratch only).

Usage: GITSAFETY_SCRATCH=<scratch> GITSAFETY_OLD_SRC=<exported origin/main src> python clean_fixture_ab.py
Writes results/clean_fixture_old_vs_final.json next to the harness. The fixture has no knowledge claims,
so the build digest shows that the build path is identical, not that claim content is identical.
"""
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
S = Path(os.environ["GITSAFETY_SCRATCH"])
OLD = os.environ["GITSAFETY_OLD_SRC"]
NEW = str(HERE.parents[2] / "src")
d = S / "ab-clean"
subprocess.run([sys.executable, str(HERE / "make_repo.py"), str(d), str(S / "m-ab"), "nofilter"],
               check=True, capture_output=True)
head = subprocess.run(["git", "-C", str(d), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
BOOT = ("import sys; sys.path.insert(0, sys.argv[1]); "
        "sys.argv = ['sensemaking-skills'] + sys.argv[2:]; from sensemaking_skills.cli import main; main()")


def run(src, args):
    p = subprocess.run([sys.executable, "-c", BOOT, src, *args], capture_output=True, text=True, timeout=600)
    return p.returncode, p.stdout.strip()


out = {}
for label, src in [("origin_main", OLD), ("final", NEW)]:
    db = S / f"ab-{label}.db"
    if db.exists():
        db.unlink()
    rc, txt = run(src, ["semantic", "knowledge-build", "--repo", str(d), "--repository", "gs-test",
                        "--target-ref", head, "--db", str(db), "--temporary-checkout", "--json"])
    build = json.loads(txt[txt.index("{"):])
    rc2, txt2 = run(src, ["semantic", "impact-preview", "--repo", str(d), "--target-ref", head,
                          "--subject", "notes", "--json"])
    rc3, txt3 = run(src, ["release", "audit", "--repo-root", str(d), "--json"])
    out[label] = {
        "build_exit": rc, "build_digest": build.get("digest"), "build_claims": build.get("claim_count"),
        "impact_exit": rc2, "impact_payload_sha256": hashlib.sha256(txt2.encode()).hexdigest(),
        "release_exit": rc3, "release_payload_sha256": hashlib.sha256(txt3.encode()).hexdigest(),
    }
out["identical"] = {k: out["origin_main"][k] == out["final"][k] for k in out["origin_main"]}
(HERE.parent / "results" / "clean_fixture_old_vs_final.json").write_text(
    json.dumps(out, indent=2) + "\n", encoding="utf-8", newline="\n")
print(json.dumps(out["identical"], indent=1))
