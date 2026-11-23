/**
 * LUMINA — Main JavaScript
 * Scroll reveals, hamburger menu, form interactivity
 */

document.addEventListener('DOMContentLoaded', function() {
  initHamburgerMenu();
  initScrollReveal();
});

/**
 * Hamburger Menu Toggle
 */
function initHamburgerMenu() {
  const hamburger = document.getElementById('hamburger');
  const navMenu = document.getElementById('navMenu');
  const navLinks = document.querySelectorAll('.nav-link');

  if (!hamburger) return;

  hamburger.addEventListener('click', function() {
    navMenu.classList.toggle('active');
  });

  navLinks.forEach(link => {
    link.addEventListener('click', function() {
      navMenu.classList.remove('active');
    });
  });
}

/**
 * Scroll Reveal Animation
 * Fade + rise elements as they enter viewport
 */
function initScrollReveal() {
  const reveals = document.querySelectorAll('.card, .service-card, .testimonial, details, .enquiry-form');

  if (!window.IntersectionObserver) {
    // Fallback for older browsers
    reveals.forEach(el => el.classList.add('reveal'));
    return;
  }

  const observer = new IntersectionObserver(function(entries) {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('reveal');
        observer.unobserve(entry.target);
      }
    });
  }, {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
  });

  reveals.forEach(el => observer.observe(el));
}

/**
 * Smooth scroll for anchor links
 */
document.querySelectorAll('a[href*="#"]').forEach(anchor => {
  anchor.addEventListener('click', function(e) {
    const href = this.getAttribute('href');
    if (!href) return;

    const parts = href.split('#');
    const path = parts[0];
    const hash = parts[1];

    if (!hash) return;

    // Check if we are on the same page or if path is empty/index
    const currentPath = window.location.pathname;
    const isIndexPage = currentPath === '/' || currentPath === '/index' || path === '' || path === '/';

    if (isIndexPage && (path === '' || path === '/' || path === currentPath)) {
      const target = document.getElementById(hash);
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth' });
        history.pushState(null, null, '#' + hash);
      }
    }
  });
});
