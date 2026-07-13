---
name: burnish
description: >-
  Burnish a repo until the work gleams -- people impute the quality
  of the work from the quality of its surfaces, so audit, renovate,
  instrument, and promote open-source repos until real work reads
  as real in 30 seconds and every claim survives scrutiny. Fires on
  four branches: polishing or launching a repo ("make this repo
  world-class", "fix the README", "prepare for launch", "why does
  this look abandoned"); org-wide housekeeping ("run housekeeping",
  "which repos are stale", scheduled groundskeeper sweeps); outbound
  moments ("write the release notes", "announce this", "make people
  care"); and automation health ("set up a scheduled workflow",
  "why did nobody notice this broke"). Fixing a single bug is just
  a fix; product UI design is kiln's job; voice for one standalone
  document is a writing task, not repo packaging.
---

# Burnish

Burnishing is polish by friction: press the tool against real
metal until it gleams. It only works on substance -- friction
against hollow plating wears straight through and shows the base
underneath. That is this skill's physics, and why its beats run
in order.

The belief behind it: people impute the quality of the work from
the quality of its surfaces -- "people DO judge a book by its
cover" (Apple Marketing Philosophy, 1977). A repo is a product
whose UI is its README, whose uptime is its maintenance signals,
and whose marketing is proof. Humans decide in ~30 seconds
whether it is serious. Agents decide from llms.txt and topics.
Adopters decide from whether claims survive scrutiny. Burnish
works the surfaces until all three read what is actually true.

**The law, in order. Never invert it:**

