/**
 * Yojana.AI - Shared PDF Generation Utility
 * Handles the communication with backend API to generate and download AI Guides.
 */

window.downloadPDFGuide = async function (schemeId, btnElement = null) {
    const profile = JSON.parse(localStorage.getItem('userProfile')) || { name: 'Applicant', language: 'en' };

    // Attempt to retrieve compliance data from shared state or localStorage
    const schemeScores = JSON.parse(localStorage.getItem('schemeScores')) || {};
    const compliance = schemeScores[schemeId] || (window.getSchemeCompliance ? window.getSchemeCompliance(schemeId) : null);

    const langLocalizations = {
        hi: { generating: "उत्पन्न किया जा रहा है...", failed: "विफल रहा", success: "सफलता!" },
        bn: { generating: "তৈরি করা হচ্ছে...", failed: "ব্যর্থ হয়েছে", success: "সফল!" },
        ta: { generating: "உருவாக்கப்படுகிறது...", failed: "தோல்வி", success: "வெற்றி!" },
        mr: { generating: "तयार होत आहे...", failed: "यशस्वी झाले नाही", success: "यशस्वी!" }
    };

    const l = langLocalizations[profile.language] || { generating: "Generating...", failed: "Failed", success: "Success!" };

    // If btnElement is not provided, try to find it by common ID patterns
    const btn = btnElement || document.getElementById('guide-btn') || document.getElementById(`btn-guide-${schemeId}`);

    const originalText = btn ? btn.innerText : "";
    if (btn) {
        btn.innerText = l.generating;
        btn.disabled = true;
    }

    try {
        let url = `/api/download-guide/${schemeId}?name=${encodeURIComponent(profile.name || 'User')}`;
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

        if (btn) {
            btn.innerText = l.success;
            setTimeout(() => {
                btn.innerText = originalText;
                btn.disabled = false;
            }, 3000);
        }
    } catch (e) {
        console.error("PDF Download Error:", e);
        if (btn) {
            btn.innerText = "❌ " + l.failed;
            setTimeout(() => {
                btn.innerText = originalText;
                btn.disabled = false;
            }, 3000);
        } else {
            alert("Error downloading PDF Guide. Please try again later.");
        }
    }
};
