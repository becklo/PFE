function show() {

    var carId,ParkingName,Date,interest, payload, interestList = "";
    carId = document.forms["form1"]["carId"].value;
    ParkingName = document.forms["form1"]["ParkingName"].value;
    Date = document.forms["form1"]["Date"].value;
    interest = document.forms["form1"].elements["service"];
    for(var i =0;i<interest.length;i++){
        if(interest[i].checked){
            interestList += "\"" + interest[i].value + "\",";
        }
    }
    interestList = interestList.substring(0, interestList.length - 1);
    console.log(" carId " + carId + " Parking : " + ParkingName + " Date : " + Date + " interest : " + interestList);
    payload = "{" +
        "\"carId\" : \"" + carId + "\"," +
        "\"ParkingName\" : \"" + ParkingName + "\"," +
        "\"Date\" : \"" + Date + "\"," +
        "\"interest\" : [" + interestList + "]" +
        "}";

    post(4,payload);

    document.getElementById("form1").submit();

}

