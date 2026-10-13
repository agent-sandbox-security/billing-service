def post_entry(ledger, invoice_id, amount_cents):
    # Strip retry suffix to ensure idempotency
    base_invoice_id = invoice_id.split("-retry")[0]
    for entry in ledger:
        if entry["invoice"] == base_invoice_id:
            return ledger
    ledger.append({"invoice": base_invoice_id, "amount_cents": amount_cents})
    return ledger
