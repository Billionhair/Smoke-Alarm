function sendSMS_(to, message) {
  const settings = getSettings_();
  const provider = (settings.SMS_PROVIDER || "clicksend").toLowerCase();
  if (provider === "twilio") return sendSMS_Twilio_(to, message, settings);
  return sendSMS_ClickSend_(to, message, settings);
}

function sendSMS_ClickSend_(to, message, settings) {
  const payload = { messages: [{ source: "javascript", to: to, body: message }] };
  const resp = UrlFetchApp.fetch("https://rest.clicksend.com/v3/sms/send", {
    method: "post",
    contentType: "application/json",
    headers: { "Authorization": "Basic " + Utilities.base64Encode((settings.CLICKSEND_USER||"") + ":" + (settings.CLICKSEND_KEY||"")) },
    payload: JSON.stringify(payload),
    muteHttpExceptions: true
  });
  return resp.getContentText();
}

function sendSMS_Twilio_(to, message, settings) {
  const sid = settings.TWILIO_SID, token = settings.TWILIO_AUTH_TOKEN, from = settings.TWILIO_FROM;
  const url = "https://api.twilio.com/2010-04-01/Accounts/" + sid + "/Messages.json";
  const payload = { To: to, From: from, Body: message };
  const resp = UrlFetchApp.fetch(url, {
    method: "post",
    payload: payload,
    headers: { "Authorization": "Basic " + Utilities.base64Encode(sid + ":" + token) },
    muteHttpExceptions: true
  });
  return resp.getContentText();
}
