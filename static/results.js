
const matchedContainer = document.getElementById('skills-container');
const matchedSkills = matchedContainer.dataset.skills.split(', ');
const maxShow = 7;

function renderSkills(container, skills, toggleId, showAll = false) {
    container.innerHTML = '';
    const toShow = showAll ? skills : skills.slice(0, maxShow);
    toShow.forEach(skill => {
        const span = document.createElement('span');
        span.textContent = skill;
        container.appendChild(span);
    });
    const toggle = document.getElementById(toggleId);
    if (skills.length > maxShow) {
        toggle.style.display = 'inline-block';
        toggle.textContent = showAll ? 'Show less' : `...and ${skills.length - maxShow} more`;
    } else {
        toggle.style.display = 'none';
    }
}

// Initial render
renderSkills(matchedContainer, matchedSkills, 'toggle-skills', false);

// Toggle matched skills
document.getElementById('toggle-skills').addEventListener('click', () => {
    const showingAll = document.getElementById('toggle-skills').textContent === 'Show less';
    renderSkills(matchedContainer, matchedSkills, 'toggle-skills', !showingAll);
});

// Missing skills
const missingContainer = document.getElementById('missing-skills-container');
const missingSkills = missingContainer.dataset.skills.split(', ');

// Initial render for missing skills
renderSkills(missingContainer, missingSkills, 'toggle-missing-skills', false);

// Toggle missing skills
document.getElementById('toggle-missing-skills').addEventListener('click', () => {
    const showingAll = document.getElementById('toggle-missing-skills').textContent === 'Show less';
    renderSkills(missingContainer, missingSkills, 'toggle-missing-skills', !showingAll);
});

// Rescan button
const rescanBtn = document.getElementById("rescan-btn");
rescanBtn.addEventListener("click", () => {
    const jd = rescanBtn.dataset.jd || "";
    // Redirect to home route with jd_text as query param
    let redirectUrl = '/';
    if (jd) {
        redirectUrl += `?jd_text=${encodeURIComponent(jd)}`;
    }
    window.location.href = redirectUrl;
});
