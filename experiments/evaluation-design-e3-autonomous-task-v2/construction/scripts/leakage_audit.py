"""Task 21 Step 3: grep every agent-visible file for oracle-spec sentences
(>8 words) that appear verbatim in the corresponding evaluator-only file."""
import re
import sys
from pathlib import Path

PILOT_DIR = Path(sys.argv[1])


def sentences(text: str) -> list[str]:
    # crude sentence split; good enough for a substring leakage check
    text = re.sub(r"\s+", " ", text)
    parts = re.split(r"(?<=[.!?])\s+", text)
    return [p.strip() for p in parts if len(p.split()) > 8]


def main():
    findings = []
    for pilot_id in ("T1", "T2", "T3"):
        agent_text = (PILOT_DIR / "bundles" / "agent-visible" / f"{pilot_id}.md").read_text(encoding="utf-8")
        oracle_text = (PILOT_DIR / "bundles" / "evaluator-only" / f"{pilot_id}.md").read_text(encoding="utf-8")
        oracle_sents = sentences(oracle_text)
        for sent in oracle_sents:
            if sent and sent in agent_text:
                findings.append((pilot_id, sent))
    if findings:
        print("LEAKAGE FOUND:")
        for pid, s in findings:
            print(f"  [{pid}] {s!r}")
        sys.exit(1)
    else:
        print("No leakage found: 0 oracle sentences (>8 words) appear verbatim in any agent-visible file.")


if __name__ == "__main__":
    main()
