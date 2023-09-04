
let checkboxes = document.getElementsByClassName('form-check-input')
const checkedprofiles = []

for (let checkbox of checkboxes) {
    checkbox.addEventListener("click", (e) => {
        const checked = e.target.checked
        const span = e.target.nextSibling.nextSibling
        const profile_id = span.title
        if (checked) {
            checkedprofiles.push(profile_id)
        }
        else {
            if (checkedprofiles.includes(profile_id)) {
                checkedprofiles.splice(checkedprofiles.indexOf(profile_id), 1)
            }
        }
        console.log('user ', checkedprofiles)
    })

}

let delete_link = document.getElementById("submitlink")

delete_link.addEventListener('click', (e) => {
    e.preventDefault()
    if (checkedprofiles.length > 0) {
        document.getElementById("idsinput").value = JSON.stringify(checkedprofiles);
        let form = document.getElementById("deletegatherman")
        form.submit()
    }
    else {
        // notify the user we can't delete nothing..
        // show the error message..
    }
})
document.getElementById('yearfilterlink').addEventListener('click', (e) => {
    const form = document.getElementById("yearform")
    form.submit()
})