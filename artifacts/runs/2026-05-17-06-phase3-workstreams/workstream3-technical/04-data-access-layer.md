# Data Access Layer Design - Finance Module

**Document**: Phase 3 Workstream 3 - Technical Foundation
**Date**: 2026-05-17
**Purpose**: Consolidate 80+ lines of duplicated Supabase queries into reusable, testable data access functions

---

## 1. Problem Statement

**Current state**: Supabase queries are embedded directly in server actions

```typescript
// In closeMonthAction
const { data: transactions, error: txError } = await supabase
  .from("financial_transactions")
  .select("*, financial_categories(*)")
  .eq("project_id", project.id)
  .gte("reference_date", range.startDate)
  .lte("reference_date", range.endDate);

// In setVerifiedAction (similar, but slightly different)
const { data: transactions } = await supabase
  .from("financial_transactions")
  .select("*")
  .eq("project_id", project.id)
  .eq("is_verified", false);

// In prepareReviewQueue (yet another variant)
const { data: unreviewed } = await supabase
  .from("financial_transactions")
  .select("id, amount, category_id")
  .eq("project_id", project.id)
  .eq("is_verified", false)
  .order("reference_date");
```

**Issues**:
- Same query written multiple times with slight variations
- Hard to debug (which version is used where?)
- Schema changes require updates in multiple files
- Can't add caching without updating everywhere
- No single place to add query optimization
- Testing requires mocking Supabase in each test file
- N+1 query problem not obvious

---

## 2. Solution: Data Access Functions

Create `lib/data-access/` directory with organized, testable query functions.

### File Structure
```
lib/data-access/
├── index.ts                # Export all functions
├── types.ts                # Query result types
├── transactions.ts         # Transaction queries
├── categories.ts           # Category queries
├── payables.ts             # Payable/AP queries
├── payers.ts               # Billing payer queries
├── contracts.ts            # Billing contract queries
├── reconciliation.ts       # Reconciliation/matching queries
├── months.ts               # Month closure queries
└── inbox.ts                # Inbox item queries
```

---

## 3. Core Types

```typescript
// lib/data-access/types.ts

/**
 * All data access functions return Result type with error handling
 */
import { Result, ErrorCode, err, ok } from "@/lib/result-types";

export type QueryResult<T> = Result<T>;

/**
 * Transaction row from database
 */
export interface TransactionRow {
  id: string;
  projectId: string;
  description: string | null;
  amount: number;
  transactionType: "income" | "expense";
  categoryId: string | null;
  paymentMethod: string | null;
  sourceFileUrl: string | null;
  isVerified: boolean;
  referenceDate: string;
  createdAt: string;
  updatedAt: string;
  financialCategories?: {
    id: string;
    name: string;
  } | null;
}

/**
 * Category row from database
 */
export interface CategoryRow {
  id: string;
  projectId: string;
  name: string;
  type: "income" | "expense";
  isFixed: boolean;
  createdAt: string;
}

/**
 * Payable row from database
 */
export interface PayableRow {
  id: string;
  projectId: string;
  description: string;
  vendorName: string | null;
  amount: number;
  dueDate: string;
  status: "open" | "settled" | "cancelled";
  categoryName: string | null;
  paymentMethodPreference: string | null;
  createdAt: string;
  updatedAt: string;
}
```

---

## 4. Transaction Queries

