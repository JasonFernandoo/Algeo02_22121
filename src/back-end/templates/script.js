fetch('/calculate', {
    method: 'POST', // or 'POST' based on your requirement
    mode: 'no-cors',
})
    .then(response => {
        // Handle the response
    })
    .catch(error => {
        console.error('Error:', error);
    });
