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
let output = [{ [crop_name[0]]: 0 }]
let intial_crop = crop_name[0]

for (let i = 0; i < crop_name.length; i++) {
    if (crop_name[i].trim() === intial_crop.trim()) {
        // console.log('yes sir ', crop_name[i].trim(), intial_crop.trim())
        // then its found in our output metadata.. you need to update ur output
        for (let j = 0; j < output.length; j++) {
            // console.log(Object.keys(output[j])[0], output[j], ' check output')
            if (Object.keys(output[j])[0].trim() === crop_name[i].trim()) {
                // console.log('still outside')
                // console.log('output to change ', output[j][Object.keys(output[j])[0]])
                output[j][Object.keys(output[j])[0]] += parseInt(crop_yield[i])
                // console.log('output after change ', )
            }
        }
    }
    else {
        const metadata = { [crop_name[i]]: crop_yield[i] }
        output.push(metadata)
    }
    intial_crop = crop_name[i + 1]
}

console.log('this is output ', output)













