const sr = ScrollReveal ({
    distance: '40px' ,
    duration: 2050,
    delay: 200,
    reset: true
});

//home
sr.reveal('.home-text',{origin: 'left'});
sr.reveal('.home-photo',{origin: 'right'});
//about
sr.reveal('.about-text h1', {origin: 'top'});
sr.reveal('.wrapper', {origin: 'bottom'});
//description
sr.reveal('.product, .how-to',{origin: 'left'});
//image
sr.reveal('.container', {origin: 'bottom'});
sr.reveal('.input-img', {origin: 'left'});
sr.reveal('.search-img', {origin: 'right'});