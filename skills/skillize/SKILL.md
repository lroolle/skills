---
name: skillize
description: >-
  Crystallize a session's workflow into a reusable agent skill:
  survey what happened, classify corrections by durability, extract
  the repeatable pattern, draft SKILL.md with references, optionally
  eval via skill-creator. Fires on two branches: the user wants the
  workflow just performed captured for reuse ("skillize this", "turn
  this into a skill"); or they notice a recurring pattern ("I keep
  doing this same thing"). Creating a skill from scratch with no
  session behind it is skill-creator's job.
---

# /skillize -- Session to Skill

A devlog captures *why* you made decisions. A skill captures *how* to
repeat the workflow. Skillize extracts the repeatable pattern from a
session and packages it as a Claude Code skill.

The test: if someone invokes this skill six months from now on a
similar problem, does it reproduce the quality of today's session
without re-discovering the process?

## When to skillize vs. when NOT to

**Good candidates:**
- Multi-step workflow that took 10+ minutes and would recur
- Process where you discovered non-obvious tool sequences
- Workflow with user corrections that became stable rules
- Domain-specific knowledge that required research to find
- Pattern where Claude kept going wrong until guided right
- Recurring diagnostic workflows (incident triage, leak hunting)

**Bad candidates:**
- One-off investigation (use /reflect instead)
- Simple task Claude handles well without guidance
- Workflow that depends entirely on specific data or context
- One-off debugging whose fix lives in code (not the process)
- Process that changes every time (no stable pattern)

## Process

### Phase 1: Survey

Reconstruct the session. Don't rely on memory -- check the evidence.

1. **Conversation scan**: Walk the conversation for tool calls, user
   corrections, repeated patterns, and stable decisions.

2. **Artifact check**: If inside a git repo, run `git diff` and
   `git log` to see what actually changed. If not in a git repo,
   inspect the conversation for files created or modified, scan
   target directories with `ls -lt`, and check file mtimes. Read
   files that were created or modified either way.

3. **Correction map**: Identify where the user redirected you.
   Classify each correction before encoding (see Tier 1 in
   `references/crystallization.md`):

   | Type | Action | Example |
   |---|---|---|
   | Durable rule | Encode as instruction/anti-pattern | "Use Read, not cat" |
   | Local preference | Parameterize, don't hardcode | "I prefer org format" |
   | One-off env fix | Drop | "Use absolute path X not ~" |
   | Unresolved judgment | Note as tradeoff, not rule | Changed direction mid-stream |

   Only durable rules harden into the skill.

4. **Tool sequence**: List the tools used in order. Look for:
   - Repeated subsequences (same 3-4 tools in the same order)
   - Tools that were always used together
   - Tools the user told you to use instead of your default choice

Produce a survey summary (internal, not written to file):

```
WORKFLOW: [2-5 word description]
TRIGGER: [what kind of user request starts this]
STEPS: [numbered sequence of what happened]
CORRECTIONS: [classified: durable / preference / env / judgment]
TOOLS: [tool sequence, noting which are essential vs incidental]
OUTPUT: [what the workflow produces]
DOMAIN: [knowledge that was discovered, not obvious from tools alone]
```

### Phase 2: Crystallize

This is the hard part. Separate what's *repeatable* from what's
*incidental*.

Read `references/crystallization.md` for the full heuristic set.
The core judgment:

**Keep** if the step would be needed in 80%+ of similar invocations.
**Parameterize** if the step varies but the shape stays the same.
**Drop** if the step was specific to today's data/context/environment.

For each step in the survey, classify:

| Classification | Action |
|---|---|
| Core | Include as instruction in SKILL.md |
| Parameterized | Include with variable markers |
| Domain knowledge | Move to references/ |
| Incidental | Drop |
| Anti-pattern | Include as "don't do this" |

Anti-patterns are especially valuable. If Claude went wrong and the
user corrected it with a durable rule, that correction is a landmine
for future sessions. Encode it explicitly.

### Phase 3: Draft

Write the skill. The structure follows the agent skills spec:

```
skill-name/
├── SKILL.md          (required)
└── Bundled Resources  (optional)
    ├── scripts/       executable code for deterministic tasks
    ├── references/    docs loaded into context as needed
    └── assets/        files used in output (templates, etc.)
```

**Progressive disclosure** -- skills load in three tiers:
1. **Metadata** (name + description): ~100 words, always in context
2. **SKILL.md body**: <500 lines ideal, loaded when skill triggers
3. **Bundled resources**: unlimited, loaded on demand by the skill

Keep SKILL.md under 500 lines. When approaching that limit, move
domain knowledge into references/ with clear pointers about when to
read each file.

**SKILL.md contents:**
- Frontmatter: name, description (see below)
- Purpose: one paragraph, what and why
- When to use / when not to: honest scope boundaries
- Process: step-by-step instructions
- Anti-patterns: things Claude gets wrong without guidance
- Output format: what the skill produces

**Writing style**: Explain the *why* behind instructions rather than
heavy-handed MUSTs. The model using this skill is smart -- when it
understands the reasoning, it adapts to edge cases instead of
following rigid rules off a cliff. If you find yourself writing
ALWAYS or NEVER in caps, reframe as reasoning.

**Description writing**: The description is the trigger mechanism.
Claude undertriggers skills -- it needs explicit nudging. Include:
- What the skill does
- Explicit trigger phrases ("turn this into a skill", "skillize")
- Adjacent situations to trigger on ("I keep doing this same thing")
- Negative boundary (what NOT to trigger on)
- Be pushy. "Use when the user mentions X, Y, or Z, even if they
  don't explicitly name the skill" is better than a terse summary.

### Phase 4: Install draft

Before writing to any target, check for collisions:

1. Check if `<target>/<name>/` already exists
2. If it exists: show a diff of the existing vs new SKILL.md,
   snapshot the old version to `<target>/<name>.bak-<YYYYMMDD>/`,
   then ask the user before overwriting
3. Never overwrite silently

Default install locations (detect which roots exist on this machine):

1. Current project's `.claude/skills/<name>/` if project-specific
2. User-scope skill directory (e.g., `~/.claude/skills/<name>/`)
3. Any additional skill roots the user has configured

If multiple user-scope skill roots exist, ask whether to install
to all of them or just one. Don't auto-mirror -- the user may have
intentional divergence between roots.

Ask the user which scope. Then copy to install location(s).

### Phase 5: Eval (optional)

The eval phase validates that the crystallized skill actually
reproduces the session's quality on similar problems. It is not
always needed.

**Skip eval when:**
- The skill is lightweight / process-only (under ~50 lines)
- The output is subjective (writing style, design taste)
- The user says `--dry` or just wants the draft

**Run eval when:**
- The skill has objectively checkable output
- The workflow is complex enough to break in subtle ways
- The user explicitly wants to iterate

If running eval, generate 2-3 realistic test prompts based on the
original session's trigger. These should be variations of what a
real user would say -- concrete, detailed, with context -- not the
exact words from this session and not abstract one-liners.

**If skill-creator is available** (check installed skill directories
for `skill-creator/SKILL.md`): follow its eval/optimize pipeline:

- Spawn with-skill and baseline runs in parallel
- Draft assertions while runs execute
- Grade, aggregate, launch eval viewer for the user
- Collect feedback, iterate on the skill
- Optionally run description optimization

**If skill-creator is NOT available**: run a lightweight eval:

- For each test prompt, invoke the skill yourself and capture output
- Compare the output against the session's original quality
- Ask the user to review: "Does this reproduce the workflow? What's
  missing or wrong?"
- Iterate based on their feedback

Either way, the eval loop ends when the user is satisfied or
feedback is empty.

### Phase 6: Ship

Final checklist:
- [ ] SKILL.md under 500 lines
- [ ] Description is pushy and trigger-generous
- [ ] Durable corrections encoded, one-off fixes dropped
- [ ] References loaded conditionally, not always
- [ ] No collision -- existing skill snapshotted if overwritten
- [ ] Installed to user's chosen scope(s)
- [ ] Eval passing (if eval was run)

## Usage

```
/skillize                    # Infer workflow from session context
/skillize deploy-pipeline    # Explicit topic / name hint
/skillize --dry              # Show the draft, don't write files
/skillize --scope user       # Pre-select install scope
/skillize --no-eval          # Skip eval, draft + install only
```

When called with no arguments, survey the conversation to identify the
dominant workflow. When called with a topic, use it as the skill name
hint and focus extraction on that workflow thread.

`--dry` prints the SKILL.md draft to the conversation for review
before writing any files.
