function post(fieldNumber,value) {
    var http = new XMLHttpRequest();
    var url = "https://api.thingspeak.com/update.json";
    var params = "api_key=YIWBEMNVPZ1XKN6Z&field"+fieldNumber+"="+value;
    http.open("POST", url, true);

//Send the proper header information along with the request
    http.setRequestHeader("Content-type", "application/x-www-form-urlencoded");

    http.onreadystatechange = function() {//Call a function when the state changes.
        if(http.readyState == 4 && http.status == 200) {
            alert(http.responseText);
        }
    }
    http.send(params);
    return false
}

