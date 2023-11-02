const text = document.querySelector(".title-text");

const textLoad = () => {
    // fungsi judul ketikan
    setTimeout(() => {
        text.textContent = "Tugas Besar Algeo";
    }, 0);
    setTimeout(() => {
        text.textContent = "Now You See Us";
    }, 5000);
}

textLoad();
setInterval(textLoad, 10000);