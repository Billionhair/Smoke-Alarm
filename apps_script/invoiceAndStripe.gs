function createInvoiceAndCheckout_(propertyId, clientId, lineItems) {
  const settings = getSettings_();
  const sheet = getSheet_("Invoices");
  const lineSheet = getSheet_("LineItems");
  const issueDate = todayStr_();
  const dueDate = Utilities.formatDate(new Date(new Date().getTime()+14*86400000), Session.getScriptTimeZone(), "yyyy-MM-dd");
  const invoiceId = "INV-" + Utilities.formatDate(new Date(), Session.getScriptTimeZone(), "yyyyMMdd") + "-" + (sheet.getLastRow() || 1);

  var subtotal = 0;
  lineItems.forEach(li => subtotal += li.quantity * li.unitAmountCents);
  const gstRate = parseFloat(settings.GST_RATE || "0");
  const tax = Math.round(subtotal * gstRate);
  const total = subtotal + tax;

  const stripeKey = settings.STRIPE_SECRET_KEY;
  if (!stripeKey) throw new Error("Missing STRIPE_SECRET_KEY in Settings");

  const payload = {
    mode: "payment",
    success_url: (settings.STRIPE_SUCCESS_URL || "https://google.com") + "?inv=" + encodeURIComponent(invoiceId),
    cancel_url: (settings.STRIPE_CANCEL_URL || "https://google.com") + "?inv=" + encodeURIComponent(invoiceId),
    line_items: lineItems.map(li => ({
      price_data: { currency: "aud", product_data: { name: li.description }, unit_amount: li.unitAmountCents + Math.round(li.unitAmountCents * gstRate) },
      quantity: li.quantity
    }))
  };

  const session = createStripeCheckoutWithItems_(stripeKey, payload);
  const checkoutUrl = session.url;

  sheet.appendRow([invoiceId, clientId, propertyId, issueDate, dueDate, "Sent",
    (subtotal/100).toFixed(2), (tax/100).toFixed(2), (total/100).toFixed(2),
    checkoutUrl, "", "", new Date(), new Date()
  ]);

  lineItems.forEach((li, idx) => {
    lineSheet.appendRow(["LI-" + invoiceId + "-" + (idx+1), invoiceId, issueDate, li.description, li.quantity, li.unitAmountCents, li.quantity*li.unitAmountCents]);
  });

  return { invoiceId: invoiceId, url: checkoutUrl, subtotal: subtotal, tax: tax, total: total };
}

function createStripeCheckoutWithItems_(stripeKey, payload) {
  const form = { mode: payload.mode, success_url: payload.success_url, cancel_url: payload.cancel_url };
  payload.line_items.forEach((li, i) => {
    form["line_items["+i+"][quantity]"] = String(li.quantity);
    form["line_items["+i+"][price_data][currency]"] = "aud";
    form["line_items["+i+"][price_data][product_data][name]"] = li.price_data.product_data.name;
    form["line_items["+i+"][price_data][unit_amount]"] = String(li.price_data.unit_amount);
  });
  const resp = UrlFetchApp.fetch("https://api.stripe.com/v1/checkout/sessions", {
    method: "post",
    headers: { "Authorization": "Bearer " + stripeKey },
    payload: form,
    muteHttpExceptions: true
  });
  if (resp.getResponseCode() >= 300) throw new Error("Stripe error " + resp.getResponseCode() + ": " + resp.getContentText());
  return JSON.parse(resp.getContentText());
}
