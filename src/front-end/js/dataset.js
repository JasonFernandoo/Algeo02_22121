document.getElementById('uploadButton').addEventListener('click', function () {
    document.getElementById('datasetInput').click();
});

document.getElementById('datasetInput').addEventListener('change', function () {
    const selectedFiles = this.files;
    if (selectedFiles.length > 0) {
        // Handle the selected folder and its contents here
        // You can use FormData to send the files to the server
        const formData = new FormData();

        for (let i = 0; i < selectedFiles.length; i++) {
            const file = selectedFiles[i];
            // Append each file to the FormData object with the same key
            formData.append('files[]', file);
        }

        // Send the FormData object to the server using fetch
        fetch('/upload-folder', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (response.ok) {
                return response.json(); // Assuming the server returns JSON
            } else {
                throw new Error('Folder upload failed.');
            }
        })
        .then(data => {
            // Handle the response from the server if needed
            console.log(data);
        })
        .catch(error => {
            console.error(error);
        });
    }
});
