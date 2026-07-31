# Elementor Integration Notes - Enterprise Header

## Overview
This header component is designed for seamless conversion into WordPress Elementor Pro. The HTML structure follows Elementor's container-based approach and uses clean, modular CSS that can be easily replicated using Elementor's styling controls.

---

## File Structure
```
header.html     → Main HTML structure
header.css      → Complete styling (840+ lines)
script.js       → Vanilla JS for interactivity
```

---

## Elementor Conversion Guide

### 1. TOP BAR SECTION

**Elementor Structure:**
- **Section**: Full-width, single column
- **Height**: Custom → 40px
- **Background**: `#0a1628` (Primary color)

**Container Setup:**
```
Section (Top Bar)
└── Container (max-width: 1400px)
    ├── Container (Left - Flex row)
    │   ├── Icon Box (Email)
    │   └── Icon Box (Phone)
    └── Container (Right - Flex row)
        ├── Heading (Serving text)
        ├── Divider (1px, 14px height)
        └── Icon Box (Office hours)
```

**Styling Notes:**
- Font size: 12px (XS)
- Text color: `#d4d4d4` (Gray 300)
- Hover color: `#c9a227` (Accent gold)
- Gap between items: 32px left, 24px right

---

### 2. MAIN HEADER SECTION

**Elementor Structure:**
- **Section**: Full-width, sticky on scroll
- **Height**: Custom → 92px (desktop), 80px (sticky)
- **Background**: Gradient with glassmorphism effect

**Gradient Settings:**
```
Type: Linear
Angle: 135deg
Color 1: rgba(255, 255, 255, 0.95) at 0%
Color 2: rgba(255, 255, 255, 0.85) at 100%
Backdrop Filter: Blur 20px
```

**Container Setup:**
```
Section (Main Header)
└── Container (max-width: 1400px, Flex justify: Space Between)
    ├── Container (Logo - Left)
    │   └── Site Logo / Image Box
    ├── Container (Navigation - Center, Flex grow: 1)
    │   └── Nav Menu Widget
    └── Container (Actions - Right)
        ├── Icon (Search trigger)
        ├── Button (Request Quote)
        └── Hamburger Menu (Mobile only)
```

---

### 3. MEGA MENU CONFIGURATION

**Elementor Approach:**
Use Elementor Pro's Mega Menu capability or create a custom template:

**Option A - Elementor Pro Nav Menu:**
1. Go to Templates → Theme Builder → Header
2. Add Nav Menu widget
3. Enable "Mega Menu" in advanced settings
4. Create menu items with custom templates

**Option B - Custom Template:**
```
Mega Menu Container (Absolute position)
├── Container (Grid: 4 columns)
│   ├── Column 1 (Systems)
│   │   └── Icon List (Plumbing, HVAC, Fire Fighting)
│   ├── Column 2 (Equipment)
│   │   └── Icon List (Electrical, Gas, Pumps)
│   ├── Column 3 (Specialized + Brands)
│   │   ├── Icon List (Water Treatment, Tools)
│   │   └── Image Carousel (Brand logos)
│   └── Column 4 (Promo Card)
│       ├── Heading
│       ├── Text Editor
│       └── Button
```

**Mega Menu Styling:**
- Width: 1200px max
- Padding: 48px
- Background: `#ffffff`
- Border-radius: 16px
- Box-shadow: `0 25px 50px -12px rgba(0, 0, 0, 0.25)`
- Animation: Fade in + slide up (250ms ease)

---

### 4. REQUEST QUOTE BUTTON

**Button Styling:**
```
Background Type: Gradient
Gradient: Linear 135deg
Color 1: #0a1628
Color 2: #1a365d
Text Color: #ffffff
Padding: 16px 32px
Border Radius: 8px
Font Weight: 600
Font Size: 14px
Box Shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1)
Hover: TranslateY(-2px), Enhanced shadow
```

**Icon Position:** Right of text, 8px gap

---

### 5. STICKY HEADER SETUP

**Elementor Sticky Settings:**
1. Select the Main Header section
2. Advanced → Motion Effects → Sticky → Top
3. Sticky On: Desktop, Tablet, Mobile
4. Offset: 0
5. Effects Offset: 40px (trigger point)

**CSS Classes to Add:**
- Section: `main-header`
- When sticky active: `sticky` class auto-applied via JS

**Alternative (Elementor Pro):**
Use Theme Builder's sticky header feature instead of custom JS.

---

### 6. MOBILE OFF-CANVAS MENU

**Elementor Approach:**
Use Elementor's built-in mobile menu OR create custom:

**Custom Implementation:**
```
Popup Template (Off-canvas)
├── Container (Header - 80px height)
│   ├── Site Logo
│   └── Close Icon
├── Container (Content - Scrollable)
│   ├── Accordion / Toggle (Menu items)
│   │   └── Nested items for submenus
│   ├── Container (Contact info)
│   │   ├── Icon Box (Email)
│   │   └── Icon Box (Phone)
│   └── Button (Request Quote - Full width)
```

