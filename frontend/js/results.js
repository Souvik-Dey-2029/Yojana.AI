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
            no: "नहीं",
            ai_match: "✨ एआई मैच"
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
            no: "না",
            ai_match: "✨ এআই ম্যাচ"
        },
        ta: {
            title: "உங்களுக்கான தகுதியுள்ள திட்டங்கள்",
            subtitle: "உங்கள் சுயவிவரத்தின் அடிப்படையில், நீங்கள் விண்ணப்பிக்கக்கூடிய திட்டங்கள் இங்கே உள்ளன.",
            search_placeholder: "பெயர் அல்லது முக்கிய வார்த்தை மூலம் திட்டங்களைத் தேடுங்கள்...",
            sort_relevance: "வரிசை: பொருத்தம்",
            sort_popularity: "வரிசை: பிரபலம்",
            analyzer_title: "🧠 விண்ணப்ப வெற்றி ஆய்வாளர்",
            analyzer_sub: "ஆவணங்களின் இணக்கத்தின் அடிப்படையில் ஒவ்வொரு திட்டத்திற்கும் உங்கள் ஒப்புதலுக்கான வாய்ப்பைக் கணக்கிட இந்த 8 எளிய கேள்விகளுக்குப் பதிலளிக்கவும்.",
            calculate_btn: "ஒப்புதல் வாய்ப்பைக் கணக்கிடுங்கள்",
            analyzing_btn: "ஆய்வு செய்யப்படுகிறது...",
            recalculate_btn: "மீண்டும் கணக்கிடுங்கள்",
            required_docs: "தேவையான ஆவணங்கள்",
            apply_now: "இப்பொழுதே விண்ணப்பிக்கவும்",
            ai_guide: "AI வழிகாட்டி",
            deadline: "காலக்கெடு",
            approval: "ஒப்புதல்",
            ai_suggestions: "AI இணக்க பரிந்துரைகள்",
            q_aadhaar_name: "அனைத்து ஆவணங்களிலும் ஆதார் பெயர் ஒன்றாக உள்ளதா?",
            q_income_valid: "வருமானச் சான்றிதழ் 12 மாதங்களுக்குள் வழங்கப்பட்டதா?",
            q_bank_dbt: "வங்கி கணக்கு DBT இயக்கப்பட்டதா?",
            q_address_match: "ஆதார் மற்றும் ரேஷன் கார்டில் முகவரி பொருந்துகிறதா?",
            q_category_valid: "வகைச் சான்றிதழ் செல்லுபடியாகுமா?",
            q_photo_correct: "வழிகாட்டுதல்களின்படி பாஸ்போர்ட் அளவு புகைப்படம் உள்ளதா?",
            q_mobile_linked: "ஆதார் மொபைலுடன் இணைக்கப்பட்டுள்ளதா?",
            q_self_attested: "சுய சான்றொப்பம் பெற்ற ஆவணங்கள் தயாராக உள்ளனவா?",
            yes: "ஆம்",
            no: "இல்லை",
            ai_match: "✨ AI பொருத்தம்"
        },
        mr: {
            title: "तुमच्यासाठी पात्र योजना",
            subtitle: "तुमच्या प्रोफाइलवर आधारित, तुम्ही अर्ज करू शकता अशा योजना येथे आहेत.",
            search_placeholder: "नाव किंवा कीवर्डद्वारे योजना शोधा...",
            sort_relevance: "क्रमवारी: प्रासंगिकता",
            sort_popularity: "क्रमवारी: लोकप्रियता",
            analyzer_title: "🧠 अर्ज यश विश्लेषक",
            analyzer_sub: "कागदपत्रांच्या पूर्ततेवर आधारित प्रत्येक योजनेसाठी तुमच्या मंजुरीच्या शक्यतेचा अंदाज घेण्यासाठी या ८ सोप्या प्रश्नांची उत्तरे द्या.",
            calculate_btn: "मंजुरीची शक्यता मोजा",
            analyzing_btn: "विश्लेषण केले जात आहे...",
            recalculate_btn: "पुन्हा मोजा",
            required_docs: "आवश्यक कागदपत्रे",
            apply_now: "आता अर्ज करा",
            ai_guide: "AI मार्गदर्शक",
            deadline: "डेडलाईन",
            approval: "मंजुरी",
            ai_suggestions: "AI अनुपालन सूचना",
            q_aadhaar_name: "सर्व कागदपत्रांमध्ये आधारवरील नाव सारखे आहे का?",
            q_income_valid: "उत्पन्न प्रमाणपत्र १२ महिन्यांच्या आतील आहे का?",
            q_bank_dbt: "बँक खाते DBT सक्षम आहे का?",
            q_address_match: "आधार आणि रेशन कार्डमधील पत्ता जुळतो का?",
            q_category_valid: "वर्ग प्रमाणपत्र वैध आहे का?",
            q_photo_correct: "मार्गदर्शक तत्त्वांनुसार पासपोर्ट आकाराचा फोटो आहे का?",
            q_mobile_linked: "आधार मोबाईलशी लिंक आहे का?",
            q_self_attested: "स्व-साक्षांकित कागदपत्रे तयार आहेत का?",
            yes: "हो",
            no: "नाही",
            ai_match: "✨ AI मॅच"
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
                const groups = form.querySelectorAll('.q-group, .q-group-sidebar');
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
    // Per-scheme scores: { scheme_id: { score, risk_level, suggestions } }
    let schemeScores = null;

    if (runAnalysisBtn) {
        runAnalysisBtn.addEventListener('click', async () => {
            const l = LOCALIZATIONS[userProfile.language] || {};
            const form = document.getElementById('compliance-form');
            const formData = new FormData(form);
            const data = {};
            formData.forEach((value, key) => data[key] = parseInt(value));

            // Include all currently visible scheme IDs so backend can score each one
            data.scheme_ids = currentSchemes.map(s => s.id);

            runAnalysisBtn.innerText = l.analyzing_btn || "Analyzing Risks...";
            runAnalysisBtn.disabled = true;

            try {
                const res = await fetch('/api/predict-scheme-scores', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
                if (!res.ok) throw new Error("Prediction API Error");

                const result = await res.json();
                schemeScores = result.scores; // { scheme_id: { score, risk_level, suggestions } }
                console.log("DEBUG: Per-scheme scores received:", schemeScores);

                // Refresh rendering with new per-scheme data
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
            headline.innerText = `${schemes.length} Premium Schemes Found`;
        }

        grid.innerHTML = '';

        const aiMatchLabel = l.ai_match || "✨ AI Match";

        schemes.forEach((scheme, index) => {
            const card = document.createElement('div');
            card.className = 'scheme-card animate-fade-in';
            card.style.animationDelay = `${index * 0.08}s`;

            const aiMatchBadge = scheme.is_ml_recommended ? `<span class="badge badge-ai" style="background: var(--gov-green); color: white; margin-left: 0.5rem; font-size: 0.7rem; padding: 2px 8px; border-radius: 4px;">${aiMatchLabel}</span>` : '';

            /* TOP RIGHT STATUS TAG (Official Badge Style) */
            let topStatusTag = '';
            const badgeStyle = 'style="background: rgba(4, 106, 56, 0.12); color: #046A38; padding: 4px 10px; border-radius: 6px; font-size: 12px;"';
            if (scheme.is_recommended) {
                topStatusTag = `<span class="status-badge" ${badgeStyle}>Recommended</span>`;
            } else if (schemeScores && schemeScores[scheme.id] && schemeScores[scheme.id].score > 80) {
                topStatusTag = `<span class="status-badge" ${badgeStyle}>High Approval Chance</span>`;
            } else {
                topStatusTag = `<span class="status-badge" ${badgeStyle}>Eligible</span>`;
            }

            let approvalUI = '';
            let suggestionBox = '';
            let matchStatusText = "Eligibility Guaranteed";
            let statusColor = "var(--gov-green)";

            // Default state without analysis
            if (!schemeScores || !schemeScores[scheme.id]) {
                matchStatusText = "Scan to Verify";
                statusColor = "var(--ashoka-navy)";
            } else {
                const sData = schemeScores[scheme.id];
                statusColor = sData.risk_level === 'LOW' ? 'var(--gov-green)' : (sData.risk_level === 'MEDIUM' ? 'var(--medium-saffron)' : 'var(--danger-red)');
                matchStatusText = sData.risk_level === 'LOW' ? "High Probability" : (sData.risk_level === 'MEDIUM' ? "Moderate Match" : "Attention Required");

                approvalUI = `
                    <div style="margin-top: 1rem;">
                        <div style="display: flex; justify-content: space-between; font-size: 0.8rem; font-weight: 800; color: ${statusColor}; margin-bottom: 0.4rem;">
                            <span>${l.approval} Probability</span>
                            <span>${sData.score}%</span>
                        </div>
                        <div class="approval-meter-premium">
                            <div class="approval-meter-fill-premium" style="width: ${sData.score}%; background: ${statusColor};"></div>
                        </div>
                    </div>
                `;

                if (sData.risk_level !== 'LOW' && sData.suggestions.length > 0) {
                    suggestionBox = `
                        <div class="ai-suggestions" style="margin-top: 1.25rem; padding: 1.25rem; border-radius: 12px; background: rgba(255, 122, 0, 0.05); border: 1px dashed var(--primary-saffron); border-left: 4px solid var(--primary-saffron);">
                            <div style="font-size: 0.75rem; color: var(--primary-saffron); font-weight: 800; margin-bottom: 0.6rem; display: flex; align-items: center; gap: 0.5rem; text-transform: uppercase;">
                                <span>📋</span> ${l.ai_suggestions}
                            </div>
                            <ul style="font-size: 0.8rem; color: #4B5563; padding-left: 1.2rem; margin: 0; line-height: 1.4;">
                                ${sData.suggestions.map(s => `<li>${s}</li>`).join('')}
                            </ul>
                        </div>
                    `;
                }
            }

            card.innerHTML = `
                ${topStatusTag}
                <div class="scheme-match-badge" style="background: ${statusColor}; border-radius: 4px; font-weight: 800; font-size: 0.7rem;">${matchStatusText}</div>
                <div class="scheme-icon-wrapper" style="font-size: 3rem; background: #f8fafc; width: 70px; height: 70px; display: flex; align-items: center; justify-content: center; border-radius: 16px; margin-bottom: 1.5rem; border: 1px solid rgba(0,0,0,0.03);">${scheme.icon || '🏛️'}</div>
                
                <h3 style="margin: 0; font-size: 1.4rem; line-height: 1.3; color: var(--ashoka-navy);">${scheme.name}</h3>
                <p style="font-size: 0.95rem; color: #6B7280; margin: 0.75rem 0 1.25rem;">${scheme.description}</p>
                
                <div style="display: flex; flex-wrap: wrap; gap: 0.5rem; margin-bottom: 1.25rem;">
                    <div class="benefit-pill">
                        <span>💰</span> ${scheme.benefits}
                    </div>
                </div>

                ${approvalUI}
                ${suggestionBox}

                <div style="margin-top: 1.5rem; border-top: 1px solid #f3f4f6; padding-top: 1.5rem;">
                    <div class="docs-title" style="font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.5px; opacity: 0.7; margin-bottom: 0.75rem;">${l.required_docs}</div>
                    <ul class="docs-list" style="columns: 2; column-gap: 1rem; margin-bottom: 1.5rem; font-size: 0.85rem; color: #4B5563;">
                        ${scheme.required_documents.map(doc => `<li>${doc}</li>`).join('')}
                    </ul>
                </div>

                <div class="card-footer" style="display: flex; gap: 0.75rem; margin-top: auto; padding-top: 1rem;">
                    <button onclick="downloadPDFGuide('${scheme.id}')" id="btn-guide-${scheme.id}" class="btn glass" style="flex: 1; display: flex; align-items: center; justify-content: center; gap: 0.5rem; font-size: 0.9rem;">
                        <span>📄</span> ${l.ai_guide}
                    </button>
                    <a href="${scheme.apply_url}" target="_blank" class="btn btn-primary" style="flex: 1.2; text-align: center; display: flex; align-items: center; justify-content: center; gap: 0.5rem; font-size: 0.9rem;">
                        <span>Apply</span> <span>🚀</span>
                    </a>
                </div>
                <div style="font-size: 0.75rem; color: #9CA3AF; margin-top: 1rem; text-align: center; font-weight: 500;">
                    ${l.deadline}: ${scheme.deadline}
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
    // Returns the score for a specific scheme, or null if scores not yet computed
    window.getSchemeCompliance = (schemeId) => schemeScores ? schemeScores[schemeId] : null;
});

// PDF Loader (Global)
async function downloadPDFGuide(schemeId) {
    const profile = JSON.parse(localStorage.getItem('userProfile')) || { name: 'Applicant', language: 'en' };
    // Get the specific compliance data for THIS scheme
    const compliance = window.getSchemeCompliance ? window.getSchemeCompliance(schemeId) : null;

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
