function getSheet_(name) { return SpreadsheetApp.getActive().getSheetByName(name); }

function getSettings_() {
  const sh = getSheet_("Settings");
  const values = sh.getRange(2,1,Math.max(sh.getLastRow()-1,0),2).getValues();
  const map = {};
  values.forEach(r => { if (r[0]) map[r[0]] = r[1]; });
  return map;
}

function todayStr_() { return Utilities.formatDate(new Date(), Session.getScriptTimeZone(), "yyyy-MM-dd"); }

function uid_(prefix) { return prefix + "-" + Utilities.getUuid().slice(0,8).toUpperCase(); }

function findRowByValue_(sheetName, colIdx, value) {
  const sh = getSheet_(sheetName);
  const rng = sh.getRange(2, colIdx, Math.max(sh.getLastRow()-1, 0), 1).getValues();
  for (var i=0;i<rng.length;i++) if (String(rng[i][0]).trim() === String(value).trim()) return i+2;
  return -1;
}

function sendEmail_(to, subject, body, attachments) {
  const options = attachments ? {attachments: attachments} : {};
  GmailApp.sendEmail(to, subject, body, options);
}
