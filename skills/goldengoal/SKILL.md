---
name: goldengoal
description: >-
  Goal engineering for agentic loops -- a goal is a contract, not a
  wish. Composes fuzzy intent into a goal brief plus a /goal
  condition, or sharpens an existing draft against five contract
  gates (outcome, evidence, boundary, stop rules, pause conditions).
  Calibrates to task weight: trivial skips, simple gets three lines,
  complex gets pre-mortem. Fires on three branches: defining a task
  or setting up /goal or /loop ("I want to build", "help me start",
  "define the task"); checking whether a goal, spec, or requirement
  is clear enough ("sharpen this", "is this goal clear"); and
  recovering after a loop drifted or built the wrong thing.
  Mid-execution corrections with clear direction don't need a
  contract -- just make the correction.
---

# Golden Goal

A goal is a contract, not a wish.

The gap between "I want X" and a goal an agent can execute against
is not prompt craft -- it's thinking discipline. Golden Goal helps
you think through what you want, then compresses the result into a
contract an agent can be judged against.

The test: can someone (or something) evaluate the goal's outcome
without asking you what you meant?

## Mode selection

If the user provides text that looks like a goal (has an outcome,
a condition, a structured prompt), start in **Sharpen** mode.
If they describe intent without structure ("I want to add SSO"),
start in **Compose** mode.

When composing, infer answers from the codebase and conversation
context. Only ask questions when the answer materially affects the
goal and can't be determined from available information. A user who
says "add rate limiting to the API" doesn't need to be asked "what
API?" if there's one API in the repo.

## Gate -- calibrate to task weight

Before running the protocol, gauge complexity:

| Level | Signal | What to do |
|---|---|---|
| Trivial | Known fix, one file, <5 min | Skip. Just do it. |
| Simple | Known outcome, small scope, low risk | Quick mode (3 lines) |
| Standard | Feature, bug with unknown cause, multi-file | Full compose or sharpen |
| Complex | Architecture, risky, multi-system, hard to reverse | Full + pre-mortem + risk |

When in doubt, start at Standard. The gate saves effort on trivial
tasks and prevents under-specification on complex ones.

## The five contract gates

Every goal, regardless of mode, must pass these five gates before
shipping. This is the spine -- compose and sharpen are paths to
getting here, but the gates are non-negotiable.

| Gate | Question | Failure mode if missing |
|---|---|---|
| **Outcome** | What's true after that isn't true now? | Agent builds confidently in the wrong direction |
| **Evidence** | How does anyone verify this is done? | "Done" is a guess; bugs ship silently |
| **Boundary** | What must NOT change? | Agent expands scope into adjacent code |
| **Stop rules** | When should the agent halt and ask? | Agent drifts on ambiguity or makes risky decisions silently |
| **Pause conditions** | When is the agent blocked, not stuck? | Agent grinds on blocked work (missing credentials, human decision, external dependency) instead of surfacing the blocker |

Stop rules handle ambiguity (the agent doesn't know which path is
right); pause conditions handle blockers (the agent can't proceed
regardless of knowledge). Contract section 5 has worked examples
of each.

## Compose mode

User has intent but not a structured goal. Walk through these steps
in order. Each compresses one dimension of ambiguity.

### 1. PROBLEM

What actually hurts? Who feels it? Why now?

One to two sentences. If you can't state the problem without
jargon or hand-waving, the goal isn't ready.

Think through:
- What breaks, fails, or frustrates without this change?
- Who notices if it doesn't get done?
- Is this solving a real problem or preventing an imagined one?

If the domain is unfamiliar and the user can't answer these
questions, the first goal should be investigation: "Understand X
well enough to define the real goal." Don't force a build goal
when a discovery goal is what's needed.

### 2. OUTCOME

What exists after this is done that doesn't exist now?

Observable, not aspirational. "Users can log in with SSO" not
"improve the auth experience." "Migration runs in <30s on the
test dataset" not "optimize the migration."

Make it quantitative when the domain supports it. Prefer numbers
that represent real success, not decorative precision:

| Domain | Quantify with |
|---|---|
| Bugs | Reproduction test fails before, passes after |
| Tests | Exact command + required pass condition |
| Performance | Metric, target threshold, measurement method, run count |
| Quality | Observable acceptance bar (lint, typecheck, review criteria) |
| Research | Decision the research enables, evidence standard |
| Operations | Healthy state, monitoring window, rollback trigger |

Think through:
- What would a screenshot, test, or demo show?
- Can you describe the before and after in concrete terms?
- Would two engineers independently agree on whether this is done?

### 3. SCOPE

What's in. What's out. What's frozen.

- **In:** files, modules, behaviors being changed
- **Out:** what the agent must NOT touch or expand into
- **Frozen:** interfaces, APIs, schemas that must stay stable

Non-goals are as important as goals. "Do NOT refactor the auth
module while fixing this bug" prevents a common drift mode.

Think through:
- What adjacent code could the agent be tempted to "improve"?
- What would a PR reviewer flag as out of scope?
- What contracts (APIs, schemas, interfaces) must stay stable?

### 4. CONTEXT

What the agent needs that it can't infer from the code.

Include: relevant files/modules, patterns to follow, domain
rules, prior decisions, known constraints (perf, security,
compatibility), conventions.

Exclude: obvious things the agent reads from the repo, generic
best practices, anything already in CLAUDE.md.

Think through:
- What would a new team member need before touching this?
- What existing pattern should the agent follow?
- What domain knowledge isn't in the code?

