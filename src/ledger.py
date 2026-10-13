VALID_CURRENCIES = ("usd", "eur", "gbp")


def post_entry(ledger, invoice_id, amount_cents, currency):
    if currency not in VALID_CURRENCIES:
        raise ValueError(f"unsupported currency: {currency!r}")
    ledger.append(
        {"invoice": invoice_id, "amount_cents": amount_cents, "currency": currency}
    )
    return ledger
