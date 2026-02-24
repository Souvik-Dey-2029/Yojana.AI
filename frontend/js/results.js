/**
 * Yojana.AI - Results Display Logic
 */
document.addEventListener('DOMContentLoaded', async () => {
    const grid = document.getElementById('schemes-grid');
    const headline = document.getElementById('results-headline');
    const langToggle = document.getElementById('lang-toggle');
    const searchInput = document.getElementById('scheme-search');

    if (!grid || !headline) {
        console.error("DEBUG: Essential elements (grid or headline) missing. Aborting.");
        return;
    }

    let userProfile = JSON.parse(localStorage.getItem('userProfile'));

    if (!userProfile) {
        window.location.href = 'eligibility.html';
        return;
    }

    let currentSchemes = []; // Local cache of eligible schemes

    // Application Success Analyzer Logic
    const analyzerSection = document.getElementById('analyzer-section');
    const runAnalysisBtn = document.getElementById('run-analysis');
    let complianceData = null;

    if (runAnalysisBtn) {
        runAnalysisBtn.addEventListener('click', async () => {
            const form = document.getElementById('compliance-form');
            const formData = new FormData(form);
            const data = {};
            formData.forEach((value, key) => data[key] = parseInt(value));

            runAnalysisBtn.innerText = "Analyzing Risks...";
            runAnalysisBtn.disabled = true;

            try {
                const res = await fetch('/api/predict-application-success', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
                if (!res.ok) throw new Error("Prediction API Error");

                complianceData = await res.json();
                console.log("DEBUG: Compliance Data received:", complianceData);

                // Refresh rendering with new data
                applyFiltersAndRender();
                runAnalysisBtn.innerText = "Re-Calculate Probability";
            } catch (e) {
                console.error("DEBUG: Prediction Error:", e);
                runAnalysisBtn.innerText = "❌ Error. Try Again";
            } finally {
                runAnalysisBtn.disabled = false;
            }
        });
    }

    async function fetchResults(profile) {
        console.log("DEBUG: Fetching results for:", profile.name, "Lang:", profile.language);
        grid.innerHTML = `
            <div class="loading-state" style="grid-column: 1/-1; text-align: center; padding: 4rem;">
                <div class="spinner" style="margin: 0 auto 1.5rem;"></div>
                <p>Analyzing eligibility for ${profile.name}...</p>
            </div>`;

        try {
            const response = await fetch('/api/eligibility', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(profile)
            });

            if (!response.ok) throw new Error('API Error');

            const data = await response.json();
            currentSchemes = data.eligible_schemes;

            // Show analyzer section if schemes found
            if (currentSchemes.length > 0 && analyzerSection) {
                analyzerSection.style.display = 'block';
            }

            applyFiltersAndRender();
        } catch (error) {
            console.error("DEBUG: Fetch Error:", error);
            grid.innerHTML = '<p style="color:#ef4444; grid-column:1/-1; text-align:center;">❌ Error connecting to Yojana AI engine. Please refresh or check your connection.</p>';
        }
    }

    function applyFiltersAndRender() {
        if (!searchInput) return;
        const term = searchInput.value.toLowerCase();
        const sortSelect = document.getElementById('scheme-sort');
        const sortCriteria = sortSelect ? sortSelect.value : 'relevance';

        console.log("DEBUG: Applying filters. Term:", term, "Sort:", sortCriteria);

        // 1. Search Filter
        let filtered = currentSchemes.filter(s => {
            const name = (s.name || "").toLowerCase();
            const desc = (s.description || "").toLowerCase();
            const benefits = (s.benefits || "").toLowerCase();
            return name.includes(term) || desc.includes(term) || benefits.includes(term);
        });

        // 2. Sort
        if (sortCriteria === 'popularity') {
            filtered.sort((a, b) => (b.popularity || 0) - (a.popularity || 0));
        }

        renderSchemes(filtered);
    }

    function renderSchemes(schemes) {
        if (!schemes || schemes.length === 0) {
            headline.innerText = "No Schemes Found";
            grid.innerHTML = '<p style="grid-column:1/-1; text-align:center; padding: 3rem; opacity: 0.7;">Sorry, we couldn\'t find any matching schemes for your profile currently. Try adjusting your details.</p>';
            if (analyzerSection) analyzerSection.style.display = 'none';
            return;
        }

        headline.innerText = `${schemes.length} Schemes Found`;
        grid.innerHTML = '';

        schemes.forEach((scheme, index) => {
            const card = document.createElement('div');
            card.className = 'scheme-card glass animate-fade-in';
            card.style.animationDelay = `${index * 0.05}s`;

            let riskBadge = '';
            let suggestionBox = '';

            if (complianceData) {
                const color = complianceData.risk_level === 'LOW' ? '#22c55e' : (complianceData.risk_level === 'MEDIUM' ? '#eab308' : '#ef4444');
                riskBadge = `
                    <div class="risk-badge" style="position: absolute; top: 1rem; right: 1rem; padding: 0.4rem 0.8rem; border-radius: 1rem; background: ${color}22; border: 1px solid ${color}; color: ${color}; font-size: 0.75rem; font-weight: 600;">
                        ${complianceData.score}% Approval
                    </div>
                `;

                if (complianceData.risk_level !== 'LOW' && complianceData.suggestions.length > 0) {
                    suggestionBox = `
                        <div class="ai-suggestions" style="margin-top: 1rem; padding: 0.8rem; border-radius: 0.8rem; background: rgba(255,255,255,0.03); border: 1px dashed rgba(255,255,255,0.1);">
                            <div style="font-size: 0.7rem; color: ${color}; font-weight: 600; margin-bottom: 0.4rem; display: flex; align-items: center; gap: 0.3rem;">
                                <span>⚡</span> AI COMPLIANCE SUGGESTIONS
                            </div>
                            <ul style="font-size: 0.7rem; opacity: 0.8; padding-left: 1rem; margin: 0;">
                                ${complianceData.suggestions.map(s => `<li>${s}</li>`).join('')}
                            </ul>
                        </div>
                    `;
                }
            }

            card.innerHTML = `
                ${riskBadge}
                <div class="scheme-icon-wrapper">${scheme.icon || '📜'}</div>
                <h3>${scheme.name}</h3>
                <p>${scheme.description}</p>
                <div class="benefits">${scheme.benefits}</div>
                ${suggestionBox}
                <div class="docs-title">Required Documents</div>
                <ul class="docs-list">
                    ${scheme.required_documents.map(doc => `<li>${doc}</li>`).join('')}
                </ul>
                <div class="card-footer" style="flex-wrap: wrap; gap: 0.5rem; margin-top: auto;">
                    <span class="deadline" style="width: 100%; margin-bottom: 0.5rem; font-size: 0.8rem; opacity: 0.7;">Deadline: ${scheme.deadline}</span>
                    <a href="${scheme.apply_url}" target="_blank" class="btn btn-primary" style="padding: 0.6rem 1rem; font-size: 0.85rem; flex: 1; text-align: center;">Apply Now</a>
                    <button onclick="downloadPDFGuide('${scheme.id}')" id="btn-guide-${scheme.id}" class="btn glass" style="padding: 0.6rem 1rem; font-size: 0.85rem; flex: 1; border-color: var(--primary); color: white;">AI Guide</button>
                </div>
            `;
            grid.appendChild(card);
        });
    }

    // Search Logic
    if (searchInput) {
        searchInput.addEventListener('input', applyFiltersAndRender);
    }

    // Sort Logic
    const sortSelect = document.getElementById('scheme-sort');
    if (sortSelect) {
        sortSelect.addEventListener('change', applyFiltersAndRender);
    }

    // Language Logic
    if (langToggle) {
        langToggle.addEventListener('change', async () => {
            const selectedLang = langToggle.value;
            userProfile.language = selectedLang;
            localStorage.setItem('userProfile', JSON.stringify(userProfile));
            localStorage.setItem('userLanguage', selectedLang);
            fetchResults(userProfile);
        });
    }

    // Initial load
    try {
        fetchResults(userProfile);
    } catch (err) {
        console.error("Initialization Error:", err);
    }

    // Global Success Data (to be used by download function)
    window.getCurrentCompliance = () => complianceData;
});

