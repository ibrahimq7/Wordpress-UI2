/**
 * Enterprise Header - MEP Procurement Platform
 * Vanilla JavaScript for Interactive Features
 * 
 * Features:
 * - Sticky header on scroll
 * - Mobile off-canvas menu toggle
 * - Mobile submenu accordion
 */

(function() {
    'use strict';

    // DOM Elements
    const mainHeader = document.getElementById('mainHeader');
    const mobileMenuToggle = document.getElementById('mobileMenuToggle');
    const offCanvasMenu = document.getElementById('offCanvasMenu');
    const offCanvasOverlay = document.getElementById('offCanvasOverlay');
    const closeMenuBtn = document.getElementById('closeMenuBtn');
    const offCanvasItems = document.querySelectorAll('.off-canvas-item.has-submenu');

    // ============================================
    // Sticky Header on Scroll
    // ============================================
    
    let lastScrollY = window.scrollY;
    const stickyThreshold = 100;

    function handleScroll() {
        const currentScrollY = window.scrollY;
        
        if (currentScrollY > stickyThreshold) {
            mainHeader.classList.add('sticky');
        } else {
            mainHeader.classList.remove('sticky');
        }
        
        lastScrollY = currentScrollY;
    }

    // Throttle scroll events for performance
    let ticking = false;
    
    window.addEventListener('scroll', function() {
        if (!ticking) {
            window.requestAnimationFrame(function() {
                handleScroll();
                ticking = false;
            });
            ticking = true;
        }
    });

    // ============================================
    // Mobile Menu Toggle
    // ============================================
    
    function openMobileMenu() {
        offCanvasMenu.classList.add('active');
        offCanvasOverlay.classList.add('active');
        mobileMenuToggle.classList.add('active');
        document.body.style.overflow = 'hidden';
    }

    function closeMobileMenu() {
        offCanvasMenu.classList.remove('active');
        offCanvasOverlay.classList.remove('active');
        mobileMenuToggle.classList.remove('active');
        document.body.style.overflow = '';
        
        // Close all open submenus
        offCanvasItems.forEach(function(item) {
            item.classList.remove('active');
        });
    }

    if (mobileMenuToggle) {
        mobileMenuToggle.addEventListener('click', function(e) {
            e.preventDefault();
            
            if (offCanvasMenu.classList.contains('active')) {
                closeMobileMenu();
            } else {
                openMobileMenu();
            }
        });
    }

    if (closeMenuBtn) {
        closeMenuBtn.addEventListener('click', function(e) {
            e.preventDefault();
            closeMobileMenu();
        });
    }

    if (offCanvasOverlay) {
        offCanvasOverlay.addEventListener('click', function(e) {
            closeMobileMenu();
        });
    }

    // ============================================
    // Mobile Submenu Accordion
    // ============================================
    
    offCanvasItems.forEach(function(item) {
        const link = item.querySelector('.off-canvas-link');
        
        if (link) {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                
                // Close other open submenus
                offCanvasItems.forEach(function(otherItem) {
                    if (otherItem !== item && otherItem.classList.contains('active')) {
                        otherItem.classList.remove('active');
                    }
                });
                
                // Toggle current submenu
                item.classList.toggle('active');
            });
        }
    });

    // ============================================
    // Keyboard Navigation Support
    // ============================================
    
    document.addEventListener('keydown', function(e) {
        // Close menu on Escape key
        if (e.key === 'Escape' && offCanvasMenu.classList.contains('active')) {
            closeMobileMenu();
        }
    });

    // ============================================
    // Mega Menu Accessibility (Desktop)
    // ============================================
    
    const megaMenuItems = document.querySelectorAll('.has-mega-menu');
    
    megaMenuItems.forEach(function(item) {
        const link = item.querySelector('.nav-link');
        const megaMenu = item.querySelector('.mega-menu');
        
        if (link && megaMenu) {
            // Keyboard support for mega menu
            link.addEventListener('keydown', function(e) {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    // Note: CSS handles hover, this is for keyboard users
                    megaMenu.style.visibility = megaMenu.style.visibility === 'visible' ? 'hidden' : 'visible';
                    megaMenu.style.opacity = megaMenu.style.opacity === '1' ? '0' : '1';
                }
            });
            
            // Close mega menu when mouse leaves
            item.addEventListener('mouseleave', function() {
                setTimeout(function() {
                    if (!item.matches(':hover')) {
                        megaMenu.style.visibility = '';
                        megaMenu.style.opacity = '';
                    }
                }, 100);
            });
        }
    });

    // ============================================
    // Search Trigger (Future Enhancement Ready)
    // ============================================
    
    const searchTrigger = document.querySelector('.search-trigger');
    
    if (searchTrigger) {
        searchTrigger.addEventListener('click', function(e) {
            e.preventDefault();
            // Placeholder for future search functionality
            console.log('Search triggered - Ready for integration');
        });
    }

    // ============================================
    // Resize Handler
    // ============================================
    
    let resizeTimer;
    
    window.addEventListener('resize', function() {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(function() {
            // Close mobile menu if switching to desktop
            if (window.innerWidth > 1024 && offCanvasMenu.classList.contains('active')) {
                closeMobileMenu();
            }
        }, 250);
    });

    // ============================================
    // Initialize on DOM Ready
    // ============================================
    
    function init() {
        // Check initial scroll position
        handleScroll();
        
        // Log initialization
        console.log('Enterprise Header initialized successfully');
    }

    // Run initialization
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

})();
