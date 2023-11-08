document.getElementById('uploadButton').addEventListener('click', function () {
    document.getElementById('folderInput').click();
});

document.getElementById('folderInput').addEventListener('change', function () {
    // Handle the selected folder and its contents here
    const selectedFiles = this.files;
    if (selectedFiles.length > 0) {
        // You can access the selected folder's contents using selectedFiles
        // For example, you can loop through the files and process them
        for (let i = 0; i < selectedFiles.length; i++) {
            const file = selectedFiles[i];
            // Do something with the file, e.g., display or upload it
            console.log(file.name);
        }
    }
});