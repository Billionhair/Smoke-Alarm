import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Config:
    sheet_id: str = os.getenv("GOOGLE_SHEET_ID","")
    sa_path: str = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON","service_account.json")
    subject_email: str = os.getenv("GOOGLE_SUBJECT_EMAIL","")
    price_service_cents: int = int(float(os.getenv("PRICE_SERVICE_CENTS","12900")))
    price_alarm_cents: int = int(float(os.getenv("PRICE_ALARM_CENTS","4500")))
    gst_rate: float = float(os.getenv("GST_RATE","0.00"))
    stripe_key: str = os.getenv("STRIPE_SECRET_KEY","")
    success_url: str = os.getenv("STRIPE_SUCCESS_URL","https://example.com/success")
    cancel_url: str = os.getenv("STRIPE_CANCEL_URL","https://example.com/cancel")
    sms_provider: str = os.getenv("SMS_PROVIDER","clicksend").lower()
    clicksend_user: str = os.getenv("CLICKSEND_USER","")
    clicksend_key: str = os.getenv("CLICKSEND_KEY","")
    twilio_sid: str = os.getenv("TWILIO_SID","")
    twilio_token: str = os.getenv("TWILIO_AUTH_TOKEN","")
    twilio_from: str = os.getenv("TWILIO_FROM","")

cfg = Config()
