# Sources -- Goal Engineering and Agentic Loops

Curated from HN, X, articles, and competing skills. Organized by
what they teach, not when they were posted.


## On goals as engineering contracts

**A sufficiently detailed spec is code**
https://news.ycombinator.com/item?id=47434047
Core philosophical thread: as a goal prompt gets precise enough,
it converges toward code, tests, or formal spec. The implication:
natural language is useful for intent but weak as final truth.

**Leslie Lamport: Thinking for Programmers**
https://news.ycombinator.com/item?id=7533938
Writing is thinking. Specs expose sloppy thought before code
exists. Directly applicable to goal prompts.

**Get Shit Done: meta-prompting, context engineering, spec-driven dev**
https://news.ycombinator.com/item?id=47417804
Best direct thread on frameworks around specs, plans, and agents.
Strong debate over whether meta-frameworks help or just burn tokens.


## On agentic coding workflows

**What is agentic engineering?**
https://news.ycombinator.com/item?id=47393908
Requirements, tests, CI, docs, modularity still matter. The tools
changed; the discipline didn't.

**We put a coding agent in a while loop**
https://news.ycombinator.com/item?id=45005434
Directly on goal loops. Exit conditions, autonomous iteration,
prompt length effects, real experiences.

**Ask HN: Why are AI coding agents not working for me?**
https://news.ycombinator.com/item?id=46598278
Context management, task slicing, treating the agent like a
mid-level engineer, reviewing against spec.

**Getting good results from Claude Code**
https://news.ycombinator.com/item?id=44836879
Practical prompting, Socratic planning, incremental steps, specs,
CLAUDE.md usage, iterative review loops.

**Agentic Coding Recommendations**
https://news.ycombinator.com/item?id=44255608
Planning first ("do not write code"), writing plans to MD files,
agent self-critique, real workflows.


## On quality and failure modes

**Breaking the spell of vibe coding**
https://news.ycombinator.com/item?id=47006615
Hidden costs: dead-end architecture, shallow understanding,
hallucinated bugs, ownership loss.

**Ask HN: Anyone struggling to get value out of coding LLMs?**
https://news.ycombinator.com/item?id=44095189
High-signal disagreement. Greenfield/boilerplate works; complex
existing systems are harder. Code quality is the bottleneck.

**Why don't software development methodologies work?**
https://news.ycombinator.com/item?id=15885171
Ownership, team quality, and short feedback loops beat ritual.
Process is context-sensitive.


## On prompt and context engineering

**Effective context engineering for AI agents** (Anthropic)
https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
High-signal minimal context. JIT retrieval over context dumps.
Compaction/summarization for long sessions.

**Claude.md, Skills, Subagents, Plugins, and MCPs**
https://news.ycombinator.com/item?id=48289950
CLAUDE.md examples, skills, structuring instructions, delegation.


## On loop engineering

**Addy Osmani -- Loop Engineering**
https://addyosmani.com/blog/loop-engineering/
Clear definition. /goal vs /loop. Benefits/risks (token costs,
comprehension debt). Sub-agents, skills, worktrees, external state.

**What Is Loop Engineering?** (MindStudio)
https://www.mindstudio.ai/blog/what-is-loop-engineering-ai-coding-agents
Iterative cycles (ReAct-style), building blocks, patterns
(retry, plan-execute-verify, multi-agent), failure modes.


## On goal prompt structure (X/Twitter)

**@kloss_xyz goal template**
https://x.com/kloss_xyz/status/2054096165055217987
GOAL/CONTEXT/CONSTRAINTS/PLAN/DONE WHEN/VERIFY/OUTPUT/STOP RULES
structure. Most cited practical template for /goal prompts.

**@selinaai_ on treating agents as senior engineers**
https://x.com/selinaai_/status/2067429531389202871
Stop saying "do this" -- use structured goals instead.


## Competing skills -- what they teach

**OpenAI define-goal** (openai/skills)
Quantification heuristics by domain (bugs, tests, performance,
quality, research, operations). Lean contract-first approach.
Strong examples of good vs weak goals. Codex-specific API hooks.

**dbs-goal** (dontbesilent2025/dbskill) -- 6.3K installs
Wittgenstein's language philosophy applied to goal clarification.
"Engine idling" concept: words must do work. Three tests:
pointability, falsifiability, real endpoint. Strongest in life/
business goals; engineering goals need different treatment.

**qiaomu-goal-meta-skill** (joeseesun) -- 609 installs
Pause conditions vs stop conditions distinction. Iteration policy.
Discovery-first goals for unfamiliar domains. Risk classification.
Bilingual (Chinese/English). Codex-specific output format.

**mattpocock to-prd** -- 288K installs
No interview -- just synthesizes existing conversation into PRD.
Testing seams concept. Highest adoption of any planning skill.
PRD scope, not goal scope.

**obra/superpowers writing-plans** -- 159K installs
Detailed implementation planning with TDD. Bite-sized tasks.
Self-review checklist. Assumes spec already exists.


## Key insight (consensus across all sources and competitors)

Agents amplify clear thinking. If you can define the outcome,
evidence, and constraints, they move fast. If you cannot, they
produce plausible code around the wrong mental model.

The rare skill is not "prompting." It is turning intent into a
small, falsifiable engineering contract -- one that distinguishes
between "I don't know which path" (stop and ask) and "I can't
proceed" (pause and surface the blocker).
