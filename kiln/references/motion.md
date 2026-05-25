# Motion

Communication channel. Like color or size, motion carries meaning.
Non-communicative motion is noise.

## Six signals

Every UI motion communicates one of these. If an animation does not map
to one, cut it.

| Signal | What it tells the user | Example |
|---|---|---|
| State | Something changed | Toggle, success indicator |
| Spatial origin | Where something lives | Sidebar from left |
| Continuity | Same object, new form | Card -> detail view |
| Hierarchy | This matters more | Staggered: first to move = most important |
| Feedback | Input received | Button press, hover lift |
| Progress | System working | Skeleton, progress bar |

## Vocabulary

Finite set. Every animation is a primitive or composition of these.

### Entrance / Exit

| Type | Mechanic | Communicates |
|---|---|---|
| Fade | opacity 0 -> 1 | Appearance, low spatial info |
| Slide | translateX/Y | Spatial origin |
| Scale | scale 0.95 -> 1 | Emergence |
| Reveal | clip-path / overflow | Containment |

Exits are faster than entrances. Entrance 200-500ms, exit 100-250ms.
The user initiated the exit; they want it done.

### State transition

| Type | Mechanic | Communicates |
|---|---|---|
| Crossfade | opacity swap | Content A -> B |
| Morph | shape interpolation | Same object, new form |
| Instant | no transition | Deliberate discontinuity |

### Feedback

| Type | Mechanic | Communicates |
|---|---|---|
| Press | scale 0.97-0.98 on :active | Physical depression |
| Lift | translateY -1px + shadow on hover | Affordance |
| Highlight | background flash | Action origin |

### Loading

| Type | Mechanic | Communicates |
|---|---|---|
| Skeleton | Layout placeholder + pulse | Structure preview |
| Progress | Determinate bar | Time estimate |
| Spinner | Indeterminate rotation | Working (last resort) |

Skeletons must match loaded layout dimensions. Generic gray rectangles
are noise. If skeleton does not structurally match loaded state, it is
wrong.

## Physical metaphors

Same vocabulary, different physics. Brand personality enters here.

### Snappy

Linear, Raycast feel. Arrives and stops. No overshoot.
- Micro: 100ms. Transition: 200ms. Entrance: 250ms.
- Easing: cubic-bezier(0.16, 1, 0.3, 1)
- Character: precision tool, respects time.

### Weighted

Apple feel. Spring physics, slight overshoot, settles.
- Micro: 120ms. Transition: 250ms. Entrance: 400ms.
- Easing: spring(stiffness: 300, damping: 20)
- Character: physical mass, things feel real.

### Deliberate

Stripe feel. Purposeful, unhurried.
- Micro: 150ms. Transition: 300ms. Entrance: 500ms.
- Easing: cubic-bezier(0.16, 1, 0.3, 1) entrance, ease-in-out state.
- Character: confident, watch me arrive.

### Mechanical

Brutalist feel. Instant or near-instant.
- Micro: 50ms. Transition: 100ms. Entrance: 150ms or instant.
- Easing: linear or step-end.
- Character: machine, no pretense.

## Stagger

Sequential reveals create hierarchy. First to move = most important.

- Delay between elements: 40-120ms.
- Direction follows reading order (top-bottom, left-right in LTR).
- Max 8-10 items. Beyond that, batch.
- Parent and children must share render tree for coordination.

## Scroll

The user's primary navigation tool. Respect it.

| Model | When | Risk |
|---|---|---|
| Natural (1:1) | Almost always | None |
| Snap | Full-viewport sections | Feels locked |
| Triggered entrance | Content-heavy | Over-animation |
| Parallax | Very sparingly | Distracting |
| Hijacked | NEVER | Steals navigation |

Scroll-triggered entrances:
- IntersectionObserver, not scroll listeners.
- Trigger once. Threshold 0.1-0.2.
- prefers-reduced-motion: skip, show immediately.

## Performance

- Animate ONLY transform and opacity. Never layout properties.
- will-change on actively animating elements only. Remove after.
- Background effects on position:fixed pointer-events:none layers.
- z-index systematic: nav 10, dropdown 20, modal 30, toast 40.
- React continuous animations: MotionValue outside render cycle.
  Never useState for frame-rate work.

## Choreography by template

### Editorial

Minimal. Content arrives, reader reads.
- Load: title fade 300ms, body immediate.
- Scroll: no entrance OR subtle opacity-only 200ms.
- Hover: lift on linked cards (1px + shadow shift).
- Nav: instant between articles.

### Dashboard

Functional only. Data changes visible, not theatrical.
- Load: skeleton -> content crossfade 200ms.
- Update: number morph OR instant swap.
- Hover: highlight on data rows.
- Nav: instant panels, slide-in details.

### Landing

Expressive. One orchestrated sequence per viewport.
- Hero: stagger (title -> subtitle -> CTA, 400ms total).
- Sections: scroll-triggered fade+slide, one per section.
- Hover: CTA effects.
- Nav: crossfade between sections.

## Motion anti-patterns (permanent)

- Animating layout properties (top, left, width, height).
- Bounce/elastic easing on non-playful interfaces.
- No prefers-reduced-motion handling.
- Uniform entrance (everything identical = no hierarchy).
- Scroll listeners instead of IntersectionObserver.
- Continuous animation on non-status elements.
- Exit slower than entrance.
