---
name: htmlize
description: >-
  HTML artifact protocol for agent deliverables. Decides whether a
  deliverable should be a self-contained HTML file instead of
  markdown, picks the artifact shape, builds it against a craft
  baseline, and reviews existing artifacts for quality problems.
  Trigger on: "make an HTML file", "HTML artifact", "make it
  visual", "make this interactive", /htmlize, any request for a
  plan, spec, report, explainer, comparison, code review writeup,
  incident report, slide deck, diagram, or one-off editor; and any
  deliverable whose markdown equivalent would run past ~100 lines.
  Also trigger when the user shows an HTML deliverable (a report,
  plan, or deck -- not a product UI) that looks like generic AI
  output and wants it improved. Do NOT trigger for production
  frontend code, web app features, or hand-maintained docs like
  README and CONTRIBUTING.
---

# htmlize

Markdown serializes everything into one column. A comparison, a
diff, a timeline, a parameter sweep -- markdown flattens each into
prose the reader scrolls past. HTML keeps the shape: side-by-side
stays side-by-side, flow stays a diagram, state becomes something
the reader can drag, filter, or tune.

This skill turns agent deliverables into self-contained HTML
artifacts when -- and only when -- the artifact beats the markdown.
The most valuable thing it does is say no.

Two modes:
- **Create mode**: a deliverable needs to be produced
- **Review mode**: an HTML artifact exists, something is off

## The protocol

Four steps: Gate -> Shape -> Build -> Check. Review mode runs
Check alone.

### Step 1 -- Gate

Should this be HTML at all?

Stay in markdown when any of these hold:

| Signal | Why markdown wins |
|---|---|
| The answer fits in one screen of chat | Wrapping a paragraph in a web page is ceremony |
| The deliverable is code | A fenced block already renders code perfectly |
| The reader will paste from it into a shell | They need copyable text, not a page to admire |
| It belongs in git and gets reviewed as diffs | Reviewers can read a markdown diff; an HTML diff is churn |
| A human will edit it after you | Hand-editing generated markup punishes the person you made it for |
| It is read once and discarded | HTML costs several times markdown's tokens; spend them where they get read |

Go HTML when any of these hold:

| Signal | What HTML buys |
|---|---|
| The reader must weigh alternatives | Options in parallel columns; prose forces them single-file |
| Structure is the content: diffs, flows, timelines | Position and color carry what sentences would bury |
| The reader tunes, toggles, drags, or filters | Doing beats describing |
| The document needs navigation: tabs, collapse, jump links | A long file gets scrolled past; a navigable one gets used |
| It will travel beyond this conversation | A link gets opened; an attached .md gets archived unread |
| The markdown version would pass ~100 lines | Past that, markdown stops being read at all -- the founding observation of this approach |
| The data needs a purpose-built micro-tool | One throwaway page beats a paragraph describing the edits |

Tie-break on the document's lifespan in the reader's hands:
minutes of active use -- navigating, comparing, deciding,
forwarding -- justify HTML. One pass from top to bottom does not.

If the gate says markdown, stop here and say so. That is the
skill working, not the skill failing.

### Step 2 -- Shape

State what the artifact is for in one sentence before writing
any HTML: "compare four caching strategies," "retriage thirty
tickets." A request that cannot be reduced to a sentence like
that is not ready -- find out what the reader will decide or do
with it first.

| Job | Shape |
|---|---|
| Explore options, compare approaches or designs | Exploration grid |
| Plan, spec, RFC, implementation writeup | Plan document |
| Review a PR, explain code, map a subsystem | Code review board |
| Status, incident, concept explainer, benchmark results | Report / explainer |
| Present to a room | Arrow-key deck |
| Flowchart, architecture map, sequence diagram | Inline SVG diagram |
| Triage, reorder, tag, tune, curate, annotate | One-off editor |

Layout guidance for every shape is in
[patterns.md](references/patterns.md); editors additionally
follow [export.md](references/export.md).

One artifact, one job. A request that spans jobs -- a spec that
needs design mockups and a sequence diagram -- composes those
shapes inside one file, under one job. When sections stop serving
the job sentence, they are padding; cut them.

### Step 3 -- Build

Read [style.md](references/style.md) before writing CSS. The
rules every artifact must satisfy:

1. **Single self-contained `.html` file.** Inline CSS and JS. No
   build step. A CDN reference is a dependency on someone else's
   uptime, and the file must outlive it -- on surfaces with a CDN
   allowlist an external library is a deliberate trade, never the
   default. System font stacks instead of external fonts.
2. **Real layout, not markdown wearing tags.** Columns for
   comparison, a timeline for time, a rendered diff for diffs.
   If the HTML is stacked headers and paragraphs, the gate was
   wrong -- it should have been markdown.
3. **Five-second first viewport.** Title, one-line framing of
   what this is and what to do with it, then substance. A reader
   who cannot orient in five seconds closes the tab.
4. **Calm typography, color that works.** Serif body for
   documents, sans for tools. 60-75ch line length. Every color
   carries meaning -- severity, status, category. A color that is
   only mood gets removed. The full baseline lives in
   [style.md](references/style.md).
5. **Semantic HTML.** Code in `<pre><code>`, tabular data in
   `<table>`, diagrams as inline `<svg>` with real elements. The
   reader should be able to select and copy any value on the page.
