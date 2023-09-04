// executing Fertilizer add weight logics...
let label = document.getElementById("defaultLabelfertilizer")
let seed_label = document.getElementById("defaultLabelseed")
let yield_label = document.getElementById("defaultLabelyield")

let seedInput = document.getElementById('idadiyambegu')
let yieldInput = document.getElementById('estimatedoutput')
let fertiInput = document.getElementById("uzito")

let ferterrcont = document.getElementById("fertamounterror")
let seederrcont = document.getElementById("seedamounterror")
let yielderrcont = document.getElementById("yieldamounterr")

let yieldbtn = document.getElementById("addyield")
let fertaddbtn = document.getElementById("addamountfert")
let seedaddbtn = document.getElementById("addamountseed")

let previewferti = document.getElementById("previewfertivalue")
let previewseed = document.getElementById("previewseedvalue")
let previewyield = document.getElementById("previewoutput")


let errorMessage;


function displayError(errorMessage, errorContainer, input) {
    errorContainer.innerText = errorMessage
    errorContainer.style.display = 'block'
    input.value = ""

    setTimeout(() => {
        errorContainer.style.display = "none"
    }, 3000)
}

function addtoPreviewYield(label, valueinput, previewContainer) {
    spans = document.getElementsByClassName("yield-crop-name")

    for (let span of spans) {
        if (span.innerText.trim().toString() === label.innerText.trim().toString()) {
            span.nextSibling.innerText = `${(parseInt(valueinput.value.trim()) * 120).toString()}KG`
            valueinput.value = ""
            return;
        }
    }

    let holderDiv = document.createElement('div')
    holderDiv.className = "mx-2 yieldvalue-holder"
    holderDiv.style.display = 'flex'
    holderDiv.style.alignItems = 'center'

    let titleSpan = document.createElement('span')
    titleSpan.className = "yield-crop-name fst-italici"
    titleSpan.innerText = `${label.innerText}`

    let valueSpan = document.createElement('span')
    valueSpan.className = "yield-number text-success text-uppercase"
    valueSpan.style.fontWeight = 'bold'
    valueSpan.style.marginLeft = '10px'
    valueSpan.innerText = `${(parseInt(valueinput.value.trim()) * 120).toString()}KG`

    let deleteimg = document.createElement('img')
    deleteimg.className = 'mx-2'
    deleteimg.style.cursor = 'pointer'
    deleteimg.src = "{% static 'argonomist/images/x-mark.png' %}"
    deleteimg.style.width = "14px"
    deleteimg.addEventListener('click', (e) => {
        e.target.parentNode.parentNode.removeChild(e.target.parentNode)
    })

    holderDiv.appendChild(titleSpan)
    holderDiv.appendChild(valueSpan)
    holderDiv.appendChild(deleteimg)

    previewContainer.appendChild(holderDiv)
    valueinput.value = ""
}

function addtoPreviewSeed(label, valueinput, previewContainer) {
    spans = document.getElementsByClassName('seed-name')

    for (let span of spans) {
        if (span.innerText.trim().toString() === label.innerText.trim().toString()) {
            span.nextSibling.innerText = `${valueinput.value.trim()}`
            valueinput.value = ""
            return;
        }
    }

    let holderDiv = document.createElement('div')
    holderDiv.className = "mx-2 seedvalue-holder"
    holderDiv.style.display = 'flex'
    holderDiv.style.alignItems = 'center'
    let titleSpan = document.createElement('span')
    titleSpan.className = "seed-name fst-italici"
    titleSpan.innerText = `${label.innerText}`
    // i don't need KG..
    let idadiSpan = document.createElement('span')
    idadiSpan.className = "seed-number text-success text-uppercase"
    idadiSpan.style.fontWeight = 'bold'
    idadiSpan.style.marginLeft = '10px'
    idadiSpan.innerText = `${valueinput.value.trim()}`

    let deleteimg = document.createElement('img')
    deleteimg.className = 'mx-2'
    deleteimg.style.cursor = 'pointer'
    deleteimg.src = "{% static 'argonomist/images/x-mark.png' %}"
    deleteimg.style.width = "14px"
    deleteimg.addEventListener('click', (e) => {
        e.target.parentNode.parentNode.removeChild(e.target.parentNode)
    })
    holderDiv.appendChild(titleSpan)
    holderDiv.appendChild(idadiSpan)
    holderDiv.appendChild(deleteimg)

    previewContainer.appendChild(holderDiv)
    valueinput.value = ""
}

