document.addEventListener('DOMContentLoaded', () => {
    // Scroll Reveal Logic
    const observerOptions = {
        threshold: 0.15,
        rootMargin: "0px 0px -50px 0px"
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('active');
            }
        });
    }, observerOptions);

    // Observe animatable elements
    document.querySelectorAll('.animate-fade-in, .feature-card, .blog-card, .fact-box, .price-card').forEach((el, index) => {
        el.style.transitionDelay = `${(index % 3) * 0.15}s`;
        observer.observe(el);
    });

    // --- Static Ticker Management ---
    const ticker = document.getElementById('pulse-ticker');
    if (ticker) {
        // Ticker is handled by CSS animation in main.css
    }

    // Citizen Pulse Toast System (Replacing futuristic Live Pulse)
    const pulseToast = document.getElementById('live-pulse');
    const pulseContent = document.getElementById('pulse-content');

    const pulseMessages = [
        "Government Insight: 450+ central schemes are currently active.",
        "Success: A citizen in Maharashtra just accessed 4 eligible benefits.",
        "Tip: Complete your profile for better scheme matching accuracy.",
        "Update: PM-Kisan portal is now processing direct transfers.",
        "Support: Available in Hindi, Bengali, Tamil, and 7 more languages."
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
});
