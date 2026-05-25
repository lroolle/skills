# Patterns

Composable structural building blocks. Framework-agnostic, aesthetic-agnostic.
Each pattern: problem, mechanic, composition rules.

## Typographic scale

Problem: reading hierarchy.

Pick one ratio, commit:
- 1.25 (major third): tight, data-friendly
- 1.333 (perfect fourth): balanced, editorial
- 1.5 (perfect fifth): dramatic, brand-forward

| Role | Scale | Use |
|---|---|---|
| xs | 0.75rem | Captions, legal, timestamps |
| sm | 0.875rem | Metadata, secondary labels |
| base | 1rem (16px) | Body text |
| lg | base * ratio | Subheadings, lead text |
| xl+ | base * ratio^2..n | Headlines, hero |

Rules:
- Body line length: 65-75ch max.
- Line-height inversely with size: body 1.5-1.6, headlines 1.1-1.2.
- Light on dark compensation: line-height +0.05, letter-spacing +0.01em,
  weight +1 step. All three axes, not just one.
- Paragraph rhythm: space between OR first-line indent. Never both.

Composition: density multiplier adjusts base size. Surface pattern
constrains padding relative to type.

## Baseline grid

Problem: vertical rhythm.

All vertical spacing is a multiple of the line-height unit. Body at
16px/1.5 = 24px unit. Margins, padding, gaps, image heights snap to grid.

- Half-units (12px) for tight internal component spacing.
- Section gaps: 3-6 units (72-144px at 24px).
- Derive unit from body line-height, not arbitrary numbers.

Composition: constrains typographic scale leading. Constrains surface
padding.

## Density control

Problem: information per viewport without losing hierarchy.

| Level | Multiplier | Feel | Use |
|---|---|---|---|
| Airy | 1.5 | Gallery, luxury | Landing, portfolio |
| Normal | 1.0 | Standard | Most apps |
| Dense | 0.85 | Professional | Dashboards, tools |
| Packed | 0.7 | Cockpit | Trading, monitoring |

At density <= 0.75: monospace for all numbers (column alignment).
At density <= 0.7: drop card containers, use border-top or divide-y.
Base size can decrease: 1rem normal, 0.9375rem dense, 0.875rem packed.

Composition: multiplies baseline unit. Packed density drops shadows/radius.

## Asymmetric composition

Problem: break centered-stack default.

- Split screen (60/40, 70/30): content one side, media other.
- Offset grid: content column with generous margin on one edge.
- Asymmetric whitespace: content hugs one edge, other is empty.

Wider zone carries primary content. Narrower supports.
Mobile: collapse to single column, primary first in source order.
Centered layouts acceptable for modals, login, error pages. Not for
primary page structure.

## Visible compartmentalization

Problem: group without containers.

- Rule-separated: 1px horizontal rules between groups.
- Border-boxed: 1px border, no shadow, minimal radius.
- Space-separated: generous whitespace, no borders.
- Mixed: rules within groups, space between groups.

Prefer rules and space over cards. Cards add elevation and semantic meaning
(discrete independent unit). Not everything is a discrete unit.
Never nest cards in cards. Emphasis within cards: background tint,
border-top, or typographic weight.

## Color strategy ladder

Problem: palette commitment level.

Pick before choosing colors:

| Strategy | Coverage | Default for |
|---|---|---|
| Restrained | Tinted neutrals + accent <= 10% | Product UI |
| Committed | One saturated color at 30-60% | Brand pages |
| Full palette | 3-4 named roles | Data viz, campaigns |
| Drenched | Surface IS the color | Campaign heroes |

The "one accent at 10%" rule is Restrained only. Committed and above
exceed it intentionally. Within Restrained, never pure gray -- tint
toward accent hue.

## State communication

Problem: show system state without clutter.

| State | Method | Anti-pattern |
|---|---|---|
| Loading | Skeleton matching layout dimensions | Generic spinner |
| Empty | Composed design showing how to populate | "No data" gray text |
| Error | Inline near failure point | Modal alert |
| Success | Brief dismissible confirmation | Persistent banner |
| Transition | Crossfade or morph | Instant swap with CLS |

Skeletons must match loaded layout. Generic rectangles are noise.
Empty states are design surfaces. Explain what belongs here.
Don't celebrate routine operations.

## Progressive disclosure

Problem: manage complexity.

| Tier | Behavior |
|---|---|
| P0 | Always visible |
| P1 | Visible by default, collapsible |
| P2 | Behind a click/tap |
| P3 | Settings or advanced views |

Disclosure controls must be visible and labeled. A "..." menu is hiding,
not disclosing. Expanded content pushes down, does not overlay.
