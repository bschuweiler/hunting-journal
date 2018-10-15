/**
Builds the form using index.html as the template
**/
function doGet(e) {
  return HtmlService
    .createTemplateFromFile('hunting-journal-form.html')
    .evaluate()
    .setSandboxMode(HtmlService.SandboxMode.NATIVE);
}


/**
Writes form data to the Google Sheet
**/
function writeForm(form) {
  var input = formDataToInputData(form);
  
  if (validateFormData(input)) {
    var ss = SpreadsheetApp.openById('fill-this-in');
    
    writeHunt(ss, input);
    writeHunters(ss, input);

    if (input.birdsList) {
      writeBirds(ss, input);
    }
    
    var returnString = Utilities.formatString('Hunt written: {%s, %s, %s}',
                          input.date, input.timeOfDay, input.location);
    
    return returnString;
  }
  else {
    throw new Error('Missing required field(s)');
  }
}


/**
Converts form data to a normalized input object
**/
function formDataToInputData(form) {
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
  
  var input = {};
  input.date = form.date;
  input.timeOfDay = form.timeOfDay;
  input.location = form.location;
  input.huntersList = normalizeFormArrayField(form.hunters);
  
  input.birdsList = normalizeFormArrayField(form.birds);
  input.gendersList = normalizeFormArrayField(form.genders);
  input.lostList = normalizeFormArrayField(form.lost);
  input.bandedList = normalizeFormArrayField(form.banded);
  input.mountedList = normalizeFormArrayField(form.mounted);
  
  return input;
}


/**
Normalizes array fields from the form
**/
function normalizeFormArrayField(field) {
  return (typeof(field) == "undefined" || (Array.isArray(field)) ? field : [field]);
}


/**
Validates the input data for required fields
**/
function validateFormData(input) {
  if (input.date
      && input.timeOfDay
      && input.location
      && input.huntersList) {
    return true;
  }
  return false;
}


/**
Writes hunt row to the 'Hunts' sheet of the Google Sheet
**/
function writeHunt(spreadsheet, input) {
  var sheet = spreadsheet.getSheetByName('Hunts');
  
  var originalLastRow = sheet.getLastRow();
  var newRow = originalLastRow + 1;
  var numRows = 1; var column = 1; var numColumns = 3;
  var writeRange = sheet.getRange(newRow, column, numRows, numColumns);
  
  // setValues takes multi-dimensional array
  // (first dimension is rows, second is columns)
  var values = [[input.date, input.location, input.timeOfDay]];
  writeRange.setValues(values);
  
  // fill down the calc'd cells from previous last row
  var sourceRange = sheet.getRange(originalLastRow, 4, 1, 5);
  var targetRange = sheet.getRange(newRow, 4, 1, 5);
  sourceRange.copyTo(targetRange);
  
  // Set the 'Written by Script' column for posterity
  var scriptIndicatorRange = sheet.getRange(newRow, 9, 1, 1);
  scriptIndicatorRange.setValue("TRUE");
}


/**
Writes hunters rows to the 'Hunters' sheet of the Google Sheet
**/
function writeHunters(spreadsheet, input) {
  var sheet = spreadsheet.getSheetByName('Hunters');
  for each (var hunter in input.huntersList) {
    var originalLastRow = sheet.getLastRow();
    var newRow = originalLastRow + 1;
    var numRows = 1; var column = 1; var numColumns = 4;
    var writeRange = sheet.getRange(newRow, column, numRows, numColumns); 
    
    // setValues takes multi-dimensional array
    // (first dimension is rows, second is columns)
    var values = [[input.date, input.location, input.timeOfDay, hunter]];
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


/**
Writes bird rows to the 'Birds' sheet of the Google Sheet
**/
function writeBirds(spreadsheet, input) {
  var sheet = spreadsheet.getSheetByName('Birds');
  for (var index in input.birdsList) {
    var originalLastRow = sheet.getLastRow();
    var newRow = originalLastRow + 1;
    var numRows = 1; var column = 1; var numColumns = 8;
    var writeRange = sheet.getRange(newRow, column, numRows, numColumns); 
    
    // setValues takes multi-dimensional array
    // (first dimension is rows, second is columns)
    var values = [[input.date, input.location, input.timeOfDay,
                   input.birdsList[index], input.gendersList[index],
                   input.bandedList[index], input.lostList[index],
                   input.mountedList[index]]];
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