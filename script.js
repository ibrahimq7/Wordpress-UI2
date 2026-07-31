/**
 * Enterprise Header - MEP Procurement Platform
 * Vanilla JavaScript for Interactive Functionality
 */

(function() {
    'use strict';

    // DOM Elements
    const mainHeader = document.getElementById('mainHeader');
    const mobileMenuToggle = document.getElementById('mobileMenuToggle');
    const offcanvasMenu = document.getElementById('offcanvasMenu');
    const offcanvasOverlay = document.getElementById('offcanvasOverlay');
    const offcanvasClose = document.getElementById('offcanvasClose');
    const offcanvasItems = document.querySelectorAll('.offcanvas-item.has-submenu');

    // State
    let lastScrollY = window.scrollY;
    let ticking = false;

    /**
     * Initialize all functionality
     */
    function init() {
        setupStickyHeader();
        setupMobileMenu();
        setupOffcanvasSubmenus();
        setupScrollListener();
    }

    /**
     * Sticky Header with scroll detection
     */
    function setupStickyHeader() {
        window.addEventListener('scroll', function() {
            if (!ticking) {
                window.requestAnimationFrame(function() {
                    handleScroll();
                    ticking = false;
                });
                ticking = true;
            }
        });
    }

    /**
     * Handle scroll events for sticky header
     */
    function handleScroll() {
        const currentScrollY = window.scrollY;

        // Add sticky class when scrolled past top bar height
        if (currentScrollY > 40) {
            mainHeader.classList.add('sticky');
            document.body.classList.add('header-sticky-active');
        } else {
            mainHeader.classList.remove('sticky');
            document.body.classList.remove('header-sticky-active');
        }

        lastScrollY = currentScrollY;
    }

    /**
     * Setup scroll listener with requestAnimationFrame
     */
    function setupScrollListener() {
        // Initial check
        handleScroll();
    }

    /**
     * Mobile Menu Toggle
     */
    function setupMobileMenu() {
        if (!mobileMenuToggle || !offcanvasMenu || !offcanvasOverlay) return;

        // Open menu
        mobileMenuToggle.addEventListener('click', function(e) {
            e.preventDefault();
            openOffcanvasMenu();
        });

        // Close menu
        offcanvasClose.addEventListener('click', function(e) {
            e.preventDefault();
            closeOffcanvasMenu();
        });

        offcanvasOverlay.addEventListener('click', function() {
            closeOffcanvasMenu();
        });

        // Close on escape key
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape' && offcanvasMenu.classList.contains('active')) {
                closeOffcanvasMenu();
            }
        });
    }

    /**
     * Open offcanvas menu
     */
    function openOffcanvasMenu() {
        mobileMenuToggle.classList.add('active');
        offcanvasMenu.classList.add('active');
        offcanvasOverlay.classList.add('active');
        document.body.style.overflow = 'hidden';
        
        // Trap focus inside menu
        trapFocus(offcanvasMenu);
    }

    /**
     * Close offcanvas menu
     */
    function closeOffcanvasMenu() {
        mobileMenuToggle.classList.remove('active');
        offcanvasMenu.classList.remove('active');
        offcanvasOverlay.classList.remove('active');
        document.body.style.overflow = '';
        
        // Return focus to menu toggle
        mobileMenuToggle.focus();
    }

    /**
     * Setup offcanvas submenu toggles
     */
    function setupOffcanvasSubmenus() {
        offcanvasItems.forEach(function(item) {
            const link = item.querySelector('.offcanvas-link');
            
            if (link) {
                link.addEventListener('click', function(e) {
                    e.preventDefault();
                    
                    // Close other open submenus
                    offcanvasItems.forEach(function(otherItem) {
                        if (otherItem !== item && otherItem.classList.contains('active')) {
                            otherItem.classList.remove('active');
                        }
                    });
                    
                    // Toggle current submenu
                    item.classList.toggle('active');
                });
            }
        });
    }

    /**
     * Trap focus within an element for accessibility
     */
    function trapFocus(element) {
        const focusableElements = element.querySelectorAll(
            'a[href], button:not([disabled]), textarea:not([disabled]), input:not([disabled]), select:not([disabled]), [tabindex]:not([tabindex="-1"])'
        );
        
        if (focusableElements.length === 0) return;

        const firstFocusable = focusableElements[0];
        const lastFocusable = focusableElements[focusableElements.length - 1];

        firstFocusable.focus();

        element.addEventListener('keydown', function(e) {
            if (e.key !== 'Tab') return;

            if (e.shiftKey) {
                if (document.activeElement === firstFocusable) {
                    lastFocusable.focus();
                    e.preventDefault();
                }
            } else {
                if (document.activeElement === lastFocusable) {
                    firstFocusable.focus();
                    e.preventDefault();
                }
            }
        });
    }

    /**
     * Handle window resize
     */
    let resizeTimer;
    window.addEventListener('resize', function() {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(function() {
            // Close mobile menu if switching to desktop
            if (window.innerWidth > 1024 && offcanvasMenu.classList.contains('active')) {
                closeOffcanvasMenu();
            }
        }, 250);
    });

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