6. **Build DOM safely.** `textContent` for text,
   `createElement` for structure. Never assign `innerHTML` from
   anything containing a variable -- it is an XSS vector and the
   first thing any security review flags.
7. **SVG text does not wrap.** Size the shape to the label, or
   use `<foreignObject>` with an HTML div inside. Overflowing
   labels silently collide with neighboring shapes.
8. **Works on a phone, in print, and in the dark.** Viewport
   meta, single-column collapse under ~700px, `@media print`
   plus a `beforeprint` handler that opens collapsed `<details>`
   (no CSS can), `prefers-color-scheme` dark palette.
9. **Real data, pre-populated.** The user already gave you the
   tickets, the config, the diff. Never make them paste it again.
   Never pad with lorem ipsum.
10. **State lives in memory; export is the persistence layer.**
    No `localStorage` -- in sandboxed artifact iframes merely
    accessing it throws, so even feature-detection crashes the
    script -- and a throwaway should not leave residue. Anything
    the user manipulates ends with an export button. The export
    contract lives in [export.md](references/export.md).

Filename is part of the artifact: descriptive kebab-case,
`cache-strategy-comparison.html`, not `output.html`. Related
artifacts (exploration -> mockups -> plan) share a folder. After
writing, tell the user the path and how to open it.

### Step 4 -- Check

Review the artifact against this table. In review mode, output
one row per violation found: Before (the offending code), After
(the fix), Why (drawn from this table's third column).

| Issue | Fix | Why |
|---|---|---|
| `innerHTML` assigned from a variable | `textContent` + `createElement` | XSS vector; first thing security review flags |
| `localStorage` / `sessionStorage` | In-memory state + export button | Accessing it throws in sandboxed surfaces; throwaways leave no residue |
| External CDN, framework, or font link | Inline everything, system fonts | The file must outlive someone else's uptime |
| Gradient hero, emoji headers, card grid | Calm typographic layout | Generic AI look destroys trust in the content |
| Stacked headers and prose in HTML | Spatial layout -- or revert to markdown | Markdown wearing tags is cost without benefit |
| Editor with no export | Add copy-as-markdown/JSON/diff button | An editor without export is a dead end |
| `navigator.clipboard` with no fallback | Textarea + `execCommand` fallback | Rejects in sandboxed iframes and unfocused documents |
| SVG `<text>` overflowing its shape | Size shape to label, or `<foreignObject>` | SVG text never wraps; it collides silently |
| Lorem ipsum or placeholder rows | Pre-populate from the task data | The user already provided the real data |
| No viewport meta, breaks under 700px | Add meta, collapse to one column | Artifacts get opened on phones |
| Light-only or screen-only | Dark palette + print styles | Specs get printed; phones run dark mode |
| Durable record exists only in HTML | Write the markdown source, HTML as view | Git diffs markdown; HTML is a rendering |

## Boundaries

- **kiln** owns product UI design judgment -- what your
  application's interface should be. htmlize owns agent
  deliverables -- the documents and tools Claude produces while
  working for you.
- **animate-it** owns motion. Inside artifacts, keep motion
  minimal: 150-250ms ease-out transitions on interactive elements,
  nothing else. If the artifact's *subject* is animation, build it
  with animate-it's rules.
- **Production frontend is out of scope.** An artifact is a
  deliverable, not a product. The moment someone wants to deploy
  it, maintain it, or add a backend, it leaves this skill's
  territory.
- **Auto round-trip is out of scope.** Exports go through the
  clipboard; the user pastes back. The reasoning, and the
  heavier alternative this trades away, is in
  [export.md](references/export.md).

## Accessibility

- Color never carries meaning alone. Pair severity and status
  with a label or shape -- printed pages, color-blind readers,
  and grayscale screenshots all get the same information.
- Interactive controls are real elements (`<button>`, `<input>`,
  `<details>`), keyboard-reachable, with visible focus. If an
  editor ships j/k shortcuts, the same actions must also work by
  tab and click.
- Body text meets WCAG AA contrast in both palettes. The
  style.md baseline does; keep that true after re-theming.

## Privacy

Artifacts carry real task data -- ticket text, config values,
code, names. Treat the `.html` file like a data file, not like
code: do not commit it to public repos, do not deploy it to
public hosting. Real incidents exist of teams leaking prospect
lists and customer PII through casually published artifacts. A
file shared by link is published.

## Output format

Create mode:

```
## Gate
[HTML or markdown, and why. If markdown: stop, deliver markdown.]

## Shape
[The job in one sentence. The shape chosen.]

## Artifact
[Write the .html file. Report the path.]

## Check
[Confirm the Step 4 table passes. Note anything intentionally skipped.]
```

Review mode:

```
## Review
| Before | After | Why |
|---|---|---|
| ... | ... | ... |
```

## References

| File | Load when |
|---|---|
| [patterns.md](references/patterns.md) | Building any artifact -- per-shape layout guidance |
| [style.md](references/style.md) | Writing CSS -- baseline, palette, anti-slop list |
| [export.md](references/export.md) | The artifact is interactive or affects durable docs |
| [prior-art.md](references/prior-art.md) | Understanding the lineage and design choices |
