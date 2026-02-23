/**
 * Yojana.AI - Results Display Logic
 * Fetches personalized schemes from the engine, handles real-time search,
 * and manages multilingual translation for scheme details.
 */
document.addEventListener('DOMContentLoaded', async () => {
    const grid = document.getElementById('schemes-grid');
    const headline = document.getElementById('results-headline');
    const langToggle = document.getElementById('lang-toggle');

    const userProfile = JSON.parse(localStorage.getItem('userProfile'));

    if (!userProfile) {
        window.location.href = 'eligibility.html';
        return;
    }

    // Set initial language toggle
    langToggle.value = userProfile.language;

    async function fetchResults(profile) {
        grid.innerHTML = '<div class="loading-state"><div class="spinner"></div><p>Analyzing eligibility...</p></div>';

        try {
            const response = await fetch('/api/eligibility', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(profile)
            });

            if (!response.ok) throw new Error('API Error');

            const data = await response.json();
            renderSchemes(data.eligible_schemes);
        } catch (error) {
            console.error(error);
            grid.innerHTML = '<p style="color:red; grid-column:1/-1; text-align:center;">Error connecting to Yojana AI engine. Make sure backend is running.</p>';
        }
    }

    function renderSchemes(schemes) {
        if (!schemes || schemes.length === 0) {
            headline.innerText = "No Schemes Found";
            grid.innerHTML = '<p style="grid-column:1/-1; text-align:center;">Sorry, we couldn\'t find any matching schemes for your profile currently.</p>';
            return;
        }

        headline.innerText = `${schemes.length} Schemes Found`;
        grid.innerHTML = '';

        schemes.forEach((scheme, index) => {
            const card = document.createElement('div');
            card.className = 'scheme-card glass animate-fade-in';
            card.style.animationDelay = `${index * 0.1}s`;
            card.innerHTML = `
                <div class="scheme-icon-wrapper">${scheme.icon || '📋'}</div>
                <h3>${scheme.name}</h3>
                <p>${scheme.description}</p>
                <div class="benefits">${scheme.benefits}</div>
                <div class="docs-title">Required Documents</div>
                <ul class="docs-list">
                    ${scheme.required_documents.map(doc => `<li>${doc}</li>`).join('')}
                </ul>
                <div class="card-footer" style="flex-wrap: wrap; gap: 0.5rem;">
                    <span class="deadline" style="width: 100%; margin-bottom: 0.5rem;">Deadline: ${scheme.deadline}</span>
                    <a href="${scheme.apply_url}" target="_blank" class="btn btn-primary" style="padding: 0.5rem 1rem; font-size: 0.85rem; flex: 1;">Apply Now</a>
                    <button onclick="downloadPDFGuide('${scheme.id}', '${userProfile.name}')" id="btn-guide-${scheme.id}" class="btn glass" style="padding: 0.5rem 1rem; font-size: 0.85rem; flex: 1; border-color: var(--primary); color: white;">Download Guide</button>
                </div>
            `;
            grid.appendChild(card);
        });
    }

    // PDF Download Helper
    window.downloadPDFGuide = async (schemeId, userName) => {
        const btn = document.getElementById(`btn-guide-${schemeId}`);
        const originalText = btn.innerText;
        btn.innerText = "Generating...";
        btn.disabled = true;

        try {
            const response = await fetch(`/api/download-guide/${schemeId}?name=${encodeURIComponent(userName)}`);
            if (!response.ok) throw new Error("PDF generation failed");

            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `${schemeId}_AI_Guide.pdf`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            btn.innerText = "Check your downloads!";
            setTimeout(() => {
                btn.innerText = originalText;
                btn.disabled = false;
            }, 3000);
        } catch (error) {
            console.error(error);
            btn.innerText = "❌ Error";
            btn.style.borderColor = "#ef4444";
            setTimeout(() => {
                btn.innerText = originalText;
                btn.disabled = false;
                btn.style.borderColor = "var(--primary)";
            }, 3000);
        }
    };

    // Search Functionality
    const searchInput = document.getElementById('scheme-search');

    function applySearchFilter() {
        const term = searchInput.value.toLowerCase();
        const cards = document.querySelectorAll('.scheme-card');
        cards.forEach(card => {
            const name = card.querySelector('h3').innerText.toLowerCase();
            const desc = card.querySelector('p').innerText.toLowerCase();
            if (name.includes(term) || desc.includes(term)) {
                card.style.display = 'flex';
            } else {
                card.style.display = 'none';
            }
        });
    }

    if (searchInput) {
        searchInput.addEventListener('input', applySearchFilter);
    }

    // Translation logic
    langToggle.addEventListener('change', async (e) => {
        const selectedLang = langToggle.value;
        userProfile.language = selectedLang;
        localStorage.setItem('userProfile', JSON.stringify(userProfile));
        localStorage.setItem('userLanguage', selectedLang);
        fetchResults(userProfile);
    });

    // Initial fetch
    fetchResults(userProfile);
});
