# Error Handling Strategy - Finance Module

**Document**: Phase 3 Workstream 3 - Technical Foundation
**Date**: 2026-05-17
**Purpose**: Design consistent, typed error handling across all finance server actions

---

## 1. Current State Problems

### Problem 1: Errors Communicated Via URL Parameters
All errors today are communicated by redirecting to the same page with error in query param:
```typescript
redirect(buildRedirect({ error: "Mês inválido" }));
// Results in: /admin/finance?error=M%C3%AAs%20inv%C3%A1lido
```

**Issues**:
- Errors can be lost if user navigates away
- No client-side error boundary (errors silently consumed)
- Hard to distinguish error types in UI (validation vs. auth vs. system)
- No error code for client logging/analytics
- Error messages not localized

### Problem 2: No Typed Response Contract
Server action result is either:
- Redirect (success or error)
- Nothing (silent success)
- Thrown exception (uncaught)

**Issues**:
- Client can't tell if action succeeded without polling
- No clear contract for client implementation
- Exception handling varies by action
- Batch operations can partially fail with no clarity

### Problem 3: Inconsistent Error Messages
From audit:
```typescript
// createTransaction
redirect(buildRedirect({ error: "Tipo inválido." }));           // Punctuation

// createPayable
redirect(buildRedirect(monthKey, { error: "Descricao da conta a pagar obrigatoria." }));
// Missing punctuation, different style

// closeMonth
redirect(`/admin/finance/reports?error=${encodeURIComponent("Marque a caixa...")}`);
// Different redirect approach

// All missing context
```

