fertpreview = document.getElementById("ferti-prev")
seedpreview = document.getElementById("seed-prev")
yieldprev = document.getElementById("yield-prev")

seedContainer = document.getElementById("seed")
yieldContainer = document.getElementById("yield")

seeds = JSON.parse(seedContainer.value)
yields = JSON.parse(yieldContainer.value)

fertilizersContainer = document.getElementById("fertilizers")
fertilizers = JSON.parse(fertilizersContainer.value)

for (let fertilizer of fertilizers) {
    fert_name = Object.keys(fertilizer)[0]
    fert_weight = Object.values(fertilizer)[0]

    div = document.createElement("div")
    div.className = ""
    div.style.display = "flex"
    div.style.alignItem = "center"

    let titleSpan = document.createElement('span')
    titleSpan.className = "fst-italici"
    titleSpan.innerText = fert_name

    let valueSpan = document.createElement('span')
    valueSpan.className = "text-success text-uppercase"
    valueSpan.style.fontWeight = 'bold'
    valueSpan.style.marginLeft = '10px'
    valueSpan.innerText = `${fert_weight}KG`

    div.appendChild(titleSpan)
    div.appendChild(valueSpan)

    fertpreview.appendChild(div)
}

for (let seed of seeds) {
    seed_name = Object.keys(seed)[0]
    seed_weight = Object.values(seed)[0]

    div = document.createElement("div")
    div.className = ""
    div.style.display = "flex"
    div.style.alignItem = "center"

    let titleSpan = document.createElement('span')
    titleSpan.className = "fst-italici"
    titleSpan.innerText = seed_name

    let valueSpan = document.createElement('span')
    valueSpan.className = "text-success text-uppercase"
    valueSpan.style.fontWeight = 'bold'
    valueSpan.style.marginLeft = '10px'
    valueSpan.innerText = `${seed_weight}`

    div.appendChild(titleSpan)
    div.appendChild(valueSpan)

    seedpreview.appendChild(div)
}

for (let yield of yields) {
    crop_name = Object.keys(yield)[0]
    estimated_yield = Object.values(yield)[0]
    console.log(crop_name, estimated_yield)
    div = document.createElement("div")
    div.className = ""
    div.style.display = "flex"
    div.style.alignItem = "center"

    let titleSpan = document.createElement('span')
    titleSpan.className = "fst-italici"
    titleSpan.innerText = crop_name

    let valueSpan = document.createElement('span')
    valueSpan.className = "text-success text-uppercase"
    valueSpan.style.fontWeight = 'bold'
    valueSpan.style.marginLeft = '10px'
    valueSpan.innerText = `${estimated_yield}KG`

    div.appendChild(titleSpan)
    div.appendChild(valueSpan)
    yieldprev.appendChild(div)
}