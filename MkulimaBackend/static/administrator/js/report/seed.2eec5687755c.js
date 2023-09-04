loadCount = 0;

document.addEventListener("DOMContentLoaded", (e) => {
  if (loadCount < 1) {
    let containers = document.getElementsByClassName("seedamount");
    for (let container of containers) {
      // console.log('this is container inner text ', container.innerText)

      metadata = JSON.parse(container.innerText);
      container.innerText = "";
      for (let data of metadata) {
        crop = Object.keys(data);
        cropname = crop.join(", ");
        div = document.createElement("div");
        div.style.whiteSpace = "nowrap";
        cropSmall = document.createElement("small");
        cropSmall.innerText = `${cropname}`;

        yield = Object.values(data)[0];
        yieldSmall = document.createElement("small");
        yieldSmall.className = "text-success mx-2";
        yieldSmall.style.fontWeight = "bold";
        // SI unit of seed is based on aina ya mbegu kwa mfano kwa mihogo ni miche, kwa maharage ni kilo..
        // google in wikipedia "measurement of seed amount."
        console.log("yield ", yield);
        yieldSmall.innerText = `${yield}`;
        div.appendChild(cropSmall);
        div.appendChild(yieldSmall);
        container.appendChild(div);
      }
    }
    loadCount += 1;
  }
});
