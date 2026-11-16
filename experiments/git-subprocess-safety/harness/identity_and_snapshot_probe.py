"""Campaign target snapshot: canaries fired and identity preservation, old (origin/main) versus final (scratch only).

Usage: GITSAFETY_SCRATCH=<scratch> GITSAFETY_OLD_SRC=<exported origin/main src> python identity_and_snapshot_probe.py
Writes results/identity_and_snapshot_probe.json. The identity comparison takes BOTH snapshots of the SAME
repository, because repository_id and repository_root depend on the path and head_sha depends on the commit.
"""
import dataclasses
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
S = Path(os.environ["GITSAFETY_SCRATCH"])
OLD = os.environ["GITSAFETY_OLD_SRC"]
NEW = str(HERE.parents[2] / "src")
MAKE = HERE / "make_repo.py"
M = S / "m-snap"


def snapshot(src, repo):
    code = (f"import sys,json,dataclasses; sys.path.insert(0, r'{src}'); from pathlib import Path; "
            f"from sensemaking_skills.campaigns.target_snapshot import capture_target_snapshot as c; "
            f"print(json.dumps(dataclasses.asdict(c(Path(r'{repo}'))), default=str, sort_keys=True))")
    p = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, timeout=300)
    return json.loads(p.stdout)


def fired():
    names = sorted(p.name for p in M.iterdir()) if M.exists() else []
    for p in list(M.iterdir()) if M.exists() else []:
        p.unlink()
    return names


result = {"snapshot_filtered_repo": {}, "identity_plain_repo": {}}
for label, src in [("origin_main", OLD), ("final", NEW)]:
    d = S / f"snap-{label}"
    subprocess.run([sys.executable, str(MAKE), str(d), str(M), "filter"], check=True, capture_output=True)
    hook = d / ".git" / "hooks" / "post-index-change"
    hook.write_text("#!/bin/sh\necho x >> \"" + (M / "post-index-change").as_posix() + "\"\n",
                    encoding="utf-8", newline="\n")
    fired()
    snapshot(src, d)
    result["snapshot_filtered_repo"][label] = fired()

# Identity: one plain, dirty repository; both snapshots of the same repository.
d = S / "identity-plain"
if d.exists():
    shutil.rmtree(d, onexc=lambda f, p, e: (os.chmod(p, 0o700), f(p)))
d.mkdir(parents=True)
ID = ["-c", "user.name=t", "-c", "user.email=t@invalid"]
subprocess.run(["git", "-C", str(d), "init", "-q"], check=True)
(d / "a.txt").write_bytes(b"one\n")
(d / "b.md").write_bytes(b"two\n")
subprocess.run(["git", "-C", str(d), *ID, "add", "-A"], check=True)
subprocess.run(["git", "-C", str(d), *ID, "commit", "-qm", "x"], check=True)
(d / "a.txt").write_bytes(b"changed\n")
old_s, new_s = snapshot(OLD, d), snapshot(NEW, d)
result["identity_plain_repo"] = {
    "fields_compared": sorted(old_s),
    "differing_fields": [k for k in old_s if old_s[k] != new_s[k]],
    "worktree_sha256_identical": old_s["worktree_sha256"] == new_s["worktree_sha256"],
    "dirty": [old_s["dirty"], new_s["dirty"]],
}
(HERE.parent / "results" / "identity_and_snapshot_probe.json").write_text(
    json.dumps(result, indent=2) + "\n", encoding="utf-8", newline="\n")
print(json.dumps(result, indent=1))
