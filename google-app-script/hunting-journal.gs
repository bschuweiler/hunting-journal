//basic function that builds the form using index.html as the template
function doGet(e) {
  return HtmlService
    .createTemplateFromFile('hunting-journal-form.html')
    .evaluate()
    .setSandboxMode(HtmlService.SandboxMode.NATIVE);
}
 
function writeForm(form) {
  /**
  Example form data coming in:
  {date=10/10/2018,
  timeOfDay=Afternoon,
  location=Heart Island,
  banded=[FALSE, FALSE],
  gender=[Drake, Drake],
  birds=[Ring-necked Duck, Ring-necked Duck],
  lost=[FALSE, FALSE],
  hunters=Steve,
  mounted=[FALSE, FALSE]}
  **/
  
  var date = form.date;
  var timeOfDay = form.timeOfDay;
  var location = form.location;
  var huntersList = form.hunters;
  var birdsList = form.birds;
  var gendersList = form.genders;
  var lostList = form.lost;
  var bandedList = form.banded;
  var mountedList = form.mounted;
  
  var ss = SpreadsheetApp.openById('1OgFlebGdUybZj5ISZn-uCLbJMkDPMNN9dQsM78u09sI');
  
  writeHunt(ss, date, location, timeOfDay);
  writeHunters(ss, date, location, timeOfDay, huntersList);  
  writeBirds(ss, date, location, timeOfDay, birdsList, gendersList, lostList, bandedList, mountedList);
  
  var returnString = 'Hunt written: {'
  + date + ', '
  + timeOfDay + ', '
  + location + ', '
  + huntersList.length + ' hunters, '
  + birdsList.length + ' birds'
  + '}';
  
  return returnString;
}

function writeHunt(spreadsheet, date, location, timeOfDay) {
  var sheet = spreadsheet.getSheetByName('Hunts');
  
  var originalLastRow = sheet.getLastRow();
  var newRow = originalLastRow + 1;
  var numRows = 1; var column = 1; var numColumns = 3;
  var writeRange = sheet.getRange(newRow, column, numRows, numColumns);
  
  // setValues takes multi-dimensional array
  // (first dimension is rows, second is columns)
  var values = [[date, location, timeOfDay]];
  writeRange.setValues(values);
  
  // fill down the calc'd cells from previous last row
  var sourceRange = sheet.getRange(originalLastRow, 4, 1, 5);
  var targetRange = sheet.getRange(newRow, 4, 1, 5);
  sourceRange.copyTo(targetRange);
  
  // Set the 'Written by Script' column for posterity
  var scriptIndicatorRange = sheet.getRange(newRow, 9, 1, 1);
  scriptIndicatorRange.setValue("TRUE");
}

function writeHunters(spreadsheet, date, location, timeOfDay, huntersList) {
  var sheet = spreadsheet.getSheetByName('Hunters');
  for each (var hunter in huntersList) {
    var originalLastRow = sheet.getLastRow();
    var newRow = originalLastRow + 1;
    var numRows = 1; var column = 1; var numColumns = 4;
    var writeRange = sheet.getRange(newRow, column, numRows, numColumns); 
    
    // setValues takes multi-dimensional array
    // (first dimension is rows, second is columns)
    var values = [[date, location, timeOfDay, hunter]];
    writeRange.setValues(values);
    
    // fill down the calc'd cells from previous last row
    var sourceRange = sheet.getRange(originalLastRow, 5, 1, 5);
    var targetRange = sheet.getRange(newRow, 5, 1, 5);
    sourceRange.copyTo(targetRange);
    
    // Set the 'Written by Script' column for posterity
    var scriptIndicatorRange = sheet.getRange(newRow, 10, 1, 1);
    scriptIndicatorRange.setValue("TRUE");
  }
}

function writeBirds(spreadsheet, date, location, timeOfDay, birdsList, gendersList, lostList, bandedList, mountedList) {
  var sheet = spreadsheet.getSheetByName('Birds');
  for (var index in birdsList) {
    var originalLastRow = sheet.getLastRow();
    var newRow = originalLastRow + 1;
    var numRows = 1; var column = 1; var numColumns = 8;
    var writeRange = sheet.getRange(newRow, column, numRows, numColumns); 
    
    // setValues takes multi-dimensional array
    // (first dimension is rows, second is columns)
    var values = [[date, location, timeOfDay, birdsList[index], gendersList[index], bandedList[index], lostList[index], mountedList[index]]];
    writeRange.setValues(values);
    
    // fill down the calc'd cells from previous last row
    var sourceRange = sheet.getRange(originalLastRow, 9, 1, 5);
    var targetRange = sheet.getRange(newRow, 9, 1, 5);
    sourceRange.copyTo(targetRange);
    
    // Set the 'Written by Script' column for posterity
    var scriptIndicatorRange = sheet.getRange(newRow, 14, 1, 1);
    scriptIndicatorRange.setValue("TRUE");
  }
}