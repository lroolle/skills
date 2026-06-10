Skills live in flat directories under `skills/`. Each skill is a
self-contained folder with a SKILL.md and optional bundled resources
(scripts/, references/, assets/).

Every skill in `skills/` must have:
- An entry in `.claude-plugin/plugin.json`
- A listing in the top-level `README.md`

Skill structure follows the agent skills spec (agentskills.io):
- `name` and `description` in YAML frontmatter (required)
- SKILL.md body under 500 lines
- Description is the trigger mechanism -- write it pushy
- References loaded on demand, not always
