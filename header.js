/**
 * Enterprise MEP Procurement Header
 * Premium Navigation Component JavaScript
 */

(function() {
    'use strict';

    // DOM Elements
    const header = document.getElementById('mepHeader');
    const mobileToggle = document.querySelector('.mobile-toggle');
    const mobileMenu = document.getElementById('mobileMenu');
    const mobileOverlay = document.getElementById('mobileOverlay');
    const mobileClose = document.querySelector('.mobile-close');
    const mobileSubmenuButtons = document.querySelectorAll('.mobile-nav-link.has-submenu');

    // State
    let isMenuOpen = false;
    let lastScrollY = window.scrollY;
    let ticking = false;

    /**
     * Initialize all event listeners
     */
    function init() {
        // Scroll handling
        window.addEventListener('scroll', handleScroll, { passive: true });
        
        // Mobile menu toggle
        if (mobileToggle) {
            mobileToggle.addEventListener('click', toggleMobileMenu);
        }
        
        // Mobile menu close
        if (mobileClose) {
            mobileClose.addEventListener('click', closeMobileMenu);
        }
        
        // Overlay click to close
        if (mobileOverlay) {
            mobileOverlay.addEventListener('click', closeMobileMenu);
        }
        
        // Mobile submenu toggles
        mobileSubmenuButtons.forEach(button => {
            button.addEventListener('click', handleSubmenuToggle);
        });
        
        // Keyboard navigation
        document.addEventListener('keydown', handleKeyboardNavigation);
        
        // Handle initial scroll state
        updateHeaderState();
    }

    /**
     * Handle scroll events with requestAnimationFrame
     */
    function handleScroll() {
        lastScrollY = window.scrollY;
        
        if (!ticking) {
            window.requestAnimationFrame(() => {
                updateHeaderState();
                ticking = false;
            });
            ticking = true;
        }
    }

    /**
     * Update header state based on scroll position
     */
    function updateHeaderState() {
        if (lastScrollY > 50) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    }

    /**
     * Toggle mobile menu open/closed
     */
    function toggleMobileMenu() {
        if (isMenuOpen) {
            closeMobileMenu();
        } else {
            openMobileMenu();
        }
    }

    /**
     * Open mobile menu
     */
    function openMobileMenu() {
        isMenuOpen = true;
        mobileToggle.classList.add('active');
        mobileMenu.classList.add('active');
        mobileOverlay.classList.add('active');
        document.body.style.overflow = 'hidden';
        
        // Trap focus in mobile menu
        trapFocus(mobileMenu);
    }

    /**
     * Close mobile menu
     */
    function closeMobileMenu() {
        isMenuOpen = false;
        mobileToggle.classList.remove('active');
        mobileMenu.classList.remove('active');
        mobileOverlay.classList.remove('active');
        document.body.style.overflow = '';
        
        // Return focus to toggle button
        if (mobileToggle) {
            mobileToggle.focus();
        }
    }

    /**
     * Handle mobile submenu toggle
     */
    function handleSubmenuToggle(e) {
        const button = e.currentTarget;
        const isActive = button.classList.contains('active');
        
        // Close all other submenus
        mobileSubmenuButtons.forEach(btn => {
            if (btn !== button) {
                btn.classList.remove('active');
            }
        });
        
        // Toggle current submenu
        button.classList.toggle('active', !isActive);
    }

    /**
     * Handle keyboard navigation
     */
    function handleKeyboardNavigation(e) {
        // Close menu on Escape key
        if (e.key === 'Escape' && isMenuOpen) {
            closeMobileMenu();
        }
    }

    /**
     * Trap focus within an element (for accessibility)
     */
    function trapFocus(element) {
        const focusableElements = element.querySelectorAll(
            'a[href], button:not([disabled]), textarea:not([disabled]), input[type="text"]:not([disabled]), input[type="radio"]:not([disabled]), input[type="checkbox"]:not([disabled]), select:not([disabled])'
        );
        
        const firstFocusable = focusableElements[0];
        const lastFocusable = focusableElements[focusableElements.length - 1];

        if (firstFocusable) {
            firstFocusable.focus();
        }

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
     * Handle resize events
     */
    let resizeTimer;
    window.addEventListener('resize', () => {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(() => {
            // Close mobile menu if switching to desktop
            if (window.innerWidth > 1200 && isMenuOpen) {
                closeMobileMenu();
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
