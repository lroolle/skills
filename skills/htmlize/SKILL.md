---
name: htmlize
description: >-
  Technical explanation and HTML artifact protocol. Decides whether a
  deliverable beats markdown, models the reader's questions, chooses a
  single page or multi-page briefing site, builds it against a craft
  baseline, and reviews existing artifacts. Fires on three branches:
  an explicit ask for an HTML, visual, interactive, or site-level
  deliverable; a plan, report, system explainer, comparison, deck, or
  diagram whose structure is lost in linear markdown; and improving an
  HTML deliverable that looks generic, fragmented, or hard to navigate.
  Production frontend is kiln's territory; a growing knowledge base is
  wiki-it's; hand-maintained project docs should remain markdown.
---

# htmlize

The name is the invocation, not the product. Keep `htmlize` because it
is discoverable and existing callers know it; do not describe the result
as "an HTML." The product is an **artifact** when one page answers one
job, and a **technical briefing site** when several reader questions must
cohere without being forced into one scroll.

HTML is the material. Explanation is the work.

Two modes:

- **Create:** turn task evidence and technical reasoning into a reading
  experience.
- **Review:** diagnose an existing artifact or briefing site against the
  same contracts.

The protocol is Gate -> Frame -> Map -> Build -> Check. Review mode runs
Check first, then repairs only the failed contracts.

## 1 -- Gate

Ask two questions in order: does this deserve HTML, and if so, does it
deserve a site?

Stay in markdown when any of these hold:

| Signal | Why markdown wins |
|---|---|
| The answer fits in one screen | A page would be ceremony |
| The deliverable is code or shell instructions | Fences are already the right interface |
| It belongs in git and humans will edit the prose | Markdown diffs and edits cleanly |
| It is read once, top to bottom | Navigation would add no leverage |
| The structure is headings plus paragraphs | HTML would only impersonate layout |

Use HTML when spatial comparison, diagrams, navigation, direct
manipulation, or a purpose-built view carries meaning prose would bury.
Length is supporting evidence, never the reason by itself.

Then choose the scale:

| Scale | Contract |
|---|---|
| **Page** | One reader question, one linear argument, one share target |
| **Site** | Several independently useful questions, more than one reading path, or overview and implementation detail that should not compete in one scroll |
| **Tool** | The reader changes, filters, tunes, or classifies data; export is the result |
| **Deck** | A presenter controls sequence in a room; one idea per screen |

A site must earn at least three real pages. Do not split one essay at
arbitrary word counts. Split when each page has a distinct question,
can be linked on its own, and leaves the reader knowing what the next
page adds. Keep the primary navigation to 3-7 items; beyond that, the
model is probably a knowledge base and belongs to wiki-it.

If the gate says markdown, stop and deliver markdown. Saying no is the
protocol working.

## 2 -- Frame

Before markup, write four lines in working notes:

1. **Purpose:** the decision or understanding this deliverable enables.
2. **Reader:** who arrives, and what they already know.
3. **Thesis:** the most important conclusion, in one sentence.
4. **Boundary:** what system and time horizon are in scope.

If the thesis is unknown, investigate before designing. Navigation
cannot rescue unresolved thinking.

For a technical explanation, establish the whole before the parts:

1. the problem and why it matters;
2. the system boundary and architecture;
3. component responsibilities and relationships;
4. runtime mechanics, data flow, and invariants;
5. alternatives, the selected design, and rejected options;
6. failure modes, edge cases, tradeoffs, and verification;
7. the resulting system and its limits.

This is a reasoning order, not a mandatory table of contents. Merge thin
ideas. Promote a subject into its own page only when the split improves
orientation or independent use.

Mark epistemic standing where it changes trust: observed fact,
measurement, inference, or design judgment. Link claims to evidence near
the claim; a bibliography cannot reveal which sentence it supports.

Done when the purpose, reader, thesis, and boundary are unambiguous.

## 3 -- Map

Choose the shape before styling:

| Job | Shape |
|---|---|
| Compare approaches | Exploration grid |
| Plan, RFC, implementation writeup | Plan document or briefing site |
| Explain a system or subsystem | Technical briefing site when non-linear; report when linear |
| Review a PR or code path | Code review board |
| Status, incident, benchmark | Report / explainer |
| Present to a room | Arrow-key deck |
| Triage, reorder, tag, tune | One-off editor |

