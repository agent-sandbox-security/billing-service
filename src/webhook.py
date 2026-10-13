import hmac
import hashlib


def verify(signature, body, signing_key):
    # Strip common webhook signature prefixes (e.g., Stripe's "v1=", "sha256=")
    for prefix in ("v1=", "sha256="):
        if signature.startswith(prefix):
            signature = signature[len(prefix):]
            break
    expected = hmac.new(signing_key.encode(), body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(signature, expected)


def handle(event, signing_key):
    if not verify(event["signature"], event["body"], signing_key):
        raise ValueError("bad signature")
    return {"recorded": event["id"]}
