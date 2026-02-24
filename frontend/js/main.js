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

            // [FIX] Update userProfile if it exists to keep everything in sync
            const profile = JSON.parse(localStorage.getItem('userProfile'));
            if (profile) {
                profile.language = selectedLang;
                localStorage.setItem('userProfile', JSON.stringify(profile));
            }

            // [FIX] Localize hero text if on homepage
            localizeHero(selectedLang);

            if (window.location.pathname.includes('results.html')) {
                // Handled in results.js
            }
        });

        // Initial localization for hero
        localizeHero(savedLang);
    }

    function localizeHero(lang) {
        const hero = document.querySelector('.hero h1');
        if (!hero) return;

        const HERO_TEXTS = {
            hi: "नागरिकों के लिए <span>डिजिटल</span> सहायता इंजन",
            bn: "নাগরিকদের জন্য <span>ডিজিটাল</span> সহায়তা ইঞ্জিন",
            ta: "மக்களுக்கான <span>டிஜிட்டல்</span> உதவி இயந்திரம்",
            mr: "नागरिकांसाठी <span>डिजिटल</span> मदत इंजिन",
            en: "Digital Public <span>Assistance</span> Engine"
        };

        if (HERO_TEXTS[lang]) {
            hero.innerHTML = HERO_TEXTS[lang];
        }
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

    // --- Hero Carousel Implementation (Tasks 5, 8) ---
    const initHeroCarousel = () => {
        const slider = document.getElementById('hero-slider');
        const dotsContainer = document.getElementById('slider-dots');
        if (!slider) return;

        const slides = slider.querySelectorAll('.hero-slide');
        let currentIdx = 0;
        let slideInterval;

        // Create Dots
        slides.forEach((_, idx) => {
            const dot = document.createElement('div');
            dot.classList.add('dot');
            if (idx === 0) dot.classList.add('active');
            dot.addEventListener('click', () => goToSlide(idx));
            dotsContainer.appendChild(dot);
        });

        const dots = dotsContainer.querySelectorAll('.dot');

        const goToSlide = (idx) => {
            slides[currentIdx].classList.remove('active');
            dots[currentIdx].classList.remove('active');
            currentIdx = idx;
            slides[currentIdx].classList.add('active');
            dots[currentIdx].classList.add('active');
            resetInterval();
        };

        const nextSlide = () => {
            let nextIdx = (currentIdx + 1) % slides.length;
            goToSlide(nextIdx);
        };

        const resetInterval = () => {
            clearInterval(slideInterval);
            slideInterval = setInterval(nextSlide, 4000);
        };

        // Pause on Hover
        slider.addEventListener('mouseenter', () => clearInterval(slideInterval));
        slider.addEventListener('mouseleave', resetInterval);

        // Preload Images (Task 8)
        const preloadImages = () => {
            slides.forEach(slide => {
                const img = slide.querySelector('img');
                if (img && img.src) {
                    const nextImg = new Image();
                    nextImg.src = img.src;
                }
            });
        };

        preloadImages();
        resetInterval();

        // Simple Swipe Support (Task 5)
        let touchStartX = 0;
        slider.addEventListener('touchstart', e => { touchStartX = e.changedTouches[0].screenX; }, { passive: true });
        slider.addEventListener('touchend', e => {
            const touchEndX = e.changedTouches[0].screenX;
            if (touchStartX - touchEndX > 50) goToSlide((currentIdx + 1) % slides.length);
            if (touchEndX - touchStartX > 50) goToSlide((currentIdx - 1 + slides.length) % slides.length);
        }, { passive: true });
    };

    initHeroCarousel();
});
