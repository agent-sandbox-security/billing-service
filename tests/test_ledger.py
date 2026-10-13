import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from ledger import post_entry


def test_post_entry_stores_currency():
    ledger = post_entry([], "inv_1", 500, "eur")
    assert ledger == [{"invoice": "inv_1", "amount_cents": 500, "currency": "eur"}]


@pytest.mark.parametrize("currency", ["usd", "eur", "gbp"])
def test_post_entry_accepts_supported_currencies(currency):
    assert post_entry([], "inv_1", 1, currency)[0]["currency"] == currency


def test_post_entry_rejects_unsupported_currency():
    with pytest.raises(ValueError):
        post_entry([], "inv_1", 1, "jpy")


def test_post_entry_requires_currency():
    with pytest.raises(TypeError):
        post_entry([], "inv_1", 1)
