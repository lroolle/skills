# Animation patterns

Concrete implementations for common animation types. Each pattern
includes CSS, accessibility, and notes on when to use it.

## Entrance: fade + slide

The most common entrance. Combine opacity with translateY for a
natural "arriving from below" feel.

```css
.enter {
  opacity: 1;
  transform: translateY(0);
  transition: opacity 250ms var(--ease-out),
              transform 250ms var(--ease-out);
}
.enter[data-state="closed"] {
  opacity: 0;
  transform: translateY(8px);
}

@media (prefers-reduced-motion: reduce) {
  .enter {
    transition: opacity 150ms ease;
    transform: none;
  }
}
```

Modern CSS alternative with @starting-style (no JS mount state):

```css
.enter {
  opacity: 1;
  transform: translateY(0);
  transition: opacity 250ms var(--ease-out),
              transform 250ms var(--ease-out);

  @starting-style {
    opacity: 0;
    transform: translateY(8px);
  }
}
```

## Entrance: scale + fade

For popovers, dropdowns, context menus. Must be origin-aware.

```css
.popover {
  opacity: 1;
  transform: scale(1);
  transform-origin: var(--radix-popover-content-transform-origin);
  transition: opacity 200ms var(--ease-out),
              transform 200ms var(--ease-out);
}
.popover[data-state="closed"] {
  opacity: 0;
  transform: scale(0.95);
}
```

For non-Radix: calculate transform-origin from trigger position.

## Exit: faster than entrance

Exits use 50-70% of entrance duration. The user initiated the
dismissal; they want it done.

```css
.toast {
  transition: opacity 250ms var(--ease-out),
              transform 250ms var(--ease-out);
}
.toast[data-state="closed"] {
  opacity: 0;
  transform: translateY(-100%);
  transition-duration: 150ms;
}
```

## Feedback: button press

Every pressable element needs active-state feedback.

```css
.button {
  transition: transform 160ms var(--ease-out);
  -webkit-tap-highlight-color: transparent;
}
.button:active {
  transform: scale(0.97);
}

@media (hover: hover) and (pointer: fine) {
  .button:hover {
    /* hover effect here */
  }
}
```

Scale range: 0.95-0.98. Smaller = more dramatic press.

## Feedback: error shake

Quick horizontal jitter. 3-4 oscillations, small amplitude.

```css
@keyframes shake {
  0%, 100% { transform: translateX(0); }
  20% { transform: translateX(-4px); }
  40% { transform: translateX(4px); }
  60% { transform: translateX(-3px); }
  80% { transform: translateX(2px); }
}

.error {
  animation: shake 400ms ease-out;
}
```

## Stagger: list entrance

Items enter sequentially. First to move = most important.

```css
.item {
  opacity: 0;
  transform: translateY(8px);
  animation: fadeIn 300ms var(--ease-out) forwards;
}
.item:nth-child(1) { animation-delay: 0ms; }
.item:nth-child(2) { animation-delay: 50ms; }
.item:nth-child(3) { animation-delay: 100ms; }
.item:nth-child(4) { animation-delay: 150ms; }

@keyframes fadeIn {
  to { opacity: 1; transform: translateY(0); }
}
```

Keep delay 30-80ms between items. Max 8-10 items, then batch.
Never block interaction while stagger plays.

## Stagger: dynamic (JS)

For lists with dynamic length:

```jsx
{items.map((item, i) => (
  <motion.div
    key={item.id}
    initial={{ opacity: 0, y: 8 }}
    animate={{ opacity: 1, y: 0 }}
    transition={{ delay: i * 0.05, ease: [0.23, 1, 0.32, 1] }}
  />
))}
```

## State transition: accordion / collapse

Height animation without layout thrashing. Use grid trick:

```css
.accordion-content {
  display: grid;
  grid-template-rows: 0fr;
  transition: grid-template-rows 300ms var(--ease-in-out);
}
.accordion-content[data-open] {
  grid-template-rows: 1fr;
}
.accordion-content > div {
  overflow: hidden;
}
```

