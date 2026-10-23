# Session Receipt v1 (`sensemaking_session_receipt`)

**Status:** contract reference for `using-sensemaking` (proposed ADR 0032)  
**Validator:** `scripts/validate-receipt.py` (also routed by `sensemaking-skills validate --artifact <file>`)  
**Reader:** `scripts/summarize-receipts.py`

## 1. What a receipt is and is not

A session receipt is the control loop's **flight recorder**: a small, typed
YAML record of what one session set out to do, what it was allowed to do,
which responsibilities it ran, where it stopped, and what remains open. It is
written so that a later session, a headless runner or an owner reading
asynchronously can reconstruct the stop state **without the conversation**.

```text
receipt             != essay or narrative report
receipt             != reviewed knowledge (.sensemaking/knowledge/*.json)
receipt             != Campaign state (it may point to one)
receipt             != authority grant (it records authority; it never creates it)
receipt written     != receipt persisted (only a commit/push or host upload survives)
```

The receipt carries **facts and pointers**. Analysis lives in the artifacts it
points to (`repository_sensemaking_brief`, `strategic_repository_analysis`,
`owner_decision_capsule`, ...). Text fields are capped at 300 characters
(labels at 120) and the validator rejects longer values with
`RECEIPT_TEXT_TOO_LONG`. Never paste reasoning, file contents or chain-of-thought
into a receipt.

## 2. Lifecycle: open, update, finalize

| Moment | What to do | `state` | `stop.disposition` | `persistence` |
|---|---|---|---|---|
| After Section 1 (goal + authority) is established | **Open** the receipt | `in_progress` | `IN_PROGRESS` | `pending` |
| After each responsibility completes, or a finding/question appears | **Update** it in place | `in_progress` | `IN_PROGRESS` | `pending` |
| At any stop (Section 13) | **Finalize** it | `final` | terminal value | how it was persisted |

Writing early is the point: a session killed mid-run leaves an `in_progress`
receipt that the next session's reader reports as **UNFINISHED**. That is a
tombstone, not a failure of the receipt. Once `final`, a receipt is
`immutable: true`; later sessions never edit it. They record their own
receipt and point back via `continuity.resumes` and
`continuity.resolves_questions`.

One receipt per session. A session that is resumed in a fresh context writes a
**new** receipt with `continuity.resumes: <prior session_ref>`.

## 3. Location and persistence

```text
<target-repo>/.sensemaking/receipts/<session_ref>.session.yaml
session_ref = YYYY-MM-DD-<lowercase-slug>      e.g. 2026-10-23-observe-skills
```

The directory sits beside `.sensemaking/knowledge/` but is **not** ingested by
the semantic knowledge index (which reads only `intent.md`, `context.md`,
`invariants.md`, `decisions/*.md` and `knowledge/*.json`).

**A receipt survives only if it leaves the container.** A cloud or CI checkout
is as ephemeral as `/tmp`. Therefore:

- if the session may commit, commit the receipt with (or as) the session's last
  change and push it with that change; set `persistence: committed`;
- if a host uploads run outputs (CI artifact, runner store), set
  `persistence: host_uploaded`;
- if neither is allowed, set `persistence: working_tree_only` and **say in the
  final report that the receipt will be lost with the checkout**. The validator
  warns with `RECEIPT_NOT_DURABLE`.

Never push to a protected branch, open a PR, or widen authority merely to
persist a receipt. Persisting follows the session's existing Git authority.

Every `artifact_refs`, `durable_ref` and `campaign_ref` must be a plain
repository-relative path. Absolute, home, scheme-prefixed (`file:`, `C:`) and
`..` paths are rejected with `RECEIPT_NON_DURABLE_REF`, because a pointer into
a scratch directory is a pointer into nothing. Persist the artifact in the
repository first, then reference it.

## 4. Reading receipts at session start (the consumer)

Before Section 1, if `.sensemaking/receipts/` exists in the target repository:

```bash
python scripts/summarize-receipts.py --repo <target-repo>
```

(`scripts/` is the framework checkout or the installed validator runtime.)
Then:

1. **UNFINISHED** receipts: an earlier session stopped without finalizing.
   Treat its last recorded responsibility as unverified; re-check before
   continuing it.
2. **OPEN QUESTIONS**: if the current goal depends on one, resolve it before
   acting. Apply the question ratchet: repository evidence first, then the
   owner. When answered, list it in your receipt's
   `continuity.resolves_questions` as `<session_ref>#Q-<n>`.
