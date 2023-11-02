const dropArea = document.getElementById("drop-area");
const inputFile = document.getElementById("input-file");
const imageView = document.getElementById("view-img");

inputFile.addEventListener("change", uploadImage);

let fileName = document.getElementById("file-name");

function uploadImage(){
    //fungsi memunculkan gambar yang diinput
    let imgLink = URL.createObjectURL(inputFile.files[0]);
    imageView.style.backgroundImage = `url(${imgLink}`;
    imageView.textContent = "";
    imageView.style.border = 0;
    // fungsi memunculkan nama file image
    fileName.textContent = inputFile.files[0].name;
}
//fungsi drop image
dropArea.addEventListener("dragover", function(e){
    e.preventDefault();
});
dropArea.addEventListener("drop", function(e){
    e.preventDefault();
    inputFile.files = e.dataTransfer.files;
    uploadImage();
});