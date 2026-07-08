# lroolle/skills -- craft doctrine

Skills live in flat directories under `skills/`. Each skill is a
self-contained folder: SKILL.md plus optional scripts/, references/,
assets/. Follows the agent skills spec (agentskills.io).

Every skill in `skills/` must have an entry in
`.claude-plugin/plugin.json` and a listing in the top-level
`README.md`. When you add, rename, or remove a skill, sync both.

## The root virtue

A skill exists to make a stochastic system take the same *process*
every run -- predictability of behavior, not sameness of output
(parallax should predictably diverge; its tokens vary, its protocol
doesn't). Every rule below serves this.

## Our shape

The house style is the **protocol skill**: a gate, then ordered
phases, then a check.

- **Gate first.** The most valuable output of a skill is often "no"
  or "not this heavy." Every protocol opens by sizing the task
  (htmlize: does this beat markdown? goldengoal: trivial/simple/
  standard/complex) so ceremony scales with stakes.
- **Phases end on completion criteria.** Each phase states the
  condition that tells the agent it's done -- checkable (done vs
  not-done is decidable) and, where it matters, exhaustive ("every
  interactive element keyboard-reachable", not "make it accessible").
  Vague criteria invite the agent to declare victory early.
- **Check is a rubric, not a vibe.** The closing phase lists concrete
  smashable defects (kiln smashes underfired pieces; htmlize has a
  review table). A check the agent can't fail is decoration.

## Descriptions

The description is the trigger mechanism and it costs context on
every turn of every session, whether the skill fires or not. Earn it:

- **One trigger per branch.** List each genuinely distinct situation
  that should fire the skill once. Synonym piles ("goal, goal prompt,
  my goal is, write me a goal...") restate one branch five times --
  collapse them and spend the tokens on a branch you missed.
- **Front-load the leading word.** The first noun should be the
  concept users naturally reach for when they want this skill.
- **Negative boundaries route, not forbid.** When a trigger collides
  with a sibling skill, say where the other case goes ("creating
  skills from scratch is skill-creator's job") -- routing beats
  bare prohibition.

## Body style

- **Explain why, not just what.** The model adapts to edge cases
  when it knows the reason; a bare MUST rots into cargo cult. All-caps
  imperatives are a yellow flag.
- **Steer positive.** "Don't write vague outcomes" names vagueness
  and makes it available; "write outcomes two engineers would verify
  identically" installs the target. Keep prohibitions only as hard
  guardrails, paired with what to do instead. (Named anti-pattern
  *catalogs* for diagnosis -- Template Zombie, card-in-card -- are
  reference, not steering; they stay.)
- **Leading words over paragraphs.** A pretrained concept the agent
  already holds (contract, gate, smash, spread, seam) anchors more
  behavior per token than a sentence of adjectives. When three
  adjectives restate one quality, hunt for the single word.
- **No-op test.** For each line ask: does this change behavior versus
  what the model does by default? "Be thorough" fails; delete the
  sentence, don't trim it.

## Information hierarchy

SKILL.md body under 500 lines, and shorter is better when nothing is
lost. The ladder: steps the agent always needs stay inline; reference
some runs need goes to references/ behind a pointer whose *wording*
says when to load it ("Load signals.md in sharpen mode"); templates
and palettes go to assets/. Keep a concept's definition, rules, and
caveats under one heading -- scattered halves of one idea cost more
than their length.

Each meaning gets one home. When two skills need the same fact, one
owns it and the other points. When a new skill supersedes an old one
(goldengoal over charter), the old one is deleted, not left beside it
-- two skills sharing triggers fight over invocation and the loser
is predictability.

## Pruning discipline

Skills sediment: adding feels safe, removing feels risky, and stale
layers pile up. On every edit pass, re-run the no-op test and the
relevance test (does this line still bear on what the skill does?)
over the sections you touch. Delete failing sentences whole.

## Invocation

Default is model-invoked: description present, agent fires it, other
skills can reach it. A skill that only ever fires by hand (repo
utilities, personal rituals) can set `disable-model-invocation: true`
-- its description drops from the agent's context entirely and the
human's memory becomes the only index. Pay context load only for
skills the agent must discover on its own.

## Sources and IP

Ideas absorbed from other skill collections are rewritten in our own
voice -- never pasted. MIT/Apache sources are citable with
attribution; unlicensed sources contribute ideas only. Third-party
skills installed for study live in `.agents/` (gitignored) and are
never committed.

**Routes vs credit.** An external repo may appear in operational
text only as a route ("for maximum divergence at 5-10x cost, use
ADHD directly") -- routing changes agent behavior. Credit does not:
no source names, "adapted from", dates, or star counts inside steps,
rules, or reference material the agent works from. Credit lives in
exactly two human-facing places: the repo README (the story) and one
compact Lineage footer at the bottom of SKILL.md (skills travel as
single folders; the footer travels with them). A long lineage story
can be a disclosed reference (htmlize's prior-art.md) behind a
pointer no operational path loads. Direct quotes are the exception
-- a quote keeps its source beside it or becomes a paraphrase.

Craft vocabulary (predictability, leading words, no-op, sediment,
one-trigger-per-branch) draws on Matt Pocock's
[writing-great-skills](https://github.com/mattpocock/skills) (MIT),
merged with our gate-first protocol style.