**Popup Settings:**
- Trigger: Hamburger icon click
- Position: Right side
- Width: 400px (desktop), 100% (mobile)
- Overlay: Enabled, blur effect
- Animation: Slide from right (350ms)

---

### 7. RESPONSIVE BREAKPOINTS

**Desktop (>1024px):**
- Full navigation visible
- Mega menu enabled
- Request quote button with text

**Tablet (768px - 1024px):**
- Hide serving text in top bar
- Hide desktop navigation
- Show hamburger menu
- Mega menu disabled

**Mobile (<768px):**
- Top bar stacks vertically
- Logo tagline hidden
- Search icon only (no label)
- Request quote → icon only
- Off-canvas full width

**Small Mobile (<480px):**
- Hide divider in top bar
- Hide request quote button entirely

---

### 8. CSS VARIABLES MAPPING

Map these to Elementor Global Colors/Fonts:

**Colors:**
- Primary: `#0a1628` → Elementor Primary Color
- Accent: `#c9a227` → Elementor Accent Color
- Gray scale: Use Elementor's text colors

**Typography:**
- Font Family: Inter → Elementor System Font
- Sizes: Map to Elementor's typography scale

**Spacing:**
- Use Elementor's spacing controls (padding/margin)
- Reference CSS variables for consistency

---

### 9. CUSTOM CSS IN ELEMENTOR

Add this to Site Settings → Custom CSS or individual widgets:

```css
/* Glassmorphism effect */
.main-header {
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
}

/* Mega menu hover animation */
.nav-item:hover .mega-menu {
    opacity: 1;
    visibility: visible;
    transform: translateX(-50%) translateY(0);
}

/* Button hover effect */
.btn-request-quote:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-lg);
}

/* Mobile menu animations */
.offcanvas-menu.active {
    transform: translateX(0);
}
```

---

### 10. JAVASCRIPT INTEGRATION

**For Elementor:**
1. Add script.js to theme's functions.php or use "Insert Headers and Footers" plugin
2. Alternatively, use Elementor's Custom Code feature (Elementor Pro)

**Key Functions:**
- Sticky header on scroll
- Mobile menu toggle
- Off-canvas submenu expansion
- Focus trap for accessibility
- Escape key to close menu

**Elementor Alternative:**
Most functionality can be achieved with Elementor Pro's built-in features:
- Sticky headers (Motion Effects)
- Popups for mobile menu
- Dynamic visibility conditions

---

### 11. ACCESSIBILITY FEATURES

**Built-in:**
- ARIA labels on buttons
- Keyboard navigation support
- Focus states with accent color outline
- Screen reader friendly structure
- Escape key closes menus

**Elementor Enhancement:**
- Add proper heading hierarchy
- Ensure color contrast meets WCAG AA
- Test with keyboard only navigation

---

### 12. PERFORMANCE OPTIMIZATION

**Recommendations:**
1. Convert SVG icons to inline or use Elementor's icon library
2. Minify CSS for production
3. Lazy load off-canvas menu content
4. Use Elementor's asset optimization features
5. Enable caching for header template

**Load Order:**
1. Critical CSS inline (header styles)
2. Defer non-critical JS
3. Preload key assets

---

### 13. TESTING CHECKLIST

Before deployment:

- [ ] Sticky header triggers at correct scroll position
- [ ] Mega menu displays correctly on hover
- [ ] Mobile menu opens/closes smoothly
- [ ] All links are clickable and accessible
- [ ] Request quote button stands out visually
- [ ] Top bar information is readable
- [ ] Responsive breakpoints work correctly
- [ ] Browser compatibility (Chrome, Safari, Firefox, Edge)
- [ ] Performance score >90 on PageSpeed Insights

---

### 14. COMMON ISSUES & SOLUTIONS

**Issue**: Mega menu gets cut off
**Solution**: Ensure parent containers have `overflow: visible`

**Issue**: Sticky header flickers
**Solution**: Use `will-change: transform` on header element

**Issue**: Mobile menu doesn't close on route change
**Solution**: Add event listener for page navigation

**Issue**: Glassmorphism not working in Safari
**Solution**: Include `-webkit-backdrop-filter` prefix

---

### 15. EXPORT FOR ELEMENTOR

**To export as Elementor template:**
1. Rebuild header in Elementor Theme Builder
2. Save as "Header" template type
3. Set display conditions: Entire Site
4. Export via Elementor → Tools → Import/Export

**Template JSON will include:**
- Section structures
- Widget configurations
- Style settings
- Responsive breakpoints

---

## Support & Maintenance

For updates or modifications:
1. Keep CSS variables in sync with Elementor Global Colors
2. Test all interactions after Elementor updates
3. Maintain vanilla JS (no jQuery dependencies)
4. Document any custom code additions

---

**Version**: 1.0  
**Last Updated**: 2024  
**Compatibility**: Elementor Pro 3.15+, WordPress 6.0+
