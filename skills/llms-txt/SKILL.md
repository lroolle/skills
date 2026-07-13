---
name: llms-txt
description: >-
  Generate and maintain llms.txt -- the curated markdown map a
  website, docs directory, repo, or knowledge vault publishes at its
  root so agents can orient in one fetch. Fires on three branches:
  creating one ("add llms.txt", "make my site/docs/repo
  agent-readable", GEO/AEO asks); refreshing an existing llms.txt
  after content changed (minimal diff, stable ordering); and
  checking one ("is my llms.txt valid or stale?"). Whole-repo
  release packaging is burnish's job -- it routes here for this one
  artifact; compiling sources into a knowledge vault is wiki-it's
  job. llms-txt maps content that already exists.
---

# llms-txt

llms.txt is robots.txt inverted: not what a crawler may read, but
the fastest true path through what it should. One markdown file at
the corpus root -- a title, a blockquote summary, and sections of
links with one-line descriptions -- so orientation costs an agent
one fetch instead of a crawl through HTML built for humans.

It is a derived artifact, and stability is the contract: the map is
regenerated from the corpus, never hand-grown. Rerun on an unchanged
corpus, the file is byte-identical; refresh after a change, and only
the entries whose sources changed move. A map that drifts from its
territory is worse than no map -- agents trust the map first.

## Gate

Honesty first: evidence that classic search crawlers fetch llms.txt
is thin. Its real consumers are agents fetching docs on demand and
humans loading docs into context. Sell it as agent-legibility; treat
GEO/SEO as possible upside, never the promise.

| Situation | Move |
|---|---|
| Goal is ranking in classic search | Not this file -- improve the docs and page metadata themselves. |
| Private corpus for your own agents | That is a vault's index.md (wiki-it), not a published map. |
| Whole-repo release polish | burnish's job; it routes back here for this one artifact. |
| Corpus is a single README | The README already is the map. Skip. |
| Site, docs dir, repo, or vault that agents will read | Build the map. |

## The format

The shape, per the llms.txt proposal:

```markdown
# Project Name

> One-paragraph summary: what this is and who it serves.

Optional prose: constraints, versions, gotchas an agent must know
before following any link.

## Section Name

- [Page title](https://example.com/docs/page.md): one line that
  lets an agent decide to fetch or skip

## Optional

- [Secondary page](url): safe to drop when context is tight
```

Rules: exactly one H1, first line of the file; blockquote summary
directly after it; every other section is an H2 over a list of
links. `## Optional` is the only reserved section name -- agents may
drop it when context is tight, so nothing load-bearing goes there.
Link the markdown version of a page whenever one exists; HTML is
what this file routes around. Every URL must be fetchable without
auth by a stranger's agent.

## Protocol

### Survey

Inventory the corpus and collect each page's existing
self-description: frontmatter `description`, HTML meta description,
first heading plus first sentence, nav/sidebar titles. Identify the
reader tasks the corpus serves (get started, look up API, understand
concepts, see examples). If an llms.txt already exists, switch to
Refresh. Done when: every candidate page is listed with its best
existing description, or flagged as having none.

### Map

Choose sections by reader task, not by directory tree -- "Getting
started / API / Concepts / Examples" beats mirroring `src/`. Most
load-bearing section first; genuinely secondary material goes under
`## Optional`. Fix the ordering rule once -- nav order where the
corpus has one, alphabetical where it doesn't -- because a stable
order is what keeps refresh diffs minimal. Done when: the section
list, entry order, and canonical URL form are decided.

### Write

Derive every description from the page's own self-description; write
one from scratch only where none exists, one line, tuned so an agent
can *skip* confidently. No marketing voice: the blockquote orients
("what this is"), it does not sell ("blazingly fast"). Done when:
the file matches the format above and every entry passes the
fetch-or-skip test.

### Check

Run `scripts/llms_txt_check.py <llms.txt> [--root DIR]`: shape
validity, dead local links, drift against the corpus. Then rerun
your own generation pass mentally or literally: an unchanged corpus
must yield an unchanged file. Done when: the checker exits 0 and a
rerun produces no diff.

## Refresh

Diff the corpus against the map, then touch only what changed: new
content adds entries in their ordered place; removed content deletes
its entries; a changed page updates its description only if the
page's own self-description changed. Never reorder, never reword
untouched entries -- the diff a reviewer sees should be exactly the
content change, nothing else. Report added / removed / updated
counts. Done when: the checker passes and the diff contains no line
whose source didn't change.

## llms-full.txt

When the corpus's full text is small enough to load whole (roughly
under ~100k tokens), also emit `llms-full.txt`: the mapped pages'
markdown content concatenated in map order with clear separators.
The map is for routing; the full file is for agents that want the
territory in one fetch. Regenerate it wholesale on every refresh --
it is mechanical, and partial updates are where corruption hides.

## Check rubric

Smash what fails:

- description invented where the source already had one
- refresh diff touching entries whose sources didn't change
- link a stranger's agent cannot fetch (auth-walled, 404, moved)
- section named after a directory instead of a reader task
- load-bearing content parked under `## Optional`
- blockquote that sells instead of orients
- map listing a page the corpus no longer contains
- corpus page an agent would need that the map doesn't route to

## Toolchain

- `scripts/llms_txt_check.py <llms.txt> [--root DIR]` -- stdlib-only
  shape validator, dead-link and drift reporter; exit 1 on errors.

---

Lineage: the llms.txt proposal (Answer.AI, CC BY), HN field reports
on real-world adoption, and the map conventions shared with wiki-it
vault indexes.
