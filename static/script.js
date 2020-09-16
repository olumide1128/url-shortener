

function myFunction() {
	document.getElementById("info").innerHTML = "Your Shortend URL has been copied!";
	document.getElementById("icon").style.display = "inline";
	var copyText = document.getElementById("shorturl");
	copyText.select();
	copyText.setSelectionRange(0, 99999);
	document.execCommand("copy");
  
}

function showMsg(msg){
	document.getElementById("alert").style.display = "block";
	document.getElementById("alert").innerHTML = msg;
}

function validate(){
	var x = document.forms["myform"]["url"].value;
    if (x == null || x == "") {
        showMsg("You must enter a URL!");
        return false;
    }

    else if(x !== "" && !x.match(/^(www\.|http:\/\/|https:\/\/)[A-Za-z0-9\._\-]+[\.][A-Za-z]{2,4}$/)){
    	showMsg("Please Enter a valid URL!");
    	return false;
    }
}



