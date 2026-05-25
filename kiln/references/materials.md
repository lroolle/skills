# Materials

Parameterized palette systems. Each palette generates tokens from small
parameter sets. Material kits are named compositions across all palettes.

## Color system

OKLCH for perceptual uniformity and wide-gamut support.

### Parameters

| Param | Description |
|---|---|
| Seed hue | Identity color, 0-360deg |
| Neutral tint | warm (toward seed) / cool (away) / neutral |
| Strategy | restrained / committed / full / drenched |
| Chroma range | low (0.02-0.06) / medium (0.06-0.12) / high (0.12-0.20) |

### Token derivation

From seed hue + neutral tint:

```
-- Surfaces --
background:       L 97%  C 0.005  H seed
surface:          L 95%  C 0.008  H seed
surface-alt:      L 92%  C 0.010  H seed

-- Text --
foreground:       L 12%  C 0.005  H seed
foreground-muted: L 40%  C 0.005  H seed

-- Borders --
border:           L 88%  C 0.005  H seed
border-strong:    L 75%  C 0.008  H seed

-- Accent (chroma per strategy) --
accent:           L 55%  C [strategy]  H seed
accent-fg:        L 98%  C 0.005  H seed

-- Semantic (hue offsets) --
error:            H seed+150 (toward red)  C 0.15
warning:          H seed+60  (toward amber) C 0.12
success:          H seed-60  (toward green) C 0.10
```

### Dark mode derivation

Do not invert. Redesign:

```
-- Surfaces flip --
background:       L 10%  C 0.008  H seed
surface:          L 14%  C 0.010  H seed
surface-alt:      L 18%  C 0.012  H seed

-- Text flips --
foreground:       L 92%  C 0.005  H seed
foreground-muted: L 65%  C 0.005  H seed

-- Accent adjusts --
accent:           chroma * 0.85 (reduce to prevent halation)

-- Elevation via surface lightness, not shadows --
elevated:         L surface + 4%
```

## Type system

### Parameters

| Param | Description |
|---|---|
| Display face | Headlines: family + weight + tracking |
| Body face | Body copy: family + weight + leading |
| Mono face | Code/data: family + weight |
| Scale ratio | 1.25 / 1.333 / 1.5 |
| Base size | 1rem / 1.0625rem / 1.125rem |

### Token derivation

| Token | Size | Line-height | Weight |
|---|---|---|---|
| text-xs | base / ratio^2 | 1.4 | 400 |
| text-sm | base / ratio | 1.45 | 400 |
| text-base | base | leading | 400 |
| text-lg | base * ratio | 1.35 | 500 |
| text-xl | base * ratio^2 | 1.25 | 600 |
| text-2xl | base * ratio^3 | 1.15 | 700 |
| text-3xl | base * ratio^4 | 1.1 | 800 |

Fluid responsive via clamp():
```css
/* headlines compress 2:1 */
--text-3xl: clamp(1.75rem, 1rem + 2.5vw, 3.5rem);
/* body barely changes */
--text-base: clamp(1rem, 0.95rem + 0.25vw, 1.125rem);
```

### Pairing

Contrast on multiple axes:
- Serif + sans (structure contrast)
- Geometric + humanist (personality contrast)
- Condensed + wide (proportion contrast)

Never pair similar-but-not-identical faces. They create tension without
hierarchy. One family with weight/size contrast is often stronger than
two weak pairings.

System fonts (-apple-system, system-ui) are underrated: native feel,
instant load, high readability. Consider for apps where performance
matters more than personality.

## Spacing system

### Parameters

| Param | Description |
|---|---|
| Base unit | From body line-height (e.g., 24px at 16px/1.5) |
| Scale | [0.25, 0.5, 0.75, 1, 1.5, 2, 3, 4, 6, 8] |
| Density | 0.7 / 0.85 / 1.0 / 1.5 |

### Token derivation

space-{n} = base * scale[n] * density

At base=24px, density=1.0:
- space-1: 6px
- space-2: 12px
- space-4: 24px (1 baseline unit)
- space-8: 48px (2 units)
- space-12: 72px (3 units)
- space-24: 144px (6 units, section gap)

Section gaps: minimum 3x internal component spacing.
Same gap everywhere kills rhythm. Vary intentionally.

## Surface system

### Parameters

| Param | Values |
|---|---|
| Border weight | 0 / 1px / 2px |
| Border style | solid / none |
| Radius | 0 / 4px / 8px / 12px (pick max 2 values) |
| Elevation | flat / subtle / layered |
| Texture | none / grain / noise |

### Elevation rules

- flat: no shadows, surfaces differ by border or background only.
- subtle: one level, box-shadow 0.03-0.05 opacity, tinted to bg hue.
- layered: 2-3 levels, higher = more spread + lighter.
- If shadow is visible in isolation, it is too strong.
- Dark mode: elevation via surface lightness, not shadows.

## Imagery system

### Parameters

| Param | Values |
|---|---|
| Photography | none / desaturated / warm-toned / high-contrast / duotone |
| Illustration | none / line-art / geometric / editorial / icon-only |
| Icon set | phosphor / radix / lucide / custom |
| Icon weight | Standardize one weight across entire interface |
| Data viz | minimal / dense / editorial |
| Empty state | illustration / typography-only / subtle-icon |

