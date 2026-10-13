def post_entry(ledger, invoice_id, amount_cents):
    base = invoice_id.removesuffix('-retry')
    if any(e['invoice'] == base for e in ledger):
        return ledger
    ledger.append({'invoice': base, 'amount_cents': amount_cents})
    return ledger
