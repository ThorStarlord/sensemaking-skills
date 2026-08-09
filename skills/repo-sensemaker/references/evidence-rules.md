# Evidence Rules for Repo Sensemaking

To maintain diagnostic rigor, all claims in a **Repository Sensemaking Brief** must be backed by evidence:

1. **File Citation**: Mention the specific file and line numbers (if possible) where a signal or weakness is found.
2. **Structural Proof**: Cite the directory tree or file organization as proof of shape or missing pieces.
3. **Contrastive Evidence**: Compare what the README says vs. what the `ls` or `view_file` output shows.
4. **Logic Trace**: Follow the execution path of a workflow or skill to identify where boundaries are unenforced.
5. **No Vibe-based Diagnosis**: Avoid saying something "feels" off. State exactly which boundary is unproven or ambiguous.

## Citation Format: Two Output Modes

Rule 1 (File Citation) supports **two output modes**, optimized for different consumers of the brief.

### Mode 1: Investigative

**When to use:** Default mode when a human is reading the brief directly to decide what to do next.

**What to cite:**
- Specific file paths **with line numbers** (e.g., `src/auth/login.ts:42-58`)
- Exact code snippets showing the problem
- Direct quotes from documentation

**Why:** Investigators need exact locations to quickly verify the problem in their IDE.

### Mode 2: Durable

**When to use:** When the brief will be consumed by downstream skills that validate, transform, or act on the evidence (e.g. `to-prd`, `to-issues`, `workflow-planner`, `sensemaking-docs-reconciler`).

**What to cite:**
- File paths **only, no line numbers** (e.g., `src/auth/login.ts`)
- Behavioral descriptions, not code locations
- All claims must be **grep-verifiable** against the current tree

**Why:** Downstream tools can't maintain line numbers as the codebase evolves. They need claims verifiable by grep, not by sight.

### Choosing your mode

Signal the mode in Section 7 of the [Repository Sensemaking Brief](repo-analysis-template.md):

```markdown
## 7. Evidence

<!-- mode: investigative | durable -->
```

If unsure, default to **investigative** — a downstream skill can transform investigative-mode evidence into durable form, but the reverse (durable -> investigative) is not possible without re-running the analysis, since line numbers are already gone.

### Testing your evidence

- **Investigative mode** is self-evident: open the file at the line number and verify the problem exists.
- **Durable mode** must pass a grep test: take the file path, grep for key terms from the behavioral description, and confirm the results show the problem described. If grep returns nothing, or shows the problem is already fixed, the evidence is stale.

## Related

- [Repository Sensemaking Brief Template](repo-analysis-template.md) — Section 7 (Evidence)
- [Artifact Contracts: repository_sensemaking_brief](../../workflow-planner/references/artifact-contracts.yaml) — Consumer requirements
