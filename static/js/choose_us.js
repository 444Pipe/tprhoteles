// Animaciones para la sección "¿Por qué elegirnos?"
document.addEventListener('DOMContentLoaded', function () {
    const cards = document.querySelectorAll('.choose-card');

    // Disable tilt on touch devices for better UX/performance
    const isTouch = ('ontouchstart' in window) || navigator.maxTouchPoints > 0;

    // IntersectionObserver para revelar al hacer scroll
    const io = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('in-view');
                io.unobserve(entry.target);
            }
        });
    }, { threshold: 0.12 });

    cards.forEach(card => io.observe(card));

    // Efecto tilt simple en hover: solo para no-touch devices
    if (!isTouch) {
        cards.forEach(card => {
            function onMove(e) {
                const rect = card.getBoundingClientRect();
                const x = (e.clientX - rect.left) / rect.width - 0.5; // -0.5 .. 0.5
                const y = (e.clientY - rect.top) / rect.height - 0.5;
                const rx = (-y) * 6; // rotateX
                const ry = (x) * 8;  // rotateY
                card.style.transform = `translateZ(0) perspective(700px) rotateX(${rx}deg) rotateY(${ry}deg) scale(1.02)`;
                card.style.transition = 'transform 0.08s linear';
            }

            function onLeave() {
                card.style.transform = '';
                card.style.transition = 'transform 0.35s cubic-bezier(.2,.8,.2,1)';
            }

            card.addEventListener('mousemove', onMove);
            card.addEventListener('mouseleave', onLeave);
        });
    }
});
