# Goal Quality Signals

Reference for sharpen mode. Check a goal against the five contract
gates and the engine test.


## The engine test (outcome statement only)

Every word in the outcome must do work. Test by removal: take out a
word -- does the meaning change? If not, the word is idling.

Common idling words in engineering goals: robust, scalable, clean,
proper, comprehensive, elegant, production-ready, best-practice,
high-quality, efficient, optimized.

These words feel like they add requirements but they don't constrain
anything. "Build a robust API" and "build an API" ask for the same
thing -- neither tells the agent what "robust" means in this context.

Replace idling words with specific constraints:
- "robust" -> "handles 500 concurrent connections without error"
- "scalable" -> "response time stays under 200ms at 10x current load"
- "clean" -> "passes eslint with zero warnings, no file over 200 lines"
- "production-ready" -> "has error handling, logging, health check, and deploy script"

The engine test applies only to the outcome statement. Scope,
context, and contract sections use different language and different
failure modes.


## Contract gate signals

### Gate 1: Outcome -- strong signals

**Observable.** You can point to a diff, a test, a screenshot,
a metric. "Users can reset passwords via email" not "improve auth."

**Quantified when possible.** Names the metric, threshold, and
measurement method. Not all outcomes need numbers, but outcomes
that can be quantified should be.

**Single mission.** One goal, one outcome. If the goal has "and also"
more than once, it's probably two goals.

### Gate 1: Outcome -- weak signals

**Vague.** "Improve", "optimize", "clean up", "make better"
without measurable criteria. Improve what dimension? By how much?
Measured how?

**Aspirational.** Describes a feeling ("better user experience")
instead of an observable state ("checkout completes in under 3 clicks").

**Kitchen sink.** Ten goals in one goal. "Add auth AND refactor
the database layer AND update the docs AND add rate limiting AND..."
Break them up.


### Gate 2: Evidence -- strong signals

**Actionable verification.** Specific test commands, lint targets,
manual steps. Not "test it" but "run `pytest test/auth -v` and verify
the 401 response body matches the OpenAPI spec."

**Multi-layer.** Has both automated checks (tests, lint, typecheck)
and a concrete manual verification step for behavior that tests miss.

### Gate 2: Evidence -- weak signals

**Hand-wave.** "Test it" or "make sure it works." Which
tests? What input? What output? What does failure look like?

**Missing.** No verification at all. "Just make it work." How will
you know?


### Gate 3: Boundary -- strong signals

**Bounded scope.** Explicit non-goals prevent drift. The agent knows
what it must NOT touch. Frozen interfaces are named.

**Named constraints.** Specific files, modules, APIs, schemas listed
as frozen. Not "don't break anything" but "the /v1/users endpoint
response shape must not change."

### Gate 3: Boundary -- weak signals

**Missing boundary.** No non-goals or frozen interfaces. The agent
will expand scope into adjacent code because nothing tells it not to.

**Implicit boundary.** Relies on the agent's judgment about what's
"related." Agents don't have good judgment about scope boundaries --
they need explicit ones.


### Gate 4: Stop rules -- strong signals

**Stop rules exist.** The agent knows when to halt instead of guessing.
"Stop if the fix requires a schema migration" prevents expensive
silent decisions.

**Risk-calibrated.** Stop rules target the highest-risk ambiguity,
not every possible question. One good stop rule beats five generic ones.

### Gate 4: Stop rules -- weak signals

**No stop condition.** The agent can run forever on ambiguous work,
making risky decisions silently.

**Generic stops.** "Stop if anything is unclear" is too broad -- the
agent will stop on every minor decision. Target the specific
ambiguities that would change the outcome.


### Gate 5: Pause conditions -- strong signals

**Blocker-aware.** Names external dependencies that could block
progress: credentials, human approvals, CI pipeline, third-party
services, budget limits.

**Distinct from stops.** Stop rules handle "I don't know which path."
Pause conditions handle "I can't proceed regardless of path."

### Gate 5: Pause conditions -- weak signals

**Missing entirely.** Most goals have no pause conditions. The agent
grinds on blocked work, burns tokens, and produces nothing.

**Confused with stops.** "Stop if credentials are missing" is a pause
condition, not a stop rule. The distinction matters because the
resolution is different: stops need human judgment, pauses need
human action.


## Anti-patterns

**The Wish.** "Make the app faster." Faster than what? Measured how?
Which user path? What's the target? This isn't a goal; it's a
direction without a destination.

**The Kitchen Sink.** Ten goals in one goal. Each goal interferes
with the others. Break them up. Ship one at a time.

**The Micromanage.** Every implementation step dictated. Trust the
agent to implement. Constrain the outcome, not the path.

**The YOLO.** No verification at all. "Done" is a guess and bugs
ship silently.

**The Novel.** A 2000-word prompt when 200 would do. Agents get
slower and less focused on bloated prompts. Cut to the essential
problem, scope, and contract.

**The Mirror.** Copying the user's vague request back as a goal.
The skill's job is to compress ambiguity, not echo it.

**The Template Zombie.** Filling every template section with
placeholder text. "CONTEXT: relevant code. VERIFY: appropriate
tests." The sections exist to force thinking. Placeholders defeat
the purpose.

**The Grinder.** No iteration policy. Agent retries the same failing
approach 20 times. Define max rounds and what to inspect between
attempts.

**The Wishful Pause.** No pause conditions. Agent spends 30 minutes
trying to authenticate with missing credentials instead of
surfacing the blocker in 30 seconds.


## Quick checklist

Before shipping a goal, verify:

- [ ] Could two engineers independently agree on whether this is done?
- [ ] Does every word in the outcome statement do work? (engine test)
- [ ] Is there at least one specific verification command or step?
- [ ] Does the scope name at least one non-goal?
- [ ] Is there a stop rule for the highest-risk ambiguity?
- [ ] Is there a pause condition for the most likely external blocker?
- [ ] Does the iteration policy cap retries and define what to check between attempts?
- [ ] Is the goal brief under 500 words? (shorter is usually better)
- [ ] Does the /goal condition string fit in one sentence?
- [ ] For Complex tasks: has a pre-mortem been done?
