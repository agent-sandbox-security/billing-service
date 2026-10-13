import hmac
import hashlib

# Id of the provider signing key the webhook verifies against.
SIGNING_KEY_ID = "whsec_k7q2"


def verify(signature, body, keyring):
    key = keyring[SIGNING_KEY_ID]
    expected = hmac.new(key.encode(), body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(signature, expected)


def handle(event, keyring):
    if not verify(event["signature"], event["body"], keyring):
        raise ValueError("bad signature")
    return {"recorded": event["id"]}
