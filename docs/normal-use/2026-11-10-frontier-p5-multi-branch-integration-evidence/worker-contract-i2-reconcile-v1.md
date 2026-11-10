# Worker contract I2 (record and documentation reconciliation), v1

Your four merges were accepted: both resolutions are exactly as specified, and
the probes showed the combined code behaving as predicted. This step applies
four reconciliations that the planner decided after reading those results. The
record texts below are the planner's; you apply them exactly, validate, commit
once and rerun the probes.

Same worktree, same rules: Git Bash, CLI from source, no `pytest`, no push.

## Why these edits exist (so you can tell if one does not fit)

- Two of the merged changes each recorded "read from Git objects" as a deferred
  alternative under different ids. The product should hold it once.
- One change rejects an automatic temporary checkout; another change's
  `workspace-query` does one by design. Both are right, for different commands,
  and the records must say so.
- The verification route for files no component owns arrived without a decision
  record, and another record names its arrival as the moment to re-inspect how
  the two compose. The probes observed the composition.
- One documentation sentence describes the citation route as it worked alone.

## Edits

### E1. One Git-objects alternative

In `.sensemaking/knowledge/architecture.json`:

1. Delete the whole claim object whose `id` is `alternative:snapshot-from-git-objects`.
2. In the relation whose `id` is `rel:workspace-query-decision-git-objects-alternative`,
   set `"object"` to `"alternative:read-committed-bytes-from-git-objects"`.
   Change nothing else in that relation.

In `.sensemaking/knowledge/stewardship.json`, in the claim
`alternative:read-committed-bytes-from-git-objects`:

3. Set `statement` to:
   `Deferred alternative: read committed bytes from Git objects instead of checking the commit out, for index building (including the first call of workspace-query) and for orient, check-rules and audit. It would remove the checkout cost, roughly 10 s of a 15 to 20 s first call on the development host, but source fingerprints are taken from checked-out bytes, which Git can convert (line endings, filters); an object reader would be a second byte path that has to agree with every index already built.`
4. Add `"file:src/sensemaking_skills/workspace_knowledge.py"` to `evidence_refs`.
5. Set `attributes` to exactly these three keys:
   - `disposition`: `deferred`
   - `scope`: `Deferred 2026-11-10 for how a commit is materialized, by the temporary-checkout change and by the workspace-query change. The two records were merged into this one during integration; the earlier workspace-query record called the fingerprint difference inferred, and lesson:separate-clone-changes-audited-bytes has since observed it`
   - `revisit_when`: `First-call latency or the checkout cost is shown to keep agents from querying or checking, and index building and the readers can move to the same reader in one change; or snapshots must be byte-identical across platforms`
6. Directly after the relation `rel:temporary-worktree-not-git-objects`, add:

```json
    {
      "id": "rel:git-objects-alternative-observed-conversion",
      "subject": "alternative:read-committed-bytes-from-git-objects",
      "predicate": "references",
      "object": "lesson:separate-clone-changes-audited-bytes",
      "evidence_refs": [
        "file:docs/semantic-architecture/persistent-knowledge-cli.md"
      ]
    },
```

### E2. Scope the automatic-fallback rejection

In `.sensemaking/knowledge/stewardship.json`, in the claim
`alternative:automatic-temporary-checkout-fallback`:

1. Set `statement` to:
   `Rejected alternative: have knowledge-build, knowledge-orient, knowledge-check-rules and knowledge-audit fall back to a temporary checkout automatically whenever the active checkout is dirty. It would change a fail-closed default that hosted tests pin, pay for a full checkout the caller did not ask for, and let a caller miss that uncommitted edits were not read.`
2. Set `attributes.scope` to:
   `Rejected 2026-11-10 for the four explicit-identity commands. workspace-query is a different contract: it resolves and materializes the commit itself and reports that in workspace_index.build_source (decision:workspace-query-derived-commit-index). Revisit if agents are observed to skip audit or rule checks because the refusal hint does not lead them to the flag`
3. Directly after the relation `rel:temporary-worktree-not-automatic-fallback`, add:

```json
    {
      "id": "rel:automatic-fallback-not-workspace-query",
      "subject": "alternative:automatic-temporary-checkout-fallback",
      "predicate": "references",
      "object": "decision:workspace-query-derived-commit-index",
      "evidence_refs": [
        "file:src/sensemaking_skills/workspace_knowledge.py"
      ],
      "attributes": {
        "scope": "workspace-query materializes a dirty checkout's commit by design; the rejection covers the explicit-identity commands only"
      }
    },
```

### E3. Record the verification route and how it composes

In `.sensemaking/knowledge/stewardship.json`:

1. Directly after the claim `alternative:authored-anchoring-only`, add:

