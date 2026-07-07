# Skills

> Agent skills with opinions: design, motion, artifacts, decisions,
> and the craft of making skills themselves.

[![skills.sh](https://skills.sh/b/lroolle/skills)](https://skills.sh/lroolle/skills)
[![license](https://img.shields.io/github/license/lroolle/skills)](LICENSE)
[![spec](https://img.shields.io/badge/spec-agentskills.io-blue)](https://agentskills.io/specification)

Small, composable skills that solve real problems I hit daily with Claude Code
and Codex. Not a framework. Not a process. Just focused tools you can drop into
any project and hack on.

## Quickstart

```bash
npx skills@latest add lroolle/skills
```

Pick the skills you want and which agents to install them on.

<details><summary>Manual install</summary>

```bash
git clone https://github.com/lroolle/skills.git
cd skills
./scripts/link-skills.sh
```

Or copy individual skills:

```bash
cp -r skills/kiln ~/.claude/skills/kiln
```

</details>

## Why these skills exist

### The AI-generated look

Most AI-built interfaces are instantly recognizable: Inter font, purple
gradient, card-in-card layouts, magnetic cursor effects. They converge on the
same defaults because agents reach for training-data reflexes.

**kiln** fixes this by separating permanent perceptual rules (human vision
doesn't change) from temporal taste (what's saturated right now). It ships six
material kits with distinct personalities, anti-pattern detection, and a
quarterly-versioned zeitgeist file that tracks which aesthetics have been
strip-mined by AI generators.

### The animation that doesn't feel right

Agents add animation the way they add comments: everywhere, uniformly,
without judgment. `transition: all`, scale(0) entrances, ease-in on
exits, motion on keyboard actions that fire a hundred times a day.

**animate-it** is the implementation protocol: gate (should this animate
at all?), classify the motion type, specify easing/duration/tool, then
code against the rules that separate "has animation" from "feels right."
Kiln decides what should move and why; animate-it makes it move
correctly.

### The wall of markdown

Agents produce 300-line markdown plans nobody reads. Comparisons get
stacked instead of side-by-side, timelines become bullet lists, and
anything interactive gets described instead of built. The fix isn't
"always output HTML" -- generated HTML has its own failure modes:
slop styling, lost git diffs, dead-end editors.

**htmlize** is the artifact protocol: gate (does this deliverable beat
markdown?), shape (which artifact pattern), build (self-contained
single file, calm typography, safe DOM), check (the review rubric).
Exports go through the clipboard; markdown stays the source of truth.

### The first answer that sticks

Claude picks the first reasonable approach and builds on it. For most
problems, that's fine. For decisions that are expensive to reverse --
architecture, naming, strategy -- it produces competent, forgettable
output. The real cost isn't a bad answer. It's never seeing the better
one because you stopped looking.

**parallax** forces a structured pause: frame the decision, generate 3-5
approaches that differ on fundamental assumptions (not implementation
details), surface the traps, commit to one with explicit trade-offs.
Inspired by [ADHD](https://github.com/UditAkhourii/adhd)'s divergent
ideation work, but designed as a lightweight protocol -- not an
orchestration harness. One context, zero infrastructure.

### The workflow you can't repeat

You spend 40 minutes getting an agent to do something perfectly -- tool
sequences, corrections, domain knowledge discovered along the way. Next week
you need the same workflow and start from scratch.

**skillize** crystallizes a session into a reusable skill. It surveys the
conversation, classifies corrections by durability (permanent rule vs one-off
fix), extracts the repeatable pattern, and drafts a SKILL.md. The workflow is
preserved, not just the output.

### The goal that drifts

You set `/goal` and the agent runs for an hour -- then you discover it
built the wrong thing. The goal was vague, the scope was open-ended, the
verification was "looks good." The agent filled every ambiguity gap with
its own assumptions.

**goldengoal** shapes fuzzy intent into a falsifiable engineering
contract before execution starts. Five contract gates -- outcome,
evidence, boundary, stop rules, pause conditions -- plus a pre-mortem
for complex work. Two modes: compose (walk through problem, outcome,
scope, context, contract) and sharpen (engine-test an existing draft).
Calibrates protocol weight to task complexity -- a typo fix gets three
lines, an architecture change gets full scope and stop rules. Produces
two artifacts: a goal brief (full spec) and a `/goal` condition (the
evaluator's exit gate).

### The book you read but never use

You read a methodology book, highlight half of it, and a year
later make the same decisions you would have made anyway. The
knowledge stayed at "I've read it" -- it never activates when an
agent is actually working.

**distill** turns a knowledge source -- book, transcript, course,
doc set -- into the few skills it actually earns. Strict yield:
every candidate unit must pass four gates (grounded in 2+
independent passages, predictive beyond the source's own examples,
non-obvious to a smart generalist, and behavioral -- it changes
what an agent does, checkably). Most sources earn 0-3 skills; the
rest becomes an honest digest that says what didn't make it and
why. Verification gates adapted from
[cangjie-skill](https://github.com/kangarooking/cangjie-skill)
(MIT), rebuilt around this collection's gate-first doctrine.

### Skills that can't travel alone

You build a skill that depends on another skill's scripts. You share the
`.skill` file and the recipient's eval pipeline silently breaks because the
dependency isn't there.

**skillbun** resolves inter-skill dependencies, renames to avoid collisions
with independently installed copies, and packages everything into a single
`.skill` archive. One file, one install.

## Skills

- **[kiln](skills/kiln/SKILL.md)** -- Precision UX design instrument.
  Layered architecture: perceptual principles -> composable patterns ->
  parameterized material palettes. Six curated kits. Anti-AI-slop detection.
  Generates and audits interfaces.
- **[animate-it](skills/animate-it/SKILL.md)** -- Animation implementation
  protocol. Gate -> classify -> specify -> code -> check. Custom easing
  curves, duration tables, tool selection, and a review rubric for
  animation code that feels wrong.
- **[htmlize](skills/htmlize/SKILL.md)** -- HTML artifact protocol.
  Gate -> shape -> build -> check. Turns agent deliverables into
  self-contained HTML artifacts when they beat markdown -- and says no
  when they don't. Starter templates, a build-time diagram pipeline
  (graphviz / d2 / mermaid), clipboard exports, markdown as source of
  truth.
- **[parallax](skills/parallax/SKILL.md)** -- Multi-perspective decision
  protocol. Frame -> spread -> commit. Forces genuinely different alternatives
  before choosing. Trap detection as a first-class operation.
- **[goldengoal](skills/goldengoal/SKILL.md)** -- Goal engineering
  protocol. Compose (intent -> contract) or sharpen (engine-test an
  existing draft). Five contract gates, pre-mortem, iteration policy.
  Produces goal brief + /goal condition.
- **[skillize](skills/skillize/SKILL.md)** -- Session-to-skill crystallizer.
  Extracts repeatable workflows from agent sessions, classifies corrections,
  drafts SKILL.md with references. Optional eval pipeline.
- **[distill](skills/distill/SKILL.md)** -- Source-to-skills
  distiller. Gate -> survey -> hunt -> earn -> shape -> prove.
  Four verification gates, strict yield, digest as first-class
  residue. Books, transcripts, courses, doc sets.
- **[skillbun](skills/skillbun/SKILL.md)** -- Skill bundler. Resolves
  dependencies, renames to avoid collisions, packages into `.skill` archives.

## Repo structure

```
.
├── .claude-plugin/           # plugin manifest for skills.sh
│   └── plugin.json
├── scripts/                  # repo utilities
│   ├── link-skills.sh        #   symlink all skills to ~/.claude/skills/
│   └── list-skills.sh        #   list all SKILL.md files
├── skills/                   # flat -- each skill is self-contained
│   ├── kiln/
│   ├── animate-it/
│   ├── htmlize/
│   ├── parallax/
│   ├── skillize/
│   ├── skillbun/
│   ├── goldengoal/
│   └── distill/
└── template/                 # starter SKILL.md
    └── SKILL.md
```

## Creating a new skill

1. Copy `template/SKILL.md` into a new directory under `skills/`
2. Name the directory to match the `name:` field in frontmatter
3. Write the instructions (keep SKILL.md under 500 lines)
4. Add the skill to `.claude-plugin/plugin.json`
5. Test: `./scripts/link-skills.sh` then invoke in your agent

Or: use `/skillize` after completing a workflow to auto-extract one.

## Contributing

1. Fork the repo
2. Create your skill under `skills/`
3. Validate: `name` matches directory, description under 1024 chars
4. Add to `.claude-plugin/plugin.json`
5. Open a PR

## License

[Apache 2.0](LICENSE)
