---
name: wiki-it
description: >-
  Build and run a knowledge vault -- interlinked markdown+frontmatter
  pages compiled from sources by agents, made trustworthy through
  human review, self-describing so any agent can operate it without
  this skill. Fires on four branches: starting a vault ("build a
  wiki / knowledge base about X", "make this material navigable");
  working inside an existing vault (ingest a source, add or enrich
  pages -- the vault's own AGENTS.md wins where they disagree);
  review ("what needs review", work the queue, promote pages); and
  audit ("lint the vault", find stale, broken, or orphaned pages).
  Turning a source into agent behavior is distill's job; a one-shot
  report with no maintenance life needs no vault -- write the report
  directly.
---

# Wiki-it

The pipeline is a compiler: `Sources -> Schema -> Compiler (LLM) ->
Review gate (human) -> Product (plain files)`. The domain-specific
parts are the schema and the sources; the workflow is universal; the
product is markdown+frontmatter that outlives the agent, the human,
and the tooling.

Two tests, and both must pass:

- **Reader test:** a person lands on any editorial page and learns
  something true that makes them want to go deeper.
- **Cold-agent test:** an agent lands on the vault with this skill
  absent and still operates it correctly, because the vault carries
  its own contract (AGENTS.md, schema.md, llms.txt).

The second test is the architecture. This skill is the compiler and
toolchain; the vault is the program. Build-time knowledge lives here;
the run-time contract ships inside the vault, so it travels with the
artifact to every future agent, tool, and fork.

## Gate

A vault is a maintenance commitment, not a document. Size the ask
before building one:

| Situation                                                   | Move                                                                                |
|-------------------------------------------------------------|-------------------------------------------------------------------------------------|
| One question, one answer                                    | Answer it. No vault.                                                                |
| Source should change how agents *behave*                    | distill's job.                                                                      |
| A report nobody will maintain                               | Write the report directly.                                                          |
| Under ~15 concepts                                          | One reference page, not a vault.                                                    |
| Directory already has AGENTS.md / schema.md                 | Operate mode: read them first -- they win over this skill. Jump to Operating modes. |
| A domain with structure, recurring readers, growing sources | Build: Phases 0-4.                                                                  |

## Trust model

The scarcest resource in the loop is human review minutes. Evidence
from a real build: a 314-page vault shipped with zero pages reviewed
-- not because review was refused, but because it was packaged as
homework ("read 300 pages"). Review debt is the default outcome
unless the design spends human attention only where machines cannot
verify. Three consequences:

`origin` names where trust comes from; `reviewed` records that a
human spent theirs.

| origin      | trust source                                                      | human review                     |
|-------------|-------------------------------------------------------------------|----------------------------------|
| `data`      | mechanically derived from a structured source; lint can re-verify | not required                     |
| `editorial` | an agent wrote judgments in prose                                 | required -- enters the queue     |
| `human`     | a person wrote or corrected it                                    | protected: append, never rewrite |

- Agents never set `reviewed: true` on their own judgment. Flip it
  only on an explicit human instruction, and record that instruction
  in log.md -- the flag is a signature, and a forged signature is
  worse than none.
- **WIP limit.** When unreviewed editorial pages exceed the vault's
  limit (default 20), stop compiling and surface the queue. A batch
  that writes 100 editorial pages doesn't produce knowledge, it
  produces debt.
- **Review policy**, declared at bootstrap with one question to the
  human: `strict` (every editorial page queues), `sampled`
  (spot-check k of each batch, log the result), or `off` (agent-only
  vault -- honest, but the front page must say so).

## Vault anatomy

```
vault/                     ships; a git repo from the first commit
  AGENTS.md                operating contract (generated at bootstrap)
  index.md                 front door; no frontmatter
  schema.md                types, properties, link rules -- source of truth
  review.md                the queue: generated, risk-ranked, never hand-edited
  log.md                   what changed, newest first
  llms.txt                 one-fetch map for agents
  <namespace>/
    index.md               hub: lists every child with a one-liner
    <concept>.md           one concept per file; ID = path minus .md
reference/                 supply chain: sources, dumps, clones. Never ships,
                           never inside vault/ -- mixing them is how a
                           vault stops being a product.
```

Frontmatter contract for concept pages (index, log, review, llms.txt
exempt):

```yaml
---
type: <concept-type>              # required; defined in schema.md
origin: data | editorial | human  # required; see Trust model
reviewed: false                   # required when origin: editorial
title: <display name>
description: <one line>           # agents triage on this -- write it so a
                                  # page can be *skipped* confidently
volatility: hot | warm | cold | frozen   # staleness horizon 30/90/365/never
aliases: [alt names]
---
```

Cite as you write: a numbered `# Citations` section for external
sources, `(ref: reference/<file>)` for supply-chain files, and
`(editorial)` on any claim with no source behind it. The
`(editorial)` marks are not decoration -- the review queue counts
them and the reviewer reads exactly those sentences. An unmarked
unsourced claim is a hallucination nobody will ever check.

## Build protocol

### Phase 0 -- Survey

Collect sources into `reference/`: repos, dumps, docs, analyses.
Prefer many chapter-sized files over one book-sized file -- the same
model produces slop from a 500-page input and signal from its
chapters. Done when: you can name the domain's kinds (what are the
things?), its links (how do they connect?), and its center of
gravity (what does a reader actually look up?).

### Phase 1 -- Schema

Concept types (at most ~10 -- more means the ontology needs merging),
required properties per type, link rules (what must point at what),
center of gravity, namespaces. Write schema.md. Ontology design is a
decision where the obvious answer being wrong is expensive -- when
the kinds are unclear, spread alternatives before committing
(parallax, if available). Done when: the human has seen and approved
schema.md -- pages generated before schema agreement are pages
generated twice.

### Phase 2 -- Bootstrap

This phase makes the vault self-describing:

1. `git init` the vault; the contract is the first commit.
2. Generate AGENTS.md from `assets/AGENTS.template.md`: write/read
   contract, domain rules, format, review policy, WIP limit.
3. Write index.md, llms.txt, log.md, and an empty review.md.
4. Ask the human the one bootstrap question: review policy and WIP
   limit.

Done when: `scripts/vault_lint.py` passes on the empty vault, and the
cold-agent test holds -- AGENTS.md alone would teach a skill-less
agent the contract.

### Phase 3 -- Scaffold

Pages from structured sources: correct frontmatter with
`origin: data`, minimal body, hubs listing every child, stubs so no
link points at nothing. No prose here -- scaffold written as prose
produces hundreds of mediocre pages instead of hundreds of accurate
rows; a stub with true properties beats a paragraph of filler. Done
when: every link resolves, lint is clean, and the batch is committed.

### Phase 4 -- Editorial

The product. Pick the canon: the 20-50 concepts nearest the center
of gravity. Write sections that teach, not describe -- load
`references/editorial.md` for section shapes per concept role. Every
editorial page: 5+ outgoing links, citations, `(editorial)` marks,
`origin: editorial`, `reviewed: false`. Two-layer honesty: an LLM
generates 200 accurate stubs in minutes and cannot write 200 pages
worth reading, so the editorial tier is small on purpose. Done when:
the canon is written, the queue is regenerated, the WIP limit is
respected, the batch is committed, and the queue size with estimated
review minutes is reported to the human.

## Operating modes

Most sessions in a vault's life are these, not the build. Inside an
existing vault its own AGENTS.md is authoritative; what follows is
the default contract a bootstrap installs.

### Ingest (the habit)

Accept a source -> classify it against schema.md -> touch 5-15 pages
(create or append; the range forces cross-referencing -- a one-page
ingest is a note, not knowledge) -> update hubs -> lint -> commit ->
report the queue. Append to existing pages rather than rewriting.
Never rewrite `origin: human` or `reviewed: true` content without
explicit instruction -- create alongside instead. If the source does
not fit the schema, extend schema.md first and log the extension;
inventing an off-schema pattern quietly is how vaults rot.

### Review (agent prepares, human decides)

1. Regenerate the queue: `scripts/vault_lint.py <vault>` writes
   review.md ranked by incoming links (gravity first); each entry
   carries the page description and its count of `(editorial)`
   claims.
2. The human works the queue in their own reading surface (Logseq,
   Obsidian, editor, any rendering server). Their cost per page is
   verifying the flagged claims -- ~30 seconds, not 5 minutes.
3. On "promote"/"looks good": set `reviewed: true` and log the
   instruction.
4. When the human edits a page directly, it becomes `origin: human`
   and inherits protection.

Report the queue size at the end of every writing session -- silent
debt is how 314 unreviewed pages happen.

### Audit

Run `scripts/vault_lint.py` for mechanics: missing required
properties, broken links, orphans, empty pages, duplicate titles,
credential leaks, stale-by-volatility. Load `references/lint.md` for
the full rule table and severities. Lint is the migration: when the
schema evolves, fix pages to conform rather than writing migration
scripts. For editorial quality beyond mechanics, sample pages against
the Check rubric.

## Read contract

For any agent in any session, including this one:

1. One fetch first: llms.txt or AGENTS.md -- the map before the rooms.
2. schema.md before concept pages.
3. Triage on `description`, navigate via hubs, load at most ~5 pages
   in full. A 300-page vault does not fit in context; it is designed
   so you never need it to.
4. Frontmatter before body -- for scanning tasks the properties
   suffice.
5. Weight by trust: `reviewed: true` > `origin: data` > unreviewed
   editorial. Flag unreviewed editorial when synthesizing from it.
6. Vault vs agent memory: dangerous-if-forgotten goes to memory;
   useful-when-asked goes to the vault.

## Check

Smash what fails -- each is a defect, not a style preference:

- prose page labeled `origin: data` (trust mislabeled)
- editorial page that describes instead of teaches ("X is important
  because...")
- unsourced claim without an `(editorial)` mark
- queue above the WIP limit while compilation continues
- reference material inside vault/, or vault pages in reference/
- link to nowhere; hub missing a child; orphaned concept page
- `reviewed: true` with no logged human instruction
- vault not a git repo, or a batch left uncommitted
- schema violated silently instead of extended loudly

## Toolchain

- `scripts/vault_lint.py <vault> [--format logseq] [--queue-out PATH]`
  -- stdlib-only lint and review-queue generator; exit 1 on errors.
- `scripts/logseq_to_okf.py` -- export a Logseq vault to an OKF
  bundle (YAML frontmatter, hub index.md files).
- `references/formats.md` -- load when the vault is Logseq, or when
  OKF export or compatibility matters.
- `references/editorial.md` -- load in Phase 4, or when pages read
  flat.
- `references/lint.md` -- load when auditing.
- `references/lessons.md` -- load when designing a new vault or when
  a living vault feels wrong: failure modes and the patterns that
  counter them.

---

Lineage: distilled from six llm-wiki implementations, Google's Open
Knowledge Format v0.1, and a 314-page classical-music vault build.
Supersedes knowledge-vault v1.
