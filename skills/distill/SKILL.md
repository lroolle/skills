---
name: distill
description: >-
  Distill a knowledge source -- book, transcript, course, doc set,
  post series -- into the few agent skills it actually earns.
  Strict yield: most sources earn 0-3 skills and a digest; every
  unit must pass four gates (grounded, predictive, earned,
  behavioral) before it ships. Fires on two branches: the user
  wants a source turned into skills ("distill this book", "make
  skills from this course / transcript / doc set"); or they ask
  whether a source is worth distilling. Capturing a live session's
  workflow is skillize's job; a skill from scratch is
  skill-creator's. A summary, review, or reference wiki needs no
  skill -- write the deliverable directly.
---

# Distill

Most of a book boils away. Story, restatement, context, charisma --
all of it matters to a reader and none of it changes how an agent
works. What condenses is small: the two or three moves the author
actually invented. Distill finds those, proves each one earns its
place, and ships them as skills built to this collection's
doctrine. Everything else becomes the digest.

The test for every unit: **holding it, does an agent behave
differently in a nameable situation -- and could you check?**
Knowledge that only makes answers sound wiser is reading material,
not a skill.

## When to invoke

**Use when:**

- The user has a source (book text, video/podcast transcript,
  course, documentation set, post series) and wants skills from it
- The user asks whether a source is worth distilling
- A prior distillation produced skills that never fire, and the
  user wants them re-earned or retired

**Route elsewhere:**

- The workflow to capture happened in this session -> skillize
- No source, no session -- skill from scratch -> skill-creator
- The user wants a summary, reading notes, or a navigable
  reference wiki -> write that deliverable directly; skills are
  for behavior, and none of those change an agent's

## Ground rules

**Work from the actual text.** Model memory of a book is a summary
of other people's summaries -- quotes come out mangled and the
distinctive units are exactly what memory flattens. If there is no
file, stop and ask for one (for video or podcast, ask for the
transcript).

**Quote like a reviewer, not a reprinter.** At most one short
quote per skill, under 25 words, attributed with its location
(chapter, timestamp, or section). Everything else is restated in
your own words. For non-English sources, translate yourself --
never lift a published translation.

## Gate -- triage the source

Before reading deeply, estimate operational density: how much of
this source tells someone *what to do* rather than what happened
or how it felt?

| Source shape | Signals | Expected yield |
|---|---|---|
| Method-dense | Frameworks, checklists, decision rules on every other page | 3-5 skills |
| Mixed | A few named moves inside narrative or theory | 1-3 skills |
| Narrative / inspirational | Stories, worldview, taste; wisdom without procedure | 0-1, usually 0 |
| Reference | Facts, APIs, specifications | 0 -- lookup material, not behavior |

Report the triage before proceeding. **Zero is a valid yield**: a
great book can earn no skills -- the digest was the right
deliverable, and saying so early saves the whole pipeline. If the
user only asked "is this worth distilling," stop here with the
verdict.

## Survey

Read the source end to end (chunk long sources; keep running
notes per chunk). Produce three things:

1. **Spine** -- the source's core argument in 3-5 sentences
2. **Claims** -- the named methods, rules, and frameworks the
   author advances, each with where it appears
3. **Blind spots** -- what the author ignores, overclaims, or
   assumes; where the method would fail. This critical pass is
   not optional: blind spots become the boundary sections of
   every skill you ship.

Survey is done when you can state the spine without hedging and
every candidate claim has at least one located appearance. Show
the user the spine and candidate list before hunting deeper --
one confirmation here prevents distilling toward the wrong
emphasis.

## Hunt

Sweep the source once through five lenses. One context, five
passes of attention -- like parallax's lenses, not five agents
(for sources too large for one context, chunk and sweep per
chunk; spawning parallel extractors is a cost multiplier that
buys little on a text that fits).

| Lens | Hunting for |
|---|---|
| Framework | Decision procedures, orderings, if-then structures |
| Rule | Principles and checklists the author states as invariants |
| Case | Episodes where the author personally ran the method |
| Failure | Modes the author warns against; what breaks the method |
| Term | Coinages that compress a concept (candidate leading words) |

Each candidate unit gets one line: name, type, locations. Cases,
failures, and terms usually attach to a framework or rule as
evidence and boundary material -- they rarely stand alone.

## Earn

The quality gate that separates distillation from book-summarizing.
Run every candidate through four tests; all four must pass.

1. **Grounded.** The unit appears in 2+ independent contexts --
   different chapters, different subjects, different conclusions.
   The cheat: one example paraphrased twice. If the author only
   said it once, it is a quote for the digest, not a method.
2. **Predictive.** Pose a question the source never discusses and
   derive a non-trivial answer using the unit. The cheat: posing a
   question the book *does* discuss in other words. A real method
   extrapolates; a description only points back at its examples.
3. **Earned.** Strip the author's name: would a smart generalist
   say this unprompted? "Respect your time" is idle. "Maintain a
   stop-doing list" survives -- the ordering is counter-intuitive.
   This is the no-op test applied to knowledge: the model already
   holds common sense; only differentiated insight changes output.
4. **Behavioral.** Name the agent situation where this fires and
   what the agent does differently -- checkably. "Knows about
   inversion" fails; "before committing a design, lists the three
   outcomes to avoid and works backward" passes. A unit that only
   informs tone is digest material.

Track the yield rate. Under ~10% on a method-dense source means
the hunt was shallow -- re-sweep. Over ~60% means the gates went
soft -- re-run them colder. (Bands adapted from cangjie-skill's
pass-rate telemetry.)

Present survivors and casualties to the user with one-line
reasons: "these N earn skills; these M go to the digest -- rescue
or cut anything?" Shaping is the expensive phase; this checkpoint
is the cheap one.

## Shape

Each earned unit becomes a skill directory built to this
collection's doctrine -- gate-first body, one-trigger-per-branch
description, completion criteria, positive steering. Load
[shaping.md](references/shaping.md) for the construction recipe:
section-by-section mapping from unit to SKILL.md, frontmatter
fields for source attribution, and worked examples of trigger
descriptions built from language signals.

The two decisions that make or break each skill:

- **The description comes from future situations, not source
  content.** Ask: in what working situations will someone need
  this move, and what will they *say*? Those language signals are
  the description. A description that summarizes the chapter
  fires never; one that matches the user's words fires precisely.
- **The boundary comes from the blind-spot list.** What the
  author warned against, plus what the author couldn't see. A
  skill without a boundary gets invoked everywhere and disappoints.

Name skills by the move, not the source: `inversion-check`, not
`munger-chapter-3`. The source lives in frontmatter attribution.

## Prove

For each shaped skill, write a bait set of 6-9 prompts, three
kinds: should-fire (varied phrasings of the real situations),
should-hold (adjacent situations that belong to common sense or
another skill), and sibling-bait (situations that should fire a
*different* skill distilled from the same source -- the confusion
test). Walk each prompt against the descriptions and judge which
skill fires.

A skill that misfires goes back to Shape for a sharper
description; one that cannot be separated from its sibling merges
into it; one whose should-fire prompts feel contrived gets cut --
contrived triggers mean the situation never actually occurs, and
Earn should have caught it. When skill-creator is installed, its
eval pipeline replaces hand-walking with real trigger runs.

## Deliver

1. Write `DIGEST.md` beside the skills: the spine, the earned
   skills with one-line triggers, and -- first-class, not an
   appendix -- what did *not* become a skill and why (failed
   which gate). The residue is where the next reader's trust
   comes from, and it doubles as resume state if distillation
   is interrupted.
2. Install the skills where the user wants them (project or user
   scope), following the collection's registration rules if they
   land in a skills repo.
3. Offer skillbun when the set should travel as one archive.

## Output shape

```
<source-slug>/
├── DIGEST.md            # spine + earned skills + residue with reasons
├── <move-1>/SKILL.md    # skills named by move, built to doctrine
└── <move-2>/SKILL.md
```

Report at the end: yield (earned/candidates), the gate each
casualty failed, and where the skills were installed.

## Composition

| Skill | Crystallizes |
|---|---|
| skillize | A session's lived workflow |
| **distill** | A source's transferable methods |
| skill-creator | Intent, from scratch, with evals |
| skillbun | Any of the above, into a shippable archive |

## Lineage

The verification gates adapt cangjie-skill's triple-verify
(cross-domain, predictive power, exclusivity) and its
future-trigger insight -- descriptions from situations, not
summaries (MIT, github.com/kangarooking/cangjie-skill). The
behavioral gate, strict-yield posture, digest-as-first-class
output, and single-context hunt are this collection's doctrine
applied to their pipeline. Survey's critical pass descends from
Adler's *How to Read a Book*; the R/I/A scaffold in shaping.md
traces to Zhao Zhou's bookmark method via cangjie.
