---
validator_case: positive
validator_args:
  - --brief
  - tests/fixtures/validate-alignment/data/valid-companion-brief.md
---
# Problem Frame: Payment System

## 1. Raw Fog
Build a payment system.

## 2. Problem Under the Problem
Payment gateway selection is critical for cost and compliance.

## 3. Object Under Pressure
payment gateway integration workflow between frontend and payment provider. The selection of Stripe vs PayPal vs Square affects architecture, compliance, and fraud detection.

## 4. Failure Mode
Wrong gateway leads to expensive migration, compliance penalties, chargebacks.

## 5. Success Condition
Working payment flow with PCI compliance.

## 6. What Must Be True
- Third-party gateway (not in-house)
- PCI DSS compliance path confirmed
- Refund workflow defined

## 7. Next Artifact
Unknowns Map
