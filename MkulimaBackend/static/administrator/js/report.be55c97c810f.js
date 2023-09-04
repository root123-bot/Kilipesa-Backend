let yearfilter = document.getElementById("yearfilter");
let regionfilter = document.getElementById("regionfilter");
let districtfilter = document.getElementById("districtfilter");
let filters = [yearfilter, regionfilter, districtfilter];

let yearIndicator = document.getElementById("selectedyear");
let regionIndicator = document.getElementById("selectedregion");
let districtIndicator = document.getElementById("selecteddistrict");

console.log("indicators ", yearIndicator, regionIndicator, districtIndicator);

let advices = []; // you should have initial button set to all fams fetched intially

let savereportbtn = document.getElementById("savereportbtn");

function filterFarms() {
  let filteredfarms = [...advices];
  if (yearfilter.value !== "All") {
    filteredfarms = filteredfarms.filter(
      (value) =>
        value.get_added_year.toString().trim() ===
        yearfilter.value.toString().trim()
    );
  }

  if (regionfilter.value !== "All") {
    filteredfarms = filteredfarms.filter(
      (value) => value.region.trim() === regionfilter.value.trim()
    );
  }

  if (districtfilter.value !== "All") {
    filteredfarms = filteredfarms.filter(
      (value) => value.district.trim() === districtfilter.value.trim()
    );
  }

  return filteredfarms;
}

savereportbtn.addEventListener("click", (e) => {
  e.preventDefault();
  result = filterFarms();

  console.log("result ", result);
  // then we should add logic to create pdf..
  // initialize jsPDF document
  const info = [];
  result.forEach((element, index) => {
    info.push([
      element.farm_owner,
      element.farm_location,
      element.size,
      element.have_report,
      element.get_recommended_fertilizer,
      element.get_recommended_crops,
    ]);
  });
  let doc = new jsPDF();

  doc.autoTable({
    head: [
      [
        "Farm Owner",
        "Farm Size",
        "Farm Location",
        "Is Recommended",
        "Recommended Fertilizers",
        "Recommended Crops",
      ],
    ],
    body: info,
  });

  doc.save("report.pdf");
});

for (let filter of filters) {
  filter.addEventListener("change", (e) => {
    // everytime one of em change then you need to update the district > years > regions..
    regionIndicator.innerText = regionfilter.value;
    yearIndicator.innerText = yearfilter.value;
    districtIndicator.innerText = districtfilter.value;

    if (regionIndicator.innerText === "All") {
      regionIndicator.innerText = "All Regions";
    }
    if (districtIndicator.innerText === "All") {
      districtIndicator.innerText = "All Districts";
    }

    if (yearIndicator.innerText === "All") {
      yearIndicator.innerText = "All Years";
    }

    mapendekezo = [...recommendations];
    mapendekezo = mapendekezo.filter((value) => value.get_report_date !== null);
    if (yearfilter.value !== "All") {
      let recomms = mapendekezo.filter(
        (value) =>
          value.get_report_date.toString() === yearfilter.value.toString()
      );
      mapendekezo = [...recomms];
    }

    if (regionfilter.value !== "All") {
      mapendekezo = mapendekezo.filter(
        (value) => value.get_farm_region === regionfilter.value
      );
      let wilaya = [...mapendekezo];
    }

    if (districtfilter.value !== "All") {
      mapendekezo = mapendekezo.filter(
        (value) => value.get_farm_district === districtfilter.value
      );
    }

    // start logics for all condition to display recommended number for given filtered..
    if (
      yearfilter.value !== "All" ||
      regionfilter.value !== "All" ||
      districtfilter.value === "All"
    ) {
      // document.getElementById("totalfarms").style.display = 'none'
      // document.getElementById("recommsfarms").innerText = 'Recommended: ' + mapendekezo.length
    }
    if (
      yearfilter.value === "All" &&
      regionfilter.value === "All" &&
      districtfilter.value === "All"
    ) {
      // display both of them
      // document.getElementById("totalfarms").style.display = 'block'
      // document.getElementById("recommsfarms").innerText = 'Recommended: ' + mapendekezo.length
    }
    // logic to display recommended farms vs total farms

    console.log("Result of our filtered ", mapendekezo);
    // advices = [...mapendekezo]
    console.log("advices ", advices);

    const data = computeReports(mapendekezo);
    const pie_labels = [];
    const pie_values = [];
    for (let zao of data) {
      let value = Object.keys(zao)[0];
      pie_labels.push(value);
    }

    for (let mark of data) {
      let value = Object.values(mark)[0];
      pie_values.push(value);
    }
    chart2.data.labels = [...pie_labels];
    chart2.data.datasets[0].data = [...pie_values];
    chart2.update();

    // lets go to compute our bar chart
    let bar_labels = [...pie_labels];
    const yieldmetadata = computeYields(mapendekezo, bar_labels);
    const yieldintons = Object.values(yieldmetadata).map((value) =>
      parseFloat(parseFloat(value[Object.keys(value)[0]]) / 1000)
    );
    // console.log('yields in tons ', yieldintons)

    const bar_data = [...yieldintons];
    // console.log('metadata ', yieldmetadata)
    // you should consider the metadata returned from 'computerYield' and not the pie labels because pie_labels having 5 fields but
    // our computeYield return the 3 data or less than 5 and other reasons
    actual_bar_labels = [];
    for (let lebo of yieldmetadata) {
      actual_bar_labels.push(Object.keys(lebo)[0]);
    }
    bar_labels = actual_bar_labels;
    chart.data.labels = bar_labels;
    chart.data.datasets[0].data = bar_data;
    chart.update();
  });
}

