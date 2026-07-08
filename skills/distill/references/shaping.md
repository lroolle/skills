# Shaping -- from earned unit to skill

Loaded during the Shape phase. Each earned unit becomes one skill
directory. The construction runs in the order below because each
section feeds the next.

## 1. Restate the move

Write the method's skeleton in your own words, 5-15 lines, as
instructions to an agent -- imperative, present tense. The check:
someone who never read the source can run the move from this text
alone. If a line reads like "the author argues that..." you are
summarizing, not shaping -- rewrite it as what to *do*.

This restatement becomes the skill's process section. Give each
step a completion criterion (the collection's doctrine applies to
distilled skills with no discount).

## 2. Anchor with the author's own case

Pick the strongest episode where the author personally ran the
move: what situation, what they did, what happened. One case,
tightly told, in your own words. It becomes the worked example
inside the skill -- the analogy material an agent reaches for
when applying the move to a new situation.

At most one direct quote here, under 25 words, with location
(chapter / timestamp / section). If the best sentence is longer,
paraphrase it and keep the location.

## 3. Build the trigger from language signals

List 3-5 working situations where someone needs this move, then
write what they would actually *say* in each -- the language
signals. The description assembles from these, one trigger per
branch, leading word first.

Good (inversion-check):

> Fires when the user is weighing a decision and enumerating
> upsides without traction ("why isn't this working", "help me
> decide, everything looks good"), or asks how to make a plan
> succeed and the failure modes haven't been named.

Bad:

> Use when the user needs to think about decisions.

The bad one summarizes a mental state; the good one matches words
a person types. If you cannot write realistic language signals,
the situation never actually occurs -- return the unit to the
digest.

Write the sibling routing last, once all skills from the source
are shaped: name the adjacent skill and the tell that separates
them ("naming failure modes before building is inversion-check;
weighing alternatives is second-order-effects' job").

## 4. Fence the boundary

Three sources, in order of value:

1. **The author's own warnings** -- where they said the method
   breaks (from the Failure lens)
2. **The blind-spot list** -- what the survey's critical pass
   found the author ignoring or overclaiming
3. **The sibling map** -- adjacent moves this one gets confused
   with

State boundaries as routing where possible ("for X, use Y
instead") and keep hard prohibitions paired with the positive
alternative. A distilled skill without a boundary section gets
invoked everywhere the source's vocabulary appears, then
disappoints -- boundary is what makes the author's method safe
in hands that never read the book.

## 5. Frontmatter and lineage

```yaml
---
name: <move-slug>            # the move, not the source
description: >-
  <assembled from language signals, one trigger per branch,
  sibling routing included>
---
```

Credit the source in a compact **Lineage footer** -- the last
section of SKILL.md, 1-3 lines: title, author, location of the
two strongest appearances, license if the source is a repo.
Skills travel as single folders, so the footer travels with them.
Nowhere else: no "the author says" inside steps, no dates or
popularity counts anywhere -- credit is for the reader; the agent
needs the move. (The one exception is a direct quote, which keeps
its location beside it.)

## 6. Self-check before Prove

- [ ] Process runs without the source at hand (restate test)
- [ ] Every step's done-condition is checkable
- [ ] One quote max, <25 words, located; the rest is your voice
- [ ] Description built from language signals, not chapter summary
- [ ] Sibling routing names the tell, not just the neighbor
- [ ] Boundary carries at least one author warning or blind spot
- [ ] Credit sits only in the Lineage footer, never inside steps
- [ ] The skill changes what an agent does, not how it sounds
