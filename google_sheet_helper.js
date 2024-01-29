var API_URL = 'http://127.0.0.1:8000/api/gs/changed';
var AUTH_TOKEN = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyIiwiZXhwIjoxNzM3NzMwNjQ0fQ.HWGioY_TVmykcfstgQsm_H6YjriAoMwWC2ISTWho6gE';
var TARGET_COLUMN = 7;
var VALID_STATUSES = ['contact', 'declined', 'dnm'];

function onEdit(e) {
  var range = e.range;
  var sheet = range.getSheet();
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
          'Authorization': AUTH_TOKEN
        },
        'payload': JSON.stringify(payload)
      };


      var response = UrlFetchApp.fetch(API_URL, options);
    }
  }
}