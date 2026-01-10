function openVideo(videoId) {
    const modal = document.getElementById("videoModal");
    const container = document.getElementById("playerContainer");

    // Clear previous content
    container.innerHTML = '';

    // Inject iframe
    const iframe = document.createElement("iframe");
    iframe.src = `https://www.youtube.com/embed/${videoId}?autoplay=1`;
    iframe.allow = "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture";
    iframe.allowFullscreen = true;

    container.appendChild(iframe);

    modal.style.display = "flex";
}

function closeVideo() {
    const modal = document.getElementById("videoModal");
    const container = document.getElementById("playerContainer");

    modal.style.display = "none";
    container.innerHTML = ''; // Stop video playback
}

// Close modal when clicking outside
window.onclick = function (event) {
    const modal = document.getElementById("videoModal");
    if (event.target == modal) {
        closeVideo();
    }
}

function openTab(evt, sheetName) {
    // Hide all sheet sections
    const sections = document.getElementsByClassName("sheet-section");
    for (let i = 0; i < sections.length; i++) {
        sections[i].classList.remove("active");
    }

    // Deactivate all buttons
    const tabButtons = document.getElementsByClassName("tab-button");
    for (let i = 0; i < tabButtons.length; i++) {
        tabButtons[i].classList.remove("active");
    }

    // Show current sheet and activate button
    document.getElementById(sheetName).classList.add("active");
    evt.currentTarget.classList.add("active");
}
