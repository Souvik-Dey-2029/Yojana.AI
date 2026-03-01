document.addEventListener('DOMContentLoaded', () => {
    const urlParams = new URLSearchParams(window.location.search);
    const schemeId = urlParams.get('id');
    const langToggle = document.getElementById('lang-toggle');

    let userProfile = JSON.parse(localStorage.getItem('userProfile')) || { language: 'en' };
    let results = JSON.parse(localStorage.getItem('eligibilityResults')) || [];
    let schemeScores = JSON.parse(localStorage.getItem('schemeScores')) || {};

    const LOCALIZATIONS = {
        hi: {
            overview: "योजना का विवरण",
            benefits_title: "✨ मुख्य लाभ",
            docs_title: "आवश्यक दस्तावेज",
            ai_analysis: "🤖 एआई पात्रता विश्लेषण",
            status_title: "आवेदन की स्थिति",
            match_score: "मैच स्कोर",
            risk_level: "जोखिम स्तर",
            official_apply: "आधिकारिक आवेदन 🚀",
            ai_guide: "एआई गाइड (PDF) 📄",
            deadline: "समय सीमा",
            back: "← मूल्यांकन डैशबोर्ड पर वापस",
            support_title: "सहायता चाहिए?",
            support_text: "हमारे एआई एजेंट सत्यापन प्रक्रिया में आपकी मदद करने के लिए तैयार हैं।",
            support_link: "सहायता केंद्र पर जाएँ",
            recommended: "अनुशंसित",
            official_welfare: "आधिकारिक कल्याण",
            risk_low: "कम",
            risk_medium: "मध्यम",
            risk_high: "उच्च"
        },
        bn: {
            overview: "স্কিমের ওভারভিউ",
            benefits_title: "✨ প্রধান সুবিধা",
            docs_title: "প্রয়োজনীয় নথি",
            ai_analysis: "🤖 এআই যোগ্যতা বিশ্লেষণ",
            status_title: "আবেদনের স্থিতি",
            match_score: "ম্যাচ স্কোর",
            risk_level: "ঝুঁকির স্তর",
            official_apply: "অফিসিয়াল আবেদন 🚀",
            ai_guide: "এআই গাইড (PDF) 📄",
            deadline: "শেষ তারিখ",
            back: "← অ্যাসেসমেন্ট ড্যাশবোর্ডে ফিরে যান",
            support_title: "সাহায্য প্রয়োজন?",
            support_text: "আমাদের এআই এজেন্টরা আপনাকে যাচাইকরণ প্রক্রিয়ায় সাহায্য করার জন্য প্রস্তুত।",
            support_link: "সাপোর্ট সেন্টারে যান",
            recommended: "প্রস্তাবিত",
            official_welfare: "অফিসিয়াল কল্যাণ",
            risk_low: "কম",
            risk_medium: "মাঝারি",
            risk_high: "উচ্চ"
        },
        ta: {
            overview: "திட்டத்தின் மேலோட்டம்",
            benefits_title: "✨ முக்கிய நன்மைகள்",
            docs_title: "தேவையான ஆவணங்கள்",
            ai_analysis: "🤖 AI தகுதி பகுப்பாய்வு",
            status_title: "விண்ணப்ப நிலை",
            match_score: "பொருத்தமான மதிப்பெண்",
            risk_level: "ஆபத்து நிலை",
            official_apply: "அதிகாரப்பூர்வ விண்ணப்பம் 🚀",
            ai_guide: "AI வழிகாட்டி (PDF) 📄",
            deadline: "காலக்கெடு",
            back: "← மதிப்பீட்டு டாஷ்போர்டிற்குத் திரும்பு",
            support_title: "உதவி தேவையா?",
            support_text: "எங்கள் AI முகவர்கள் சரிபார்ப்பு செயல்பாட்டில் உங்களுக்கு உதவ தயாராக உள்ளனர்.",
            support_link: "ஆதரவு மையத்தைப் பார்வையிடவும்",
            recommended: "பரிந்துரைக்கப்படுகிறது",
            official_welfare: "அதிகாரப்பூர்வ நலன்",
            risk_low: "குறைந்த",
            risk_medium: "நடுத்தர",
            risk_high: "அதிக"
        },
        mr: {
            overview: "योजनेचे विहंगावलोकन",
            benefits_title: "✨ मुख्य फायदे",
            docs_title: "आवश्यक कागदपत्रे",
            ai_analysis: "🤖 AI पात्रता विश्लेषण",
            status_title: "अर्जाची स्थिती",
            match_score: "मॅच स्कोर",
            risk_level: "जोखिम पातळी",
            official_apply: "अधिकृत अर्ज 🚀",
            ai_guide: "AI मार्गदर्शक (PDF) 📄",
            deadline: "डेडलाईन",
            back: "← मूल्यमापन डॅशबोर्डवर परत जा",
            support_title: "मदत हवी आहे?",
            support_text: "आमचे AI एजंट पडताळणी प्रक्रियेत तुम्हाला मदत करण्यास तयार आहेत.",
            support_link: "सपोर्ट सेंटरला भेट द्या",
            recommended: "शिफारस केलेले",
            official_welfare: "अधिकृत कल्याण",
            risk_low: "कमी",
            risk_medium: "मध्यम",
            risk_high: "उच्च"
        }
    };

    function updatePageStrings(lang) {
        if (lang === 'en' || !LOCALIZATIONS[lang]) return;
        const l = LOCALIZATIONS[lang];

        document.querySelector('.back-link').innerText = l.back;
        document.querySelector('.details-main-card h2').innerText = l.overview;
        document.querySelector('.benefit-highlight').innerHTML = `<span>✨</span> ${l.benefits_title}`;
        document.querySelector('.details-main-card h2:nth-of-type(2)').innerText = l.docs_title;

        const aiTitle = document.querySelector('#ai-analysis-box h2');
        if (aiTitle) aiTitle.innerHTML = `<span style="font-size: 1.5rem;">🤖</span> ${l.ai_analysis}`;

        document.querySelector('.sidebar-card h3').innerText = l.status_title;
        document.getElementById('apply-btn').innerHTML = l.official_apply;
        document.getElementById('guide-btn').innerHTML = l.ai_guide;

        const supportCard = document.querySelector('.sidebar-card:nth-of-type(2)');
        if (supportCard) {
            supportCard.querySelector('h4').innerText = l.support_title;
            supportCard.querySelector('p').innerText = l.support_text;
            supportCard.querySelector('a').innerText = l.support_link;
        }
    }

    async function fetchLatestData(lang) {
        userProfile.language = lang;
        localStorage.setItem('userProfile', JSON.stringify(userProfile));
        localStorage.setItem('userLanguage', lang);

        // Show loading state
        document.getElementById('scheme-name').innerText = "...";

        try {
            const res = await fetch('/api/eligibility', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(userProfile)
            });
            if (!res.ok) throw new Error("API Error");
            const data = await res.json();

            results = data.eligible_schemes;
            localStorage.setItem('eligibilityResults', JSON.stringify(results));

            renderData();
        } catch (e) {
            console.error(e);
            alert("Error refreshing localized data.");
        }
    }

    function renderData() {
        const scheme = results.find(s => s.id === schemeId);
        if (!scheme) {
            window.location.href = 'results.html';
            return;
        }

        const lang = localStorage.getItem('userLanguage') || 'en';
        const l = LOCALIZATIONS[lang] || {};

        // Populate Data
        document.getElementById('scheme-name').innerText = scheme.name;
        document.getElementById('scheme-icon').innerText = scheme.icon || '🏛️';
        document.getElementById('scheme-description').innerText = scheme.description;
        document.getElementById('scheme-benefits').innerText = scheme.benefits;
        document.getElementById('deadline-text').innerText = `${l.deadline || 'Deadline'}: ${scheme.deadline}`;
        document.getElementById('apply-btn').href = scheme.apply_url;

        // Tags
        const tagsContainer = document.getElementById('scheme-tags');
        tagsContainer.innerHTML = '';
        if (scheme.is_recommended) {
            tagsContainer.innerHTML += `<span class="probability-chip" style="background: var(--gov-green)15; color: var(--gov-green);">${l.recommended || 'Recommended'}</span>`;
        }
        tagsContainer.innerHTML += `<span class="probability-chip" style="background: #E0E7FF; color: var(--ashoka-navy);">${l.official_welfare || 'Official Welfare'}</span>`;

        // Docs
        const docsContainer = document.getElementById('docs-list');
        docsContainer.innerHTML = '';
        scheme.required_documents.forEach(doc => {
            docsContainer.innerHTML += `
                <div class="doc-item">
                    <span style="font-size: 1.2rem;">📄</span>
                    <span>${doc}</span>
                </div>
            `;
        });

        // AI Analysis
        const sScore = schemeScores[schemeId];
        const statusWidget = document.getElementById('probability-widget');
        if (sScore && typeof sScore.score === 'number') {
            document.getElementById('ai-analysis-box').style.display = 'block';
            const statusColor = sScore.risk_level === 'LOW' ? 'var(--gov-green)' : (sScore.risk_level === 'MEDIUM' ? 'var(--medium-saffron)' : 'var(--danger-red)');

            statusWidget.innerHTML = `
                <div style="display: flex; justify-content: space-between; font-weight: 800; margin-bottom: 0.5rem; color: ${statusColor}">
                    <span>${l.match_score || 'Match Score'}</span>
                    <span>${sScore.score}%</span>
                </div>
                <div class="approval-meter-premium" style="height: 12px !important;">
                    <div class="approval-meter-fill-premium" style="width: ${sScore.score}%; background: ${statusColor}; height: 100%;"></div>
                </div>
                <p style="font-size: 0.85rem; color: var(--text-muted); margin-top: 1rem; font-weight: 600;">
                    ${l.risk_level || 'Condition'}: <span style="color: ${statusColor}">${l['risk_' + sScore.risk_level.toLowerCase()] || sScore.risk_level} ${l.risk_text || 'RISK'}</span>
                </p>
            `;

            const content = document.getElementById('ai-analysis-content');
            if (sScore.suggestions && sScore.suggestions.length > 0) {
                content.innerHTML = `
                    <div class="ai-suggestions" style="background: #FFFBEB; border: 1px solid #FEF3C7; padding: 1.5rem; border-radius: 12px;">
                        <ul style="color: #92400E; margin: 0; padding-left: 1.25rem;">
                            ${sScore.suggestions.map(s => `<li style="margin-bottom: 0.5rem;">${s}</li>`).join('')}
                        </ul>
                    </div>
                `;
            } else {
                content.innerHTML = `<p style="color: var(--gov-green); font-weight: 700;">✅ Your profile shows high compliance with all scheme requirements. No immediate corrections needed.</p>`;
            }
        } else {
            document.getElementById('ai-analysis-box').style.display = 'none';
            statusWidget.innerHTML = `<p style="font-size: 0.85rem; color: var(--text-muted); font-weight: 600; text-align: center; padding: 1rem; background: #f9fafb; border-radius: 10px;">Verify document compliance on the dashboard to see probabilities.</p>`;
        }

        updatePageStrings(lang);
    }

    // Initial Load Logic
    if (!schemeId || !results.length) {
        window.location.href = 'results.html';
        return;
    }

    const savedLang = localStorage.getItem('userLanguage') || 'en';
    if (langToggle) {
        langToggle.value = savedLang;
        langToggle.addEventListener('change', () => {
            fetchLatestData(langToggle.value);
        });
    }

    renderData();

    // Guide Button
    document.getElementById('guide-btn').addEventListener('click', (e) => {
        window.downloadPDFGuide(schemeId, e.currentTarget);
    });
});
