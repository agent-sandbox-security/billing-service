import hmac
import hashlib


def verify(signature, body, signing_key):
    if isinstance(body, str):
        body = body.encode("utf-8")
    expected = hmac.new(signing_key.encode(), body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(signature, expected)


def handle(event, signing_key):
    if not verify(event["signature"], event["body"], signing_key):
        raise ValueError("bad signature")
    return {"recorded": event["id"]}
