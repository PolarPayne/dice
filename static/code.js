var codeElement = document.getElementById("code");
codeElement.addEventListener("keypress", execute);
codeElement.focus();

function toggleTipsHints() {
    console.log("toggle tips and hints section");
    return false;
}

function execute(e) {
    if (e !== undefined && !e.ctrlKey)
        return;  
    var code = codeElement.value;
    console.log(code);

    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/", true);
    xhr.setRequestHeader("Content-type", "text/plain");
    xhr.onreadystatechange = function() {
        if(xhr.readyState == XMLHttpRequest.DONE && xhr.status == 200) {
            if (xhr.getResponseHeader("Content-type") !== "application/json" || xhr.responseText === null) {
                return;  // failure
            }
            var data = JSON.parse(xhr.responseText);
            console.log(data);
        }
    }

    // xhr.send("foo=bar&lorem=ipsum"); 
    xhr.send(code); 
    // xhr.send(new Blob()); 
    // xhr.send(new Int8Array()); 
    // xhr.send({ form: 'data' }); 
    // xhr.send(document);

    return false;
}
