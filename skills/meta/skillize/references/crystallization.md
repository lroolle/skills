# Crystallization Heuristics

How to separate repeatable workflow from incidental session noise.

## Signal strength hierarchy

Not all session evidence is equal. Ranked by reliability:

### Tier 1: User corrections (highest signal)

When the user says "no, do X instead" or "stop doing Y", that's a
direct statement about where Claude's defaults fail. But not every
correction is durable. Classify before encoding:

| Type | Durability | Action | Example |
|---|---|---|---|
| Durable rule | Permanent | Instruction or anti-pattern | "Always use Read, not cat" |
| Local preference | Per-user | Parameterize | "I prefer org-mode format" |
| One-off env fix | Ephemeral | Drop | "Use absolute path X not ~" |
| Unresolved judgment | Uncertain | Note as tradeoff | User changed mind mid-stream |

Only durable rules harden into the skill. Local preferences become
parameters with the user's choice as default. One-off fixes get
dropped. Unresolved judgments get noted in a "Tradeoffs" or
"Open questions" section so future users know the decision is live.

**Test**: Would this correction apply to someone else running the
same workflow on a different machine, different day? If yes, it's
durable. If only for this user, parameterize. If only for this
session, drop.

Examples:
- "Don't use symlinks, cp instead" -> durable anti-pattern
- "User scope, not project scope" -> local preference (parameterize)
- "Read the file first, don't grep" -> durable process instruction
- "Actually, let's try the other approach" -> unresolved judgment

### Tier 2: Repeated tool sequences

If the same 3+ tool calls appeared in the same order multiple times,
that's a stable subprocess. It should become a named step in the
skill's process section.

Look for:
- Read -> Edit -> Read (verify pattern)
- Search -> Read -> Write (research-then-create)
- Bash(test) -> Edit -> Bash(test) (fix loop)
- Any sequence that appeared 2+ times

**Extraction rule**: Name the subsequence. Describe when to invoke it.
Include the specific tools if the choice is non-obvious (e.g., "use
Read, not cat" or "use grep, not the Explore agent").

### Tier 3: Domain knowledge discovered

Information the session had to look up, research, or discover that
wouldn't be obvious to Claude on a fresh start. This includes:
- API details, configuration formats, file locations
- Library quirks, platform-specific behavior
- Organizational conventions (naming, directory structure, process)

**Extraction rule**: If it took >1 tool call to find, it belongs in
`references/`. If it's a single fact, inline it in SKILL.md.

### Tier 4: Architectural decisions

Choices about structure, scope, or approach that the user confirmed.
These set the skill's default posture.

Examples:
- "Layered architecture: L0 -> L1 -> L2 -> L3"
- "Separate source repo from install location"
- "Under 500 lines for SKILL.md"

**Extraction rule**: Decisions become structural constraints in the
skill. State the constraint and the reasoning.

### Tier 5: Output shape (lowest reliable signal)

What the session produced. This tells you the skill's expected output
format, but be careful -- the specific content is incidental even if
the structure is repeatable.

**Extraction rule**: Abstract the output to its structure. "Produces
a SKILL.md with frontmatter + 6 sections" not "produces a file about
UX design with sections for principles, patterns..."

## Noise filters

### Exploration and false starts

Early-session tool calls are often exploratory. If a Read or Search
was followed by a completely different direction, it was exploration,
not workflow. Drop it unless the exploration itself is the skill's
purpose (e.g., a research skill).

**Test**: Would this step appear if you already knew the answer?
If no, it's exploration.

### Environment-specific steps

Steps that depend on the current machine, directory structure, or
installed tools. These don't transfer.

Examples:
- "cd to /home/user/projects/..." (specific path)
- "Install X with brew" (specific package manager)
- "The config is at ~/.config/tool/..." (specific tool setup)

**Test**: Would this step work on a different machine?
If no, either parameterize the path or drop the step.

### One-off debugging

Error -> fix -> retry cycles where the error was caused by typo,
stale state, or misunderstanding. The fix belongs in the code, not
the skill.

**Test**: Would this error recur in a fresh session on the same
workflow? If no, drop it. If yes, add it as an anti-pattern.

Note: recurring diagnostic *workflows* (memory leak investigation,
incident triage playbooks) are good skill candidates even though
they involve debugging. The filter is whether the *fix* or the
*process* is the reusable part.

### Conversational scaffolding

Clarification questions, confirmations, name brainstorming, voting
on options. These are session mechanics, not workflow.

**Exception**: If the skill requires user input at a specific point
(e.g., "ask which scope to install to"), model that as a decision
point in the process.

## Parameterization

Some steps are repeatable in *shape* but variable in *content*.
These should be parameterized.

### Identifying parameters

Look for values that:
- Were provided by the user or derived from user input
- Would be different in a different invocation
- Are used in multiple steps (so they need a name)

### Common parameter patterns

| Pattern | Example | Parameterize as |
|---|---|---|
| Target directory | ./output/my-skill/ | `<target-dir>` |
| Name/identifier | "kiln" | `<skill-name>` |
| Scope choice | user vs project | Decision point |
| Input source | conversation context vs file | Mode flag |
| Output format | org vs markdown | Format parameter |

### What NOT to parameterize

- Internal constants that the workflow always uses
- Tool choices (Read vs cat) -- these are instructions, not parameters
- Quality criteria -- these are constraints, not variables

## Composition detection

Sometimes a session contains multiple workflows. Signs:

- Clear topic shift in the conversation
- Different tool sets used in different phases
- User explicitly said "ok now let's do Y"

If the session has 2+ distinct workflows, ask the user which to
crystallize. Or crystallize each as a separate skill.

## Minimum viable skill

Not every workflow needs references/, scripts/, or complex structure.

| Session complexity | Skill structure |
|---|---|
| Simple (5-10 steps, no domain knowledge) | SKILL.md only |
| Medium (10-20 steps, some domain content) | SKILL.md + 1-2 references |
| Complex (20+ steps, deep domain, scripts) | Full structure |

Start minimal. The eval phase will reveal if more structure is needed.
