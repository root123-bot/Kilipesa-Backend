arr = [
    {
        "id": 1,
        "crop": "[\"Avocado\", \"Beans, dry, edible, for grains\", \"Bergamot\"]",
        "fertilizer_name": "[\"Urea 46%N\", \"NPK 17:17:17\"]",
        "total_yield_in_ton": 2.76
    },
    {
        "id": 2,
        "crop": "[\"Palm, oil\", \"Potato, sweet\", \"Soybean\"]",
        "fertilizer_name": "[\"Booster IIC\", \"Maxi MKP\", \"Pot Phos\"]",
        "total_yield_in_ton": 12
    },
    {
        "id": 3,
        "crop": "[\"Alfalfa for fodder\",\"Raspberry (all varieties)\",\"Maize (hybrid)\"]",
        "fertilizer_name": "[\"Urea 46%N\",\"Di-Ammonium Phosphate (DAP)\",\"NPK 25:5:5\"]",
        "total_yield_in_ton": 0.6
    },
    {
        "id": 4,
        "crop": "[\"Urena (Congo jute) \",\"Oil palm \",\"Hempseed\",\"Indigo \"]",
        "fertilizer_name": "[\"Urea 46%N\",\"Sumicoat303\",\"Potassium Nitrate\"]",
        "total_yield_in_ton": 0.96
    },
    {
        "id": 5,
        "crop": "[\"Yam\",\"Maize, ordinary\",\"Quinoa\"]",
        "fertilizer_name": "[\"Calcium Ammonium Nitrate (CAN)\",\"Oc-booster \"]",
        "total_yield_in_ton": 0.84
    },
    {
        "id": 6,
        "crop": "[\"Maize, ordinary\",\"Cassava (manioc)\",\"Beans, dry, edible, for grains\"]",
        "fertilizer_name": "[\"Urea 46%N\",\"Di-Ammonium Phosphate (DAP)\"]",
        "total_yield_in_ton": 0.84
    },
    {
        "id": 7,
        "crop": "[\"Urena (Congo jute) \",\"Maize, ordinary\",\"Beans, dry, edible, for grains\"]",
        "fertilizer_name": "[\"Urea 46%N\",\"D.I Grow \",\"Di-Ammonium Phosphate (DAP)\"]",
        "total_yield_in_ton": 35.16
    },
    {
        "id": 8,
        "crop": "[\"Radish\",\"Maize, ordinary\",\"Avocado\"]",
        "fertilizer_name": "[\"Di-Ammonium Phosphate (DAP)\",\"Urea 46%N\",\"Booster IIC \"]",
        "total_yield_in_ton": 0.48
    },
    {
        "id": 9,
        "crop": "[\"Maize, ordinary\",\"Avocado\",\"Cassava (manioc)\"]",
        "fertilizer_name": "[\"Calcium Ammonium Nitrate (CAN)\",\"Urea 46%N\",\"Easy grow Flower and Fruits\"]",
        "total_yield_in_ton": 1.08
    }
]
/* 
    logic behind this scenario is that we calculate we need to use for loop of (for let i=0; i< ..; i++)
    to have correct value of next element of our array, if you choose to use shortcut of the for loop i mea
     >> for (let crop of crosp) will be difficult to get index of the next element if there is a duplicates
    and we depend on this logic of moving to the next element what i mean here is for example you have array 
    of duplicates of ['a', 'a', 'a', 'b', 'f' ].. if you want to move to the next index when you use
    shortcut of for loop will make u use indexOf and index of return the first occured elemnt if there is duplicates
    for example if i want index of second 'a' it will give me index 0 instead of one and this is when 
    we user arr.indexOf('a')... ko here for computing the occurance of elements its advisable to use the
    traditional for loop...
    this script here yield our output in object i mean element and its occurance for example 
    output = {a: 8, b: 1, mama: 2}.. so throught this object you will see that ok element of value 'a' is 
    most occured and it occured 8 out of 10 elements.. throught getting this number you can come forward and 
    calculate % percent of occurance of a, b, m all all your elements... THAT'S ALL MR
*/
crops = []

for (let data of arr) {
    for (let crop of JSON.parse(data.crop)) {

        crops.push(crop)
    }
}
sorted_crops = crops.sort()

console.log(crops.sort())
let output = [{ 'Alfalfa for fodder': 0 }]
let lastcrop = crops.sort()[0] // first value to start compare
for (let crop = 0; crop < crops.sort().length; crop++) {

    if (crops.sort()[crop] === lastcrop) {



        let keys = []
        for (let data of output) {

            keys = [...Object.keys(data)]
        }


        if (keys.includes(crops.sort()[crop])) {
            const funguo = []
            for (let out of output) {
                funguo.push(out)
            }

            output[0][crops.sort()[crop]] = output[0][crops.sort()[crop]] + 1;
        }
        else {

            output[0][crops.sort()[crop]] = 1
        }
    }

    lastcrop = crops.sort()[crop + 1]


}

console.log(output)


sorted_with_percent = []
occurence = Object.values(output[0])
console.log(occurence)
percent_only = []
occurence_in_percent = []
for (let i = 0; i < occurence.length; i++) {
    percent_only.push(Math.round(((occurence[i] / 9).toFixed(2) * 100)))
    occurence_in_percent.push({ [occurence[i]]: Math.round(((occurence[i] / 9).toFixed(2) * 100)) })
}

console.log(percent_only)
console.log(occurence_in_percent)

sorted_percent_only = percent_only.sort((a, b) => b - a)
console.log(sorted_percent_only)

// now we have occurence in percent can you arrange them 











