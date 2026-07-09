<div align="center">

<pre>
     _    _ _ _
 ___| | _(_) | |___
/ __| |/ / | | / __|
\__ \   &lt;| | | \__ \
|___/_|\_\_|_|_|___/
</pre>

**Nine small skills with strong opinions — and gates that say no.**

design · motion · artifacts · decisions · goals · the craft of skills itself

[![skills.sh](https://skills.sh/b/lroolle/skills)](https://skills.sh/lroolle/skills)
[![license](https://img.shields.io/github/license/lroolle/skills)](LICENSE)
[![spec](https://img.shields.io/badge/spec-agentskills.io-blue)](https://agentskills.io/specification)

[Quickstart](#quickstart) · [The skills](#the-skills) · [Proof](#proof) · [Doctrine](CLAUDE.md) · [llms.txt](llms.txt)

<sub>AI agents: fetch [llms.txt](llms.txt) — one line per skill, with raw links.</sub>

</div>

---

Most agent output is competent and forgettable: the purple-gradient
dashboard, the 300-line plan nobody reads, `transition: all`, the
first reasonable answer polished until it ships. These skills exist
to refuse that. Each one is a protocol that opens with a gate, and
the gate's favorite word is no:

```text
> make this dashboard look better

  kiln · gate: "AI tool -> Inter + purple gradient" is the first
  training-data reflex. Refused. Firing broadsheet kit: serif
  display, ruled 1px surfaces, 0.85 density...

> should this shortcut animate?

  animate-it · gate: keyboard-initiated, fires 200x/day.
  No animation. Ever.
```

*Illustrative transcript; the refusals are verbatim from the
skills' own rules. Sizing the task before spending your tokens is
the product.*

## Quickstart

```bash
npx skills@latest add lroolle/skills
```

Pick the skills you want and which agents to install them on.
Then feel one work — say any of these:

| Say | Fires |
|---|---|
| "audit this repo's README" | burnish |
| "should this modal animate?" | animate-it |
| "run /parallax on \<a decision you're stuck on\>" | parallax |
| "turn this session into a skill" | skillize |

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

## The skills

Each entry: what it does in one line, and the itch it scratches
behind the fold.

**[kiln](skills/kiln/SKILL.md)** — precision UX design instrument:
perceptual principles → composable patterns → six material kits,
with anti-AI-slop detection. Generates and audits.

<details><summary>the AI-generated look</summary>

Most AI-built interfaces are instantly recognizable: Inter font,
purple gradient, card-in-card layouts, magnetic cursor effects.
They converge on the same defaults because agents reach for
training-data reflexes. kiln separates permanent perceptual rules
(human vision doesn't change) from temporal taste (what's
saturated right now), ships six material kits with distinct
personalities, and versions a zeitgeist file tracking which
aesthetics have been strip-mined by AI generators.

</details>

**[animate-it](skills/animate-it/SKILL.md)** — animation
implementation protocol: gate → classify → specify → code → check.
Custom easing, duration tables, tool selection, review rubric.

<details><summary>the animation that doesn't feel right</summary>

Agents add animation the way they add comments: everywhere,
uniformly, without judgment. `transition: all`, scale(0)
entrances, ease-in on exits, motion on keyboard actions that fire
a hundred times a day. animate-it codes against the rules that
separate "has animation" from "feels right" — kiln decides what
should move and why; animate-it makes it move correctly.

</details>

**[htmlize](skills/htmlize/SKILL.md)** — HTML artifact protocol:
gate → shape → build → check. Self-contained files, calm
typography, build-time diagram pipeline, clipboard exports.

<details><summary>the wall of markdown</summary>

Agents produce 300-line markdown plans nobody reads. Comparisons
get stacked instead of side-by-side, timelines become bullet
lists, anything interactive gets described instead of built. The
fix isn't "always output HTML" — generated HTML has its own
failure modes: slop styling, lost git diffs, dead-end editors.
htmlize gates first (does this beat markdown?), and markdown
stays the source of truth.

</details>

**[parallax](skills/parallax/SKILL.md)** — multi-perspective
decision protocol: frame → spread → commit. Genuinely different
alternatives, trap detection as a first-class operation.

<details><summary>the first answer that sticks</summary>

Claude picks the first reasonable approach and builds on it. For
decisions that are expensive to reverse — architecture, naming,
strategy — that produces competent, forgettable output. The real
cost isn't a bad answer; it's never seeing the better one because
you stopped looking. parallax forces 3-5 approaches that differ
on fundamental assumptions, surfaces the traps, then commits with
explicit trade-offs. One context, zero infrastructure.

</details>

**[goldengoal](skills/goldengoal/SKILL.md)** — goal engineering:
compose intent into a contract, or sharpen a draft against five
gates. Produces a goal brief + `/goal` condition.

<details><summary>the goal that drifts</summary>

You set `/goal` and the agent runs for an hour — then you discover
it built the wrong thing. The goal was vague, the scope open, the
verification "looks good"; the agent filled every ambiguity gap
with its own assumptions. goldengoal shapes fuzzy intent into a
falsifiable contract before execution: outcome, evidence,
boundary, stop rules, pause conditions — weighted to task
complexity, so a typo fix gets three lines, not a ceremony.

</details>

**[skillize](skills/skillize/SKILL.md)** — session-to-skill
crystallizer: survey the conversation, classify corrections by
durability, extract the repeatable pattern, draft the SKILL.md.

<details><summary>the workflow you can't repeat</summary>

You spend 40 minutes getting an agent to do something perfectly —
tool sequences, corrections, domain knowledge discovered along the
way. Next week you need the same workflow and start from scratch.
skillize preserves the workflow, not just the output.

</details>

**[distill](skills/distill/SKILL.md)** — source-to-skills
distiller: gate → survey → hunt → earn → shape → prove. Four
verification gates, strict yield, digest as first-class residue.

<details><summary>the book you read but never use</summary>

You read a methodology book, highlight half of it, and a year
later make the same decisions you would have made anyway. distill
turns a source into the few skills it actually earns — every unit
must be grounded in 2+ passages, predictive beyond the examples,
non-obvious, and behavioral. Most sources earn 0-3 skills; the
rest becomes an honest digest that says what didn't make it and
why.

</details>

**[skillbun](skills/skillbun/SKILL.md)** — skill bundler: resolve
inter-skill dependencies, rename to avoid collisions, package into
one `.skill` archive.

<details><summary>skills that can't travel alone</summary>

You build a skill that depends on another skill's scripts. You
share the `.skill` file and the recipient's pipeline silently
breaks because the dependency isn't there. skillbun ships the
whole graph as one file.

</details>

**[burnish](skills/burnish/SKILL.md)** — repo packaging and
promotion: audit → renovate → instrument → tell, in trust-damage
order. README anatomy, honest numbers, agent surfaces, automation
tripwires.

<details><summary>the great work nobody sees</summary>

You shipped something real. But the README opens with install
instructions, the last release trails the commits by a year, and a
scheduled job has been green-but-dead for weeks. Visitors spend 30
seconds, impute neglect, and leave — the work was never the
problem. burnish works the surfaces until they read what is
actually true, and its law never inverts: work → proof →
packaging → telling. This README is its output.

</details>

## Proof

Claims about craft should be checkable:

| Claim | Check |
|---|---|
| Nine skills, each a self-contained folder | `ls skills/` |
| Every body ≤ 500 lines, every description ≤ 1024 chars | `./scripts/validate.sh` |
| Every skill registered and listed — no orphans | `./scripts/validate.sh` |
| Zero runtime dependencies: markdown, three shell scripts | `ls scripts/` |

`validate.sh` is the reproduce command; it exits non-zero on any
violation, so CI and skeptics get the same verdict.

## When to use · when to skip

Use this collection if you want protocols with taste built in —
gates that size the task, refusals where the defaults are slop,
and completion criteria an agent can actually check.

Skip it if:

- you want breadth-first coverage —
  [anthropics/skills](https://github.com/anthropics/skills) is the
  official library and covers far more ground
- you want an orchestration framework — these are single-context
  protocols; there is deliberately no infrastructure here
- you disagree with the opinions — they are load-bearing, not
  decoration; fork and re-season rather than fight the gates

## Kin

These skills stand on named shoulders:

| Collection | What we took, with thanks |
|---|---|
| [mattpocock/skills](https://github.com/mattpocock/skills) | writing-great-skills gave the doctrine its vocabulary — predictability, leading words, the no-op test (MIT) |
| [kangarooking/cangjie-skill](https://github.com/kangarooking/cangjie-skill) | the book-to-skills pipeline distill adapts to strict yield (MIT) |
| [UditAkhourii/adhd](https://github.com/UditAkhourii/adhd) | parallel-frame divergence, traded by parallax for a zero-infra single context |
| [headroomlabs-ai/headroom](https://github.com/headroomlabs-ai/headroom) | the repo-packaging study behind burnish (Apache-2.0) |

## Creating a new skill

1. Copy `template/SKILL.md` into a new directory under `skills/`
2. Name the directory to match the `name:` field in frontmatter
3. Write the instructions to the [doctrine](CLAUDE.md) — gate
   first, one trigger per branch, under 500 lines
4. Register it in `.claude-plugin/plugin.json` and list it here
5. `./scripts/validate.sh`, then `./scripts/link-skills.sh` and
   invoke it in your agent

Or: use `/skillize` after completing a workflow to auto-extract
one.

## Contributing

Fork, build your skill under `skills/`, run
`./scripts/validate.sh`, open a PR. Opinions welcome; slop
refused.

## License

[Apache 2.0](LICENSE)
