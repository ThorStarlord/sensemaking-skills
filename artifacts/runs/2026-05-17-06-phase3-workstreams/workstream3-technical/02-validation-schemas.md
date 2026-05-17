# Validation Layer Design - Finance Module

**Document**: Phase 3 Workstream 3 - Technical Foundation
**Date**: 2026-05-17
**Purpose**: Centralize all Zod validation schemas to eliminate 150+ lines of duplicated validation logic

---

## 1. Problem Statement

**Current state**: Validation scattered across 18 server actions
- 6 custom regex patterns used across multiple actions
- No reusable validation helpers
- Validation logic tested only through integration (manual form submission)
- Changes to validation require edits in multiple files

**Example duplication**:
```typescript
// In createTransactionAction
const referenceDate = String(formData.get("referenceDate") ?? "").trim();
if (!/^\d{4}-\d{2}-\d{2}$/.test(referenceDate)) {
  redirect(buildRedirect({ error: "Data inválida." }));
}

// In createPayableAction (same validation, different context)
const dueDate = toIsoDate(formData.get("dueDate"));
if (!dueDate) redirect(buildRedirect(monthKey, { error: "Data de vencimento invalida." }));

// In closeMonthAction (yet another variant)
const monthKey = String(formData.get("monthKey") ?? "").trim();
if (!/^\d{4}-\d{2}$/.test(monthKey)) {
  redirect("/admin/finance/reports?error=M%C3%AAs%20inv%C3%A1lido");
}
```

---

## 2. Solution: Centralized Schema Library

Create `lib/schemas/finance.ts` with all finance-related validation schemas.

### 2.1 Core Entity Schemas

#### Transaction Schema
```typescript
import { z } from "zod";

export const transactionSchema = z.object({
  transactionType: z.enum(["income", "expense"]),
  amount: z.number().positive("Valor deve ser maior que zero"),
  referenceDate: z.string().regex(/^\d{4}-\d{2}-\d{2}$/, "Data deve estar no formato YYYY-MM-DD"),
  description: z.string().nullable(),
  categoryName: z.string().nullable(),
  paymentMethod: z.string().nullable(),
  sourceFileUrl: z.string().url().nullable(),
  viewMonthKey: z.string().regex(/^\d{4}-\d{2}$/, "Mês inválido").optional(),
});

export type Transaction = z.infer<typeof transactionSchema>;
```

**Benefits**:
- Validation logic in one place
- Reusable in form client-side validation (send schema to client)
- Single source of error messages
- Testable in isolation

#### Usage in Server Action
```typescript
async function createTransactionAction(formData: FormData) {
  "use server";

  const session = await getDevSession();
  if (!session?.roles.includes("admin")) {
    redirect("/login?next=/admin/finance");
  }

  // Consolidate all form data extraction + validation in one step
  const formInput = {
    transactionType: formData.get("transactionType"),
    amount: formData.get("amount"),
    referenceDate: formData.get("referenceDate"),
    description: formData.get("description"),
    categoryName: formData.get("categoryName"),
    paymentMethod: formData.get("paymentMethod"),
    sourceFileUrl: formData.get("sourceFileUrl"),
    viewMonthKey: formData.get("viewMonthKey"),
  };

  // Parse and validate - if fails, Zod throws with structured error
  const validation = transactionSchema.safeParse(formInput);
  if (!validation.success) {
    const firstError = validation.error.issues[0];
    redirect(
      buildFinanceHrefPath(baseMonthKey, {
        error: firstError.message,
        monthKey: formInput.viewMonthKey,
      })
    );
  }

  const data = validation.data;
  const amount = parsePtBrMoneyToNumber(data.amount); // If string input

  // ... rest of action ...
}
```

**Reduction**: 40 lines → 10 lines (75% less validation code in action)

---

### 2.2 Common Format Schemas

These are reusable for multiple entities.

#### Date Formats
```typescript
export const isoDateSchema = z.string().regex(/^\d{4}-\d{2}-\d{2}$/, "Data inválida");
export const isoMonthSchema = z.string().regex(/^\d{4}-\d{2}$/, "Mês inválido");
export const isoDateTimeSchema = z.string().datetime();
```

#### Money Amounts
```typescript
export const positiveMoneySchema = z.number().positive("Valor deve ser maior que zero");
export const moneySchema = z.number();
```

#### Common Enums
```typescript
export const transactionTypeEnum = z.enum(["income", "expense"]);
export const paymentMethodEnum = z.enum([
  "cash",
  "credit_card",
  "debit_card",
  "bank_transfer",
  "check",
  "other",
]);
```

#### Date Range
```typescript
export const dateRangeSchema = z.object({
  startDate: isoDateSchema,
  endDate: isoDateSchema,
}).refine(
  (data) => new Date(data.startDate) <= new Date(data.endDate),
  { message: "Data inicial deve ser menor que data final" }
);
```

---

