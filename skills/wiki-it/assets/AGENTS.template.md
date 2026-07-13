# {VAULT_TITLE} -- agent operating contract

This directory is a knowledge vault: {DOMAIN_ONE_LINER}. It is
compiled by agents, reviewed by humans, and read by both. This file
is the contract for any agent working here -- no external skill is
required to operate this vault correctly. The vault is a conformant
OKF (Open Knowledge Format v0.1) bundle.

- Review policy: {POLICY}  <!-- strict | sampled (k per batch) | off -->
- WIP limit: {WIP_LIMIT} unreviewed editorial pages
- Center of gravity: {CENTER_TYPE} -- when in doubt, organize around it
- Format: {FORMAT}  <!-- "YAML frontmatter, nested directories (default)" or "Logseq: property:: lines, flat pages/, ___ namespaces" -->

## Orient -- every session, before anything

1. Read this file, then `index.md` (the map), then the tail of
   `log.md` (the recent past).
2. Search before you create: check index.md and grep for every
   entity you are about to write about. Duplicates come from
   skipped orientation.
3. Check `review.md`: over the WIP limit, stop editorial writing
   and tell the human.

## Schema

{SCHEMA}
<!-- concept types (~10 max) with required properties per type,
     link rules, controlled vocabularies, namespaces. Extend this
     section BEFORE using a new type, property, or tag -- never
     invent an off-schema pattern quietly. -->

## Write contract

- Every concept page carries `type`, `origin`, `description`, and
  (when editorial) `reviewed: false`. `origin` is provenance:
  `data` = derived from a structured source lint can re-check;
  `editorial` = an agent wrote judgments in prose; `human` = a
  person wrote or corrected it.
- Page thresholds: a concept earns a page at 2+ sources or by
  being central to one source; a passing mention earns a link, not
  a page. Split pages past ~200 lines.
- An ingest touches 5-15 pages and updates every hub it crosses.
- Append, never rewrite: `origin: human` and `reviewed: true`
  content is protected -- extend alongside or below it.
- Never set `reviewed: true` yourself. Flip it only on explicit
  human instruction, and record the instruction in `log.md`.
- Contradictions: keep both positions with dates and sources, set
  `contested: true`, and let the review queue surface it.
- Cite as you write: `# Citations` for external sources,
  `(ref: reference/<file>)` for supply-chain files, `(editorial)`
  on any unsourced claim -- reviewers read exactly the marked
  sentences.
- Source materials live in `reference/` outside the vault, never
  in here.
- A batch is not done until linted, committed, and the queue size
  reported to the human.

## Read contract

1. Triage on `description` fields; navigate via hubs; load at most
   ~5 pages in full.
2. Weight by trust: `reviewed: true` > `origin: data` > unreviewed
   editorial -- flag the latter when synthesizing from it.
3. File back syntheses that were painful to derive as new pages,
   and log them. Trivial lookups are not filed.

## Domain rules

{DOMAIN_RULES}
<!-- whatever the schema declares that an agent must not discover
     the hard way: per-type link requirements, naming conventions,
     controlled vocabularies -->
