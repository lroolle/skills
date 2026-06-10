# Easing curves and spring configurations

## CSS custom properties

Define these once at the root. Use them everywhere.

```css
:root {
  /* Strong ease-out for UI interactions */
  --ease-out: cubic-bezier(0.23, 1, 0.32, 1);

  /* Strong ease-in-out for on-screen movement */
  --ease-in-out: cubic-bezier(0.77, 0, 0.175, 1);

  /* iOS-like drawer curve (from Ionic Framework) */
  --ease-drawer: cubic-bezier(0.32, 0.72, 0, 1);

  /* Subtle ease for hover/color changes */
  --ease-subtle: cubic-bezier(0.25, 0.1, 0.25, 1);
}
```

The built-in CSS `ease-out`, `ease-in-out`, etc. are too weak.
They lack the punch that makes animations feel intentional. Always
use custom curves.

## Easing comparison

| Easing | When to use | Curve |
|---|---|---|
| ease-out (strong) | Entrances, exits, most UI | cubic-bezier(0.23, 1, 0.32, 1) |
| ease-in-out (strong) | On-screen movement, morph | cubic-bezier(0.77, 0, 0.175, 1) |
| ease (subtle) | Hover, color change | cubic-bezier(0.25, 0.1, 0.25, 1) |
| linear | Constant motion, progress bars | linear |
| drawer | Bottom sheets, drawers | cubic-bezier(0.32, 0.72, 0, 1) |

## Never ease-in for UI

ease-in starts slow and ends fast. This delays the initial movement
at the exact moment the user is watching most closely. A dropdown
with ease-in at 300ms FEELS slower than ease-out at the same 300ms.

The only valid use: an object accelerating away (a ball being
thrown). In UI, almost nothing accelerates away from the user.

## Asymmetric easing

Press and release use different curves:

```css
/* Release: fast snap-back */
.overlay {
  transition: clip-path 200ms var(--ease-out);
}

/* Press: slow and deliberate */
.button:active .overlay {
  transition: clip-path 2s linear;
}
```

Pattern: slow where the user is deciding, fast where the system
is responding.

## Spring configurations

### Apple-style (duration + bounce)

Easier to reason about. Apple uses this internally.

```js
{ type: "spring", duration: 0.5, bounce: 0.2 }
```

- `duration`: how long the animation feels (not exact)
- `bounce`: 0 = no overshoot, 0.5 = very bouncy. Keep 0.1-0.3.

### Traditional physics (mass + stiffness + damping)

More control, harder to tune.

```js
{ type: "spring", mass: 1, stiffness: 100, damping: 10 }
```

- `stiffness`: higher = snappier (100-300 typical)
- `damping`: higher = settles faster (10-30 typical)
- `mass`: higher = heavier feel (0.5-2 typical)

### Preset spring configs

| Feel | Config | Use for |
|---|---|---|
| Snappy | `{ stiffness: 300, damping: 30 }` | Button feedback, tooltips |
| Bouncy | `{ stiffness: 200, damping: 15 }` | Playful entrances, celebrations |
| Heavy | `{ stiffness: 100, damping: 20, mass: 2 }` | Drawers, large panels |
| Gentle | `{ stiffness: 80, damping: 20 }` | Background movement, parallax |
| Apple Dynamic Island | `{ duration: 0.5, bounce: 0.25 }` | Morphing containers |

### When to use springs vs duration

Springs:
- Gesture interactions (drag, swipe) -- maintains velocity on interrupt
- Elements that should feel "alive"
- Any animation the user might interrupt mid-flight

Duration-based:
- Predetermined UI transitions (enter, exit, hover)
- Constant-speed motion (progress bars, marquees)
- Animations where exact timing matters

## Tools for curve design

- easing.dev -- visual curve editor with presets
- easings.co -- curated collection of easing functions
- Chrome DevTools > Elements > Computed > click on a transition
  value to open the visual cubic-bezier editor

## Perceptual duration

A spring that technically oscillates for 800ms but visually settles
at 400ms "feels" 400ms long. When comparing springs to
duration-based animations, compare the perceptual duration (when it
looks done) not the mathematical duration (when it stops moving).

Motion's `duration` in Apple-style springs approximates this
perceptual feel rather than exact mathematical completion.
