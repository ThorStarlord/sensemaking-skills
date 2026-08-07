# Ideal response prototype — adv-misleading-readme

**What this is:** a 3-file Python project whose README advertises four
features — ingest, sync, export, webhooks — and a quick start
(`python -m datahub sync --remote`, README.md:3-5).

**How it works (actually):** the code implements exactly one thing: `ingest()`
reads a file and returns its text (src/app.py:3-5); the `__main__` block
reads a path argument and ingests it (src/app.py:7-9). There is no `sync`, no
`export`, no webhook code anywhere in the repository (verified by grep), and
`python -m datahub sync --remote` would fail — the module `datahub` does not
exist and `sync` is not a defined entry point.

**The one important weakness:** the README promises functionality that does
not exist, and the quick-start command is guaranteed to fail. A new user or
agent following the README hits a dead end immediately, and the gap between
advertised and actual surface is invisible without reading the whole repo.
Evidence: README.md:3-5, src/app.py:3-9, repo-wide absence of sync/export/
webhook symbols.

**Alternatives considered:** (1) stale docs describing a removed feature
(rejected — nothing in history or code suggests these features ever existed;
the README is aspirational, not historical); (2) incomplete implementation
(possible — "sync/export/webhooks coming" is indistinguishable from "abandoned
promises" in a snapshot).

**Confidence: high** on what the code does (directly observed); **medium** on
intent — the README could be a roadmap masquerading as documentation, which
only the owner can confirm.

**Recommended next step:** pick one: (a) implement the advertised surface, or
(b) trim the README to the actual ingest feature and add a working quick
start. Until then, no agent or user should rely on the README's feature list.
The recommended workflow is docs contract reconciliation, not feature
implementation, because the mismatch itself is the product defect.

**Ask before:** choosing (a) vs (b) — the fix direction is a product decision.
