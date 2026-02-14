document.addEventListener('DOMContentLoaded', function () {
    const buttons = document.querySelectorAll('.js-hero-btn');
    const reservarBtn = document.querySelector('.js-hero-reservar');

    if (!buttons.length) return;

    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    const style = document.createElement('style');
    style.textContent = `
        .hero-toast-msg {
            position: fixed;
            left: 50%;
            bottom: 24px;
            transform: translateX(-50%) translateY(10px);
            background: rgba(20, 20, 20, 0.92);
            color: #fff;
            padding: 10px 14px;
            border-radius: 10px;
            font-size: 0.9rem;
            z-index: 1200;
            opacity: 0;
            pointer-events: none;
            transition: opacity 0.22s ease, transform 0.22s ease;
        }
        .hero-toast-msg.show {
            opacity: 1;
            transform: translateX(-50%) translateY(0);
        }
        .hero-cta-group .js-hero-btn {
            position: relative;
            overflow: hidden;
            transition: transform .18s ease, box-shadow .18s ease;
            will-change: transform;
        }
        .hero-cta-group .js-hero-btn.hero-press {
            transform: scale(0.98);
        }
        .hero-cta-group .js-hero-btn .hero-ripple {
            position: absolute;
            border-radius: 999px;
            transform: translate(-50%, -50%);
            background: rgba(255, 255, 255, 0.35);
            pointer-events: none;
            animation: heroRipple .55s ease-out;
        }
        .hero-cta-group .js-hero-reservar.disabled.bump {
            animation: heroBump .25s ease;
        }
        @keyframes heroRipple {
            from { width: 0; height: 0; opacity: 0.7; }
            to { width: 220px; height: 220px; opacity: 0; }
        }
        @keyframes heroBump {
            0%, 100% { transform: translateX(0); }
            25% { transform: translateX(-4px); }
            50% { transform: translateX(4px); }
            75% { transform: translateX(-3px); }
        }
    `;
    document.head.appendChild(style);

    let toastTimer = null;
    function showToast(message) {
        const old = document.querySelector('.hero-toast-msg');
        if (old) old.remove();

        const toast = document.createElement('div');
        toast.className = 'hero-toast-msg';
        toast.textContent = message;
        document.body.appendChild(toast);

        requestAnimationFrame(function () {
            toast.classList.add('show');
        });

        clearTimeout(toastTimer);
        toastTimer = setTimeout(function () {
            toast.classList.remove('show');
            setTimeout(function () { toast.remove(); }, 220);
        }, 1800);
    }

    buttons.forEach(function (button) {
        button.addEventListener('click', function (event) {
            const rect = button.getBoundingClientRect();
            const ripple = document.createElement('span');
            ripple.className = 'hero-ripple';
            ripple.style.left = (event.clientX - rect.left) + 'px';
            ripple.style.top = (event.clientY - rect.top) + 'px';
            button.appendChild(ripple);
            setTimeout(function () { ripple.remove(); }, 560);

            button.classList.add('hero-press');
            setTimeout(function () { button.classList.remove('hero-press'); }, 140);
        });

        if (prefersReducedMotion) return;

        button.addEventListener('mousemove', function (event) {
            const rect = button.getBoundingClientRect();
            const x = (event.clientX - rect.left) / rect.width - 0.5;
            const y = (event.clientY - rect.top) / rect.height - 0.5;
            button.style.transform = `translate(${x * 3}px, ${y * 3}px)`;
        });

        button.addEventListener('mouseleave', function () {
            button.style.transform = '';
        });
    });

    if (reservarBtn && reservarBtn.classList.contains('disabled')) {
        reservarBtn.addEventListener('click', function (event) {
            event.preventDefault();
            reservarBtn.classList.add('bump');
            setTimeout(function () { reservarBtn.classList.remove('bump'); }, 260);
            showToast('Primero carga hoteles para habilitar reservas.');
        });
    }
});
