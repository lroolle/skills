# Bundle Format

A .skillbun is a distributable archive containing multiple agent
skills with dependency metadata and an install script.

## Directory layout

```
<bundle-name>/
├── BUNDLE.md              # manifest (required)
├── install.sh             # install script (required)
└── skills/                # skill directories
    ├── <primary-skill>/
    │   ├── SKILL.md
    │   ├── references/
    │   ├── scripts/
    │   └── assets/
    └── <dependency-skill>/
        ├── SKILL.md
        └── ...
```

## BUNDLE.md format

YAML frontmatter + markdown body, mirroring SKILL.md's pattern.

### Frontmatter fields

| Field | Required | Description |
|---|---|---|
| name | yes | Bundle identifier, kebab-case |
| version | yes | Semver string |
| created | yes | ISO-8601 date |
| skills | yes | Array of skill entries |
| system-requirements | no | Runtime dependencies (git, python, etc.) |

### Skill entry fields

| Field | Required | Description |
|---|---|---|
| name | yes | Skill directory name |
| role | yes | `primary` or `dependency` |
| required-by | if dependency | Which skill needs this |

### Example frontmatter

```yaml
---
name: skillize-bundle
version: 1.0.0
created: 2026-05-22
skills:
  - name: skillize
    role: primary
  - name: skill-creator
    role: dependency
    required-by: skillize
system-requirements: python3, claude-cli (for description optimization)
---
```

### Body sections

1. **One-paragraph description** of what the bundle provides
2. **Contents table**: skill name, role, one-line description
3. **Install instructions**: both script and manual
4. **Dependency graph**: ASCII representation
5. **Compatibility notes**: system requirements, agent compatibility

## Archive format

A `.skillbun` file is a standard zip archive:

```bash
# Create
zip -r my-bundle.skillbun my-bundle/

# Extract
unzip my-bundle.skillbun

# Inspect without extracting
unzip -l my-bundle.skillbun
```

The extension is conventional, not required. Any zip tool works.

## install.sh contract

The install script must:

1. Be POSIX-compatible (bash or sh)
2. Work on macOS and Linux
3. Detect the user's skill root directory
4. Back up existing skills before overwriting
5. Copy each skill to the target root
6. Print what it installed
7. Exit 0 on success, non-zero on failure
8. Not require sudo or elevated permissions
9. Not install system packages or modify PATH
10. Not phone home or fetch remote resources

Detection order for skill root:

```
$AGENT_SKILLS_DIR          # explicit override
$HOME/.claude/skills       # Claude Code
$HOME/.agents/skills       # VS Code / Copilot
$HOME/.codex/skills        # Codex
```

If multiple roots exist, install to the first found and print
a note about the others.

## Dependency detection

Since the Agent Skills spec has no `dependencies` field, skillbun
infers dependencies by scanning skill content.

### Scan targets

1. SKILL.md body text
2. Files in references/
3. Import statements in scripts/

### Detection patterns

| Pattern | Confidence | Example |
|---|---|---|
| "read the X SKILL.md" | high | "read the skill-creator SKILL.md" |
| "follow X's section" | high | "follow skill-creator's eval section" |
| "invoke /X" or "use /X" | high | "invoke /skill-creator" |
| "X skill" in instructions | medium | "the skill-creator skill" |
| import from skill path | medium | `from skill_creator.scripts import` |
| tool name in compatibility | low | "requires skill-creator" |

### False positive filters

- Skill names appearing in examples or anti-patterns (not deps)
- Self-references (the skill mentioning its own name)
- Generic terms that happen to match skill names

### Cycle detection

If A depends on B and B depends on A, report the cycle and ask
the user to break it. Cycles indicate a design problem, not a
packaging problem.

## Excluded from bundles

These are stripped during collection:

| Pattern | Reason |
|---|---|
| `__pycache__/` | Python bytecode, rebuild on install |
| `node_modules/` | npm packages, reinstall on demand |
| `.DS_Store` | macOS metadata |
| `*.pyc`, `*.pyo` | Python bytecode |
| `evals/` | Test artifacts, not runtime |
| `*-workspace/` | Eval workspaces, not runtime |
| `.git/` | Version control, not distribution |

## Versioning

Bundle version tracks the collection, not individual skills.
If a skill updates, bump the bundle version and re-package.

Recommended: include a `CHANGELOG.md` in the bundle root for
non-trivial bundles that will be re-distributed.
