function oneTimeSetup() {
  const ss = SpreadsheetApp.getActive();
  const tabs = {
    "Clients": ["ClientID","Type","BusinessName","ContactName","Email","Phone","BillingAddress","Notes","PreferredChannel","StripeCustomerId","CreatedAt","UpdatedAt"],
    "Properties": ["PropertyID","ClientID","AddressLine1","AddressLine2","Suburb","Postcode","State","TenantName","TenantEmail","TenantPhone","AccessNotes","KeySafeCode","LastInspectionDate","NextDueDate","Status","Notes","CreatedAt","UpdatedAt"],
    "Alarms": ["AlarmID","PropertyID","Location","Type","PowerSource","InstallDate","ExpiryDate","LastServiceDate","Brand","Model","Notes","CreatedAt","UpdatedAt"],
    "Inspections": ["InspectionID","PropertyID","Date","Technician","FindingsSummary","ActionsTaken","BatteriesReplacedCount","AlarmsReplacedCount","PhotosFolderUrl","ComplianceStatus","NextDueDate","ReportPdfUrl","InvoiceID","CreatedAt","UpdatedAt"],
    "LineItems": ["LineItemID","InvoiceID","Date","Description","Quantity","UnitPrice","Total"],
    "Invoices": ["InvoiceID","ClientID","PropertyID","IssueDate","DueDate","Status","Subtotal","Tax","Total","StripeCheckoutUrl","XeroInvoiceId","Notes","CreatedAt","UpdatedAt"],
    "Events": ["EventID","Type","DateTime","PropertyID","ClientID","Channel","Direction","Subject","Message","RelatedId"],
    "Settings": ["Key","Value","Notes"],
    "Templates": ["Name","DocTemplateId","DriveFolderId","Notes"]
  };
  Object.keys(tabs).forEach(name => {
    var sh = ss.getSheetByName(name) || ss.insertSheet(name);
    sh.clear();
    sh.getRange(1,1,1,tabs[name].length).setValues([tabs[name]]).setFontWeight("bold");
  });
}

function ensureTriggers() {
  const triggers = ScriptApp.getProjectTriggers();
  const exists = triggers.some(t => t.getHandlerFunction() === "renewalReminders");
  if (!exists) ScriptApp.newTrigger("renewalReminders").timeBased().everyDays(1).atHour(9).create();
}