### Problem 4: No Error Classification
Can't distinguish between:
- Validation errors (user input problem)
- Authorization errors (permission denied)
- Not found errors (data doesn't exist)
- Conflict errors (concurrent update)
- System errors (database down)

---

## 2. Solution: Typed Result Pattern

### 2.1 Define Result Type

```typescript
// lib/result-types.ts

/**
 * Discriminated union for server action results
 * All async functions return either success or typed error
 */

export type Result<T = void> =
  | { ok: true; data: T }
  | { ok: false; error: ErrorDetails };

export type ErrorDetails = {
  /** Error code for client handling/logging */
  code: ErrorCode;
  /** User-friendly message (should be localized) */
  message: string;
  /** Additional context for debugging */
  context?: Record<string, unknown>;
};

export enum ErrorCode {
  // Validation (4xx-like)
  VALIDATION_ERROR = "VALIDATION_ERROR",
  INVALID_DATE = "INVALID_DATE",
  INVALID_AMOUNT = "INVALID_AMOUNT",
  INVALID_MONTH = "INVALID_MONTH",
  MISSING_FIELD = "MISSING_FIELD",

  // Authorization (401/403-like)
  UNAUTHORIZED = "UNAUTHORIZED",
  FORBIDDEN = "FORBIDDEN",

  // Not Found (404-like)
  PROJECT_NOT_FOUND = "PROJECT_NOT_FOUND",
  CATEGORY_NOT_FOUND = "CATEGORY_NOT_FOUND",
  TRANSACTION_NOT_FOUND = "TRANSACTION_NOT_FOUND",
  PAYER_NOT_FOUND = "PAYER_NOT_FOUND",
  PAYABLE_NOT_FOUND = "PAYABLE_NOT_FOUND",
  MONTH_NOT_FOUND = "MONTH_NOT_FOUND",

  // Conflict (409-like)
  MONTH_LOCKED = "MONTH_LOCKED",
  TRANSACTION_ALREADY_VERIFIED = "TRANSACTION_ALREADY_VERIFIED",
  DUPLICATE_ENTRY = "DUPLICATE_ENTRY",

  // System (500-like)
  DATABASE_ERROR = "DATABASE_ERROR",
  INTERNAL_SERVER_ERROR = "INTERNAL_SERVER_ERROR",
}

/**
 * Helper to create success result
 */
export function ok<T>(data: T): Result<T> {
  return { ok: true, data };
}

/**
 * Helper to create error result
 */
export function err(
  code: ErrorCode,
  message: string,
  context?: Record<string, unknown>
): Result<never> {
  return {
    ok: false,
    error: { code, message, context },
  };
}
```

### 2.2 Apply to Server Actions

Before (current):
```typescript
async function createTransactionAction(formData: FormData) {
  "use server";

  const session = await getDevSession();
  if (!session || !session.roles.includes("admin")) {
    redirect("/login?next=/admin/finance");
  }

  const amount = parsePtBrMoneyToNumber(amountRaw);
  if (amount === null || amount <= 0) {
    redirect(buildRedirect({ error: "Valor inválido." }));
  }

  // ... 100+ more lines ...

  redirect(buildRedirect({ notice: "Lançamento salvo." }));
}
```

After (with Result type):
```typescript
async function createTransactionAction(
  formData: FormData
): Promise<Result<{ transactionId: string; monthKey: string }>> {
  "use server";

  // Auth check
  const session = await getDevSession();
  if (!session) {
    return err(ErrorCode.UNAUTHORIZED, "Sessão expirada");
  }
  if (!session.roles.includes("admin")) {
    return err(ErrorCode.FORBIDDEN, "Permissão insuficiente para criar lançamentos");
  }

  // Extract & validate using schema (from doc 02)
  const validation = extractFormData(formData, transactionInputSchema);
  if (!validation.success) {
    const issue = validation.error.issues[0];
    return err(
      ErrorCode.VALIDATION_ERROR,
      issue.message,
      { field: issue.path[0] }
    );
  }

  const { transactionType, amount, referenceDate } = validation.data;

  // Check month lock
  const isLocked = await checkMonthLocked(project.id, referenceDate.slice(0, 7));
  if (isLocked) {
    return err(
      ErrorCode.MONTH_LOCKED,
      "Mês fechado. Reabra o mês em Relatórios para lançar.",
      { monthKey: referenceDate.slice(0, 7) }
    );
  }

  // Get or create category
  let categoryId: string | null = null;
  if (validation.data.categoryName) {
    const categoryResult = await getOrCreateCategory(
      project.id,
      transactionType,
      validation.data.categoryName
    );
    if (!categoryResult.ok) return categoryResult;
    categoryId = categoryResult.data.id;
  }

  // Insert transaction
  const insertResult = await insertTransaction(project.id, {
    transactionType,
    amount,
    referenceDate,
    categoryId,
    // ... other fields
  });
  if (!insertResult.ok) return insertResult;

  // Record audit
  await recordFinanceEvent({
    projectId: project.id,
    actorUserId: session.user.id,
    eventType: "finance.transaction.create",
    entityId: insertResult.data.id,
    metadata: { amount, transactionType },
  });

  return ok({
    transactionId: insertResult.data.id,
    monthKey: referenceDate.slice(0, 7),
  });
}
```

**Benefits**:
- ✅ All errors typed and enumerated
- ✅ No redirects in business logic (cleaner code)
- ✅ Client can handle all error types
- ✅ Testable: can assert on error codes
- ✅ Error context available for debugging

---

## 3. Client-Side Error Handling

### 3.1 Form Action Pattern

With Next.js form actions, the result needs to be returned to client as JSON:

```typescript
// app/admin/finance/page.tsx

"use client";

import { useState } from "react";
import { createTransactionAction } from "./actions";

export function CreateTransactionForm() {
  const [error, setError] = useState<{ code: string; message: string } | null>(null);
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);

  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setSuccess(false);

    const formData = new FormData(e.currentTarget);
    const result = await createTransactionAction(formData);

    setLoading(false);

    if (result.ok) {
      setSuccess(true);
      // Redirect or refetch data
      window.location.href = `/admin/finance?month=${result.data.monthKey}&notice=Lançamento salvo`;
    } else {
      setError({
        code: result.error.code,
        message: result.error.message,
      });

      // Client-specific error handling
      switch (result.error.code) {
        case "VALIDATION_ERROR":
          // Highlight field with error
          break;
        case "MONTH_LOCKED":
          // Show "month locked" modal with "open month" link
          break;
        case "UNAUTHORIZED":
          // Redirect to login
          break;
        default:
          // Show generic error toast
      }
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      {error && (
        <ErrorAlert
          code={error.code}
          message={error.message}
          onDismiss={() => setError(null)}
        />
      )}
      {success && <SuccessAlert message="Lançamento salvo" />}
      {/* Form fields */}
    </form>
  );
}
```

### 3.2 Error Alert Component

```typescript
// components/ErrorAlert.tsx

import { AlertTriangle, X } from "lucide-react";
import { ErrorCode } from "@/lib/result-types";

export function ErrorAlert({
  code,
  message,
  onDismiss,
}: {
  code: string;
  message: string;
  onDismiss: () => void;
}) {
  const getIcon = () => {
    switch (code) {
      case ErrorCode.MONTH_LOCKED:
        return "🔒"; // Locked icon
      case ErrorCode.VALIDATION_ERROR:
        return "⚠️"; // Warning
      default:
        return <AlertTriangle className="w-5 h-5" />;
    }
  };

  const getAction = () => {
    if (code === ErrorCode.MONTH_LOCKED) {
      return (
        <a href="/admin/finance/reports" className="text-blue-600 underline">
          Abrir mês em Relatórios
        </a>
      );
    }
    return null;
  };

  return (
    <div className="rounded-lg border border-red-200 bg-red-50 p-4 flex items-start gap-3">
      <span className="text-xl">{getIcon()}</span>
      <div className="flex-1">
        <p className="font-medium text-red-900">{message}</p>
        {getAction() && <p className="text-sm text-red-700 mt-2">{getAction()}</p>}
      </div>
      <button onClick={onDismiss} className="text-red-700 hover:text-red-900">
        <X className="w-5 h-5" />
      </button>
    </div>
  );
}
```

---

## 4. Error Messages Dictionary

Centralize all error messages for consistency + future i18n:

```typescript
// lib/error-messages.ts

import { ErrorCode } from "./result-types";

export const errorMessages: Record<ErrorCode, string> = {
  // Validation
  [ErrorCode.VALIDATION_ERROR]: "Dados inválidos. Verifique os campos e tente novamente.",
  [ErrorCode.INVALID_DATE]: "Data inválida. Use o formato YYYY-MM-DD.",
  [ErrorCode.INVALID_AMOUNT]: "Valor inválido. Deve ser maior que zero.",
  [ErrorCode.INVALID_MONTH]: "Mês inválido. Use o formato YYYY-MM.",
  [ErrorCode.MISSING_FIELD]: "Campo obrigatório não preenchido.",

  // Authorization
  [ErrorCode.UNAUTHORIZED]: "Sessão expirada. Faça login novamente.",
  [ErrorCode.FORBIDDEN]: "Você não tem permissão para executar esta ação.",

  // Not Found
  [ErrorCode.PROJECT_NOT_FOUND]: "Projeto não encontrado.",
  [ErrorCode.CATEGORY_NOT_FOUND]: "Categoria não encontrada.",
  [ErrorCode.TRANSACTION_NOT_FOUND]: "Lançamento não encontrado.",
  [ErrorCode.PAYER_NOT_FOUND]: "Responsável financeiro não encontrado.",
  [ErrorCode.PAYABLE_NOT_FOUND]: "Conta a pagar não encontrada.",
  [ErrorCode.MONTH_NOT_FOUND]: "Mês não encontrado.",

  // Conflict
  [ErrorCode.MONTH_LOCKED]: "Mês fechado. Reabra o mês em Relatórios para alterar.",
  [ErrorCode.TRANSACTION_ALREADY_VERIFIED]: "Lançamento já foi auditado.",
  [ErrorCode.DUPLICATE_ENTRY]: "Registro duplicado.",

  // System
  [ErrorCode.DATABASE_ERROR]: "Erro ao acessar o banco de dados.",
  [ErrorCode.INTERNAL_SERVER_ERROR]: "Erro interno do servidor. Tente novamente mais tarde.",
};

/**
 * Get error message with fallback
 */
export function getErrorMessage(code: ErrorCode): string {
  return errorMessages[code] || "Erro desconhecido";
}
```

---

## 5. Batch Operation Error Handling

For actions like `bulkSetVerified` that modify multiple records:

```typescript
// Batch operation result type
export type BatchResult<T> = {
  ok: true;
  successful: T[];
  failed: Array<{
    id: string;
    error: ErrorDetails;
  }>;
} | {
  ok: false;
  error: ErrorDetails; // Total failure
};

async function bulkSetVerifiedAction(
  formData: FormData
): Promise<BatchResult<{ transactionId: string }>> {
  "use server";

  const transactionIds = formData.getAll("transactionId");
  const monthKey = formData.get("monthKey");

  // Validate month lock once
  const isLocked = await checkMonthLocked(project.id, monthKey);
  if (isLocked) {
    return {
      ok: false,
      error: {
        code: ErrorCode.MONTH_LOCKED,
        message: "Mês fechado. Reabra para alterar.",
      },
    };
  }

  const successful: Array<{ transactionId: string }> = [];
  const failed: Array<{ id: string; error: ErrorDetails }> = [];

  for (const id of transactionIds) {
    const result = await setTransactionVerified(project.id, id, true);
    if (result.ok) {
      successful.push({ transactionId: id });
    } else {
      failed.push({ id, error: result.error });
    }
  }

  return { ok: true, successful, failed };
}
```

Client receives detailed failure info:
```typescript
const result = await bulkSetVerifiedAction(formData);
if (result.ok) {
  console.log(`Updated ${result.successful.length}, failed ${result.failed.length}`);
  
  if (result.failed.length > 0) {
    showPartialSuccessAlert({
      successCount: result.successful.length,
      failedCount: result.failed.length,
      failures: result.failed,
    });
  }
}
```

---

## 6. Integration with Validation Layer (Doc 02)

Error handling works with Zod schemas:

```typescript
// In server action
const validation = extractFormData(formData, transactionInputSchema);
if (!validation.success) {
  // Zod validation error → ErrorCode.VALIDATION_ERROR
  const issue = validation.error.issues[0];
  return err(
    ErrorCode.VALIDATION_ERROR,
    issue.message,
    { field: issue.path[0], code: issue.code }
  );
}
```

---

## 7. Logging & Monitoring

With typed errors, can implement better observability:

```typescript
// lib/error-logging.ts

import { ErrorDetails, ErrorCode } from "./result-types";

export function logError(
  action: string,
  error: ErrorDetails,
  context?: Record<string, unknown>
) {
  // Separate handling by severity
  if (isServerError(error.code)) {
    // Log to Sentry/DataDog
    console.error(`[${action}] Server error`, { error, context });
  } else if (isClientError(error.code)) {
    // Track in analytics
    console.warn(`[${action}] Client error`, { code: error.code, context });
  }
}

function isServerError(code: ErrorCode): boolean {
  return code.includes("INTERNAL") || code.includes("DATABASE");
}

function isClientError(code: ErrorCode): boolean {
  return code.includes("VALIDATION") || code.includes("AUTHORIZATION");
}

// Usage in action
const result = await doSomething();
if (!result.ok) {
  logError("createTransaction", result.error, { projectId: project.id });
  return result;
}
```

---

## 8. Testing Error Handling

```typescript
// __tests__/admin/finance/page.test.ts

describe("createTransactionAction", () => {
  it("returns VALIDATION_ERROR for negative amount", async () => {
    const formData = new FormData();
    formData.set("amount", "-100");
    
    const result = await createTransactionAction(formData);
    
    expect(result.ok).toBe(false);
    expect(result.error.code).toBe(ErrorCode.VALIDATION_ERROR);
  });

  it("returns MONTH_LOCKED error when month is closed", async () => {
    mockMonthLocked("2026-05");
    
    const formData = new FormData();
    formData.set("referenceDate", "2026-05-17");
    
    const result = await createTransactionAction(formData);
    
    expect(result.ok).toBe(false);
    expect(result.error.code).toBe(ErrorCode.MONTH_LOCKED);
    expect(result.error.context?.monthKey).toBe("2026-05");
  });

  it("returns success with transactionId on valid input", async () => {
    const formData = validTransactionFormData();
    
    const result = await createTransactionAction(formData);
    
    expect(result.ok).toBe(true);
    expect(result.data.transactionId).toBeDefined();
  });
});
```

---

## 9. Migration Checklist

- [ ] Define Result type and ErrorCode enum
- [ ] Create error messages dictionary
- [ ] Create ErrorAlert UI component
- [ ] Refactor `createTransactionAction` to use Result pattern
- [ ] Add result serialization (if not using form actions)
- [ ] Update form components to handle typed errors
- [ ] Test error handling in E2E tests
- [ ] Create logging integration
- [ ] Refactor remaining 17 server actions
- [ ] Add analytics tracking for error codes

---

## 10. Expected Benefits

| Aspect | Current | After |
|--------|---------|-------|
| Error types handled | URL params | Typed enum (12+ codes) |
| Error context | None | Yes (context object) |
| Client error handling | Manual checks | Discriminated union |
| Testability | 10% (through UI) | 90% (unit test errors) |
| Debug time for bug | 20 min | 5 min (error code leads investigation) |
| Localization support | Hard (strings in UI) | Easy (centralized dictionary) |

---

## Related Documents
- `01-server-architecture-audit.md` - Audit findings
- `02-validation-schemas.md` - Validation layer design
- `04-data-access-layer.md` - Query error handling
- `TECHNICAL-ARCHITECTURE-SPEC.md` - Integration with full system
