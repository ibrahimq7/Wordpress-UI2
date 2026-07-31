/**
 * Header Component JavaScript
 * Handles: Sticky header, Mega menu, Mobile drawer
 */

(function() {
    'use strict';

    // DOM Elements
    const header = document.getElementById('mainHeader');
    const megaMenu = document.getElementById('megaMenu');
    const mobileHamburger = document.querySelector('.mobile-hamburger');
    const mobileDrawer = document.getElementById('mobileDrawer');
    const drawerOverlay = document.getElementById('drawerOverlay');
    const drawerClose = document.querySelector('.drawer-close');
    const productsNavItem = document.querySelector('.has-mega-menu');

    // ============================================
    // STICKY HEADER
    // ============================================
    let lastScrollY = window.scrollY;
    const stickyThreshold = 100;

    function handleScroll() {
        const currentScrollY = window.scrollY;
        
        if (currentScrollY > stickyThreshold) {
            header.classList.add('sticky');
        } else {
            header.classList.remove('sticky');
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

    // Initial check on page load
    handleScroll();

    // ============================================
    // MEGA MENU
    // ============================================
    if (productsNavItem && megaMenu) {
        const navLink = productsNavItem.querySelector('.nav-link');
        let hoverTimeout;

        // Desktop hover behavior
        productsNavItem.addEventListener('mouseenter', function() {
            clearTimeout(hoverTimeout);
            megaMenu.classList.add('active');
            navLink.classList.add('active');
        });

        productsNavItem.addEventListener('mouseleave', function() {
            hoverTimeout = setTimeout(function() {
                megaMenu.classList.remove('active');
                navLink.classList.remove('active');
            }, 150);
        });

        megaMenu.addEventListener('mouseenter', function() {
            clearTimeout(hoverTimeout);
        });

        megaMenu.addEventListener('mouseleave', function() {
            hoverTimeout = setTimeout(function() {
                megaMenu.classList.remove('active');
                navLink.classList.remove('active');
            }, 150);
        });

        // Touch/click support for mobile
        navLink.addEventListener('click', function(e) {
            if (window.innerWidth <= 1024) {
                e.preventDefault();
                megaMenu.classList.toggle('active');
                navLink.classList.toggle('active');
            }
        });
    }

    // Close mega menu when clicking outside
    document.addEventListener('click', function(e) {
        if (megaMenu && !megaMenu.contains(e.target) && 
            (!productsNavItem || !productsNavItem.contains(e.target))) {
            megaMenu.classList.remove('active');
            if (productsNavItem) {
                productsNavItem.querySelector('.nav-link').classList.remove('active');
            }
        }
    });

    // ============================================
    // MOBILE DRAWER
    // ============================================
    function openDrawer() {
        mobileDrawer.classList.add('active');
        drawerOverlay.classList.add('active');
        mobileHamburger.classList.add('active');
        document.body.style.overflow = 'hidden';
    }

    function closeDrawer() {
        mobileDrawer.classList.remove('active');
        drawerOverlay.classList.remove('active');
        mobileHamburger.classList.remove('active');
        document.body.style.overflow = '';
    }

    if (mobileHamburger) {
        mobileHamburger.addEventListener('click', function() {
            if (mobileDrawer.classList.contains('active')) {
                closeDrawer();
            } else {
                openDrawer();
            }
        });
    }

    if (drawerClose) {
        drawerClose.addEventListener('click', closeDrawer);
    }

    if (drawerOverlay) {
        drawerOverlay.addEventListener('click', closeDrawer);
    }

    // Close drawer on escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && mobileDrawer.classList.contains('active')) {
            closeDrawer();
        }
    });

    // Handle resize events
    let resizeTimeout;
    window.addEventListener('resize', function() {
        clearTimeout(resizeTimeout);
        resizeTimeout = setTimeout(function() {
            // Close drawer on desktop
            if (window.innerWidth > 1024 && mobileDrawer.classList.contains('active')) {
                closeDrawer();
            }
        }, 150);
    });

    // ============================================
    // SMOOTH SCROLL FOR ANCHOR LINKS
    // ============================================
    document.querySelectorAll('a[href^="#"]').forEach(function(anchor) {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href !== '#' && href.length > 1) {
                const target = document.querySelector(href);
                if (target) {
                    e.preventDefault();
                    const headerHeight = header.offsetHeight;
                    const targetPosition = target.getBoundingClientRect().top + window.scrollY - headerHeight;
                    
                    window.scrollTo({
                        top: targetPosition,
                        behavior: 'smooth'
                    });

                    // Close drawer if open
                    if (mobileDrawer.classList.contains('active')) {
                        closeDrawer();
                    }
                }
            }
        });
    });

})();
