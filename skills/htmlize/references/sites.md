# Technical briefing sites

Load this reference only in site mode. A briefing site is a finite,
navigable explanation of one system or decision. It is not a chopped-up
essay, a miniature docs platform, or a knowledge base.

## Product model

The unit of design is the reader's question. The unit of delivery is the
bundle. The unit of coherence is the thesis.

This distinction prevents three common failures:

- Treating HTML as the product produces a polished shell with no reading
  model.
- Treating files as the product produces a directory whose pages do not
  add up to an argument.
- Treating the site as an application produces routing, state, and build
  infrastructure that the explanation never needed.

The chosen architecture is deliberately boring: real HTML pages, shared
local CSS and JS, relative links, editable sources, no runtime fetch, no
framework, no client router. It opens from `file://`, publishes as a
static bundle, prints, deep-links, and keeps working when JavaScript is
blocked.

## Alternatives considered

| Model | Advantage | Failure at this job | Verdict |
|---|---|---|---|
| One long HTML file | Portable; no cross-file drift | Overview, decisions, mechanics, and risks compete in one scroll | Keep for one-question artifacts |
| Single-page app with tabs/routes | One shell; app-like transitions | Essential navigation depends on JS; history, print, and file viewing become work | Reject |
| Generated docs framework | Strong navigation and authoring | Dependencies, build chain, themes, and configuration outweigh a finite briefing | Route maintained docs elsewhere |
| Fully self-contained HTML per page | Every page travels alone | CSS/JS duplication drifts and inflates every revision | Reject for sites |
| Static bundle with shared assets | Real pages, deep links, offline, small runtime | Repeated nav can drift | Choose; `site.json` + checker control the drift |

## Default question map

Use this as a diagnostic, not a quota. Delete or merge any page that
cannot earn its question.

| Page | Reader question | Must contain |
|---|---|---|
| `index.html` / Overview | What is this system, why does it exist, and what resulted? | Problem, thesis, boundary, system-at-a-glance, named reading paths |
| `architecture.html` / Architecture | What are the major parts and how do they relate? | Context boundary, component responsibilities, relationship diagram, interfaces |
| `mechanics.html` / Mechanics | How does it behave at runtime? | Critical flow, state/data lifecycle, invariants, implementation details |
| `decisions.html` / Decisions | Why this design instead of the alternatives? | Decision drivers, genuinely different options, selection, rejected options, tradeoffs |
| `risks.html` / Risks | Where does it fail and how will we know? | Failure modes, edge cases, security/operational traps, mitigations, verification limits |

Common earned additions:

- `evidence.html` when measurements, experiments, or source analysis are
  large enough to interrupt the system explanation;
- `reference.html` when implementers need exact schemas, APIs, state
  tables, or configuration that other readers can skip;
- `migration.html` when rollout and coexistence are a design problem of
  their own.

Do not add a Conclusions page that repeats Overview. Put the final design
and its limits in the first viewport, then let later pages prove it.

## Split and merge tests

Split a page when all four are true:

1. it answers a question distinct from its neighbors;
2. a reader would share a link directly to it;
3. it has its own diagram, decision, table, or flow rather than only
   prose continuation; and
4. removing it from the parent makes the parent's argument clearer.

Merge pages when any of these are true:

- one page is under roughly two substantive sections;
- the second page begins by reconstructing the first page's context;
- readers cannot predict the distinction from the nav labels;
- the pages must be read consecutively to make sense;
- a page exists only to match the template.

Three strong pages beat seven skeletal ones.

## Bundle anatomy

The template uses a flat page level so every page shares the same
relative paths. Keep it flat unless the site has genuinely nested
domains; a five-page briefing does not.

```text
system-briefing/
  index.html
  architecture.html
  mechanics.html
  decisions.html
  risks.html
  site.json              canonical title, purpose, page order/questions
  assets/
    site.css              shared visual system and print rules
    diagram-viewer.js     zoom, pan, fit, and fullscreen enhancement
    site.js               page-local contents and print-detail handling
  sources/
    brief.md              editable reasoning source
    diagrams/             .dot, .d2, or .mmd when diagrams exist
```

`site.json` is the map, not a runtime database. Browsers opening local
files cannot reliably `fetch()` adjacent JSON, so each page contains its
plain HTML nav. The checker compares every nav with the manifest. This
trades a small amount of repeated markup for zero runtime dependency and
mechanically catches drift.

Example manifest:

