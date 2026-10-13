import hmac
import hashlib

from src import ledger


def verify(signature, body, signing_key):
    expected = hmac.new(signing_key.encode(), body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(signature, expected)


def handle(event, signing_key):
    if not verify(event["signature"], event["body"], signing_key):
        raise ValueError("bad signature")
    ledger.post_entry([], event["invoice_id"], event["amount_cents"])
    return {"recorded": event["id"]}
