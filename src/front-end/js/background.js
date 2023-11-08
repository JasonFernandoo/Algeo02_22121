const bg = document.getElementById('home');

window.addEventListener('scroll', function(){
    bg.style.backgroundSize = 160 - +window.scrollY / 12 + '%';
    bg.style.opacity = 1 - +window.scrollY / 700 + '';
})