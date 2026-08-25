"""SHA-256 helpers for Autonomous Task v2 candidate/manifest hashing."""
import hashlib
import json


def sha256_file(path: str) -> str:
    with open(path, "rb") as f:
        data = f.read()
    return hashlib.sha256(data).hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def canonical_manifest_json(records: list[dict]) -> str:
    """Canonical serialization for manifest hashing: records sorted by
    candidate_id, keys sorted, no extraneous whitespace, LF-only."""
    ordered = sorted(records, key=lambda r: r["candidate_id"])
    return json.dumps(ordered, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def sha256_manifest(records: list[dict]) -> str:
    return sha256_text(canonical_manifest_json(records))
