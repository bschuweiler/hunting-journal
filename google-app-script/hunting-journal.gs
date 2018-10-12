//basic function that builds the form using index.html as the template
function doGet(e) {
  return HtmlService
    .createTemplateFromFile('hunting-journal-form.html')
    .evaluate()
    .setSandboxMode(HtmlService.SandboxMode.NATIVE);
}
 
function writeHunt(form) {
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
  
  try {  
    var date = form.date;
    var timeOfDay = form.timeOfDay;
    var location = form.location;
    var birdsList = form.birds;
    var huntersList = form.hunters;
    var lostList = form.lost;
    var bandedList = form.banded;
    var mountedList = form.mounted;
    
    /*var ss = SpreadsheetApp.openById('1OgFlebGdUybZj5ISZn-uCLbJMkDPMNN9dQsM78u09sI');
    var sheet = ss.getSheetByName('Hunters');
    var newRow = sheet.getLastRow() + 1;//go to the first blank row           
    
    //writes the form data to the spreadsheet
    var range = sheet.getRange(newRow, 3);    
    range.setValue(timeOfDay);*/
    
    var returnString = 'Hunt written: {'
      + date + ', '
      + timeOfDay + ', '
      + location + ', '
      + huntersList.length + ' hunters, '
      + birdsList.length + ' birds, '
      + '}';
    
    return returnString;
  } 
  catch (error) { 
    return error.toString();
  }
}