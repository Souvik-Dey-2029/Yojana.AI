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

    // --- Interactive Particle Background ---
    const canvas = document.getElementById('hero-canvas');
    if (canvas) {
        const ctx = canvas.getContext('2d');
        let particles = [];
        const particleCount = 100;
        const mouse = { x: null, y: null, radius: 150 };

        window.addEventListener('mousemove', (e) => {
            mouse.x = e.x;
            mouse.y = e.y;
        });

        function resize() {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        }
        window.addEventListener('resize', resize);
        resize();

        class Particle {
            constructor() {
                this.x = Math.random() * canvas.width;
                this.y = Math.random() * canvas.height;
                this.size = Math.random() * 2 + 1;
                this.baseX = this.x;
                this.baseY = this.y;
                this.density = (Math.random() * 30) + 1;
            }

            draw() {
                ctx.fillStyle = 'rgba(99, 102, 241, 0.5)';
                ctx.beginPath();
                ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
                ctx.closePath();
                ctx.fill();
            }

            update() {
                let dx = mouse.x - this.x;
                let dy = mouse.y - this.y;
                let distance = Math.sqrt(dx * dx + dy * dy);
                let forceDirectionX = dx / distance;
                let forceDirectionY = dy / distance;
                let maxDistance = mouse.radius;
                let force = (maxDistance - distance) / maxDistance;
                let directionX = forceDirectionX * force * this.density;
                let directionY = forceDirectionY * force * this.density;

                if (distance < mouse.radius) {
                    this.x -= directionX;
                    this.y -= directionY;
                } else {
                    if (this.x !== this.baseX) {
                        let dx = this.x - this.baseX;
                        this.x -= dx / 10;
                    }
                    if (this.y !== this.baseY) {
                        let dy = this.y - this.baseY;
                        this.y -= dy / 10;
                    }
                }
            }
        }

        function init() {
            particles = [];
            for (let i = 0; i < particleCount; i++) {
                particles.push(new Particle());
            }
        }

        function animate() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            for (let i = 0; i < particles.length; i++) {
                particles[i].draw();
                particles[i].update();
            }
            requestAnimationFrame(animate);
        }

        init();
        animate();
    }

    // --- Language Toggle Sync ---
    const langToggle = document.getElementById('lang-toggle');
    if (langToggle) {
        // Load initial
        const savedLang = localStorage.getItem('userLanguage') || 'en';
        langToggle.value = savedLang;

        langToggle.addEventListener('change', (e) => {
            const selected = e.target.value;
            localStorage.setItem('userLanguage', selected);

            // Also update userProfile if it exists to maintain sync
            const profile = JSON.parse(localStorage.getItem('userProfile'));
            if (profile) {
                profile.language = selected;
                localStorage.setItem('userProfile', JSON.stringify(profile));
            }

            console.log("DEBUG: Home language synced to:", selected);
        });
    }

    // Observe Blog Cards
    document.querySelectorAll('.blog-card').forEach((card, index) => {
        card.style.transitionDelay = `${index * 0.15}s`;
        observer.observe(card);
    });

});
