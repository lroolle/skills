---
name: animate-it
description: >-
  Animation implementation protocol for web interfaces: easing,
  duration, springs, CSS transitions, keyframes, Motion (Framer
  Motion), WAAPI. Fires on three branches: adding motion to a
  component ("animate this", "should this animate?"); diagnosing
  motion that feels wrong ("make this transition smoother", "what
  easing should I use"); and reviewing pasted animation code.
  Deciding what should move and why is kiln's job (motion.md);
  this skill makes it move correctly. Static styling without
  motion is kiln's too.
---

# animate-it

Kiln decides what should move and why. This skill decides how to
make it move correctly -- easing, duration, implementation, and the
invisible details that separate "has animation" from "feels right."

Two modes:
- **Implement mode**: component has no animation, needs some
- **Review mode**: component has animation, something feels off

## The protocol

Five steps. Skip the ones you don't need.

### Step 1 -- Gate

Should this animate at all?

| Frequency | Decision |
|---|---|
| 100+ times/day (keyboard shortcuts, command palette) | No animation. Ever. |
| Tens of times/day (hover, list navigation) | Remove or drastically reduce |
| Occasional (modals, drawers, toasts) | Standard animation |
| Rare / first-time (onboarding, celebrations) | Can add delight |

Don't add entrance/exit animations to keyboard-initiated actions.
They repeat hundreds of times a day and animation makes them feel
slow. Focus-ring transitions and highlight movement at <=100ms are
fine -- those are feedback, not ceremony.

If the answer is "don't animate," stop here. Saying no is the most
valuable thing this skill does.

### Step 2 -- Classify

What kind of motion is this? Each type has different rules.

| Type | Examples | Key constraint |
|---|---|---|
| Entrance / exit | Modal open, toast appear, dropdown | Exits faster than entrances |
| Feedback | Button press, hover lift, error shake | Must be instant-feeling |
| State transition | Tab switch, accordion, toggle | Preserve spatial context |
| Scroll-triggered | Reveal on scroll, parallax | Trigger once, low threshold |
| Continuous | Spinner, marquee, skeleton pulse | GPU-only, no layout props |
| Gesture | Drag, swipe, pinch | Needs spring physics |

### Step 3 -- Specify

Three decisions: easing, duration, tool.

**Easing decision tree:**

Is the element entering or exiting?
-> ease-out (starts fast, instant feedback)

Is it moving/morphing on screen?
-> ease-in-out (natural acceleration/deceleration)

Is it a hover or color change?
-> var(--ease-subtle) -- subtle, doesn't draw attention

Is it constant motion (marquee, progress)?
-> linear

Is it a gesture or drag interaction?
-> spring (physics-based, interruptible)

Default -> ease-out

Use custom curves. Built-in CSS easings are too weak:

```css
--ease-out: cubic-bezier(0.23, 1, 0.32, 1);
--ease-in-out: cubic-bezier(0.77, 0, 0.175, 1);
--ease-drawer: cubic-bezier(0.32, 0.72, 0, 1);
--ease-subtle: cubic-bezier(0.25, 0.1, 0.25, 1);
```

Never use ease-in for UI animations. It starts slow, which makes
the interface feel sluggish at the exact moment the user is watching
most closely.

**Duration table:**

| Element | Duration | Why |
|---|---|---|
| Button press / feedback | 100-160ms | Must feel synchronous with the physical press |
| Tooltips, small popovers | 125-200ms | Quick enough to feel instant, slow enough to track |
| Dropdowns, selects | 150-250ms | User is deciding; animation aids spatial orientation |
| Modals, drawers | 200-500ms | Larger elements need time to read as coherent motion |
| Exit (any element) | 50-70% of entrance | User initiated dismissal; they want it done |

UI animations stay under 300ms. A 180ms dropdown feels more
responsive than a 400ms one.

**Tool selection:**

| Situation | Use | Why |
|---|---|---|
| Predetermined animation (enter, exit, hover) | CSS transitions | Off main thread for transform/opacity, interruptible |
| Complex keyframe sequence | CSS @keyframes | Off main thread for transform/opacity, declarative |
| Dynamic/conditional animation | Motion (Framer Motion) | Composable, layout-aware |
| Gesture with momentum | Spring (useSpring) | Physics-based, maintains velocity |
| Programmatic with CSS perf | WAAPI | Hardware-accelerated, JS control |
| Animation on rapidly-triggered element | CSS transitions | Keyframes restart from zero |

Prefer CSS transitions for UI. They interrupt and retarget smoothly.
Keyframes restart from zero, which causes jumps when triggered
rapidly (e.g., adding toasts).

### Step 4 -- Code

Output the implementation. Follow these rules:

**Start from scale(0.95), never scale(0).** Nothing in the real
world disappears completely. Even a barely-visible initial scale
feels more natural.

```css
/* Wrong */
.entering { transform: scale(0); }

/* Right */
.entering { transform: scale(0.95); opacity: 0; }
```

**Specify exact properties in transition.** Never `transition: all`.
It animates properties you didn't intend and triggers unnecessary
layout work.

```css
/* Wrong */
.element { transition: all 300ms; }

/* Right */
.element { transition: transform 200ms var(--ease-out), opacity 200ms var(--ease-out); }
```

**Make popovers origin-aware.** Popovers scale from their trigger,
not from center. Modals are the exception -- they stay centered.

```css
.popover { transform-origin: var(--radix-popover-content-transform-origin); }
```

**Add press feedback to all buttons.**

```css
.button { transition: transform 160ms var(--ease-out); }
.button:active { transform: scale(0.97); }
```

**Use @starting-style for entry animations** (modern CSS, no JS):

```css
.toast {
  opacity: 1;
  transform: translateY(0);
  transition: opacity 250ms var(--ease-out), transform 250ms var(--ease-out);
  @starting-style {
    opacity: 0;
    transform: translateY(100%);
  }
}
```

**Use blur to mask imperfect crossfades.** When a crossfade between
two states feels off, add `filter: blur(2px)` during the transition.
It tricks the eye into perceiving one smooth transformation instead
of two objects swapping.

**Asymmetric timing on deliberate actions.** Press should be slow
when deliberate (hold-to-delete: 2s linear), release always snappy
(200ms ease-out).

**Percentage translateY for adaptive sizing.** `translateY(100%)`
moves an element by its own height regardless of actual dimensions.
Prefer this over hardcoded pixel values.

**Skip tooltip delay on subsequent hovers.** First tooltip delays
to prevent accidental activation. Adjacent tooltips after that open
instantly with no animation.

Load [patterns.md](references/patterns.md) for the full pattern
cookbook with code for 15+ common animations.

### Step 5 -- Check

Review the animation against these rules. Output a markdown table.

| Issue | Fix | Why |
|---|---|---|
| `transition: all` | Specify exact properties | Avoids unintended layout animation |
| `scale(0)` entry | Start from `scale(0.95)` + `opacity: 0` | Nothing appears from nothing |
| `ease-in` on UI element | Switch to `ease-out` or custom curve | ease-in feels sluggish |
| `transform-origin: center` on popover | Set to trigger location | Popovers anchor to trigger |
| Animation on keyboard action | Remove entirely | Too frequent, feels slow |
| Duration > 300ms on UI element | Reduce to 150-250ms | UI should feel snappy |
| Hover without media query | Add `@media (hover: hover) and (pointer: fine)` | Touch devices false-trigger hover |
| Keyframes on rapidly-triggered element | Use CSS transitions | Keyframes restart from zero |
| Motion `x`/`y` props under load | Use `transform: "translateX()"` | Guarantees GPU compositing; older Motion used rAF |
| No `:active` state on button | Add `scale(0.97)` on `:active` | Buttons must feel responsive |
| Same enter/exit speed | Make exit 50-70% of entrance | Users want exits done fast |
| No `prefers-reduced-motion` | Add reduced-motion media query | Accessibility requirement |

## Accessibility

Reduced motion means fewer and gentler animations, not zero.
Keep opacity and color transitions. Remove movement and position
animations.

```css
@media (prefers-reduced-motion: reduce) {
  .element {
    animation: fade 0.2s ease;
    /* No transform-based motion */
  }
}
```

Gate hover animations behind `@media (hover: hover) and (pointer: fine)`
to prevent false positives on touch devices.

## Performance

- Animate ONLY transform and opacity. Everything else triggers layout.
- CSS variables on a parent recalculate all children. Update
  `transform` directly on the element for drag interactions.
- Older Framer Motion (v10-) used requestAnimationFrame for `x`/`y`
  shorthand. Motion v11+ may use WAAPI. When in doubt, use the full
  `transform` string to guarantee GPU acceleration.
- CSS animations beat JS under load. When the browser is busy, JS
  animations (requestAnimationFrame) drop frames. CSS stays smooth.
- `will-change` on actively animating elements only. Remove after.
- Keep `filter: blur()` under 20px, especially in Safari. Heavy
  blur is expensive and can cause frame drops.

## Anti-patterns

- **Animating layout properties.** `top`, `left`, `width`, `height`,
  `padding`, `margin` trigger layout recalc. Use transform instead.
- **Bounce/elastic on non-playful interfaces.** A banking dashboard
  with bouncy modals reads as unserious.
- **Uniform entrance.** Everything entering identically = no
  hierarchy. Stagger to communicate importance.
- **Motion without purpose.** If the animation doesn't communicate
  state, origin, continuity, hierarchy, feedback, or progress, cut
  it.
- **Scroll hijacking.** Never steal the user's scroll. Use
  IntersectionObserver for scroll-triggered effects.

## Spring quick reference

Springs feel more natural than duration-based animations for gestures
and interruptible motion.

```js
// Apple-style (easier to reason about)
{ type: "spring", duration: 0.5, bounce: 0.2 }

// Traditional physics (more control)
{ type: "spring", mass: 1, stiffness: 100, damping: 10 }
```

Springs maintain velocity when interrupted -- CSS animations restart
from zero. Use springs for anything the user might change mid-motion.

## Output format

For implement mode:
```
## Gate
[Should it animate? Frequency assessment.]

## Classification
[What type of motion. Key constraint.]

## Specification
[Easing curve, duration, tool choice with reasoning.]

## Code
[Production-ready CSS/JS. Includes reduced-motion.]
```

For review mode:
```
## Review
| Before | After | Why |
|---|---|---|
| ... | ... | ... |
```

## References

| File | Load when |
|---|---|
| [patterns.md](references/patterns.md) | Implementing a specific animation type (entrance, gesture, scroll, etc.) |
| [vocabulary.md](references/vocabulary.md) | User uses an animation term you need to look up; includes production constants from sonner/vaul |
| [easing-curves.md](references/easing-curves.md) | Choosing or customizing easing curves and spring configs |
