
let first = document.getElementById('firstsection')
let second = document.getElementById('secsection')
let prevbtn = document.getElementById("prevbtn")
let nextbtn = document.getElementById("nextbtn")
let submitbtn = document.getElementById('submitbtn')
console.log(prevbtn.style.display, nextbtn.style.display)
// initially script should make the prev disappear


nextbtn.addEventListener('click', (e) => {
    e.preventDefault()
    second.style.display = 'block'
    first.style.display = 'none'

    nextbtn.style.display = 'none'
    prevbtn.style.display = 'inline'

    // lets display the submit button..
    submitbtn.style.display = 'block'
})

prevbtn.addEventListener('click', (e) => {
    e.preventDefault()
    first.style.display = 'block'
    second.style.display = 'none'
    nextbtn.style.display = 'inline'
    prevbtn.style.display = 'none'

    // lets not display the submit button..
    submitbtn.style.display = 'none'
})