```typescript
// lib/data-access/transactions.ts

import { getSupabaseServerClient } from "@/lib/supabase-server";
import { Result, err, ok, ErrorCode } from "@/lib/result-types";
import { TransactionRow, QueryResult } from "./types";

const supabase = getSupabaseServerClient();

/**
 * Get all transactions for a project in a date range
 * Used in: closeMonthAction, reports, exports
 */
export async function getTransactionsByDateRange(
  projectId: string,
  startDate: string,
  endDate: string,
  options?: {
    includeCategories?: boolean;
    onlyUnverified?: boolean;
  }
): Promise<QueryResult<TransactionRow[]>> {
  try {
    let query = supabase
      .from("financial_transactions")
      .select(
        options?.includeCategories
          ? "*, financial_categories(*)"
          : "*"
      )
      .eq("project_id", projectId)
      .gte("reference_date", startDate)
      .lte("reference_date", endDate)
      .order("reference_date", { ascending: false });

    if (options?.onlyUnverified) {
      query = query.eq("is_verified", false);
    }

    const { data, error } = await query;

    if (error) {
      return err(
        ErrorCode.DATABASE_ERROR,
        "Falha ao buscar lançamentos",
        { originalError: error.message }
      );
    }

    return ok((data || []) as TransactionRow[]);
  } catch (error) {
    return err(
      ErrorCode.INTERNAL_SERVER_ERROR,
      "Erro ao processar lançamentos",
      { error: error instanceof Error ? error.message : "Unknown" }
    );
  }
}

/**
 * Get transactions by month
 * Convenience wrapper around getTransactionsByDateRange
 */
export async function getTransactionsByMonth(
  projectId: string,
  monthKey: string
): Promise<QueryResult<TransactionRow[]>> {
  const [year, month] = monthKey.split("-");
  const startDate = `${year}-${month}-01`;
  const endDate = `${year}-${month}-31`; // DB filters to actual month end

  return getTransactionsByDateRange(projectId, startDate, endDate, {
    includeCategories: true,
  });
}

/**
 * Get single transaction by ID
 */
export async function getTransaction(
  projectId: string,
  transactionId: string
): Promise<QueryResult<TransactionRow>> {
  try {
    const { data, error } = await supabase
      .from("financial_transactions")
      .select("*, financial_categories(*)")
      .eq("id", transactionId)
      .eq("project_id", projectId)
      .maybeSingle();

    if (error) {
      return err(
        ErrorCode.DATABASE_ERROR,
        "Falha ao buscar lançamento",
        { originalError: error.message }
      );
    }

    if (!data) {
      return err(
        ErrorCode.TRANSACTION_NOT_FOUND,
        "Lançamento não encontrado"
      );
    }

    return ok(data as TransactionRow);
  } catch (error) {
    return err(ErrorCode.INTERNAL_SERVER_ERROR, "Erro ao processar lançamento");
  }
}

/**
 * Get unverified transactions count
 */
export async function getUnverifiedTransactionCount(
  projectId: string
): Promise<QueryResult<number>> {
  try {
    const { data, error } = await supabase
      .from("financial_transactions")
      .select("id", { count: "exact", head: true })
      .eq("project_id", projectId)
      .eq("is_verified", false);

    if (error) {
      return err(
        ErrorCode.DATABASE_ERROR,
        "Falha ao contar lançamentos não auditados"
      );
    }

    // Supabase count is in error or returned as data length
    return ok(data ? data.length : 0);
  } catch (error) {
    return err(ErrorCode.INTERNAL_SERVER_ERROR, "Erro ao contar lançamentos");
  }
}

/**
 * Update transaction verification status
 */
export async function setTransactionVerified(
  projectId: string,
  transactionId: string,
  isVerified: boolean
): Promise<QueryResult<TransactionRow>> {
  try {
    const { data, error } = await supabase
      .from("financial_transactions")
      .update({ is_verified: isVerified })
      .eq("id", transactionId)
      .eq("project_id", projectId)
      .select()
      .maybeSingle();

    if (error) {
      return err(
        ErrorCode.DATABASE_ERROR,
        "Falha ao atualizar status de auditoria",
        { originalError: error.message }
      );
    }

    if (!data) {
      return err(
        ErrorCode.TRANSACTION_NOT_FOUND,
        "Lançamento não encontrado"
      );
    }

    return ok(data as TransactionRow);
  } catch (error) {
    return err(
      ErrorCode.INTERNAL_SERVER_ERROR,
      "Erro ao atualizar lançamento"
    );
  }
}

/**
 * Bulk update transaction verification status
 */
export async function setTransactionsVerified(
  projectId: string,
  transactionIds: string[],
  isVerified: boolean
): Promise<QueryResult<TransactionRow[]>> {
  if (transactionIds.length === 0) {
    return ok([]);
  }

  try {
    const { data, error } = await supabase
      .from("financial_transactions")
      .update({ is_verified: isVerified })
      .eq("project_id", projectId)
      .in("id", transactionIds)
      .select();

    if (error) {
      return err(
        ErrorCode.DATABASE_ERROR,
        "Falha ao atualizar lançamentos em lote"
      );
    }

    return ok((data || []) as TransactionRow[]);
  } catch (error) {
    return err(
      ErrorCode.INTERNAL_SERVER_ERROR,
      "Erro ao processar lote de lançamentos"
    );
  }
}

/**
 * Create transaction
 */
export async function createTransaction(
  projectId: string,
  data: {
    description: string | null;
    amount: number;
    transactionType: "income" | "expense";
    categoryId: string | null;
    paymentMethod: string | null;
    sourceFileUrl: string | null;
    referenceDate: string;
  }
): Promise<QueryResult<TransactionRow>> {
  try {
    const { data: inserted, error } = await supabase
      .from("financial_transactions")
      .insert({
        project_id: projectId,
        ...data,
      })
      .select()
      .maybeSingle();

    if (error) {
      return err(
        ErrorCode.DATABASE_ERROR,
        "Falha ao criar lançamento",
        { originalError: error.message }
      );
    }

    if (!inserted) {
      return err(
        ErrorCode.INTERNAL_SERVER_ERROR,
        "Lançamento não foi criado"
      );
    }

    return ok(inserted as TransactionRow);
  } catch (error) {
    return err(
      ErrorCode.INTERNAL_SERVER_ERROR,
      "Erro ao criar lançamento"
    );
  }
}
```

