# Style baseline

An ugly artifact is a net loss: it spent several times markdown's
tokens to produce something the reader trusts less. This file is
the default visual system for when the user has no design system
of their own, and the failure list that tells you an artifact
needs rebuilding.

The templates in [../assets/templates/](../assets/templates/)
are this baseline made executable -- start from one of them
rather than retyping the CSS below. This file is the why and the
retheming reference; the templates are the what. They ship
together: a change to one is a change to both.

## Documents vs tools

Two baselines, chosen by what the artifact is:

- **Documents** (plans, reports, explainers, reviews): serif
  body, 17px, 60-75ch measure, generous margins. Reads like a
  publication.
- **Tools** (editors, boards, tuners, pickers): sans body, 14px,
  full-width, dense. Reads like an instrument panel.

The most common style failure is using the airy document layout
for a tool (feels sluggish) or the dense tool layout for a
document (feels like a config screen).

## Baseline CSS

The accent is blue, not violet -- violet decoration is the first
thing the anti-slop check smashes. Dark-mode status colors
included. Three surface levels provide depth without shadows.

```css
:root {
  --bg:        #faf9f7;
  --surface:   #ffffff;
  --surface-2: #f5f4f0;   /* inset panels, inline code bg */
  --ink:       #1d1d20;
  --ink-2:     #5c5c66;   /* secondary text */
  --ink-3:     #8a8a96;   /* tertiary: labels, lang tags */
  --rule:      #e6e4de;   /* borders, dividers */
  --accent:    #1a6db0;   /* links, the one highlight */
  --ok:        #166534;
  --warn:      #b45309;
  --bad:       #b91c1c;

  --serif: "Charter", "Iowan Old Style", Georgia, serif;
  --sans:  ui-sans-serif, system-ui, -apple-system, sans-serif;
  --mono:  ui-monospace, "SF Mono", Menlo, Consolas, monospace;
}

@media (prefers-color-scheme: dark) {
  :root {
    --bg:        #131316;
    --surface:   #1c1c21;
    --surface-2: #222228;
    --ink:       #ececf0;
    --ink-2:     #9c9ca8;
    --ink-3:     #6c6c78;
    --rule:      #2c2c33;
    --accent:    #5aa3dd;
    --ok:        #4ade80;
    --warn:      #fbbf24;
    --bad:       #f87171;
  }
}

/* Document baseline */
body {
  font: 17px/1.6 var(--serif);
  background: var(--bg);
  color: var(--ink);
  max-width: calc(72ch + 16rem);
  margin: 3rem auto;
  padding: 0 1.25rem;
}

/* Tool baseline -- replaces the body rule above */
body.tool {
  font: 14px/1.45 var(--sans);
  max-width: none;
  margin: 0;
  padding: 1rem;
}

h1 { font-size: 2rem; line-height: 1.15; letter-spacing: -0.02em; }
h2 {
  font-size: 1.3rem; margin-top: 2.4em;
  padding-bottom: 0.4em;
  border-bottom: 1px solid var(--rule);
}
h3 { font-size: 1.05rem; margin-top: 1.8em; }
h1, h2, h3 { text-wrap: balance; }
```

### Code blocks

Monospace at 0.85em body with 1.55 line height. Inline code gets
a `--surface-2` pill. Block code shows an optional language label
top-right: `<span class="lang">go</span>` inside the `<pre>`.

```css
code { font-family: var(--mono); font-size: 0.88em; }
:not(pre) > code {
  background: var(--surface-2);
  padding: 0.15em 0.35em;
  border-radius: 3px;
}
pre {
  position: relative;
  font-family: var(--mono);
  font-size: 0.85em;
  line-height: 1.55;
  background: var(--surface);
  border: 1px solid var(--rule);
  border-radius: 5px;
  padding: 1rem 1.15rem;
  overflow-x: auto;
  tab-size: 4;
}
pre .lang {
  position: absolute; top: 0; right: 0;
  font-family: var(--sans);
  font-size: 0.7rem;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  color: var(--ink-3);
  padding: 0.3rem 0.65rem;
  user-select: none;
}
```

### Tables

Row hover with `--surface-2`. Header text is small sans with
slight tracking. Numeric columns right-aligned with tabular
digits -- units go in the header, not the cells.

```css
table { border-collapse: collapse; width: 100%; font-size: 0.95em; }
th, td {
  text-align: left; vertical-align: top;
  padding: 0.55rem 0.75rem;
  border-bottom: 1px solid var(--rule);
}
th {
  font-family: var(--sans); font-size: 0.8rem;
  font-weight: 600; letter-spacing: 0.02em; color: var(--ink-2);
}
tr:hover td { background: var(--surface-2); }
td.num, th.num {
  text-align: right;
  font-variant-numeric: tabular-nums;
  font-family: var(--sans);
}
```

### KPI stat tiles

For 2-4 headline numbers at the top of a section. Big number,
uppercase label, optional delta. The `.accent` modifier colors the
top border; without it the border is `--rule`. Do not use for
things that are not metrics -- "3 files reviewed" in a stat tile
is dashboard furniture and the slop list catches it.