3. **NEXT**: the latest final session's warranted responsibility is a
   *defeasible* starting point (Section 3 inherited-responsibility backstop),
   not an instruction.
4. **PENDING / REPEATED KNOWLEDGE MISSES** are inputs for
   `repository-semantic-steward` RECONCILE, not a backlog.

A receipt is evidence about a past session. It does not override current code,
current owner intent or the current Level-3 projection.

## 5. Schema (all fields required unless marked nullable)

```yaml
artifact_id: sensemaking_session_receipt
schema_version: 1
session_ref: 2026-10-23-example            # YYYY-MM-DD-<slug>; must match the file name
state: in_progress | final
created_at: "2026-10-23T06:00:00Z"         # UTC, second precision
updated_at: "2026-10-23T06:40:00Z"
target_repository: owner/repo
source_identity:
  start_ref: <40-hex commit>               # HEAD when the session began
  end_ref: <40-hex commit> | null          # required (non-null) when final
  worktree_clean_at_end: true | false | null
skill_identity:
  load_mode: harness_discovered | manual_explicit_load | unknown
  sensemaking_source_ref: <sha/version> | null
goal:
  statement: <=300 chars, the owner's goal in their terms
  source: owner_message | issue | handoff | prior_receipt | campaign | other
  source_ref: <=200 chars | null           # issue URL/number, handoff path, ...
delegation:
  granted: [read, local_write, ...]        # non-empty; values from the authority list below
  withheld: [merge, release, ...]          # may be empty; must not overlap granted
continuity:
  resumes: <session_ref> | null
  campaign_ref: <repo-relative path> | null
  resolves_questions: ["<session_ref>#Q-1"]
responsibilities:                          # in the order they ran; may be empty
  - id: R-1
    responsibility: <=120 chars            # e.g. repository_sensemaking
    capability: <=120 chars | null         # Skill id or ordinary_coding
    status: in_progress | completed | partial | skipped | blocked | not_started
    reason: <=300 chars                    # why it ran, was skipped or stopped
    artifact_refs: [<repo-relative path>]
    validation:
      - command: <=200 chars
        result: PASS | FAIL | NOT_RUN
findings:                                  # consequential claims only; may be empty
  - id: F-1
    statement: <=300 chars
    epistemic_status: OBSERVED | DERIVED | INFERRED | HYPOTHESIZED | RATIFIED | CONTRADICTED | SUPERSEDED | UNRESOLVED
    evidence_refs: [<file:lines or artifact path>]   # non-empty
    disposition: open | resolved | handed_off | no_action
open_questions:                            # may be empty
  - id: Q-1
    question: <=300 chars
    source: owner_intent | repository_evidence | empirical | external_environment
    blocking: true | false
    options:                               # >=2 required when source is owner_intent
      - option: <=120 chars
        consequence: <=300 chars           # what choosing it leads to
    durable_ref: <repo-relative path> | null   # e.g. an owner_decision_capsule
stop:
  disposition: IN_PROGRESS | GOAL_SATISFIED | NO_FURTHER_WARRANT | OWNER_DECISION_REQUIRED | AUTHORITY_BOUNDARY | EXTERNAL_BLOCKER | SAFETY_STOP | SCOPE_EXHAUSTED | INTERRUPTED
  reason: <=300 chars
next:
  warranted_responsibility: <=300 chars | null
  blocked_on: ["Q-1", "authority:merge"]   # local question ids or authority:<grant>
persistence: pending | committed | working_tree_only | host_uploaded
claim_ceiling: <=300 chars                 # what this session's evidence does NOT establish
action_authorized_by_receipt: false        # must be false
immutable: false | true                    # true exactly when state is final
```

Field notes:

- `end_ref` is the last commit **before** the receipt's own commit. A file
  cannot contain the hash of the commit that adds it, so commit the work first
  and the finalized receipt last.
- `worktree_clean_at_end` ignores the receipt files themselves.
- `delegation` records what this session was actually allowed to do.
  Authority not explicitly granted belongs in `withheld` when it matters to the
  stop (for example `merge` or `knowledge_edit`).

Authority values: `read`, `local_write`, `run_local_commands`, `commit`,
`push`, `open_pr`, `merge`, `release`, `deploy`, `tracker_write`,
`knowledge_edit`, `external_publication`.

