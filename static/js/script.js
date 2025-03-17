// Custom JavaScript for Python Learn

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Highlight active nav item
    const currentLocation = window.location.pathname;
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    
    navLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (href && currentLocation.includes(href) && href !== '/') {
            link.classList.add('active');
        } else if (href === '/' && currentLocation === '/') {
            link.classList.add('active');
        }
    });

    // Code syntax highlighting for pre code blocks
    document.querySelectorAll('pre code').forEach((el) => {
        if (window.hljs) {
            hljs.highlightElement(el);
        }
    });

    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            if (targetId !== '#') {
                const targetElement = document.querySelector(targetId);
                if (targetElement) {
                    targetElement.scrollIntoView({
                        behavior: 'smooth'
                    });
                }
            }
        });
    });

    // Add animation to Pro badges
    const proBadges = document.querySelectorAll('.badge.bg-warning');
    proBadges.forEach(badge => {
        badge.addEventListener('mouseover', function() {
            this.style.transform = 'scale(1.1)';
            this.style.transition = 'transform 0.3s ease';
        });
        badge.addEventListener('mouseout', function() {
            this.style.transform = 'scale(1)';
        });
    });
}); 