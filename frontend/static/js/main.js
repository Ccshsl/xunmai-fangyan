const Xunmai = {
    init: function() {
        this.setupScrollAnimations();
        this.setupNavbar();
        this.setupSmoothScrolling();
    },

    setupScrollAnimations: function() {
        const items = document.querySelectorAll('.timeline-item, .fade-in');
        if (!items.length) return;

        let ticking = false;
        let animatedCount = 0;

        items.forEach((item, index) => {
            item.style.opacity = '0';
            item.style.transform = 'translateY(30px)';
            item.style.transition = `opacity 0.5s ease ${index * 0.05}s, transform 0.5s ease ${index * 0.05}s`;
        });

        const checkVisibility = () => {
            if (ticking) return;
            ticking = true;

            requestAnimationFrame(() => {
                const windowHeight = window.innerHeight;

                items.forEach((item, index) => {
                    if (item.dataset.animated === 'true') return;

                    const rect = item.getBoundingClientRect();
                    if (rect.top < windowHeight * 0.9 && rect.bottom > 0) {
                        item.style.opacity = '1';
                        item.style.transform = 'translateY(0)';
                        item.dataset.animated = 'true';
                        animatedCount++;

                        if (animatedCount >= items.length) {
                            window.removeEventListener('scroll', checkVisibility);
                        }
                    }
                });

                ticking = false;
            });
        };

        window.addEventListener('scroll', checkVisibility, { passive: true });
        checkVisibility();
    },

    setupNavbar: function() {
        const navbar = document.querySelector('.navbar');
        if (!navbar) return;

        const handleScroll = () => {
            if (window.scrollY > 50) {
                navbar.style.boxShadow = '0 4px 30px rgba(0, 0, 0, 0.15), 0 0 60px rgba(6, 182, 212, 0.1)';
            } else {
                navbar.style.boxShadow = '0 4px 30px rgba(0, 0, 0, 0.1), 0 0 60px rgba(6, 182, 212, 0.15)';
            }
        };

        window.addEventListener('scroll', handleScroll, { passive: true });
    },

    setupSmoothScrolling: function() {
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function(e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({ behavior: 'smooth' });
                }
            });
        });
    },

    createDynamicBackground: function(options = {}) {
        const lightLayer = document.getElementById('light-layer');
        if (!lightLayer) return;

        const config = {
            floatLights: options.floatLights || 3,
            stars: options.stars || 6
        };

        for (let i = 0; i < config.floatLights; i++) {
            const floatLight = document.createElement('div');
            floatLight.className = 'float-light';
            const colors = ['blue', 'cyan', 'green'];
            floatLight.classList.add(colors[i % colors.length]);
            floatLight.style.left = Math.random() * 100 + '%';
            floatLight.style.top = Math.random() * 100 + '%';
            floatLight.style.width = (15 + Math.random() * 10) + 'px';
            floatLight.style.height = floatLight.style.width;
            floatLight.style.animationDelay = Math.random() * 10 + 's';
            floatLight.style.animationDuration = (20 + Math.random() * 10) + 's';
            floatLight.style.willChange = 'transform';
            floatLight.style.transform = 'translateZ(0)';
            lightLayer.appendChild(floatLight);
        }

        for (let i = 0; i < config.stars; i++) {
            const star = document.createElement('div');
            star.className = 'star';
            star.style.left = Math.random() * 100 + '%';
            star.style.top = Math.random() * 100 + '%';
            star.style.width = '2px';
            star.style.height = '2px';
            star.style.animationDelay = Math.random() * 3 + 's';
            star.style.animationDuration = (3 + Math.random() * 2) + 's';
            lightLayer.appendChild(star);
        }
    }
};

document.addEventListener('DOMContentLoaded', () => {
    Xunmai.init();
    Xunmai.createDynamicBackground();
});
