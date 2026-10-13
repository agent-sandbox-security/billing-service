def post_entry(ledger, invoice_id, amount_cents):
    """Append an invoice entry to the ledger and return the ledger."""
    ledger.append({"invoice": invoice_id, "amount_cents": amount_cents})
    return ledger
