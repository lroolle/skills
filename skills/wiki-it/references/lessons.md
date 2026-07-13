# Lessons -- what breaks, and the patterns that counter it

Load this when designing a new vault (Bootstrap steps 1-3) or when a
living vault feels wrong. Sourced from six llm-wiki implementations,
30+ practitioner reports, and a 314-page vault build.

## What breaks

| Failure mode | Why it happens | Counter |
|---|---|---|
| Review debt | Review packaged as homework; agent out-produces human attention | origin tiers, queue with briefs, WIP limit, end-of-session queue report |
| Entropy accumulation | LLMs add without pruning | schema constraints, lint, volatility staleness, log.md |
| Confident errors compound | Bad entries get cited by later agents | `reviewed` gate, citations, `(editorial)` marks |
| Coverage theater | Bulk generation feels like progress; each page is "a database row wearing a markdown costume" | two-layer split: scaffold is `origin: data` infrastructure, editorial is the product |
| Novelty cliff | More fun to build than to use | editorial pages must teach; ingest habit keeps the vault alive |
| Context ceiling | Vault exceeds model context | description triage, hub navigation, ~5-page load budget |
| Human edits clobbered | Agent rewrites what a person fixed | `origin: human` protection; append, never rewrite |
| Source granularity wrong | Book-sized inputs produce slop | split to chapter/section before compiling |
| Uncommitted drift | "Commit each phase" stated but never enforced | git init at bootstrap; a batch isn't done until committed |
| Secret leak | Vault is git-tracked; agents paste credentials into pages | credential lint (error severity); secrets never belong in a vault |
| Duplicate pages | Session skipped orientation; agent wrote without checking what exists | orient ritual (contract, map, log tail), then search before create |

The review-debt row is the load-bearing one. The 314-page build had a
correct write contract and a described review phase -- and still
ended with zero pages reviewed and zero commits. Contracts that
depend on the human initiating work do not execute; contracts where
the agent prepares and the human only decides, do.

## The pattern shelf

Adopt deliberately; each earned its place in at least one working
implementation.

- **Routing test (vault vs memory).** "If the agent errs without this
  fact, is it dangerous? -> agent memory. Merely inconvenient? ->
  vault." Credentials and safety rules never go in a git-tracked
  vault.
- **Orient ritual.** Contract, map, log tail -- three reads before
  any operation, then search before create. Every duplicate page
  traces back to a session that skipped this.
- **Page thresholds.** A concept earns a page at 2+ sources or by
  being central to one; a passing mention earns a link. Split past
  ~200 lines; archive fully superseded pages.
- **Query file-back.** Syntheses painful to derive become pages;
  trivial lookups don't. The read path is where a vault compounds --
  today's question is tomorrow's page.
- **Contradiction protocol.** Keep both positions with dates and
  sources, set `contested: true`, let the queue surface it. Silent
  overwrite destroys the evidence a reviewer needs.
- **JIT retrieval.** Load at most ~3-5 pages in full per task;
  descriptions and hubs exist so this is enough.
- **5-15 page touches per ingest.** Forces cross-referencing; below
  the range you wrote a note, above it you're bulk-generating.
- **Append-only for existing pages.** Rewrites destroy provenance and
  human edits; appends accumulate. Reserve rewrites for explicit
  restructuring instructions.
- **Review queue over review phase.** A generated, risk-ranked queue
  with per-page briefs converts review from a project into minutes.
- **Sampled promotion.** For scaffold batches: spot-check k of N
  against the source; log pass/fail for the batch. Mechanical trust
  for mechanical content.
- **Validation gate on entry.** A page enters the graph only when its
  required properties parse -- reject at write time, not audit time.
- **WIP limit.** Cap unreviewed editorial pages (default 20). The cap
  throttles the agent's overproduction instinct and makes review a
  rhythm instead of a reckoning.
- **Center of gravity.** One concept type everything radiates from
  (the thing a reader looks up). It decides the editorial canon, the
  queue ranking, and the hub layout.

## Schema examples by domain

| Domain | Center | Types | Key cross-refs |
|---|---|---|---|
| Classical music | Work | Composer, Work, Form, Epoch, Performer, Recording | Work -> Composer, Work -> Form |
| Programming | Function | Module, Function, Type, Pattern, Example | Example -> Function, Function -> Module |
| Cooking | Recipe | Recipe, Ingredient, Technique, Cuisine | Recipe -> Ingredient, Recipe -> Technique |
| History | Event | Event, Person, Place, Period, Source | Event -> Person, Event -> Period |
| Data catalog | Table | Dataset, Table, Column, Metric, Query, Playbook | Query -> Table, Table -> Dataset |
| Biology | Organism | Species, Gene, Pathway, Ecosystem | Species -> Gene, Gene -> Pathway |
