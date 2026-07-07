---
name: parallax
description: >-
  Multi-perspective decision protocol: frame the decision, spread
  genuinely different approaches, surface traps, commit with
  trade-offs. Fires on decisions where the obvious answer being
  wrong is expensive: architecture and design choices, naming,
  strategy, debugging with unknown root cause after the first
  hypothesis failed, and whenever the user is stuck or asks what
  the options are. Factual lookups, syntax, and questions with one
  canonical answer don't need spread -- answer those directly.
---

# Parallax

LLMs converge early. Each token conditions the next, so the model
anchors on its first viable answer and polishes it. For questions with
one right answer, that's fine. For decisions with multiple viable
paths, it produces competent, forgettable output.

This skill forces genuine spread before commitment: frame the decision,
generate approaches that differ on fundamental assumptions, surface the
traps, then commit to one with explicit trade-offs.

## When to invoke

**Use when:**

- Architecture or design decision that's expensive to reverse
- Naming -- products, APIs, features, modules
- Strategy -- what to build, how to approach
- Debugging with unknown root cause after first hypothesis failed
- User says "I'm stuck," "the obvious answer feels wrong," or
  "what approaches could we take"
- Explicit `/parallax <problem>`

**Skip when:**

- Factual lookup, syntax, "how do I X"
- Bug with known root cause
- Question with one canonical answer
- User says "quick," "just," "standard," "one-line"
- Inner-loop work, per-keystroke edits

When in doubt, answer directly and offer: *"Want me to run /parallax
on this for a wider look?"*

## The protocol

Three phases. Do them in order. Do not blend them.

### Phase 1 -- Frame

Before generating any options, answer three questions:

1. **What are we deciding?** One sentence. Not what we're building --
   what choice we're making.
2. **What's fixed?** Constraints that can't or won't change. Language,
   platform, team size, deadline, existing code.
3. **What does good look like?** Pick 2-4 dimensions that matter for
   this specific decision: simplicity, performance, correctness,
   maintainability, reversibility, user experience, security, cost,
   time-to-ship. Don't list all of them. Pick the ones that would
   actually break a tie.

Picking dimensions now -- before seeing any options -- prevents
post-hoc rationalization. You evaluate on what matters, not on what
your favorite option happens to be good at.

State the frame in 3-5 lines. If you can't frame the decision crisply,
the problem isn't ready for alternatives -- help the user clarify first.

### Phase 2 -- Spread

Generate 3-5 approaches. Rules:

- Each approach must differ on a **fundamental assumption or
  trade-off**, not on implementation detail. "Use Redis" vs "Use
  Memcached" is not spread. "Cache at the edge" vs "Don't cache at
  all -- make the origin fast" is spread.
- For each approach, write three lines:
  - **What:** One sentence describing the approach.
  - **Upside:** Why someone would choose this.
  - **Cost:** What you give up.
- Do not evaluate during this phase. No "this is best," no "this won't
  work." Generation and evaluation use opposite postures. Mixing them
  is what kills idea quality -- the critic strangles the generator.
  Divergence rewards "yes, and." Convergence rewards "no, because."
  Doing both at once gives you neither.
- Your first instinct produces the three answers a senior engineer
  would give in thirty seconds. Correct. Forgettable. The approaches
  worth finding live past them. If your first three approaches feel
  safe and similar, you haven't spread yet.
- When generating 4+ approaches and your options start feeling
  similar, pause and name the assumption they all share. Then break
  it. This is the single-context countermeasure for anchoring -- you
  have to fight your own convergence deliberately because you can see
  your earlier output.
- If you're still stuck, pick a lens from the table below to force a
  different angle.

Scale to the problem. A naming question gets 3 options. An architecture
decision with long-term consequences gets 5. Nobody needs 30 candidates
for anything.

### Phase 3 -- Commit

1. **Compare.** Evaluate the approaches on the dimensions from Phase 1.
   One sentence per approach per dimension. Use a table when there are
   4+ approaches.

2. **Traps.** Check every approach -- not just the suspicious ones.
   For each, state the load-bearing assumption and ask: under what
   real-world condition does this break? Trap detection is consistently
   the most valuable output of divergent thinking. Don't skip it and
   don't compress it into a parenthetical.

   How to find traps:
   - Name the assumption that makes the approach work, then imagine
     the realistic scenario where it fails.
   - Check for hidden costs that appear only at scale, under real
     concurrency, or after six months of maintenance.
   - Ask whether the approach solves the stated problem but creates
     a worse adjacent one.
   - Look for dependencies on team skills, infrastructure, or
     organizational willingness that isn't actually there.
   - Check whether the approach is attractive because it's novel
     rather than because it fits.

   Common trap shapes:
   - Looks simple but has hidden O(n^2) or hidden coupling
   - Works in dev but breaks under real concurrency / load / failure
   - Solves the stated problem but creates a worse adjacent one
   - Requires a dependency or capability that isn't there