```css
.kpi-row { display: flex; gap: 1rem; margin: 1.5em 0; }
.kpi {
  flex: 1;
  padding: 1rem 1.15rem;
  border-top: 3px solid var(--rule);
  background: var(--surface);
  border-radius: 0 0 4px 4px;
}
.kpi-value {
  font-family: var(--sans);
  font-size: 1.9rem; font-weight: 700;
  line-height: 1.1; letter-spacing: -0.02em;
  font-variant-numeric: tabular-nums;
}
.kpi-label {
  font-family: var(--sans);
  font-size: 0.72rem; font-weight: 600;
  letter-spacing: 0.1em; text-transform: uppercase;
  color: var(--ink-2); margin-top: 0.35rem;
}
.kpi-delta { font-family: var(--sans); font-size: 0.8rem; margin-top: 0.25rem; }
.kpi-delta.up   { color: var(--ok); }
.kpi-delta.down { color: var(--bad); }
.kpi-delta.flat { color: var(--ink-3); }
.kpi.accent     { border-top-color: var(--accent); }
```

### Grid utilities

Three layout grids for side-by-side content. `.grid-asym` uses
1.2fr/0.8fr so columns are not equal-width -- equal tiles are a
common AI-output signature.

```css
.grid-2    { display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; }
.grid-3    { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.5rem; }
.grid-asym { display: grid; grid-template-columns: 1.2fr 0.8fr; gap: 1.5rem; }
```

### Diagram viewer

The document and site templates contain the complete viewer baseline;
reuse it rather than restyling controls per diagram. Its visual hierarchy
is intentionally quiet: one neutral toolbar attached to the viewport,
compact native controls, a tabular percentage, and Full at the far edge.
The diagram remains the object; the controls never become a dashboard.

Keep the unenhanced rule (`figure.diagram > svg { max-width: 100%;
height: auto; }`) outside enhancement classes. JavaScript wraps the SVG
only after it has built the complete control surface, so a script failure
leaves a readable fitted figure rather than half an interface.

Fullscreen is a reading mode, not motion: no scale transition, backdrop
animation, or decorative dimming. Preserve the original figure height
with a placeholder, lock background scroll, and use a solid `--bg`
surface. In print, hide the toolbar and force the SVG to fitted width.
The behavioral contract and keyboard map live in
[diagrams.md](diagrams.md).

### Responsive

All multi-column grids collapse to one column under 900px.
KPI tiles wrap at 50% width, then 100% under 500px.

```css
@media (max-width: 900px) {
  .grid-2, .grid-3, .grid-asym { grid-template-columns: 1fr; }
  .kpi-row { flex-wrap: wrap; }
  .kpi { min-width: calc(50% - 0.5rem); }
}
@media (max-width: 500px) {
  .kpi { min-width: 100%; }
}
@media print {
  body { max-width: none; margin: 0; font-size: 11pt; }
  .no-print { display: none; }
}
```

Collapsed `<details>` cannot be expanded for print from CSS --
`open` is an HTML attribute, and closed details hide their
content inside the UA shadow tree where author styles cannot
reach. Use print event handlers:

```js
addEventListener('beforeprint', () =>
  document.querySelectorAll('details:not([open])').forEach(d => {
    d.dataset.autoOpened = '';
    d.open = true;
  }));
addEventListener('afterprint', () =>
  document.querySelectorAll('details[data-auto-opened]').forEach(d => {
    d.open = false;
    delete d.dataset.autoOpened;
  }));
```

One accent color. Status colors (`--ok`, `--warn`, `--bad`)
appear only on status. If you want a second accent, you want a
diagram instead.

## The slop list

Markers of machine output -- each one says nobody looked at this
page before shipping it:

- Hero banner wearing a gradient wash
- Emoji decorating section headers
- Rows of cards where a table was the honest structure
- An indigo-to-violet palette attached to no meaning
- Frosted glass, floating blobs, ambient background motion
- Every element centered
- Big-number stat cards for things that are not metrics ("3 files reviewed")
- A fake navbar with a logo slot
- Empty image placeholders waiting for stock photos

The repair is structural, not cosmetic: swap decoration for
typography, cards for tables, the hero for a title and one
framing sentence. A page showing three or more of these markers
gets regenerated from the baseline, not sanded down.

## Matching an existing design system

When the artifact belongs to a project with a real visual
identity, do not invent one:

1. Read the project's tokens -- Tailwind config, CSS variables,
   `theme.ts`, design token files.
2. Map them onto the `:root` block above (background, ink,
   accent, fonts). Brand fonts do not survive self-containment --
   no font files, no font CDN -- so map to the nearest system
   stack and note the substitution.
3. Keep the baseline's structure (measure, spacing, hierarchy)
   even when adopting the project's colors and type.

For repeat use, generate a `design-system.html` reference sheet
once -- swatches with token names, type scale, spacing -- and
read it before each future artifact in that project.

## Motion in artifacts

Artifacts are documents and tools, not products. The budget:
150-250ms ease-out transitions on interactive elements (hover,
expand, drag feedback), and nothing else. No entrance animations,
no scroll effects, no stagger. If the artifact's subject is
motion (prototyping an animation), that is animate-it's
territory -- use its curves and durations.

## Navigation

Documents use a right-side sticky TOC -- it stays visible as the
reader scrolls without pushing content off-center. Active section
highlighting via IntersectionObserver: the current heading gets
an accent left-border and color. On mobile (<900px), the TOC
collapses above the content as a flat list. The TOC label is
small-caps uppercase: "Contents".

## Endmark

An endmark (&#8718; or similar) right-aligned at the bottom of the
last section signals editorial closure -- the document is complete,
not truncated. Low opacity, tertiary color. Optional but preferred
for long documents.

## What good looks like

A well-set technical book. Tufte's information density. A printed
RFC. gwern.net's long essays. The internal design doc people
actually forward to each other. Typography does the hierarchy,
color marks the exceptions, diagrams carry the structure, and
nothing moves unless the reader moved it.
