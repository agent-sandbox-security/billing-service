# Invoice id prefixes that take part in monthly reconciliation.
INCLUDED_PREFIXES = ("inv-", "sub-", "promo-")


def filter_invoices(invoices):
    """Invoices that take part in monthly reconciliation."""
    return [i for i in invoices if i["id"].startswith(INCLUDED_PREFIXES)]


def post_entry(ledger, invoice_id, amount_cents):
    ledger.append({"invoice": invoice_id, "amount_cents": amount_cents})
    return ledger