let domain = "http://147.182.138.184/api/";
let chart = "";
let ctx = "";
let ctx2 = "";
let chart2 = "";
let recommendations = [];

function computeReports(recommendations) {
  recommendations = recommendations.filter(
    (value) => value.get_report_date !== null
  );
  let crops = [];
  let sorted_crops = [];
  let output = [{ [JSON.parse(recommendations[0].crop).sort()[0]]: 0 }];

  for (let data of recommendations) {
    for (let crop of JSON.parse(data.crop)) {
      crops.push(crop);
    }
  }
  sorted_crops = [...crops.sort()];
  let lastcrop = sorted_crops[0];

  for (let crop = 0; crop < sorted_crops.length; crop++) {
    if (sorted_crops[crop] === lastcrop) {
      let keys = [];
      for (let data of output) {
        keys = [...Object.keys(data)];
      }

      if (keys.includes(sorted_crops[crop])) {
        output[0][sorted_crops[crop]] = output[0][sorted_crops[crop]] + 1;
      } else {
        output[0][sorted_crops[crop]] = 1;
      }
    }
    lastcrop = sorted_crops[crop + 1];
  }

  let occurence = Object.values(output[0]);
  let percent_only = [];
  let occurence_in_percent = [];
  let OUTPUT;
  funguo = Object.keys(output[0]);
  alama = Object.values(output[0]);

  OUTPUT = funguo.map((val, index) => {
    return { [val]: parseInt(alama[index]) };
  });

  // remove that 9 because its hardcode total ercomms
  for (let i = 0; i < occurence.length; i++) {
    percent_only.push(
      Math.round((occurence[i] / recommendations.length).toFixed(2) * 100)
    );
    occurence_in_percent.push({
      [occurence[i]]: Math.round(
        (occurence[i] / recommendations.length).toFixed(2) * 100
      ),
    });
  }

  keysonly = [];
  for (let data of occurence_in_percent) {
    valu = Object.keys(data)[0];
    keysonly.push(parseInt(valu));
  }
  cloned = keysonly;
  cloned = cloned.sort((a, b) => b - a);
  topfive = cloned.filter((value, index) => index < 5);
  // console.log('top five ', topfive)
  topFiveMetadata = [];
  for (let elem of topfive) {
    // hii data inaleta element 6 kwenye ku-filter endapo kuna element zenye same values nyingi..
    data = OUTPUT.filter(
      (value) => parseInt(Object.values(value)[0]) === parseInt(elem)
    );
    // console.log('data ', data)  // kwa
    for (let dd of data) {
      // console.log('dd ', dd)
      metadataKeys = [];
      for (let md of topFiveMetadata) {
        metadataKeys.push(Object.keys(md)[0]);
      }

      if (metadataKeys.includes(Object.keys(dd)[0])) {
        continue;
      }

      if (topFiveMetadata.length < 6) {
        // console.log('topfive metadata length ', topFiveMetadata.length)
        topFiveMetadata = [...topFiveMetadata, ...data];
      }
    }
    // topFiveMetadata = [...topFiveMetadata, ...data]
  }
  console.log("top five metadata ", topFiveMetadata);

  // for now only ..FOR NOW ONLY LETS LIMIT IT TO FIVE, ina-make sense kwa certain crops to appear
  // the same in number of farms.. that's why we should trim() them off...
  topFiveMetadata = topFiveMetadata.filter((value, index) => index < 5);
  // we'll come and solve this duplicates returned which makes data added more than 5..

  let cloned_percent_only = [...percent_only];
  let sorted_percent_only = cloned_percent_only.sort((a, b) => b - a);

  pie_chart = [];
  for (let i = 0; i < topFiveMetadata.length; i++) {
    value = topFiveMetadata[i];
    value[Object.keys(value)[0]] = sorted_percent_only[i];

    pie_chart.push(value);
  }

  // console.log('pie chart ', pie_chart)

  most_recommended_crops = [];

  return pie_chart;
}

