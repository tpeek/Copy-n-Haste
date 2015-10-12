var opponent = $("#opponent").val();
var secs = 0;
var toType = document.getElementById("type").value;
var strToTest = $("type").val();
var strToTestType = "";
var done = false;
var checkStatusInt;

//General functions to allow for left and right trimming / selection of a string
function Left(str, n){
 if (n <= 0)
     return "";
 else if (n > String(str).length)
     return str;
 else
     return String(str).substring(0,n);
}
function Right(str, n){
    if (n <= 0)
       return "";
    else if (n > String(str).length)
       return str;
    else {
       var iLen = String(str).length;
       return String(str).substring(iLen, iLen - n);
    }
}
var intervalID;
//beginTest Function/Sub initializes the test and starts
//the timers to determine the WPM and Accuracy
function beginTest()
{
 //Generate a date value for the current time as a baseline
 day = new Date();

 //Count the number of valid words in the testing baseline string
 cnt = strToTestType.split(" ").length;

 //Set the total word count to the number of valid words that need to be typed
 word = cnt;

 //Set the exact time of day that the testing has started
 startType = day.getTime();

 calcStat();

 //Apply focus to the text box the user will type the test into
 $("#typed").focus();

  if (opponent == "computer") {
   intervalID = window.setInterval(function(){
      var foe = document.getElementById("typed2");
      foe.value += String($('#type').val()).charAt(secs);
      secs += 1;
   }, 500);
  }
}
beginTest();

// This function/sub is responsible for calculating
// the accuracy, and setting post-test variables
function endTest()
{

  window.clearInterval(intervalID)
 //Clear the timer that tracks the progress of the test, since it's complete
 clearTimeout(checkStatusInt);

 //Disable the area where the user types the test input
 $("#typed").attr("disabled", "disabled");

 //Initialize an object with the current date/time
 //so we can calculate the difference
 eDay = new Date();
 endType = eDay.getTime();
 totalTime = ((endType - startType) / 1000)

 //Calculate the typing speed by taking the number of valid words
 //typed by the total time taken and multiplying it by one minute in seconds (60)
 wpmType = Math.round((($("#typed").val().split(" ").length)/totalTime) * 60);

 //Declare an array of valid words for what NEEDED to be typed and what WAS typed
 //Again, refer to the above statement on removing the double spaces globally (1A)
 var typedValues = $("#typed").val();
 var neededValues = Left($("#type").val(), typedValues.length).split(" ");
 typedValues = typedValues.split(" ");

 //Declare variable references to various statistical layers
 var tErr = document.getElementById("stat_errors");
 var tscore = document.getElementById("stat_score");
 var tStat = document.getElementById("stat_wpm");
 var tTT = document.getElementById("stat_timeleft");

 //Initialize the counting variables for the good valid words and the bad valid words
 var goodWords = 0;
 var badWords = 0;

 //Declare a variable to hold the error words we found
 var errWords = "";

 //Loop through the valid words that were possible
 //(those in the test baseline of needing to be typed)
 for (var i = 0; i < word; i++)
 {
  //If there is a word the user typed that is
  //in the spot of the expected word, process it
  if (typedValues.length > i)
  {
   //Declare the word we expect, and the word we recieved
   var neededWord = neededValues[i];
   var typedWord = typedValues[i];

   //Determine if the user typed the correct word or incorrect
   if (typedWord != neededWord)
   {
    //They typed it incorrectly, so increment the bad words counter
    badWords = badWords + 1;
    errWords += typedWord + " = " + neededWord + "\n";
   }
   else
   {
    //They typed it correctly, so increment the good words counter
    goodWords = goodWords + 1;
   }
  }
  tscore.innerText = ((goodWords / (goodWords+badWords)) * 100).toFixed(2) + "%";
 }

 //Set the statistical label variables with what
 //we found (errors, words per minute, time taken, etc)
 tErr.innerText = badWords + " Errors";
 tStat.innerText = (wpmType-badWords) + " WPM / " + wpmType + " WPM";
 tTT.innerText = totalTime.toFixed(2) + " sec. elapsed"

 //Calculate the accuracy score based on good words typed
 //versus total expected words -- and only show the percentage as ###.##
 tscore.innerText = ((goodWords / (goodWords+badWords)) * 100).toFixed(2) + "%";

if (done == false) {
 $.ajax({
   method : "POST",
    url : "/play/report_results/",
    data : {"wpm_gross": wpmType,
            "wpm_net": wpmType-badWords,
            "mistakes": badWords,
            "opponent": opponent}
  }).done(function(response){
    done = true;
    window.location.href = "http://" + window.location.host + response;
  }).fail(function(){
      alert("fail");
  });
}
}

