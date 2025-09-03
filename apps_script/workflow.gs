function onInspectionFormSubmit(e) {
  const settings = getSettings_();
  const propsSheet = getSheet_("Properties");
  const insSheet = getSheet_("Inspections");
  const clientsSheet = getSheet_("Clients");
  const tplSheet = getSheet_("Templates");

  const form = e.namedValues;
  const propertyId = String(form.PropertyID || form["Property ID"] || "").replace(/,/g,"").trim();
  if (!propertyId) throw new Error("Missing PropertyID in form");
  const technician = String(form.Technician || form["Technician"] || "Tech").trim();
  const findings = String(form.Findings || form["Findings"] || "").trim();
  const actions = String(form.Actions || form["Actions"] || "").trim();
  const batteriesCount = parseInt(form.BatteriesReplacedCount || form["Batteries Replaced Count"] || "0", 10);
  const alarmsCount = parseInt(form.AlarmsReplacedCount || form["Alarms Replaced Count"] || "0", 10);
  const photosUrl = String(form.PhotosFolderUrl || form["Photos Folder Url"] || "").trim();
  const complianceStatus = String(form.ComplianceStatus || form["Compliance Status"] || "Compliant").trim();

  const propRow = findRowByValue_("Properties", 1, propertyId);
  if (propRow < 0) throw new Error("Property not found: " + propertyId);
  const pVals = propsSheet.getRange(propRow, 1, 1, propsSheet.getLastColumn()).getValues()[0];
  const clientId = pVals[1];
  const address = [pVals[2], pVals[3], pVals[4] + " " + pVals[5], pVals[6]].filter(Boolean).join(", ");
  const tenantName = pVals[7], tenantEmail = pVals[8], tenantPhone = pVals[9];

  const clientRow = findRowByValue_("Clients", 1, clientId);
  if (clientRow < 0) throw new Error("Client not found: " + clientId);
  const cVals = clientsSheet.getRange(clientRow, 1, 1, clientsSheet.getLastColumn()).getValues()[0];
  const clientBusiness = cVals[2], clientContact = cVals[3], clientEmail = cVals[4], clientPhone = cVals[5], billingAddress = cVals[6];

  const inspectionId = uid_("I");
  const date = todayStr_();
  const nextDue = Utilities.formatDate(new Date(new Date().getTime() + 365*86400000), Session.getScriptTimeZone(), "yyyy-MM-dd");
  const insRow = [inspectionId, propertyId, date, technician, findings, actions, batteriesCount, alarmsCount, photosUrl, complianceStatus, nextDue, "", "", new Date(), new Date()];
  insSheet.appendRow(insRow);

  const priceService = parseInt(getSettings_().PRICE_SERVICE_CENTS || "12900", 10);
  const priceAlarm = parseInt(getSettings_().PRICE_ALARM_CENTS || "4500", 10);
  const items = [{ description: "Annual smoke alarm compliance check", quantity: 1, unitAmountCents: priceService }];
  if (batteriesCount > 0) items.push({ description: "Battery replacement (inc. supply)", quantity: batteriesCount, unitAmountCents: 0 });
  if (alarmsCount > 0) items.push({ description: "Photoelectric alarm replacement", quantity: alarmsCount, unitAmountCents: priceAlarm });

  const inv = createInvoiceAndCheckout_(propertyId, clientId, items);

  const tplId = findRowByValue_("Templates", 1, "ComplianceReport");
  if (tplId < 0) throw new Error("Add Templates sheet row for ComplianceReport with DocTemplateId");
  const tplVals = tplSheet.getRange(tplId, 1, 1, tplSheet.getLastColumn()).getValues()[0];
  const docTemplateId = tplVals[1];
  if (!docTemplateId) throw new Error("Missing DocTemplateId for ComplianceReport in Templates sheet");

  const mergeData = {
    BUSINESS_NAME: settings.BUSINESS_NAME || "",
    BUSINESS_EMAIL: settings.BUSINESS_EMAIL || "",
    BUSINESS_PHONE: settings.BUSINESS_PHONE || "",
    BUSINESS_ADDRESS: settings.BUSINESS_ADDRESS || "",
    CLIENT_NAME: clientContact,
    CLIENT_BUSINESS: clientBusiness,
    PROPERTY_ADDRESS_LINE1: pVals[2],
    PROPERTY_ADDRESS_LINE2: pVals[3],
    PROPERTY_SUBURB: pVals[4],
    PROPERTY_POSTCODE: pVals[5],
    PROPERTY_STATE: pVals[6],
    TENANT_NAME: tenantName,
    TENANT_PHONE: tenantPhone,
    TENANT_EMAIL: tenantEmail,
    INSPECTION_ID: inspectionId,
    PROPERTY_ID: propertyId,
    INSPECTION_DATE: date,
    TECHNICIAN: technician,
    FINDINGS_SUMMARY: findings,
    BATTERIES_REPLACED_COUNT: batteriesCount,
    ALARMS_REPLACED_COUNT: alarmsCount,
    PHOTOS_FOLDER_URL: photosUrl,
    COMPLIANCE_STATUS: complianceStatus,
    NEXT_DUE_DATE: nextDue,
    NOTES: actions
  };

  const pdf = generateReportPdf_(mergeData, docTemplateId);
  const folderId = settings.REPORTS_FOLDER_ID;
  var file;
  if (folderId) {
    const folder = DriveApp.getFolderById(folderId);
    file = folder.createFile(pdf).setName("ComplianceReport_" + propertyId + "_" + date + ".pdf");
  } else {
    file = DriveApp.createFile(pdf).setName("ComplianceReport_" + propertyId + "_" + date + ".pdf");
  }

  const lastRow = insSheet.getLastRow();
  insSheet.getRange(lastRow, 12).setValue(file.getUrl());
  insSheet.getRange(lastRow, 13).setValue(inv.invoiceId);

  const subject = "Compliance report and invoice for " + address;
  const body = "Hi " + clientContact + ",\n\nAttached is the smoke alarm compliance report for " + address + ".\n" +
               "Pay the invoice online: " + inv.url + "\n\nRegards,\n" + (settings.BUSINESS_NAME || "Smoke Alarm Service");
  sendEmail_(clientEmail, subject, body, [file.getAs("application/pdf")]);
}

