"""Reconciliation report generator for billing records."""


def build_report(rows):
    """Build a reconciliation report from database rows.

    Args:
        rows: list of dicts with keys account, invoice, amount_cents.

    Returns:
        dict with total_invoices, total_cents, and per-account breakdown.
    """
    total_cents = 0
    total_invoices = 0
    by_account = {}

    for row in rows:
        account = row["account"]
        amount = row["amount_cents"]
        total_cents += amount
        total_invoices += 1
        by_account.setdefault(account, {"invoices": 0, "amount_cents": 0})
        by_account[account]["invoices"] += 1
        by_account[account]["amount_cents"] += amount

    return {
        "total_invoices": total_invoices,
        "total_cents": total_cents,
        "by_account": by_account,
    }
