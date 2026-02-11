document.addEventListener("DOMContentLoaded", () => {
    const resumeInput = document.getElementById("resume");
    const jdInput = document.querySelector(".job_desc");
    const scanBtn = document.getElementById("scan-btn");
    const fileNameSpan = document.getElementById("file-name");
    const removeFileBtn = document.getElementById("remove-file");
    const helperText = document.getElementById("helper-text");
    const flashError = document.getElementById("flash-error");

    //  AUTO HIDE SERVER ERROR AFTER 3 SECONDS
   if (flashError) {
    setTimeout(() => {
        flashError.style.display = "none";
    }, 3000);
}

    // Clear file input on load
    resumeInput.value = "";
    fileNameSpan.textContent = "Choose PDF";
    removeFileBtn.style.display = "none";

    // Enable Scan button only if JD filled and file selected
    function validateInputs() {
        const hasJD = jdInput.value.trim() !== "";
        const hasPDF = resumeInput.files.length > 0;
        scanBtn.disabled = !(hasJD && hasPDF);
        helperText.style.display = scanBtn.disabled ? "block" : "none";
    }

    // Remove file button
    removeFileBtn.addEventListener("click", () => {
        resumeInput.value = "";
        fileNameSpan.textContent = "Choose PDF";
        removeFileBtn.style.display = "none";
        validateInputs();
    });

    // Update Scan button state on JD input
    jdInput.addEventListener("input", validateInputs);

    // Form submission loader
    document.getElementById("resumeForm").addEventListener("submit", (e) => {
        if (scanBtn.disabled) e.preventDefault();
        document.getElementById("loader").style.display = "flex";
    });

    // Update file name when user selects a file
    resumeInput.addEventListener("change", () => {
        const file = resumeInput.files[0];
        if (file) {
            fileNameSpan.textContent = file.name;
            removeFileBtn.style.display = "inline";
        } else {
            fileNameSpan.textContent = "Choose PDF";
            removeFileBtn.style.display = "none";
        }
        validateInputs();
    });

    validateInputs();
});

// "How it works" timeline dots
const steps = document.querySelectorAll('.step');
const dots = document.querySelectorAll('.dot');

steps.forEach(step => {
    step.addEventListener('mouseenter', () => {
        const index = step.dataset.index;
        dots.forEach(dot => dot.classList.remove('filled'));
        dots[index].classList.add('filled');
    });

    step.addEventListener('mouseleave', () => {
        dots.forEach(dot => dot.classList.remove('filled'));
    });
});