function addtoPreview(label, valueinput, previewContainer) {

    // first detect the label if its "Select one" igonore,
    // then go to check the value if there is no any value just igonore
    // if the value is not integer just give display error text...
    spans = document.getElementsByClassName('fertilizer-name')

    for (let span of spans) {
        if (span.innerText.trim().toString() === label.innerText.trim().toString()) {
            console.log('span ', span)
            span.nextSibling.innerText = `${valueinput.value.trim()}KG`
            valueinput.value = ""
            return;
        }
    }


    let holderDiv = document.createElement('div')
    holderDiv.className = "mx-2 fertivalue-holder"
    holderDiv.style.display = 'flex';
    holderDiv.style.alignItems = 'center';
    let titleSpan = document.createElement('span')
    titleSpan.className = "fertilizer-name fst-italici"
    titleSpan.innerText = `${label.innerText}`
    let weightSpan = document.createElement('span')
    weightSpan.className = "fertilizer-weight text-success text-uppercase"
    weightSpan.style.fontWeight = 'bold'
    weightSpan.style.marginLeft = '10px'
    weightSpan.innerText = `${valueinput.value.trim()}KG`
    let deleteimg = document.createElement('img')
    deleteimg.className = "mx-2"
    deleteimg.style.cursor = "pointer"
    deleteimg.src = "{% static 'argonomist/images/x-mark.png' %}"
    deleteimg.style.width = "14px"
    deleteimg.addEventListener('click', (e) => {
        e.target.parentNode.parentNode.removeChild(e.target.parentNode)
    })
    holderDiv.appendChild(titleSpan)
    holderDiv.appendChild(weightSpan)
    holderDiv.appendChild(deleteimg)

    previewContainer.appendChild(holderDiv)

    // then clear the 'input'
    valueinput.value = ""
}


seedaddbtn.addEventListener('click', () => {
    if (seedInput.value.trim().length < 1) {
        errorMessage = "Error, Please enter something to add"
        displayError(errorMessage, seederrcont, seedInput)
        return;
    }
    if (isNaN(Number(yieldInput.value.trim()))) {
        errorMessage = "Error, please enter number only"
        displayError(errorMessage, seederrcont, seedInput)
        return
    }

    if (seed_label.innerText === "Select one") {
        // then we've an error here..
        errorMessage = "Amount submitted should have crop, click dropdown to select one"
        displayError(errorMessage, seederrcont, seedInput)
        return
    }

    addtoPreviewSeed(seed_label, seedInput, previewseed)
})

yieldbtn.addEventListener('click', () => {
    if (yieldInput.value.trim().length < 1) {
        errorMessage = "Error, Please enter something to add"
        displayError(errorMessage, yielderrcont, yieldInput)
        return;
    }
    if (isNaN(Number(yieldInput.value.trim()))) {
        errorMessage = "Error, please enter number only"
        displayError(errorMessage, yielderrcont, yieldInput)
        return
    }

    if (yield_label.innerText === "Select one") {
        // then we've an error here..
        errorMessage = "Amount submitted should have crop, click dropdown to select one"
        displayError(errorMessage, yielderrcont, yieldInput)
        return
    }

    addtoPreviewYield(yield_label, yieldInput, previewyield)
})

fertaddbtn.addEventListener('click', () => {
    if (fertiInput.value.trim().length < 1) {
        errorMessage = "Error, Please enter something to add"
        displayError(errorMessage, ferterrcont, fertiInput)
        return;
    }
    if (isNaN(Number(fertiInput.value.trim()))) {
        errorMessage = "Error, please enter number only"
        displayError(errorMessage, ferterrcont, fertiInput)
        return
    }

    if (label.innerText === "Select one") {
        // then we've an error here..
        errorMessage = "Amount submitted should have fertilizer, click dropdown to select one"
        displayError(errorMessage, ferterrcont, fertiInput)
        return
    }

    // we're good to go...
    // at first you should make sure if the fertilizer name found in its found you should update
    // instead of create a new one..
    addtoPreview(label, fertiInput, previewferti)


}) 
