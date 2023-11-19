document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('form1');
    const button = document.getElementById('search');
    const resultTab = document.getElementById('result-tab');

    // Click event listener for the "Search" button
    button.addEventListener('click', function (event) {
        // Prevent the default form submission behavior
        event.preventDefault();

        // Serialize form data
        const formData = new FormData(form);

        // Perform AJAX submission
        fetch(form.action, {
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

    // Function to handle the received image data and display it with pagination
    function handleImageData(data) {
        var startTime = performance.now();

        // Get the image container
        var container = document.getElementById("imageContainer");
        container.innerHTML = ""; // Clear existing images

        // Create an img element for each image URL
        data.forEach(function (item) {
            var img = document.createElement("img");
            img.src = item.image_url;
            container.appendChild(img);
        });

        // Display pagination
        displayPagination(data);

        var endTime = performance.now();
        var runtime = endTime - startTime;
        console.log("API fetch runtime: " + runtime + " milliseconds");
    }

    // Function to display pagination
    function displayPagination(data) {
        var container = document.getElementById("pagination");
        var itemsPerPage = 6;
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
            var img = document.createElement("img");
            img.src = item.image_url;
            container.appendChild(img);
        });
    }
});
