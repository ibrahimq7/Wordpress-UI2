# Elementor Integration Notes - Enterprise Header

## Overview
This enterprise header component is designed for seamless conversion into WordPress Elementor Pro. The code follows modular, container-based architecture that maps directly to Elementor's Flexbox Containers and Grid system.

---

## File Structure
```
header.html     → HTML structure for reference
header.css      → Complete styling (import into Elementor Custom CSS)
script.js       → JavaScript functionality (add to Elementor Custom Code)
```

---

## Elementor Container Mapping

### 1. Main Header Wrapper
**Elementor Type:** Flexbox Container  
**Direction:** Column  
**ID:** `enterprise-header`  
**CSS Classes:** `enterprise-header`

**Settings:**
- Content Width: Full Width
- Min Height: Default
- Overflow: Visible
- Z-Index: 1000

---

### 2. Top Bar Section
**Elementor Type:** Flexbox Container  
**Direction:** Row  
**CSS Classes:** `top-bar`, `container`

**Settings:**
- Justify Content: Space Between
- Align Items: Center
- Min Height: 38px
- Background: Gradient (#0A2540 → #1E3A5F)

**Child Containers:**
- **Left Container** (`top-bar-left`): Email + Phone
- **Right Container** (`top-bar-right`): GCC Countries + Office Hours

---

### 3. Main Header Section
**Elementor Type:** Flexbox Container  
**Direction:** Row  
**CSS Classes:** `main-header`, `container`

**Settings:**
- Justify Content: Space Between
- Align Items: Center
- Min Height: 92px
- Background: White (#FFFFFF)
- Border Bottom: 1px solid #E2E8F0

**Child Containers:**
- **Logo Container** (`logo-wrapper`): Left side
- **Navigation Container** (`main-nav`): Center (Desktop only)
- **Actions Container** (`header-actions`): Right side

---

### 4. Logo Widget
**Elementor Type:** Image or Site Logo  
**CSS Classes:** `logo-link`, `logo-placeholder`

**Alternative:** Use Text Editor widget with custom HTML:
```html
<span class="logo-text">MEP<span class="logo-accent">PROCURE</span></span>
```

---

### 5. Navigation Menu
**Elementor Type:** Nav Menu Widget  
**CSS Classes:** `nav-list`

**Settings:**
- Layout: Horizontal
- Pointer: None (custom styling applied)
- Dropdown: Classic

**Menu Items:**
1. Products (with Mega Menu)
2. Brands
3. RFQ Center
4. About
5. Contact

---

### 6. Mega Menu Implementation

**Option A: Elementor Pro Nav Menu**
- Use Elementor's built-in mega menu feature
- Create a 4-column grid in the dropdown
- Add promotional card in rightmost column

**Option B: Custom HTML Widget**
Paste the mega-menu HTML structure inside the Products menu item using custom code.

**Mega Menu Grid Settings:**
- Columns: 4
- Gap: 32px
- Width: 900px
- Padding: 32px
- Border Radius: 12px
- Box Shadow: 0 16px 48px rgba(0,0,0,0.15)

**Column Structure:**
```
Column 1: Plumbing, HVAC, Fire Fighting
Column 2: Electrical, Gas Systems, Pumps
Column 3: Water Treatment, Tools, Featured Brands
Column 4: Promotional Card (Gradient background)
```

---

### 7. Search Trigger
**Elementor Type:** Icon Widget  
**CSS Classes:** `search-trigger`

**Settings:**
- Icon: Search (magnifying glass)
- Size: 20px
- Color: #4A5568
- Hover Color: #0A2540

**Alternative:** Use Button widget with icon only, styled as circle.

---

### 8. Request Quote Button
**Elementor Type:** Button Widget  
**CSS Classes:** `btn`, `btn-primary`, `request-quote-btn`

**Settings:**
- Text: "Request Quote"
- Link: Your quote page URL
- Background: Gradient (#C9A227 → #D4AF37)
- Text Color: #0A2540
- Border Radius: 8px
- Padding: 8px 32px
- Typography: 14px, Weight 600

**Hover Effect:**
- Transform: Translate Y -2px
- Shadow: Medium elevation

---

### 9. Mobile Menu Toggle
**Elementor Type:** Not needed (handled by Elementor's responsive Nav Menu)

**Alternative:** If using custom implementation:
- Use Icon widget with hamburger icon
- CSS Classes: `mobile-menu-toggle`
- Visibility: Mobile Only

---

### 10. Off-Canvas Mobile Menu
**Elementor Type:** Popup Template

**Create a new Popup:**
1. Templates → Popups → Add New
2. Design mobile menu layout
3. Set trigger to hamburger button
4. Animation: Slide In From Right
5. Overlay: Enable with dark background

**Popup Settings:**
- Width: 100% (max 400px)
- Height: 100vh
- Position: Fixed, Right: 0
- Z-Index: 1002

**Inside Popup:**
- Header: Logo + Close button
- Nav Menu Widget (Vertical layout)
- Contact Info section
- CTA Button (Request Quote)

---

## CSS Integration Methods

### Method 1: Global Custom CSS (Recommended)
**Location:** Elementor → Site Settings → Custom Code → Custom CSS

Copy entire `header.css` content here for global application.

### Method 2: Page-Specific CSS
**Location:** Page Settings → Advanced → Custom CSS

Paste CSS for individual page customization.

### Method 3: HTML Widget
Add `<style>` tags inside an HTML widget at the top of your header template.

---

## JavaScript Integration

### Location: Elementor → Site Settings → Custom Code → Body Scripts

**Steps:**
1. Go to Elementor Dashboard
2. Site Settings → Custom Code
3. Add New Script
4. Paste `script.js` content
5. Set location: Body End
6. Set display: Entire Site

**Alternative:** Use a plugin like "Header Footer Code Manager"

---

## Responsive Breakpoints

### Desktop (>1024px)
- Full navigation visible
- Mega menu enabled
- Search trigger visible
- Request Quote button visible

### Tablet (768px - 1024px)
- Serving text hidden
- Mega menu: 2 columns
- Reduced padding

### Mobile (<768px)
- Top bar hidden
- Desktop nav hidden
- Hamburger menu visible
- Off-canvas menu active
- Search & CTA moved to mobile menu

---

## Sticky Header Setup

### Elementor Motion Effects
**Container Settings:**
- Select Main Header Container
- Motion Effects → Sticky → Top
- Effects Offset: 0
- Sticky On: Desktop, Tablet, Mobile

### CSS Class Method
Add class `sticky` via Elementor's Advanced → CSS Classes when scroll threshold is reached (handled by script.js).

---

## Typography Settings

**Font Family:** Inter (or similar sans-serif)  
**Load via:** Elementor → Site Settings → Global Fonts

**Sizes:**
- Top Bar: 12px
- Nav Links: 14px
- Logo: 24px
- Mobile Nav: 20px

**Weights:**
- Regular: 400
- Medium: 500
- Semi-Bold: 600
- Bold: 700

---

## Color Palette (Global Colors)

Set these in Elementor Site Settings → Global Colors:

1. **Primary:** #0A2540
2. **Secondary:** #1E3A5F
3. **Accent:** #C9A227
4. **Text Dark:** #1A1A1A
5. **Text Medium:** #4A5568
6. **Text Light:** #718096
7. **Background Light:** #F7F9FC
8. **Border:** #E2E8F0

---

## Performance Optimization

### 1. Asset Loading
- Load CSS in `<head>`
- Load JS before `</body>`
- Enable Elementor's Asset Unification

### 2. Caching
- Enable Elementor's Minify CSS/JS
- Use caching plugin (WP Rocket, W3 Total Cache)

### 3. Images
- Optimize logo SVG/PNG
- Use WebP format where possible

---

## Accessibility Checklist

✅ Semantic HTML structure  
✅ ARIA labels on buttons  
✅ Keyboard navigation support  
✅ Focus states defined  
✅ Color contrast WCAG AA compliant  
✅ Screen reader friendly  

---

## Testing Checklist

### Desktop
- [ ] Sticky header activates on scroll
- [ ] Mega menu opens on hover
- [ ] All links functional
- [ ] Search trigger clickable
- [ ] Request Quote button works

### Tablet
- [ ] Layout adapts properly
- [ ] Mega menu displays correctly
- [ ] Touch interactions work

### Mobile
- [ ] Hamburger menu toggles
- [ ] Off-canvas slides in/out
- [ ] Submenus accordion properly
- [ ] Close button functional
- [ ] Overlay closes menu

---

## Common Issues & Solutions

### Issue: Mega Menu Not Showing
**Solution:** Check z-index hierarchy. Ensure mega-menu z-index (1001) is higher than header (1000).

### Issue: Sticky Header Jitter
**Solution:** Add `will-change: transform;` to header CSS.

### Issue: Mobile Menu Overlap
**Solution:** Verify body overflow is set to hidden when menu is open.

### Issue: Font Not Loading
**Solution:** Import 'Inter' font in Elementor Site Settings → Custom Fonts or use Google Fonts integration.

---

## Export/Import Template

### Save as Elementor Template:
1. Right-click on header container
2. Save as Template
3. Name: "Enterprise Header"
4. Access via: Templates → Saved Templates

### Import to Another Site:
1. Export template as JSON
2. Import via Elementor Template Library
3. Reapply global colors if needed

---

## Support & Maintenance

**Version:** 1.0  
**Last Updated:** Current  
**Compatibility:** Elementor Pro 3.15+  
**WordPress:** 6.0+  

For updates or modifications, maintain the CSS variable structure to ensure easy theming and consistency across the platform.

---

## Quick Start Guide

1. **Create Header Template:**
   - Templates → Theme Builder → Header → Add New
   
2. **Build Structure:**
   - Add containers as mapped above
   - Apply CSS classes
   
3. **Add Custom CSS:**
   - Copy header.css to Site Settings
   
4. **Add JavaScript:**
   - Copy script.js to Site Settings → Custom Code
   
5. **Set Display Conditions:**
   - Include: Entire Site
   
6. **Publish & Test:**
   - Preview on all devices
   - Verify all interactions

---

**End of Integration Notes**
