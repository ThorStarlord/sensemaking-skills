# Domain-Technical Synchronization Document

**Date**: 2026-05-17  
**Workstream 1 & 3 Sync**: Domain Model ↔ Technical Implementation  
**Purpose**: Validate that explicit state machine is implementable with current tech stack  
**Reviewers**: Backend Engineer (Rafael Gomes), Database Architect  

---

## Executive Summary

This document validates that Workstream 1's domain model (explicit 4-state machine, invariants, n8n integration) is:
1. **Implementable** with current Next.js + Supabase + n8n stack
2. **Performant** without major refactoring
3. **Maintainable** with clear code patterns

**Key Finding**: Domain model is implementable with **minimal schema changes**. Main work is adding state enum, transition validation, and n8n integration error handling.

**Estimated Implementation Effort**: 2-3 weeks (including tests)

---

## Database Schema Changes

### Current Schema (Implicit)
```sql
financial_month_closures:
├── id: UUID (PK)
├── project_id: UUID (FK)
├── month_key: STRING (YYYY-MM)
├── is_locked: BOOLEAN          ← Single boolean for multiple concepts
├── snapshot: JSONB
├── notes: TEXT
├── closed_at: TIMESTAMP
├── reopened_count: INTEGER     ← Partial state tracking
├── created_at: TIMESTAMP
└── updated_at: TIMESTAMP
```

**Issues**:
- `is_locked` boolean can't represent 4 distinct states
- No audit trail (no transition timestamps)
- No idempotency key
- No GL posting reference
- `reopened_count` doesn't track individual reopens

### Proposed Schema (Explicit State)

```sql
-- Enhanced financial_month_closures table
CREATE TABLE financial_month_closures (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  project_id UUID NOT NULL REFERENCES projects(id),
  month_key VARCHAR(7) NOT NULL, -- YYYY-MM format
  
  -- Explicit state machine
  state VARCHAR(20) NOT NULL CHECK (state IN ('ABERTO', 'EM_REVIEW', 'PRONTO', 'POSTADO')),
  
  -- Transition tracking
  entered_review_at TIMESTAMP NULL,
  entered_review_by UUID NULL REFERENCES auth.users(id),
  approved_at TIMESTAMP NULL,
  approved_by UUID NULL REFERENCES auth.users(id),
  posted_at TIMESTAMP NULL,
  posted_by UUID NULL REFERENCES auth.users(id),
  gl_posting_id VARCHAR(50) NULL, -- Reference to external GL system
  
  -- Reopen tracking
  reopened_at TIMESTAMP NULL,
  reopened_by UUID NULL REFERENCES auth.users(id),
  reopened_count INTEGER DEFAULT 0 CHECK (reopened_count >= 0 AND reopened_count <= 5),
  reopened_reason TEXT NULL,
  
  -- Rejection handling
  rejected_at TIMESTAMP NULL,
  rejected_by UUID NULL REFERENCES auth.users(id),
  rejection_reason TEXT NULL,
  
  -- Data snapshot (for comparison after reopen)
  snapshot_at_pronto JSONB NULL, -- Snapshot when entering PRONTO
  snapshot_at_posting JSONB NULL, -- Snapshot when posted to GL
  snapshot_before_reopen JSONB NULL, -- Snapshot before reopen (for comparison)
  
  -- Idempotency
  idempotency_key VARCHAR(100) UNIQUE NULL, -- For deduplicating postings
  
  -- Audit trail
  posting_error TEXT NULL, -- Error message if posting fails
  posting_error_count INTEGER DEFAULT 0, -- Track retry attempts
  posting_error_last_at TIMESTAMP NULL,
  
  -- Standard timestamps
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
  
  -- Constraints
  UNIQUE (project_id, month_key),
  CHECK (
    -- State machine invariants
    CASE 
      WHEN state = 'ABERTO' THEN entered_review_at IS NULL AND approved_at IS NULL AND posted_at IS NULL
      WHEN state = 'EM_REVIEW' THEN entered_review_at IS NOT NULL AND approved_at IS NULL AND posted_at IS NULL
      WHEN state = 'PRONTO' THEN approved_at IS NOT NULL AND posted_at IS NULL
      WHEN state = 'POSTADO' THEN posted_at IS NOT NULL AND gl_posting_id IS NOT NULL
      ELSE FALSE
    END
  )
);

-- Index for common queries
CREATE INDEX idx_financial_closures_project_month ON financial_month_closures(project_id, month_key);
CREATE INDEX idx_financial_closures_state ON financial_month_closures(project_id, state);
CREATE INDEX idx_financial_closures_reopened ON financial_month_closures(project_id) WHERE reopened_count > 0;

-- New table: State transition audit log
CREATE TABLE financial_state_transitions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  closure_id UUID NOT NULL REFERENCES financial_month_closures(id),
  from_state VARCHAR(20) NOT NULL,
  to_state VARCHAR(20) NOT NULL,
  triggered_by UUID NOT NULL REFERENCES auth.users(id),
  reason TEXT NULL,
  preconditions_met BOOLEAN NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Index for audit queries
CREATE INDEX idx_state_transitions_closure ON financial_state_transitions(closure_id);

-- New table: Transaction locks (per month)
CREATE TABLE financial_month_locks (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  month_id UUID NOT NULL REFERENCES financial_month_closures(id),
  project_id UUID NOT NULL,
  -- Other fields as needed
  created_at TIMESTAMP DEFAULT NOW(),
  
  UNIQUE (month_id)
);
```

