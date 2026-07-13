# Lint -- rules, severities, and the migration principle

Load when auditing. `scripts/vault_lint.py` implements the mechanical
rules; the judgment rules at the bottom are sampled by hand against
the Check rubric in SKILL.md.

Severities: **error** breaks the contract (exit 1; the batch does not
ship), **warning** degrades quality, **info** is an improvement
opportunity.

## Mechanical rules (vault_lint.py)

| # | Rule | Severity | Auto-fixable |
|---|---|---|---|
| 1 | Missing `type` on a concept page | error | no -- requires classification |
| 2 | Missing or invalid `origin` | error | no -- requires provenance judgment |
| 3 | `origin: editorial` without `reviewed` | error | yes: add `reviewed: false` |
| 4 | Credential/secret pattern in content | error | no -- remove and rotate |
| 5 | Broken wikilink or relative link | warning | yes: create a stub target |
| 6 | Hub missing a child | warning | yes: append the entry |
| 7 | Orphan page (no incoming links; hubs exempt) | warning | yes: link from hub |
| 8 | Empty body (frontmatter only) | warning | no |
| 9 | Duplicate titles/aliases (case-insensitive) | warning | no -- merge or alias |
| 10 | `index.md` carrying frontmatter | info | yes: remove it |
| 11 | Stale by volatility (hot 30d / warm 90d / cold 365d / frozen never) | info | no -- re-verify content |
| 12 | Page body over ~200 lines | warning | no -- split into sub-topics |
| 13 | `contested: true` page (unresolved contradiction) | info | no -- human resolves |
| 14 | Queue exceeds the WIP limit declared in AGENTS.md | warning | no -- stop editorial writing, work the queue |

Auto-fixes are proposals: apply them, then commit them as their own
batch so the human can see what lint changed.

## Domain rules

The AGENTS.md schema section declares per-type requirements ("works
must link their composer and form", "queries must link a table").
Audit them with the same severities; when a rule fires on many pages
at once, the schema changed -- which is the point:

**Lint is the migration.** When the schema evolves, do not write
migration scripts or grandfather old pages. Update AGENTS.md, run
the audit, fix pages until clean. The schema stays alive because
conformance is continuously re-earned, and the fix batch documents
the migration in git.

## Judgment rules (sampled by hand)

Mechanics can't catch these; sample 5-10 pages per audit:

- editorial page that describes instead of teaches
- unsourced claim missing its `(editorial)` mark
- description field that doesn't let a reader skip the page
- prose smuggled into `origin: data` pages
- citations that don't actually support the sentence they follow
