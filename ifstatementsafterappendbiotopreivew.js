if (parseInt(distancebetweenbottomofviewedwindowtobottomofelement) > 300) {
    dimensions = e.target.getBoundingClientRect()
    previewElem.style.position = "absolute"
    previewElem.style.top = (dimensions.bottom + window.scrollY) + "px"
    previewElem.style.left = (dimensions.left - dimensions.left/4) + "px"

    previewElem.addEventListener('mouseover', (e) => {
        previewElem.style.display = "flex"
        previewElem.style.justifyContent = "center"
        previewElem.style.alignItems = "center"
        isPreviewStillHoverred = true

        // remove if there is loading..
        removeLoader()
    })

    previewElem.addEventListener('mouseout', (e) => {
        previewElem.style.display = "flex"
        previewElem.style.justifyContent = "center"
        previewElem.style.alignItems = "center"
        // labda ni muhimu kuwa na delay before making it disappear
        setTimeout(() => {
            isPreviewStillHoverred = false

            // kwanini tusi-remove that element hapahapa...
            previewElem.remove()
        }, 50)

        // remove if there is loaders
        removeLoader()
    })
    document.body.appendChild(previewElem)

}


else {
    dimensions = e.target.getBoundingClientRect()
    previewElem.style.position = "absolute"
    previewElem.style.top = (dimensions.top + window.scrollY - 210) + "px"
    previewElem.style.left = (dimensions.left - dimensions.left/4) + "px"

    previewElem.addEventListener('mouseover', (e) => {
        previewElem.style.display = "flex"
        previewElem.style.justifyContent = "center"
        previewElem.style.alignItems = "center"
        isPreviewStillHoverred = true

        // remove if there is loader 
        removeLoader()
    })

    previewElem.addEventListener('mouseout', (e) => {
        previewElem.style.display = "none"
        setTimeout(() => {
            isPreviewStillHoverred = false
            previewElem.remove()
        }, 50)

        // remove if there is loader
        removeLoader()
    })

    document.body.appendChild(previewElem)
}



// other for loop end the script

for (let i=0; i < argospans.length; i++) {
    argospans[i].addEventListener('mouseout', function removePopup(e) {
        // remove if  there is loaders
        removeLoader()

        previews = document.getElementsByClassName("preview")
        for (let j=0; j < previews.length; j++) {
            
            setTimeout(() => {
                if (!isPreviewStillHoverred) {
                        if (previews[j]) {
                            previews[j].remove()
                        }
                        else {
                            removePopup(e)
                        }
                }
            }, 30)
            
        }
    })
}