**Schema Changes Summary**:
- ✅ Replace `is_locked` boolean with `state` enum
- ✅ Add transition tracking (entered_review_at, approved_at, posted_at)
- ✅ Add GL posting reference (gl_posting_id)
- ✅ Add idempotency key (deduplication)
- ✅ Add state transition audit log table
- ✅ Add CHECK constraint enforcing state invariants
- ⚠️ Add transaction lock state (optional: could use flag on financial_transactions table instead)

**Implementation Effort**: 1-2 days (migration script, rollback plan)

---

## TypeScript/Zod Schema Updates

### Current Types
```typescript
// Current: string representation
export type MonthState = string; // Could be anything

const monthSchema = z.object({
  id: z.string().uuid(),
  monthKey: z.string().regex(/^\d{4}-\d{2}$/),
  isLocked: z.boolean(), // Ambiguous
  reopenedCount: z.number().int(),
});
```

### Proposed Types
```typescript
// Proposed: Explicit enum
export const monthStateEnum = z.enum(['ABERTO', 'EM_REVIEW', 'PRONTO', 'POSTADO']);
export type MonthState = z.infer<typeof monthStateEnum>;

// Complete month schema
export const monthClosureSchema = z.object({
  id: z.string().uuid('Invalid closure ID'),
  projectId: z.string().uuid('Invalid project ID'),
  monthKey: z.string().regex(/^\d{4}-\d{2}$/, 'Month key must be YYYY-MM'),
  
  // State machine
  state: monthStateEnum,
  enteredReviewAt: z.date().nullable().optional(),
  enteredReviewBy: z.string().uuid().nullable().optional(),
  approvedAt: z.date().nullable().optional(),
  approvedBy: z.string().uuid().nullable().optional(),
  postedAt: z.date().nullable().optional(),
  postedBy: z.string().uuid().nullable().optional(),
  glPostingId: z.string().regex(/^[A-Za-z0-9\-_]+$/, 'Invalid GL posting ID').nullable().optional(),
  
  // Reopen tracking
  reopenedAt: z.date().nullable().optional(),
  reopenedBy: z.string().uuid().nullable().optional(),
  reopenedCount: z.number().int().min(0).max(5),
  reopenedReason: z.string().max(500).nullable().optional(),
  
  // Rejection handling
  rejectedAt: z.date().nullable().optional(),
  rejectedBy: z.string().uuid().nullable().optional(),
  rejectionReason: z.string().max(500).nullable().optional(),
  
  // Idempotency
  idempotencyKey: z.string().regex(/^month-\d{4}-\d{2}-\d+$/, 'Invalid idempotency key').nullable().optional(),
  
  // Snapshots
  snapshotAtPronto: z.record(z.unknown()).nullable().optional(),
  snapshotAtPosting: z.record(z.unknown()).nullable().optional(),
  snapshotBeforeReopen: z.record(z.unknown()).nullable().optional(),
  
  // Audit
  postingError: z.string().max(1000).nullable().optional(),
  postingErrorCount: z.number().int().min(0),
  
  // Standard
  createdAt: z.date(),
  updatedAt: z.date(),
});

export type MonthClosure = z.infer<typeof monthClosureSchema>;

// State transition validation
export function canTransitionFrom(from: MonthState, to: MonthState): boolean {
  const validTransitions: Record<MonthState, MonthState[]> = {
    ABERTO: ['EM_REVIEW'],
    EM_REVIEW: ['ABERTO', 'PRONTO'],
    PRONTO: ['POSTADO'],
    POSTADO: ['ABERTO'],
  };
  return validTransitions[from]?.includes(to) ?? false;
}
```