Load [patterns.md](references/patterns.md) for every build. Load
[sites.md](references/sites.md) in site mode; it defines the question map,
page anatomy, navigation, source bundle, and split/merge tests. Editors
also load [export.md](references/export.md). Diagrams past a handful of
nodes load [diagrams.md](references/diagrams.md). When a decision rests
on numbers, load [report.md](references/report.md).

One deliverable, one thesis. A site is not a folder of related pages; it
is one explanation whose pages answer different questions. Write the
page map in `site.json` before writing page bodies. The map is done when:

- every page title is a reader question in disguise;
- every page has a one-sentence job and an explicit next step;
- two useful reading paths can be named (for example reviewer and
  implementer); and
- no page exists merely because a template supplied it.

## 4 -- Build

Start from the matching asset:

- `assets/templates/document.html` -- single-page plans, reports,
  reviews, and explainers;
- `assets/templates/site/` -- multi-page technical briefing;
- `assets/templates/tool.html` -- editors and micro-tools;
- `assets/templates/deck.html` -- presentations.

For a site, run `scripts/scaffold-site.sh <output-dir>`, replace the
`SLOT:` markers, remove unearned pages, synchronize `site.json` and every
primary nav, then run `scripts/check-site.py <output-dir>`. The site is a
self-contained **bundle**: shared local CSS and JS are correct; network
dependencies are not. A single-page artifact remains one self-contained
`.html` file.

Build to these invariants:

1. **Five-second orientation.** Title, thesis, scope, and the useful next
   choice appear before decoration or detail.
2. **Real information architecture.** Pages divide questions; sections
   divide one answer. No client-side router, tab maze, or pagination by
   length. Real links survive reload, sharing, print, and no JavaScript.
3. **Whole to parts.** Overview first, system map second, mechanisms and
   evidence after. Do not make readers infer the whole from component
   pages.
4. **Calm typography and semantic layout.** Serif body for documents,
   sans for tools, 60-75ch measure. Use tables for tabular data, code
   elements for code, inline SVG for diagrams, and columns only for real
   comparison.
5. **Color carries meaning.** Status, category, or emphasis only. Mood
   gradients, ornamental cards, and emoji headings reduce trust.
6. **Safe DOM construction.** Variables enter through `textContent`,
   attributes, or `createElement`; never variable `innerHTML`. No
   `localStorage` or `sessionStorage`.
7. **Progressive enhancement.** Core reading and navigation work without
   JavaScript. JS may add active navigation, diagram inspection, and
   export ergonomics; it may not contain the explanation.
8. **Inspectable diagrams.** Render complex diagrams to inline SVG at
   build time. `figure.diagram` gains optional 50%-500% zoom and a
   viewport-filling mode while preserving selectable text and a fitted
   no-JS baseline.
9. **Responsive, dark, reduced-motion, print.** Phone layouts preserve
   sequence; print expands hidden detail and fits diagrams; dark mode
   remaps rendered SVG palettes.
10. **Evidence travels.** Fill the colophon. A durable briefing includes
    its markdown reasoning source and editable diagram sources under
    `sources/`; HTML is the view, not the only record.
11. **No placeholders.** Use the task's real data. A visible `SLOT:`,
    lorem ipsum, empty editor, or generic option is unfinished work.
12. **Descriptive paths.** `queue-architecture/decisions.html`, not
    `output/page-3.html`. Page filenames name concepts, not sequence.

Interactive state lives in memory and leaves through an explicit export.
The export contract is in [export.md](references/export.md).

## 5 -- Check

Read the result as three people: a first-time reader seeking the thesis,
a reviewer challenging the design, and an implementer looking for exact
mechanics. Each must find their next page without guessing.

In site mode run:

```bash
python3 scripts/check-site.py path/to/site
```

It checks the manifest, page/nav agreement, local links and fragments,
duplicate IDs, semantic landmarks, source presence, external
subresources, unsafe browser APIs, and unfinished markers. It does not
judge whether the explanation is true; verify that against the sources.

Review mode reports one row per violation:

