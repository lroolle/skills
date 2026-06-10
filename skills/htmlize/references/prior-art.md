# Prior art

htmlize descends from "The unreasonable effectiveness of HTML"
and synthesizes the ecosystem that formed around it. Lineage and
what we changed.

## Sources

- **Thariq Shihipar, "Using Claude Code: The unreasonable
  effectiveness of HTML"** (Anthropic blog, 2026-05) -- the
  founding argument: information density, visual clarity,
  shareability, two-way interaction, data ingestion. With a
  gallery of 20 canonical examples at
  [thariqs.github.io/html-effectiveness](https://thariqs.github.io/html-effectiveness/)
  (Apache-2.0, mirrored at anthropics/html-effectiveness).
- **[dogum/html-artifacts](https://github.com/dogum/html-artifacts)**
  (Apache-2.0) -- the best-shaped community skill: recognition
  heuristic, markdown carve-outs, category references, taste
  warnings. Our Gate tables and style baseline owe the most to
  this skill's "when to reach for HTML" / "when to stay in
  markdown" sections and its typography-first design doctrine.
- **[f-labs-io/agent-html-skills](https://github.com/f-labs-io/agent-html-skills)**
  (MIT) -- the most ambitious: 16 skills plus a two-way submit
  loop (browser -> agent via local listener). Our Build rules
  adopt its HTML output foundation ideas (safe DOM, SVG text
  wrapping, no browser storage, print/accessibility floors). We
  deliberately did not adopt the server loop -- see export.md.
- **[aDragon0707/claude-code-html-skill](https://github.com/aDragon0707/claude-code-html-skill)**
  (Apache-2.0) -- contributed the "name the job first" discipline
  and the markdown-as-source-of-truth loop, which we kept, minus
  its routing-contract bureaucracy.
- **HN thread 48071940** (528 points) -- the field evidence. The
  strongest objections (co-editing friction, diff noise, token
  cost, slop styling, artifacts leaking PII through casual
  publishing) shaped the Gate step, the slop list, and the
  Privacy section. The strongest pro ("purpose-generated
  ephemeral UI") shaped the editor patterns.

## Design choices

1. **Gate first.** Every prior skill mentions when not to use
   HTML; none makes it a protocol step. dogum's posture is "use
   HTML aggressively." Ours is "the most valuable thing the skill
   does is say no" -- because the failure mode of this whole
   philosophy is HTML-by-default applied to things markdown does
   better, and the HN thread is full of exactly that complaint.
2. **One skill, four steps.** f-labs ships 16 skills; that
   granularity helps triggering but costs coherence and
   maintenance. We compress the territory into one protocol with
   shape references, the same architecture as our animate-it.
3. **Review mode.** No prior skill reviews existing artifacts.
   Generated HTML that "looks off" is now common enough that the
   Check table doubles as a standalone review rubric.
4. **Clipboard, not server.** The f-labs auto-submit loop is
   better UX bought with platform-specific machinery (local
   listener, monitor wiring, teardown skills). We take the
   portable subset and link to f-labs for users who want the
   loop. A skill that works identically across harnesses beats
   one that is magical in exactly one.
5. **Markdown keeps the record.** The strongest sustained
   objection to HTML artifacts is losing co-editing and git
   diffing. We resolve it structurally: durable state lives in
   markdown, HTML is a generated view with exports that write
   back. HTML never becomes the system of record.
6. **Privacy as a first-class section.** The HN thread documents
   real PII leaks from casually published artifacts. No prior
   skill mentions this. Artifacts are data files, and the skill
   says so.
