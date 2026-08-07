---
name: compost
description: >-
  Compost the docs that restate your code -- tag agent-visible
  markdown, prove restatement with a blind rediscovery test (a
  subagent that reads only the code tries to reconstruct each
  doc's claims), delete or quarantine what fails, promote what
  survives into the three keepers code cannot carry (ADRs,
  glossary, navigation roads), and reinvest the savings in code
  that explains itself. Fires on three branches: a docs-hygiene
  pass ("clean up docs/", "are these docs stale?", "docs and code
  disagree", agents citing markdown over source); right after a
  wave of generated overview or architecture files ("delete this
  doc spam"); and installing the keeper layer in a repo that has
  none. Generating the navigation artifact itself is llms-txt's
  job; a knowledge vault from non-code sources is wiki-it's;
  polishing human-facing surfaces (README, release story) is
  burnish's.
---

# Compost

Docs that explain code start rotting the moment the code moves.
Composting is what a gardener does with rot: not landfill, and
not denial -- decompose it and feed what was alive in it back to
the soil. Here the soil is the codebase. A pass is complete when
no agent-visible doc survives whose content an agent could
rediscover by reading the code, and the savings have visibly
fed the code itself.

Why stale explanatory docs are worse than none: an agent loads
doc and code together, and when they disagree it cannot tell
which is true -- the stale essay wins just often enough to hurt,
because it wears the authority of documentation. Meanwhile the
doc's maintenance bill never stops arriving. This skill is a
budget reallocation: the tokens spent keeping an essay in sync
buy renames, types, tests, and error messages instead -- forms
of explanation that cannot drift, because they are the code.

## Gate

Run a pass when any of these hold: agent output cites markdown
more often than source; docs and code tell different stories (or
you fear they do); a wave of generated "overview" or
"architecture" files just landed; context windows fill with
restated implementation.

Go light or stop when:

- **Docs are the product.** A published user-facing docs site is
  a product surface with its own craft, not restatement.
- **The docs belong to another team.** Produce the tagged
  inventory and hand it over -- deleting someone else's source
  of truth without sign-off is how this doctrine gets banned.
- **The repo has zero keepers.** Install homes first (Phase 3's
  keeper shapes), then delete. Why-knowledge orphaned mid-pass
  with nowhere to go dies in the deletion.

## Phase 1 -- Inventory and tag

List every doc an agent can reach: markdown in the repo, wiki
pages, anything greppable. Tag each:

| Tag | Meaning | Default verdict |
|---|---|---|
| `restate` | Says what or how the code already says | Compost |
| `why` | Decisions, rejected alternatives, domain rules | Promote to keeper |
| `nav` | Where to look next | Keep thin -- roads, not essays |
| `human-only` | Support, legal, product runbooks | Keep; move off the agent path if it pollutes context |
| `archive` | History worth keeping, not trusting | Quarantine branch |

Rule of thumb: if an agent could rediscover it by reading the
code, it is `restate` -- a cache of the code, and caches of code
rot. Completion: every agent-visible doc carries exactly one tag.

## Phase 2 -- The rediscovery test

Tagging by judgment pattern-matches on headings. When a tag is
contested, or a doc is load-bearing enough that deleting it
scares someone, don't argue -- run the trial. The test measures
the only thing that matters: what the doc adds for a reader who
already has the code. That reader is an agent, so use one.

1. Extract the doc's checkable claims -- concrete behavioral
   statements, not opinions.
2. Rewrite each claim as a neutral question that does not leak
   the doc's answer.
3. Dispatch a subagent with the code and the questions -- never
   the doc.
4. Grade each claim by what came back:

| Verdict | Meaning | Consequence |
|---|---|---|
| REDISCOVERED | Reconstructed from code alone | Restatement -- compostable |
| UNREACHABLE | Code genuinely cannot yield it | The doc's living core -- promote to a keeper |
| CONTRADICTED | Code says otherwise | Drift: the doc is misinforming every agent that loads it -- resolve before anything else |

CONTRADICTED is the highest-value find and the reason the test
beats deletion-by-vibes: it doesn't just sort docs, it catches
docs actively lying. Protocol details, the subagent prompt, the
navigation-miss re-run, and per-doc scoring:
references/rediscovery.md.

Completion: every contested doc has a per-claim verdict sheet,
and zero CONTRADICTED claims remain unresolved.

## Phase 3 -- Verdicts

Execute per doc, in this order:

1. **Resolve contradictions first.** Either the code drifted from
   a real decision (fix the code, record the decision as an ADR)
   or the code legitimately moved on (the doc dies). Never leave
   dual truth standing -- it is the emergency this skill exists
   for.
2. **Promote survivors.** Each UNREACHABLE claim goes to its
   keeper genre -- decision-shaped to an ADR, term-shaped to the
   glossary, location-shaped to a navigation road. Shapes and
   quality bars: references/keepers.md. Generating or refreshing
   the llms.txt-style map itself is the llms-txt skill's job.
3. **Compost the rest.** Delete, or collapse to a one-line
   pointer at the code path that now carries the meaning.
   Deleting loses nothing -- git history holds every byte; a doc
   you might want back is one `git log --follow` away.
4. **Quarantine `archive` material on a separate branch** (call
   it `attic`). Not gitignore: agents grep ignored files happily;
   only a branch is genuinely outside the working tree.

Completion: every tagged doc has been executed -- no doc remains
whose claims were all REDISCOVERED.

## Phase 4 -- Reinvest

Deletion without reinvestment is just tidying. Each composted doc
existed because something in the code was illegible enough that
someone wrote prose to compensate -- the doc was a symptom;
the disease is in the code. For each one, name the defect that
made it feel necessary and fix that:

| Spend on | Example |
|---|---|
| Names | `qualifiesForFreeShipping`, not `check` |
| Types | Illegal states unrepresentable |
| Extracted functions | Intention-revealing steps instead of a comment block |
| Errors | The 400 names the bad field and the allowed values |
| Tests | Behavior as executable spec |
| Seams | Module boundaries that match the domain |

Completion: at least one such improvement has landed per pass.
Without it you only deleted -- the compost never reached the
soil.

## Phase 5 -- Wire the agents

Point AGENTS.md / CLAUDE.md at keepers and code only, and give
future sessions the routing that prevents re-sedimentation: when
something needs explaining, first try a rename or refactor; if it
is a decision, write an ADR; if it is a term, add it to the
glossary; if it is a location, add a road. A fourth genre of doc
needs a justification. State plainly that code is the source of
truth for behavior.

Completion: the agent instructions name the keeper paths, and no
instruction asks agents to generate explanatory markdown.

## Turning the pile (recurring)

Compost is a cadence, not an event. Each release or every few
agent-heavy sessions: diff for new agent-visible markdown and tag
it; spot-check one ADR against the code it governs (fix whichever
drifted); confirm every road still resolves. New `restate` files
are the signal that Phase 5's wiring needs strengthening, not
that the pass failed.

## Completion criteria

- Every agent-visible doc carries a tag and an executed verdict.
- Zero CONTRADICTED claims unresolved -- no dual truth anywhere.
- Every promoted keeper entry passes the non-derivability bar
  (references/keepers.md).
- Quarantined material sits on a branch, not gitignored on main.
- At least one code-legibility improvement landed from the
  savings.
- Agent instructions point at keepers + code, nothing else.

## Boundaries

- Multi-team and regulated repos get a tagged inventory and a
  recommendation, not a purge.
- This skill works agent-visible repo docs. Published docs sites,
  onboarding curricula, and compliance runbooks are `human-only`
  by default -- move them off the agent path rather than judging
  them.
- Keepers first, always: never delete `why` material before its
  keeper home exists.

## References

| File | Load when |
|---|---|
| references/rediscovery.md | Running Phase 2 -- claim extraction, subagent prompt, grading, per-doc scoring |
| references/keepers.md | Promoting survivors in Phase 3, or installing the keeper layer from scratch |

## Lineage

Operationalizes Matt Pocock's July 2026 delete-docs doctrine --
delete restate-the-code docs; keep ADRs, glossaries, and
navigation pointers; spend the savings on self-explanatory code;
quarantine on a separate branch -- and the derivability rule from
the surrounding discussion ("don't include anything in the docs
that could be discovered by reading the code," Fergus Noble). The
blind rediscovery test is this skill's own addition.
