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
    executeButton = document.getElementById("execute-button"),
    outUlElement = document.getElementById("out-ul"),
    errorsUlElement = document.getElementById("errors-ul");

codeElement.addEventListener("keypress", execute);
codeElement.focus();


function execute(e) {
    // allow user to execute with ctrl + enter
    // only allow to execute once the previous one is complete
    if ((e !== undefined && !e.ctrlKey) || executeButton.disabled)
        return;


    var code = codeElement.value;

    document.body.style = "cursor: wait;";
    executeButton.disabled = true;
    executeButton.textContent = "Executing...";

    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/", true);
    xhr.setRequestHeader("Content-type", "text/plain");
    xhr.onreadystatechange = function() {
        if (xhr.readyState !== XMLHttpRequest.DONE) {
            return;
        }

        document.body.style = "";
        executeButton.disabled = false;
        executeButton.textContent = "Execute";

        if (xhr.status == 500) {
            return window.alert(
                "The server encountered an error parsing the input.\n" +
                "Sorry about that..."
            );
        } else if (xhr.status == 200) {
            if (xhr.getResponseHeader("Content-type") !== "application/json" || xhr.responseText === null) {
                return;  // failure
            }
            var data = JSON.parse(xhr.responseText);

            function appendAllToElement(element, list) {
                var li = null;
                while (element.firstChild)
                    element.removeChild(element.firstChild);

                for (var i = 0; i < list.length; i++) {
                    li = document.createElement("li");
                    li.innerText = list[i];
                    element.appendChild(li);
                }
            }

            appendAllToElement(outUlElement, data.out);
            appendAllToElement(errorsUlElement, data.errors);

            return;
        }
    }
    xhr.send(code);
    return false;
}
