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

console.log("main.js loaded");

window.changeLanguage = function (lang) {
    if (typeof translations === 'undefined') {
        console.error("Translations not loaded");
        return;
    }

    // Update Site Title
    const titleKey = document.querySelector('h1[data-key]').getAttribute('data-key');
    if (translations[titleKey] && translations[titleKey][lang]) {
        document.querySelector('h1[data-key]').textContent = translations[titleKey][lang];
    }

    // Update Last Updated Label
    const lastUpdatedKey = document.querySelector('span[data-key="last_updated_label"]').getAttribute('data-key');
    if (translations[lastUpdatedKey] && translations[lastUpdatedKey][lang]) {
        document.querySelector('span[data-key="last_updated_label"]').textContent = translations[lastUpdatedKey][lang];
    }

    // Update Tab Buttons
    const buttons = document.querySelectorAll('.tab-button[data-key]');
    buttons.forEach(btn => {
        const key = btn.getAttribute('data-key');
        if (translations.tabs[key] && translations.tabs[key][lang]) {
            btn.textContent = translations.tabs[key][lang];
        }
    });

    // Save preference (optional, implementing for better UX)
    localStorage.setItem('preferredLanguage', lang);
}

function detectUserLanguage() {
    const lang = navigator.language || navigator.userLanguage;
    if (!lang) return null;

    const code = lang.toLowerCase();

    if (code.startsWith('zh')) return 'TC'; // Simplified or Traditional, default to TC for this app
    if (code.startsWith('ko')) return 'KR';
    if (code.startsWith('ja')) return 'JP';
    if (code.startsWith('en')) return 'EN';

    return null; // Fallback to default (TC) if unknown
}

// Load saved language or auto-detect or default to TC
const savedLang = localStorage.getItem('preferredLanguage') || detectUserLanguage() || 'TC';

// We need to wait for DOM to be ready to run changeLanguage if we want to set initial state purely by JS,
// but since the server renders TC by default, we only need to change if savedLang != TC.
if (savedLang !== 'TC') {
    // Wrap in DOMContentLoaded to ensure elements exist
    document.addEventListener('DOMContentLoaded', () => {
        changeLanguage(savedLang);
    });
}
// Sort Toggle Logic
let currentSortOrder = 'desc'; // Default state

function toggleSort() {
    currentSortOrder = currentSortOrder === 'desc' ? 'asc' : 'desc';
    sortVideos(currentSortOrder);
    updateSortButton();
}

function updateSortButton() {
    const btn = document.getElementById('sortToggle');
    if (!btn) return;

    // ⬇️ = Descending (Newest First)
    // ⬆️ = Ascending (Oldest First)
    if (currentSortOrder === 'desc') {
        btn.textContent = '📅 ⬇️ Date';
    } else {
        btn.textContent = '📅 ⬆️ Date';
    }
}

function sortVideos(order) {
    // Select ALL sections, not just the active one
    const sections = document.querySelectorAll('.sheet-section');

    sections.forEach(section => {
        const container = section.querySelector('.content-container');
        if (!container) return;

        const groups = Array.from(container.getElementsByClassName('date-group'));

        groups.sort((a, b) => {
            const dateA = a.getAttribute('data-date') || '';
            const dateB = b.getAttribute('data-date') || '';

            // Simple string comparison for YYYY-MM-DD works
            if (order === 'asc') {
                return dateA.localeCompare(dateB);
            } else {
                return dateB.localeCompare(dateA);
            }
        });

        // Re-append sorted elements
        groups.forEach(group => container.appendChild(group));
    });
}
