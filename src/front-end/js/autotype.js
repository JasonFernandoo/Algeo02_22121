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
        
            if (isElementInViewport(descriptionSection) && i === 0) {
                autoTyper();
            }
        });

        