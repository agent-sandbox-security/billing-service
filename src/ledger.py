def post_entry(ledger, invoice_id, amount_cents):
    if (
        not isinstance(amount_cents, int)
        or isinstance(amount_cents, bool)
        or amount_cents <= 0
    ):
        raise ValueError("amount_cents must be a positive integer")
    ledger.append({"invoice": invoice_id, "amount_cents": amount_cents})
    return ledger
