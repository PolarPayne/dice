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

var codeElement = document.getElementById("code"),
    outElement = document.getElementById("out"),
    outUlElement = document.getElementById("out-ul"),
    errorsElement = document.getElementById("errors"),
    errorsUlElement = document.getElementById("errors-ul"),
    warningsElement = document.getElementById("warnings"),
    warningsUlElement = document.getElementById("warnings-ul"),
    genericError = "Something went wrong while doing the request.";

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
        if(xhr.readyState === XMLHttpRequest.DONE && xhr.status == 200) {
            if (xhr.getResponseHeader("Content-type") !== "application/json" || xhr.responseText === null) {
                window.alert(genericError);
                return;  // failure
            }
            var data = JSON.parse(xhr.responseText);
            console.log(data);
            
            function appendAllToElement(element, list) {
                var li = null;
                element.innerHTML = "";
                for (var i = 0; i < list.length; i++) {
                    li = document.createElement("li");
                    li.innerText = list[i];
                    element.appendChild(li);
                }
            }

            appendAllToElement(outUlElement, data.out);
            appendAllToElement(errorsUlElement, data.errors);
            appendAllToElement(warningsUlElement, data.warnings);
            
            return;
        }

    }
    xhr.send(code);
    return false;
}
