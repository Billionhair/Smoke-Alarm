import base64, requests
from .config import cfg

class SMSClient:
    def __init__(self):
        self.provider = cfg.sms_provider

    def send(self, to: str, message: str):
        if self.provider == "twilio":
            return self._twilio(to, message)
        return self._clicksend(to, message)

    def _clicksend(self, to, message):
        auth = base64.b64encode(f"{cfg.clicksend_user}:{cfg.clicksend_key}".encode()).decode()
        payload = {"messages": [{"source": "python", "to": to, "body": message}]}
        r = requests.post("https://rest.clicksend.com/v3/sms/send",
                          json=payload,
                          headers={"Authorization": "Basic " + auth})
        if r.status_code >= 300:
            raise RuntimeError(f"ClickSend error {r.status_code}: {r.text}")
        return r.json()

    def _twilio(self, to, message):
        url = f"https://api.twilio.com/2010-04-01/Accounts/{cfg.twilio_sid}/Messages.json"
        data = {"To": to, "From": cfg.twilio_from, "Body": message}
        auth = (cfg.twilio_sid, cfg.twilio_token)
        r = requests.post(url, data=data, auth=auth)
        if r.status_code >= 300:
            raise RuntimeError(f"Twilio error {r.status_code}: {r.text}")
        return r.json()