Icon stroke weight must be consistent. Pick 1.5 or 2.0, commit.
Photography on dark backgrounds: filter: brightness(0.85-0.9).
Empty states are design surfaces, not error messages.

## Curated kits

### broadsheet

Editorial newsroom. BBC, FT, broadsheet on screen.

```
Color:      Seed 15deg warm red. Neutral: warm. Strategy: restrained.
Type:       Display: Georgia or Charter, 700, -0.02em.
            Body: system sans (-apple-system), 400, 1.6.
            Mono: Menlo. Scale: 1.333. Base: 1.0625rem.
Spacing:    Base: 24px. Density: 0.85.
Surface:    Border: 1px solid. Radius: 0. Elevation: flat.
Motion:     Mechanical. Micro: 80ms. Transition: 150ms. Entrance: 200ms.
Adaptation: Priority-based. Bottom tabs mobile. Headlines compress 2:1.
Imagery:    Photography: warm-toned editorial. Icons: phosphor regular.
            Data viz: minimal. Illustration: none.
```

### terminal

Code, monitoring, data-dense. Dark ground, monospace-forward.

```
Color:      Seed 120deg green. Neutral: cold. Strategy: restrained.
Type:       Display: none (same as body). Body: Geist Sans, 400, 1.5.
            Mono: Geist Mono, 400. Scale: 1.25. Base: 0.9375rem.
Spacing:    Base: 20px. Density: 0.75.
Surface:    Border: 1px solid. Radius: 0. Elevation: flat.
Motion:     Mechanical. Micro: 50ms. Transition: 100ms linear. Entrance: instant.
Adaptation: Density-first. Reduced motion default. Monospace numbers always.
Imagery:    Photography: none. Illustration: none. Icons: phosphor thin.
            Data viz: dense.
```

### warm-ground

Document, workspace. Paper warmth, humanist type.

```
Color:      Seed 40deg amber. Neutral: warm. Strategy: restrained.
Type:       Display: Atkinson Hyperlegible or system sans, 700, -0.01em.
            Body: same family, 400, 1.6. Mono: JetBrains Mono.
            Scale: 1.333. Base: 1rem.
Spacing:    Base: 24px. Density: 1.0.
Surface:    Border: 1px solid. Radius: 8px. Elevation: subtle (0.04).
Motion:     Snappy. Micro: 100ms. Transition: 200ms expo-out. Entrance: 300ms.
Adaptation: Content-priority. Dark mode: sepia-warm (#1C1917 base).
Imagery:    Photography: warm-toned. Illustration: line-art.
            Icons: phosphor regular. Data viz: minimal.
```

### cold-open

Developer tools, tech products. Precise, committed color.

```
Color:      Seed 220deg slate blue. Neutral: cool. Strategy: committed.
Type:       Display: Geist, 800, -0.04em. Body: Geist, 400, 1.5.
            Mono: Geist Mono. Scale: 1.333. Base: 1rem.
Spacing:    Base: 24px. Density: 1.0.
Surface:    Border: 0 (none). Radius: 12px. Elevation: layered.
Motion:     Snappy. Micro: 100ms. Transition: 200ms expo-out. Entrance: 250ms.
Adaptation: Container-responsive. Dark-first design.
Imagery:    Photography: none. Illustration: geometric.
            Icons: radix. Data viz: minimal.
```

### gallery

Museum, portfolio, Swiss precision. Achromatic, heavy type, generous air.

```
Color:      Seed 0deg achromatic. Neutral: true neutral. Strategy: restrained.
Type:       Display: Helvetica Neue or Suisse Intl, 900, -0.03em.
            Body: same, 400, 1.55. Mono: none. Scale: 1.5. Base: 1.125rem.
Spacing:    Base: 28px. Density: 1.5.
Surface:    Border: 0. Radius: 0. Elevation: flat.
Motion:     Deliberate. Micro: 150ms. Transition: 300ms. Entrance: 500ms.
Adaptation: Heavy scale compression (3:1 headlines). Single column tablet.
Imagery:    Photography: high-contrast B&W. Illustration: geometric.
            Icons: none (typography-only nav). Data viz: editorial.
```

### burnt-studio

Art, photography, creative studio. Warm saturation, tactile texture.

```
Color:      Seed 25deg terracotta. Neutral: warm. Strategy: drenched.
Type:       Display: serif (check zeitgeist, avoid saturated picks), 600, -0.02em.
            Body: system sans, 400, 1.6. Mono: Source Code Pro.
            Scale: 1.333. Base: 1.0625rem.
Spacing:    Base: 24px. Density: 1.0.
Surface:    Border: 0. Radius: 0. Elevation: flat.
            Texture: grain (noise overlay at 0.03 opacity).
Motion:     Deliberate. Micro: 120ms. Transition: 350ms. Entrance: 500ms.
Adaptation: Image-heavy responsive. Photography drives breakpoints.
Imagery:    Photography: warm-toned, slightly desaturated.
            Illustration: editorial. Icons: phosphor fill.
```
