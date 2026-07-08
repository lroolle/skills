# README anatomy — the proof architecture

The ordering is the insight: most engineers write install-first,
feature-list READMEs. Order by *reader decision state* instead:
hook (should I care?) → proof (is it real?) → start (can I feel it in
60 seconds?) → depth (collapsed until wanted).

## The slots, in order

1. **Centered header** — ASCII-art name or logo inside
   `<div align="center">`, one-line tagline under it stating the
   category you own ("The context compression layer for AI agents").
2. **Value line** — `<p align="center"><strong>` with the numbers and
   the form factors: "60–95% fewer tokens (JSON), 15–20% (coding
   agents) · library · proxy · MCP · local-first · reversible".
   Scoped numbers, middot-separated nouns.
3. **Badge row** — only badges that answer a reader question: CI
   (does it build?), coverage (is it tested?), package version (is it
   released?), license (can I use it?), docs (where do I learn?).
   Each badge links somewhere useful. A badge that answers no
   question is lint.
4. **Nav line** — `Docs · Install · Proof · Agents · Discord ·
   llms.txt`. One line, anchors + external links mixed.
5. **Agent pointer** — a `<sub>` line addressed to non-humans:
   "AI agents / LLMs: read /llms.txt here, or fetch the live index."
   Costs one line, serves a growing share of first contact.
6. **Demo** — GIF or screenshot with a *concrete caption*:
   "Live: 10,144 → 1,260 tokens — same FATAL found." The caption
   carries numbers; the image carries feeling.
7. **What it does** — 5-8 bullets, each `**bold lead** — payoff`,
   one form factor or capability per bullet.
8. **How it works (30 seconds)** — one ASCII diagram of the data
   flow, then one line per box. ASCII beats an image: it renders
   everywhere, diffs cleanly, and agents can read it.
9. **Get started (60 seconds)** — numbered, copy-paste-runnable,
   ends with a verification command (a `doctor` / `status`
   subcommand is the classic shape) so the reader knows it worked.
   If it honestly takes 10 minutes, fix the product or the
   promise, not the wording.
10. **Proof** — the section most READMEs lack and the one that
    converts. Before/after tables on real workloads, accuracy
    benchmarks showing nothing broke, and a **reproduce command**
    that regenerates the tables. Claims without repro paths are
    marketing; with them, they're engineering.
11. **When to use · When to skip** — an honest anti-pitch. "Skip it
    if you only use a single provider's native compaction." Telling
    people to leave builds more trust than any feature bullet.
12. **Depth, collapsed** — `<details>` blocks for integrations
    tables, internals, pipeline lifecycle. Depth is available, not
    imposed. The README stays scannable at every scroll position.
13. **Docs table** — two columns: "Start here" / "Go deeper".
    Curated, not exhaustive.
14. **Compared to** — a table against real alternatives with honest
    checkmarks, followed by *generous attribution*: call the
    competitor excellent when it is, thank the teams you build on,
    explain how you use their tools. Attribution reads as
    confidence.
15. **Teams / sustainability** (when applicable) — value-first, no
    dark patterns: "Everything in this repo stays open source. The
    managed offering is for teams that would rather have it deployed
    for them." State who OSS is for, who pays, and why both win.
16. **Contributing · Community · License** — short, linking out.

## Anti-patterns (the cringe list)

- Star-history charts and trend badges on repos without stars yet —
  aspirational flair signals the opposite of traction.
- Badges that answer no reader question (visitor counters, "made
  with love", language percentages).
- Feature lists before any evidence the thing works.
- "Blazingly fast" and friends — unscoped superlatives. Replace
  with a number and its conditions, or delete.
- Screenshot walls with no captions; captions with no numbers.
- Corporate boilerplate health files that obviously came from a
  generator — worse than short honest ones.

## The 30-second test

Hand the README to someone cold. In 30 seconds they should answer:
what is it, why should I care (with a number), how do I try it.
If any answer is missing, the anatomy has a hole at that slot.