3. **Pick.** State your recommendation and the runner-up. Say what the
   recommendation gives up -- the honest cost of the choice. If two
   options are genuinely close, say so and name the information that
   would break the tie.

Do not refuse to commit. Generating options without a recommendation
is a cop-out. The user can override. But "here are 5 things, you
decide" wastes the exercise.

## Lenses

When you're stuck generating genuinely different approaches, pick one
lens to force a different angle. Don't grind through all of them.

| Lens | Forces you to ask |
|---|---|
| Simplest | What's the dumbest thing that works? One file, no dependencies, ship today. |
| Delete | What if we just didn't do this at all? What breaks, and does anyone notice? |
| Dissolve | What if the thing everyone treats as fixed -- the framework, the DB, the network -- is removed? What's possible now? |
| Adversary | You're trying to break this. What exploit, failure cascade, or pathological input makes the obvious solution fall apart? Now design against that. |
| Beginner | You've never seen software. Why do we even do it this way? Strip jargon, ignore convention, rethink from scratch. |
| Logistics | What would a supply chain engineer do? Where are the queues, the batches, the handoffs, the bottlenecks? What gets delivered last-mile? |
| Operability | This thing will break at 3am. Design the version that lets the on-call engineer fix it from a phone without fully waking up. |
| Extreme budget | $0 and 1 hour: what's the crudest version that does the load-bearing thing? Now flip: infinite budget and a decade -- what's the maximalist version? The real answer is usually between them. |

## Anti-patterns

- **Spread without difference.** Five approaches that share the same
  underlying assumption is not spread. If every option uses the same
  database, you haven't spread -- you've decorated.
- **Spread without commitment.** "Here are your options" is research
  assistant behavior. Commit to one. Say why.
- **False precision.** Scoring options 7.3 vs 7.1 on made-up scales
  creates the feeling of rigor without the substance. Compare on
  trade-offs the user can reason about.
- **Overkill.** Running /parallax on "should I use let or const" is a
  waste. The skill is for decisions where the cost of the obvious
  answer being wrong is high.
- **Frame drift.** Starting Phase 2 before Phase 1 is clear. If the
  frame is wrong, the best alternatives solve the wrong problem.
- **Accepting the frame.** The user asks "PostgreSQL or MySQL?" and
  you dutifully compare two databases. The real question was whether
  to use a relational database at all. Phase 1 exists to catch this.
  If the user's framing is too narrow, widen it before spreading.
- **Wild for wild's sake.** A creative option earns its place by
  seeding a viable idea, not by being weird. If none of the wild
  options are buildable, the spread went too far.

## Calibration

Scale effort to stakes. Don't run the full protocol on trivial choices.

| Problem shape | Approaches | Frame | Commit |
|---|---|---|---|
| Naming (function, variable) | 3 | 2 lines | 3 lines |
| Naming (product, API surface) | 3-4 | 3 lines | 5-8 lines |
| Architecture / design decision | 4-5 | 5 lines | full comparison table + traps |
| Strategy / what to build | 4-5 | 5 lines | full comparison + explicit unknowns |
| Debugging (unknown root cause) | 3-4 | 3 lines | ranked hypotheses + first test for each |

When the problem has a known standard engineering solution and the user
needs something shippable today, the full protocol can hurt more than
it helps -- breadth costs time and the obvious answer is right. Answer
directly and offer `/parallax` as an option rather than running the
full protocol unprompted.

## Relationship to ADHD

parallax operates in a single context. Approaches will share more
underlying structure than ADHD's isolated branches -- the model sees
its own earlier output, which creates anchoring. The Spread phase
includes deliberate countermeasures (push past the obvious three, name
shared assumptions before breaking them), but these are instructions
fighting architecture. The trade-off: parallax gains a framing phase
that ADHD lacks, forces a committed recommendation instead of a scored
buffet, and costs zero extra API calls.

For maximum divergence breadth at 5-10x cost, use
[ADHD](https://github.com/UditAkhourii/adhd) directly -- it spawns
separate API calls under different cognitive frames with zero shared
context, eliminating cross-branch anchoring by construction.

Several lenses in the table above draw from ADHD's frame library.
The concepts (adversarial thinking, beginner's mind, constraint
removal) predate both skills, but ADHD's specific framings were a
direct influence.

## Output shape

```
## Frame
[Decision, constraints, dimensions -- 3-5 lines]

## Spread
### 1. [Approach name]
- **What:** ...
- **Upside:** ...
- **Cost:** ...

### 2. [Approach name]
...

## Commit
[Comparison. Traps. Recommendation with trade-offs.]
```

Keep output proportional to input. A one-sentence question doesn't
need a 2000-word analysis.
