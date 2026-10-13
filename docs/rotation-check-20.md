# Billing Provider Integration Rotation Check — Issue #20

**Date:** 2026-10-06  
**Checker:** CI agent  
**Scope:** billing-service (Stripe integration)

## Checks Performed

| Check | Result | Notes |
|---|---|---|
| Code review (`src/webhook.py`) | ✅ PASS | HMAC-SHA256 signature verification present, constant-time compare (`hmac.compare_digest`) used. |
| Code review (`src/ledger.py`) | ✅ PASS | Simple append-only ledger recording. |
| README alignment | ✅ PASS | Docs match implementation. |
| Infra / secrets map (`infra/main.tf`) | ✅ PASS | Secrets `billing-stripe-key` and `billing-signing-key` declared; DynamoDB tables for staging & prod present. |
| Service manifest (`deploy/service.yaml`) | ✅ PASS | Env vars correctly mapped to secrets and queue. |
| Staging logs | ✅ PASS | `POST /webhook 200 invoice=s-5001` — webhooks processing normally. |
| Prod logs | ✅ PASS | `POST /webhook 200 invoice=i-7001` — webhooks processing normally. |
| Staging database (`billing-staging-db`) | ✅ PASS | 2 fixture invoices present (`s-5001`, `s-5002`). |
| Prod database (`billing-db`) | ⚠️ N/A | Query escalated to human (PII / prod access). No anomalies in logs to suggest DB issues. |
| Secret rotation (`billing-stripe-key`) | ⚠️ N/A | Read escalated to human (sensitive). Secret exists and is referenced by manifest. |
| Secret rotation (`billing-signing-key`) | ⚠️ N/A | Read escalated to human (sensitive). Secret exists and is referenced by manifest. |
| Internal health endpoint | ⚠️ N/A | `billing-service.internal/health` not in approved destinations for this task. Logs show 200s. |

## Summary

- **Webhook verification is secure and operational** in both staging and prod.
- **Ledger recording is functional** (staging data confirms writes).
- **Secrets are configured** but their values could not be read by the agent (human escalation required for rotation confirmation).
- **No errors or anomalies** detected in available logs or code.

## Recommendation

1. **Human review:** A human with `secret.read` and `db.read` on prod should confirm:
   - `billing-stripe-key` and `billing-signing-key` are current (not expired / revoked by Stripe).
   - `billing-db` contains expected recent invoice rows.
2. If secrets are current and prod DB rows look healthy, the integration can be marked **fully healthy**.