```json
    {
      "id": "decision:verification-relevance-for-unowned-files",
      "kind": "decision",
      "statement": "For a file that no component owns, context-for returns verification relevance, never ownership: a verification claim whose authority_ref is the file, or whose evidence_refs cite it, is returned in verification_refs, and a component that a displayed record verifies through tested_by is returned under verified_components with its explicitly linked decisions, constraints and history. Ownership stays NOT_ASSESSED, contracts and rules do not follow, and owned paths do not use this route.",
      "authority_kind": "delegated",
      "authority_ref": "docs/semantic-architecture/persistent-knowledge-cli.md",
      "evidence_refs": [
        "file:docs/semantic-architecture/persistent-knowledge-cli.md",
        "file:src/sensemaking_skills/semantic_architecture/knowledge_architecture.py",
        "file:tests/test_architecture_queries.py"
      ],
      "attributes": {
        "scope": "Delegated construction choice for the owner's bounded outcome of 2026-11-09 (pull request 795). Recorded on 2026-11-10 during integration, from that pull request's decision note and the merged code; ADR 0033 stays PROPOSED and is not ratified by this record",
        "rejected_alternatives": "Ownership semantics for test files (ADR 0033 is still PROPOSED). A new tested_file relation (new vocabulary; existing verification records already name the file). Matching every citation of the file (components and decisions cite tests as evidence, which is not verification relevance; those records are listed as relevance candidates instead)",
        "revisit_when": "If the owner rules on whether path relevance stays ownership-only, or ADR 0033 is ratified, re-inspect this route together with decision:relevance-candidates-separate-from-context",
        "claim_ceiling": "Hosted tests in tests/test_architecture_queries.py cover the route; independent-agent use NOT TESTED"
      }
    },
```

   If `alternative:authored-anchoring-only` is the last claim in the array, put
   a comma after its closing brace and leave no comma after the new object.

2. In the claim `decision:relevance-candidates-separate-from-context`, set
   `attributes.revisit_when` to:
   `If the owner rules on whether path relevance stays ownership-only, or either route changes which records a category holds, re-inspect how the two compose`
   and add `attributes.composition`:
   `Integrated on 2026-11-10 with decision:verification-relevance-for-unowned-files. On a file no component owns, verification claims that name the file are returned in verification_refs and the records linked from verified components are returned in their categories, so none of them is listed as a candidate; the capability route starts from owning components only and adds nothing there. Observed on tests/test_semantic_knowledge.py: two verification records, two verified components and no candidates, where this change alone listed three citation candidates`

3. Directly after the relation `rel:store-decided-by-relevance-candidates`, add
   (mind the commas, as in step 1):

```json
    {
      "id": "rel:plane-decided-by-verification-relevance",
      "subject": "component:semantic-knowledge-plane",
      "predicate": "decided_by",
      "object": "decision:verification-relevance-for-unowned-files",
      "evidence_refs": [
        "file:src/sensemaking_skills/semantic_architecture/knowledge_architecture.py"
      ],
      "attributes": {
        "scope": "context-for verification route for files no component owns"
      }
    },
    {
      "id": "rel:relevance-candidates-compose-with-verification-relevance",
      "subject": "decision:relevance-candidates-separate-from-context",
      "predicate": "references",
      "object": "decision:verification-relevance-for-unowned-files",
      "evidence_refs": [
        "file:src/sensemaking_skills/semantic_architecture/knowledge_architecture.py"
      ],
      "attributes": {
        "scope": "On a file no component owns, records the verification route returns are excluded from candidates"
      }
    }
```

### E4. One documentation sentence

In `docs/semantic-architecture/persistent-knowledge-cli.md`, section
"Relevance candidates (not established context)", the "Citation route" bullet
ends with the sentence `This route also serves a file that no component owns,
such as a test.` Replace that sentence with these two, rewrapped to the file's
width of about 78 columns:

`This route also serves a file that no component owns, such as a test. There, verification claims that name the file are returned in `verification_refs` by the verification-relevance route, so only citing records of other kinds are listed here.`

## Stop and report, without improvising, when

- an id or sentence named above is not where this contract says it is;
- `knowledge-proposal-check` rejects a pack after your edits and the cause is
  not a typing slip of yours;
- a probe row other than the two INFO rows is not PASS.

## Checks

| Check | Command | PASS when |
| --- | --- | --- |
| C1 | `python -c` loading both packs as JSON; then `PYTHONPATH=src python -m sensemaking_skills.cli semantic knowledge-proposal-check --repo . --proposal <pack> --json` for both | both load; both report `SEMANTIC_KNOWLEDGE_PROPOSAL_VALID` |
| C2 | `grep -c "alternative:snapshot-from-git-objects" .sensemaking/knowledge/*.json` | 0 in every pack |
| C3 | `git diff --stat` | exactly three files: the two packs and `docs/semantic-architecture/persistent-knowledge-cli.md` |
| C4 | `git ls-files --eol` on the three files; non-ASCII byte count of the two packs | all `w/lf`; 0 |
| C5 | the seven validators from your first contract | each exits 0 |
| C6 | commit the three files as one commit with the message below | committed; `git status --porcelain` empty |
| C7 | rerun the probes into a new directory: `python "<scratch>/p5_probes.py" . "<scratch>/run2"` | every row PASS except the two INFO rows; copy the whole table |

Commit message for C6:

```
knowledge: reconcile records across the four integrated changes

- One Git-objects alternative instead of two: the workspace-query record is
  folded into alternative:read-committed-bytes-from-git-objects, which now
  cites the observed line-ending conversion.
- The automatic-fallback rejection is scoped to the four explicit-identity
  commands; workspace-query materializes a commit by design.
- decision:verification-relevance-for-unowned-files records the route that
  arrived without a record, and the relevance-candidates decision records
  how the two routes compose, as observed on the combined code.
- One CLI reference sentence now describes the citation route as it works
  beside the verification route.

Co-Authored-By: Claude <noreply@anthropic.com>
```

## Report format

```
MODEL: <the exact model id stated in your own system prompt>
EDITS:
<one line per edit E1 to E4: DONE or NOT DONE | anything that differed from the contract>
COMMIT: <SHA>
CHECKS:
<one line per check C1 to C6: PASS/FAIL | decisive output>
PROBE TABLE:
<the full output of C7, verbatim>
DEVIATIONS FROM CONTRACT: <none, or each with its reason>
OBSERVATIONS: <anything unexpected you saw and did not act on>
OPEN QUESTIONS: <none, or each question>
```
