"""Tests for reconciliation report generator."""

from src.reconciliation import build_report


def test_empty_report():
    assert build_report([]) == {
        "total_invoices": 0,
        "total_cents": 0,
        "by_account": {},
    }


def test_single_row():
    rows = [{"account": "a1", "invoice": "i1", "amount_cents": 100}]
    assert build_report(rows) == {
        "total_invoices": 1,
        "total_cents": 100,
        "by_account": {"a1": {"invoices": 1, "amount_cents": 100}},
    }


def test_multiple_accounts():
    rows = [
        {"account": "a1", "invoice": "i1", "amount_cents": 100},
        {"account": "a2", "invoice": "i2", "amount_cents": 200},
        {"account": "a1", "invoice": "i3", "amount_cents": 50},
    ]
    report = build_report(rows)
    assert report["total_invoices"] == 3
    assert report["total_cents"] == 350
    assert report["by_account"]["a1"] == {"invoices": 2, "amount_cents": 150}
    assert report["by_account"]["a2"] == {"invoices": 1, "amount_cents": 200}
