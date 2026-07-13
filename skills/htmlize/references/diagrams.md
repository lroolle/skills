# Diagrams

Layout is computation. Placing nodes, routing edges around each
other, and keeping labels off the lines is exactly the work
language models do worst and layout engines do instantly. Past
roughly 8 nodes -- or any diagram where edges cross -- stop
hand-authoring SVG and render one.

The doctrine stays self-contained: the layout engine runs once,
at build time, on the agent's machine. The artifact receives a
plain inline `<svg>` -- selectable text, themeable, zero runtime
JS. The renderer is the agent's tool, never the file's dependency.

## The pipeline

1. **Author the source** in a diagram language (`.dot`, `.d2`,
   `.mmd`), styled with the baseline palette below.
2. **Render**: `scripts/render-diagram.sh --figure --caption
   "what the diagram shows" src.mmd` picks an engine, strips the
   XML prolog, remaps palette hexes inside embedded `<style>`
   blocks to `var(--token, #hex)` (themeable when inlined, still
   correct standalone thanks to the fallback), and writes a
   ready-to-paste `src.html` fragment: `<figure class="diagram">`
   with the SVG, a numbered caption, and the escaped source in a
   collapsed `<details>`.
3. **Inline the fragment** into the artifact. Keeping the source
   under the figure is not optional -- it is the editable form,
   the same reason markdown stays the source of truth for prose.

Without `--figure` the script emits just the cleaned `.svg`;
wrap and caption it yourself per the steps above.

## Renderers, in order of preference

| Engine | Get it | Strengths | Caveats |
|---|---|---|---|
| Graphviz `dot` | `apt install graphviz` / `brew install graphviz` | Tiny, instant, no browser. Colors pass through as plain `fill`/`stroke` attributes -- trivially dark-mode-able | Flowcharts, architecture, state machines only; no sequence diagrams |
| `d2` | `curl -fsSL https://d2lang.com/install.sh \| sh -s --` | Single binary, best-looking defaults, ~20KB output with subsetted fonts | Styles live in an embedded stylesheet -- harder to retheme than dot |
| Mermaid (`mmdc`) | `npm i -g @mermaid-js/mermaid-cli` | The syntax agents know best; sequence diagrams, ER, gantt | Needs Chrome via puppeteer: **fails on arm64 Linux** (no Chrome build). Use the Docker image there |
| Mermaid (Docker) | `docker run --rm -u $(id -u) -v "$PWD":/data minlag/mermaid-cli -i /data/in.mmd -o /data/out.svg -b transparent` | Multi-arch image; works where npx mmdc cannot | The mounted path must be visible to the Docker daemon (host path, not container-local `/tmp`) |
| None available | -- | Hand-author per patterns.md's inline-SVG rules | Small diagrams only; past ~8 nodes the result will not be worth shipping |

Pick by diagram type first: sequence diagrams and ER diagrams
need mermaid; flowcharts and architecture maps are best from
`dot` or `d2`. Installing `dot` takes seconds -- prefer a
ten-second install over a degraded hand-drawn diagram.

## Styling the source

Style at the source level with the baseline palette, so the
rendered SVG arrives calm instead of needing repair.

Graphviz:

```dot
digraph arch {
  rankdir=LR;                       // LR for pipelines, TB for hierarchies
  bgcolor="transparent";
  node [shape=box, style="rounded,filled", fillcolor="#ffffff",
        color="#e6e4de", fontname="Helvetica", fontsize=13,
        fontcolor="#1d1d20", margin="0.22,0.12"];
  edge [color="#5c5c66", fontname="Helvetica", fontsize=11,
        fontcolor="#5c5c66", arrowsize=0.7];

  // critical path gets the one accent
  orders -> queue [label="order.created", color="#1a6db0",
                   fontcolor="#1a6db0", penwidth=1.6];
}
```

Mermaid: render with `-b transparent` plus a config file
(`assets/mermaid-theme.json` in this skill) that sets
`theme: "base"` and maps `themeVariables` to the baseline palette
and system font stack. Pass `--svgId` a unique id per diagram --
mermaid scopes its embedded styles to the SVG id, and two
diagrams with the same id fight.

## Dark mode

Rendered SVGs carry light-palette hexes. Remap them in the
artifact's stylesheet -- presentation attributes lose to any CSS
rule, so no SVG surgery is needed:

```css
.diagram svg [fill="#ffffff"]   { fill: var(--surface); }
.diagram svg [fill="#faf9f7"]   { fill: var(--bg); }
.diagram svg [fill="#1d1d20"]   { fill: var(--ink); }     /* labels */
.diagram svg [fill="#5c5c66"]   { fill: var(--ink-2); }   /* arrowheads */
.diagram svg [stroke="#5c5c66"] { stroke: var(--ink-2); } /* edges */
.diagram svg [stroke="#e6e4de"] { stroke: var(--rule); }
.diagram svg [fill="#1a6db0"]   { fill: var(--accent); }
.diagram svg [stroke="#1a6db0"] { stroke: var(--accent); }
```

This covers `dot` output, whose colors are all presentation
attributes. Mermaid and `d2` put colors in an embedded `<style>`
block instead, where attribute selectors cannot reach --
`render-diagram.sh` rewrites those to `var(--token, #hex)` at
render time, so a script-rendered diagram needs no manual work.
Mermaid also hardcodes a few colors that ignore both the theme
config and the rewrite (`stroke="#666"` actor lines,
`fill="#eaeaea"` activation bars, `stroke="#000000"` arrowheads);
the template's remap block catches them -- without it, arrowheads
vanish in dark mode. Never ship a diagram that turns illegible
when the OS theme flips: check both themes, not just the one
your OS happens to be in.

## Taste rules

Unchanged from hand-authored SVG -- the engine does geometry, not
judgment:

- Color groups things; it does not decorate. 2-3 muted fills plus
  one accent on the critical path.
- Label every edge that is not obvious; an unlabeled arrow between
  two services is a guess the reader has to make.
- `rankdir=LR` for pipelines and data flow, `TB` for hierarchies
  and sequences.
- Past ~15 nodes, split into an overview diagram plus per-cluster
  detail diagrams. A hairball renders faster than it reads.
- A diagram that restates a list ("A -> B -> C", no branching) is
  a sentence, not a diagram. The gate applies to diagrams too.

## The CDN exception

On surfaces with a CDN allowlist (claude.ai artifacts), loading
mermaid.js at runtime and letting it render in the reader's
browser is a workable deliberate trade -- mermaid is on the
allowlist there. Everywhere else it is the worst option: ~2.8MB
of JS to do at view time, on every view, what `dot` does once at
build time -- and the file dies offline. Build-time rendering is
the default; say so in the artifact comment when you trade away
from it.
