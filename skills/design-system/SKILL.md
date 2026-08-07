---
name: design-system
description: >-
  Design system for building any user interface: install a material
  contract into a repo, then generate, judge, and move against it.
  Fires on four branches: standing up a design system in a project
  that has none ("give this repo a design system", "set up our
  tokens/design language", a fresh template to make ours); building
  or restyling a surface once a system exists; judging whether a
  change earned its keep; and choosing fonts, icons, or a reference
  to work from. Generating one component is kiln's job and judging
  one diff is taste's — this skill installs the material and routes
  to them with it loaded.
---

# design-system

A design system you install into a repo, not a component library you
import. It makes taste structural: the material becomes a contract file
an agent reads before every UI touch, rejections become memory, and the
verdict becomes a step. The one-line test for anything it produces: **a
change that makes the surface prettier and the task harder must fail** —
that failure is *costume*, and it fails no matter how it photographs.

Load [references/doctrine.md](references/doctrine.md) once to calibrate on
*why*; it is not needed per-run.

## Gate

| Situation | Move |
|---|---|
| Repo has no `DESIGN.md` / `TASTE.md` | **Install** the system (below). |
| System installed, a surface to build or restyle | **Build** → route to kiln with the material loaded. |
| A change, diff, or redesign to judge | **Judge** → route to taste. |
| A motion decision | route to animate-it. |
| Choosing a font, icon set, or decomposing a reference | [references/catalog.md](references/catalog.md), then build. |
| One-off with no product life (a throwaway page) | Skip the system. Just build it. |

Ceremony scales with stakes. A component tweak in an installed system is a
one-line material lookup; standing up a system on a new product is the
full install.

This skill orchestrates three others that must be installed alongside it:
**kiln** (generate + audit surfaces), **taste** (verdict protocol), and
**animate-it** (motion). Where they are not present, do the step by hand
against this repo's references and say so.

## Install

Give a repo a design system. Four phases; each ends on a checkable state.

### 1. Classify

Name the surfaces before choosing anything. Brand surfaces (landing,
marketing) — design IS the product. Product surfaces (dashboard, admin,
auth) — design serves the task. Write down, per surface, the primary task
and the **protected functions**: the task path, the information the user
actually reads, labels, navigation, legal copy. Most taste failures are
brand moves applied to product surfaces; this list is what a later verdict
checks against.

Done when: every surface is labelled brand/product with its protected
functions written down.

### 2. Seed the material

**Design-system-first.** Before inventing anything, check
[references/catalog.md](references/catalog.md) §0: does an official design
system already govern this product's context (GOV.UK, USWDS, Polaris,
Primer, Material, Apple)? If it does, that system *is* the material —
adopt it, don't recreate it by hand, and skip kit selection. An aesthetic
(glassmorphism, editorial, brutalism) is not a system; seed a kit for it.

Otherwise, pick a kit from
[references/materials.md](references/materials.md) whose default density
and territory match the *primary task* — not the one that photographs best
(that choice is itself the first taste decision, and a `taste` verdict if
contested). Re-seed the hue for identity. Decide the radius token *now*,
before any component. Choose the font and icon set from
[references/catalog.md](references/catalog.md) §8–9 against its rules (no
saturated reflex; one icon set, one weight) — not by default. If kiln is
present, run its `kit` command to derive concrete OKLCH tokens; otherwise
adapt `assets/bisque.css` as the worked example.

Done when: a token file exists with one seed hue driving both light and
dark, one accent, one radius, and semantic states as token offsets — no
raw palette values.

### 3. Install the contracts

Copy the templates and fill every placeholder against the *actual* tokens:

- `assets/DESIGN.md.tmpl` → `DESIGN.md` — the material contract.
- `assets/TASTE.md.tmpl` → `TASTE.md` — ships seeded with structural
  scars; project scars accrete beneath them.
- `assets/bans.sh` → the repo (e.g. `scripts/`), pointed at the app/page
  dirs.

A contract that lies about what the code does is worse than none. If the
material changes later, rewrite `DESIGN.md` in the same commit.

Done when: `DESIGN.md` describes the real tokens, `TASTE.md` is present,
and `bans.sh` runs clean.

### 4. Wire the agents

Point the repo's `AGENTS.md` / `CLAUDE.md` at the two contracts so every
UI touch reads them first: "Read DESIGN.md before touching UI; TASTE.md
holds prior rulings; run bans.sh before shipping." Add the route-and-mount
audit to template-adoption checklists (demo routes, global widget mounts,
orphaned keyframes: earn their place or delete).

Done when: an agent opening the repo cold is directed to the material and
the scars before it writes a line of UI.

## Build · Judge · Move

Once installed, this skill is thin — it routes with the material as context:

- **Build** a surface → kiln's `craft`, with `DESIGN.md` loaded as the
  material and the surface's brand/product class set. Self-audit against
  the material and `bans.sh` before presenting.
- **Judge** a change → taste's verdict protocol: protected functions
  first, count what changes, behavior before surfaces, verdict of *better
  / different / costume*. A rejection writes a scar into `TASTE.md`.
- **Move** → animate-it, honoring the material's motion law (no urgency
  devices, `prefers-reduced-motion` respected).

## Check

Smash the delivered system if any survive:

- `DESIGN.md` describes tokens the code doesn't actually use — a contract
  that lies.
- Two corner languages, or semantic states from raw palette classes —
  `bans.sh` would catch these; it wasn't run.
- A kit adopted whole with its DESIGN.md left describing the old material.
- Fonts or icons chosen by reflex (a saturated face, mixed icon sets)
  rather than from [references/catalog.md](references/catalog.md)'s rule.
- A material invented from scratch inside a context an official design
  system already governs (the design-system-first check was skipped).
- Template adoption with no route-and-mount audit — demo routes and widget
  mounts still shipping.
- A surface that photographs better and made the task harder, shipped as
  "better." That is costume; the verdict step exists to catch it.

## Lineage

Distilled from a source-verified vault: the Apple Human Interface
Guidelines lineage (1980–1992), the impeccable / taste-skill ecosystem,
and the reference-library practice for feeding agents visual coordinates.
The material engine and verdict protocol are the kiln / taste / animate-it
skills; this skill installs the material and routes to them. The costume
test is theirs by demonstration; the contract-install method is ours.
