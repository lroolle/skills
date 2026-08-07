# Doctrine

Why this design system exists, and the few load-bearing beliefs
everything else derives from. Load this once to calibrate; the
operational rules live in SKILL.md and the other references.

## The thesis

**Taste is judgment anchored in evidence, exercised on behavior before
surfaces.** Not a style, not a palette, not an aesthetic. The one-line
test that falls out of it: *a change that makes the surface prettier and
the task harder must fail.* That failure has a name — **costume** — and
interfaces die of it looking their best.

Three independent traditions converge on this and none of them is about
looks:

- **Behavior before surfaces.** The 1987 Apple Human Interface Guidelines
  list ten principles; nine are behavioral (direct manipulation,
  see-and-point, user control, forgiveness, perceived stability…) and
  "aesthetic integrity" is *tenth*, defined as *communication*, not
  decoration. Early Apple designed the user's transferable mental model
  first; the surface served it.
- **Evidence over opinion.** When a design tool shipped prettier
  before/after examples, practitioners killed them on sight — "the
  dashboard looks more organized, but that's because it lost most of its
  useful information" — and the author conceded and pulled them. Automated
  passes are evidence, never proof; you judge the real interaction path.
- **Mechanism over skin.** References give an agent visual coordinates,
  not answers. Copying a hero's gradient produces a worse copy of someone
  else's decision; extracting *why the hero works* transfers. Quality
  comes from decomposing references into mechanisms, constraints, and
  acceptance criteria.

## The failure this is built against

Most AI-built interfaces are recognizable in three seconds — one saturated
sans, one purple gradient, glass cards, a pulsing "limited offer," a
pricing page for plans that don't exist. That is not a style problem; it
is a *judgment* problem. Nothing in a normal stack ever asks whether a
change served the user or just the screenshot. This skill makes that
question structural: it installs the material as a contract, the scars as
memory, and the verdict as a step.

The second-order trap: replacing one default with another. "No purple
gradient" becomes "editorial serif on warm-black" — a new monoculture.
Anti-slop is adversarial; once a tell is known, the tell moves. So this
skill does not ship a *look*. It ships a **method** and a set of material
*kits* you re-seed, plus a running memory (TASTE.md) that keeps the bans
from fossilizing into the next reflex.

## What that makes it

A design system you install into a repo, not a component library you
import:

- **A material** — tokens, type, radius, motion — as a contract file
  (`DESIGN.md`) an agent reads before every UI touch.
- **A memory** — rejections recorded as scars with their *why*
  (`TASTE.md`), so taste compounds instead of restarting each session.
- **Deterministic bans** — the scars that can be grepped, as a runnable
  check (`bans.sh`).
- **A judgment loop** — the verdict protocol (better / different /
  costume) that runs before a change ships.
- **Tools** — generate (kiln), judge (taste), move (animate-it) — that
  operate *with the installed material as context*.

The behavioral floor beneath all of it (visible state, verbs on buttons,
disabled-not-hidden, reversibility, honest feedback, labels on
multi-state controls) predates the web and outranks every visual
consideration. A redesign that violates it to look better is costume by
definition.
