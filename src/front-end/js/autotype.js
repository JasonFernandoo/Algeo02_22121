var message = "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged.";
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

        