**Implementation Effort**: 1 day (update existing schemas, add validation functions)

---

## Server Action Patterns

### Current Pattern (Implicit Guards)
```typescript
// Current: Guards scattered
async function closeMonth(formData: FormData) {
  "use server";
  
  const monthKey = String(formData.get("month_key"));
  const { data: closure, error } = await supabase
    .from("financial_month_closures")
    .select("*")
    .eq("month_key", monthKey)
    .maybeSingle();
  
  if (!closure) {
    return { error: "Month not found" };
  }
  
  if (closure.is_locked) {
    return { error: "Month already locked" };
  }
  
  // Update without explicit state validation
  await supabase.from("financial_month_closures").update({ is_locked: true });
  
  redirect("/admin/finance");
}
```

**Issues**:
- No explicit state validation
- No precondition checking (are transactions verified?)
- No transition audit log
- Error messages not specific
- No idempotency

### Proposed Pattern (Explicit State Machine)

```typescript
// Proposed: Centralized state machine validation

type TransitionResult = 
  | { ok: true; closure: MonthClosure }
  | { ok: false; error: string; code: string; context?: Record<string, unknown> };

async function transitionMonth(
  projectId: string,
  monthKey: string,
  toState: MonthState,
  userId: string,
  reason?: string
): Promise<TransitionResult> {
  "use server";
  
  const supabase = getSupabaseServerClient();
  
  // 1. Load current closure
  const { data: closure, error: loadError } = await supabase
    .from("financial_month_closures")
    .select("*")
    .eq("project_id", projectId)
    .eq("month_key", monthKey)
    .maybeSingle();
  
  if (loadError) {
    return { ok: false, error: loadError.message, code: "DB_ERROR" };
  }
  
  const currentState = closure?.state ?? 'ABERTO';
  
  // 2. Validate transition is allowed
  if (!canTransitionFrom(currentState, toState)) {
    return {
      ok: false,
      error: `Cannot transition from ${currentState} to ${toState}`,
      code: "INVALID_TRANSITION",
      context: { from: currentState, to: toState },
    };
  }
  
  // 3. Check preconditions for this transition
  const preconditionCheck = await validateTransitionPreconditions(
    projectId,
    monthKey,
    currentState,
    toState,
    userId
  );
  
  if (!preconditionCheck.ok) {
    return {
      ok: false,
      error: preconditionCheck.error,
      code: preconditionCheck.code,
      context: preconditionCheck.context,
    };
  }
  
  // 4. Execute transition
  let updateData: Partial<MonthClosure> = { state: toState, updatedAt: new Date() };
  
  // Populate transition-specific fields
  if (toState === 'EM_REVIEW') {
    updateData.enteredReviewAt = new Date();
    updateData.enteredReviewBy = userId;
  } else if (toState === 'PRONTO') {
    updateData.approvedAt = new Date();
    updateData.approvedBy = userId;
    updateData.idempotencyKey = generateIdempotencyKey(monthKey);
  } else if (toState === 'POSTADO') {
    updateData.postedAt = new Date();
    updateData.postedBy = userId;
  } else if (toState === 'ABERTO' && currentState === 'POSTADO') {
    updateData.reopenedAt = new Date();
    updateData.reopenedBy = userId;
    updateData.reopenedCount = (closure?.reopenedCount ?? 0) + 1;
    updateData.reopenedReason = reason ?? null;
  }
  
  const { data: updatedClosure, error: updateError } = await supabase
    .from("financial_month_closures")
    .update(updateData)
    .eq("id", closure?.id ?? 'new')
    .select()
    .single();
  
  if (updateError) {
    return { ok: false, error: updateError.message, code: "UPDATE_ERROR" };
  }
  
  // 5. Log state transition
  await supabase.from("financial_state_transitions").insert({
    closure_id: updatedClosure.id,
    from_state: currentState,
    to_state: toState,
    triggered_by: userId,
    reason: reason ?? null,
    preconditions_met: true,
  });
  
  // 6. Side effects (notifications, events)
  await executeTransitionSideEffects(projectId, monthKey, currentState, toState, userId);
  
  // 7. Return result
  return { ok: true, closure: updatedClosure };
}

// Precondition validators per transition
async function validateTransitionPreconditions(
  projectId: string,
  monthKey: string,
  from: MonthState,
  to: MonthState,
  userId: string
): Promise<TransitionResult> {
  const supabase = getSupabaseServerClient();
  
  // ABERTO → EM_REVIEW preconditions
  if (from === 'ABERTO' && to === 'EM_REVIEW') {
    // Check: All transactions verified
    const { data: unverified } = await supabase
      .from("financial_transactions")
      .select("id")
      .eq("project_id", projectId)
      .eq("month_key", monthKey)
      .eq("is_verified", false)
      .limit(1);
    
    if (unverified && unverified.length > 0) {
      return {
        ok: false,
        error: "Cannot send to review: some transactions are unverified",
        code: "PRECONDITION_UNVERIFIED_TRANSACTIONS",
        context: { unverifiedCount: unverified.length },
      };
    }
    
    // Check: All documents attached
    const { data: missingDocs } = await supabase
      .from("financial_transactions")
      .select("id")
      .eq("project_id", projectId)
      .eq("month_key", monthKey)
      .neq("transaction_type", "reversal")
      .is("source_file_url", null)
      .limit(1);
    
    if (missingDocs && missingDocs.length > 0) {
      return {
        ok: false,
        error: "Cannot send to review: some transactions missing documents",
        code: "PRECONDITION_MISSING_DOCUMENTS",
        context: { missingDocCount: missingDocs.length },
      };
    }
    
    // Check: Reconciliation balanced
    const balanceCheck = await validateReconciliation(projectId, monthKey);
    if (!balanceCheck.ok) {
      return {
        ok: false,
        error: `Reconciliation unbalanced: ${balanceCheck.variance}`,
        code: "PRECONDITION_RECONCILIATION_FAILED",
        context: { variance: balanceCheck.variance },
      };
    }
    
    return { ok: true, closure: null as any }; // Placeholder
  }
  
  // EM_REVIEW → PRONTO preconditions (similar structure)
  if (from === 'EM_REVIEW' && to === 'PRONTO') {
    // Re-check all EM_REVIEW preconditions still hold
    // (in case data changed)
    return { ok: true, closure: null as any };
  }
  
  // PRONTO → POSTADO preconditions
  if (from === 'PRONTO' && to === 'POSTADO') {
    // Check: Idempotency key exists
    const { data: closure } = await supabase
      .from("financial_month_closures")
      .select("idempotency_key")
      .eq("project_id", projectId)
      .eq("month_key", monthKey)
      .single();
    
    if (!closure?.idempotency_key) {
      return {
        ok: false,
        error: "Idempotency key not found (internal error)",
        code: "PRECONDITION_NO_IDEMPOTENCY_KEY",
      };
    }
    
    return { ok: true, closure: null as any };
  }
  
  // POSTADO → ABERTO preconditions
  if (from === 'POSTADO' && to === 'ABERTO') {
    const { data: closure } = await supabase
      .from("financial_month_closures")
      .select("reopened_count")
      .eq("project_id", projectId)
      .eq("month_key", monthKey)
      .single();
    
    if ((closure?.reopened_count ?? 0) >= 5) {
      // Check if user can override
      const user = await getDevSession();
      if (!user?.roles.includes("admin")) {
        return {
          ok: false,
          error: "This month has been reopened 5 times. Cannot reopen without director override.",
          code: "PRECONDITION_REOPEN_LIMIT_EXCEEDED",
        };
      }
    }
    
    return { ok: true, closure: null as any };
  }
  
  return { ok: true, closure: null as any };
}

// Execute side effects (notifications, audit, etc.)
async function executeTransitionSideEffects(
  projectId: string,
  monthKey: string,
  from: MonthState,
  to: MonthState,
  userId: string
) {
  // Send notifications
  // Update audit log
  // Invalidate caches
  // Trigger integrations (n8n, etc.)
}
```

