function onEdit(e) {
  var sheet = e.source.getActiveSheet();
  var range = e.range;


  if (sheet.getName() === 'Sheet1' && range.getColumn() === 6 && range.getRow() > 1) {
    var row = range.getRow();
    var dataRange = sheet.getRange(row, 1, 1, 7);
    var rowData = dataRange.getValues()[0];

    var url = '127.0.0.1:8000/api/gs/changed';
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
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyIiwiZXhwIjoxNzM3NzMwNjQ0fQ.HWGioY_TVmykcfstgQsm_H6YjriAoMwWC2ISTWho6gE'
      },
      'payload': JSON.stringify(payload)
    };


    var response = UrlFetchApp.fetch(url, options);

  }
}