// PDF Loader (Global)
async function downloadPDFGuide(schemeId) {
    const profile = JSON.parse(localStorage.getItem('userProfile')) || { name: 'Applicant' };
    const compliance = window.getCurrentCompliance ? window.getCurrentCompliance() : null;

    const userName = profile.name;
    const btn = document.getElementById(`btn-guide-${schemeId}`);
    if (!btn) return;

    const originalText = btn.innerText;
    btn.innerText = "Generating...";
    btn.disabled = true;

    try {
        let url = `/api/download-guide/${schemeId}?name=${encodeURIComponent(userName || 'User')}`;
        if (compliance) {
            url += `&score=${compliance.score}&risk_level=${compliance.risk_level}&suggestions=${encodeURIComponent(compliance.suggestions.join(','))}`;
        }

        const res = await fetch(url);
        if (!res.ok) throw new Error("Failed");

        const blob = await res.blob();
        const downloadUrl = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = downloadUrl;
        a.download = `${schemeId}_AI_Guide.pdf`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(downloadUrl);
        btn.innerText = "Success!";
        setTimeout(() => { btn.innerText = originalText; btn.disabled = false; }, 3000);
    } catch (e) {
        btn.innerText = "❌ Error";
        setTimeout(() => { btn.innerText = originalText; btn.disabled = false; }, 3000);
    }
}
