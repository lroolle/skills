---
name: kiln
description: >-
  Precision UX design instrument: perceptual principles, composable
  patterns, parameterized material kits, anti-AI-slop detection.
  Fires on three branches: designing or restyling any frontend
  surface (layout, typography, color, spacing, responsive, dark
  mode, accessibility); auditing or critiquing an existing
  interface; and rescuing output that looks generic or AI-made
  ("make it look better", "needs more taste"). Animation design
  decisions live here (motion.md); implementing the animation is
  animate-it's job.
---

# Kiln

Raw requirements in, coherent interfaces out. Like ceramic firing: the
process is deliberate, the quality control is built in, and underfired
pieces get smashed.

Generates and diagnoses. Both modes use the same layer stack.

## Architecture

Four layers, ordered by durability:

| Layer | Contains | Updates |
|---|---|---|
| L0 Principles | Perceptual and cognitive invariants | Never |
| L1 Patterns | Composable structural building blocks | Rarely |
| L2 Materials | Parameterized palette systems + kits | Per project |
| L3 Templates | Page recipes (pattern + material compositions) | Per aesthetic |

Cross-cutting: anti-patterns split into **permanent** (below) and
**zeitgeist** ([versioned, dated](references/zeitgeist.md)).

## L0: Principles

Human perception and cognition. These constrain every downstream decision.

### Preattentive channels

Color hue, size, orientation, and motion process in <250ms without effort.
These are hierarchy tools. Using them on non-priority elements is noise.

### Gestalt grouping

Proximity > similarity > continuity > closure. Whitespace groups faster
than borders. Borders faster than color. Whitespace is the primary
structural tool, not card components.

### Weber's law

Perceived difference is proportional to magnitude. 2px between 10px and
12px is obvious; between 40px and 42px invisible. Modular type scales use
ratios (1.25x, 1.333x), not fixed increments (+2px).

### Saccadic fixation

Eyes jump between fixation points. Fixation edges must be predictable.
Left-aligned text has a consistent edge; centered text forces the eye to
search each line start. Body text: left-aligned unless structurally
justified.

### Working memory

4 +/- 1 chunks. Navigation ceiling: 7 items. Dashboard with 12
undifferentiated metrics: unusable. Group before detail.

### Signal-to-noise

Every element is signal (serves comprehension) or noise. A page feels
clean or cluttered based on this ratio, not absolute content volume.
Dense can be clean. Sparse can be cluttered.

### Figure-ground

The eye resolves foreground/background before parsing content. Ambiguous
separation (low contrast, competing layers, no focal point) creates
anxiety before the user reads anything.

### Constraint breeds identity

Fewer choices made deliberately create more character than many choices
by default. A constrained palette reads as intentional. A diverse palette
reads as accidental.

## Permanent anti-patterns

Structural failures. Match-and-refuse. These will not expire.

### Convergence signal

If someone could guess the font, color, and layout from the domain name
alone, it is the first training-data reflex. Rework until the answer is
not obvious from the category. Then check: is the ALTERNATIVE also
predictable? ("AI tool that avoids purple -> editorial serif" is the
second-order reflex.)

### Container inception

Cards in cards. Modals on modals. Each container layer adds visual weight
and cognitive overhead. Flatten. Use whitespace, borders, or background
tint for emphasis.

### Flat type hierarchy

Heading sizes too close (14/15/16/18px). If squinting makes two levels
indistinguishable, merge or increase ratio. Minimum 1.25x between adjacent
levels.

### Side-stripe accent

border-left/right > 1px as colored accent on cards, alerts, list items.
Use full borders, background tints, or nothing.

### Gradient text

background-clip: text with gradient. Decorative, never meaningful, harder
to read. Single solid color.

### Shadow inflation

If everything floats, nothing does. Shadow only when elevation communicates
hierarchy. Tint to background hue. Never pure black shadow.

### Modal-first

