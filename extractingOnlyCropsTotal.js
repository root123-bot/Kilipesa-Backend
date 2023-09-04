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
crops = ["Rice", "Cassava (manioc)", "Potato", "Beans, dry, edible, for grains", "Wheat "] // hii wheat uki-parse ina trim() all white space so make sure you trim all of em

let total = 0
let totalarr = []
let total_yield = [{ "dummy": "dummy_value" }]
for (let crop of crops) {
    for (let data of arr) {
        let yield_metadata = JSON.parse(data.standard_yield)
        for (let yield of yield_metadata) {
            // console.log('yield ', yield)

            if (Object.keys(yield)[0].trim() === crop.trim()) {

                // hapa ndo inapojirudia you should 'break' out of loop if you have.. ko kwa mfano nina {dummy}, itaenda mara moja.. then {dummy, rice} itaenda mara mbili, lets try to break out of loop since we expect to have only one obj.. can you ask me why i break outside of loop is because our TOTAL-YIELD SHOULD HAVE ONLY ONE OF OBJECT HAVING KEY OF 'CROP', SO ONCE CROP IS FOUND THERE IS NO NEED OF ITERATING TO OTHER LOOP SINCE WE WANT THE TOTAL-YIELD TO BE PLAIN WITH NO DUPLICATES..
                for (let addedmetadata of total_yield) {
                    if (Object.keys(addedmetadata)[0].trim() === crop.trim()) {


                        addedmetadata[Object.keys(addedmetadata)[0]]
                            = addedmetadata[Object.keys(addedmetadata)[0]] + parseInt(Object.values(yield)[0])

                        total = total + parseInt(Object.values(yield)[0])

                        break;
                    }
                    else {
                        totalarr.push({ [crop]: total })
                        total = 0
                        const metadata = { [crop.trim()]: parseInt(Object.values(yield)[0]) }
                        total_yield.push(metadata)
                        break;
                    }
                }

            }


        }
    }
}
console.log('TOTAL YIELD ', total_yield)



// next stef feed total_yield.shift

total_yield = [
    { Rice: 8040 },
    { Rice: 54000 },
    { Rice: 720 },
    { Rice: 1200 },
    { Rice: 2400 },
    { Rice: 36000 },
    { Rice: 2400 },
    { 'Cassava (manioc)': 1920 },
    { 'Cassava (manioc)': 3840 },
    { 'Cassava (manioc)': 15600 },
    { 'Cassava (manioc)': 1560 },
    { 'Cassava (manioc)': 2400 },
    { Potato: 14400 },
    { Potato: 1440 },
    { Potato: 1440 },
    { Potato: 5400 },
    { 'Beans, dry, edible, for grains': 9600 },
    { 'Beans, dry, edible, for grains': 960 },
    { 'Beans, dry, edible, for grains': 24000 },
    { Wheat: 1440 },
    { Wheat: 7200 },
    { Wheat: 1440 }
]

let crop_name = []
let crop_yield = []
for (let yield of total_yield) {
    crop_name.push((Object.keys(yield))[0])
    crop_yield.push((Object.values(yield))[0])
}
let output = crop_name.map(value => {
    return { [value]: 0 }
})
let intial_crop = crop_name[0]

for (let i = 0; i < crop_name.length; i++) {
    if (crop_name[i].trim() === intial_crop.trim()) {
        // console.log('yes sir ', crop_name[i].trim(), intial_co update ur output
        let counter = 0
        for (let j = 0; j < output.length; j++) {
            counter += 1

            if (Object.keys(output[j])[0].trim() === crop_name[i].trim()) {
                output[j][Object.keys(output[j])[0]] += parseInt(crop_yield[i])

            }


        }

    }
    intial_crop = crop_name[i + 1]
}

console.log('this is output ', output)


// 
const good_output = output.filter((val, index) => {
    if (index === 1) {
        return val
    }
    else {
        if (JSON.stringify(val) !== JSON.stringify(output[index - 1])) {
            return val
        }
    }
})










