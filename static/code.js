var tipsHintsElement = document.getElementById("tips-hints"),
    tipsHintsVisible = true;


function toggleTipsHints() {
    if (tipsHintsVisible)
        tipsHintsElement.style = "display: none";
    else
        tipsHintsElement.style = "";

    tipsHintsVisible = !tipsHintsVisible;

    return false;
}

var codeElement = document.getElementById("code");
codeElement.addEventListener("keypress", execute);
codeElement.focus();


function execute(e) {
    if (e !== undefined && !e.ctrlKey)
        return;  
    var code = codeElement.value;
    
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
    xhr.send(code);
    return false;
}
