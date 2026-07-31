# ELEMENTOR INTEGRATION NOTES

## Enterprise MEP Procurement Header Component

---

## 📋 OVERVIEW

This header component is designed for seamless conversion into Elementor Pro using Containers (Flexbox/Grid). The structure follows Elementor's container-based architecture for easy implementation.

---

## 🏗️ STRUCTURE BREAKDOWN FOR ELEMENTOR

### Main Container Hierarchy

```
Header Section (Fixed Position)
├── Top Bar Container (Height: 40px)
│   └── Inner Container (Max-width: 1400px)
│       ├── Left Content (Flex Row)
│       │   ├── Email Link
│       │   └── Phone Link
│       └── Right Content (Flex Row)
│           ├── Serving Label
│           ├── Country List
│           └── Office Hours
│
└── Main Navigation Container (Height: 90px → 80px on scroll)
    └── Inner Container (Max-width: 1400px)
        ├── Logo Container (Flex Row)
        │   ├── Logo Mark (SVG/Image)
        │   └── Logo Text (2 Lines)
        │
        ├── Primary Navigation Container
        │   └── Nav Menu Items
        │       └── Mega Menu (Absolute Positioned Container)
        │           └── Grid Container (4 Columns)
        │               ├── Column 1: Systems
        │               ├── Column 2: Equipment
        │               ├── Column 3: Specialized
        │               └── Column 4: Promo Card
        │
        └── Actions Container (Flex Row)
            ├── Search Button
            ├── Request Quote CTA
            └── Mobile Toggle (Hidden Desktop)
```

---

## 🎨 CSS VARIABLES MAPPING

Copy these into Elementor → Site Settings → Global Colors/Typography:

### Colors
```
Primary Teal 900: #0f766e
Primary Teal 800: #118880
Primary Teal 700: #139990
Primary Teal 600: #0d9488
Primary Teal 500: #14b8a6

Slate 900: #0f172a
Slate 800: #1e293b
Slate 700: #334155
Slate 600: #475569
Slate 500: #64748b
Slate 400: #94a3b8
Slate 300: #cbd5e1
Slate 200: #e2e8f0
Slate 100: #f1f5f9
Slate 50: #f8fafc
```

### Typography
```
Font Family: Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto
Font Sizes:
  - XS: 12px (0.75rem)
  - SM: 14px (0.875rem)
  - Base: 16px (1rem)
  - LG: 18px (1.125rem)
  - XL: 20px (1.25rem)
```

### Spacing System
```
Spacing 1: 4px
Spacing 2: 8px
Spacing 3: 12px
Spacing 4: 16px
Spacing 5: 20px
Spacing 6: 24px
Spacing 8: 32px
Spacing 10: 40px
Spacing 12: 48px
```

### Border Radius
```
SM: 6px
MD: 8px
LG: 12px
XL: 16px
2XL: 20px
```

### Shadows
```
SM: 0 1px 2px 0 rgba(0,0,0,0.05)
MD: 0 4px 6px -1px rgba(0,0,0,0.1)
LG: 0 10px 15px -3px rgba(0,0,0,0.1)
XL: 0 20px 25px -5px rgba(0,0,0,0.1)
2XL: 0 25px 50px -12px rgba(0,0,0,0.25)
```

---

## 🔧 ELEMENTOR IMPLEMENTATION STEPS

### Step 1: Create Header Template
1. Go to Templates → Theme Builder → Header
2. Add New Header
3. Set Display Conditions: Entire Site
4. Disable default Elementor header

### Step 2: Build Top Bar
1. Add Container (Flexbox)
   - Height: 40px (Fixed)
   - Background: #0f172a
   - Content Width: 1400px
   - Justify Content: Space Between
   
2. Add Left Container
   - Direction: Row
   - Gap: 24px
   - Add Icon + Text widgets for email/phone

3. Add Right Container
   - Direction: Row
   - Gap: 16px
   - Add Text widgets for countries

### Step 3: Build Main Navigation
1. Add Container (Flexbox)
   - Height: 90px (Desktop), 70px (Mobile)
   - Background: Transparent
   - Content Width: 1400px
   
2. Logo Implementation
   - Use Image widget or SVG
   - Size: 40x40px (Desktop), 36x36px (Mobile)
   
3. Navigation Menu
   - Use Elementor Nav Menu widget
   - Or build custom with Icon Box widgets
   
4. Mega Menu Setup
   - Create Inner Section with 4 columns
   - Position: Absolute
   - Use Motion Effects for hover reveal

### Step 4: CTA Button
1. Add Button Widget
2. Style:
   - Background Type: Gradient
   - Color 1: #139990
   - Color 2: #0d9488
   - Border Radius: 12px
   - Box Shadow: 0 4px 14px 0 rgba(13,148,136,0.4)
   - Hover Animation: Float

### Step 5: Mobile Menu
1. Use Elementor's built-in Mobile Menu toggle
2. Create Off-Canvas template
3. Style with same color system
4. Add Slide-in animation

---

## 🎭 SCROLL EFFECT SETUP

