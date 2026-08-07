# Material kits

A material is a small parameter set that generates all the tokens: color
seed, type pairing, radius, density, surface treatment, motion. Kits are
*starting points*, not law — mix dimensions across them, re-seed the hue,
swap the type. What you may NOT do is inherit a kit's DESIGN.md unchanged
while shipping a different look: rewrite the contract in the same commit.

Deriving concrete tokens from a kit (OKLCH ramps, type scale, spacing) is
kiln's `kit` command — this file names the kits and their parameters;
kiln computes the values. `assets/bisque.css` is one fully-derived kit
you can read end to end.

## Derivation rules (the invariants every kit obeys)

- **OKLCH, one seed hue.** Surfaces, text, borders, and accent all carry a
  trace of the seed (chroma 0.005–0.015 on neutrals). Both light and dark
  derive from it — dark mode is a *redesign*, not an inversion, and never
  drops to chroma 0 or pure black/white.
- **Semantic states are hue offsets from the seed**, held in tokens
  (`--destructive`, `--chart-*`). App code never reaches for a raw
  palette class.
- **Radius is decided before the first component.** Pick one value; the
  scale (sm/md/lg) derives from it. One corner language per surface.
- **Structure before shadow.** Prefer 1px rules and background steps;
  shadow only where elevation carries meaning, tinted to the bg hue.
- **Type pairs on an axis** (serif×sans, geometric×humanist, or one
  family across weights). Never two similar-but-not-identical faces. Check
  the font is not a saturated reflex (see catalog.md).
- **One icon set, one weight.** Committed, not mixed.

## The kits

Each line: seed · type · radius · density · surface · motion · territory.

### bisque — warm clay, fired but unglazed (the worked example)

Warm, precise, structural, nothing to hide behind. Fully derived in
`assets/bisque.css`.

```
Color:   Seed hue 55-60 warm clay. Neutral: warm. Strategy: committed.
         Accent ember, oklch(0.54 0.15 40). Both themes from one seed.
Type:    IBM Plex Sans (body/UI) + IBM Plex Mono (data/numerals).
         No display serif. CJK: Noto Sans SC harmonizes.
Radius:  0.25rem, one corner language.
Surface: 1px ruled borders + background steps. Shadow only for overlays.
Density: 1.0+ on product surfaces; brand may breathe.
Motion:  Snappy 120-180ms, opacity/transform only. No urgency devices.
Territory: SaaS chassis, developer products, anything that refuses slop.
```

### broadsheet — editorial newsroom

```
Color:   Seed 15deg warm red. Neutral: warm. Strategy: restrained.
Type:    Display Georgia/Charter 700 -0.02em. Body system sans 1.6. Mono Menlo.
Radius:  0. Surface: 1px solid, flat. Density: 0.85.
Motion:  Mechanical. 80/150/200ms.
Territory: BBC, FT, editorial, long-form.
```

### terminal — code, monitoring, data-dense

```
Color:   Seed 120deg green. Neutral: cold. Strategy: restrained.
Type:    Body Geist Sans 1.5. Mono Geist Mono. Scale 1.25. Base 0.9375rem.
Radius:  0. Surface: 1px solid, flat. Density: 0.75. Mono numerals always.
Motion:  Mechanical. 50/100ms linear. Reduced motion default.
Territory: dashboards, logs, monitoring, ops.
```

### warm-ground — document, workspace

```
Color:   Seed 40deg amber. Neutral: warm. Strategy: restrained.
Type:    Atkinson Hyperlegible/system sans 700. Body 1.6. Mono JetBrains Mono.
Radius:  8px. Surface: 1px, subtle elevation (0.04). Density: 1.0.
Motion:  Snappy. 100/200ms expo-out. Dark: sepia-warm.
Territory: Notion-like, docs, knowledge tools.
```

### cold-open — developer tools, tech products

```
Color:   Seed 220deg slate. Neutral: cool. Strategy: committed.
Type:    Geist 800 -0.04em display. Body Geist 1.5. Mono Geist Mono.
Radius:  12px. Surface: borderless, layered elevation. Density: 1.0.
Motion:  Snappy. 100/200ms expo-out. Dark-first.
Territory: Linear-like, dev tools, technical SaaS.
```

### gallery — museum, portfolio, Swiss precision

```
Color:   Seed 0deg achromatic. Neutral: true. Strategy: restrained.
Type:    Helvetica Neue/Suisse 900 -0.03em. Body 1.55. Scale 1.5. Base 1.125rem.
Radius:  0. Surface: borderless, flat. Density: 1.5 (generous air).
Motion:  Deliberate. 150/300/500ms. Headlines compress 3:1.
Territory: portfolios, museums, high-craft brand.
```

### burnt-studio — art, photography, creative studio

```
Color:   Seed 25deg terracotta. Neutral: warm. Strategy: drenched.
Type:    Display serif (check catalog, avoid saturated) 600. Body system 1.6.
Radius:  0. Surface: flat, grain texture (noise 0.03). Density: 1.0.
Motion:  Deliberate. 120/350/500ms.
Territory: art, photography, editorial-creative.
```

## Choosing

Match the kit to the *primary task and territory*, then re-seed for
identity. A product surface wants density and restraint (terminal,
broadsheet, bisque); a brand surface can spend expressiveness (gallery,
cold-open, burnt-studio). When two kits fit, pick the one whose default
density matches the task, not the one that photographs better — that
choice is the first taste decision, and it is a `taste` verdict if
contested.
