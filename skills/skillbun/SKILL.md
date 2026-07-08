---
name: skillbun
description: >-
  Bundle agent skills into a distributable .skill archive: resolve
  inter-skill dependencies, rename to avoid collisions, validate,
  zip. Fires when the user wants to share or export skills, package
  a skill together with its dependencies, or prepare a collection
  for another machine or teammate. Creating or editing the skills
  themselves is skill-creator's job.
---

# /skillbun -- Skill Bundler

The Agent Skills spec defines single skills. A skill that depends on
another (skillize needs skill-creator's eval tooling) has no way to
declare or distribute that dependency. skillbun closes this gap:
resolve deps, rename to avoid collisions, validate, bundle, ship.

## Process

### 1. Identify targets

Accept one or more skill paths or names (full flag set under
Usage). For each target, verify SKILL.md exists and validate: frontmatter
has `name` and `description`, name matches directory, kebab-case.

### 2. Resolve dependencies

Scan each skill's SKILL.md and reference files for inter-skill
references. Detection heuristics:

**Explicit** (high confidence):
- "read the skill-creator SKILL.md" or similar
- References to paths containing another skill's name
- "follow skill-creator's section on X"

**Implicit** (medium confidence):
- "use /other-skill" or "invoke /other-skill"
- References to scripts/agents/assets in another skill's directory

**System** (note in manifest, don't bundle):
- `compatibility` field requirements (git, python, docker)

Build a dependency graph. Check for cycles. Present for confirmation:

```
skillize
  └── skill-creator (eval pipeline, scripts, agents)

2 skills, 0 cycles
Bundle? [Y/n]
```

### 3. Rename for distribution

Skills bundled from third-party sources should be renamed to avoid
collision with independently installed copies. The rename must be
consistent across three places:

1. **Directory name**: `skill-creator/` -> `ant-skill-creator/`
2. **Frontmatter `name:` field**: must match the new directory name
3. **References in other skills**: update any SKILL.md text that
   points to the old name

Naming convention for renamed skills:
- Prefix with a short namespace: `ant-` (Anthropic), `oai-` (OpenAI),
  or the author's handle
- Keep the original name recognizable after the prefix

Ask the user to confirm the rename mapping before applying:

```
Rename for bundling:
  skill-creator -> ant-skill-creator

Apply? [Y/n]
```

Skip rename when:
- The skill is the user's own (no collision risk)
- The user explicitly says `--no-rename`

### 4. Collect and stage

For each skill in the resolved graph:

1. Locate the skill directory. Search order:
   - Path provided by user
   - Current project `.claude/skills/` or `.agents/skills/`
   - User-scope skill directories
2. Copy to a staging directory as top-level siblings:
   ```
   <staging>/
   ├── skillize/
   └── ant-skill-creator/
   ```
3. Apply renames (directory + frontmatter `name:` field)
4. Update cross-references in SKILL.md files to use new names
5. Strip build artifacts: `__pycache__/`, `node_modules/`,
   `.DS_Store`, `*.pyc`, `evals/`, `*-workspace/`, `.git/`

### 5. Package

Output as `.skill` (zip). Multiple skill directories in one archive:

```bash
cd <staging>
zip -rq <bundle-name>.skill skill-a/ skill-b/
```

The `.skill` extension is a standard zip. Platforms that accept
`.skill` files will extract the contents. Each top-level directory
is a valid skill with its own SKILL.md.

Alternative: `.zip` extension for environments that don't recognize
`.skill`. Same contents, different extension.

### 6. Verify

After packaging, verify:

1. Each skill directory has valid SKILL.md
2. Every `name:` field matches its directory name
3. No stale cross-references to old (pre-rename) names
4. No personal paths, container-specific references, or secrets
5. Archive extracts cleanly

Present a summary:

```
skillize.skill (81 KB)
  skillize/            (2 files, 12 KB)
  ant-skill-creator/   (18 files, 128 KB)
```

## Anti-patterns

- **Name collision**: Bundling `skill-creator` without renaming it
  will overwrite the user's independently installed copy on extract.
  Always rename third-party skills.

- **Stale references**: Renaming the directory but not updating
  `name:` in frontmatter, or not updating references in dependent
  skills. All three must be consistent.

- **Bundling everything**: Only include actual dependencies, not
  every installed skill.

- **Personal paths**: Scrub container-specific paths, usernames,
  and environment-specific references before bundling.

- **Missing validation**: Every skill must pass validation. A
  bundle with an invalid skill installs broken tools silently.

## Usage

```
/skillbun <skill> [skill...]     # bundle named skills + deps
/skillbun --all                  # bundle all skills in current root
/skillbun --from <dir>           # bundle from specific directory
/skillbun --dry                  # show dep graph + renames, don't package
/skillbun --no-deps              # skip dependency resolution
/skillbun --no-rename            # skip rename step
```

## References

| File | Load when |
|---|---|
| [bundle-format.md](references/bundle-format.md) | Inspecting or modifying bundle structure |