---

## 5. Category Queries

```typescript
// lib/data-access/categories.ts

import { getSupabaseServerClient } from "@/lib/supabase-server";
import { Result, err, ok, ErrorCode } from "@/lib/result-types";
import { CategoryRow, QueryResult } from "./types";

const supabase = getSupabaseServerClient();

/**
 * Get category by name (case-insensitive)
 */
export async function getCategoryByName(
  projectId: string,
  type: "income" | "expense",
  name: string
): Promise<QueryResult<CategoryRow>> {
  try {
    const { data, error } = await supabase
      .from("financial_categories")
      .select("*")
      .eq("project_id", projectId)
      .eq("type", type)
      .ilike("name", name)
      .maybeSingle();

    if (error) {
      return err(
        ErrorCode.DATABASE_ERROR,
        "Falha ao buscar categoria"
      );
    }

    if (!data) {
      return err(
        ErrorCode.CATEGORY_NOT_FOUND,
        `Categoria "${name}" não encontrada`
      );
    }

    return ok(data as CategoryRow);
  } catch (error) {
    return err(ErrorCode.INTERNAL_SERVER_ERROR, "Erro ao processar categoria");
  }
}

/**
 * Get or create category
 * Returns existing if found, creates if not
 */
export async function getOrCreateCategory(
  projectId: string,
  type: "income" | "expense",
  name: string
): Promise<QueryResult<CategoryRow>> {
  // Try to find existing
  const existing = await getCategoryByName(projectId, type, name);
  if (existing.ok) {
    return existing;
  }

  // Create new
  try {
    const { data, error } = await supabase
      .from("financial_categories")
      .insert({
        project_id: projectId,
        name,
        type,
        is_fixed: false,
      })
      .select()
      .maybeSingle();

    if (error) {
      return err(
        ErrorCode.DATABASE_ERROR,
        "Falha ao criar categoria",
        { originalError: error.message }
      );
    }

    if (!data) {
      return err(
        ErrorCode.INTERNAL_SERVER_ERROR,
        "Categoria não foi criada"
      );
    }

    return ok(data as CategoryRow);
  } catch (error) {
    return err(
      ErrorCode.INTERNAL_SERVER_ERROR,
      "Erro ao criar categoria"
    );
  }
}

/**
 * Get all categories for a project
 */
export async function getCategories(
  projectId: string,
  type?: "income" | "expense"
): Promise<QueryResult<CategoryRow[]>> {
  try {
    let query = supabase
      .from("financial_categories")
      .select("*")
      .eq("project_id", projectId);

    if (type) {
      query = query.eq("type", type);
    }

    const { data, error } = await query.order("name");

    if (error) {
      return err(
        ErrorCode.DATABASE_ERROR,
        "Falha ao buscar categorias"
      );
    }

    return ok((data || []) as CategoryRow[]);
  } catch (error) {
    return err(
      ErrorCode.INTERNAL_SERVER_ERROR,
      "Erro ao processar categorias"
    );
  }
}
```

---

## 6. Month Closure Queries

