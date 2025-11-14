# iOS Design System - ClassyCouture

**Last Updated**: November 9, 2025
**Status**: ✅ Implemented
**Design Language**: Apple iOS 18 / iPadOS

---

## Overview

ClassyCouture now features a complete iOS-inspired design system that brings the polish, fluidity, and attention to detail of Apple's interface guidelines to your e-commerce platform. This document outlines all the design tokens, components, and patterns implemented.

---

## 🎨 Design Tokens

### Typography

**Font Stack**:
```css
-apple-system, BlinkMacSystemFont, 'SF Pro Display', 'SF Pro Text',
'Helvetica Neue', system-ui, Arial, sans-serif
```

**Features**:
- SF Pro font family with Apple system font fallbacks
- Antialiased rendering for crisp text
- Optimized line-height and letter-spacing
- Responsive typography scale

**Font Rendering**:
- `-webkit-font-smoothing: antialiased`
- `-moz-osx-font-smoothing: grayscale`
- `text-rendering: optimizeLegibility`

---

### Color System

#### iOS System Colors

```javascript
{
  blue: '#007AFF',      // Primary actions, links
  indigo: '#5856D6',    // Secondary actions
  purple: '#AF52DE',    // Accents
  pink: '#FF2D55',      // Highlights
  red: '#FF3B30',       // Destructive, errors
  orange: '#FF9500',    // Warnings
  yellow: '#FFCC00',    // Alerts
  green: '#34C759',     // Success
  teal: '#5AC8FA',      // Info
  mint: '#00C7BE',      // Fresh accents
  cyan: '#32ADE6',      // Links alternative

  // Grays (for UI elements)
  gray: '#8E8E93',      // Text secondary
  gray2: '#AEAEB2',     // Borders, dividers
  gray3: '#C7C7CC',     // Backgrounds
  gray4: '#D1D1D6',     // Input backgrounds
  gray5: '#E5E5EA',     // Subtle backgrounds
  gray6: '#F2F2F7',     // Page backgrounds
}
```

#### Semantic Colors