**Benefits**:
- ✅ Centralized transition logic
- ✅ Preconditions validated before state change
- ✅ Structured error responses
- ✅ Audit log of every transition
- ✅ Side effects clearly separated
- ✅ Easy to test each precondition

**Implementation Effort**: 3-4 days (write validators, integration tests)

---

## n8n Integration (Webhook Implementation)

### Current Implementation
- **Status**: Incomplete (referenced but not fully documented)
- **Location**: Not found in codebase

### Proposed n8n Webhook Handler

```typescript
// lib/finance-n8n-webhook.ts

export type N8nWebhookPayload = {
  projectId: string;
  monthKey: string;
  monthClosureId: string;
  idempotencyKey: string; // For deduplication
  closedBy: string; // User ID
  closedAt: string; // ISO timestamp
  summary: {
    totalIncome: number;
    totalExpense: number;
    netIncome: number;
    transactionCount: number;
    categoriesByCost: Array<{ name: string; amount: number; count: number }>;
  };
};

export type N8nWebhookResponse = 
  | { ok: true; glPostingId: string; postedAt: string }
  | { ok: false; error: { code: string; message: string; retryable: boolean } };

// Main webhook caller (with retries)
export async function callN8nWebhook(
  closure: MonthClosure,
  options?: {
    maxRetries?: number;
    timeout?: number;
    webhookUrl?: string;
  }
): Promise<Result<N8nWebhookResponse>> {
  const maxRetries = options?.maxRetries ?? 3;
  const timeout = options?.timeout ?? 30000;
  const webhookUrl = options?.webhookUrl || process.env.N8N_WEBHOOK_URL;
  
  if (!webhookUrl) {
    return failure('INTERNAL_ERROR', 'N8N_WEBHOOK_URL not configured');
  }
  
  const payload = buildN8nPayload(closure);
  let lastError: unknown;
  
  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    // Exponential backoff: 0s, 1s, 3s, 10s
    if (attempt > 0) {
      const backoffMs = [1000, 3000, 10000][Math.min(attempt - 1, 2)];
      await delay(backoffMs);
    }
    
    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), timeout);
      
      const response = await fetch(webhookUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Idempotency-Key': payload.idempotencyKey,
          'X-Webhook-Version': 'v1',
        },
        body: JSON.stringify(payload),
        signal: controller.signal,
      });
      
      clearTimeout(timeoutId);
      
      // Parse response
      const data = (await response.json()) as unknown;
      const validated = validateN8nResponse(data);
      
      if (!validated.ok) {
        return failure('N8N_INVALID_RESPONSE', validated.error);
      }
      
      const responseData = validated.data;
      
      // Handle error response
      if (!responseData.ok) {
        if (responseData.error.retryable && attempt < maxRetries) {
          lastError = new Error(responseData.error.message);
          continue; // Retry
        }
        
        return failure(
          responseData.error.code,
          responseData.error.message
        );
      }
      
      // Success!
      return success(responseData as N8nWebhookResponse);
      
    } catch (err) {
      clearTimeout(timeoutId);
      
      // Handle timeout
      if (err instanceof Error && err.name === 'AbortError') {
        // TIMEOUT: Query GL system to check if posting succeeded
        const glCheckResult = await queryGlPostingStatus(closure);
        
        if (glCheckResult.ok) {
          // Month was posted (we just didn't get the response)
          return success({
            ok: true,
            glPostingId: glCheckResult.glPostingId,
            postedAt: glCheckResult.postedAt,
          });
        } else if (glCheckResult.unknown) {
          // Can't determine if posted; need manual intervention
          if (attempt < maxRetries) {
            lastError = err;
            continue; // Retry
          }
          
          return failure(
            'WEBHOOK_TIMEOUT_GL_QUERY_FAILED',
            'Posting timeout; GL query inconclusive. Manual check required.'
          );
        } else {
          // Definitely not posted; safe to retry
          lastError = err;
          if (attempt < maxRetries) continue;
          return failure('WEBHOOK_TIMEOUT', 'Webhook timed out');
        }
      }
      
      // Handle network errors
      if (isRetryableNetworkError(err)) {
        lastError = err;
        if (attempt < maxRetries) continue;
        return failure('NETWORK_ERROR', 'Network call failed after retries');
      }
      
      // Non-retryable error
      return failure('WEBHOOK_ERROR', err instanceof Error ? err.message : String(err));
    }
  }
  
  return failure('WEBHOOK_RETRIES_EXHAUSTED', 'Max retries exceeded');
}

// Query GL system to verify if month was posted
async function queryGlPostingStatus(
  closure: MonthClosure
): Promise<
  | { ok: true; glPostingId: string; postedAt: string }
  | { ok: false; unknown: false } // Definitely not posted
  | { ok: false; unknown: true }  // Can't determine
> {
  // TODO: Implement based on GL API
  // Returns: Was month posted? If yes, get GL posting ID
  
  const glApiUrl = process.env.GL_API_URL;
  if (!glApiUrl) {
    return { ok: false, unknown: true }; // Can't check
  }
  
  try {
    const response = await fetch(`${glApiUrl}/postings/${closure.monthKey}`, {
      headers: { Authorization: `Bearer ${process.env.GL_API_KEY}` },
      timeout: 10000,
    });
    
    if (response.status === 404) {
      return { ok: false, unknown: false }; // Definitely not posted
    }
    
    if (response.ok) {
      const data = await response.json();
      return {
        ok: true,
        glPostingId: data.glPostingId,
        postedAt: data.postedAt,
      };
    }
    
    return { ok: false, unknown: true }; // Server error; unknown status
  } catch {
    return { ok: false, unknown: true };
  }
}

// Build the webhook payload
function buildN8nPayload(closure: MonthClosure): N8nWebhookPayload {
  return {
    projectId: closure.projectId,
    monthKey: closure.monthKey,
    monthClosureId: closure.id,
    idempotencyKey: closure.idempotencyKey!,
    closedBy: closure.approvedBy!,
    closedAt: closure.approvedAt!.toISOString(),
    summary: {
      // Fetch from database
      totalIncome: 0, // TODO
      totalExpense: 0,
      netIncome: 0,
      transactionCount: 0,
      categoriesByCost: [],
    },
  };
}

// Validate n8n response structure
function validateN8nResponse(
  data: unknown
): { ok: true; data: N8nWebhookResponse } | { ok: false; error: string } {
  if (typeof data !== 'object' || data === null || !('ok' in data)) {
    return { ok: false, error: 'Invalid response structure' };
  }
  
  const response = data as any;
  
  if (response.ok === true) {
    if (typeof response.glPostingId !== 'string' || typeof response.postedAt !== 'string') {
      return { ok: false, error: 'Success response missing glPostingId or postedAt' };
    }
  } else if (response.ok === false) {
    if (!response.error || typeof response.error.code !== 'string') {
      return { ok: false, error: 'Error response missing error.code' };
    }
  } else {
    return { ok: false, error: 'Response.ok must be boolean' };
  }
  
  return { ok: true, data: response as N8nWebhookResponse };
}

// Integrate into state transition
export async function transitionToPOSTADO(
  projectId: string,
  monthKey: string,
  userId: string
): Promise<TransitionResult> {
  const supabase = getSupabaseServerClient();
  
  // 1. Load closure in PRONTO state
  const { data: closure } = await supabase
    .from("financial_month_closures")
    .select("*")
    .eq("project_id", projectId)
    .eq("month_key", monthKey)
    .eq("state", "PRONTO")
    .single();
  
  if (!closure) {
    return { ok: false, error: "Month not found or not in PRONTO state", code: "NOT_FOUND" };
  }
  
  // 2. Call n8n webhook
  const webhookResult = await callN8nWebhook(closure);
  
  if (!webhookResult.ok) {
    // Log the posting error
    await supabase
      .from("financial_month_closures")
      .update({
        posting_error: webhookResult.message,
        posting_error_count: (closure.posting_error_count ?? 0) + 1,
        posting_error_last_at: new Date(),
      })
      .eq("id", closure.id);
    
    // Return error to user (they can retry)
    return { ok: false, error: webhookResult.message, code: webhookResult.code };
  }
  
  const response = webhookResult.data;
  
  // 3. Update month to POSTADO
  const { data: updated, error: updateError } = await supabase
    .from("financial_month_closures")
    .update({
      state: 'POSTADO',
      posted_at: new Date(),
      posted_by: userId,
      gl_posting_id: response.glPostingId,
      posting_error: null,
      posting_error_count: 0,
    })
    .eq("id", closure.id)
    .select()
    .single();
  
  if (updateError) {
    return { ok: false, error: updateError.message, code: "UPDATE_ERROR" };
  }
  
  // 4. Send success notification
  // ... notify team ...
  
  return { ok: true, closure: updated };
}
```

