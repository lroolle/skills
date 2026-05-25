# Adaptation

Intent preservation across constraints. The user's goal does not change
when the screen shrinks. The design's job does not change. What changes:
space, input method, environment.

## Content priority tiers

Classify before choosing breakpoints:

| Tier | Behavior | Examples |
|---|---|---|
| P0 | Always visible | Primary content, primary action, status |
| P1 | Visible, collapsible | Secondary content, navigation, metadata |
| P2 | On demand | Filters, settings, tertiary info |
| P3 | Large-viewport only | Supplementary, parallel comparisons |

This mapping IS the responsive strategy. CSS is implementation.

## Scale compression

Dimensions compress at different rates. Headlines compress most.
Body text compresses least. Hierarchy preserved.

| Dimension | Desktop | Mobile | Ratio |
|---|---|---|---|
| Headlines | 3-4rem | 1.75-2rem | ~2:1 |
| Body text | 1.0625-1.125rem | 1rem | ~1.1:1 |
| Section gaps | 96-144px | 40-60px | ~2.4:1 |
| Component padding | 32-40px | 16-24px | ~1.7:1 |

Fluid clamp() with per-element ratios:

```css
/* aggressive headline compression */
font-size: clamp(1.75rem, 1rem + 2.5vw, 3.5rem);

/* minimal body compression */
font-size: clamp(1rem, 0.95rem + 0.25vw, 1.125rem);

/* proportional spacing compression */
padding-block: clamp(2.5rem, 1rem + 5vw, 6rem);
```

## Interaction model swap

| Desktop | Mobile | Reason |
|---|---|---|
| Hover preview | Tap to expand | No hover on touch |
| Right-click menu | Long press / swipe | No right-click |
| Drag and drop | Tap-select, tap-place | Drag conflicts with scroll |
| Side-by-side | Swipeable tabs | No room |
| Keyboard shortcuts | Touch gestures | No keyboard |
| Tooltip on hover | Inline label | Hover unavailable |

Hover enhances, never gates. If accessing something requires hover,
it is invisible on mobile.

## Navigation metamorphosis

Primary destinations visible on all viewports.

```
Desktop:   Horizontal nav (5-7 items)
           OR persistent sidebar

Tablet:    Condensed horizontal (4-5 with labels)
           OR collapsible sidebar

Mobile:    Bottom tab bar (4-5 icons, always visible)
           NOT hamburger (hides everything)
```

Hamburger hides 100% of navigation. Bottom tabs keep top destinations
visible. Remaining items: 5th "More" tab.

## Dark mode

Not inversion. Redesign four systems:

### Elevation

Light: higher = darker shadow on lighter surface.
Dark: higher = lighter surface. Shadows invisible on dark.

```
Light:  #FFFFFF -> #F5F5F5 -> #EEEEEE  (darker = lower)
Dark:   #1A1A1A -> #242424 -> #2E2E2E  (lighter = higher)
```

### Chroma

Saturated colors on dark backgrounds cause halation. Reduce accent
chroma 10-20% in dark mode.

### Weight

Light text on dark appears thinner. Compensate all three:
- Weight: +1 step (400 -> 450-500)
- Letter-spacing: +0.01em
- Line-height: +0.05

### Images

Full-brightness images on dark backgrounds jar. Options:
- filter: brightness(0.85-0.9)
- Subtle dark overlay
- Dark-mode illustration variants

## Reduced motion

prefers-reduced-motion is NOT animation: none.

| Full | Reduced |
|---|---|
| Entrance (fade+slide) | Instant or <100ms fade |
| Scroll-triggered | Already visible |
| State transitions | Instant cut |
| Loading pulse | Static skeleton |
| Ambient motion | Removed |
| Color/opacity changes | KEEP |

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

## Touch targets

| Context | Minimum |
|---|---|
| Pointer (mouse) | 24px |
| Touch (mobile) | 44px |
| Hybrid (tablet) | 36px |

Targets can be larger than visual elements via padding.
Adjacent targets: 8px minimum gap.

## CJK typography

| Aspect | Latin | CJK |
|---|---|---|
| Word separation | Spaces | No spaces, equidistant chars |
| Line height | 1.5-1.6 | 1.7-1.8 |
| Measure | 65-75ch | 30-40 characters |
| Emphasis | Italic | Bold or emphasis dots |
| Hyphenation | Available | Not applicable |
| Line breaking | Between words | Between characters |

Mixed CJK + Latin:
- Half-width space between CJK and Latin/digits/symbols.
- Font stack with explicit CJK entries:
  ```css
  font-family: 'Geist', 'PingFang SC', 'Hiragino Sans GB',
               'Microsoft YaHei', 'Noto Sans CJK SC', sans-serif;
  ```
- CJK may need slightly larger base size at same visual weight.

## Print

```css
@media print {
  nav, footer, .interactive { display: none; }
  a[href]::after { content: " (" attr(href) ")"; font-size: 0.8em; }
  * { background: white !important; color: black !important; }
  body { font-family: Georgia, serif; font-size: 12pt; line-height: 1.5; }
  h1, h2, h3, figure, table { break-inside: avoid; }
  img { max-width: 100%; }
}
```

## Forced colors (Windows high contrast)

System overrides all colors. Survivors:
- Layout structure
- Borders (sole surface differentiator)
- outline for focus (not box-shadow)
- System color keywords

Surfaces that rely on background color alone: invisible in forced-colors.
Borders are the fallback.

## Viewport units

dvh, not vh. 100vh on iOS Safari does not account for the address bar.

```css
.full-height { min-height: 100dvh; }
```

## Container queries

Components adapt to their container, not the viewport.

```css
.wrapper { container-type: inline-size; }

@container (max-width: 400px) {
  .card { flex-direction: column; }
}
```

Use container queries for components in variable-width containers.
Use media queries for page-level layout and navigation.
