// Get references to the video, canvas, and image elements
const cameraFeed = document.getElementById('cameraFeed');
const countdownOverlay = document.getElementById('countdownOverlay');
const capturedCanvas = document.getElementById('capturedCanvas');
const capturedImage = document.getElementById('capturedImage');

// Declare captureInterval in an accessible scope
let captureInterval;
let shouldCapture = true; // Flag to determine if captureImage should execute
let cameraStream; // Reference to the camera stream

// Function to capture an image from the camera
function captureImage() {
    if (!shouldCapture) {
        return; // Do not capture image if shouldCapture is false
    }

    // Ensure the canvas dimensions match the video dimensions
    capturedCanvas.width = cameraFeed.videoWidth;
    capturedCanvas.height = cameraFeed.videoHeight;

    // Draw the current frame from the video feed onto the canvas
    const context = capturedCanvas.getContext('2d');
    context.drawImage(cameraFeed, 0, 0, capturedCanvas.width, capturedCanvas.height);
}

// Function to display countdown overlay
function displayCountdownOverlay(seconds) {
    countdownOverlay.style.display = 'block';

    function updateCountdown() {
        if (!shouldCapture) {
            clearInterval(captureInterval);
            countdownOverlay.style.display = 'none';
            
            // Stop the camera stream
            if (cameraStream) {
                cameraStream.getTracks().forEach(track => track.stop());
            }

            return; // Stop countdown if shouldCapture is false
        }

        countdownOverlay.textContent = `${seconds}`;
        seconds--;

        if (seconds < 0) {
            clearInterval(captureInterval);
            countdownOverlay.style.display = 'none';

            // Capture an image when the countdown reaches 0
            captureImage();

            // Show the canvas
            capturedCanvas.style.display = 'block';
        }
    }

    updateCountdown(); // Initial update
    captureInterval = setInterval(updateCountdown, 500);
}

// Set up a click event listener for the button
document.getElementById('captureButton').addEventListener('click', () => {
    // Access the user's camera
    navigator.mediaDevices.getUserMedia({ video: true })
        .then((stream) => {
            // Set the video element's source to the camera stream
            cameraFeed.srcObject = stream;

            // Save the reference to the camera stream
            cameraStream = stream;

            // Play the video
            cameraFeed.play();

            // Show the canvas initially
            capturedCanvas.style.display = 'block';

            // Wait for the metadata to be loaded before capturing the initial image
            cameraFeed.addEventListener('loadedmetadata', () => {
                captureImage();
            });

            // Set up an interval to capture an image every 5 seconds
            captureInterval = setInterval(() => {
                displayCountdownOverlay(5);
            }, 5000);
        })
        .catch((error) => {
            console.error('Error accessing camera:', error);
        });
});

function showCamera() {
    const cameraContainer = document.getElementById('cameraContainer');
    cameraContainer.classList.add('show');
    shouldCapture = true; // Reset the flag when showing the camera
}

document.addEventListener('click', function(event) {
    const cameraContainer = document.getElementById('cameraContainer');
    const button = document.getElementById('captureButton');
    const resultTab = document.getElementById('result-tab');

    if (event.target === button) {
        // Clicking the "Search" button should show the result-tab, but don't hide it.
        showCamera();
        resultTab.classList.add('show');
    } else if (event.target !== cameraContainer && !cameraContainer.contains(event.target)) {
        // Clicking outside of the result-tab hides it and stops capturing
        cameraContainer.classList.remove('show');
        clearInterval(captureInterval);
        shouldCapture = false; // Set the flag to false when clicking outside
    }
});
