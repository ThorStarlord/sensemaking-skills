# Problem Frame: Metamorfose Pedagogico System

## 1. Raw Fog

The Pedagogico admin page (`app/admin/pedagogico/[surface]/page.tsx`, 12 lines) is a Next.js server component that renders a single, delegated component.

**The code:**
```tsx
import { FinanzasAdminRoutePage } from "@/components/admin/finanzas-admin-route-page";

export const dynamic = "force-dynamic";

type PageProps = {
  params: Promise<{ surface: string }>;
};

export default async function PedagogicoSurfacePage(props: PageProps) {
  const params = await props.params;
  return <FinanzasAdminRoutePage href={`/admin/pedagogico/${params.surface}`} />;
}
```

**What is immediately clear:**
- This is a **wrapper/router component**, not a business logic implementation
- It receives a `surface` URL parameter and passes it to a generic component
- The component name (`FinanzasAdminRoutePage`) and href suggest a **generic routing pattern** shared across multiple admin sections
- There is minimal state, logic, or decision-making in this 12-line file

## 2. Problem Under the Problem

The minimal code raises a **clarity question**: Is this the entire pedagogico interface, or is the real complexity hidden in `FinanzasAdminRoutePage`?

The problem is **deceptively simple**: This page is either:
- A **transparent routing layer** (no real problem to solve here, just navigation)
- A **facade hiding complexity** (the real pedagogico logic lives in the shared component)

But within the scope of **this specific file**, there is almost no problem to frame. The page:
- Takes a parameter
- Passes it to a reusable component
- Returns markup

This suggests that **pedagogico** might not be a "system" at all in the architectural sense—it's just a view into a generic admin interface.

## 3. Object Under Pressure

**File**: `app/admin/pedagogico/[surface]/page.tsx` (12 lines)

**Specific points:**
- Line 3: `export const dynamic = "force-dynamic"` — indicates this page cannot be statically cached (likely because surface parameter varies)
- Line 9: Dynamic route parameter `params.surface` — the only runtime variable
- Line 11: URL construction `/admin/pedagogico/${params.surface}` — passes the surface directly to child component
- No data loading, no validation, no error handling

**Clarity**: The structure is maximally simple. There are no hidden constraints or implicit assumptions visible in this file.

## 4. Failure Mode

If this page has a failure mode, it would only be at the **integration boundary** with `FinanzasAdminRoutePage`:
- What if `params.surface` contains invalid characters? (handled by router or component?)
- What if `FinanzasAdminRoutePage` doesn't expect a pedagogico-specific href? (would show broken UI)
- What if the generic component isn't designed for pedagogico use cases? (feature parity problem)

But these failures are **not in this file**—they're in the component it delegates to or in the overall routing design.

## 5. Success Condition

A clear understanding that:
- Pedagogico is implemented as a **delegated component**, not a standalone system
- The real business logic and data model live in `FinanzasAdminRoutePage` or its children
- Any pedagogico-specific problems belong to that component, not this wrapper
- The routing is straightforward and requires no additional validation

## 6. What Must Be True

For the success condition to be reachable:
- [x] This 12-line file is the complete pedagogico page (verified by reading source)
- [x] The page is a transparent wrapper with no business logic
- [ ] `FinanzasAdminRoutePage` is the actual implementation (not verified yet, but not necessary for this frame)
- [ ] The routing parameter (`surface`) is valid and well-formed (delegated to router)

## 7. Next Artifact

**Unknowns Map** — to verify:
- Are there actually any unknowns in this ultra-minimal system?
- What assumptions must be true about the reused component?
- Is research needed, or is the simplicity genuine?
- Routing decision: Should we skip deeper research for this transparent wrapper?
