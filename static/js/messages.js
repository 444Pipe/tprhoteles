// Interactive message behavior for site alerts
document.addEventListener('DOMContentLoaded', function () {
    // inject minimal fade-out CSS
    const style = document.createElement('style');
    style.textContent = '\n+.alert.fade-out{ opacity:0; transform:translateY(-8px); transition:opacity .35s ease, transform .35s ease; }\n+';
    document.head.appendChild(style);

    const alerts = document.querySelectorAll('.container .alert');
    alerts.forEach(function (alert) {
        const AUTO_HIDE_MS = 6000;
        let remaining = AUTO_HIDE_MS;
        let hideTimer = null;
        let startTime = null;

        function startTimer() {
            startTime = Date.now();
            hideTimer = setTimeout(hideAlert, remaining);
        }

        function pauseTimer() {
            if (!hideTimer) return;
            clearTimeout(hideTimer);
            hideTimer = null;
            const elapsed = Date.now() - startTime;
            remaining = Math.max(0, remaining - elapsed);
        }

        function hideAlert() {
            alert.classList.add('fade-out');
            setTimeout(function () { if (alert.parentNode) alert.remove(); }, 380);
        }

        // Pause on hover
        alert.addEventListener('mouseenter', pauseTimer);
        alert.addEventListener('mouseleave', function () {
            startTimer();
        });

        // Close button immediate removal
        const closeBtn = alert.querySelector('.btn-close');
        if (closeBtn) closeBtn.addEventListener('click', function () { if (alert.parentNode) alert.remove(); });

        // Start countdown
        startTimer();
    });
});
