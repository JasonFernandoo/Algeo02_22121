const toggle = document.getElementById("toggle");

toggle.onclick = function() {
    toggle.classList.toggle("texture");
    // ganti class toggle
    if (toggle.classList.contains("color")) {
        toggle.classList.replace("color", "texture");
        toggle.setAttribute("value", "texture");
    }
    else {
        toggle.classList.toggle("color");
        toggle.setAttribute("value", "color");
    }

    const pElements = document.querySelectorAll('p.texture');
    const p1Elements = document.querySelectorAll('p.color');
    // fungsi ubah warna saat indicator diclick
    if(toggle.classList.contains("texture")){
        pElements.forEach(function(p) {
            p.style.color = '#5c71a9';
        });
    }
    else {
        pElements.forEach(function(p) {
            p.style.color = 'white';
        });
    }
    if (toggle.classList.contains("color")) {
        p1Elements.forEach(function(p) {
            p.style.color = '#5c71a9';
    });
    }
    else {
        p1Elements.forEach(function(p) {
            p.style.color = 'white';
        });
    }
}