function computeYields(arr, crops) {
  let total_yield = [{ dummy: "dummy_value" }];
  // remove dummy/null recomms from our array
  arr = arr.filter((value) => value.get_farm_region !== null);
  for (let crop of crops) {
    for (let data of arr) {
      let yield_metadata = JSON.parse(data.standard_yield);
      for (let yield of yield_metadata) {
        if (Object.keys(yield)[0].trim() === crop.trim()) {
          for (let addedmetadata of total_yield) {
            if (Object.keys(addedmetadata)[0].trim() === crop.trim()) {
              addedmetadata[Object.keys(addedmetadata)[0]] =
                addedmetadata[Object.keys(addedmetadata)[0]] +
                parseInt(Object.values(yield)[0]);

              break;
            } else {
              const metadata = {
                [crop.trim()]: parseInt(Object.values(yield)[0]),
              };
              total_yield.push(metadata);
              break;
            }
          }
        }
      }
    }
  }
  // console.log('TOTAL YIELD ', total_yield)
  total_yield.shift();
  // return total_yield

  let crop_name = [];
  let crop_yield = [];
  for (let yield of total_yield) {
    crop_name.push(Object.keys(yield)[0]);
    crop_yield.push(Object.values(yield)[0]);
  }
  let output = crop_name.map((value) => {
    return { [value]: 0 };
  });
  let intial_crop = crop_name[0];

  for (let i = 0; i < crop_name.length; i++) {
    if (crop_name[i].trim() === intial_crop.trim()) {
      let counter = 0;
      for (let j = 0; j < output.length; j++) {
        counter += 1;

        if (Object.keys(output[j])[0].trim() === crop_name[i].trim()) {
          output[j][Object.keys(output[j])[0]] += parseInt(crop_yield[i]);
        }
      }
    }
    intial_crop = crop_name[i + 1];
  }

  //
  const good_output = output.filter((val, index) => {
    if (index === 0) {
      return val;
    } else {
      if (JSON.stringify(val) !== JSON.stringify(output[index - 1])) {
        return val;
      }
    }
  });

  return good_output;
}

function executeRegions() {
  let year = yearfilter.value;

  let year_recomms = [...recommendations];
  if (year !== "All") {
    let regions = year_recomms
      .filter((value) => value.get_report_date !== null)
      .filter((val) => val.get_report_date.toString() === year.toString())
      .map((value) => value.get_farm_region);

    // remove duplicates
    regions = regions.sort().filter((value, index) => {
      if (index === 0) {
        return value;
      } else {
        if (value.toString() !== regions[index - 1]) {
          return value;
        }
      }
    });

    // Clear available regions..
    for (let elem of Object.values(regionfilter.children)) {
      if (elem.innerText !== "All regions") {
        regionfilter.removeChild(elem);
      }
    }

    for (let region of regions) {
      let opt = document.createElement("option");
      opt.innerHTML = region;
      regionfilter.appendChild(opt);
    }
  } else {
    for (let elem of Object.values(regionfilter.children)) {
      if (elem.innerText !== "All regions") {
        regionfilter.removeChild(elem);
      }
    }

    // remember this also have effect directly on districts, so lets also return default options in district
    // filter because even if all regions became "All regions" it have no effect
    // to get out districts to default value...  for more
    for (let elem of Object.values(districtfilter.children)) {
      if (elem.innerText !== "All districts") {
        districtfilter.removeChild(elem);
      }
    }
  }
}

function executeDistricts() {
  // console.log('im clicked...')
  let region = regionfilter.value;

  let region_recomms = [...recommendations];
  if (region !== "All") {
    let districts = region_recomms
      .filter((value) => value.get_farm_region !== null)
      .filter((val) => val.get_farm_region === region)
      .map((value) => value.get_farm_district);

    // console.log('region recoms ', districts)
    // remove duplicates

    districts = districts.sort().filter((value, index) => {
      if (index === 0) {
        return value;
      } else {
        if (value.toString() !== districts[index - 1]) {
          // kama sio sawasawa, then append it
          return value;
        }
      }
    });
    // clear
    for (let elem of Object.values(districtfilter.children)) {
      if (elem.innerText !== "All districts") {
        districtfilter.removeChild(elem);
      }
    }

    for (let district of districts) {
      let opt = document.createElement("option");
      opt.innerHTML = district;
      districtfilter.appendChild(opt);
    }
  } else {
    for (let elem of Object.values(districtfilter.children)) {
      if (elem.innerText !== "All districts") {
        districtfilter.removeChild(elem);
      }
    }
  }
}

