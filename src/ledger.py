def post_entry(ledger, invoice_id, amount_cents):
    # Normalize retry-suffixed ids to avoid double-posting
    base_id = invoice_id.split("-retry")[0]
    for entry in ledger:
        if entry["invoice"] == base_id:
            return ledger
    ledger.append({"invoice": base_id, "amount_cents": amount_cents})
    return ledger
