const dropArea = document.getElementById("drop-area");
const inputFile = document.getElementById("input-file");
const imageView = document.getElementById("view-img");
const fileName = document.getElementById("file-name");

// Menggabungkan logika ke dalam satu fungsi
function handleFileSelection(files) {
    let imgLink = URL.createObjectURL(files[0]);
    imageView.style.backgroundImage = `url(${imgLink})`;
    imageView.textContent = "";
    imageView.style.border = 0;

    fileName.textContent = files[0].name;

    // Send the file to the backend
    sendFileToBackend(files[0]);
    dropArea.style.border = "2px dashed #ccc";
}

// Satu event listener untuk elemen inputFile
inputFile.addEventListener("change", function (e) {
    handleFileSelection(e.target.files);
});

// Event listeners untuk elemen dropArea
dropArea.addEventListener("dragover", function (e) {
    e.preventDefault();
    dropArea.style.border = "2px dashed #333";
});

dropArea.addEventListener("drop", function (e) {
    e.preventDefault();
    handleFileSelection(e.dataTransfer.files);
});

function sendFileToBackend(file) {
    const formData = new FormData();
    formData.append("files", file);

    fetch("/upload", {
        method: "POST",
        body: formData,
    })
    // .then(response => response.json())
    // .then(data => {
    //     console.log("File uploaded successfully:", data);
    //     // Handle the response from the backend as needed
    // })
    .catch(error => {
        console.error("Error uploading file:", error);
    });
}
