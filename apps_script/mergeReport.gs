function generateReportPdf_(data, templateId) {
  const templateFile = DriveApp.getFileById(templateId);
  const parentId = templateFile.getParents().hasNext() ? templateFile.getParents().next().getId() : DriveApp.getRootFolder().getId();
  const tmpDoc = templateFile.makeCopy("TMP_" + (data.INSPECTION_ID || uid_("I")), DriveApp.getFolderById(parentId));
  const doc = DocumentApp.openById(tmpDoc.getId());
  const body = doc.getBody();
  Object.keys(data).forEach(k => body.replaceText("{{" + k + "}}", String(data[k] ?? "")));
  doc.saveAndClose();
  const pdf = DriveApp.getFileById(tmpDoc.getId()).getAs("application/pdf");
  DriveApp.getFileById(tmpDoc.getId()).setTrashed(true);
  return pdf;
}