```typescript
// lib/data-access/months.ts

import { getSupabaseServerClient } from "@/lib/supabase-server";
import { Result, err, ok, ErrorCode } from "@/lib/result-types";
import { QueryResult } from "./types";

const supabase = getSupabaseServerClient();

/**
 * Check if a month is locked
 * Used in 6+ server actions - single source of truth
 */
export async function isMonthLocked(
  projectId: string,
  monthKey: string
): Promise<QueryResult<boolean>> {
  // Validate month format
  if (!/^\d{4}-\d{2}$/.test(monthKey)) {
    return err(
      ErrorCode.INVALID_MONTH,
      "Formato de mês inválido",
      { monthKey }
    );
  }

  try {
    const { data, error } = await supabase
      .from("financial_month_closures")
      .select("id", { count: "exact", head: true })
      .eq("project_id", projectId)
      .eq("month_key", monthKey)
      .eq("is_locked", true);

    if (error) {
      return err(
        ErrorCode.DATABASE_ERROR,
        "Falha ao verificar status do mês"
      );
    }

    return ok(data && data.length > 0);
  } catch (error) {
    return err(
      ErrorCode.INTERNAL_SERVER_ERROR,
      "Erro ao verificar mês"
    );
  }
}

/**
 * Assert month is not locked
 * Convenience function that returns error directly instead of boolean
 */
export async function assertMonthNotLocked(
  projectId: string,
  monthKey: string
): Promise<Result<void>> {
  const isLocked = await isMonthLocked(projectId, monthKey);
  if (!isLocked.ok) {
    return isLocked;
  }

  if (isLocked.data) {
    return err(
      ErrorCode.MONTH_LOCKED,
      "Mês fechado. Reabra o mês em Relatórios para alterar.",
      { monthKey }
    );
  }

  return ok(undefined);
}

/**
 * Get month closure record
 */
export async function getMonthClosure(
  projectId: string,
  monthKey: string
): Promise<QueryResult<{
  id: string;
  isLocked: boolean;
  closedAt: string | null;
  closedByUserId: string | null;
}>> {
  try {
    const { data, error } = await supabase
      .from("financial_month_closures")
      .select("id, is_locked, closed_at, closed_by_user_id")
      .eq("project_id", projectId)
      .eq("month_key", monthKey)
      .maybeSingle();

    if (error) {
      return err(
        ErrorCode.DATABASE_ERROR,
        "Falha ao buscar status do mês"
      );
    }

    if (!data) {
      return err(
        ErrorCode.MONTH_NOT_FOUND,
        "Mês não encontrado"
      );
    }

    return ok({
      id: data.id as string,
      isLocked: (data.is_locked as boolean) ?? false,
      closedAt: (data.closed_at as string) ?? null,
      closedByUserId: (data.closed_by_user_id as string) ?? null,
    });
  } catch (error) {
    return err(
      ErrorCode.INTERNAL_SERVER_ERROR,
      "Erro ao processar mês"
    );
  }
}

/**
 * Lock a month (close month)
 */
export async function lockMonth(
  projectId: string,
  monthKey: string,
  userId: string,
  notes?: string
): Promise<QueryResult<string>> {
  try {
    const { data, error } = await supabase
      .from("financial_month_closures")
      .upsert(
        {
          project_id: projectId,
          month_key: monthKey,
          is_locked: true,
          closed_at: new Date().toISOString(),
          closed_by_user_id: userId,
          notes: notes || null,
        },
        { onConflict: "project_id,month_key" }
      )
      .select("id")
      .maybeSingle();

    if (error) {
      return err(
        ErrorCode.DATABASE_ERROR,
        "Falha ao fechar mês",
        { originalError: error.message }
      );
    }

    if (!data) {
      return err(
        ErrorCode.INTERNAL_SERVER_ERROR,
        "Mês não foi fechado"
      );
    }

    return ok((data as { id: string }).id);
  } catch (error) {
    return err(
      ErrorCode.INTERNAL_SERVER_ERROR,
      "Erro ao fechar mês"
    );
  }
}

/**
 * Unlock a month (reopen month)
 */
export async function unlockMonth(
  projectId: string,
  monthKey: string,
  userId: string,
  reason?: string
): Promise<Result<void>> {
  try {
    const { error } = await supabase
      .from("financial_month_closures")
      .update({
        is_locked: false,
        closed_at: null,
        closed_by_user_id: null,
        reopen_reason: reason || null,
        reopened_by_user_id: userId,
        reopened_at: new Date().toISOString(),
      })
      .eq("project_id", projectId)
      .eq("month_key", monthKey);

    if (error) {
      return err(
        ErrorCode.DATABASE_ERROR,
        "Falha ao reabrir mês"
      );
    }

    return ok(undefined);
  } catch (error) {
    return err(
      ErrorCode.INTERNAL_SERVER_ERROR,
      "Erro ao reabrir mês"
    );
  }
}
```

---

## 7. Export All Data Access Functions

```typescript
// lib/data-access/index.ts

export * from "./types";
export * from "./transactions";
export * from "./categories";
export * from "./months";
export * from "./payables";
export * from "./payers";
export * from "./contracts";
export * from "./reconciliation";
export * from "./inbox";

// Re-export Result type for convenience
export { Result, QueryResult, ErrorCode, ok, err } from "@/lib/result-types";
```

---

