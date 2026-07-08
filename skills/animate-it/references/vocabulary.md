# Animation glossary

Working definitions for terms that show up in animation requests,
organized by the protocol's motion types. Each term gets what it
is and how it is actually built; production values are cited from
MIT-licensed [sonner](https://github.com/emilkowalski/sonner)
(toasts) and [vaul](https://github.com/emilkowalski/vaul)
(drawers). Interactive demos:
[animations.dev/vocabulary](https://animations.dev/vocabulary).

## Entrances and exits

- **Fade**: opacity transition between 0 and 1. The cheapest,
  most neutral entrance; combine with a small translate or scale
  so the element arrives from somewhere.
- **Slide**: element translates in from an offset. UI slides use
  8-16px of offset, not off-screen distances -- the motion is a
  cue, not a journey. Percentage transforms
  (`translateY(100%)`) move an element by its own height, which
  is how sonner enters toasts of any size with one rule.
- **Scale entrance**: element grows to full size as it appears.
  Start at 0.95, never 0 -- nothing real materializes from a
  point.
- **Pop**: scale entrance that overshoots past 1.0 before
  settling. Reads as playful; spend it on rare moments, not
  every mount.
- **Reveal**: content uncovered by an animated `clip-path` or
  mask while the element itself stays put. Hardware-accelerated
  and interruptible, unlike width/height animation.
- **Enter/exit pair**: the mount and unmount animations. Exits
  run at 50-70% of the entrance duration -- the user asked for
  the dismissal; make it feel obeyed. sonner's exit is 200ms,
  and it keeps the DOM node alive exactly that long
  (`TIME_BEFORE_UNMOUNT = 200`) so React unmount and CSS exit
  end together.

## Feedback

- **Press feedback**: scale-down on `:active`, 0.95-0.98.
  Confirms the press landed before any async work begins.
- **Hold-to-confirm**: a fill or progress effect that completes
  only if the user keeps pressing -- slow deliberate press
  (seconds, linear), instant snap-back on release.
- **Shake**: 3-4 small horizontal oscillations (±2-4px,
  ~400ms total) signaling rejection. Amplitude decays toward
  zero; a constant-amplitude shake reads as broken, not firm.
- **Ripple**: circle expanding from the tap point, Material
  Design's signature. Implemented as a scaled pseudo-element or
  appended span at the click coordinates.
- **Rubber-banding**: drag resistance past a boundary with
  snap-back on release. The resistance must be sublinear --
  vaul dampens overdrag with `8 * (ln(v + 1) - 2)`, a
  logarithmic curve, so the first pixels past the edge move
  noticeably and further dragging buys less and less.

## State transitions

- **Crossfade**: outgoing element fades out while the incoming
  one fades in, in the same place. A 2px blur during the swap
  masks imperfect alignment by tricking the eye into reading one
  continuous object.
- **Morph**: one shape continuously deforms into another instead
  of swapping -- animated `clip-path`, SVG path interpolation, or
  a shared-element transition.
- **Layout animation / FLIP**: animate size and position changes
  by measuring First and Last positions, applying the Inverted
  delta as a transform, then Playing it back to zero. Turns
  layout changes (reordering, reparenting) into cheap composited
  transforms.
- **Shared element transition**: an element appears to travel
  between two views, keeping its identity across navigation.
  FLIP under the hood; the View Transitions API gives it to you
  across page loads.
- **Accordion**: height expand/collapse. Animate
  `grid-template-rows: 0fr -> 1fr` or a measured pixel height --
  never `max-height` to an arbitrary cap, which distorts the
  easing for short content.
- **Direction-aware transition**: content slides left going
  forward, right going back; the motion encodes which way the
  user moved through the hierarchy.
- **Spatial consistency**: across any transition, the element
  keeps its identity -- position, scale, and origin connect the
  before and after instead of teleporting.

## Scroll

- **Scroll reveal**: element animates in when entering the
  viewport. IntersectionObserver, trigger once, low threshold
  (~0.1) with negative rootMargin so the reveal starts before
  the element is fully visible.
- **Scroll-driven animation**: progress bound to scroll position
  rather than time -- CSS `animation-timeline: scroll()` or a
  scroll listener writing a CSS variable.
- **Parallax**: layers translating at different rates to fake
  depth. Subtle ratios (0.1-0.3 of scroll delta) on decoration
  only; never on content the user is trying to read.
- **View transitions**: the browser API that snapshots old and
  new DOM, then animates between them -- crossfade by default,
  shared elements via `view-transition-name`.
- **Page transition**: motion across navigation. Without the
  View Transitions API this means exit-animate, navigate,
  enter-animate -- and it must never block the navigation.

## Continuous and ambient

- **Marquee**: content scrolling in an infinite loop. Duplicate
  the content and translate the pair -100%; linear easing,
  pause on hover.
- **Pulse**: gentle repeating scale or opacity cycle. Built-in
  ease-in-out is fine for ambient loops -- nobody is waiting on
  them.
- **Skeleton / shimmer**: loading placeholder with a moving
  sheen -- an animated `background-position` over a three-stop
  gradient. Must match the loaded layout's dimensions or it is
  noise, not anticipation.
- **Float / orbit**: slow ambient drift or circular motion on
  decoration. Defaults to "no" at the gate; if kept, transform
  only, long period, small amplitude.
- **Alternate / yoyo**: a loop that plays forward then reverses
  (`animation-direction: alternate`), avoiding the snap-back of
  a restarting loop.
- **Idle animation**: subtle motion while an element waits for
  interaction. The most over-added category; earn it or cut it.

## Gesture

- **Drag**: pointer capture + transform updates per move event.
  Write `transform` directly on the element, not through a CSS
  variable on a parent -- variable inheritance recalculates every
  child per frame.
- **Swipe to dismiss**: distance OR velocity, whichever triggers
  first. sonner dismisses a toast past 45px of travel
  (`SWIPE_THRESHOLD = 45`) or a flick faster than 0.11 px/ms --
  the velocity path is what makes a short, fast flick feel
  heard.
- **Velocity threshold**: the flick speed that overrides
  distance. vaul treats a release faster than 0.4 px/ms
  (`VELOCITY_THRESHOLD`) as intent: a fast flick closes the
  drawer no matter how short the drag was.
- **Close threshold**: the distance fallback for a slow drag.
  vaul closes the drawer past 25% of its height
  (`CLOSE_THRESHOLD = 0.25`); short of it, the drawer springs
  back to open.
- **Snap points**: the resting positions a sheet can settle at
  (peek, half, full). On release, vaul advances exactly one
  snap point in the flick's direction when the flick is fast
  and travel is under 40% of the viewport; a slow release
  settles at whichever point is nearest.
- **Momentum**: motion carries the release velocity instead of
  stopping dead. Springs give this for free; duration-based
  animation cannot.
- **Drag to reorder**: dragging items within a list. The dragged
  item follows the pointer; siblings FLIP into their new slots.
- **Interruptible animation**: motion that can be redirected
  mid-flight without restarting from zero -- the property that
  makes springs and CSS transitions right for gestures, and CSS
  keyframes wrong.

## Timing and easing

- **Keyframes**: fixed points (0%, 50%, 100%) the browser
  interpolates between. Keyframes restart from zero when
  retriggered -- use transitions for anything that fires rapidly.
- **Tween / interpolation**: the generated in-between frames.
- **Stepped animation**: discrete jumps instead of smooth
  interpolation -- `steps(n)`. The mechanism behind typewriter
  effects and sprite playback.
- **Stagger**: each item's animation starts 30-80ms after the
  previous one. First to move reads as most important; past
  8-10 items, batch the rest.
- **Orchestration**: coordinating multiple animations so they
  read as one event rather than a pileup -- shared timing
  origin, deliberate delays, one easing family.
- **Delay**: time before an animation starts. On tooltips it is
  a feature: the first tooltip waits (~300-500ms) to filter
  accidental hovers, then adjacent tooltips open instantly.
- **Fill mode**: whether the element holds the first/last
  keyframe styles outside the animation window
  (`animation-fill-mode: forwards` keeps the end state).
- **Easing**: the speed curve. ease-out for things responding to
  the user, ease-in-out for on-screen movement, linear for
  constant motion, never ease-in for anything the user awaits.
- **Cubic-bezier**: the four-number curve behind custom easing.
  vaul's drawer rides `cubic-bezier(0.32, 0.72, 0, 1)` for
  500ms -- a curve that spends most of its time decelerating,
  which is what makes the sheet feel weighty but obedient.
- **Asymmetric easing**: different curves for the two directions
  of one interaction -- slow deliberate press, fast snap
  release.

## Springs

- **Stiffness / tension**: how strongly the spring pulls toward
  its target. Higher is snappier (100-300 typical).
- **Damping / friction**: how quickly oscillation dies. Higher
  settles faster (10-30 typical).
- **Mass**: inertia. Higher feels heavier and slower to
  redirect (0.5-2 typical).
- **Bounce**: overshoot past the target before settling. Keep
  0.1-0.3; serious UI tolerates less bounce than you think.
- **Perceptual duration**: when the spring *looks* done --
  earlier than when it mathematically stops. Compare springs to
  duration-based animation on this number, and prefer
  duration+bounce APIs that target it directly.
- **Velocity injection**: starting a spring with the gesture's
  release velocity so the handoff from finger to animation is
  seamless.

## Text and numbers

- **Typewriter**: text appearing character by character --
  `steps()` over a `ch`-width or incremental slicing. Reserve
  for genuinely streamed content; fake streaming irritates.
- **Text morph**: changing text animates per character --
  shared characters stay, differing ones crossfade or flip.
- **Number ticker**: digits roll to a new value, odometer-style:
  a vertical strip of digits translated per place value.
- **Tabular numbers**: `font-variant-numeric: tabular-nums` --
  fixed-width digits so updating numbers don't cause layout
  shift. Not an animation; the thing that stops an unwanted
  one.

## Reveals, masks, depth

- **Clip-path**: clips an element to a shape; animatable and
  composited. The standard tool for wipes, hold-to-confirm
  fills, and reveals.
- **Mask**: hides or shows parts of an element through an image
  or gradient's alpha -- soft edges where clip-path is hard.
- **Line drawing**: an SVG path drawing itself --
  `stroke-dasharray` set to the path length, `stroke-dashoffset`
  animated from that length to 0.
- **Before/after slider**: a draggable divider wiping between
  two stacked images -- clip-path width driven by pointer
  position.
- **Perspective / 3D tilt**: `perspective` on the parent gives
  depth to `rotateX/rotateY` on children. Low values (600-1000px)
  exaggerate; subtle tilt needs higher.
- **Scaled background / depth stack**: the page behind a sheet
  scales down and rounds its corners, reading as a card pushed
  into the distance. vaul scales the background with the same
  500ms drawer curve and an 8px radius so both layers move as
  one scene.

## Performance

- **Compositing**: the GPU moving or fading a layer with no
  main-thread layout or paint. Only `transform` and `opacity`
  qualify; everything else pays layout tax.
- **Layout thrash**: animating properties (width, top, margin)
  that force synchronous layout every frame, or interleaving
  style reads and writes in JS.
- **Jank / dropped frames**: visible stutter when a frame
  misses its 16.7ms (60fps) budget. CSS animations survive a
  busy main thread; rAF-driven JS animation does not.
- **will-change**: promotes an element to its own layer ahead
  of animation. Apply only while animating, remove after --
  layers cost memory and too many defeat the optimizer.
- **Perceived performance**: the right animation makes waiting
  feel shorter -- skeletons that match the layout, instant
  feedback before slow work, exits faster than entrances. The
  clock does not move; the experience does.

## Classic principles

The Disney-era principles that survive in interfaces:
**anticipation** (a small wind-up before the move),
**follow-through** (parts settle after the main motion stops),
**squash and stretch** (deformation conveys weight -- in UI, a
subtle scale on press is its descendant). And the
interface-native ones: motion must communicate state, origin,
hierarchy, feedback, or progress -- and the more often an
animation is seen, the shorter and subtler it must be.
