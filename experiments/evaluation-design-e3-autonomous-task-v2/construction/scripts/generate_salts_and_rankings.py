"""Post-manifest-freeze salt generation and deterministic ranking, per
AUTONOMOUS-TASK-V2-PROTOCOL-DRAFT.md:282-291.

rank_key(candidate_id) = sha256(manifest_hash_hex + salt_hex + candidate_id)
ascending, within each (family, complexity_level) cell.
"""
import json
import secrets
import sys
from pathlib import Path

from hash_utils import sha256_text


def generate_salt() -> str:
    return secrets.token_hex(32)


def rank_candidates(manifest_hash: str, salt: str, records: list[dict]) -> dict:
    by_cell: dict[tuple[str, str], list[dict]] = {}
    for r in records:
        by_cell.setdefault((r["family"], r["complexity_level"]), []).append(r)
    ranking = {}
    for cell, cands in by_cell.items():
        keyed = sorted(
            cands,
            key=lambda r: sha256_text(manifest_hash + salt + r["candidate_id"]),
        )
        ranking["-".join(cell)] = [c["candidate_id"] for c in keyed]
    return ranking


def main(manifest_json_path: str, out_path: str) -> None:
    manifest = json.loads(Path(manifest_json_path).read_text(encoding="utf-8"))
    salt = generate_salt()
    ranking = rank_candidates(manifest["manifest_hash"], salt, manifest["records"])
    Path(out_path).write_text(
        json.dumps(
            {"manifest_hash": manifest["manifest_hash"], "salt": salt, "ranking": ranking},
            indent=2, sort_keys=True,
        ),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