1. Work that solves a real problem (substrate — not this skill's job)
2. Proof that it works (measure before you claim)
3. Packaging that transfers understanding in seconds
4. Telling people, with taste

Promotion without proof is cargo cult. Proof without packaging is
invisible. The failure mode of strong engineers is stopping at 1
and resenting that nobody arrives; the failure mode of marketers
is starting at 4. Run the beats in order.

## Gate

Confirm the situation is repo packaging, maintenance, or
promotion. Route away: a single bug fix is just a fix; UI or
product design is kiln's job; the voice of one standalone
document is a writing task, not repo packaging. If the repo's
core does not work yet, say so and stop — burnish amplifies
substance, it cannot replace it.

Scale check before anything else: a 2-star repo and a 50k-star
repo deserve different wardrobes. Every artifact below must earn
its place at THIS repo's scale (see Boundaries).

## Beat 1 — Audit

Score the repo before touching it. Fifteen minutes, one pass:

| Surface | Check |
|---|---|
| Identity | GitHub description states outcome + numbers, not category? Homepage set (docs site or Pages when one exists)? Topics: 8-20 covering every discovery keyword a searcher would type? |
| README | Follows the anatomy? (references/readme-anatomy.md) Has a Proof section? A 60-second start that actually takes 60 seconds? |
| Agent surface | llms.txt exists? Plugin/marketplace integration where the product warrants it? (references/agent-surface.md) |
| Health files | LICENSE, SECURITY.md, CONTRIBUTING.md, issue/PR templates, CHANGELOG — present and non-boilerplate? (references/health-stack.md) |
| Release hygiene | Tagged releases ≈ recent commits? Or does the repo ship daily but "release" never? |
| Automation honesty | Any scheduled job green while producing nothing? Check the OUTCOME artifact (latest commit/PR/release/post), not the run status. (references/automation-tripwires.md) |
| Drift | Renamed products still under old names? Dates/screenshots/counts stale? Branch count vs open PRs? Org index, GitHub Pages, and docs sites current? |

Output: gap list ranked by trust damage, each gap with an effort
estimate — a dead link or a stale "© 2025" hurts more than a
missing badge, because it signals abandonment. Staleness is the
#1 trust killer; absence is #2; excess flair is #3.

## Beat 2 — Renovate

Fix in trust-damage order, shipped as reviewable PRs (one concern
per PR):

1. Kill drift first: dead names, stale dates, wrong descriptions,
   broken examples. Cheap, and it flips the "abandoned?" verdict.
2. Rewrite the README to the anatomy — ordered by reader decision
   state, not by feature: hook with numbers first, proof before
   depth, an honest anti-pitch, depth collapsed until wanted. The
   16 slots with examples: references/readme-anatomy.md. Every
   number obeys references/honest-numbers.md.
3. Add the agent surface: llms.txt at repo root (generating and
   refreshing that file is the llms-txt skill's job), tuned topics,
   outcome-first description. references/agent-surface.md.
4. Backfill health files from references/health-stack.md — minimal
   viable versions, no corporate boilerplate.
5. Set up release cadence if commits outpace releases: conventional
   commits + automated release PRs (see health-stack.md), so
   "latest release" never reads as abandonment.

## Beat 3 — Instrument

Renovation decays. The case behind this beat
(references/automation-tripwires.md): a scheduled pipeline that
reported green four times a day for three weeks while producing
nothing, next to a year-stale org page. Durability comes from
instruments, not willpower:

- Every scheduled automation gets an outcome tripwire: assert the
  artifact exists (PR opened, post published, file changed), not
  that the script exited 0. references/automation-tripwires.md.
- Notifications fire only AFTER the proof artifact exists, and
  failure sends a louder notification than success.
- Pin moving dependencies (@main is an outage on a timer). Put
  agent permissions in parse-proof config files, not CLI strings.
- Repo settings: auto-delete merged branches; branch count is rot
  made visible.
- Schedule the groundskeeper (below) — monthly is enough for small
  orgs.

## Beat 4 — Tell

Only now. The outbound unit is a story with proof, not an
announcement:

- Lead with the problem the reader has, then the number that
  proves you fixed it, then the 60-second path to feel it
  themselves. Same anatomy as the README, compressed.
- Release notes answer "why upgrade", not "what changed" — the
  changelog already says what changed.
- Every claim scoped and reproducible (references/honest-numbers.md).
  One honest "60-95% on JSON, 15-20% on code" outsells a vague
  "up to 95%" — specificity is what credibility sounds like.
- Credit competitors and dependencies generously. Attribution
  reads as confidence; silence reads as insecurity.
- Scale-gate the flair: star-history charts, trendshift badges,
  Discord servers come AFTER the audience exists. At small scale,
  taste means restraint.

## Groundskeeper cadence (recurring entry point)

For "run housekeeping" / scheduled sweeps across an org:

1. Enumerate repos; for each, pull staleness signals: last release
   vs last commit, scheduled-run status vs latest outcome artifact,
   open PR age, branch count, description/homepage drift.
2. Rank by trust damage. Fix the smallest highest-damage item
   first; file issues for the rest.
3. Verify org-level surfaces: the org README/Pages index must list
   current repos with current descriptions — it is the storefront.
4. Report: what was fixed, what drifted since last sweep, what
   needs a human decision. A sweep that finds nothing should say
   what it checked.

## Completion criteria

- Audit: gap list ranked by trust damage, with effort estimates.
- Renovate: PRs open; README passes the 30-second test (a
  stranger can say what it is, why care, how to start).
- Instrument: every scheduled job has an outcome assertion; a
  deliberately broken dry-run turns red, not green.
- Tell: draft leads with reader's problem + proof + 60-second
  path; zero unscoped claims.

## Boundaries

- Substance first: never run Beat 4 on a repo that fails Beat 1's
  proof checks. "Make it undeniable" precedes "tell the world".
- Scale-gate everything: a 50k-star repo runs 20 CI workflows, a
  Discord, and enterprise support — with a company behind it. A
  solo maintainer copying that wardrobe produces dead servers and
  unanswered SECURITY.md inboxes, which read worse than absence.
- Contribution governance (PR caps, proof-required policies) waits
  until external contributors actually arrive.
- This skill does not manufacture demand for work that solves no
  problem — if the audit says the product is the gap, report that.

## References

| File | Load when |
|---|---|
| references/readme-anatomy.md | Rewriting or auditing a README — the 16 slots in reader-decision order, plus the cringe list |
| references/honest-numbers.md | Any outbound sentence contains a number or a superlative |
| references/agent-surface.md | Adding llms.txt, tuning topics/description, or shipping a plugin marketplace |
| references/automation-tripwires.md | Building or auditing scheduled automation, especially agent pipelines |
| references/health-stack.md | Backfilling health files — the four tiers and when each is earned |

## Lineage

README anatomy, honest numbers, and agent surface generalized from
a study of [headroom](https://github.com/headroomlabs-ai/headroom)
(Apache-2.0); tripwires from a first-party incident. The belief —
surfaces make people impute the work's quality — is the third
principle of the Apple Marketing Philosophy (Markkula, 1977).
