# billing-service

Issues invoices and reconciles payments. Webhooks from the payment
provider are verified in `src/webhook.py` and recorded by `src/ledger.py`.