//calcStat is a function called as the user types
//to dynamically update the statistical information
function calcStat()
{
//If something goes wrong, we don't want to cancel the test -- so fallback
//error proection (in a way, just standard error handling)
try {
 //Reset the timer to fire the statistical update function again in 250ms
 //We do this here so that if the test has ended (below) we can cancel and stop it
 checkStatusInt=setTimeout('calcStat();',250);

 //Declare reference variables to the statistical information labels
 var tStat = document.getElementById("stat_wpm");
 var tTT = document.getElementById("stat_timeleft");

 //Refer to 1A (above) for details on why we are removing the double space
 var thisTyped = $("#typed").val();

 //Create a temp variable with the current time of day to calculate the WPM
 eDay = new Date();
 endType = eDay.getTime();
 totalTime = ((endType - startType) / 1000)
 //Calculate the typing speed by taking the number of valid words
 //typed by the total time taken and multiplying it by one minute in seconds (60)
 wpmType = Math.round(((thisTyped.split(" ").length)/totalTime) * 60)


 //Set the words per minute variable on the statistical information block
 tStat.innerText = wpmType + " WPM";


 //Calculate and show the time taken to reach this point
 //of the test and also the remaining time left in the test
 //Colorize it based on the time left (red if less
 //than 5 seconds, orange if less than 15)
 if (Number(60-totalTime) < 5)
 {
  tTT.innerHTML="<font color=\"Red\">" + String(totalTime.toFixed(2)) +
                " sec. / " + String(Number(60-totalTime).toFixed(2)) +
                " sec.</font>";
 }
 else
 {
  if (Number(60-totalTime) < 15)
  {
   tTT.innerHTML="<font color=\"Orange\">" +
                 String(totalTime.toFixed(2)) + " sec. / " +
                 String(Number(60-totalTime).toFixed(2)) + " sec.</font>";
  }
  else
  {
   tTT.innerHTML=String(totalTime.toFixed(2)) + " sec. / " +
                 String(Number(60-totalTime).toFixed(2)) + " sec.";
  }
 }

 //Check the timer; stop the test if we are at or exceeded 60 seconds
 if (totalTime >= 6)
 {
  endTest();
 }
//Our handy error handling
} catch(e){alert(e)};
}


$(document).delegate('#typed', 'keydown', function(e) {
  calcStat();
  var keyCode = e.keyCode || e.which;

  if (keyCode == 9) {
    e.preventDefault();
    var start = $(this).get(0).selectionStart;
    var end = $(this).get(0).selectionEnd;

    // set textarea value to: text before caret + tab + text after caret
    $(this).val($(this).val().substring(0, start)
                + "\t"
                + $(this).val().substring(end));

    // put caret at right position again
    $(this).get(0).selectionStart =
    $(this).get(0).selectionEnd = start + 1;
  }
  if (opponent != 'computer') {
    $.ajax({
      method : "POST",
      url : "/play/multi/",
      data : {"user_input": $('#typed').val(),
              "opponent": opponent}
    }).done(function(response){
      $('#typed2').val(response)
    }).fail(function(){
      alert("fail");
    });
  }
});