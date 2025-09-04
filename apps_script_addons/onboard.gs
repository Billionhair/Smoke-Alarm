function onFormSubmit(e) {
  const data = e.namedValues;
  const name = String(data.Name || "").trim();
  const email = String(data.Email || "").trim();
  const phone = String(data.Phone || "").trim();
  const sh = getSheet_("Leads");
  sh.appendRow([todayStr_(), name, email, phone]);
  const msg = "Thanks, we'll book your first $129 check this week";
  if (email) sendEmail_(email, "Welcome to Smoke Alarm Service", msg);
  if (phone) sendSMS_(phone, msg);
}
