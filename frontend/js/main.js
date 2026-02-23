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

    // Initial setup for cards
    const cards = document.querySelectorAll('.feature-card');
    cards.forEach((card, index) => {
        card.classList.add('reveal-on-scroll');
        card.style.transitionDelay = `${index * 0.15}s`;
        observer.observe(card);
    });

    // Other reveal elements
    document.querySelectorAll('.reveal-on-scroll:not(.feature-card)').forEach(el => {
        observer.observe(el);
    });

});
