let formElem = document.getElementById('recommendForm')
let frotnEndMsgPElem = document.getElementById('frontEndMessage')
let frontEndMsgElem = document.getElementById('frontEndMsg')
let previewf = document.getElementById("previewfertivalue")
let previews = document.getElementById("previewseedvalue")
let previewy = document.getElementById("previewoutput")
let submitbtn = document.getElementById("completebtn")

console.log('prevferti ', previewf)


function nionesheError(message) {
    window.scrollTo(0, 0)
    frotnEndMsgPElem.innerText = message
    frontEndMsgElem.style.display = "block"
    setTimeout(() => {
        frontEndMsgElem.style.display = "none"
    }, 2000)
}


function compareTheseArrays(inPreview, inDropdown, code) {
    // Law of Thumb: inDropDown length should be either the same to inPreview array length or greater in length than inPreview array
    if (inPreview.length !== inDropdown.length || inPreview.length > inDropdown.length) {
        let message = ''
        if (code === "fer") {
            message = "Make sure you submitted the total weight of each fertilizer you picked."
        }

        if (code === "seed") {
            message = "Make sure you submitted the number of seed for each crop you picked."
        }

        if (code === "yield") {
            message = "Make sure you submitted the estimated yield amount for each crop you picked"
        }

        nionesheError(message)
        return false;
    }
    else {
        return true;
    }

    for (let data of inPreview) {
        if (!inDropdown.includes(data)) {
            let message = ''
            if (code === "fer") {
                message = "You added weight to fertlizer you never picked."
            }

            if (code === "seed") {
                message = "You added seed number to crop you never picked."
            }

            if (code === "yield") {
                message = "You added output/yield to crop you never picked"
            }
            nionesheError(message)
            return false;
        }
        else {
            return true;
        }
    }

}

function giveMeMetadataObj(target) {
    let val;
    if (target.nextSibling.innerText.includes('KG')) {
        val = parseInt(target.nextSibling.innerText.substr(0, target.nextSibling.innerText.indexOf('K')))
    }
    else {
        val = parseInt(target.nextSibling.innerText.toString())
    }
    return { [target.innerText.trim()]: val }
}

submitbtn.addEventListener('click', e => {
    console.log('someone clicked me!')
    e.preventDefault()
    e.stopPropagation()
    // let's do our validation
    console.log('pass1')
    if (document.getElementById("culttype").value === "Open this select menu") {
        nionesheError(
            "You should provide the cultivation type"
        )
        return
    }

    if (JSON.parse(document.getElementById('fertilizer').value).length < 1) {
        nionesheError(
            "You should pick at least one fertilizer"
        )
        return;
    }

    if (previewf.children.length < 1) {
        nionesheError("Add the individual amount of fertilizer, (total fertilizer weight)")
        return;
    }

    if (JSON.parse(document.getElementById("crop").value).length < 1) {
        nionesheError(
            "You should pick at least one crop"
        )
        return;
    }

    if (previews.children.length < 1) {
        nionesheError("Add the individual total amount of seed")
        return
    }

    if (previewy.children.length < 1) {
        nionesheError("Add the individual estimated yield of crops you recommended")
        return
    }

    // fertilizer validation
    let fertlizerWeightAddedName = []
    let fertilizermetdata = []
    for (let node of Object.values(previewf.children)) {
        for (let span of Object.values(node.children)) {

            if (span.className === "fertilizer-name fst-italici") {
                fertilizermetdata.push(giveMeMetadataObj(span))
                fertlizerWeightAddedName.push(span.innerText)
            }
        }
    }
    let selectedferts = JSON.parse(document.getElementById('fertilizer').value)
    const fertresp = compareTheseArrays(fertlizerWeightAddedName, selectedferts, 'fer')

    // i don't understand this logic, in short i don't know what happen.
    if (!fertresp) {
        return;
    }

    // continue down to seed amount validation..
    // seed validation 

    let seedAmountAdded = []
    let seedamountmetadata = []
    for (let node of Object.values(previews.children)) {
        for (let span of Object.values(node.children)) {
            if (span.className === "seed-name fst-italici") {
                seedamountmetadata.push(giveMeMetadataObj(span))
                seedAmountAdded.push(span.innerText)
            }
        }
    }

    let selectedseeds = JSON.parse(document.getElementById("crop").value)
    const seedresp = compareTheseArrays(seedAmountAdded, selectedseeds, 'seed')

    if (!seedresp) {
        return;
    }

    // end of seed validation

    // yield validation
    let yieldamountAdded = []
    let yieldmetadata = []
    for (let node of Object.values(previewy.children)) {
        for (let span of Object.values(node.children)) {
            if (span.className === "yield-crop-name fst-italici") {

                const metadata = giveMeMetadataObj(span)
                yieldmetadata.push(metadata)
                yieldamountAdded.push(span.innerText)
            }
        }
    }

    let selectedcropstoyield = JSON.parse(document.getElementById("crop").value)
    const yieldresp = compareTheseArrays(yieldamountAdded, selectedcropstoyield, 'yield')
    if (!yieldresp) {
        return;
    }

    // end of yield validation..
    console.log('Now everything is good..')

    console.log(fertilizermetdata, seedamountmetadata, yieldmetadata)
    document.getElementById("seed").value = JSON.stringify(seedamountmetadata)
    document.getElementById("output").value = JSON.stringify(yieldmetadata)
    document.getElementById("fweight").value = JSON.stringify(fertilizermetdata)

    // after that submit the form...
    document.getElementById("recommendForm").submit()
})