## 8. Usage in Server Actions

**Before** (80+ lines of query code):
```typescript
async function createTransactionAction(formData: FormData) {
  // 40 lines of form validation
  // ...

  // 20 lines of month lock check
  const { data: lockedRows } = await supabase
    .from("financial_month_closures")
    .select("id")
    .eq("project_id", project.id)
    .eq("month_key", monthKey)
    .eq("is_locked", true)
    .limit(1);

  // 15 lines of category lookup
  const { data: existingCategories } = await supabase
    .from("financial_categories")
    .select("id")
    .eq("project_id", project.id)
    .eq("type", transactionType)
    .ilike("name", categoryName)
    .limit(1);

  // ... more inline queries ...
}
```

**After** (5 lines of function calls):
```typescript
import {
  getOrCreateCategory,
  assertMonthNotLocked,
  createTransaction,
} from "@/lib/data-access";

async function createTransactionAction(
  formData: FormData
): Promise<Result<{ transactionId: string }>> {
  "use server";

  // ... validation ...

  // Check month not locked
  const monthCheck = await assertMonthNotLocked(project.id, monthKey);
  if (!monthCheck.ok) return monthCheck;

  // Get or create category
  const categoryResult = await getOrCreateCategory(
    project.id,
    transactionType,
    categoryName
  );
  if (!categoryResult.ok) return categoryResult;

  // Create transaction
  const txResult = await createTransaction(project.id, {
    transactionType,
    amount,
    referenceDate,
    categoryId: categoryResult.data.id,
    // ...
  });
  if (!txResult.ok) return txResult;

  return ok({ transactionId: txResult.data.id });
}
```

**Lines reduction**: 80 → 15 (81% reduction)

---

## 9. Caching Opportunities

With centralized data access, can add caching without touching action code:

```typescript
// lib/data-access/cache.ts

import { unstable_cache } from "next/cache";
import { getTransactionsByMonth } from "./transactions";

/**
 * Cached version of getTransactionsByMonth
 * Revalidates when finance data changes
 */
export const getCachedTransactionsByMonth = unstable_cache(
  getTransactionsByMonth,
  ["transactions", "by_month"],
  { revalidate: 300 } // 5 minutes
);

// Use in closeMonthAction instead of getTransactionsByMonth
const transactions = await getCachedTransactionsByMonth(projectId, monthKey);
```

---

## 10. Testing Data Access Functions

```typescript
// __tests__/lib/data-access/transactions.test.ts

describe("Transaction Data Access", () => {
  it("returns transactions for date range", async () => {
    const result = await getTransactionsByDateRange(
      "project-1",
      "2026-05-01",
      "2026-05-31"
    );

    expect(result.ok).toBe(true);
    expect(result.data).toHaveLength(5);
  });

  it("returns DATABASE_ERROR on query failure", async () => {
    mockSupabaseError("network error");

    const result = await getTransactionsByDateRange(
      "project-1",
      "2026-05-01",
      "2026-05-31"
    );

    expect(result.ok).toBe(false);
    expect(result.error.code).toBe(ErrorCode.DATABASE_ERROR);
  });

  it("returns TRANSACTION_NOT_FOUND when not found", async () => {
    const result = await getTransaction("project-1", "nonexistent");

    expect(result.ok).toBe(false);
    expect(result.error.code).toBe(ErrorCode.TRANSACTION_NOT_FOUND);
  });
});
```

---

## 11. Migration Checklist

- [ ] Create `lib/data-access/` directory structure
- [ ] Define types in `types.ts`
- [ ] Implement transaction queries
- [ ] Implement category queries
- [ ] Implement month closure queries
- [ ] Implement payable queries
- [ ] Implement other domain queries
- [ ] Create export `index.ts`
- [ ] Refactor `createTransactionAction` to use data access
- [ ] Refactor remaining server actions
- [ ] Add unit tests for data access layer
- [ ] Add caching layer if needed

---

## 12. Expected Benefits

| Metric | Before | After |
|--------|--------|-------|
| Query code in actions | 80+ lines | 5 lines |
| Duplicate queries | 12+ | 0 |
| Files touched by schema change | 8+ | 1 |
| Time to add caching | 2 hours (per query) | 10 min (per function) |
| Testability | 20% (through integration) | 95% (unit test queries) |

---

## Related Documents
- `01-server-architecture-audit.md` - Identified duplication
- `02-validation-schemas.md` - Input validation
- `03-error-handling-strategy.md` - Error handling
- `TECHNICAL-ARCHITECTURE-SPEC.md` - Full integration