Modals interrupt. Exhaust inline expansion, progressive disclosure, and
slide-over alternatives first.

### Decoration without information

Gradient backgrounds, animated meshes, glassmorphism, geometric patterns
that add weight without aiding comprehension. Every decorative element
must answer: what does this help the user understand?

### Pure black / pure white

Never #000000 or #FFFFFF. Pure black creates halation. Tint neutrals
toward brand hue (OKLCH chroma 0.005-0.01). Off-black L 8-12%, off-white
L 96-98%.

### Emoji in UI

Emoji in headings, buttons, labels, or navigation degrades perceived
quality. Use icons from a consistent set at standardized weight, or
nothing.

## Material kits

Named parameter sets. Not hardcoded values. Full specs in
[materials.md](references/materials.md).

| Kit | Color seed | Type | Density | Surface | Motion | Territory |
|---|---|---|---|---|---|---|
| broadsheet | 15deg red, restrained | serif display + sans body | 0.85 | ruled 1px, 0 radius | mechanical | BBC, FT, editorial |
| terminal | 120deg green, restrained | mono + sans, 1.25 scale | 0.75 | ruled 1px, 0 radius | instant | code, monitoring |
| warm-ground | 40deg amber, restrained | humanist sans, 1.333 | 1.0 | soft 1px, 8px radius | snappy | Notion, document |
| cold-open | 220deg slate, committed | geometric sans, tight | 1.0 | floating, 12px radius | snappy | Linear, dev tools |
| gallery | 0deg achromatic, restrained | heavy swiss, 1.5 scale | 1.5 | flat, no borders | deliberate | museum, portfolio |
| burnt-studio | 25deg terracotta, drenched | display serif + mono | 1.0 | grain texture, 0 radius | deliberate | art, photography |

Kits are starting points. Mix palette dimensions across kits: broadsheet
type with terminal density with warm-ground surfaces. The system handles
composition.

## Commands

| Command | Mode | What it does |
|---|---|---|
| `craft [target]` | Generate | Design/redesign using full layer stack |
| `audit [target]` | Diagnose | Evaluate against all layers, report by layer |
| `kit [name]` | Configure | Load a material kit, show derived values |

### craft

1. Confirm target surface (page, component, app shell) and material
   kit. If no kit specified and no aesthetic described, ask.
2. Load [patterns.md](references/patterns.md) for structural decisions.
3. Load [zeitgeist.md](references/zeitgeist.md) for current saturation bans.
4. Load [motion.md](references/motion.md) if animations needed.
5. Load [adaptation.md](references/adaptation.md) if responsive/dark/a11y needed.
6. Generate working code with committed design choices.
7. Self-audit against permanent anti-patterns before presenting.

Output: production-grade code in the project's framework. Every design
choice traces to a principle, pattern, or material parameter.

### audit

1. Read target files or screenshot.
2. Check L0 principles (hierarchy, grouping, signal-to-noise).
3. Check permanent anti-patterns (match-and-refuse).
4. Check [zeitgeist.md](references/zeitgeist.md) temporal bans.
5. Check material consistency if a kit is loaded.

Output: problem list by layer. Each identifies whether the rule is
permanent (structural) or temporal (zeitgeist). Temporal problems include
the expiry context.

### kit

1. Load [materials.md](references/materials.md) for kit specification.
2. Derive concrete tokens from parameters (OKLCH colors, type stacks,
   spacing scale, surface tokens).
3. Present the derived system for confirmation or adjustment.

## References

| File | Load when |
|---|---|
| [patterns.md](references/patterns.md) | Any craft or structural audit |
| [materials.md](references/materials.md) | Loading or composing material kits |
| [motion.md](references/motion.md) | Designing animations, transitions, interactions |
| [adaptation.md](references/adaptation.md) | Responsive, dark mode, a11y, CJK, print |
| [zeitgeist.md](references/zeitgeist.md) | Any craft or audit (temporal ban check) |
