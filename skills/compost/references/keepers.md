# The keepers

Three genres of doc carry what code cannot. Everything promoted
out of a composted doc lands in one of them; a fourth genre needs
a justification. All three share one bar:

**Non-derivable.** If an agent could rediscover the content by
reading the implementation, it does not belong in a keeper -- it
is a cache, and it will rot. (Contested? That is what the
rediscovery test is for.)

## ADRs -- decisions and rejected alternatives

The shape:

```markdown
# <decision, stated as the choice made>

Context     -- what forced a decision
Decision    -- what was chosen
Alternatives considered -- what was rejected, and why
Consequences -- what this costs and enables
```

The bar: **at least one genuinely considered rejected
alternative.** An ADR with no alternatives is a changelog entry
wearing a costume. The rejected options are the payload -- they
are what stops the next agent (or engineer) from re-litigating
the decision, and they are precisely what the code cannot say.

One ADR per non-obvious choice. Home: a global, discoverable path
-- `docs/adr/` for product decisions, `.agents/adr/` for
repo-tooling decisions -- never only a PR description or a chat
log. Prose kept short enough that reading three ADRs costs less
than re-deriving one.

When promoting from a composted doc: the doc usually states the
decision but not the alternatives. Reconstruct them from git
history and from the humans while they still remember. An ADR you
cannot give a real alternative is thin -- say so in it rather
than inventing one.

## Glossary -- domain language

The shape: term, meaning, and where useful the anti-term.

```markdown
**Invoice** -- a finalized, immutable billing document.
_Not_: "bill" (we reserve that for drafts), "receipt".
```

The bar: the term is actually used -- in code identifiers, in
issues, in conversation -- and an agent has misused it or
plausibly could. Framework and language tutorials never qualify;
they are derivable from the wider world.

Home: one global file (`docs/glossary.md`, or the project's
existing context file). File-local comments fail the job -- the
agent that needed the term already opened the wrong file.

## Roads -- navigation pointers

The shape: one line per area, each road ending in code.

```markdown
- billing -> src/billing/ · ADR-014 · tests/billing/
- auth    -> src/auth/    · ADR-003
```

The bars:

- Every link resolves.
- No behavior descriptions -- a road says where, never what or
  how. The moment a road needs a paragraph, the real problem is
  a module boundary, and the fix is Phase 4 spend, not more
  prose.
- Thin enough to load whole. A map that has to be navigated has
  failed at being a map.

Generating and refreshing the artifact itself (llms.txt, an
AGENTS.md map section) is the llms-txt skill's job -- this file
only sets the bar the artifact must meet.

## Promotion routing

Each UNREACHABLE claim from the rediscovery test, by shape:

| Claim shape | Keeper |
|---|---|
| "We chose X over Y because..." | ADR |
| "Term T means..." / "Never call X a Y" | Glossary |
| "For Z, look in..." | Road |
| Business context, product intent, org history | Usually `human-only` -- keep, but off the agent path unless agents demonstrably need it |

Anything that fits none of these: challenge whether it is real
knowledge or reheated restatement, and re-run the test on it if
contested.
