---
validator_case: positive
---
# Brief: Payment Gateway Issue

## 1. Repository goal
Implement a payment processing system.

## 6. Weakest boundary
The payment gateway integration boundary between the frontend checkout flow and the payment provider's API. The selection of gateway provider affects the contract for transaction data, refund workflow, and fraud detection rules.

## 7. Evidence
File-level evidence:
- `src/payment/gateway.py` — Gateway abstraction
- `src/payment/checkout.py` — Checkout workflow
- `docs/compliance/pci.md` — Compliance requirements
