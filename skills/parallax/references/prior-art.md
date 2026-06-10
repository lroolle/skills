# Prior art

parallax draws from established ideas in cognitive science and decision
theory. The specific motivation for building it as a skill came from
the "ADHD" movement in the Claude Code community (May 2026).

## The underlying insight

Separating idea generation from evaluation improves creative output.
This appears independently in:

- Osborn's brainstorming rules (1953): defer judgment during ideation
- Design thinking's double diamond: diverge then converge
- Edward de Bono's lateral thinking (1967): structured techniques for
  generating non-obvious alternatives
- Charlie Munger's multiple mental models: approach problems through
  different disciplinary lenses
- Eisenhardt (1989): teams that consider multiple alternatives
  simultaneously make faster, better decisions than those that evaluate
  one option at a time

The insight is not new. What's new is that LLMs need it packaged as
a protocol because they default to premature convergence -- each token
conditions the next, anchoring on whatever was said first.

## Claude Code ADHD ecosystem (May 2026)

Three projects share the label but solve different problems:

**UditAkhourii/adhd** -- Multi-agent orchestration that spawns parallel
isolated LLM calls under different cognitive frames (hardware engineer,
regulator, 10-year-old, speedrunner, etc.), then runs a separate
critic pass to score, cluster, prune traps, and deepen top candidates.
Built on Claude Agent SDK. ~10 API calls per run, 5-10x cost of a
single-shot answer.

Strongest contribution: demonstrating that structured divergent
ideation significantly improves breadth, novelty, and especially trap
detection in LLM outputs. Evals (6 problems, 5W/1L) show:

| Dimension | ADHD | Baseline | Delta |
|---|---:|---:|---:|
| trap_detection | 9.50 | 1.83 | +7.67 |
| novelty | 7.83 | 2.67 | +5.17 |
| breadth | 9.00 | 4.83 | +4.17 |
| actionability | 9.50 | 6.50 | +3.00 |
| builder_usefulness | 7.67 | 6.83 | +0.83 |

The single loss (CLI timeout UX) is instructive: ADHD's broad
exploration produced creative but impractical ideas for a problem
with a known standard engineering solution (builder_usefulness: 4
vs 9 baseline). Lesson: divergent thinking has a cost, and the cost
is highest when the problem doesn't need it.

**ravila4/claude-adhd-skills** -- Productivity scaffolding for ADHD
users: SQLite-backed time reminders via hooks, daily journals,
Obsidian integration, TDD workflow. Solves a human attention
management problem, not a model reasoning problem.

**assafkip/founder-skills** -- Behavioral rules for neurodivergent
founders: no-shame communication, energy-mode task tagging, rejection
sensitivity accommodation. Changes how Claude talks, not how it
thinks.

## How parallax differs

parallax takes the core insight from divergent ideation and builds a
lightweight protocol that works within a single agent session:

| | ADHD (UditAkhourii) | parallax |
|---|---|---|
| Requires | Agent SDK or Agent/Task tools | Nothing -- works in any SKILL.md-compatible agent |
| Phases | 2 (diverge, focus) | 3 (frame, spread, commit) |
| Framing phase | None -- jumps to divergence | Explicit: what are we deciding, what's fixed, what does good look like |
| Options generated | 30 (5 frames x 6 ideas) | 3-5 genuinely different approaches |
| Evaluation | Numerical scoring (N/V/F 0-10) | Trade-off comparison on user-defined dimensions |
| Trap detection | Scoring dimension | First-class operation: check every approach, structured finding techniques |
| Output | Ranked list + clusters + deepened branches | Single recommendation with runner-up and explicit trade-offs |
| Cost | ~10 LLM calls per run | 1 (single context) |
| Best for | Open brainstorming, maximum breadth | Decisions that need depth over breadth |

The key design choices:

1. **Three phases, not two.** The explicit framing phase prevents
   generating brilliant solutions to the wrong problem.

2. **Fewer, deeper options.** 3-5 approaches that differ on
   fundamental assumptions, not 30 surface-level variations.

3. **Always commits.** Outputs a recommendation, not a list. The user
   can override, but "here are 20 ideas, you decide" is a cop-out.

4. **No numerical scoring.** Comparing options on trade-offs the user
   can reason about beats scoring them 7.3 vs 7.1 on made-up scales.

5. **No infrastructure requirement.** Works in any agent that reads
   SKILL.md. When Agent tools happen to be available, the skill can
   optionally use them -- but doesn't require them.

6. **Explicit anchoring resistance.** ADHD eliminates cross-branch
   anchoring by construction (isolated API calls, no shared context).
   parallax fights it by instruction: push past the first three
   obvious answers, name shared assumptions before breaking them.
   This is weaker than architectural isolation but costs nothing and
   works in any context.

7. **Knows when to stand down.** ADHD's one eval loss shows divergent
   thinking hurts on standard engineering problems. parallax includes
   calibration guidance and a "Skip when" section that ADHD's
   pre-flight check approximates but doesn't fully address.
