document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('form1');
    const button = document.getElementById('search');
    const resultTab = document.getElementById('result-tab');

    // Click event listener for the "Search" button
    button.addEventListener('click', async function (event) {
        // Prevent the default form submission behavior
        event.preventDefault();

        await fetchImage();
        // Serialize form data
        const formData = new FormData(form);

        // Perform AJAX submission
        await fetch(form.action, {
            method: form.method,
            body: formData
        })
        .then(response => {
            if (response.ok) {
                return response.json(); // Assuming the server returns JSON
            } else {
                throw new Error('Form submission failed.');
            }
        })
        .then(data => {
            // Handle the response from the server if needed
            console.log(data);

            // Show the result tab
            resultTab.classList.add('shows');

            // Process the data and display images with pagination
            handleImageData(data);
        })
        .catch(error => {
            console.error(error);
        });
    });

    // Click event listener for hiding the result tab
    document.addEventListener('click', function (event) {
        if (event.target === button) {
            // Clicking the "Search" button should show the result-tab, but don't hide it.
            resultTab.classList.add('shows');
        } else if (event.target !== resultTab && !resultTab.contains(event.target)) {
            // Clicking outside of the result-tab hides it.
            resultTab.classList.remove('shows');
        }
    });

    var startTime = performance.now();
    var runtimeDisplay = document.getElementById('runtime-display');
    var totalimages = document.getElementById('total-images');

    async function fetchImage(){
        const toggle = document.getElementById("toggle")
        console.log("cek");
        if (toggle.classList.contains("color")){
            console.log("color1");
            await fetchColor();
        } else {
            console.log("TEKSTUR1");
            await fetchTexture();
        }
    }

    async function fetchTexture(){
        console.log("TEKSTUR");
        var startTime = performance.now();
        await fetch("/texture", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
        })
        .then((response) => response.json())
        .then((data) => {
            if (data) {
                console.log(data);
                var endTime = performance.now();
                var runtime = endTime - startTime;
                
                runtimeDisplay.textContent = runtime.toFixed(2);
                totalimages.textContent = data.length + " Images";
                // Get the image container
                var container = document.getElementById("imageContainer");
                while (container.firstChild) { container.removeChild (container.firstChild); }

                
                // Create an img element for each image URL
                data.forEach(function (item) {
                    var div = document.createElement("div");
                    var p = document.createElement("p");
                    var img = document.createElement("img");
                    img.src = item.image_url;
                    p.textContent = item.similarity.toFixed(2);
                    div.appendChild(img);
                    div.appendChild(p);
                    container.appendChild(div);
                });
                
                // Display pagination
                displayPagination(data);
                
                console.log("API fetch runtime: " + runtime + " milliseconds");
            }
        })
        .catch((error) => {
            // Handle the error
            console.error("Error:", error);
        });
    }

    async function fetchColor(){
        var startTime = performance.now();
        await fetch("/color", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
        })
        .then((response) => response.json())
        .then((data) => {
            if (data) {
                var endTime = performance.now();
                var runtime = endTime - startTime;
                
                runtimeDisplay.textContent = runtime.toFixed(2);
                totalimages.textContent = data.length + " Images";
                // Get the image container
                var container = document.getElementById("imageContainer");
                while (container.firstChild) { container.removeChild (container.firstChild); }

                
                // Create an img element for each image URL
                data.forEach(function (item) {
                    var div = document.createElement("div");
                    var p = document.createElement("p");
                    var img = document.createElement("img");
                    img.src = item.image_url;
                    p.textContent = item.similarity.toFixed(2);
                    div.appendChild(img);
                    div.appendChild(p);
                    container.appendChild(div);
                });
                
                // Display pagination
                displayPagination(data);
                
                console.log("API fetch runtime: " + runtime + " milliseconds");
            }
        })
        .catch((error) => {
            // Handle the error
            console.error("Error:", error);
        });
    }

        

        // Function to display pagination
    function displayPagination(data) {
        var container = document.getElementById("pagination");
        var itemsPerPage = 12;
        var totalPages = Math.ceil(data.length / itemsPerPage);

        for (var i = 1; i <= totalPages; i++) {
            var pageButton = document.createElement("button");
            pageButton.textContent = i;

            pageButton.addEventListener("click", function () {
                var currentPage = parseInt(this.textContent);
                showImagesPerPage(data, currentPage, itemsPerPage);
            });

            container.appendChild(pageButton);
        }

        // Show the first page by default
        showImagesPerPage(data, 1, itemsPerPage);
    }

    // Function to show images for a specific page
    function showImagesPerPage(data, currentPage, itemsPerPage) {
        var container = document.getElementById("imageContainer");
        container.innerHTML = ""; // Clear existing images

        var startIndex = (currentPage - 1) * itemsPerPage;
        var endIndex = startIndex + itemsPerPage;

        var pageImages = data.slice(startIndex, endIndex);

        // Create an img element for each image URL
        pageImages.forEach(function (item) {
            var div = document.createElement("div");
            var p = document.createElement("p");
            var img = document.createElement("img");
            img.src = item.image_url;
            p.textContent = item.similarity.toFixed(2);
            div.appendChild(img);
            div.appendChild(p);
            container.appendChild(div);
        });
    }
});

