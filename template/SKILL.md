---
name: skill-name
description: >-
  What this skill does, leading word first. Then one trigger per
  branch -- each genuinely distinct situation that should fire it,
  listed once, no synonym piles. If a trigger collides with a
  sibling skill, route it: "X is other-skill's job."
---

# Skill Name

What this skill does and why it exists, in one paragraph. If there
is a one-line test for whether the output is good, state it here.

## Gate

Open by sizing the task. When should the agent say "no" or "not
this heavy"? A table mapping task weight to protocol depth beats
running the full ceremony on a typo fix.

## Process

1. Phase one. End on a completion criterion the agent can check:
   done vs not-done must be decidable, exhaustive where it matters
   ("every X accounted for", not "handle X").
2. Phase two. Explain *why* behind any rule the model might
   rationalize away -- reasons adapt, bare MUSTs rot.
3. Check. A rubric of concrete, smashable defects. A check the
   agent can't fail is decoration.

## Anti-patterns

Named failure modes for diagnosis (reference, not steering).
In the process itself, steer positive: state the target behavior
instead of prohibiting the failure.

## References

| Reference | When to load |
|---|---|
| references/example.md | Only some runs need it -- say which |

Inline what every run needs; disclose what only some branches
reach. The pointer's wording decides whether it gets loaded.
