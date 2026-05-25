# Skills

> Agent skills for Claude Code, Codex, and any [agentskills.io](https://agentskills.io)-compatible agent.

[![license](https://img.shields.io/github/license/lroolle/skills)](LICENSE)
[![spec](https://img.shields.io/badge/spec-agentskills.io-blue)](https://agentskills.io/specification)

Opinionated skills for design, workflow capture, and skill distribution.
Each skill is a self-contained directory with a `SKILL.md` file --
instructions, references, and scripts that agents load dynamically.

## Skills

| Skill | What it does |
|---|---|
| [kiln](skills/kiln/) | UX design instrument. Layered architecture: perceptual principles, composable patterns, parameterized material palettes, anti-AI-slop detection. Six curated kits (broadsheet, terminal, warm-ground, cold-open, gallery, burnt-studio). Generates and audits interfaces. |
| [skillize](skills/skillize/) | Session-to-skill crystallizer. Extracts repeatable workflows from agent sessions, classifies corrections by durability, drafts SKILL.md with references. Optional eval pipeline via skill-creator. |
| [skillbun](skills/skillbun/) | Skill bundler. Resolves inter-skill dependencies, renames to avoid collisions, packages multiple skills into a single `.skill` archive for distribution. |

## Quick start

### Install a single skill

```bash
# Claude Code
cp -r skills/kiln ~/.claude/skills/kiln

# VS Code / Copilot
cp -r skills/kiln .agents/skills/kiln

# Codex
cp -r skills/kiln ~/.codex/skills/kiln
```

Restart your agent after installing.

### Use it

Just mention the skill's domain in conversation. Skills activate
automatically based on their description:

```
> Design a dashboard for monitoring build pipelines
  (kiln activates -- loads patterns, materials, motion references)

> Turn this session into a reusable skill
  (skillize activates -- surveys session, crystallizes workflow)

> Bundle skillize with its dependencies for sharing
  (skillbun activates -- resolves deps, renames, packages)
```

Or invoke directly: `/kiln craft`, `/skillize`, `/skillbun skillize`.

## Repo structure

```
.
├── skills/                   # all skills live here
│   ├── kiln/                 #   UX design (6 files)
│   │   ├── SKILL.md
│   │   └── references/       #   patterns, materials, motion, adaptation, zeitgeist
│   ├── skillize/             #   session-to-skill (2 files)
│   │   ├── SKILL.md
│   │   └── references/       #   crystallization heuristics
│   └── skillbun/             #   skill bundler (3 files)
│       ├── SKILL.md
│       ├── references/       #   bundle format spec
│       └── scripts/          #   bundle.sh helper
└── template/                 # starter SKILL.md for new skills
    └── SKILL.md
```

Each skill follows the [Agent Skills spec](https://agentskills.io/specification):

```
skill-name/
├── SKILL.md          # required: metadata + instructions (<500 lines)
├── references/       # optional: domain knowledge, loaded on demand
├── scripts/          # optional: executable helpers
└── assets/           # optional: templates, static resources
```

## Creating a new skill

1. Copy `template/SKILL.md` into a new directory under `skills/`
2. Name the directory to match the `name:` field in frontmatter
3. Write the instructions
4. Test: `cp -r skills/my-skill ~/.claude/skills/my-skill`
5. Or: use `/skillize` after completing a workflow to auto-extract

See [agentskills.io/skill-creation/best-practices](https://agentskills.io/skill-creation/best-practices)
for writing guidance.

## How skills work

Skills use progressive disclosure to stay lightweight:

1. **Metadata** (~100 tokens) -- `name` and `description` from frontmatter.
   Always loaded. This is how the agent decides whether to activate the skill.
2. **Instructions** (<5000 tokens) -- the full SKILL.md body.
   Loaded when the skill activates.
3. **References** (on demand) -- files in `references/`, `scripts/`, `assets/`.
   Loaded only when the skill's instructions say to.

The agent reads many skill descriptions but only loads the full body of
skills relevant to the current task.

## Contributing

1. Fork the repo
2. Create your skill under `skills/`
3. Validate: `name` matches directory, description under 1024 chars,
   SKILL.md under 500 lines
4. Open a PR

## License

[Apache 2.0](LICENSE)
