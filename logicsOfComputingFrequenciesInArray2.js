arr =
    [
        {
            "id": 23,
            "crop": "[\"Rice \",\"Cassava (manioc)\"]",
            "fertilizer_name": "[\"Urea 46%N\",\"Di-Ammonium Phosphate (DAP)\"]",
            "standard_yield": "[{\"Cassava (manioc)\":\"1920\"},{\"Rice\":\"8040\"}]"
        },
        {
            "id": 24,
            "crop": "[\"Rice \",\"Maize, ordinary\"]",
            "fertilizer_name": "[\"Urea 46%N\",\"Di-Ammonium Phosphate (DAP)\"]",
            "standard_yield": "[{\"Rice\":54000},{\"Maize, ordinary\":44400}]"
        },
        {
            "id": 25,
            "crop": "[\"Potato, sweet \"]",
            "fertilizer_name": "[\"Ammonium Sulphate (SA)\",\"Booster IIC \"]",
            "standard_yield": "[{\"Potato, sweet\":7200}]"
        },
        {
            "id": 26,
            "crop": "[\"Beans, dry, edible, for grains\",\"Maize, ordinary\"]",
            "fertilizer_name": "[\"Urea 46%N\",\"Booster IIC \"]",
            "standard_yield": "[{\"Maize, ordinary\":960},{\"Beans, dry, edible, for grains\":9600}]"
        },
        {
            "id": 27,
            "crop": "[\"Rice \",\"Beans, dry, edible, for grains\"]",
            "fertilizer_name": "[\"Urea 46%N\",\"Booster IIC \"]",
            "standard_yield": "[{\"Rice\":720},{\"Beans, dry, edible, for grains\":960}]"
        },
        {
            "id": 28,
            "crop": "[\"Cassava (manioc)\",\"Potato \",\"Rice \"]",
            "fertilizer_name": "[\"Urea 46%N\",\"Di-Ammonium Phosphate (DAP)\",\"Dodoma Aglime\"]",
            "standard_yield": "[{\"Cassava (manioc)\":3840},{\"Potato\":14400},{\"Rice\":1200}]"
        },
        {
            "id": 29,
            "crop": "[\"Potato \",\"Cassava (manioc)\",\"Rice \"]",
            "fertilizer_name": "[\"Booster IIC \",\"Dodoma Aglime\"]",
            "standard_yield": "[{\"Potato\":1440},{\"Cassava (manioc)\":15600},{\"Rice\":2400}]"
        },
        {
            "id": 30,
            "crop": "[\"Beans, dry, edible, for grains\",\"Rice \"]",
            "fertilizer_name": "[\"Di-Ammonium Phosphate (DAP)\",\"Dodoma Aglime\"]",
            "standard_yield": "[{\"Beans, dry, edible, for grains\":24000},{\"Rice\":36000}]"
        },
        {
            "id": 31,
            "crop": "[\"Wheat \",\"Cassava (manioc)\",\"Rice \"]",
            "fertilizer_name": "[\"Di-Ammonium Phosphate (DAP)\",\"Booster IIC \",\"Dodoma Aglime\"]",
            "standard_yield": "[{\"Wheat\":1440},{\"Rice\":2400},{\"Cassava (manioc)\":1560}]"
        },
        {
            "id": 32,
            "crop": "[\"Wheat \",\"Cassava (manioc)\",\"Potato \"]",
            "fertilizer_name": "[\"Booster IIC \"]",
            "standard_yield": "[{\"Wheat\":7200},{\"Cassava (manioc)\":2400},{\"Potato\":1440}]"
        },
        {
            "id": 33,
            "crop": "[\"Broccoli\",\"Coconut \",\"Cucumber\",\"Onion, dry \"]",
            "fertilizer_name": "[\"Urea 46%N\",\"Dodoma Aglime\"]",
            "standard_yield": "[{\"Broccoli\":2520},{\"Coconut\":8400},{\"Cucumber\":2520},{\"Onion, dry\":11760}]"
        },
        {
            "id": 34,
            "crop": "[\"Wheat \",\"Potato \"]",
            "fertilizer_name": "[\"Dodoma Aglime\",\"Di-Ammonium Phosphate (DAP)\"]",
            "standard_yield": "[{\"Wheat\":1440},{\"Potato\":5400}]"
        }
    ]
crops = []

for (let data of arr) {
    for (let crop of JSON.parse(data.crop)) {

        crops.push(crop)
    }
}
sorted_crops = crops.sort()

let output = [{ 'Alfalfa for fodder': 0 }]
let lastcrop = crops.sort()[0] // first value to start compare
for (let crop = 0; crop < crops.sort().length; crop++) {
    // console.log('crop ', crops.sort()[crop],  ' lastcrop ', lastcrop, ' value ', crops[crop], ' compare ', crops.indexOf(lastcrop))
    if (crops.sort()[crop] === lastcrop) {

        let keys = []
        for (let data of output) {

            keys = [...Object.keys(data)]
        }

        if (keys.includes(crops.sort()[crop])) {
            output[0][crops.sort()[crop]] = output[0][crops.sort()[crop]] + 1;
        }
        else {
            // we need to create a new one and have 1 as its value
            output[0][crops.sort()[crop]] = 1
        }
    }
    // set the last crop here to new value
    lastcrop = crops.sort()[crop + 1]

}


console.log('OUTPUT ', output)
let OUTPUT;
funguo = Object.keys(output[0])
alama = Object.values(output[0])

OUTPUT = funguo.map((val, index) => { return { [val]: parseInt(alama[index]) } })

console.log('Overall output ', OUTPUT)

sorted_with_percent = []
occurence = Object.values(output[0])
crop_name = Object.keys(output[0])
// console.log(occurence)
percent_only = []
occurence_in_percent = []
for (let i = 0; i < occurence.length; i++) {
    percent_only.push(Math.round(((occurence[i] / 9).toFixed(2) * 100)))
    occurence_in_percent.push({ [occurence[i]]: Math.round(((occurence[i] / 9).toFixed(2) * 100)) })
}

// console.log('occu ', occurence)
// console.log(percent_only)
console.log('all of-m ', occurence_in_percent)

keysonly = []
for (let data of occurence_in_percent) {
    valu = Object.keys(data)[0]
    keysonly.push(parseInt(valu))
}
cloned = keysonly
cloned = cloned.sort((a, b) => b - a)
topfive = cloned.filter((value, index) => index < 5)
console.log('trimmed ', topfive)
console.log('keys only ', cloned)

topFiveMetadata = []
for (let elem of topfive) {
    data = OUTPUT.filter(value => parseInt(Object.values(value)[0]) === parseInt(elem))
    console.log('data ', data)
    for (let dd of data) {
        metadataKeys = []
        for (let md of topFiveMetadata) {
            metadataKeys.push(Object.keys(md)[0])
        }

        console.log('dd ', dd)
        if (metadataKeys.includes(Object.keys(dd)[0])) {
            continue
        }
        topFiveMetadata = [...topFiveMetadata, ...data]
    }
    // topFiveMetadata = [...topFiveMetadata, ...data]
}




cloned_percent_only = [...percent_only]
sorted_percent_only = cloned_percent_only.sort((a, b) => b - a)
console.log('sorted ', sorted_percent_only)
console.log('Everything u need ', topFiveMetadata)
pie_chart = []
for (let i = 0; i < topFiveMetadata.length; i++) {

    value = topFiveMetadata[i]
    value[Object.keys(value)[0]] = sorted_percent_only[i]

    pie_chart.push(value)
}

console.log('pie chart ', pie_chart)