- **Primary**: iOS Blue (#007AFF) - Main CTAs, links
- **Destructive**: iOS Red (#FF3B30) - Delete, errors
- **Background**: White (#FFFFFF) / Dark (#0A0A0A)
- **Foreground**: Near Black (#0A0A0A) / Off White (#F5F5F5)

---

### Border Radius

iOS uses generous, consistent corner radius:

```javascript
{
  'ios-sm': '8px',    // Small elements, badges
  'ios-md': '10px',   // Buttons, inputs
  'ios-lg': '12px',   // Cards, modals (default)
  'ios-xl': '14px',   // Large cards
  'ios-2xl': '16px',  // Hero elements
  'ios-3xl': '20px',  // Special components
}
```

**Usage**: iOS favors 10-14px for most UI elements.

---

### Shadows (Elevation System)

Layered, subtle shadows that create depth without being heavy:

```css
/* iOS Shadow System */
shadow-ios-sm:  /* Subtle lift */
  0 1px 2px 0 rgba(0, 0, 0, 0.05),
  0 1px 3px 0 rgba(0, 0, 0, 0.1)

shadow-ios-md:  /* Standard elevation */
  0 2px 8px 0 rgba(0, 0, 0, 0.08),
  0 4px 12px 0 rgba(0, 0, 0, 0.08)

shadow-ios-lg:  /* Prominent elements */
  0 4px 16px 0 rgba(0, 0, 0, 0.1),
  0 8px 24px 0 rgba(0, 0, 0, 0.1)

shadow-ios-xl:  /* Modals, overlays */
  0 8px 32px 0 rgba(0, 0, 0, 0.12),
  0 12px 48px 0 rgba(0, 0, 0, 0.12)

shadow-ios-inner:  /* Inset shadows */
  inset 0 1px 2px 0 rgba(0, 0, 0, 0.05)
```

---

### Backdrop Blur (Glassmorphism)

Apple's signature frosted glass effect:

```javascript
{
  'ios-sm': '10px',   // Subtle blur
  'ios': '20px',      // Standard (default)
  'ios-lg': '40px',   // Strong blur
}
```

**Pre-built Glass Classes**:
- `.glass` - Standard frosted glass (70% white, 20px blur)
- `.glass-dark` - Dark mode glass (30% black)
- `.glass-strong` - Strong glass effect (90% white, 40px blur)

---

### Animation & Transitions

#### Timing Functions

iOS uses physics-based animations:

```javascript
{
  'ios': 'cubic-bezier(0.4, 0.0, 0.2, 1)',        // Standard
  'ios-bounce': 'cubic-bezier(0.34, 1.56, 0.64, 1)', // Spring
  'ios-spring': 'cubic-bezier(0.5, 1.75, 0.75, 1)',  // Bouncy
  'ios-smooth': 'cubic-bezier(0.25, 0.1, 0.25, 1)',  // Smooth
}
```

#### Durations

iOS animations are slightly slower than web defaults for a premium feel:

```javascript
{
  'ios-fast': '200ms',   // Quick feedback
  'ios': '300ms',        // Standard (default)
  'ios-slow': '400ms',   // Emphasized
}
```

#### Pre-built Animations

```javascript
{
  'spring-in': 'springIn 0.4s cubic-bezier(0.34, 1.56, 0.64, 1)',
  'spring-out': 'springOut 0.3s cubic-bezier(0.5, 0, 0.75, 0)',
  'fade-in': 'fadeIn 0.3s ease-ios',
  'fade-out': 'fadeOut 0.2s ease-out',
  'slide-up': 'slideUp 0.4s ease-ios-bounce',
  'slide-down': 'slideDown 0.3s ease-ios',
  'scale-in': 'scaleIn 0.3s ease-ios-bounce',
  'ios-pulse': 'iosPulse 2s ease-ios infinite',
}
```

**Usage Examples**:
```html
<div class="animate-spring-in">Bounces in</div>
<div class="animate-fade-in">Fades in</div>
<div class="animate-slide-up">Slides up with bounce</div>
```

---

### Spacing

iOS uses an 8pt grid system (Tailwind's default):

```javascript
{
  1: '4px',
  2: '8px',    // Base unit
  3: '12px',
  4: '16px',   // Common spacing
  6: '24px',
  8: '32px',
  12: '48px',
  16: '64px',
}
```

**Safe Area Insets** (for iOS devices):
```javascript
{
  'ios-safe': 'env(safe-area-inset-top)',
  'ios-safe-bottom': 'env(safe-area-inset-bottom)',
  'ios-safe-left': 'env(safe-area-inset-left)',
  'ios-safe-right': 'env(safe-area-inset-right)',
}
```

---

### Touch Targets

Following Apple's Human Interface Guidelines:

```javascript
{
  'touch': '44px',     // Minimum tap target (default)
  'touch-sm': '36px',  // Small elements
  'touch-lg': '52px',  // Large, prominent CTAs
}
```

**Applied to**: All buttons, input fields, and interactive elements.

---

## 🧩 Components

### Button

**Updated Features**:
- ✅ iOS-style border radius (`rounded-ios-md`)
- ✅ Layered shadows (`shadow-ios-md`)
- ✅ Spring animations on hover/active (`ease-ios-bounce`)
- ✅ Active scale feedback (`active:scale-95`)
- ✅ Touch-optimized sizing (`min-h-touch`)
- ✅ Haptic feedback simulation

**New Variants**:
```tsx
<Button variant="default">Primary Action</Button>
<Button variant="destructive">Delete</Button>
<Button variant="outline">Secondary</Button>
<Button variant="glass">Glassmorphism</Button>
<Button variant="ghost">Minimal</Button>
```

**Sizes**:
```tsx
<Button size="sm">Small (36px)</Button>
<Button size="default">Default (44px)</Button>
<Button size="lg">Large (52px)</Button>
<Button size="icon">Icon Only</Button>
```

---

### Card

**Updated Features**:
- ✅ iOS border radius (`rounded-ios-lg`)
- ✅ Elevation shadows (`shadow-ios-md`)
- ✅ Smooth hover transitions
- ✅ Optional glassmorphism

**Usage**:
```tsx
<Card>Standard card with iOS styling</Card>
<Card glass>Glassmorphic card with blur</Card>
```

**Hover State**: Automatically scales to `scale-[1.02]` and elevates shadow.

---

### Input

**Updated Features**:
- ✅ iOS-style background (`bg-ios-gray6`)
- ✅ Minimum touch height (`min-h-touch`)
- ✅ Smooth focus transitions with ring
- ✅ Background changes on focus (gray → white)
- ✅ Proper iOS padding

**Focus Behavior**:
1. Border changes to primary color
2. Background changes from gray to white
3. Subtle shadow appears
4. Ring indicator (2px, 20% opacity)

---

### Navbar

**iOS Improvements**:
- ✅ Glassmorphism background (`.glass-strong`)
- ✅ Gradient logo text
- ✅ iOS Blue shopping bag button
- ✅ Animated badge indicators
- ✅ Spring animations on all interactions
- ✅ Touch-optimized tap targets
- ✅ Safe area padding support

**Features**:
- Frosted glass navbar that blurs content behind it
- iOS system color badges (red for wishlist, blue badge on cart)
- Spring-in animations for dynamic counts
- Active scale feedback on all buttons

---

### Badge

**Pre-built Class**:
```html
<span class="ios-badge">5</span>
```

**Features**:
- Minimum 20px diameter
- iOS Red background
- White text
- Subtle shadow
- Pill shape (fully rounded)

---

### iOS-Specific Components

#### Segmented Control
```html
<div class="ios-segmented">
  <button class="ios-segmented-item ios-segmented-item-active">Tab 1</button>
  <button class="ios-segmented-item">Tab 2</button>
  <button class="ios-segmented-item">Tab 3</button>
</div>
```

#### List
```html
<div class="ios-list">
  <div class="ios-list-item">Item 1</div>
  <div class="ios-list-item">Item 2</div>
  <div class="ios-list-item">Item 3</div>
</div>
```

#### Card Variants
```html
<div class="ios-card">Standard iOS card</div>
<div class="ios-card-glass">Glassmorphic card</div>
```

---

## 🛠 Utility Classes

### Glassmorphism

```html
<div class="glass">Standard frosted glass</div>
<div class="glass-dark">Dark mode glass</div>
<div class="glass-strong">Strong blur effect</div>
```

### Elevation

```html
<div class="elevation-0">No shadow</div>
<div class="elevation-1">Subtle lift (shadow-ios-sm)</div>
<div class="elevation-2">Standard (shadow-ios-md)</div>
<div class="elevation-3">Prominent (shadow-ios-lg)</div>
<div class="elevation-4">Maximum (shadow-ios-xl)</div>
```

### Touch Optimization

```html
<button class="touch-manipulation">
  Optimized for touch with no highlight
</button>

<button class="haptic">
  Simulates haptic feedback (scales on tap)
</button>

<button class="tap-highlight">
  Shows iOS blue highlight on tap
</button>
```

### Scrollbar

```html
<div class="scrollbar-hide">Hidden scrollbar</div>
<div class="scrollbar-ios">iOS-style thin scrollbar</div>
```

### Safe Areas

```html
<header class="safe-top">Respects notch</header>
<footer class="safe-bottom">Respects home indicator</footer>
<nav class="safe-left safe-right">Respects curved edges</nav>
```

### Animations

```html
<div class="spring">Uses spring timing function</div>
<div class="transition-all duration-ios ease-ios">
  iOS-standard transition
</div>
```

---

## 📱 Responsive Design

### Breakpoints

Using Tailwind's defaults:
- `sm`: 640px (Mobile landscape)
- `md`: 768px (Tablet)
- `lg`: 1024px (Desktop)
- `xl`: 1280px (Large desktop)
- `2xl`: 1536px (Extra large)

### Mobile-First Approach

All components are optimized for mobile:
- Touch targets minimum 44px
- Generous spacing on mobile
- Simplified layouts on small screens
- Full navigation hidden behind menu on mobile

---

## 🎭 Dark Mode Support

All components support dark mode via the `.dark` class:

```css
.dark {
  --background: 0 0% 3.9%;
  --foreground: 0 0% 98%;
  --primary: 221 83% 53%;  /* iOS Blue works in both modes */
  /* ... */
}
```

**Dark Mode Glass**:
```html
<div class="glass-dark">Dark glassmorphism</div>
```

---

## ♿ Accessibility

### Features Implemented

1. **Keyboard Navigation**:
   - All interactive elements focusable
   - Visible focus rings (iOS Blue, 2px)
   - Logical tab order

2. **Touch Targets**:
   - Minimum 44px height/width
   - Generous spacing between elements
   - Clear active states

3. **Motion**:
   - Respects `prefers-reduced-motion`
   - Animations disabled for users who prefer it

4. **Color Contrast**:
   - All text meets WCAG AA standards
   - iOS system colors are accessible

5. **Screen Readers**:
   - Semantic HTML
   - ARIA labels where needed

---

## 🚀 Performance

### Optimizations

1. **Hardware Acceleration**:
   - Transform and opacity used for animations
   - GPU-accelerated blur effects

2. **Reduced Repaints**:
   - Will-change hints on animated elements
   - Composite layers for smooth animations

3. **Minimal Bundle Impact**:
   - CSS-only utilities (no JavaScript overhead)
   - Tree-shakeable Tailwind classes

---

## 📋 Migration Guide

### From Previous Design

**Before**:
```tsx
<button className="rounded-md shadow hover:shadow-lg transition">
  Click me
</button>
```

**After**:
```tsx
<Button variant="default" size="default">
  Click me
</Button>
```

### Custom Components

To apply iOS styling to custom components:

```tsx
<div className="rounded-ios-lg bg-white shadow-ios-md transition-all duration-ios ease-ios hover:shadow-ios-lg active:scale-95 touch-manipulation">
  Custom component with iOS styling
</div>
```

---

## 🎨 Design Principles

### 1. **Clarity**
- Clean, focused interfaces
- Generous whitespace
- Clear visual hierarchy

### 2. **Deference**
- Content takes center stage
- Subtle, refined UI elements
- Translucent materials

### 3. **Depth**
- Layered shadows and blur
- Visual and tactile feedback
- Realistic motion

### 4. **Polish**
- Smooth, spring-based animations
- Pixel-perfect alignment
- Consistent spacing

---

## 🔄 What's Next

### Future Enhancements

1. **Advanced Animations**:
   - Page transitions
   - List reordering with physics
   - Pull-to-refresh

2. **More Components**:
   - iOS-style date picker
   - Action sheets
   - Toggle switches
   - Progress indicators

3. **Gestures**:
   - Swipe actions
   - Long press menus
   - Pinch to zoom

4. **Micro-interactions**:
   - Button ripples
   - Loading skeletons
   - Success animations

---

## 📚 Resources

### Official Documentation
- [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/)
- [iOS Design Resources](https://developer.apple.com/design/resources/)
- [SF Pro Font](https://developer.apple.com/fonts/)

### Tailwind CSS
- [Tailwind Documentation](https://tailwindcss.com/docs)
- [Customizing Your Theme](https://tailwindcss.com/docs/theme)

---

## 🛠 Developer Tools

### Testing iOS Styling

1. **Browser DevTools**:
   - Use responsive mode
   - Test on iOS viewport sizes (375px, 390px, 428px)

2. **Real Devices**:
   - Test on iPhone/iPad for authentic feel
   - Check safe area insets

3. **Animations**:
   - Reduce motion settings
   - Different refresh rates

### Debugging

```css
/* Visualize touch targets */
.touch-debug * {
  outline: 1px solid rgba(255, 0, 0, 0.2);
}

/* Visualize safe areas */
.safe-debug {
  background: rgba(0, 122, 255, 0.1);
}
```

---

## 📊 Comparison: Before vs After

| Aspect | Before | After |
|--------|--------|-------|
| **Border Radius** | 8px (sharp) | 10-14px (iOS standard) |
| **Shadows** | Single layer, harsh | Layered, subtle |
| **Animations** | 150ms linear | 300ms spring curves |
| **Touch Targets** | Inconsistent | Minimum 44px |
| **Colors** | Generic | iOS system colors |
| **Blur Effects** | Limited | Full glassmorphism |
| **Font** | System default | SF Pro / Apple system |
| **Accessibility** | Basic | WCAG AA compliant |

---

## ✅ Implementation Checklist

- [x] Tailwind config updated with iOS tokens
- [x] Global CSS with glassmorphism utilities
- [x] Button component iOS styling
- [x] Card component with glass variant
- [x] Input component iOS behavior
- [x] Navbar glassmorphism and refinements
- [x] iOS color system
- [x] Spring animations
- [x] Touch target compliance
- [x] Safe area support
- [x] Dark mode support
- [x] Accessibility improvements
- [x] Documentation

---

**Designed with ❤️ following Apple's Human Interface Guidelines**
**Built with Next.js 16, React 19, and Tailwind CSS**

Last updated: November 9, 2025
