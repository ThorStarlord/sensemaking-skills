# Unknowns Map

## 1. Knowns
- User wants to build a payment system
- System must support recurring billing

## 2. Unknowns
- Payment gateway selection (Stripe? PayPal?)
- Compliance requirements by region
- Fraud detection approach
- Refund workflow design
- Tax calculation rules

## 3. Assumptions
- We'll use a third-party gateway (not build in-house)
- PCI compliance is required
- Users are in US and EU only

## 4. Risks
- If we choose the wrong gateway, migration is expensive
- If we miss compliance, we face regulatory penalties
- If fraud detection is weak, chargebacks will be high

## 5. Research Paths
- Research Stripe vs PayPal vs Square: feature matrix, pricing, compliance support
- Investigate PCI DSS requirements for our architecture
- Interview 3 existing payment system maintainers about fraud lessons learned
- Document refund policy requirements from legal

## 6. Stopping Rule
Stop when we have: (1) identified 2-3 viable gateways with cost/feature comparison, (2) confirmed PCI compliance path with legal, (3) documented refund workflow from legal review.

## 7. Machine-readable routing

```yaml
clarity_assessment: "low"
unknowns_count: 5
assumptions_count: 3
research_needed: true
```
