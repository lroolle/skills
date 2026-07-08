# Health-file stack — minimal viable versions

Commodity knowledge (any senior engineer would list these), kept as
a checklist so the renovate beat doesn't re-derive it. The taste
rule: every file must be honest at this repo's scale — a generated
corporate CODE_OF_CONDUCT on a 2-star repo reads worse than none.

## Tier 1 — every public repo

- LICENSE (SPDX-recognized; badge links to it)
- README per readme-anatomy.md
- Sensible description + topics + homepage (agent-surface.md)
- .gitignore that matches reality
- Auto-delete merged branches (repo setting)

## Tier 2 — anything you want used

- CHANGELOG.md — Keep-a-Changelog format; "Unreleased" section
  maintained; entries say why it matters, not just what changed
- SECURITY.md — supported-versions table + how to report privately;
  only if someone actually reads the inbox
- Issue templates: bug (repro required), feature request; config.yml
  routing questions to discussions/chat
- PR template: description, type checkboxes, "what you actually ran"
  testing section with pasted output
- Tagged releases at meaningful points — "latest release 14 months
  ago" next to daily commits reads as chaos; automate:
  release-please (or equivalent) + conventional commits enforced by
  commitlint; version stamped across package files via extra-files
- CI badge that reflects a real test run

## Tier 3 — when contributors arrive (not before)

- CONTRIBUTING.md with routing table (bug → PR with repro+test;
  feature → issue first; refactor-only → don't; new dep → written
  justification), verification-is-the-author's-job policy, open-PR
  cap per author
- CODEOWNERS, dependabot, stale bot, CODE_OF_CONDUCT
- copilot-instructions.md / CLAUDE.md for agent contributors
- Devcontainer for one-command contributor setup

## Tier 4 — when the product warrants

- llms.txt live index + llms-full.txt on the docs site
- Plugin marketplace (.claude-plugin/marketplace.json)
- Docker images with sane tags; SBOM if enterprise users appear
- Community space (Discord/Discussions) — only with the traffic to
  keep it alive; a dead Discord is anti-marketing
