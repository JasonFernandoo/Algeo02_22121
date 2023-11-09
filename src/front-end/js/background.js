const bg = document.getElementById('home');

window.addEventListener('scroll', function(){
    bg.style.backgroundSize = 110 - +window.scrollY / 57 + '%';
    bg.style.opacity = 1 - +window.scrollY / 700 + '';
})