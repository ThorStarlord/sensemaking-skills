# Pilot Bundle Separation Audit

Extracts, from each of the three frozen pilot task/oracle pairs, two
mutually exclusive bundles:

- `bundles/agent-visible/<pilot_id>.md` — the `## Visible task contract`
  and `## Non-goal` sections only, verbatim. For T3, this deliberately
  excludes the `## Initial-state setup` section — that section describes
  repository preparation applied by the evaluator *before* dispatch
  (adding a workflow entry, repairing two fixtures), not instructions
  given to the agent.
- `bundles/evaluator-only/<pilot_id>.md` — the entire corresponding
  `*-PILOT-ORACLE.md` file, verbatim.

Header metadata (`pilot_id`, `family`, `disposable`, `repository state`)
was stripped from the agent-visible extract as internal bookkeeping, not
part of the task contract shown to a dispatched agent.

## Extraction method

Mechanical section extraction (`## <heading>` boundaries), not manual
copy-paste, to eliminate transcription risk:

```python
import re
def extract_sections(text, section_names):
    out = []
    for name in section_names:
        pattern = re.compile(rf"^## {re.escape(name)}\n(.*?)(?=^## |\Z)", re.DOTALL | re.MULTILINE)
        m = pattern.search(text)
        assert m, f"section '## {name}' not found"
        out.append(f"## {name}\n{m.group(1).rstrip()}\n")
    return "\n".join(out) + "\n"
```

## Leakage check

Every sentence longer than 8 words in each `evaluator-only/<pilot_id>.md`
file was checked for verbatim (exact-substring) appearance in the
corresponding `agent-visible/<pilot_id>.md` file.

**Result: 0 findings.** No oracle-spec sentence over 8 words appears
verbatim in any agent-visible bundle, for any of the three pilots.

(This mirrors the "task doesn't name the answer" qualification check
already independently confirmed for all three pilots during their
original construction in Tasks 1-3 — this audit re-derives it
mechanically against the actual extracted bundle files, rather than
relying on that earlier manual read.)

## Bundle file hashes

Computed via `scripts/hash_utils.py:sha256_file`.

| pilot_id | agent-visible sha256 | evaluator-only sha256 |
|---|---|---|
| T1 | `33861682d93c8da480f5bfa3868a000933c77479039eb6284aad636b601b25fb` | `f468c3f77dc902e728f9d677e1bb5bd639e9fca7ecef5326a9b9ead1bf8edbae` |
| T2 | `021fcd90156be5c0e87ead018a22d2353620c123765c728c89a8f9018546f525` | `1376f5a1b4701d8acce987639d12e4339f35b1d14da91d2a34190460e45ff55c` |
| T3 | `0dce1a825a4e7461c45177f9237892954ce799778a2c032c48a2c3bea90f0f86` | `66e4498c51f8f9cc2586f6850c7504e70f2e5014f529882e5cb7b1007d2f75c9` |

These `agent-visible` sha256 values are the ones referenced as
`--task-bundle-sha256` at Task 22's preflight run.

### Re-freeze (a7b957d) — evaluator-only hashes regenerated

The agent-visible hashes above are **byte-identical** to the old-freeze
freeze (the visible task contract / non-goal sections carried no SHA
reference and did not change under re-freeze). The `evaluator-only` hashes
were **regenerated** at the new freeze because the source `*-PILOT-ORACLE.md`
files gained a re-freeze provenance note (and T2's `git diff` base moved
`0ffb564b` → `a7b957d`). They now equal the corresponding oracle hashes in
`../PILOT-TASK-MANIFEST.md`. Old-freeze evaluator-only values
(`e4087cb8…`, `6e1ef949…`, `6e434388…`) are historical; see
`../RE-FREEZE-PROVENANCE.md`.
