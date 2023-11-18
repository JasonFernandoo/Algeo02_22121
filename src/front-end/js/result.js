function showResult() {
    const resultTab = document.getElementById('result-tab');
    resultTab.classList.add('shows');
}

document.addEventListener('click', function(event) {
    const resultTab = document.getElementById('result-tab');
    const button = document.getElementById('search');

    if (event.target === button) {
        // Clicking the "Search" button should show the result-tab, but don't hide it.
        showResult();
    } else if (event.target !== resultTab && !resultTab.contains(event.target)) {
        // Clicking outside of the result-tab hides it.
        resultTab.classList.remove('shows');
    }
});