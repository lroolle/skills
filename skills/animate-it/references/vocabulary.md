# Animation glossary

Working definitions for terms that show up in animation requests,
organized by the protocol's motion types so you can look up the
category you are implementing. For interactive demos of most of
these concepts, Emil Kowalski's
[animations.dev/vocabulary](https://animations.dev/vocabulary) is
the best single page on the web.

## Entrances and exits

- **Fade**: opacity transition between 0 and 1. The cheapest and
  most neutral entrance.
- **Slide**: element translates in from an offset position,
  usually 8-16px, not from off-screen.
- **Scale entrance**: element grows to full size as it appears.
  Start at 0.95, never 0.
- **Pop**: scale entrance with deliberate overshoot past 1.0
  before settling. Reads as playful; budget it accordingly.
- **Reveal**: content uncovered by an animated clip-path or mask
  rather than moving the element itself.
- **Enter/exit pair**: the two animations an element plays when
  mounted and unmounted. Exits run faster (50-70% of entrance).

## Feedback

- **Press feedback**: scale-down (0.95-0.98) on active state.
  Confirms the press landed.
- **Hold-to-confirm**: a fill or progress effect that completes
  only if the user keeps pressing. Slow press, instant release.
- **Shake**: 3-4 small horizontal oscillations signaling
  rejection or error.
- **Ripple**: circle expanding from the tap point. Material
  Design's signature feedback.
- **Rubber-banding**: increasing resistance when dragging past a
  boundary, with snap-back on release. iOS's signature feel.

## State transitions

- **Crossfade**: outgoing element fades out while the incoming
  one fades in, in the same place. A little blur masks imperfect
  alignment.
- **Morph**: one shape continuously deforms into another instead
  of swapping.
- **Layout animation / FLIP**: animating size or position changes
  by measuring First and Last positions, applying the Inverted
  transform, then Playing it back to zero. Turns layout changes
  into cheap transforms.
- **Shared element transition**: an element appears to travel
  between two views, keeping its identity across the navigation.
- **Accordion**: height expand/collapse. Animate grid rows or
  measured height, never max-height to an arbitrary cap.
- **Direction-aware transition**: content slides left going
  forward, right going back -- the motion encodes navigation
  direction.

## Scroll

- **Scroll reveal**: element animates in when it enters the
  viewport. Trigger once, via IntersectionObserver.
- **Scroll-driven animation**: progress bound to scroll position
  rather than time.
- **Parallax**: layers translating at different rates to fake
  depth.
- **View transitions**: the browser API that snapshots old and
  new DOM states and animates between them, including across
  page navigations.

## Continuous

- **Marquee**: content scrolling in an infinite loop.
- **Pulse**: gentle repeating scale or opacity cycle.
- **Skeleton / shimmer**: loading placeholder with a moving
  sheen. Must match the loaded layout's dimensions.
- **Idle animation**: subtle ambient motion while an element
  waits. Easy to overdo; default to none.
- **Alternate / yoyo**: a loop that plays forward then reverses
  each iteration.

## Gesture

- **Momentum**: motion that carries the drag's velocity after
  release instead of stopping dead.
- **Velocity-based dismissal**: a fast flick dismisses regardless
  of distance traveled; a slow drag needs to cross a threshold.
- **Interruptible animation**: motion that can be redirected
  mid-flight without restarting -- the property that makes
  springs feel right for gestures and CSS keyframes feel wrong.

## Timing and easing

- **Keyframes**: fixed points (0%, 50%, 100%) the browser
  interpolates between.
- **Tween / interpolation**: the generated in-between frames.
- **Stagger**: starting each item's animation slightly after the
  previous one. 30-80ms gaps; first to move reads as most
  important.
- **Orchestration**: coordinating multiple animations' timing so
  they read as one event rather than a pileup.
- **Fill mode**: whether an element holds the first/last keyframe
  styles outside the animation's active window.
- **Easing**: the speed curve. ease-out (fast start) for UI,
  ease-in-out for on-screen movement, linear for constant motion,
  never ease-in for things the user is waiting on.
- **Cubic-bezier**: the four-number curve definition behind every
  custom easing.
- **Asymmetric easing**: different curves for opposite directions
  of the same interaction (slow deliberate press, fast release).

## Springs

- **Stiffness**: how strongly the spring pulls toward its target.
  Higher is snappier.
- **Damping**: how quickly oscillation dies. Higher settles
  faster.
- **Mass**: inertia; higher feels heavier and slower to redirect.
- **Bounce**: overshoot past the target before settling.
- **Perceptual duration**: when the spring *looks* done, which is
  earlier than when it mathematically stops. Compare springs to
  duration-based animation on this number.

## Performance

- **Compositing**: the GPU moving or fading a layer without the
  main thread recalculating layout or paint. Only transform and
  opacity qualify.
- **Jank**: visible stutter from missed frames.
- **Layout thrash**: animating properties (width, top, margin)
  that force synchronous layout recalculation every frame.
- **will-change**: a hint to promote an element to its own layer.
  Apply only while animating; layers cost memory.

## Classic principles

The Disney-era animation principles that still apply to
interfaces: **anticipation** (small wind-up before the move),
**follow-through** (parts settle after the main motion stops),
**squash and stretch** (deformation conveys weight). And the
interface-native ones: motion must earn its place by communicating
something, and the more often an animation is seen, the shorter
and subtler it must be.
