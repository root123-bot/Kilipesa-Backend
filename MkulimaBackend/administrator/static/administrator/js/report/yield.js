/* hii haitakuwa called if the script above it have some errors you should know that
   thats why so you see sometimes your scripts are not executed... it means some other script
   above it raise errors..


   famountContainers = document.getElementsByClassName('famount')
    for (let container of famountContainers) {
        data = container.innerText
        datalist = data.split(', ')
        container.innerText = ""
        // console.log('container childNodes ', container.childNodes)
        for (let element of datalist) {
            list = element.split(' - ')
            console.log('list of weigth ', list)
            span = document.createElement("small")
            span.innerText = element
            span.style.display = 'block'
            span.style.whiteSpace = 'nowrap'
            container.appendChild(span)
        }
    }
    
    // http://forums.mozillazine.org/viewtopic.php?f=19&t=1590225
    // https://developer.mozilla.org/en/Code_snippets/Tabbed_browser#Detecting_page_load
    // domcontentloaded_event_running_twice_not_sure_how
    // the 'DOMcontentLoaded' event is fired twice ... WHY? https://stackoverflow.com/questions/4355344/domcontentloaded-event-firing-twice-for-a-single-page-load
    // To fix that you should add 'option' to fire only 'once'
    // dont use 'load', 'loadend', 'onreadystatechange' because are event listener
    // associated to AJAX xmlhttpresponse which is used normally by cdn you've linked in your html document..
    // so in most case we use domcontentload which only wait for dom content(html) to finish loading that means
    // its not deal with cdn, images, css and images or all other static files
    // i think in some case there are some cdn you've linked which makes your page loading twice..


    for (let container of containers) {
            data = container.innerText
            datalist = data.split('..., ')
            console.log('data ', data)
            console.log('datalist ', datalist)
            container.innerText = ""

            for (let element of datalist) {
                list = element.split(' ... - ')
                console.log('list ', list)

                div = document.createElement('div')
                div.style.whiteSpace = "nowrap"
                fnameSmall = document.createElement("small")
                fnameSmall.innerText = `${list[0]} - `

                weightSmall = document.createElement('small')
                weightSmall.innerText = `${list[1]}`
                console.log(list[1], weightSmall)

                weightSmall.style.fontWeight = 'bold'
                weightSmall.className = "text-success"
                div.appendChild(fnameSmall)
                div.appendChild(weightSmall)
                container.appendChild(div)
            }
        }

*/

loadCount = 0

document.addEventListener("DOMContentLoaded", (e) => {
    if (loadCount < 1) {
        let containers = document.getElementsByClassName("yieldamount")
        {/*
            lets have the 'array' of the 'objects' which contains the 'crop' name to its 
            corresponding yield and from it we should add the {object} of the key of 
            crop name to its yield it will look like this {"<div>cropnname</div>", "<div>cropyield</div>"}
        */}
        for (let container of containers) {
            // lets have the container inner text
            // modifiedObj = {} // No need for this ..
            // console.log('this is container inner text ', container.innerText)

            /*  {"rice": 600}
                crop = Object.keys(container)     // it return array of one key
                // but remember in crop we have something like "maize, ordinary"
                // this in our array will read as 2 element instead of one element..
                // get full crop name using joing
                cropname = crop.join(', ')
                // i will have full crop name in string.. like "Maize Ordinary"
                // this name will be pure without ', ' so for beans it will be "beans dry edible for grains"
                // its okay to have this kind of name than in the last section...
                // then create span for it start with div..
                div = document.createElement('div')
                div.style.whiteSpace = "nowrap"
                cropSmall = document.createElement("small")
                cropSmall.innerText = `${list[0]} - 0`

                
                yield = Object.values(container)[0] 
                yieldSmall = document.createElement('small')
                yieldSmall.className = "text-success"
                yieldsmall.style.fontWeight = "bold"

                div.appendChild(cropSmall)
                div.appendChild(yieldSmall)

                // clear innerText of our container
                container.innerText = ""
                container.appendChild(div)


                THIS IS HOW WE'LL COMPLETE THIS
                
            
            */
            metadata = JSON.parse(container.innerText)
            container.innerText = ""
            for (let data of metadata) {
                crop = Object.keys(data)
                {/*
                    if you have the crop array of ['Maize', 'Ordinary'] if you join this
                    it will produce one string of "Maize, Ordinary" this is what i want  to
                    have the name the same to that of our crops....
                */}
                cropname = crop.join(', ')
                div = document.createElement('div')
                div.style.whiteSpace = "nowrap"
                cropSmall = document.createElement("small")
                cropSmall.innerText = `${cropname}`

                yield = Object.values(data)[0]
                yieldSmall = document.createElement('small')
                yieldSmall.className = "text-success mx-2"
                yieldSmall.style.fontWeight = "bold"
                yieldSmall.innerText = `${yield}KG`
                div.appendChild(cropSmall)
                div.appendChild(yieldSmall)
                container.appendChild(div)
            }

        }
        loadCount += 1
    }
})