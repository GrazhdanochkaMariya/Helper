var API_URL = 'https://lead-gen-ext.andersenlab.dev/api/gs/changed';
var AUTH_TOKEN = '<paste_your_token_here>';
var AUTH_TOKEN_WITH_BEARER = 'Bearer ' + AUTH_TOKEN;
var TARGET_COLUMN = 7;
var VALID_STATUSES = ['contact', 'declined', 'dnm'];

function onEdit() {
  var sheet = SpreadsheetApp.getActiveSheet();
  var range = sheet.getActiveRange();
  var column = range.getColumn();
  var value = range.getValue().toLowerCase();

  if (column === TARGET_COLUMN) {
    var status = value.toLowerCase();
    if (VALID_STATUSES.includes(status)) {
      var row = range.getRow();
      var dataRange = sheet.getRange(row, 1, 1, 8);
      var rowData = dataRange.getValues()[0];

      var payload = {
        'lead_name': rowData[0],
        'linkedin_profile': rowData[1],
        'next_contact': rowData[7],
        'status': rowData[6]
      };


      var options = {
        'method': 'post',
        'contentType': 'application/json',
        'headers': {
          'Authorization': AUTH_TOKEN_WITH_BEARER
        },
        'payload': JSON.stringify(payload)
      };


      var response = UrlFetchApp.fetch(API_URL, options);
    }
  }
}