def post_entry(ledger, invoice_id, amount_cents):
    ledger.append({"invoice": invoice_id, "amount_cents": amount_cents})
    return ledger