```json
{
  "title": "Queue architecture",
  "purpose": "Explain the selected queue design well enough to review and implement it.",
  "source": "sources/brief.md",
  "pages": [
    {"file": "index.html", "label": "Overview", "question": "What was built and why?"},
    {"file": "architecture.html", "label": "Architecture", "question": "How do the parts relate?"},
    {"file": "mechanics.html", "label": "Mechanics", "question": "How does it behave at runtime?"},
    {"file": "decisions.html", "label": "Decisions", "question": "Why this design?"},
    {"file": "risks.html", "label": "Risks", "question": "Where can it fail?"}
  ]
}
```

Filenames stay stable when labels improve. A URL is an interface; do not
rename it for typographic polish.

## Overview contract

The home page is not a table of contents. Its first viewport must answer:

- What problem exists?
- What system is inside the boundary?
- What is the thesis or selected design?
- What should this reader do next?

Then show one system-at-a-glance diagram or component map and two or
three named reading paths. Examples:

- **Review the design:** Overview -> Decisions -> Risks.
- **Implement the system:** Architecture -> Mechanics -> Reference.
- **Verify the claims:** Evidence -> Risks.

Paths are not wizards. They are ordinary links that reveal the site's
shape and let readers self-select.

## Page anatomy

Every page repeats a small, stable shell:

1. skip link;
2. site title and primary nav;
3. page eyebrow (the question), `h1`, and one-sentence answer;
4. main narrative with a local contents list when it has 3+ sections;
5. evidence and source links beside the claims they support;
6. previous/next links that state what the destination adds;
7. provenance footer.

The first paragraph gives the answer, not scene-setting. A reader who
only skims page titles, leads, diagrams, captions, decision statements,
and risk labels should reconstruct the design accurately.

Use one `h1` per page. `h2` divides the page's answer; `h3` divides an
`h2`. Do not use heading levels to obtain a font size.

## Navigation model

Primary navigation answers "which question am I asking?" Keep its order
stable and mark the current page with `aria-current="page"`. Local
contents answers "where am I inside this answer?" It is generated from
`h2` elements as an enhancement; the narrative remains readable without
it.

Cross-links carry intent:

- weak: `Learn more`
- strong: `See why polling was rejected`

A link label should still make sense when read alone by a screen reader.
Do not open internal links in new tabs. External evidence may open in the
same tab; the reader's browser already provides a new-tab command.

## Interaction budget

A briefing is a reading system, not an app. The shared script may:

- build and highlight the page-local table of contents;
- open collapsed detail for print and restore it afterward;
- enhance inline SVG diagrams with zoom, pan, fit, and fullscreen.

It should not fetch content, hide primary pages behind tabs, remember
reader state, animate page transitions, or synthesize navigation from
JSON at runtime. Every essential sentence and link ships in HTML.

### Diagram inspection

Enhance each direct `figure.diagram > svg` independently. Controls are
created without IDs, so multiple figures do not collide:

- minus / plus, 50%-500% in 25% steps;
- labeled range and percentage output;
- Fit returns to 100% and resets both scroll axes;
- Full moves the figure into a viewport-filling layer without cloning
  the SVG or changing the surrounding page's geometry;
- zoom preserves the inspected center; Ctrl/Command-wheel uses the same
  scale model;
- `+`, `-`, `0`, `F`, and Escape work while the figure is active;
- fullscreen locks body scroll, traps focus, and returns focus to Full;
- print closes fullscreen, hides controls, and fits every diagram.

The unenhanced SVG remains fitted and selectable. The viewer owns viewing
only; `render-diagram.sh` continues to own build-time geometry.

## Source and evidence

`sources/brief.md` is the editable reasoning spine, not a verbatim dump
of the HTML. It records:

- purpose, reader, thesis, and boundary;
- page map and the question each page answers;
- claims with citations or repository paths;
- alternatives and why they lost;
- diagrams in editable source form;
- measurements with commands, environment, date, units, and spread.

Keep private evidence private. A source included in the bundle will be
published when the bundle is published. Link to sensitive local evidence
in working notes; do not copy it into a shareable site.

## Completion tests

Mechanical:

```bash
python3 scripts/check-site.py path/to/system-briefing
```

Human:

1. Read only Overview. Can you state the system, purpose, and selected
   design?
2. Follow the reviewer path. Can you find the strongest rejected option
   and the largest accepted risk?
3. Follow the implementer path. Can you name every component boundary,
   interface, invariant, and failure response?
4. Disable JavaScript. Can you read, navigate, and inspect fitted
   diagrams?
5. At 375px, dark mode, keyboard only, and print preview, does the order
   remain correct and every control remain reachable or intentionally
   absent?

The checker proves integrity. These tests judge explanation.
