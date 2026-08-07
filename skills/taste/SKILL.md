---
name: taste
description: >-
  Design judgment protocol: evidence before opinion, behavior before
  surfaces, mechanism over skin. Fires on three branches: delivering
  a verdict on a design change ("is this actually better?", a UI
  diff or before/after review, "did the redesign work"); decomposing
  references into a buildable brief ("make it like Linear", a
  screenshot to imitate, an inspiration list); and recording a
  design rejection as a reusable scar. Designing or restyling the
  surface itself is kiln's job — this skill judges whether the
  result earned its keep.
---

# Taste

Taste is judgment anchored in evidence, exercised on behavior before
surfaces. The one-line test: a change that makes the surface prettier
and the task harder must fail. That failure has a name — **costume** —
and interfaces die of it looking their best.

## Gate

| Situation | Move |
|---|---|
| Clear call: obvious regression, obvious win, stated preference | Answer directly. No protocol. |
| A surface to design, restyle, or rescue | kiln's job. Return here to judge the result. |
| A change, choice, or direction to judge | Verdict protocol. |
| A reference to apply ("like X", screenshot, moodboard) | Brief protocol. |
| A design just got rejected | Write the scar. Nothing else. |

Ceremony scales with stakes: a button-label call gets Evidence and
Verdict in two sentences; a redesign of a revenue path gets all five
phases.

## Verdict protocol

### 1. Stakes

Name what the surface is for before judging how it looks.

- **Brand or product?** On a brand surface, design IS the product and
  expressiveness is load-bearing. On a product surface, design serves
  the task and expressiveness competes with it. Most judgment errors
  are brand standards applied to product surfaces.
- **What must not break?** List the protected functions: the primary
  task path, information the user actually reads, labels and
  navigation, legal copy, the conversion path.

Done when the protected-function list is written down. A redesign
judged without this list trades function for polish silently — that
is how dashboards lose their data and still get praised.

### 2. Evidence

Judge the thing, not its description. Render it, screenshot it, or
walk the diff; then walk the primary task path start to finish.
Detector and script output count as evidence, never proof — a clean
automated pass says nothing about whether the design is strong.

Count what is countable before opining: facts visible above the fold
before vs after, steps to complete the task before vs after, labels
renamed or dropped. Counts turn "feels cleaner" into a checkable
claim.

Done when every sentence the verdict will contain has an observation
behind it.

### 3. Behavior

Surfaces are the last thing to judge, not the first. Load
[invariants.md](references/invariants.md) and check the change
against the behavioral invariants: visible state, reversibility over
confirmation, verbs on buttons, discoverable paths, honest feedback,
escapable modes. These outrank every visual consideration because
they decide whether the user's mental model survives the change —
and forty years of interface history has not moved them.

Done when each invariant is marked pass, fail, or not-applicable.

### 4. Verdict

Three verdicts exist:

- **better** — the task got easier or stayed equal, protected
  functions are intact, and at least one named mechanism improved.
- **different** — taste swapped, nothing gained. Say so plainly;
  "different" dressed up as "better" is how redesign budgets die.
- **costume** — prettier surface, harder task. Fails regardless of
  how good it looks in a screenshot.

Every judgment sentence carries its mechanism: not "cleaner" but
"nav went from 7 items to 4 by grouping billing actions". An
adjective without a mechanism is an opinion wearing a verdict's
clothes. When the call is genuinely contested, present both
steelmen and name the variable that decides it — a visible tie is
more useful than false confidence.

Close with the second-reflex check: if this change replaces a
predictable default, is the replacement also predictable? (Every
anti-generic redesign converging on the same editorial serif is the
second training-data reflex.) kiln owns the visual convergence
rules; the verdict owns the honesty about them.

### 5. Scar

Only on rejection — see Scars below. A verdict that ends in
rejection and leaves no scar will be re-litigated from zero next
session.

## Brief protocol

A reference arrives — "make it like Linear", a screenshot, an
inspiration list. Imitating its skin produces a worse copy of
someone else's decisions. Decompose it instead:

1. **Design-system-first.** Does an official design system already
   govern this context (government, platform admin, established
   brand)? Then the brief is that system, not an invention. An
   aesthetic — glassmorphism, brutalism, editorial — is not a
   system; do not promote it to one.
2. **Extract the mechanism, not the palette.** Per reference, answer:
   why does this hero work, what does the motion redirect attention
   to, how does it degrade on mobile, why is the CTA there? One
   transferable mechanism per reference beats ten screenshots. A
   reference whose beauty rides on assets you don't have
   (photography, 3D) is a trap — note it and move on.
3. **Write the brief:** mechanisms to keep, constraints (performance,
   density, accessibility floors), protected functions, and
   acceptance criteria two engineers would verify identically.

Hand the brief to kiln or whoever builds. Done when the brief
contains zero site names used as instructions — "like Linear"
decomposed into what Linear does that transfers here.

## Scars

Experimental: taste that compounds. Rejections are the most
expensive design signal a project produces, and by default they
evaporate. Keep `TASTE.md` at the project root; append one scar per
real rejection:

```markdown
## 2026-07-21 rejected: metric cards hid the raw table
Why: primary persona scans 30 rows to spot anomalies; cards cut
visible rows from 30 to 6. Prettier, slower.
Reuse: on analyst-facing surfaces, density is a feature; summarize
above the data, never instead of it.
Expires: if the anomaly workflow moves to alerts.
```

The why is the load-bearing part. Rules with whys adapt to new
cases; naked bans fossilize into style police, and an expired scar
is the new purple gradient. Read `TASTE.md` at the start of any
verdict — scars are prior rulings. Delete a scar the moment its
expiry condition arrives.

## Check

Smash the verdict if any of these survive:

- A claim with no observation behind it — the description got
  judged, not the thing
- An adjective with no mechanism attached
- A costume passed because it photographed well
- A protected function silently dropped
- An automated pass treated as proof
- A scar written as a naked ban
- The second reflex unexamined

## References

| Reference | When to load |
|---|---|
| [invariants.md](references/invariants.md) | Verdict phase 3, always; Brief protocol step 3 for acceptance-criteria material |

## Lineage

Distilled from a source-verified research vault: the Apple Human
Interface Guidelines lineage (Lisa 1980 → HIG 1987/1992),
pbakaus/impeccable (Apache-2.0), Leonxlnx/taste-skill (MIT), and
the HN threads that killed prettier-but-less-useful on sight. The
costume test is theirs by demonstration; the protocol is ours.