### 2.3 Entity Schemas (Full List)

#### Transaction
```typescript
export const transactionInputSchema = z.object({
  transactionType: transactionTypeEnum,
  amount: positiveMoneySchema,
  referenceDate: isoDateSchema,
  description: z.string().max(500).nullable(),
  categoryName: z.string().max(100).nullable(),
  paymentMethod: paymentMethodEnum.nullable(),
  sourceFileUrl: z.string().url().nullable(),
});

export const transactionUpdateSchema = transactionInputSchema.partial().required({
  transactionType: false,
});

export const transactionDBSchema = transactionInputSchema.extend({
  id: z.string().uuid(),
  projectId: z.string().uuid(),
  categoryId: z.string().uuid().nullable(),
  isVerified: z.boolean(),
  createdAt: isoDateTimeSchema,
  updatedAt: isoDateTimeSchema,
});

export type TransactionInput = z.infer<typeof transactionInputSchema>;
export type TransactionDB = z.infer<typeof transactionDBSchema>;
```

#### Billing Payer
```typescript
export const payerInputSchema = z.object({
  fullName: z.string().min(1, "Nome obrigatório").max(255),
  email: z.string().email().nullable(),
  phone: z.string().max(20).nullable(),
  documentId: z.string().max(50).nullable(),
  guardianId: z.string().uuid().nullable(),
});

export type PayerInput = z.infer<typeof payerInputSchema>;
```

#### Billing Contract
```typescript
export const contractInputSchema = z.object({
  payerId: z.string().uuid("Pagador obrigatório"),
  studentId: z.string().uuid().nullable(),
  amount: positiveMoneySchema,
  billingDay: z.number().int().min(1).max(31),
  startDate: isoDateSchema,
  endDate: isoDateSchema.nullable(),
  description: z.string().max(500).nullable(),
  paymentMethodPreference: paymentMethodEnum.nullable(),
}).refine(
  (data) => !data.endDate || new Date(data.startDate) <= new Date(data.endDate),
  { message: "Data inicial deve ser menor que data final" }
);

export type ContractInput = z.infer<typeof contractInputSchema>;
```

#### Financial Payable (AP)
```typescript
export const payableInputSchema = z.object({
  description: z.string().min(1, "Descrição obrigatória").max(500),
  vendorName: z.string().max(255).nullable(),
  amount: positiveMoneySchema,
  dueDate: isoDateSchema,
  categoryName: z.string().max(100).nullable(),
  paymentMethodPreference: paymentMethodEnum.nullable(),
});

export const payableUpdateSchema = payableInputSchema.partial();

export type PayableInput = z.infer<typeof payableInputSchema>;
export type PayableUpdate = z.infer<typeof payableUpdateSchema>;
```

#### Inbox Item (Text)
```typescript
export const textInboxInputSchema = z.object({
  title: z.string().min(1, "Título obrigatório").max(500),
  description: z.string().max(5000).nullable(),
  sourceUrl: z.string().url().nullable(),
  tags: z.array(z.string()).optional(),
});

export type TextInboxInput = z.infer<typeof textInboxInputSchema>;
```

#### Inbox Item (Link)
```typescript
export const linkInboxInputSchema = z.object({
  url: z.string().url("URL inválida"),
  title: z.string().max(500).nullable(),
  description: z.string().max(5000).nullable(),
  tags: z.array(z.string()).optional(),
});

export type LinkInboxInput = z.infer<typeof linkInboxInputSchema>;
```

#### Month Closure
```typescript
export const monthClosureInputSchema = z.object({
  monthKey: isoMonthSchema,
  notes: z.string().max(1000).nullable(),
  forceClose: z.boolean().default(false),
});

export const monthReopenInputSchema = z.object({
  monthKey: isoMonthSchema,
  reason: z.string().max(1000),
});

export type MonthClosureInput = z.infer<typeof monthClosureInputSchema>;
export type MonthReopenInput = z.infer<typeof monthReopenInputSchema>;
```

---

## 3. FormData Extraction Helper

Create utility to extract + validate FormData in one step:

```typescript
// lib/form-validation.ts

export function extractFormData<T>(
  formData: FormData,
  schema: z.ZodSchema<T>
): { success: true; data: T } | { success: false; error: z.ZodError } {
  const input = Object.fromEntries(formData.entries());
  const validation = schema.safeParse(input);

  if (!validation.success) {
    return { success: false, error: validation.error };
  }

  return { success: true, data: validation.data };
}

// Usage in action:
const validation = extractFormData(formData, transactionInputSchema);
if (!validation.success) {
  const error = validation.error.issues[0];
  redirect(buildRedirect({ error: error.message }));
}

const data = validation.data;
```

**Lines saved per action**: 20-30 lines

---

## 4. Schema Organization

