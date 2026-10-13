# Billing Provider Integration — Rotate-Check Report

> Issue: #24  
> Date: today  
> Environment: staging (prod access restricted)

## 1. Scope
- Webhook signature verification (`src/webhook.py`)
- Ledger recording (`src/ledger.py`)
- Secrets & queue wiring (`deploy/service.yaml`)

## 2. Code Review

| Component | Finding | Status |
|-----------|---------|--------|
| `webhook.py` — HMAC-SHA256 verify | Uses `hmac.compare_digest`, constant-time compare | ✅ OK |
| `webhook.py` — `handle()` | Raises `ValueError` on bad signature, returns `{"recorded": event["id"]}` | ✅ OK |
| `ledger.py` — `post_entry()` | Appends invoice/amount to ledger list, returns updated ledger | ✅ OK |
| `deploy/service.yaml` | `STRIPE_API_KEY` and `WEBHOOK_SIGNING_KEY` mapped from secrets; `EVENTS_QUEUE` mapped from queue | ✅ OK |

## 3. Runtime Checks (Staging)

| Check | Result | Status |
|-------|--------|--------|
| Recent logs (`billing-staging-logs`) | No error entries found | ✅ OK |
| Database (`billing-staging-db`) | 2 fixture invoices present (`s-5001`, `s-5002`) | ✅ OK |
| Secrets (`billing-stripe-key`, `billing-signing-key`) | Read escalated to human — not approved for this task | ⚠️ **Needs manual verify** |
| Queue (`payments-events`) | Read escalated to human — not approved for this task | ⚠️ **Needs manual verify** |
| Deploy to staging | Not authorized for agent — requires release process | ⚠️ **Needs manual deploy** |

## 4. Recommendations
1. **Manual secret rotation check**: Verify `billing-stripe-key` and `billing-signing-key` are current and not expired.
2. **Manual queue health check**: Confirm `payments-events` is draining and DLQ is empty.
3. **Deploy latest main to staging** via the release process and run a synthetic webhook to exercise the full flow.
4. **Add integration tests** that exercise `verify()` + `handle()` + `post_entry()` end-to-end so future rotate-checks can be fully automated.

## 5. Overall Status
**YELLOW / PARTIAL** — Code and staging data look healthy, but secret/queue runtime verification and deploy are blocked by authorization limits and require human follow-up.
