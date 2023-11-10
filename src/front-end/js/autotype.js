var message = "MIRROR is a user-friendly website that allows you to upload an image and find visually similar pictures in your choice of database.";
var speed = 50;
var i = 0;

function autoTyper() {
    var textElement = document.getElementById("text");

    if (i < message.length) {
        textElement.innerHTML += message.charAt(i);
        i++;

        setTimeout(autoTyper, speed);
    }
}

function isElementInViewport(element) {
    var rect = element.getBoundingClientRect();
    return (
        rect.top <= (window.innerHeight || document.documentElement.clientHeight) &&
        rect.bottom >= 0
    );
}

window.addEventListener("scroll", function () {
    var descriptionSection = document.getElementById("description");
    var containerDescElements = document.querySelectorAll('.container-desc');
    var timelineAfterElement = document.querySelector('.timeline');

    if (isElementInViewport(descriptionSection) && i === 0) {
        autoTyper();

        // Add animation class to .container-desc elements with delay based on index
        containerDescElements.forEach(function (element, index) {
            element.classList.add('animate-container-desc');
            element.style.animationDelay = index * 1 + "s"; // Adjust the delay based on your preference
        });

        // Add animation class to .timeline::after element
        timelineAfterElement.classList.add('::after');
    }
}, 3000);
        