# Skills

> Agent skills for design, workflow capture, and skill distribution.

[![license](https://img.shields.io/github/license/lroolle/skills)](LICENSE)
[![spec](https://img.shields.io/badge/spec-agentskills.io-blue)](https://agentskills.io/specification)

Small, composable skills that solve real problems I hit daily with Claude Code
and Codex. Not a framework. Not a process. Just focused tools you can drop into
any project and hack on.

## Quickstart

```bash
npx skills@latest add lroolle/skills
```

Pick the skills you want and which agents to install them on.

<details><summary>Manual install</summary>

```bash
git clone https://github.com/lroolle/skills.git
cd skills
./scripts/link-skills.sh
```

Or copy individual skills:

```bash
cp -r skills/design/kiln ~/.claude/skills/kiln
```

</details>

## Why these skills exist

### The AI-generated look

Most AI-built interfaces are instantly recognizable: Inter font, purple
gradient, card-in-card layouts, magnetic cursor effects. They converge on the
same defaults because agents reach for training-data reflexes.

**kiln** fixes this by separating permanent perceptual rules (human vision
doesn't change) from temporal taste (what's saturated right now). It ships six
material kits with distinct personalities, anti-pattern detection, and a
quarterly-versioned zeitgeist file that tracks which aesthetics have been
strip-mined by AI generators.

### The workflow you can't repeat

You spend 40 minutes getting an agent to do something perfectly -- tool
sequences, corrections, domain knowledge discovered along the way. Next week
you need the same workflow and start from scratch.

**skillize** crystallizes a session into a reusable skill. It surveys the
conversation, classifies corrections by durability (permanent rule vs one-off
fix), extracts the repeatable pattern, and drafts a SKILL.md. The workflow is
preserved, not just the output.

### Skills that can't travel alone

You build a skill that depends on another skill's scripts. You share the
`.skill` file and the recipient's eval pipeline silently breaks because the
dependency isn't there.

**skillbun** resolves inter-skill dependencies, renames to avoid collisions
with independently installed copies, and packages everything into a single
`.skill` archive. One file, one install.

## Reference

### Design

Skills for frontend craft, UX, and visual design.

- **[kiln](skills/design/kiln/SKILL.md)** -- Precision UX design instrument.
  Layered architecture: perceptual principles -> composable patterns ->
  parameterized material palettes. Six curated kits. Anti-AI-slop detection.
  Generates and audits interfaces.

### Meta

Skills for building, packaging, and distributing other skills.

- **[skillize](skills/meta/skillize/SKILL.md)** -- Session-to-skill
  crystallizer. Extracts repeatable workflows from agent sessions, classifies
  corrections, drafts SKILL.md with references. Optional eval pipeline.
- **[skillbun](skills/meta/skillbun/SKILL.md)** -- Skill bundler. Resolves
  dependencies, renames to avoid collisions, packages into `.skill` archives.

## Repo structure

```
.
├── .claude-plugin/           # plugin manifest for skills.sh
│   └── plugin.json
├── scripts/                  # repo utilities
│   ├── link-skills.sh        #   symlink all skills to ~/.claude/skills/
│   └── list-skills.sh        #   list all SKILL.md files
├── skills/
│   ├── design/               #   frontend craft, UX
│   │   └── kiln/
│   └── meta/                 #   skill tooling
│       ├── skillize/
│       └── skillbun/
└── template/                 # starter SKILL.md
    └── SKILL.md
```

## Creating a new skill

1. Copy `template/SKILL.md` into a new directory under `skills/<category>/`
2. Name the directory to match the `name:` field in frontmatter
3. Write the instructions (keep SKILL.md under 500 lines)
4. Add the skill to `.claude-plugin/plugin.json` and the category `README.md`
5. Test: `./scripts/link-skills.sh` then invoke in your agent

Or: use `/skillize` after completing a workflow to auto-extract one.

## Contributing

1. Fork the repo
2. Create your skill under the appropriate `skills/<category>/`
3. Validate: `name` matches directory, description under 1024 chars
4. Add to category `README.md` and `.claude-plugin/plugin.json`
5. Open a PR

## License

[Apache 2.0](LICENSE)