**Implementation Effort**: 2-3 days (API design, retry logic, GL integration testing)

---

## Testing Strategy

### Unit Tests

```typescript
// tests/domain/month-state-machine.test.ts

describe("Month State Machine", () => {
  describe("Transitions", () => {
    test("ABERTO → EM_REVIEW allowed", () => {
      expect(canTransitionFrom("ABERTO", "EM_REVIEW")).toBe(true);
    });
    
    test("ABERTO → POSTADO not allowed", () => {
      expect(canTransitionFrom("ABERTO", "POSTADO")).toBe(false);
    });
    
    test("EM_REVIEW → ABERTO allowed (reject)", () => {
      expect(canTransitionFrom("EM_REVIEW", "ABERTO")).toBe(true);
    });
  });
  
  describe("Preconditions", () => {
    test("ABERTO → EM_REVIEW fails if unverified transactions", async () => {
      // Create month with unverified transaction
      // Call transitionMonth(...)
      // Expect error: PRECONDITION_UNVERIFIED_TRANSACTIONS
    });
    
    test("ABERTO → EM_REVIEW fails if reconciliation unbalanced", async () => {
      // Create month with balance variance > 0.01
      // Call transitionMonth(...)
      // Expect error: PRECONDITION_RECONCILIATION_FAILED
    });
  });
  
  describe("n8n Webhook", () => {
    test("Successful posting transitions to POSTADO", async () => {
      // Mock n8n response: { ok: true, glPostingId: "GL-123", ... }
      // Call transitionToPOSTADO()
      // Verify month state = POSTADO and gl_posting_id set
    });
    
    test("Timeout queries GL system", async () => {
      // Mock n8n timeout
      // Mock GL query: posting found
      // Verify month transitions to POSTADO with GL ID
    });
    
    test("Retryable errors retry automatically", async () => {
      // Mock n8n: first 503, then success
      // Call webhook with maxRetries=3
      // Verify succeeds on retry
    });
  });
});
```

