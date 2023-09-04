frontEndMsgElem = document.getElementById("frontEndMsg")
frotnEndMsgPElem = document.getElementById("frontEndMessage")

function displayError(message) {
    frotnEndMsgPElem.innerText = message
    frontEndMsgElem.style.display = "block"
    setTimeout(() => {
        frontEndMsgElem.style.display = "none"
    }, 2000)
}


document.getElementById("completebtn").addEventListener("click", (e) => {
    e.preventDefault()
    if (document.getElementById("scolor").value === "Open this select menu") {
        displayError("Please choose soil color")
        return;
    }

    if (document.getElementById("sform").value === "Open this select menu") {
        displayError("Please choose soil form")
        return;
    }

    if (document.getElementById("sstructure").value === "Open this select menu") {
        displayError("Please choose soil structure")
        return;
    }

    if (document.getElementById("stexture").value === "Open this select menu") {
        displayError("Please choose soil texture")
        return;
    }

    // if you put text in input box of type "number" it will return "" empty string...
    // so if you put text in "input" of number it return "" empty string..
    if (document.getElementById("sdensity").value.trim().length < 1 ||
        parseInt(document.getElementById("sdensity").value.trim()) < 0) {
        displayError("Invalid bulky density")
        return;
    }

    if (document.getElementById("sporosity").value.trim().length < 1 ||
        parseInt(document.getElementById("sporosity").value.trim()) < 0) {
        displayError("Invalid soil porosity")
        return;
    }

    if (document.getElementById("smoisture").value.trim().length < 1 ||
        parseInt(document.getElementById("smoisture").value.trim()) < 0) {
        displayError("Invalid soil moisture")
        return;
    }

    if (document.getElementById("stemp").value.trim().length < 1 ||
        parseInt(document.getElementById("stemp").value.trim()) < 0) {
        displayError("Invalid soil temperature")
        return;
    }

    if (document.getElementById("sph").value.trim().length < 1 || parseInt(document.getElementById("sph").value.trim()) > 1 ||
        parseInt(document.getElementById("sph").value.trim()) < 0) {
        displayError("Invalid soil pH")
        return;
    }

    if (document.getElementById("sphos").value.trim().length < 1 ||
        parseInt(document.getElementById("sphos").value.trim()) < 0) {
        displayError("Invalid soil phosphorus level")
        return;
    }

    if (document.getElementById("spota").value.trim().length < 1 ||
        parseInt(document.getElementById("spota").value.trim()) < 0) {
        displayError("Invalid soil potassium level")
        return;
    }

    if (document.getElementById("snitr").value.trim().length < 1 ||
        parseInt(document.getElementById("snitr").value.trim()) < 0) {
        displayError("Invalid soil nitrogen level")
        return;
    }

    if (document.getElementById("sorganic").value.trim().length < 1 ||
        parseInt(document.getElementById("sorganic").value.trim()) < 0) {
        displayError("Invalid soil organic level")
        return;
    }

    // evertyhing is goold 
    document.getElementById("addreport").submit()
})