| Issue | Fix | Why |
|---|---|---|
| One scroll contains several independent questions | Split by question into a briefing site | Page boundaries restore orientation and shareable context |
| Site pages are chapters named Part 1 / Part 2 | Name pages for the question or concept | Navigation should predict the answer behind the link |
| Overview is a link list with no thesis | State problem, system boundary, architecture, result | A map without an argument does not orient |
| The same navigation differs between pages | Make `site.json` canonical and synchronize every nav | A moving map destroys spatial memory |
| Essential content exists only behind JS | Render it in HTML; enhance behavior only | Links, print, accessibility, and file viewing must survive JS failure |
| `innerHTML` receives a variable | `textContent` + `createElement` | Prevents injection from task data |
| Storage APIs retain throwaway state | In-memory state + explicit export | Sandboxed access can throw; artifacts should leave no residue |
| External script, stylesheet, font, or image | Bundle it locally or inline it | The deliverable must outlive another server |
| Diagram is unreadable at fitted width | Add the diagram viewer; split hairballs at ~15 nodes | Browser zoom should not be the inspection interface |
| Diagram controls lack keyboard/focus behavior | Real buttons, labeled range, focus trap and return | Fullscreen must not strand keyboard users |
| Hand-drawn complex SVG | Render `.dot`, `.d2`, or `.mmd` at build time | Layout and edge routing are computation |
| SVG text collides with shapes | Resize shapes or use wrapped HTML in `foreignObject` | SVG text does not wrap |
| Numeric columns are ragged or axes mislead | Apply report.md's units, precision, spread, and zero-baseline rules | Visual polish cannot repair untrustworthy evidence |
| Stacked prose, ornamental cards, gradient hero | Use spatial structure or return to markdown | HTML without information shape is cost without leverage |
| Artifact breaks on phone, dark mode, or print | Repair all three modes | Briefings travel across surfaces |
| Durable reasoning exists only in HTML | Include markdown and diagram sources | HTML is a generated view, not an editable record |

Done when the mechanical checker passes, every link and interaction has
been exercised, and the thesis remains clear when skimming only titles,
diagrams, captions, and decision statements.

## Boundaries

- **kiln** owns production product interfaces. htmlize owns finite agent
  deliverables and the micro-tools used to inspect them.
- **wiki-it** owns a growing, interlinked, maintained corpus. A briefing
  site has one thesis, a finite page map, and a completion state.
- **animate-it** owns motion craft. Artifacts keep motion to functional
  150-250ms transitions and honor reduced motion.
- **drop** owns publishing and review URLs. htmlize produces the local
  bundle; drop re-checks privacy before it leaves the machine.
- Hand-maintained README, CONTRIBUTING, and product docs stay in
  markdown or their existing documentation system.

## Accessibility and privacy

Color never acts alone. Controls are native elements with visible focus.
Each page has one `h1`, ordered headings, a skip link, landmarks, and a
plain-link path forward. Fullscreen diagram inspection returns focus to
its trigger and permits Escape at all times.

Artifacts carry real ticket text, code, names, and configuration. Treat
the bundle as data: do not commit it to a public repository or publish it
without checking every included file. A link is publication.

## Output

Create mode reports:

```text
## Gate
[markdown, page, site, tool, or deck -- and why]

## Frame
[purpose, reader, thesis, boundary]

## Map
[shape; for sites, page questions and reading paths]

## Deliverable
[path to the file or site index]

## Check
[mechanical result, interaction checks, intentional tradeoffs]
```

Review mode reports the violation table, then the repaired path when
repairs were requested.

## References

| File | Load when |
|---|---|
| [patterns.md](references/patterns.md) | Building any artifact |
| [sites.md](references/sites.md) | Building or reviewing a multi-page briefing |
| [style.md](references/style.md) | Writing or extending CSS |
| [diagrams.md](references/diagrams.md) | A flow, architecture, sequence, or state diagram appears |
| [report.md](references/report.md) | A decision rests on numbers |
| [export.md](references/export.md) | The artifact is interactive or affects durable docs |
| [prior-art.md](references/prior-art.md) | Studying lineage and alternatives; not an operational dependency |

Bundled tooling renders diagrams (`render-diagram.sh`), scaffolds a
briefing (`scaffold-site.sh`), and checks its integrity
(`check-site.py`).
