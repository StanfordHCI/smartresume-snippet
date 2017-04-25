BASE_URL = 'https://www.smartresumeonline.com/'

// eventually make functions separate and put in CDN file
function turkGetParam(name, defaultValue ) { 
    var regexS = "[\?&]"+name+"=([^&#]*)"; 
    var regex = new RegExp( regexS ); 
    var tmpURL = window.location.href; 
    var results = regex.exec( tmpURL ); 
    if( results == null ) { 
        return defaultValue; 
    } else { 
        return results[1];    
    } 
}

$(document).ready(function(){
    console.log('here in snippet script');
    // block HIT first
    console.log('body: ', $('body'))
    $('body').append('<div id="cover" style="background-color:#fff; position:fixed; width:100%; height:100%; top:0px; left:0px; z-index:1000;"><h1>Preview Hit</h1></div>');
    var assignmentId = assignmentId || turkGetParam('assignmentId', '');
    var workerId = workerId || turkGetParam('workerId', '');
    console.log('workerId: ' + workerId);
    if (workerId != '') {
        console.log('url to get: ' + BASE_URL + 'guildworkermap/?guild__id=' + PERMITTED_GUILD + '&worker__worker_id=' + workerId)
        // check if worker in guild by doing api request
        $.ajax({
            url: BASE_URL + 'guildworkermap/?guild__id=' + PERMITTED_GUILD + '&worker__worker_id=' + workerId,
            type: 'GET',
            success: function(result) {
                if (result.count == 0) {
                    $('#cover').text("result.length: " + result.length + " result: " + result + " You, assnid: " + assignmentId + " , worker " + workerId + ", are not in one of the qualification guilds required for this HIT. Please click 'Return HIT' to avoid any impact on your approval rating.");
                }
                else {
                    $('#cover').hide()
                }
            }
        });
    }
})


/*

// https://css-tricks.com/multiple-simultaneous-ajax-requests-one-callback-jquery/

$.when(
  // Get the css-tricks once
  for (var i in PERMITTED_GUILDS) {
    $.get(BASE_URL + 'guildworkermap/?guild__id=' + PERMITTED_GUILD + '&worker__worker_id=' + workerId, function(result){
    
    })
  }
).then(function(resp) {
  console.log( resp1, resp2, resp3, resp4 );
  // check if any responses are good and replace HIT text accordingly
});
*/