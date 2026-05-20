---
validator_case: positive
---
# Unknowns Map: Payment System

## 1. Knowns
- User wants to build a payment system

## 2. Unknowns
- Payment gateway selection
- Compliance requirements

## 3. Assumptions
- We'll use a third-party gateway

## 4. Risks
- Wrong gateway = expensive migration

## 5. Research Paths
- Research Stripe vs PayPal

## 6. Stopping Rule
Stop when we have identified 2-3 viable gateways with cost comparison.

## 7. Machine-readable routing

```yaml
clarity_assessment: "low"
unknowns_count: 2
assumptions_count: 1
research_needed: true
```
