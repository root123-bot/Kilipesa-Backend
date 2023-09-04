

https://developer.mozilla.org/en-US/docs/Web/API/XMLHttpRequest/readystatechange_event
document.addEventListener('readystatechange', (e) => {
    if (e.target.readyState === 'complete') {
        $('#fertilizeramount')
            .dropdown({

                onChange: value => {
                    console.log('value ', value)
                }
            })

        $('#seedamount')
            .dropdown({

                onChange: value => {
                    console.log('value ', value)
                }
            });


        $('#totalyield')
            .dropdown({

                onChange: value => {
                    console.log('value ', value)
                }
            });

    }

})