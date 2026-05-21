// LuxeThread Main JavaScript

document.addEventListener('DOMContentLoaded', function () {

    // ---- Navbar scroll effect ----
    const navbar = document.getElementById('mainNav');
    if (navbar) {
        window.addEventListener('scroll', function () {
            if (window.scrollY > 60) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        });
    }

    // ---- Auto-dismiss alerts ----
    setTimeout(function () {
        document.querySelectorAll('.luxury-alert').forEach(function (alert) {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            if (bsAlert) bsAlert.close();
        });
    }, 5000);

    // ---- Quantity controls ----
    document.querySelectorAll('.qty-minus').forEach(function (btn) {
        btn.addEventListener('click', function () {
            const input = this.closest('.qty-control').querySelector('.qty-input');
            const val = parseInt(input.value) || 1;
            if (val > 1) input.value = val - 1;
        });
    });

    document.querySelectorAll('.qty-plus').forEach(function (btn) {
        btn.addEventListener('click', function () {
            const input = this.closest('.qty-control').querySelector('.qty-input');
            const val = parseInt(input.value) || 1;
            const max = parseInt(input.getAttribute('max')) || 99;
            if (val < max) input.value = val + 1;
        });
    });

    // ---- Product image zoom on detail page ----
    const mainImg = document.getElementById('mainProductImg');
    if (mainImg) {
        mainImg.addEventListener('mousemove', function (e) {
            const rect = this.getBoundingClientRect();
            const x = ((e.clientX - rect.left) / rect.width) * 100;
            const y = ((e.clientY - rect.top) / rect.height) * 100;
            this.style.transformOrigin = `${x}% ${y}%`;
            this.style.transform = 'scale(1.35)';
        });
        mainImg.addEventListener('mouseleave', function () {
            this.style.transform = 'scale(1)';
        });
    }

    // ---- Size selector ----
    document.querySelectorAll('.size-option').forEach(function (btn) {
        btn.addEventListener('click', function () {
            document.querySelectorAll('.size-option').forEach(b => b.classList.remove('selected'));
            this.classList.add('selected');
            const sizeInput = document.getElementById('selectedSize');
            if (sizeInput) sizeInput.value = this.dataset.size;
        });
    });

    // ---- Scroll reveal for product cards ----
    const observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in-up');
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });

    document.querySelectorAll('.product-card').forEach(function (card) {
        observer.observe(card);
    });

    // ---- Smooth scroll for anchor links ----
    document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
        anchor.addEventListener('click', function (e) {
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                e.preventDefault();
                target.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });

    // ---- Cart quantity auto-submit on change ----
    document.querySelectorAll('.cart-qty-input').forEach(function (input) {
        input.addEventListener('change', function () {
            this.closest('form').submit();
        });
    });

});
