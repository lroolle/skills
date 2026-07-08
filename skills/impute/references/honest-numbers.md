# Honest numbers — the claims discipline

The counterintuitive move: qualifying your claims makes them sell
better. Specificity is what credibility sounds like; hedged
superlatives are what marketing sounds like.

## Rules

1. **Scope every number.** Not "up to 95% savings" but "60–95%
   (JSON tool outputs), 15–20% (coding agents)". The scoped
   version is smaller and more believable — and the reader trusts
   the rest of the page more because of it.
2. **Ship the reproduce path with the claim.** Benchmark tables
   end with the command that regenerates them. A number without a
   repro path is an opinion.
3. **Label estimates as estimates.** When a number cannot be
   measured directly (counterfactuals: "tokens you would have
   spent"), say "estimated", show a confidence range, and offer a
   measured mode (holdout/control) for those who want ground
   truth. Never present a model's guess as a measurement.
4. **Show what didn't change.** Savings claims need an accuracy
   table proving the answers stayed the same (GSM8K ±0.000). Every
   improvement claim implies a "at what cost?" question — answer
   it before it's asked.
5. **Write the anti-pitch.** A "When to skip" section listing who
   should NOT use this. It filters out bad-fit users (who would
   otherwise become bad-fit issue reporters) and signals the
   author has nothing to hide.
6. **Attribute generously.** Name competitors, call them excellent
   when they are, explain how you build on them and thank the
   teams by name. Generosity reads as confidence; silence about
   alternatives reads as fear of comparison.
7. **Honest defaults are marketing.** A CHANGELOG entry like
   "telemetry is opt-in, off by default, fail-closed" builds more
   trust than any feature bullet. Defaults are claims about whose
   side you're on.

## Applies to

README proof sections, release notes, launch posts, GitHub
descriptions, comparison tables, benchmark docs — every outbound
sentence containing a number or a superlative.

## Check

Read the draft and circle every number and every superlative.
Each number: scoped? reproducible? labeled if estimated? Each
superlative: replace with a number or delete.
