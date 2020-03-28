function showPrompt(){
    var result = window.prompt("Input something", "");

    if( result == null ){
        window.alert("Canceled");
    }else{
        window.alert("Done : " + result);
    }
}