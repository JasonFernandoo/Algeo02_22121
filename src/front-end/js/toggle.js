const toggle = document.getElementById("toggle");

toggle.onclick = function() {
    toggle.classList.toggle("texture");
    // ganti class toggle
    if (toggle.classList.contains("color")) {
        toggle.classList.replace("color", "texture");
    }
    else {
        toggle.classList.toggle("color");
    }

    const pElements = document.querySelectorAll('p.texture');
    const p1Elements = document.querySelectorAll('p.color');
    // fungsi ubah warna saat indicator diclick
    if(toggle.classList.contains("texture")){
        pElements.forEach(function(p) {
            p.style.background = "linear-gradient(90deg,#00dbde 20%,#fc00ff 70%)";
            p.style.fontFamily = "'Poppins', sans-serif";
            p.style.webkitBackgroundClip = "text";
            p.style.webkitTextFillColor = "transparent";
        });
    }
    else {
        pElements.forEach(function(p) {
            p.style.background = "white";
            p.style.fontFamily = "'Poppins', sans-serif";
            p.style.webkitBackgroundClip = "text";
            p.style.webkitTextFillColor = "transparent";
        });
    }
    if (toggle.classList.contains("color")) {
        p1Elements.forEach(function(p) {
            p.style.background = "linear-gradient(90deg,#00dbde 20%,#fc00ff 70%)";
            p.style.fontFamily = "'Poppins', sans-serif";
            p.style.webkitBackgroundClip = "text";
            p.style.webkitTextFillColor = "transparent";
    });
    }
    else {
        p1Elements.forEach(function(p) {
            p.style.background = "white";
            p.style.fontFamily = "'Poppins', sans-serif";
            p.style.webkitBackgroundClip = "text";
            p.style.webkitTextFillColor = "transparent";
        });
    }
}