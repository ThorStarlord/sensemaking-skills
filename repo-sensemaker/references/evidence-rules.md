# Evidence Rules for Repository Sensemaking

## Overview

Evidence citations in repository sensemaking briefs support **two output modes** optimized for different consumers:

1. **Investigative Mode** — For human consumption, immediate decision-making
2. **Durable Mode** — For downstream artifact consumption, long-term stability

This document defines both modes and when to use each.

## Mode 1: Investigative Mode

**When to use:** Default mode when a human is reading the brief directly to decide what to do next.

**What to cite:**
- Specific file paths **with line numbers** (e.g., `src/auth/login.ts:42-58`)
- Exact code snippets showing the problem
- Direct quotes from documentation
- Links to specific implementation details

**Example:**

```markdown
## Missing Pieces: Error Recovery

The error recovery path is incomplete. In `src/api/handlers.ts:156-170`, 
the `handleError` function catches exceptions but doesn't log them:

    try {
        await processRequest(req);
    } catch (e) {
        res.status(500).send("Server error");  // No logging!
    }

This means failed requests disappear from logs entirely.
```

**Why:** Investigators need exact locations to quickly verify the problem in their IDE.

---

## Mode 2: Durable Mode

**When to use:** When the brief will be consumed by downstream skills that validate, transform, or act on the evidence.

**What to cite:**
- File paths **only, no line numbers** (e.g., `src/auth/login.ts`)
- Behavioral descriptions, not code locations
- All claims must be **grep-verifiable** against the current tree
- No exact quotes (they become stale)

**Example:**

```markdown
## Missing Pieces: Error Recovery

The error recovery path in `src/api/handlers.ts` is incomplete. 
The error handler catches exceptions but does not log them, causing 
failed requests to disappear from logs entirely. This can be verified 
by searching for the error handling implementation.
```

**Why:** Downstream tools (to-prd, to-issues) can't maintain line numbers as the codebase evolves. They need claims verifiable by grep, not by sight.

---

## Choosing Your Mode

### Signal in Repository Brief Template

The `repo-analysis-template.md` Section 7 includes a mode toggle:

```markdown
## 7. Evidence

<!-- mode: investigative | durable -->
<!-- Use durable mode when this brief will be consumed by to-prd, to-issues, or other downstream skills. -->
```

**Set the mode based on where this brief will go:**

| Consumer | Mode | Reasoning |
|----------|------|-----------|
| Human reader (Slack, email, PR) | Investigative | Needs exact locations |
| to-prd (generates PRD) | Durable | Will evolve; doesn't need line numbers |
| to-issues (generates issues) | Durable | Issues reference code, not line numbers |
| workflow-orchestrator | Durable | May re-run; prefers stable claims |
| sensemaking-docs-reconciler | Durable | Reconciles with current state; lines change |

### Default: Investigative

If you're unsure which mode to use, default to **investigative**. Downstream skills can transform investigative mode to durable mode if needed. The reverse (durable → investigative) is not possible without re-running analysis.

---

## Downstream Handling

### For Downstream Skills Consuming Investigative Mode

When consuming a brief in investigative mode:

1. Check the mode flag in the brief
2. **Strip line numbers** before citing in durable artifacts (PRDs, issues)
3. Keep the file path and behavior description
4. Run a grep check to verify the claim still holds

**Pseudo-code:**
```python
if brief.mode == "investigative":
    # Transform: `src/auth/login.ts:42-58` → `src/auth/login.ts`
    # Transform exact quotes → behavioral descriptions
    evidence_durable = brief.evidence.to_durable_form()
```

### For Downstream Skills Consuming Durable Mode

When consuming a brief in durable mode:

1. Accept claims as-is
2. Treat them as already-stable (grep-verifiable)
3. No transformation needed
4. Use them directly in PRDs, issues, agent briefs

---

## Testing Your Evidence

### Investigative Mode: Self-Evident

Investigative mode is self-evident — open the file at the line number and verify the problem exists.

### Durable Mode: Grep Test

Durable mode claims **must pass a grep test** against the current codebase:

1. Take the file path from the evidence
2. Grep for key terms from the behavioral description
3. Confirm results show the problem described

**Example:**

Evidence claim (durable mode):
> "The error handler in `src/api/handlers.ts` catches exceptions but does not log them."

Grep test:
```bash
grep -n "catch" src/api/handlers.ts
# Output: Shows catch block with no logging statement nearby
```

If grep returns nothing or shows the problem is already fixed, the evidence is stale.

---

## Appendix: Mode Migration

### From Investigative → Durable

Example transformation:

**Investigative:**
```
In `src/auth/login.ts:156-170`, the password reset flow is missing 
email verification (lines 162-165 are empty):

    async resetPassword(email) {
        const token = generateToken();
        // Email verification should be here!
        return saveToken(token);
    }
```

**Durable:**
```
The password reset flow in `src/auth/login.ts` is missing email 
verification. The reset handler generates a token but does not 
send or verify it via email before accepting the reset.
```

### From Durable → Investigative (Not Possible)

Once evidence is reduced to durable form, original line numbers are lost. To re-investigate, re-run repo-sensemaker.

---

## Related

- [Repository Sensemaking Brief Template](../repo-analysis-template.md) — Section 7 (Evidence)
- [Artifact Contracts: repository_sensemaking_brief](../../workflow-orchestrator/references/artifact-contracts.yaml) — Consumer requirements
