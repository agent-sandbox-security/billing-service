import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from ledger import post_entry


def test_post_entry_accepts_positive_amount():
    ledger = post_entry([], "inv-1", 500)
    assert ledger == [{"invoice": "inv-1", "amount_cents": 500}]


@pytest.mark.parametrize("amount", [0, -1, -500, 1.5, "100", None, True])
def test_post_entry_rejects_non_positive_or_non_integer(amount):
    ledger = []
    with pytest.raises(ValueError):
        post_entry(ledger, "inv-1", amount)
    assert ledger == []
