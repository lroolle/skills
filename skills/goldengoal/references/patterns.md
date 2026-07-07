# Goal Patterns by Task Type

Common task shapes with their typical scope, essential contract
sections, quantification heuristics, and traps.


## Feature (new user-facing capability)

**Essential sections:** All seven (including pre-mortem). Features
are where under-specification hurts worst -- the agent builds
confidently in the wrong direction.

**Typical scope:**
- In: the new behavior, UI, API surface, tests
- Out: existing features that must keep working
- Frozen: public APIs, database schema (unless the feature requires changes)

**Quantify with:** Pass/fail acceptance criteria. New tests for
the feature + existing test suite still passes. Manual verification
of the happy path and at least one error path. If UI: screenshot
or browser check.

**Iteration policy:** Implement core path first, then edge cases.
Rerun full test suite after each significant change. Max 3 rounds
of refinement before reporting.

**Common traps:**
- Agent adds the feature but breaks adjacent behavior (missing non-goals)
- Feature works in isolation but doesn't integrate with existing flows
- Over-building: agent adds configuration, admin UI, extensibility
  that wasn't asked for (missing "Out" scope)


## Bug fix (known root cause)

**Essential sections:** Outcome, contract. Context optional if the
cause is clear. Often gates at Simple.

**Typical scope:**
- In: the broken behavior and its direct fix
- Out: refactoring, cleanup, or "while we're here" improvements
- Frozen: the fix should be surgical, not structural

**Quantify with:** Reproduction test that fails before fix and
passes after. Name the exact test command and expected output.

**Iteration policy:** Reproduce first, fix second. One focused
attempt. If fix doesn't work on first try, inspect logs before
retrying.

**Common traps:**
- Agent "fixes" the symptom but not the root cause
- Fix introduces a regression in a related path
- Agent refactors surrounding code "while fixing" (scope creep)


## Bug fix (unknown root cause)

**Essential sections:** Problem (symptom description), outcome
(expected vs. actual behavior), context (reproduction steps,
relevant logs, recent changes), contract with stop rules.

**Typical scope:**
- In: investigation + fix. Phase 1 is diagnosis; phase 2 is fix.
- Out: speculative fixes before diagnosis completes
- Stop rule: "Stop and report findings before applying a fix"

**Quantify with:** Reproduction test that fails before fix and
passes after. If the bug is intermittent, describe the conditions
that trigger it and verify those conditions. Number of reproduced
failures before and after.

**Iteration policy:** Investigate up to N files/paths. Stop and
report hypothesis with evidence before attempting fix. Max 2
fix attempts before escalating.

**Common traps:**
- Agent applies the first plausible fix without confirming root cause
- Intermittent bugs "fixed" by coincidence (verification doesn't
  actually test the failure condition)
- Agent investigates endlessly without converging (missing stop rules)


## Refactor (improve internals, preserve behavior)

