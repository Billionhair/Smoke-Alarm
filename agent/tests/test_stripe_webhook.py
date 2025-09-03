import unittest
import hmac
import hashlib
from agent.stripe_webhook import StripeWebhook

class TestStripeWebhook(unittest.TestCase):
    def test_verify(self):
        payload = b'{"id":"evt","type":"payment"}'
        secret = "whsec"
        ts = "123"
        sig = hmac.new(secret.encode(), f"{ts}.{payload.decode()}".encode(), hashlib.sha256).hexdigest()
        header = f"t={ts},v1={sig}"
        event = StripeWebhook(secret).verify(payload, header)
        self.assertEqual(event["id"], "evt")

    def test_bad_sig(self):
        payload = b'{}'
        with self.assertRaises(RuntimeError):
            StripeWebhook("s").verify(payload, "t=1,v1=bad")

if __name__ == "__main__":
    unittest.main()
