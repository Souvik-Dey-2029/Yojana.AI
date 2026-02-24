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

    // UI Localizations
    const LOCALIZATIONS = {
        hi: {
            title: "आपके लिए पात्र योजनाएं",
            subtitle: "आपकी प्रोफ़ाइल के आधार पर, यहाँ वे योजनाएं हैं जिनके लिए आप आवेदन कर सकते हैं।",
            search_placeholder: "नाम या कीवर्ड द्वारा योजनाएं खोजें...",
            sort_relevance: "क्रम: प्रासंगिकता",
            sort_popularity: "क्रम: लोकप्रियता",
            analyzer_title: "🧠 आवेदन सफलता विश्लेषक",
            analyzer_sub: "दस्तावेज़ अनुपालन के आधार पर प्रत्येक योजना के लिए अपनी स्वीकृति की संभावना का अनुमान लगाने के लिए इन 8 सरल प्रश्नों के उत्तर दें।",
            calculate_btn: "अनुमोदन संभावना की गणना करें",
            analyzing_btn: "जोखিমों का विश्लेषण किया जा रहा है...",
            recalculate_btn: "पुनः गणना करें",
            required_docs: "आवश्यक दस्तावेज",
            apply_now: "अभी आवेदन करें",
            ai_guide: "एआई गाइड",
            deadline: "समय सीमा",
            approval: "अनुमोदन",
            ai_suggestions: "एआई अनुपालन सुझाव",
            q_aadhaar_name: "क्या आधार का नाम सभी दस्तावेजों में समान है?",
            q_income_valid: "क्या आय प्रमाण पत्र 12 महीने के भीतर जारी किया गया है?",
            q_bank_dbt: "क्या बैंक खाता डीबीटी सक्षम है?",
            q_address_match: "क्या आधार और राशन कार्ड में पता मेल खाता है?",
            q_category_valid: "क्या श्रेणी प्रमाण पत्र मान्य है?",
            q_photo_correct: "क्या दिशानिर्देशों के अनुसार पासपोर्ट आकार का फोटो है?",
            q_mobile_linked: "क्या आधार मोबाइल से जुड़ा है?",
            q_self_attested: "क्या स्व-सत्यापित दस्तावेज तैयार हैं?",
            yes: "हाँ",
            no: "नहीं"
        },
        bn: {
            title: "আপনার জন্য যোগ্য স্কিম",
            subtitle: "আপনার প্রোফাইলের উপর ভিত্তি করে, এখানে সেই স্কিমগুলি রয়েছে যার জন্য আপনি আবেদন করতে পারেন।",
            search_placeholder: "নাম বা কীওয়ার্ড দ্বারা স্কিম খুঁজুন...",
            sort_relevance: "ক্রম: প্রাসঙ্গিকতা",
            sort_popularity: "ক্রম: জনপ্রিয়তা",
            analyzer_title: "🧠 আবেদন সাফল্য বিশ্লেষক",
            analyzer_sub: "নথিপত্র সম্মতির উপর ভিত্তি করে প্রতিটি স্কিমের জন্য আপনার অনুমোদনের সম্ভাবনা অনুমান করতে এই ৮টি সহজ প্রশ্নের উত্তর দিন।",
            calculate_btn: "অনুমোদনের সম্ভাবনা গণনা করুন",
            analyzing_btn: "ঝুঁকি বিশ্লেষণ করা হচ্ছে...",
            recalculate_btn: "পুনরায় গণনা করুন",
            required_docs: "প্রয়োজনীয় নথি",
            apply_now: "এখনই আবেদন করুন",
            ai_guide: "এআই গাইড",
            deadline: "শেষ তারিখ",
            approval: "অনুমোদন",
            ai_suggestions: "এআই সম্মতির পরামর্শ",
            q_aadhaar_name: "আধার নাম কি সব নথিতে এক?",
            q_income_valid: "আয় শংসাপত্র কি ১২ মাসের মধ্যে ইস্যু করা হয়েছে?",
            q_bank_dbt: "ব্যাঙ্ক অ্যাকাউন্ট কি DBT সক্ষম?",
            q_address_match: "আধার এবং রেশন কার্ডে ঠিকানা কি একই?",
            q_category_valid: "ক্যাটাগরি শংসাপত্র কি বৈধ?",
            q_photo_correct: "গাইডলাইন অনুযায়ী পাসপোর্ট সাইজ ফটো আছে কি?",
            q_mobile_linked: "আধার কি মোবাইলের সাথে লিঙ্কযুক্ত?",
            q_self_attested: "স্ব-প্রত্যয়িত নথিগুলি কি প্রস্তুত?",
            yes: "হ্যাঁ",
            no: "না"
        }
    };

    function updateStaticUI(lang) {
        if (lang === 'en' || !LOCALIZATIONS[lang]) return;
        const l = LOCALIZATIONS[lang];

        // Header & Search
        if (headline) headline.innerText = l.title;
        const subheadline = document.getElementById('results-subheadline');
        if (subheadline) subheadline.innerText = l.subtitle;
        if (searchInput) searchInput.placeholder = l.search_placeholder;

        // Sort Options
        const sortSelect = document.getElementById('scheme-sort');
        if (sortSelect) {
            sortSelect.options[0].text = l.sort_relevance;
            sortSelect.options[1].text = l.sort_popularity;
        }

        // Analyzer Section
        if (analyzerSection) {
            const h2 = analyzerSection.querySelector('h2');
            if (h2) h2.innerHTML = `<span style="font-size: 2rem;">🧠</span> ${l.analyzer_title}`;
            const p = analyzerSection.querySelector('p');
            if (p) p.innerText = l.analyzer_sub;
            if (runAnalysisBtn) runAnalysisBtn.innerText = l.calculate_btn;

            // Form Questions
            const form = document.getElementById('compliance-form');
            if (form) {
                const groups = form.querySelectorAll('.q-group');
                const qKeys = ['q_aadhaar_name', 'q_income_valid', 'q_bank_dbt', 'q_address_match', 'q_category_valid', 'q_photo_correct', 'q_mobile_linked', 'q_self_attested'];
                groups.forEach((group, i) => {
                    const span = group.querySelector('span');
                    if (span && qKeys[i]) span.innerText = l[qKeys[i]];
                    const select = group.querySelector('select');
                    if (select) {
                        select.options[0].text = l.yes;
                        select.options[1].text = l.no;
                    }
                });
            }
        }
    }

    // Application Success Analyzer Logic
    const analyzerSection = document.getElementById('analyzer-section');
    const runAnalysisBtn = document.getElementById('run-analysis');
    let complianceData = null;

    if (runAnalysisBtn) {
        runAnalysisBtn.addEventListener('click', async () => {
            const l = LOCALIZATIONS[userProfile.language] || {};
            const form = document.getElementById('compliance-form');
            const formData = new FormData(form);
            const data = {};
            formData.forEach((value, key) => data[key] = parseInt(value));

            runAnalysisBtn.innerText = l.analyzing_btn || "Analyzing Risks...";
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
                runAnalysisBtn.innerText = l.recalculate_btn || "Re-Calculate Probability";
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
        updateStaticUI(profile.language);

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
        const lang = userProfile.language;
        const l = LOCALIZATIONS[lang] || {
            approval: "Approval",
            ai_suggestions: "AI COMPLIANCE SUGGESTIONS",
            required_docs: "Required Documents",
            deadline: "Deadline",
            apply_now: "Apply Now",
            ai_guide: "AI Guide"
        };

        if (!schemes || schemes.length === 0) {
            headline.innerText = (lang === 'en') ? "No Schemes Found" : l.title;
            grid.innerHTML = '<p style="grid-column:1/-1; text-align:center; padding: 3rem; opacity: 0.7;">Sorry, we couldn\'t find any matching schemes for your profile currently. Try adjusting your details.</p>';
            if (analyzerSection) analyzerSection.style.display = 'none';
            return;
        }

        if (lang === 'en') {
            headline.innerText = `${schemes.length} Schemes Found`;
        }

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
                        ${complianceData.score}% ${l.approval}
                    </div>
                `;

                if (complianceData.risk_level !== 'LOW' && complianceData.suggestions.length > 0) {
                    suggestionBox = `
                        <div class="ai-suggestions" style="margin-top: 1rem; padding: 0.8rem; border-radius: 0.8rem; background: rgba(255,255,255,0.03); border: 1px dashed rgba(255,255,255,0.1);">
                            <div style="font-size: 0.7rem; color: ${color}; font-weight: 600; margin-bottom: 0.4rem; display: flex; align-items: center; gap: 0.3rem;">
                                <span>⚡</span> ${l.ai_suggestions}
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
                <div class="docs-title">${l.required_docs}</div>
                <ul class="docs-list">
                    ${scheme.required_documents.map(doc => `<li>${doc}</li>`).join('')}
                </ul>
                <div class="card-footer" style="flex-wrap: wrap; gap: 0.5rem; margin-top: auto;">
                    <span class="deadline" style="width: 100%; margin-bottom: 0.5rem; font-size: 0.8rem; opacity: 0.7;">${l.deadline}: ${scheme.deadline}</span>
                    <a href="${scheme.apply_url}" target="_blank" class="btn btn-primary" style="padding: 0.6rem 1rem; font-size: 0.85rem; flex: 1; text-align: center;">${l.apply_now}</a>
                    <button onclick="downloadPDFGuide('${scheme.id}')" id="btn-guide-${scheme.id}" class="btn glass" style="padding: 0.6rem 1rem; font-size: 0.85rem; flex: 1; border-color: var(--primary); color: white;">${l.ai_guide}</button>
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
            updateStaticUI(selectedLang);
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
    const profile = JSON.parse(localStorage.getItem('userProfile')) || { name: 'Applicant', language: 'en' };
    const compliance = window.getCurrentCompliance ? window.getCurrentCompliance() : null;

    const langLocalizations = {
        hi: { generating: "उत्पन्न किया जा रहा है...", failed: "विफल रहा", success: "सफलता!" },
        bn: { generating: "তৈরি করা হচ্ছে...", failed: "ব্যর্থ হয়েছে", success: "সফল!" }
    };

    const l = langLocalizations[profile.language] || { generating: "Generating...", failed: "Failed", success: "Success!" };

    const userName = profile.name;
    const btn = document.getElementById(`btn-guide-${schemeId}`);
    if (!btn) return;

    const originalText = btn.innerText;
    btn.innerText = l.generating;
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
        btn.innerText = l.success;
        setTimeout(() => { btn.innerText = originalText; btn.disabled = false; }, 3000);
    } catch (e) {
        btn.innerText = "❌ " + l.failed;
        setTimeout(() => { btn.innerText = originalText; btn.disabled = false; }, 3000);
    }
}