**Essential sections:** Outcome (what's cleaner and why it matters),
scope (what moves, what stays), contract (behavior unchanged).

**Typical scope:**
- In: the code being restructured
- Out: behavior changes, new features, API changes
- Frozen: all external interfaces and observable behavior

**Quantify with:** Existing test suite passes unchanged. If tests
don't exist, write characterization tests first. Diff shows only
structural changes, not behavior changes.

**Iteration policy:** One structural change at a time. Run full
test suite after each change. If any test fails, revert and
investigate before continuing.

**Common traps:**
- Agent "improves" behavior while refactoring (scope creep)
- Refactoring without adequate test coverage -- behavior silently
  changes and no test catches it
- Renaming a public API without realizing it's a breaking change


## Migration (data, dependency, or version upgrade)

**Essential sections:** All seven (including pre-mortem), with
extra emphasis on context (current state, target state,
compatibility requirements) and contract (rollback plan).

**Typical scope:**
- In: the migration target and its direct dependents
- Out: unrelated modernization, new features
- Frozen: data integrity, user-facing behavior

**Quantify with:** Migration runs successfully on test data.
Before and after states match expectations. Rollback procedure
works. Performance targets: specific time and data volume.

**Pause conditions:** Pause if migration affects production data,
requires downtime, or needs DBA approval.

**Iteration policy:** Dry run on test data first. Compare
before/after states. Only proceed to real data after dry run
passes. Max 2 retry rounds on failures.

**Common traps:**
- Data loss or corruption during migration (test on realistic data)
- Migration works on small data but times out on production volume
- Dependency upgrade cascades into 50 file changes (scope wasn't bounded)
- No rollback plan


## Cleanup (remove dead code, consolidate, simplify)

**Essential sections:** Outcome (what's removed/consolidated),
scope (strict boundary on what's touched), contract.

**Typical scope:**
- In: specific dead code, duplication, or complexity being removed
- Out: everything else. Cleanup is the highest scope-creep risk.
- Frozen: all behavior

**Quantify with:** Test suite passes. Dead code detector confirms
removal. No new warnings or errors.

**Iteration policy:** Remove one thing at a time. Run tests after
each removal. Stop if removal count exceeds the stated scope.

**Common traps:**
- "Dead" code that's actually used via reflection, dynamic import,
  or external consumer
- Cleanup cascades: removing one thing exposes three more
- Agent removes code that looks dead but is load-bearing for an
  edge case not covered by tests


## Infrastructure (CI, deployment, tooling, config)

**Essential sections:** Problem, outcome, context (current infra
state), contract with explicit verification.

**Typical scope:**
- In: the specific pipeline, config, or tool being changed
- Out: application code (unless the infra change requires it)
- Frozen: deployment targets, existing workflows

**Quantify with:** Pipeline runs successfully. Build/test/deploy
times meet targets. Rollback is tested.

**Pause conditions:** Pause if changes affect shared CI config,
production deployment pipelines, or team-wide tooling.

**Common traps:**
- Works in CI but not locally (or vice versa)
- Config change that breaks a different environment
- "Improving" a pipeline by adding complexity


## Investigation (diagnosis, performance analysis, understanding)

**Essential sections:** Problem (symptom or question), outcome
(what you need to know, not what you need to build), contract
with explicit stop conditions.

**Typical scope:**
- In: the question being answered, the area being investigated
- Out: fixes, changes, or optimizations (investigation first)
- Stop rule: "Stop and report findings when you have a hypothesis
  with evidence, or after examining N files/paths"

**Quantify with:** Concrete finding: a root cause, a performance
profile, a dependency map, a recommendation with evidence. Define
the decision the research must enable and the evidence standard.
Not "I looked at some things."

**Iteration policy:** Examine up to N files/paths. If no hypothesis
after N, stop and report what was examined and what was ruled out.
Max 2 investigation rounds before escalating.

**Common traps:**
- Agent starts fixing before understanding (premature optimization)
- Investigation scope expands indefinitely
- Findings stated without evidence
- No stop condition: agent reads the entire codebase


## Documentation

**Essential sections:** Outcome (what's documented and for whom),
scope (which docs, not which code), context (audience).

**Typical scope:**
- In: the specific documentation being written or updated
- Out: code changes (unless docs reveal a bug)
- Frozen: existing accurate documentation

**Quantify with:** Docs build without errors. Links work. Code
examples compile/run. A reader unfamiliar with the code can follow
the doc to accomplish its stated purpose.

**Iteration policy:** Draft, then review against audience needs.
One revision round after initial draft.

**Common traps:**
- Agent writes docs that describe the code rather than the user's
  task (reference vs. tutorial confusion)
- Docs that are accurate today but will rot because they duplicate
  information that lives in code


## Discovery (unfamiliar domain)

**Essential sections:** Problem (what you need to understand),
outcome (the decision this investigation enables), contract with
narrow scope and hard stop.

This pattern applies when you don't know enough to write a build
goal. The goal IS to learn enough to write the real goal.

**Typical scope:**
- In: reading docs, inspecting code, understanding patterns
- Out: making changes, building anything, installing anything
- Stop rule: "Report findings and propose a build goal after
  examining N key files/docs"

**Quantify with:** A proposed build goal that passes the five
contract gates. The discovery is done when the next goal is defined.

**Iteration policy:** Read before writing. Propose the build goal
after one pass. Let the user validate before proceeding.

**Common traps:**
- Agent starts building before understanding (premature implementation)
- Discovery expands into building ("while I was looking, I fixed...")
- Findings too vague to inform the next goal
