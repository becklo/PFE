function submitRequest(fieldNumber,value){
    post(fieldNumber,value);
    disableButton(["clickmeTruck","clickmeCloud","clickmeWeather","clickmeSensor","clickmeGPS","clickmeBLE",
        "killmeTruck","killmeCloud","killmeWeather","killmeSensor","killmeGPS","killmeBLE"
        ]);
//"clickmeTranslator" "killmeTranslator" "clickmeAll", "killmeAll"
}

function disableButton(listId){
    var listL = listId.length;
    for (let i=0; i<listL; i++){
        document.getElementById(listId[i]).disabled = "disabled";
        document.getElementById(listId[i]).innerHTML = "Disabled";
        setTimeout(function(){
            document.getElementById(listId[i]).disabled = "";
            document.getElementById(listId[i]).innerHTML = "Change Red light";
        },16000);
    }

}