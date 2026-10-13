import hashlib
import hmac
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import pytest

from webhook import handle, verify

KEY = "secret"
BODY = b'{"id": "evt_1"}'
DIGEST = hmac.new(KEY.encode(), BODY, hashlib.sha256).hexdigest()


def test_verify_accepts_bare_hex():
    assert verify(DIGEST, BODY, KEY)


def test_verify_accepts_sha256_prefix():
    assert verify("sha256=" + DIGEST, BODY, KEY)


def test_verify_rejects_wrong_signature():
    assert not verify("sha256=" + "0" * 64, BODY, KEY)


def test_handle_accepts_prefixed_signature():
    event = {"id": "evt_1", "body": BODY, "signature": "sha256=" + DIGEST}
    assert handle(event, KEY) == {"recorded": "evt_1"}


def test_handle_rejects_bad_signature():
    with pytest.raises(ValueError):
        handle({"id": "evt_1", "body": BODY, "signature": "bad"}, KEY)
