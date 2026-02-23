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
        console.log("DEBUG: Starting OCR Extraction for file:", file.name);

        const formData = new FormData();
        formData.append('file', file);

        try {
            // Add a timeout controller
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), 10000); // 10s timeout

            const response = await fetch('/api/ocr-extract', {
                method: 'POST',
                body: formData,
                signal: controller.signal
            });
            clearTimeout(timeoutId);

            const result = await response.json();
            console.log("DEBUG: OCR Backend Response:", result);

            if (result.extracted) {
                const data = result.extracted;
                console.log("DEBUG: Auto-filling fields:", data);
                if (data.name) document.getElementById('name').value = data.name;
                if (data.age) document.getElementById('age').value = data.age;
                if (data.gender) document.getElementById('gender').value = data.gender;

                if (result.status === "fallback") {
                    ocrStatus.innerText = "⚠️ Using Intelligent Demo Data (OCR engine not linked yet).";
                    ocrStatus.style.color = "#f59e0b"; // Amber
                } else {
                    ocrStatus.innerText = "✅ AI OCR: Form auto-filled successfully!";
                    ocrStatus.style.color = "var(--accent)";
                }
            } else if (result.status === "error") {
                console.error("DEBUG: OCR Backend Error:", result.message);
                ocrStatus.innerText = "❌ " + result.message;
                ocrStatus.style.color = "#ef4444";
            }
        } catch (error) {
            console.error("DEBUG: OCR Frontend Error:", error);
            if (error.name === 'AbortError') {
                ocrStatus.innerText = "⚠️ OCR Timed out. Setting demo data for speed.";
                // Trigger demo data locally if timeout happens
                document.getElementById('name').value = "Souvik Dey";
                document.getElementById('age').value = 28;
                document.getElementById('gender').value = "Male";
                ocrStatus.style.color = "#f59e0b";
            } else {
                ocrStatus.innerText = "❌ Network Error: Could not reach OCR engine.";
                ocrStatus.style.color = "#ef4444";
            }
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
