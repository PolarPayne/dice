document.getElementById("code").addEventListener("keypress", execute);

function execute(e) {
    if (e !== undefined && !e.ctrlKey)
        return;  
    var code = document.getElementById("code").value;
    console.log(code);

    return false;
}
