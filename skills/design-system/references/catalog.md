# Reference catalog

Where to look, by what you're trying to do — and what to *take* from each.
The discipline that makes this a catalog and not a mood board:
**references give visual coordinates, not answers.** Copying a skin
produces a worse copy of someone else's decision. For every reference,
extract the *mechanism* — why does this work, what does the motion
redirect attention to, how does it degrade on mobile, why is the element
there — then write it into the brief as a constraint. A reference whose
beauty rides on assets you don't have (photography, 3D, a licensed
typeface) is a trap; note it and move on. Curated for authority and
function, not volume.

## Contents — open the section you need

| § | Section | Open it when you need to… |
|---|---|---|
| [0](#0-design-system-first) | Design-system-first | decide whether to design from scratch at all |
| [1](#1-foundations) | Foundations (historical) | settle a first-principles interaction question |
| [2](#2-principles--usability) | Principles & usability (modern) | give a UX decision a *reason*, not a picture |
| [3](#3-animation--motion) | Animation & motion | find motion / interaction reference |
| [4](#4-aesthetic--layout) | Aesthetic & layout | find first-screen structure, section rhythm |
| [5](#5-product-flows--behavior) | Product flows & behavior | see how real products handle a flow or state |
| [6](#6-components) | Components | pull a component fast |
| [7](#7-color--contrast) | Color & contrast | build or verify the color ramp |
| [8](#8-fonts) | Fonts | choose a typeface (and dodge the reflex) |
| [9](#9-icons) | Icons | choose an icon set |
| [10](#10-prior-art--method) | Prior art & method | study the approach itself |

Awwwards and its kin are a **boundary, not a baseline**: they reward
expressive, brand-campaign work. Pulling that onto a product surface
over-designs it. Use them to see the edge of the space, not the default.

## 0. Design-system-first

Before you invent tokens, ask: **does an official design system already
govern this product's context?** If it does, that system *is* your
material — adopt it, don't recreate it by hand. This is the
highest-leverage check in the catalog; most "design from scratch" work in
a governed context is wasted or wrong.

| System | Where | Reach for it when |
|---|---|---|
| GOV.UK Design System | [design-system.service.gov.uk](https://design-system.service.gov.uk/) | government / civic / regulated public service — legally or institutionally expected |
| U.S. Web Design System | [designsystem.digital.gov](https://designsystem.digital.gov/) | U.S. federal / public-sector |
| Shopify Polaris | [polaris.shopify.com](https://polaris.shopify.com/) | anything embedded in the Shopify admin |
| GitHub Primer | [primer.style](https://primer.style/) | GitHub-adjacent developer tooling |
| Material 3 | [m3.material.io](https://m3.material.io/) | Android-first or explicitly Material products |
| Apple HIG (current) | [developer.apple.com/design](https://developer.apple.com/design/human-interface-guidelines) | native Apple-platform apps |

An **aesthetic** — glassmorphism, brutalism, editorial, dark-tech — is not
a design system. It has no official package, no components, no a11y
contract. Adopt an official system; *seed a material kit* for an aesthetic.

## 1. Foundations

The historical sources behind `doctrine.md`. Consult when settling a
first-principles interaction question — modes, reversibility,
disabled-not-hidden, feedback, what a button should say. Read the source,
not a paraphrase, when a rule is contested.

| Source | Where | What it settles |
|---|---|---|
| Apple HIG 1987 (ten principles) | [archive.org PDF](https://archive.org/download/apple-hig/Apple_Human_Interface_Guidelines_1987.pdf) | the canonical principle list; behavior before surfaces |
| Macintosh HIG 1992 | [archive.org PDF](https://archive.org/download/apple-hig/Macintosh_HIG_1992.pdf) | the concrete rules — microcopy, modes, icons, alerts |
| Lisa UI Standards 1980 / Guidelines 1983 | [1980](https://archive.org/download/apple-hig/1980_Lisa_UI_Standards.pdf) · [1983](https://archive.org/download/apple-hig/1983_Lisa_UI_Guidelines.pdf) | the earliest behavioral specs; modelessness |
| Susan Kare interview | [Stanford](https://web.stanford.edu/dept/SUL/sites/mac/primary/interviews/kare/mac.html) | icon design as recognition, tested at actual size |
| Folklore: Inside Macintosh | [folklore.org](https://www.folklore.org/Inside_Macintosh.html) | how the guidelines and the Toolbox became one system |
| Complete HIG archive (1978–2014) | [gingerbeardman/apple-human-interface-guidelines](https://github.com/gingerbeardman/apple-human-interface-guidelines) | every historical edition in one repo |

## 2. Principles & usability

The living *why*, complementing §1's historical sources. Reach for these
when a decision needs a reason, not a picture.

| Source | Where | Reach for it when |
|---|---|---|
| Laws of UX | [lawsofux.com](https://lawsofux.com/) | naming *why* a layout works (Fitts, Hick, Jakob, Miller, Doherty) |
| Nielsen Norman Group | [nngroup.com](https://www.nngroup.com/) | you need usability *evidence* for a flow or pattern choice |
| Refactoring UI | [refactoringui.com](https://www.refactoringui.com/) | a layout "feels off" but you can't say why — hierarchy, spacing, depth |
| Inclusive Components | [inclusive-components.design](https://inclusive-components.design/) | building any component with state (menus, tabs, toggles) accessibly |

## 3. Animation & motion

| Source | What it is | Mechanism to take |
|---|---|---|
| [landing.love](https://www.landing.love/) | ~2,100 animated sites, full-page video capture | scroll reveals, hero motion, transition timing — *what attention shift each move serves* |
| [framer.com/gallery](https://www.framer.com/community/gallery/) | Framer templates + motion prototypes | interaction choreography; watch for template homogeneity |
| [easings.net](https://easings.net/) | named easing curves, previewed | picking an easing that isn't the default `ease` |

Deciding *whether* a thing should move and *how* is `animate-it`'s job —
the catalog finds the reference, animate-it makes it move correctly.

## 4. Aesthetic & layout

| Source | What it is | Mechanism to take |
|---|---|---|
| [land-book.com](https://land-book.com/) | hand-picked galleries (landing/portfolio/blog/ecommerce) | first-screen structure, section rhythm, type pairing |
| [godly.website](https://godly.website/) | tightly curated high-craft web design | where the current ceiling of taste actually is |
| [siteinspire.com](https://www.siteinspire.com/) | brand/studio/content sites by style/type | editorial layout, restraint; often photography-driven — check |
| [onepagelove.com](https://onepagelove.com/) | single-page sites + free templates | short-narrative structure for launches, events, one-product pages |
| [lapa.ninja](https://www.lapa.ninja/) | large landing-page volume | structural patterns at scale (filter hard, quality varies) |
| [awwwards.com](https://www.awwwards.com/) | award gallery, annual trend reports | the creative *boundary* and where the year's language is heading |

Galleries solve visual imagination, not effectiveness. A pretty page has
no conversion data attached; some ugly pages convert better. Judge against
the task, not the screenshot. Single-page structures skew toward heavy JS
and weak accessibility — fit for launches, not information-dense products.

## 5. Product flows & behavior

The underrated corner. Not inspiration — *product behavior evidence*.

| Source | What it is | Mechanism to take |
|---|---|---|
| [mobbin.com](https://mobbin.com/) | ~400k app screens, full flows, states, [Copy-to-Figma](https://mobbin.com/changelog/2024-02-08-copy-to-figma) | onboarding steppers, empty/error/loading states, paywalls, settings |
| [refero.design](https://refero.design/) | searchable real app UI, web + mobile | a specific screen or flow in context ("how does X do settings") |

When an agent builds UI, what it lacks is rarely button styling — it is
flow judgment (what the empty state says, how the paywall gates, where the
error lands). This is the reference that most improves function.

## 6. Components

| Source | What it is | Note |
|---|---|---|
| [ui.shadcn.com](https://ui.shadcn.com/) | the token-driven primitive set most agents already build on | the durable base; owns your `components/ui`, managed by its generator |
| [ui.aceternity.com](https://ui.aceternity.com/) | React/Tailwind/Framer-Motion copy-paste components | speeds implementation; heavy "component smell" — unify under your tokens |
| [21st.dev](https://21st.dev/) | community React registry, AI-ready prompts | quality varies, filter; pairs with agent codegen |

Components solve *speed*, not taste, and accelerate homogenization —
everyone copying the same hero/bento/spotlight lands on the template look
in three months. Adopt the structure, re-skin to your material, delete the
borrowed animation defaults.

## 7. Color & contrast

Color lives in the token layer (the material). These build and verify the
ramp — reach for them when seeding a kit's palette, not per-component.

| Source | Where | Reach for it when |
|---|---|---|
| OKLCH picker | [oklch.com](https://oklch.com/) | building tokens in the same space the material system uses |
| Radix Colors | [radix-ui.com/colors](https://www.radix-ui.com/colors) | you need 12-step accessible scales, light+dark paired, not hand-tuned |
| Realtime Colors | [realtimecolors.com](https://www.realtimecolors.com/) | previewing a palette live on a real UI before committing |
| Huemint | [huemint.com](https://huemint.com/) | an AI palette seeded by your hue — a coordinate to react to, not an answer |
| WebAIM Contrast Checker | [webaim.org](https://webaim.org/resources/contrastchecker/) | verifying every text-on-surface pair — the accessibility floor |

## 8. Fonts

No gallery substitutes for judgment; the work is choosing a pairing that is
*not the reflex* and committing.

Browse / discover:

- [Typewolf](https://www.typewolf.com/) — fonts seen in the wild, with
  pairings; best "what does this face feel like in use" source
- [Fonts In Use](https://fontsinuse.com/) — typography indexed by industry
  and typeface; study how a face behaves at scale
- [Fontshare](https://www.fontshare.com/) — quality free-for-commercial
  faces that are *not* on every AI-generated page
- [Google Fonts](https://fonts.google.com/) — ubiquitous and free, which is
  exactly why its top-ten are saturated tells

The rule (this is the taste, not the source):

- **Avoid the saturated reflexes.** Inter, Roboto, Poppins, Montserrat, DM
  Sans, Plus Jakarta on the sans side; Playfair, Fraunces, Cormorant,
  Instrument Serif on the display side; Space Grotesk/Space Mono for
  "techy." If your reflex reaches for one, look further. (kiln's zeitgeist
  file versions the current list.)
- **Pair on an axis** (serif×sans, geometric×humanist) or run **one family
  across weights** — often stronger than two weak pairings.
- **System fonts are underrated** (`-apple-system`, `system-ui`): native
  feel, instant load, no saturation tell. Default when performance beats
  personality.
- **CJK-primary product → pick and preload the CJK face first**, then a
  Latin face that harmonizes with its proportions. Never host the identity
  on Latin while CJK is an unpreloaded fallback.

## 9. Icons

| Source | What it is | Note |
|---|---|---|
| [iconify.design](https://iconify.design/) | one unified API over 150+ open sets (~200k icons: Lucide, Phosphor, Tabler, Material Symbols, Heroicons…) | *browse everything in one place*, pull from any set without per-library installs |
| [Lucide](https://lucide.dev/) | clean, consistent open set (shadcn default) | strong default — distinctive enough, but reads as "shadcn app" if left untouched |
| [Phosphor](https://phosphoricons.com/) | large set, six weights (thin→fill) | pick ONE weight and hold it |

The rule (iconify makes the failure mode easy, so state it loudly):

- **Browse via Iconify; commit to one set.** The trap is mixing glyphs from
  three sets because they're all one search away. One family reads as
  intentional; a mix reads as accidental.
- **One stroke weight across the whole interface.** Pick 1.5 or 2.0 and
  commit — mismatched weights are the icon version of a flat type hierarchy.
- **Icon + label for anything abstract or multi-state.** Icons carry nouns
  well and actions poorly. Icon-only is earned by binary universal actions
  (close, search), tested for recognition — not chosen because it's tidier.

## 10. Prior art & method

The agent-native design-tooling this practice learned from. Read them to
understand the *method* — contract files, deterministic detectors, the
anti-slop framing — not to lift text.

| Repo | What it is | What to study |
|---|---|---|
| [pbakaus/impeccable](https://github.com/pbakaus/impeccable) | one skill, ~23 commands, browser iteration, ~46 detector rules | brand-vs-product split; `PRODUCT.md`/`DESIGN.md` context files; "automated output is evidence, not proof" |
| [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) | portable anti-slop frontend SKILL.md | design-system-first mapping; variance/motion/density dials; where bans over-reach into style-police |
| [lroolle/skills](https://github.com/lroolle/skills) | kiln (generate), taste (judge), animate-it (move) | the engine this skill orchestrates — one home for the tools |

## Using the catalog in a brief

Decompose, don't imitate. For each reference the user cites ("make it like
X"), write: the mechanism it contributes, the constraint it implies, and
the acceptance criterion two engineers would verify identically. Hand
*that* to whoever builds. A brief that still contains a site name used as
an instruction ("like Linear") has not been decomposed yet.
