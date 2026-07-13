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

The accent is blue, not violet — violet decoration is the first
thing the anti-slop check smashes. Dark-mode status colors
included.

```css
:root {
  --bg:       #faf9f7;
  --surface:  #ffffff;
  --ink:      #1d1d20;
  --ink-2:    #5c5c66;   /* secondary text */
  --rule:     #e6e4de;   /* borders, dividers */
  --accent:   #1a6db0;   /* links, the one highlight */
  --ok:       #166534;
  --warn:     #b45309;
  --bad:      #b91c1c;

  --serif: "Charter", "Iowan Old Style", Georgia, serif;
  --sans:  ui-sans-serif, system-ui, -apple-system, sans-serif;
  --mono:  ui-monospace, "SF Mono", Menlo, Consolas, monospace;
}

@media (prefers-color-scheme: dark) {
  :root {
    --bg:      #131316;
    --surface: #1c1c21;
    --ink:     #ececf0;
    --ink-2:   #9c9ca8;
    --rule:    #2c2c33;
    --accent:  #5aa3dd;
    /* Status colors need their own dark values -- the light ones
       fall below 3:1 contrast on this background */
    --ok:      #4ade80;
    --warn:    #fbbf24;
    --bad:     #f87171;
  }
}

/* Document baseline */
body {
  font: 17px/1.55 var(--serif);
  background: var(--bg);
  color: var(--ink);
  max-width: 72ch;
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

h1 { font-size: 1.9rem; line-height: 1.2; letter-spacing: -0.01em; }
h2 { font-size: 1.3rem; margin-top: 2.2em; }
h1, h2, h3 { text-wrap: balance; }  /* no widowed last word in headings */
code, pre { font-family: var(--mono); font-size: 0.92em; }
pre {
  background: var(--surface);
  border: 1px solid var(--rule);
  border-radius: 4px;
  padding: 1rem;
  overflow-x: auto;
}
table { border-collapse: collapse; width: 100%; }
th, td {
  text-align: left;
  vertical-align: top;
  padding: 0.5rem 0.75rem;
  border-bottom: 1px solid var(--rule);
}
/* Numeric columns: right-aligned tabular digits so magnitudes
   line up down the column. Units go in the header, not the cells. */
td.num, th.num {
  text-align: right;
  font-variant-numeric: tabular-nums;
  font-family: var(--sans);
}

@media (max-width: 700px) {
  body { margin: 1.5rem auto; }
  /* Any multi-column grid collapses to one column */
  .grid, .columns { grid-template-columns: 1fr; }
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

## What good looks like

A well-set technical book. Tufte's information density. A printed
RFC. gwern.net's long essays. The internal design doc people
actually forward to each other. Typography does the hierarchy,
color marks the exceptions, diagrams carry the structure, and
nothing moves unless the reader moved it.