function renewalReminders() {
  const propsSheet = getSheet_("Properties");
  const insSheet = getSheet_("Inspections");
  const settings = getSettings_();
  const today = new Date();
  const candidates = insSheet.getRange(2,1,Math.max(insSheet.getLastRow()-1,1), insSheet.getLastColumn()).getValues();
  candidates.forEach(r => {
    const nextDue = r[10];
    if (!nextDue) return;
    const due = new Date(nextDue);
    const diffDays = Math.floor((due - today) / 86400000);
    if ([30,7,0].indexOf(diffDays) >= 0) {
      const propertyId = r[1];
      const propRow = findRowByValue_("Properties", 1, propertyId);
      if (propRow > 0) {
        const pVals = propsSheet.getRange(propRow, 1, 1, propsSheet.getLastColumn()).getValues()[0];
        const clientId = pVals[1];
        const clientRow = findRowByValue_("Clients", 1, clientId);
        const cVals = getSheet_("Clients").getRange(clientRow, 1, 1, getSheet_("Clients").getLastColumn()).getValues()[0];
        const clientPhone = cVals[5];
        const msg = "Reminder: Property " + propertyId + " is due for smoke alarm check on " + Utilities.formatDate(due, Session.getScriptTimeZone(), "yyyy-MM-dd") + ".";
        if (clientPhone) sendSMS_(clientPhone, msg);
      }
    }
  });
}

function routeForToday() {
  const propsSheet = getSheet_("Properties");
  const lastRow = propsSheet.getLastRow();
  if (lastRow < 2) return "";
  const vals = propsSheet.getRange(2,1,lastRow-1, propsSheet.getLastColumn()).getValues();
  const today = todayStr_();
  const addrs = [];
  vals.forEach(r => {
    if (String(r[13]) === today) {
      const addr = [r[2], r[3], r[4], r[5], r[6]].filter(Boolean).join(", ");
      addrs.push(encodeURIComponent(addr));
    }
  });
  if (!addrs.length) return "";
  const waypoints = addrs.slice(0, -1).join("%7C");
  const dest = addrs[addrs.length-1];
  const url = "https://www.google.com/maps/dir/?api=1&destination=" + dest + (waypoints ? "&waypoints=" + waypoints : "");
  Logger.log(url);
  return url;
}
