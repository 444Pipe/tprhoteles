// Interacciones para la sección "¿Por qué elegirnos?"
document.addEventListener('DOMContentLoaded', function () {
    const cards = document.querySelectorAll('.choose-card');
    if (!cards.length) return;

    const isTouch = ('ontouchstart' in window) || navigator.maxTouchPoints > 0;
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    const style = document.createElement('style');
    style.textContent = `
        .choose-card {
            position: relative;
            overflow: hidden;
            transform-style: preserve-3d;
            transition: transform .28s cubic-bezier(.2,.8,.2,1), box-shadow .28s ease;
        }
        .choose-card::after {
            content: '';
            position: absolute;
            top: 0;
            left: -140%;
            width: 90%;
            height: 100%;
            background: linear-gradient(110deg, transparent 0%, rgba(255,255,255,.22) 50%, transparent 100%);
            transform: skewX(-18deg);
            pointer-events: none;
        }
        .choose-card.card-glow::after {
            animation: cardShine .72s ease;
        }
        .choose-card .choose-ripple {
            position: absolute;
            border-radius: 999px;
            transform: translate(-50%, -50%);
            background: rgba(255, 203, 43, .25);
            pointer-events: none;
            animation: chooseRipple .55s ease-out;
        }
        .choose-card i {
            transition: transform .28s ease, filter .28s ease;
        }
        .choose-card.card-active i {
            transform: translateY(-2px) scale(1.08);
            filter: drop-shadow(0 5px 8px rgba(255,203,43,.24));
        }
        @keyframes chooseRipple {
            from { width: 0; height: 0; opacity: .7; }
            to { width: 220px; height: 220px; opacity: 0; }
        }
        @keyframes cardShine {
            from { left: -140%; }
            to { left: 160%; }
        }
    `;
    document.head.appendChild(style);

    const io = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (!entry.isIntersecting) return;
            const card = entry.target;
            const index = Number(card.dataset.revealIndex || 0);
            const reveal = () => card.classList.add('in-view');
            if (prefersReducedMotion) {
                reveal();
            } else {
                setTimeout(reveal, index * 90);
            }
            io.unobserve(card);
        });
    }, { threshold: 0.14 });

    cards.forEach((card, index) => {
        card.dataset.revealIndex = String(index);
        card.setAttribute('tabindex', '0');
        io.observe(card);

        const activateCard = () => {
            card.classList.add('card-active', 'card-glow');
            setTimeout(() => card.classList.remove('card-glow'), 750);
        };

        const deactivateCard = () => {
            card.classList.remove('card-active');
            if (!prefersReducedMotion) card.style.transform = '';
        };

        card.addEventListener('mouseenter', activateCard);
        card.addEventListener('mouseleave', deactivateCard);
        card.addEventListener('focus', activateCard);
        card.addEventListener('blur', deactivateCard);

        card.addEventListener('click', (event) => {
            const rect = card.getBoundingClientRect();
            const ripple = document.createElement('span');
            ripple.className = 'choose-ripple';
            ripple.style.left = `${event.clientX - rect.left}px`;
            ripple.style.top = `${event.clientY - rect.top}px`;
            card.appendChild(ripple);
            setTimeout(() => ripple.remove(), 560);
        });

        card.addEventListener('keydown', (event) => {
            if (event.key === 'Enter' || event.key === ' ') {
                event.preventDefault();
                activateCard();
                setTimeout(deactivateCard, 320);
            }
        });

        if (!isTouch && !prefersReducedMotion) {
            card.addEventListener('mousemove', (event) => {
                const rect = card.getBoundingClientRect();
                const x = (event.clientX - rect.left) / rect.width - 0.5;
                const y = (event.clientY - rect.top) / rect.height - 0.5;
                const rx = (-y) * 6;
                const ry = x * 8;
                card.style.transform = `perspective(800px) rotateX(${rx}deg) rotateY(${ry}deg) scale(1.02)`;
            });
        }
    });
});