**Testing Effort**: 2-3 days (comprehensive coverage of state transitions, preconditions, error scenarios)

---

## Database Migration

### Migration Script
```sql
-- 0001_state_machine_migration.sql

BEGIN;

-- 1. Add new columns
ALTER TABLE financial_month_closures 
ADD COLUMN state VARCHAR(20) DEFAULT 'ABERTO',
ADD COLUMN entered_review_at TIMESTAMP NULL,
ADD COLUMN entered_review_by UUID NULL,
ADD COLUMN approved_at TIMESTAMP NULL,
ADD COLUMN approved_by UUID NULL,
ADD COLUMN posted_at TIMESTAMP NULL,
ADD COLUMN posted_by UUID NULL,
ADD COLUMN gl_posting_id VARCHAR(50) NULL,
ADD COLUMN reopened_at TIMESTAMP NULL,
ADD COLUMN reopened_by UUID NULL,
ADD COLUMN rejected_at TIMESTAMP NULL,
ADD COLUMN rejected_by UUID NULL,
ADD COLUMN rejection_reason TEXT NULL,
ADD COLUMN idempotency_key VARCHAR(100) UNIQUE NULL,
ADD COLUMN snapshot_at_pronto JSONB NULL,
ADD COLUMN snapshot_at_posting JSONB NULL,
ADD COLUMN snapshot_before_reopen JSONB NULL,
ADD COLUMN posting_error TEXT NULL,
ADD COLUMN posting_error_count INTEGER DEFAULT 0;

-- 2. Migrate data from is_locked to state
UPDATE financial_month_closures 
SET state = CASE 
  WHEN is_locked = FALSE THEN 'PRONTO'
  WHEN is_locked = TRUE AND reopened_count > 0 THEN 'ABERTO'
  WHEN is_locked = TRUE THEN 'POSTADO'
  ELSE 'ABERTO'
END;

-- 3. Create state enum type
DO $$ BEGIN
  CREATE TYPE month_state AS ENUM ('ABERTO', 'EM_REVIEW', 'PRONTO', 'POSTADO');
EXCEPTION
  WHEN duplicate_object THEN NULL;
END $$;

-- 4. Convert state column to enum (optional, for stricter typing)
-- (Requires recreating column; careful with production!)

-- 5. Add constraints
ALTER TABLE financial_month_closures
ADD CONSTRAINT state_invariants CHECK (
  CASE 
    WHEN state = 'ABERTO' THEN entered_review_at IS NULL AND approved_at IS NULL AND posted_at IS NULL
    WHEN state = 'EM_REVIEW' THEN entered_review_at IS NOT NULL AND approved_at IS NULL
    WHEN state = 'PRONTO' THEN approved_at IS NOT NULL AND posted_at IS NULL
    WHEN state = 'POSTADO' THEN posted_at IS NOT NULL AND gl_posting_id IS NOT NULL
    ELSE FALSE
  END
);

-- 6. Create audit log table
CREATE TABLE financial_state_transitions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  closure_id UUID NOT NULL REFERENCES financial_month_closures(id),
  from_state VARCHAR(20) NOT NULL,
  to_state VARCHAR(20) NOT NULL,
  triggered_by UUID NOT NULL REFERENCES auth.users(id),
  reason TEXT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- 7. Create indexes
CREATE INDEX idx_state_transitions_closure ON financial_state_transitions(closure_id);
CREATE INDEX idx_financial_closures_state ON financial_month_closures(project_id, state);

COMMIT;
```