function computeFilters(recommendations) {
  const fetchedyears = recommendations
    .map((value) => value.get_report_date)
    .filter((value) => value != null);
  const years = fetchedyears
    .sort((a, b) => b - a)
    .filter((value, index) => {
      if (index === 0) {
        return value;
      } else {
        if (value.toString() !== fetchedyears[index - 1].toString()) {
          return value;
        }
      }
    });
  const fetchedregions = recommendations
    .map((value) => value.get_farm_region)
    .filter((value) => value != null);
  const regions = fetchedregions.sort().filter((value, index) => {
    if (index === 0) {
      return value;
    } else {
      if (value.toString() !== fetchedregions[index - 1].toString()) {
        return value;
      }
    }
  });
  const fetcheddistricts = recommendations
    .map((value) => value.get_farm_district)
    .filter((value) => value != null);
  const districts = fetcheddistricts.sort().filter((value, index) => {
    if (index === 0) {
      return value;
    } else {
      if (value.toString() !== fetcheddistricts[index - 1].toString()) {
        return value;
      }
    }
  });

  // console.log(years, regions, districts)
  for (let year of years) {
    let optionElem = document.createElement("option");
    optionElem.innerHTML = year;
    yearfilter.appendChild(optionElem);
  }

  // I DON'T NEED TO HAVE REGIONS
  // for (let region of regions) {
  //     let optionElem = document.createElement('option')
  //     optionElem.innerHTML = region
  //     regionfilter.appendChild(optionElem)
  // }

  // I DON'T NEED TO HAVE DISTRICT LIST IF THE REGION IS NOT SELECTED..
  // for (let district of districts) {
  //     let optionElem = document.createElement("option")
  //     optionElem.innerHTML = district
  //     districtfilter.appendChild(optionElem)
  // }
}

fetch(`${domain}recomms`)
  .then((response) => response.json())
  .then((recomms) => {
    recommendations = recomms;
    // advices = recomms.filter(value => value.get_farm_region !== null)  // so initially advices set to all recommendations when we filter it will updated to filtered recommendations
    // console.log('fetched ', recomms)
    // na hapa ndo logic ya kuzi-manipulate inapotokea
    const data = computeReports(recommendations);
    computeFilters(recommendations);

    console.log("data ", data);
    const pie_labels = [];
    const pie_values = [];
    for (let zao of data) {
      let value = Object.keys(zao)[0];
      pie_labels.push(value);
    }

    for (let mark of data) {
      let value = Object.values(mark)[0];
      pie_values.push(value);
    }

    let bar_labels = [...pie_labels];
    const yieldmetadata = computeYields(recommendations, bar_labels);
    // console.log(yieldmetadata, Object.values(yieldmetadata))
    actual_bar_labels = [];
    for (let lebo of yieldmetadata) {
      actual_bar_labels.push(Object.keys(lebo)[0]);
    }
    const yieldintons = Object.values(yieldmetadata).map((value) =>
      parseFloat(parseInt(value[Object.keys(value)[0]]) / 1000)
    );
    // console.log('yields in tons ', yieldintons)
    const bar_data = [...yieldintons];
    bar_labels = actual_bar_labels;

    // pie chart
    ctx2 = document.getElementById("pie-chart");
    chart2 = new Chart(ctx2, {
      type: "pie",
      data: {
        labels: pie_labels,
        datasets: [
          {
            backgroundColor: [
              "#43C59E",
              "#FDE74C",
              "#8F3985",
              "#A3320B",
              "#385F71",
              "#82846D",
            ],
            data: pie_values,
          },
        ],
      },
      options: {
        responsive: true,
        mainAspectRatio: false,
        plugins: {
          legend: {
            display: false,
          },
          labels: {
            render: (ctx) => {
              if (ctx.label.length > 9) {
                return ctx.label.substr(0, 8) + "..";
              }
              return ctx.label;
            },
            fontColor: "#fff",
            fontStyle: "bolder",
          },
          tooltip: {
            callbacks: {
              label: (context) => {
                return `${context.parsed}% ${context.label}`;
              },
            },
          },
        },
      },
    });

    // bar chart

    ctx = document.getElementById("bar-chart");

    chart = new Chart(ctx, {
      type: "bar",
      data: {
        labels: bar_labels,
        datasets: [
          {
            backgroundColor: ["#6c7293"],
            data: bar_data,
            borderWidth: 1,
          },
        ],
      },
      options: {
        scales: {
          y: {
            beginAtZero: true,
          },
        },
        plugins: {
          legend: {
            display: false,
          },
          tooltip: {
            callbacks: {
              label: (context) => {
                return `${context.formattedValue} tons`;
              },
            },
          },
        },
      },
    });
  });

// fetch farms...
fetch(`${domain}farms`)
  .then((response) => response.json())
  .then((farms) => (advices = [...farms]));
