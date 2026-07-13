# Editorial -- section shapes, hubs, and the log

Load in Bootstrap step 5 (Editorial), or when existing pages read
flat. The test for every
editorial page: does a reader learn something true that makes them
want to go deeper? "X is important because..." fails it; "here is
what X sounds like / does / costs, start with Y" passes.

## Section shapes by concept role

For a **center-of-gravity concept** (the thing readers look up):

- **What It Is** -- one paragraph, accessible to the target reader
- **Why It Matters** -- what makes this worth a page at all
- **How It Works / What You Will Experience** -- concrete and
  specific; the section that teaches
- **Where to Start** -- 3-5 entry points for a newcomer, each linked,
  each with a reason ("the Allegretto is haunting", not "famous")
- **Notable Examples** -- specific instances, linked
- **Cross-References** -- related concepts with a phrase of context
- **# Citations** -- numbered sources for the factual claims

For a **supporting concept** (forms, techniques, vocabulary):

- **What It Is** -- definition and scope
- **Key Examples** -- linked to center-of-gravity pages
- **How It Connects** -- its relationships, stated not implied

Editorial tier sizing: 20-50 pages. Below 20 the vault has no
product; above 50 quality collapses uniformly -- the model can write
50 pages worth reading and cannot write 200.

## Hub format

A hub's job is confident navigation: every child listed, each with a
one-liner that lets the reader (or a triaging agent) skip it.

```markdown
# Composers

220 composers, Medieval to present.

## Where to Start

- [Bach](bach.md) - the architect of Western music
- [Beethoven](beethoven.md) - bridged Classical and Romantic

## All Composers

- [Albeniz](albeniz.md) - Spanish piano miniatures
- [Bach](bach.md) - the architect of Western music
...
```

Hubs carry no frontmatter. "Where to Start" is editorial judgment;
"All X" is exhaustive -- a hub missing a child is a lint warning
because an unlisted page is unreachable by navigation.

## The log

`log.md` answers "what changed and when" without reading git history
-- it is the shared memory of every agent and human who works the
vault. Newest first, date headings, leading action words:

```markdown
# Update Log

## 2026-06-16

* **Enrichment**: 47 performer pages from MusicBrainz; schema
  extended with performer type.
* **Review**: human promoted 12 composer pages (instruction: "1-12
  look good").

## 2026-05-27

* **Editorial**: 32 composers, 48 works written; queue at 80 --
  over WIP limit, compilation paused.
```

Conventional action words: **Creation**, **Editorial**,
**Enrichment**, **Review**, **Fix**, **Deprecation**, **Schema**.
Review promotions always log the human's instruction -- the log entry
is what makes a `reviewed: true` flag auditable.
