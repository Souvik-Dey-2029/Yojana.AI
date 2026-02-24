/**
 * Yojana.AI - Eligibility Step-Form Logic
 * Handles multi-step navigation and final profile submission.
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
        if (progressBar) {
            const progress = (currentStep / steps.length) * 100;
            progressBar.style.width = `${progress}%`;
        }
    };

    updateUI(); // Initial call to show progress for step 1

    const validateStep = (stepNum) => {
        const currentStepEl = document.getElementById(`step-${stepNum}`);
        const inputs = currentStepEl.querySelectorAll('input[required], select[required]');
        let isValid = true;
        inputs.forEach(input => {
            if (!input.value) {
                input.style.borderColor = 'red';
                isValid = false;
            } else {
                input.style.borderColor = 'var(--glass-border)';
            }
        });
        return isValid;
    };

    document.querySelectorAll('.next-step').forEach(btn => {
        btn.addEventListener('click', () => {
            if (validateStep(currentStep)) {
                if (currentStep < steps.length) {
                    currentStep++;
                    updateUI();
                }
            } else {
                const activeStep = document.querySelector('.step.active');
                activeStep.classList.add('shake');
                setTimeout(() => activeStep.classList.remove('shake'), 500);
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

    // Submit Logic
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const submitBtn = form.querySelector('button[type="submit"]');
        const originalText = submitBtn.textContent;

        // Loading state
        submitBtn.disabled = true;
        submitBtn.textContent = "Analyzing your profile...";

        const formData = {
            name: document.getElementById('name').value || "User",
            age: parseInt(document.getElementById('age').value) || 0,
            gender: document.getElementById('gender').value || "Other",
            state: document.getElementById('state').value || "Other (National)",
            category: document.getElementById('category').value || "General",
            income_lpa: parseFloat(document.getElementById('income').value) || 0,
            land_owned: document.querySelector('input[name="land"]:checked')?.value === 'true',
            occupation: document.getElementById('occupation').value || "Unemployed",
            education: document.getElementById('education').value || "10th",
            disability: document.querySelector('input[name="disability"]:checked')?.value === 'true',
            language: document.getElementById('language').value || "en"
        };

        try {
            const response = await fetch('/api/eligibility', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData)
            });

            if (!response.ok) throw new Error('API Error');

            const result = await response.json();

            // Store profile for personalized guide names and API fetch
            localStorage.setItem('userProfile', JSON.stringify(formData));
            localStorage.setItem('eligibilityResults', JSON.stringify(result.eligible_schemes));
            localStorage.setItem('userLanguage', formData.language);

            window.location.href = 'results.html';
        } catch (error) {
            console.error('Error:', error);
            alert('Something went wrong. Please try again.');
            submitBtn.disabled = false;
            submitBtn.textContent = originalText;
        }
    });
});
