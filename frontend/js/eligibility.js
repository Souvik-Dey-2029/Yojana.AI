/**
 * Yojana.AI - Eligibility Step-Form Logic
 * Handles multi-step navigation, Aadhaar OCR integration, and final profile submission.
 */
document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('eligibility-form');
    const steps = document.querySelectorAll('.step');
    const progressBar = document.getElementById('progress-bar');
    let currentStep = 1;

    const updateUI = () => {
        steps.forEach((step, idx) => {
            step.classList.toggle('active', idx + 1 === currentStep);
        });
        progressBar.style.width = `${(currentStep / steps.length) * 100}%`;
    };

    document.querySelectorAll('.next-step').forEach(btn => {
        btn.addEventListener('click', () => {
            if (currentStep < steps.length) {
                currentStep++;
                updateUI();
            }
        });
    });

    document.querySelectorAll('.prev-step').forEach(btn => {
        btn.addEventListener('click', () => {
            if (currentStep > 1) {
                currentStep--;
                updateUI();
            }
        });
    });

    // OCR Auto-fill
    const ocrUpload = document.getElementById('ocr-upload');
    const ocrStatus = document.getElementById('ocr-status');

    ocrUpload.addEventListener('change', async (e) => {
        const file = e.target.files[0];
        if (!file) return;

        ocrStatus.innerText = "Extracting data... Please wait.";
        ocrStatus.style.color = "var(--primary)";

        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch('/api/ocr-extract', {
                method: 'POST',
                body: formData
            });
            const result = await response.json();

            if (result.extracted) {
                const data = result.extracted;
                if (data.name) document.getElementById('name').value = data.name;
                if (data.age) document.getElementById('age').value = data.age;
                if (data.gender) document.getElementById('gender').value = data.gender;

                ocrStatus.innerText = "✅ Form auto-filled successfully!";
                ocrStatus.style.color = "var(--accent)";
            }
            if (result.warning) {
                console.warn(result.warning);
                ocrStatus.innerText = "⚠️ " + result.warning;
            }
        } catch (error) {
            console.error("OCR Error:", error);
            ocrStatus.innerText = "❌ OCR extraction failed.";
            ocrStatus.style.color = "#ef4444";
        }
    });

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const formData = {
            name: document.getElementById('name').value,
            age: parseInt(document.getElementById('age').value),
            gender: document.getElementById('gender').value,
            state: document.getElementById('state').value,
            category: document.getElementById('category').value,
            income_lpa: parseFloat(document.getElementById('income').value),
            land_owned: document.querySelector('input[name="land"]:checked').value === 'true',
            occupation: document.getElementById('occupation').value,
            education: document.getElementById('education').value,
            disability: document.querySelector('input[name="disability"]:checked').value === 'true',
            language: document.getElementById('language').value
        };

        try {
            const response = await fetch('/api/eligibility', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData)
            });

            const result = await response.json();

            // Store profile for personalized guide names and API fetch
            localStorage.setItem('userProfile', JSON.stringify(formData));
            localStorage.setItem('eligibilityResults', JSON.stringify(result.eligible_schemes));
            localStorage.setItem('userLanguage', formData.language);

            window.location.href = 'results.html';
        } catch (error) {
            console.error('Error:', error);
            alert('Something went wrong. Please try again.');
        }
    });
});
