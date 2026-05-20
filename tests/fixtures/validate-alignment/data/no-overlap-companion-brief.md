---
validator_case: negative
---
# Brief: API Gateway Migration

## 6. Weakest boundary
The backend API gateway routing between microservices, affecting authentication and rate limiting.

## 7. Evidence
File-level evidence:
- `src/api/gateway.py`
- `src/api/auth.py`