### Method 1: Elementor Motion Effects
1. Select Header Section
2. Advanced → Motion Effects
3. Scrolling Effects:
   - Background Blur: On scroll
   - Transparency: 100% → 85%
   - Shadow: Add on scroll

### Method 2: Custom Code (Recommended)
Add the provided `header.js` to:
- Elementor → Custom Code → Head
- Or use a Code widget in the header

The JS automatically handles:
- Scroll detection
- Class toggling (.scrolled)
- Mobile menu interactions
- Keyboard navigation

---

## 📱 RESPONSIVE BREAKPOINTS

### Desktop (>1200px)
- Full navigation visible
- Mega menu: 4-column grid
- Top bar visible
- Logo: 40x40px + tagline

### Tablet (768px - 1200px)
- Hide desktop navigation
- Show hamburger menu
- Hide top bar on scroll
- Logo: 36x36px

### Mobile (<768px)
- Off-canvas menu
- Hide top bar completely
- CTA becomes icon-only
- Header height: 70px

---

## ⚡ PERFORMANCE OPTIMIZATIONS

### For Elementor:
1. **Minimize Widgets**: Use HTML widgets where possible
2. **Lazy Load**: Defer non-critical assets
3. **SVG Icons**: Inline SVGs instead of icon fonts
4. **CSS**: Copy provided CSS to theme customizer
5. **JavaScript**: Add via Code snippet plugin

### Recommended Plugins:
- Perfmatters (for asset optimization)
- WP Rocket (caching)
- Asset CleanUp (remove unused CSS/JS)

---

## 🎯 MEGA MENU IMPLEMENTATION OPTIONS

### Option A: Elementor Pro Nav Menu
1. Use Nav Menu widget
2. Enable Mega Menu in settings
3. Design mega menu content in popup
4. Trigger on hover

### Option B: Custom Container (Recommended)
1. Build mega menu as nested containers
2. Position: Absolute
3. Use Custom CSS for hover states
4. More control over design

### Option C: Third-Party Plugin
- JetMenu by Crocoblock
- Premium Addons for Elementor
- AnyWhere Elementor

---

## 🔍 SEARCH FUNCTIONALITY

Current implementation shows search icon only.

### To Add Expandable Search:
1. Create Popup template
2. Add Search Form widget
3. Style with glassmorphism
4. Trigger from search button
5. Add overlay backdrop

---

## ♿ ACCESSIBILITY CHECKLIST

- ✅ Focus states defined
- ✅ Keyboard navigation supported
- ✅ ARIA labels on buttons
- ✅ Screen reader friendly
- ✅ Reduced motion support
- ✅ High contrast mode ready

### WCAG Compliance:
- Color contrast ratios meet AA standards
- All interactive elements are keyboard accessible
- Focus indicators are visible
- Semantic HTML structure

---

## 🎨 CUSTOMIZATION GUIDE

### Change Brand Color:
Replace all instances of:
```
--color-primary-600: #0d9488
```
With your brand color.

### Adjust Header Height:
Modify in CSS:
```css
.main-nav { height: 90px; } /* Desktop */
```

### Modify Mega Menu Columns:
Change grid-template-columns:
```css
grid-template-columns: repeat(3, 1fr) 320px;
/* To */
grid-template-columns: repeat(4, 1fr);
```

---

## 🐛 TROUBLESHOOTING

### Issue: Mega menu not showing
**Solution:** Check z-index hierarchy. Parent should have `position: static`.

### Issue: Scroll effect not working
**Solution:** Ensure JS file is loaded after DOM. Check console for errors.

### Issue: Mobile menu not closing
**Solution:** Verify event listeners are attached. Check for JS conflicts.

### Issue: Backdrop blur not working
**Solution:** Add vendor prefixes. Some browsers need `-webkit-backdrop-filter`.

---

## 📦 ASSETS NEEDED

1. **Logo Files**
   - SVG format (preferred)
   - PNG @2x fallback
   - Favicon version

2. **Icons**
   - Already included as inline SVG
   - Can replace with Elementor icons if preferred

3. **Illustrations**
   - Promo card visual (currently SVG placeholder)
   - Replace with custom illustration if needed

---

## 🚀 LAUNCH CHECKLIST

- [ ] Test on Chrome, Firefox, Safari, Edge
- [ ] Test on iOS Safari, Android Chrome
- [ ] Verify scroll effects work smoothly
- [ ] Check mobile menu interactions
- [ ] Test keyboard navigation
- [ ] Validate all links work
- [ ] Optimize images/SVGs
- [ ] Minify CSS/JS for production
- [ ] Set up proper caching headers
- [ ] Test with different screen sizes
- [ ] Verify accessibility with screen reader

---

## 📞 SUPPORT

For Elementor-specific questions:
- Elementor Documentation: https://elementor.com/help/
- Elementor Community: https://forum.elementor.com/

For custom development:
- Review provided CSS variables
- Check browser console for errors
- Test in incognito mode to rule out cache issues

---

**Component Version:** 1.0  
**Last Updated:** 2024  
**Compatibility:** Elementor Pro 3.0+  
**Browser Support:** Modern browsers (Chrome 80+, Firefox 75+, Safari 13+)
