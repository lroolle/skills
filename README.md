# skills

Agent skills collection. Each directory is a self-contained skill
following the [Agent Skills spec](https://agentskills.io/specification).

## Catalog

| Skill | Domain | Description |
|---|---|---|
| [kiln](kiln/) | Design | Precision UX design instrument -- perceptual principles, composable patterns, material palettes |
| [skillbun](skillbun/) | Meta | Bundle skills with dependencies into distributable .skillbun archives |
| [skillize](skillize/) | Meta | Crystallize a session's workflow into a reusable skill via eval pipeline |

## Install

### Claude Code (user-scope)

```bash
cp -r <skill-name> ~/.claude/skills/<skill-name>
```

### Claude Code (project-scope)

```bash
cp -r <skill-name> .claude/skills/<skill-name>
```

### Codex

```bash
cp -r <skill-name> ~/.codex/skills/<skill-name>
```

Restart the agent after installing.

## Structure

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

1. Copy `template/SKILL.md` into a new directory
2. Name the directory to match the `name:` field in frontmatter
3. Write the instructions
4. Install and test
5. Or: use `/skillize` after completing a workflow to auto-extract

## License

Individual skills may carry their own licenses. Unless stated
otherwise, skills in this repo are for personal use.