**Execution**: Coordinate with operations to run during low-traffic window

---

## Rollback Plan

If issues arise:

```sql
-- Rollback: financial_closures reverts to is_locked representation
-- 1. Drop new columns (keep is_locked for reference)
-- 2. Recalculate is_locked from state (reverse migration)
-- 3. Drop state column
-- 4. Drop audit table
-- 5. Restart with old code
```

---

## Performance Considerations

### Query Impact

**New indexes**:
```sql
CREATE INDEX idx_financial_closures_state ON financial_month_closures(project_id, state);
```

**Query patterns**:
- Find all months in PRONTO state: Uses idx_financial_closures_state ✅
- Find reopened months: Uses partial index (WHERE reopened_count > 0) ✅
- Find months in EM_REVIEW > 14 days: Uses idx_financial_closures_state + entered_review_at ✅

**No N+1 queries expected** (all data in single table)

### Load Impact

- Audit table appends only (no updates), minimal overhead
- n8n webhook calls are async; UI doesn't block
- Idempotency key deduplication adds one extra index lookup (negligible)

---

## Unresolved Questions for Technical Team

1. **State enum vs string**: Should we use PostgreSQL ENUM type or VARCHAR? Pros/cons?
2. **Transaction locks**: Should we track which transactions are locked, or just check month state?
3. **Snapshot strategy**: Save full transaction JSON, or just amounts by category?
4. **n8n retry logic**: Should retries happen in Next.js server action or in n8n workflow?
5. **GL API**: What's the endpoint/method for querying posting status?
6. **Idempotency**: Should key be generated client-side or server-side?

---

## Validation Conclusion

✅ **Domain model is implementable with current tech stack**

**Effort estimate**: 2-3 weeks
- Database schema: 1-2 days
- TypeScript types: 1 day
- Server actions: 3-4 days
- n8n integration: 2-3 days
- Testing: 2-3 days
- Documentation: 1 day

**Risk**: Low (incremental changes, no major refactoring)

**Benefits**:
- ✅ Explicit state machine (easier to reason about)
- ✅ Precondition validation (prevents invalid states)
- ✅ Audit trail (full transition history)
- ✅ Error recovery (retry logic for n8n)
- ✅ Idempotency (safe to retry operations)

---

**Prepared by**: Phase 3 Workstream 1  
**Validated by**: [Backend Engineer, DB Architect names - pending signature]  
**Status**: Ready for Phase 4 (Implementation Planning)
