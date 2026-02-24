document.addEventListener('DOMContentLoaded', () => {
    // Scroll Reveal Logic
    const observerOptions = {
        threshold: 0.15,
        rootMargin: "0px 0px -50px 0px"
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, observerOptions);

    // Observe animatable elements
    document.querySelectorAll('.scroll-reveal, .animate-fade-in').forEach((el, index) => {
        // Only add delay if not already specified in CSS
        if (!el.style.animationDelay) {
            el.style.transitionDelay = `${(index % 4) * 0.1}s`;
        }
        observer.observe(el);
    });

    // --- Language Sync Logic ---
    const langToggle = document.getElementById('lang-toggle');
    if (langToggle) {
        const savedLang = localStorage.getItem('userLanguage') || 'en';
        langToggle.value = savedLang;

        langToggle.addEventListener('change', () => {
            const selectedLang = langToggle.value;
            localStorage.setItem('userLanguage', selectedLang);

            // If we're on the results page, the results.js will handle the refresh.
            // For other pages, we can just reload or let it be for now since they are mostly static.
            if (window.location.pathname.includes('results.html')) {
                // results.js has its own listener, so we don't need to do much here
                // but let's make sure it's consistent.
            } else {
                // If on homepage or others, we might want to refresh to show localized text if we add that later.
                // For now, just keeping the state in sync is enough.
            }
        });
    }

    // --- Static Ticker Management ---
    const ticker = document.getElementById('pulse-ticker');
    if (ticker) {
        // Ticker is handled by CSS animation in main.css
    }

    // Citizen Pulse Toast System (Replacing futuristic Live Pulse)
    const pulseToast = document.getElementById('live-pulse');
    const pulseContent = document.getElementById('pulse-content');

    const pulseMessages = [
        "Government Insight: 50+ central schemes are currently active.",
        "Success: A citizen in Maharashtra just accessed 4 eligible benefits.",
        "Tip: Complete your profile for better scheme matching accuracy.",
        "Update: PM-Kisan portal is now processing direct transfers.",
        "Support: Available in Hindi, Bengali, Tamil, Marathi, and English."
    ];

    let messageIdx = 0;
    const showPulse = () => {
        if (!pulseToast) return;
        pulseContent.innerText = pulseMessages[messageIdx];
        pulseToast.style.display = 'flex';
        pulseToast.classList.add('active');

        setTimeout(() => {
            pulseToast.classList.remove('active');
            setTimeout(() => { pulseToast.style.display = 'none'; }, 500);
            messageIdx = (messageIdx + 1) % pulseMessages.length;
        }, 5000);
    };

    // Show initial update after 3 seconds, then every 20 seconds
    if (pulseToast) {
        setTimeout(() => {
            showPulse();
            setInterval(showPulse, 20000);
        }, 3000);
    }
    // --- Footer Date Management ---
    const footerDate = document.querySelector('.footer-last-updated');
    if (footerDate) {
        const now = new Date();
        const dateStr = now.toLocaleDateString('en-GB', {
            day: '2-digit',
            month: '2-digit',
            year: 'numeric'
        }).replace(/\//g, '-');
        footerDate.textContent = `Last updated: ${dateStr}`;
    }

    // --- Mobile Menu Toggle ---
    const menuToggle = document.querySelector('.mobile-menu-toggle');
    const navLinks = document.querySelector('.nav-links');

    if (menuToggle && navLinks) {
        menuToggle.addEventListener('click', () => {
            navLinks.classList.toggle('active');
            menuToggle.classList.toggle('active');
        });

        // Close menu when clicking a link
        navLinks.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                navLinks.classList.remove('active');
                menuToggle.classList.remove('active');
            });
        });
    }
});