Stop dispositions map onto Section 13 ("Continue, stop, or escalate"):
`GOAL_SATISFIED`, `NO_FURTHER_WARRANT` (further work unwarranted, or the next
action is stable and remaining uncertainty cannot change it),
`AUTHORITY_BOUNDARY`, `SCOPE_EXHAUSTED`, `SAFETY_STOP`; plus
`OWNER_DECISION_REQUIRED`, `EXTERNAL_BLOCKER`, and `INTERRUPTED` (the session
knows it is being cut off, e.g. budget or time).

## 6. Rules the validator enforces

| Code | Rule |
|---|---|
| `RECEIPT_STATE_CONFLICT` | `final` needs `immutable: true`, a terminal stop, `end_ref`, persistence other than `pending`, and no `in_progress` responsibility; `in_progress` keeps `IN_PROGRESS` and `immutable: false` |
| `RECEIPT_STOP_WITHOUT_QUESTION` | `OWNER_DECISION_REQUIRED` needs at least one **blocking** `owner_intent` question |
| `RECEIPT_OWNER_QUESTION_OPTIONS` | an `owner_intent` question lists at least two options, each with its consequence (neutral clarification: the owner chooses a consequence, not a label) |
| `RECEIPT_UNKNOWN_REF` | `next.blocked_on` entries name an existing question id or `authority:<grant>` |
| `RECEIPT_AUTHORITY_OVERLAP` | nothing is both granted and withheld |
| `RECEIPT_AUTHORITY_CLAIM` | `action_authorized_by_receipt` is `false` |
| `RECEIPT_NON_DURABLE_REF` / `RECEIPT_REF_MISSING` | references are repository-relative; with `--target-repo` they must exist |
| `RECEIPT_TEXT_TOO_LONG` | text fields stay within their caps |
| `RECEIPT_FILENAME` | the file is named `<session_ref>.session.yaml` |
| warnings | `RECEIPT_NOT_FINAL`, `RECEIPT_NOT_DURABLE`, `RECEIPT_LARGE` (over 250 lines) |

Validation proves shape and pointer integrity only. It does not establish that
the recorded decisions were right.

```bash
python scripts/validate-receipt.py .sensemaking/receipts/<session_ref>.session.yaml --target-repo .
sensemaking-skills validate --artifact .sensemaking/receipts/<session_ref>.session.yaml
```

## 7. Relationship to existing durable surfaces

| Need | Surface | Receipt's role |
|---|---|---|
| state must survive many sessions/actors | Campaign | point to it with `continuity.campaign_ref`; do not duplicate it |
| owner choice with real tradeoffs | `owner_decision_capsule` | record the question compactly and set `durable_ref` to the capsule |
| next agent needs a task prompt | `handoff` / `prompt_handoff` | list it in `artifact_refs` |
| Level-3 strategy changed | `STATUS.md`, `strategic_reconciliation` | record a finding; the strategy lives there |
| durable architectural lesson | `.sensemaking/knowledge/*.json` via the Steward | record a finding with `disposition: handed_off` |

The receipt is the always-present minimum; the others remain triggered by need.

## 8. Minimal example (a narrow task)

```yaml
artifact_id: sensemaking_session_receipt
schema_version: 1
session_ref: 2026-10-24-rename-config-field
state: final
created_at: "2026-10-24T09:00:00Z"
updated_at: "2026-10-24T09:12:00Z"
target_repository: example/app
source_identity:
  start_ref: 1111111111111111111111111111111111111111
  end_ref: 2222222222222222222222222222222222222222
  worktree_clean_at_end: true
skill_identity:
  load_mode: harness_discovered
  sensemaking_source_ref: null
goal:
  statement: Rename config field retry_max to max_retries and update its two tests.
  source: owner_message
  source_ref: null
delegation:
  granted: [read, local_write, run_local_commands, commit, push]
  withheld: [merge, release]
continuity:
  resumes: null
  campaign_ref: null
  resolves_questions: []
responsibilities:
  - id: R-1
    responsibility: ordinary implementation
    capability: ordinary_coding
    status: completed
    reason: Task was mechanically narrow and locally evidenced; repository sensemaking not warranted.
    artifact_refs: []
    validation:
      - command: pytest tests/test_config.py -q
        result: PASS
findings: []
open_questions: []
stop:
  disposition: GOAL_SATISFIED
  reason: Field renamed, tests pass, change pushed to the feature branch.
next:
  warranted_responsibility: null
  blocked_on: [authority:merge]
persistence: committed
claim_ceiling: Local tests only; hosted CI not observed.
action_authorized_by_receipt: false
immutable: true
```

A narrow task produces a narrow receipt. Ceremony does not grow with the
schema: empty lists are valid and expected.
