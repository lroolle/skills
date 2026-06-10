# Artifact patterns

Layout guidance per shape. Each pattern names what is load-bearing
-- the element that makes the artifact worth its tokens -- and the
mistake that most often ruins it.

## Exploration grid

For "show me N ways to do this" -- code approaches, visual
directions, naming candidates, architecture options.

Layout: CSS grid of option cards, 2-3 columns desktop, one column
mobile. Every card has the same skeleton so the eye can diff:
name, one-line thesis, the distinguishing trade-off, a sketch
(code snippet, wireframe, or mini-diagram).

Load-bearing: the options must differ on a real axis, and each
card must say which axis. A grid of recolorings of one idea is
decoration pretending to be exploration.

Mistakes:
- Unlabeled trade-offs. "Option C" with no cost statement forces
  the reader to reverse-engineer your thinking.
- A recommendation hidden or missing. Highlight the recommended
  card and say why -- refusing to commit wastes the comparison.
- Cards with different skeletons. If one card has a code sample
  and another has prose, the reader cannot compare.

## Plan document

For implementation plans, specs, RFCs. The artifact people are
least likely to read in markdown and most likely to need.

Layout: sticky table of contents (sidebar on desktop, collapsed
top bar on mobile). Sections: context, the plan itself with
phases, data flow as an inline SVG diagram, key code snippets
annotated, a risk table, and a "not doing" section -- what was
considered and cut, with one line each on why.

Load-bearing: the "not doing" section. Plans fail in review when
readers re-litigate options the author already rejected silently.
Showing the cut options closes those threads.

Mistakes:
- A wall of phases with no diagram. If the plan has data flow,
  draw the flow.
- Code snippets pasted without annotation. Each snippet earns its
  place by having a margin note saying what to look at.
- Length without navigation. Past two screens, a plan needs the
  TOC and jump links or it reads worse than the markdown it
  replaced.

## Code review board

For PR review, PR explainers, "explain this code path,"
subsystem maps.

Layout: file-by-file sections. Each section renders the actual
diff -- monospace, green/red line backgrounds, line numbers --
with findings attached to the lines they are about, in the
margin. Findings carry a severity (blocker / question / nit) as
both color and label, legend at the top. The summary verdict
goes in the first viewport, not at the bottom.

For "explain this code" rather than "review this diff": replace
the diff with the call flow. An SVG flowchart of the path through
the modules, with the 3-5 key functions rendered as annotated
snippets below it, in call order.

Load-bearing: the rendered diff with inline annotations. The
entire advantage over markdown is that position and color carry
the review -- a finding floating in prose detached from its line
is just a slower comment thread.

Mistakes:
- Re-stating the diff in prose instead of rendering it.
- Severity colors without a legend, or color as the only signal
  -- pair color with a label for accessibility and printing.
- Burying the verdict. The reviewer wants approve/block in the
  first five seconds.

## Report / explainer

For status reports, incident reports, research syntheses, "I
don't understand how X works."

Layout for status/incident: headline state at top (green/amber/
red, with words not just color), then a timeline rendered as a
vertical line with event nodes, then detail sections that
collapse. Incident reports add: impact statement, root cause as
a diagram if the chain has more than two links, action items as
a table with owners.

Layout for explainers: the concept as an inline SVG diagram
first, then the 3-4 critical code snippets annotated, then a
"gotchas" section. Optimize for someone reading once -- linear,
no tabs, generous headings.

Numeric series -- benchmarks, latency curves, cost over time --
get a hand-rolled inline SVG chart: real axes, labeled ticks,
one series color plus the accent for the anomaly the chart
exists to show. When the reader needs exact values, a table
beats a chart; when they need both, render both with the table
collapsed.

Load-bearing: the diagram. An explainer without a diagram is a
blog post; the reason to make HTML is to show the mechanism.

Mistakes:
- Stats cards for things that are not stats ("4 files changed"
  in a giant card). Dashboard furniture signals slop.
- Collapsing the wrong things. Detail collapses; the narrative
  spine stays visible.
- Timeline as a bulleted list. If it is time, draw time.

## Arrow-key deck

For presenting to a room. One `<section>` per slide, JS under 20
lines: left/right arrows, slide counter, that is all.

Layout: one idea per slide, type large enough to read from the
back (body 28px+), diagrams over bullets. Final slide is the
summary someone photographs.

Load-bearing: restraint. The deck format earns nothing if each
slide is a document.

Mistakes:
- Slide transitions, progress animations, speaker-note systems.
  Twenty lines of JS is the budget.
- Bullets that should be a diagram.

## Inline SVG diagram

For flowcharts, architecture maps, sequence diagrams, state
machines -- standalone or embedded in other shapes.

Rules:
- Real `<svg>` elements -- `<rect>`, `<path>`, `<text>`, `<g>` --
  not an embedded image. The reader should be able to copy label
  text.
- SVG text does not wrap. Two options: size every shape from its
  label length (roughly 8px per character at 14px type, plus
  16px padding each side), or use `<foreignObject>` with an HTML
  div for real wrapping. Prefer `<foreignObject>` for long or
  variable labels in inline SVG; if the diagram is likely to be
  extracted as a standalone SVG or image, break lines manually
  with `<tspan>` instead -- `<foreignObject>` content vanishes
  when SVG is rasterized or embedded via `<img>`.
- Orthogonal connectors with arrowheads (`<marker>`). Label every
  edge that is not obvious.
- Lay out left-to-right for pipelines, top-to-bottom for
  hierarchies and sequences.
- Color groups things; it does not decorate. A palette of 2-3
  muted fills plus one accent for the critical path.

Mistakes:
- Labels colliding with shapes (the wrap problem -- test with
  your longest label).
- Diagrams that restate a list. "A -> B -> C" with no branching
  is a sentence, not a diagram.
- Hairball graphs. Past ~15 nodes, split into overview + detail
  views.

## One-off editor

For triage, reorder, tag, tune, curate, annotate -- when
describing the change is harder than making it. The defining
property: the result leaves through an export button. Read
export.md before building any of these.

Sub-shapes:

**Board** (triage, reorder, bucket): columns like Now / Next /
Later / Cut, drag-and-drop cards, per-column counts. Pre-sort by
your best guess so the user edits instead of starting from zero.

**Config form** (flags, env vars, structured settings): fields
grouped by area, dependency warnings ("A requires B, currently
off"), changed-from-original highlighting. Export the diff, not
the whole config.

**Side-by-side tuner** (prompts, templates, copy): editable
source left, live preview right with variables filled, sample
inputs to switch between, char/token counter.

**Curator** (datasets, screenshots, candidate lists): one item
at a time or a dense list, approve/reject/tag with keyboard
shortcuts (j/k to move, y/n to judge), running counts, export
the labeled set.

**Annotator** (transcripts, documents, diffs): click a span to
attach a note, category tags, export annotations with their
source quotes.

**Value picker** (colors, easing curves, regexes, retry/backoff
parameters, cron schedules): visual control plus live preview
plus the value rendered in the format the user needs. For
exploring a parameter space rather than picking one value, add
sliders for each parameter and a copy button for the current
combination.

Keyboard ergonomics: if the user will process more than a few
items, add shortcuts and show them in a small "?" panel.

Mistakes:
- Building infrastructure. This file dies after one use --
  hardcode the data, skip the abstraction.
- An empty editor. Pre-populate with the actual data from the
  conversation; making the user re-enter it is a failed artifact.
- Export as an afterthought. The export is the product; the UI
  is just how the export gets its values.
