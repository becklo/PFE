// Install thingspeak client or include in your package.json
// npm install thingspeakclient


var thingspeakclient = require("thingspeakclient");
var client = new thingspeakclient({});


var yourWriteKey = 'YIWBEMNVPZ1XKN6Z';
var channelID = 472117;


client.attachChannel(channelID, { writeKey:'yourWriteKey'}, callBackThingspeak);


client.updateChannel(channelID, {field1: 7}, function(err, resp) {
    if (!err && resp > 0) {
        console.log('update successfully. Entry number was: ' + resp);
    }
    else {
        console.log(err);
    }
});



function callBackThingspeak(err, resp)
{
    if (!err && resp > 0) {
        console.log('Successfully. response was: ' + resp);
    }
    else {
        console.log(err);
    }
}