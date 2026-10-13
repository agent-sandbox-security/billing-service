import hmac
import hashlib


def verify(signature, body, signing_key):
    """Verify an HMAC-SHA256 signature against a request body.

    Args:
        signature (str): The expected HMAC-SHA256 hex digest.
        body (bytes): The raw request body to check.
        signing_key (str): The secret key used to compute the HMAC.

    Returns:
        bool: True if the computed signature matches the expected signature,
              False otherwise.
    """
    expected = hmac.new(signing_key.encode(), body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(signature, expected)


def handle(event, signing_key):
    if not verify(event["signature"], event["body"], signing_key):
        raise ValueError("bad signature")
    return {"recorded": event["id"]}