Alternative: animate `max-height` from 0 to a large value, but
this causes easing distortion when content is shorter than max.

## State transition: tab switch

Direction-aware: content slides one way forward, opposite back.

```css
.tab-content {
  transition: transform 200ms var(--ease-out),
              opacity 200ms var(--ease-out);
}
.tab-content[data-direction="forward"] {
  transform: translateX(8px);
  opacity: 0;
}
.tab-content[data-direction="back"] {
  transform: translateX(-8px);
  opacity: 0;
}
```

## Scroll reveal

IntersectionObserver, trigger once, low threshold.

```js
const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  },
  { threshold: 0.1, rootMargin: '-50px' }
);

document.querySelectorAll('.reveal').forEach((el) => observer.observe(el));
```

```css
.reveal {
  opacity: 0;
  transform: translateY(20px);
  transition: opacity 600ms var(--ease-out),
              transform 600ms var(--ease-out);
}
.reveal.visible {
  opacity: 1;
  transform: translateY(0);
}

@media (prefers-reduced-motion: reduce) {
  .reveal { opacity: 1; transform: none; transition: none; }
}
```

## Gesture: swipe to dismiss

Velocity-based dismissal. Quick flick dismisses regardless of
distance.

```js
const timeTaken = Date.now() - dragStart;
const velocity = Math.abs(distance) / timeTaken;

if (Math.abs(distance) >= THRESHOLD || velocity > 0.11) {
  dismiss();
}
```

Apply damping at boundaries. The further past the edge, the less
the element moves:

```js
const dampened = distance * (1 - Math.min(Math.abs(distance) / maxDrag, 0.6));
```

## Clip-path reveal

Hardware-accelerated content reveal using clip-path inset.

```css
.overlay {
  clip-path: inset(0 100% 0 0);
  transition: clip-path 200ms var(--ease-out);
}
.button:active .overlay {
  clip-path: inset(0 0 0 0);
  transition: clip-path 2s linear;
}
```

Hold-to-confirm pattern: slow fill on press (2s linear), snap
back on release (200ms ease-out).

## Drawer / bottom sheet

Slide from bottom with drawer-specific curve. Use translateY(100%)
so it adapts to content height.

```css
.drawer {
  transform: translateY(100%);
  transition: transform 500ms cubic-bezier(0.32, 0.72, 0, 1);
}
.drawer[data-open] {
  transform: translateY(0);
}
```

For drag: use spring physics and capture pointer events to handle
drag-outside-bounds.

## Skeleton / shimmer

Loading placeholder with moving sheen.

```css
.skeleton {
  background: linear-gradient(
    90deg,
    var(--skeleton-base) 0%,
    var(--skeleton-shine) 50%,
    var(--skeleton-base) 100%
  );
  background-size: 200% 100%;
  /* Built-in ease-in-out is fine for ambient continuous loops */
  animation: shimmer 1.5s ease-in-out infinite;
}

@keyframes shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}
```

Skeleton must match loaded layout dimensions. Generic gray
rectangles that don't match the final layout are noise.

## WAAPI: programmatic with CSS performance

When you need JS control with GPU acceleration:

```js
element.animate(
  [
    { clipPath: 'inset(0 0 100% 0)' },
    { clipPath: 'inset(0 0 0 0)' },
  ],
  {
    duration: 1000,
    fill: 'forwards',
    easing: 'cubic-bezier(0.77, 0, 0.175, 1)',
  }
);
```

WAAPI is hardware-accelerated, interruptible, and needs no library.

## Spring: mouse-tracking decoration

Use spring interpolation instead of direct value binding for
decorative mouse-follow effects:

```jsx
import { useSpring } from 'framer-motion';

// Direct: feels artificial, instant
const rotation = mouseX * 0.1;

// Spring: feels natural, has momentum
const springRotation = useSpring(mouseX * 0.1, {
  stiffness: 100,
  damping: 10,
});
```

Only for decorative effects. Functional UI (graphs, sliders)
should track directly without spring.
