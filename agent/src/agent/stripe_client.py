import requests

from .config import cfg


class StripeClient:
    """Lightweight helper for creating Stripe checkout sessions."""

    def __init__(self) -> None:
        if not cfg.stripe_key:
            raise RuntimeError("Missing STRIPE_SECRET_KEY")

    def create_checkout(self, items: list[dict]) -> dict:
        """Create a checkout session for ``items``.

        Each ``item`` must include ``description``, ``quantity`` and
        ``unitAmountCents`` keys.
        """

        gst = cfg.gst_rate
        form = {
            "mode": "payment",
            "success_url": cfg.success_url,
            "cancel_url": cfg.cancel_url,
        }
        subtotal = 0
        for i, li in enumerate(items):
            unit = int(li["unitAmountCents"])
            qty = int(li["quantity"])
            subtotal += unit * qty
            form[f"line_items[{i}][quantity]"] = str(qty)
            form[f"line_items[{i}][price_data][currency]"] = "aud"
            form[f"line_items[{i}][price_data][product_data][name]"] = li[
                "description"
            ]
            unit_with_tax = unit + int(round(unit * gst))
            form[f"line_items[{i}][price_data][unit_amount]"] = str(unit_with_tax)
        tax = int(round(subtotal * gst))
        total = subtotal + tax
        r = requests.post(
            "https://api.stripe.com/v1/checkout/sessions",
            data=form,
            headers={"Authorization": "Bearer " + cfg.stripe_key},
        )
        if r.status_code >= 300:
            raise RuntimeError(f"Stripe error {r.status_code}: {r.text}")
        data = r.json()
        data["subtotal"] = subtotal
        data["tax"] = tax
        data["total"] = total
        return data