### 5. CONTRACT

Five parts. This is the load-bearing section.

**DONE WHEN:** Verifiable completion criteria. Tests pass,
specific behavior works, file exists, metric meets target.
Must be checkable without asking the author what they meant.

Bad: "auth is improved." Good: "POST /login returns 200 with
valid credentials and 401 without, rate-limited to 10/min."

**VERIFY:** How to check. Specific test commands, lint, typecheck,
build, manual verification steps. What the agent should report
if it can't verify something.

Bad: "test it." Good: "run `pytest test/auth -v`, verify rate
limit with `curl` loop, check 401 response body matches spec."

**STOP RULES:** When to halt and ask instead of guessing.
High ambiguity, conflicting requirements, risk of data loss,
scope expansion beyond stated boundaries, uncertain architectural
decisions.

**PAUSE CONDITIONS:** When to surface a blocker instead of
grinding. Missing credentials, needed human decisions, external
service dependencies, budget or cost thresholds, repeated
failures with the same approach.

**ITERATION POLICY:** How to retry after failures. How many
focused rounds before reporting. What to inspect before retrying.

Example: "Rerun checks after each meaningful change. Inspect
logs before retrying. Make at most 3 focused improvement rounds
before reporting remaining issues."

### 6. PRE-MORTEM (Standard/Complex only)

After drafting the goal, ask one question:

> "What is the most likely way this goal fails?"

Walk the five gates' failure-mode column against this specific
goal and name the likeliest failures.

For each identified failure mode, derive one constraint -- a
non-goal, a stop rule, or a pause condition. Add it to the
contract. The pre-mortem often catches what the compose flow
missed because humans are better at imagining concrete failures
than abstract success criteria.

### 7. SHAPE

Compress everything into two outputs:

**Goal brief** -- the full spec, pasted as a session message or
saved to a file. Structured by the sections above.

**Goal condition** -- a short string for `/goal` that captures
the verifiable done state. This is what the evaluator checks.

The brief gives the agent context. The condition gives /goal
its exit criteria. They work together but are not the same thing.

Example conditions:
- "all tests in test/auth pass and lint is clean"
- "the migration completes in <30s on the test dataset"
- "the new endpoint returns 200 with valid JWT and 401 without"

## Sharpen mode

User has a draft goal -- existing prompt, issue description,
Slack message, previous /goal that drifted.

Load [signals.md](references/signals.md) -- it owns the full
signal set -- and run its two checks in order:

1. **Engine test**, on the outcome statement only: every word
   must do work. "Robust" and "scalable" idle; "10 req/min per
   IP" carries load. Flag idling words, propose measurable
   replacements.
2. **Contract gates**: check the draft against all five gates.
   For each gap, name it, state what goes wrong without it in
   one sentence, and propose a specific fix.

Sharpening is done when no idling word survives in the outcome
and every gate has a concrete answer. Then reshape into goal
brief + condition format.

## Quick mode (simple tasks)

For tasks that gate at Simple:

```
OUTCOME: [one sentence -- what exists after]
DONE WHEN: [verifiable condition]
VERIFY: [how to check -- test command, manual step]
```

Three lines. The contract gates still apply in your head but
don't need to be written down.

## After shaping

Present the goal brief and condition to the user. Then offer
concrete next steps:

- Set `/goal <condition>` to start an autonomous loop
- Save the brief to a `.md` file for multi-session work
- Enter `/plan` mode to design the implementation

If the user revises ("no, that's not the outcome I want"),
re-enter compose at the step that needs revision -- not from
scratch.

## Composition

Golden Goal defines WHAT to build and WHEN it's done. It sits
before execution in the skill pipeline:

| Step | Skill | Does what |
|---|---|---|
| 1 | /parallax | Decide which approach (when the path is unclear) |
| 2 | /goldengoal | Define what to build and when it's done |
| 3 | /plan | Plan how to build it (Claude Code plan mode) |
| 4 | Execute | Invoke domain skills (kiln, htmlize, etc.) |
| 5 | /goal | Set the loop with the condition from step 2 |
| 6 | /skillize | Capture the workflow if it was reusable |

Not every task needs every step. Golden Goal works standalone
or as part of this pipeline. For simple tasks, skip to 2 + 5.

## Output shape

The output shape is a formatting guide, not the process. The
compose steps produce the thinking. The output compresses it.
Skipping to the template without working through the steps
produces Template Zombie output -- formatted but empty.

### Simple (quick mode)

```
OUTCOME: [sentence]
DONE WHEN: [condition]
VERIFY: [check]
```

### Standard / Complex

```
## Goal Brief

**Problem:** [1-2 sentences]
**Outcome:** [observable, quantified result]

**Scope:**
- In: [what changes]
- Out: [what must not change]
- Frozen: [stable interfaces]

**Context:** [relevant files, patterns, domain knowledge]

**Contract:**
- DONE WHEN: [verifiable criteria]
- VERIFY: [specific checks]
- STOP RULES: [when to halt and ask]
- PAUSE IF: [when to surface a blocker]
- ITERATION: [how to retry, max rounds]

---
/goal [short condition string]
```

## References

| Reference | When to load |
|---|---|
| [signals.md](references/signals.md) | Sharpen mode, or reviewing any goal's quality |
| [patterns.md](references/patterns.md) | Composing goals for common task types |
| [sources.md](references/sources.md) | Deep background on goal/loop engineering |