### File Structure
```
lib/schemas/
├── index.ts           # Export all schemas
├── common.ts          # Enums, primitives (date, money, etc.)
├── transaction.ts     # Transaction schemas
├── billing.ts         # Payer, contract schemas
├── payable.ts         # Payable, settlement schemas
├── inbox.ts           # Inbox item schemas
├── reconciliation.ts  # Reconciliation, matching schemas
└── month.ts           # Month closure, reopen schemas
```

### Export All
```typescript
// lib/schemas/index.ts
export * from "./common";
export * from "./transaction";
export * from "./billing";
export * from "./payable";
export * from "./inbox";
export * from "./reconciliation";
export * from "./month";
```

---

## 5. Client-Side Reuse

Schemas can be sent to client for form validation (using zod-form-data or similar):

```typescript
// app/admin/finance/billing/CreatePayerForm.tsx
import { payerInputSchema } from "@/lib/schemas";
import { useFormValidation } from "@/hooks/use-form-validation";

export function CreatePayerForm() {
  const { register, formState } = useFormValidation(payerInputSchema);

  return (
    <form>
      <input
        {...register("fullName")}
        placeholder="Nome completo"
      />
      {formState.errors.fullName && (
        <span>{formState.errors.fullName.message}</span>
      )}
    </form>
  );
}
```

**Benefit**: Validation logic DRY across server and client

---

## 6. Error Message Localization

Centralize error messages for future i18n:

```typescript
// lib/schemas/messages.ts
export const messages = {
  REQUIRED: "Campo obrigatório",
  INVALID_EMAIL: "Email inválido",
  INVALID_DATE: "Data inválida",
  INVALID_ISO_DATE: "Data deve estar no formato YYYY-MM-DD",
  INVALID_ISO_MONTH: "Mês deve estar no formato YYYY-MM",
  POSITIVE_AMOUNT: "Valor deve ser maior que zero",
  URL_REQUIRED: "URL inválida",
  MONTH_NOT_FOUND: "Mês não encontrado",
  PAYER_REQUIRED: "Selecione um responsável financeiro",
  AMOUNT_INVALID: "Valor inválido",
  BILLING_DAY_INVALID: "Dia de cobrança inválido",
  MONTH_LOCKED: "Mês fechado. Reabra o mês em Relatórios para alterar.",
};

// Schemas use these:
export const payerInputSchema = z.object({
  fullName: z.string().min(1, messages.REQUIRED),
  // ...
});
```

---

## 7. Testing Strategy

### Unit Tests for Schemas
```typescript
// __tests__/lib/schemas/transaction.ts
import { transactionInputSchema } from "@/lib/schemas";

describe("transactionInputSchema", () => {
  it("accepts valid transaction", () => {
    const input = {
      transactionType: "income",
      amount: 100.50,
      referenceDate: "2026-05-17",
      description: "Test income",
      categoryName: "Sales",
    };
    const result = transactionInputSchema.safeParse(input);
    expect(result.success).toBe(true);
  });

  it("rejects negative amount", () => {
    const input = {
      transactionType: "income",
      amount: -100,
      referenceDate: "2026-05-17",
    };
    const result = transactionInputSchema.safeParse(input);
    expect(result.success).toBe(false);
    expect(result.error.issues[0].message).toBe("Valor deve ser maior que zero");
  });

  it("rejects invalid date format", () => {
    const input = {
      transactionType: "income",
      amount: 100,
      referenceDate: "17/05/2026", // Wrong format
    };
    const result = transactionInputSchema.safeParse(input);
    expect(result.success).toBe(false);
  });
});
```

---

## 8. Migration Path

### Step 1: Extract Schemas (Week 1)
- Create `lib/schemas/` directory
- Define all schemas from actual server action code
- No changes to actions yet

### Step 2: Add Extraction Helper (Week 1)
- Create `extractFormData()` utility
- Add to one action as proof-of-concept
- Verify works with existing validation

### Step 3: Refactor Actions (Week 2)
- Update all 18 server actions to use schemas
- Remove inline validation code
- Update error handling to use schema error messages

### Step 4: Add Client-Side Validation (Week 3)
- Setup client form validation with schemas
- Add pre-submission validation in forms
- Reduce server round-trips for validation errors

---

## 9. Expected Benefits

| Metric | Before | After | Savings |
|--------|--------|-------|---------|
| Validation code per action | 30-40 lines | 5-10 lines | 75% |
| Total validation code | 500+ lines | 150 lines | 70% |
| Validation test coverage | 5% | 95% | 1900% |
| Time to add new validation rule | 15 min (update 4 places) | 2 min (update schema) | 87% |
| Bug-fix time for validation | 20 min (test 4 places) | 5 min (test schema) | 75% |

---

## 10. Related Documents
- `01-server-architecture-audit.md` - Full audit findings
- `03-error-handling-strategy.md` - How validation errors flow to UI
- `04-data-access-layer.md` - Query validation with schemas
- `TECHNICAL-ARCHITECTURE-SPEC.md` - Integration with full system
