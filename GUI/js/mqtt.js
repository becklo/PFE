var mqtt ;
var host="192.168.0.107"; //change this mqtt.thingspeak.com
var port=9001; // 80
var channel="472117";
var API_key="EYNVO9MB25DIYJFQ";
var fieldNum="2";

function onMessage(r_message) {
    var out_msg = r_message.payloadString;

    jsonObj = JSON.parse(out_msg);
    console.log(jsonObj);
    console.log(jsonObj.serviceTest);
    // if (jsonObj.color === "Red"){
    //     document.getElementById("messageRed").innerHTML = jsonObj.lightStatus;
    //     document.getElementById("messageRedReceived").innerHTML = jsonObj.payload;
    // }
    // if (jsonObj.color === "Green"){
    //     document.getElementById("messageGreen").innerHTML = jsonObj.lightStatus;
    //     document.getElementById("messageGreenReceived").innerHTML = jsonObj.payload;
    // }
    // if (jsonObj.color === "Blue"){
    //     document.getElementById("messageBlue").innerHTML = jsonObj.lightStatus;
    //     document.getElementById("messageBlueReceived").innerHTML = jsonObj.payload;
    // }
    if (jsonObj.serviceTest === "Traffic"){
        document.getElementById("messageTraffic").innerHTML = jsonObj.serviceStatus;
        document.getElementById("messageTrafficReceived").innerHTML = jsonObj.payload;
    }
    if (jsonObj.serviceTest === "Cloud"){
        document.getElementById("messageCloud").innerHTML = jsonObj.serviceStatus;
        document.getElementById("messageCloudReceived").innerHTML = jsonObj.payload;
    }
    if (jsonObj.serviceTest === "Weather"){
        document.getElementById("messageWeather").innerHTML = jsonObj.serviceStatus;
        document.getElementById("messageWeatherReceivedFrom").innerHTML = jsonObj.payload;//["From"];
        // document.getElementById("messageWeatherReceivedData").innerHTML = jsonObj.payload["Data"];
    }
    if (jsonObj.serviceTest === "GPS"){
        document.getElementById("messageGPS").innerHTML = jsonObj.serviceStatus;
        document.getElementById("messageGPSReceived").innerHTML = jsonObj.payload;
    }
    if (jsonObj.serviceTest === "SensorData"){
        document.getElementById("messageSensor").innerHTML = jsonObj.serviceStatus;
        document.getElementById("messageSensorReceivedFrom").innerHTML = jsonObj.payload;//["From"];
        // document.getElementById("messageSensorReceivedData").innerHTML = jsonObj.payload["Data"];
    }
    if (jsonObj.serviceTest === "BLE"){
        document.getElementById("messageBLE").innerHTML = jsonObj.serviceStatus;
        document.getElementById("messageBLEReceived").innerHTML = jsonObj.payload;
    }
    if (jsonObj.serviceTest === "Translator"){
        document.getElementById("messageTranslator").innerHTML = jsonObj.serviceStatus;
        document.getElementById("messageTranslatorReceived").innerHTML = jsonObj.payload;
    }

    return false;
}


function onConnect() {
    // Once a connection has been made, make a subscription and send a message.

    var subOptions = {
        onSuccess: success,
        onFailure: failureSub,
        timeout: 10
    };
    var topic_sub = "channels/"+channel+"/subscribe/fields/field"+fieldNum+"/"+API_key;
    console.log(topic_sub);
    mqtt.subscribe(topic_sub,subOptions);
    console.log("Connected ");
    return false;
}


function success() {
    console.log("sub success");
    return false;
}

function failureSub() {
    console.log("sub fail");
    return false;
}

function failure() {
    console.log("fail");
    return false;
}

function MQTTconnect() {
    console.log("connecting to "+ host +" "+ port);
    mqtt = new Paho.MQTT.Client(host, port, "clientjsTS");
    var username = "loulabeckses"+ Math.random().toString(36).substring(2,7);
    console.log(username);
    var options = {
        // useSSL:true,
        timeout: 3,
        onSuccess: onConnect,
        onFailure: failure,
        userName: "loraroot",//"loulabckses",
        password: "root"//"D8ZQSQ59YDSSLDBE"
    };

    mqtt.onMessageArrived = onMessage;
    mqtt.connect(options); //connect
}

// function MQTTconnectGreen() {
//     console.log("connecting to "+ host +" "+ port);
//     mqttGreen = new Paho.MQTT.Client(host,port,"clientjs");
//     //document.write("connecting to "+ host);
//     var options = {
//         //useSSL:true,
//         timeout: 3,
//         onSuccess: onConnectGreen,
//         userName: "loula.beck@ses.com",
//         password: "D8ZQSQ59YDSSLDBE"
//     };
//
//     mqttGreen.onMessageArrived = onMessageGreen;
//     mqttGreen.connect(options); //connect
// }
//
// function MQTTconnectBlue() {
//     console.log("connecting to "+ host +" "+ port);
//     mqttBlue = new Paho.MQTT.Client(host,port,"clientjs");
//     //document.write("connecting to "+ host);
//     var options = {
//         //useSSL:true,
//         timeout: 3,
//         onSuccess: onConnectBlue,
//         userName: "loula.beck@ses.com",
//         password: "D8ZQSQ59YDSSLDBE"
//     };
//
//     mqttBlue.onMessageArrived = onMessageBlue;
//     mqttBlue.connect(options); //connect
// }

