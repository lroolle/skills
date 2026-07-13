# Formats -- Logseq variant and OKF conformance

Load when the vault targets Logseq, or when OKF conformance details
matter. The default format (YAML frontmatter, nested directories) is
OKF-native as SKILL.md describes it and needs no reference.

## Logseq variant

Logseq is an outliner: no YAML frontmatter, no nested directories.
Translate the contract:

- Properties are `property:: value` lines at the top of the page:

  ```
  - type:: composer
  - origin:: editorial
  - reviewed:: false
  - description:: Bridged Classical and Romantic; the heroic style
  ```

- Every line starts with `- ` (blocks). Headings live inside blocks:
  `- ## Why It Matters`.
- Files sit flat in `pages/`; namespaces use triple underscores:
  `Music___Composers___Bach.md` renders as `Music/Composers/Bach`.
- Wikilinks use the rendered path: `[[Music/Composers/Bach]]`.
- Hubs are the namespace pages themselves (`Music___Composers.md`),
  not index.md files.
- Journals (`journals/`) are Logseq's own; the vault contract does
  not apply there.
- Logseq's query system can surface pages by property (`type`,
  `reviewed`, any domain property) -- use it for review dashboards
  inside Logseq itself.

`vault_lint.py --format logseq` understands all of the above.

## OKF conformance and export

Google's Open Knowledge Format (v0.1) is a minimal convention for
knowledge bundles: markdown files with YAML frontmatter where `type`
is the only required key, `index.md` hubs without frontmatter, a
`log.md` history, links as plain markdown. Producer extensions
(unknown frontmatter keys) are legal -- consumers must tolerate and
preserve them, which is how our `origin`/`reviewed`/`volatility`
keys travel.

The distinction that matters: a YAML-frontmatter vault built by this
skill is OKF-conformant as it stands. A Logseq vault is
OKF-*convertible*, not OKF-native -- `property::` lines are not
frontmatter and flat `___` files are not directories. Author where
the human reviews (Logseq, if that's their surface); export OKF as
the interchange layer. Do not adopt OKF as the internal source of
truth for a Logseq vault -- the format's value is portability and
convention, not semantic depth.

Export: `scripts/logseq_to_okf.py <logseq-vault> <out-dir>` converts
`property::` lines to frontmatter, `___` names to directories, and
generates hub index.md files.

OKF conformance checklist for exported or native bundles:

- every non-reserved `.md` has parseable frontmatter with `type`
- `index.md` files carry no frontmatter and list children
- `log.md` groups entries by date, newest first
- links are standard markdown, absolute-from-root or relative
- consumers tolerate unknown keys and broken links (a broken link may
  be not-yet-written knowledge); producers still lint them

OKF links are untyped -- the relationship lives in the prose around
the link. When a domain needs typed edges (prerequisites, joins,
influences), encode the type in a frontmatter property or in the
sentence, and say so in the AGENTS.md schema section.
