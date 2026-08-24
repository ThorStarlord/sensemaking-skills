"""Task 21: extract agent-visible / evaluator-only bundles from the pilot
task+oracle files, then audit for leakage."""
import re
import sys
from pathlib import Path

PILOT_DIR = Path(sys.argv[1])
OUT_DIR = PILOT_DIR / "bundles"

AGENT_SECTIONS = ["Visible task contract", "Non-goal"]


def extract_sections(text: str, section_names: list[str]) -> str:
    """Extract named '## <name>' sections (up to the next '## ' or EOF)."""
    out = []
    for name in section_names:
        pattern = re.compile(
            rf"^## {re.escape(name)}\n(.*?)(?=^## |\Z)", re.DOTALL | re.MULTILINE
        )
        m = pattern.search(text)
        if not m:
            raise AssertionError(f"section '## {name}' not found")
        out.append(f"## {name}\n{m.group(1).rstrip()}\n")
    return "\n".join(out) + "\n"


def main():
    for pilot_id in ("T1", "T2", "T3"):
        task_text = (PILOT_DIR / f"{pilot_id}-PILOT-TASK.md").read_text(encoding="utf-8")
        oracle_text = (PILOT_DIR / f"{pilot_id}-PILOT-ORACLE.md").read_text(encoding="utf-8")

        agent_visible = extract_sections(task_text, AGENT_SECTIONS)
        (OUT_DIR / "agent-visible" / f"{pilot_id}.md").write_text(
            agent_visible, encoding="utf-8"
        )

        (OUT_DIR / "evaluator-only" / f"{pilot_id}.md").write_text(
            oracle_text, encoding="utf-8"
        )
        print(f"{pilot_id}: agent-visible {len(agent_visible)} chars, evaluator-only {len(oracle_text)} chars")


if __name__ == "__main__":
    main()
