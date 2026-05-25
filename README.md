# skills

Agent skills collection. Each skill is a self-contained directory
following the [Agent Skills spec](https://agentskills.io/specification).

## Catalog

| Skill | Domain | Description |
|---|---|---|
| [kiln](skills/kiln/) | Design | Precision UX design instrument -- perceptual principles, composable patterns, material palettes |
| [skillbun](skills/skillbun/) | Meta | Bundle skills with dependencies into distributable .skill archives |
| [skillize](skills/skillize/) | Meta | Crystallize a session's workflow into a reusable skill via eval pipeline |

## Install

### Claude Code (user-scope)

```bash
cp -r skills/<skill-name> ~/.claude/skills/<skill-name>
```

### Claude Code (project-scope)

```bash
cp -r skills/<skill-name> .claude/skills/<skill-name>
```

### Codex

```bash
cp -r skills/<skill-name> ~/.codex/skills/<skill-name>
```

Restart the agent after installing.

## Repo structure

```
.
├── README.md
├── template/             # starter SKILL.md for new skills
│   └── SKILL.md
└── skills/               # all skills
    ├── kiln/
    ├── skillbun/
    └── skillize/
```

Each skill follows the spec's progressive disclosure model:

```
skill-name/
├── SKILL.md          # metadata + instructions (<500 lines)
├── references/       # domain knowledge, loaded on demand
├── scripts/          # executable helpers
└── assets/           # templates, static resources
```

Only `SKILL.md` is required. See [template/](template/) for a starter.

## Creating a new skill

1. Copy `template/SKILL.md` into a new directory under `skills/`
2. Name the directory to match the `name:` field in frontmatter
3. Write the instructions
4. Install and test
5. Or: use `/skillize` after completing a workflow to auto-extract

## License

Individual skills may carry their own licenses. Unless stated
otherwise, skills in this repo are for personal use.
