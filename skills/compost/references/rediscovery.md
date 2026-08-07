# The rediscovery test

A doc claims to add knowledge on top of the code. Test the claim:
give an agent the code and the doc's questions -- never the doc --
and see how much of the doc it reconstructs. What comes back is a
measurement of the doc's added value for exactly the reader who
will consume it.

## When to run it

Run the test on contested and load-bearing docs only. A file
titled "How AuthService works" that walks the implementation
paragraph by paragraph needs no trial -- tag it `restate` and
move on. The test earns its cost when:

- someone (human or your own judgment) resists the `restate` tag,
- the doc is old enough that nobody knows whether it still tells
  the truth,
- the doc mixes genres -- some restatement, some possible `why` --
  and you need a per-claim split.

Cost shape: one subagent per doc, all of the doc's claims batched
into one dispatch, independent docs run in parallel.

## Step 1 -- Extract claims

A checkable claim is a concrete behavioral statement: a value, an
ordering, an invariant, a dependency, an "X happens when Y."
Opinions, motivations, and tutorials are not claims -- a doc with
fewer than three checkable claims is not restatement material at
all; judge it directly (it is usually `why` or `human-only`).

Aim for 5-12 claims per doc. More than that, sample: take the
ones whose loss would scare the doc's defender most.

## Step 2 -- Write neutral questions

Rewrite each claim as a question that does not leak the answer.
The doc says "the upload client retries 3 times with exponential
backoff":

- Leading (wrong): "Does the upload client retry 3 times?"
- Neutral (right): "What happens when an upload request fails?"

One idea per question. You have read the doc; the subagent must
not -- keep the doc out of its context and keep the doc's
phrasing out of your questions.

## Step 3 -- Dispatch the blind reader

One subagent per doc, prompt shaped like:

```
You are answering questions about a codebase. You have no
documentation -- answer ONLY from the code under <path>.

For each question:
- answer concretely,
- cite file:line for every part of the answer,
- rate confidence: certain / probable / cannot-determine.

If the code cannot yield an answer, say cannot-determine --
do not guess.

Questions:
1. ...
2. ...
```

## Step 4 -- Grade

Per claim:

- **REDISCOVERED** -- the answer substantively matches the doc's
  claim. Not verbatim: "retries with growing delays, up to
  MAX_RETRIES = 3" matches "3 times with exponential backoff."
  If a claim matches in part, split it and grade the parts.
- **UNREACHABLE** -- the subagent answered cannot-determine, and
  a spot-check confirms the code genuinely does not carry the
  answer. Before granting this verdict, run the navigation
  re-check below -- most misses are misses of the map, not of
  the code.
- **CONTRADICTED** -- the subagent's cited answer and the doc
  disagree, and the citations hold up. Verify the citation
  before believing either side.

### The navigation re-check

A cannot-determine can mean two different things. Re-run the
failed question with the relevant file named in the prompt:

- The answer flips to a confident match -- the code carries it,
  the agent just couldn't find it. That is a missing road, not a
  keeper: add the navigation line, grade the claim REDISCOVERED.
- Still cannot-determine -- the knowledge genuinely is not in the
  code. UNREACHABLE stands; promote it.

This distinction is the test's second product: it maps your
codebase's navigation gaps as a side effect.

## Step 5 -- Score the doc

| Claim mix | Doc verdict |
|---|---|
| All or nearly all REDISCOVERED | A cache of the code. Compost. |
| Mixed | Compost the body; promote each UNREACHABLE claim to its keeper genre |
| Mostly UNREACHABLE | This was never restatement -- retag (`why` or `human-only`) and keep whole |
| Any CONTRADICTED | Stop scoring. Resolve the dual truth first -- it outranks everything else in the pass |

Resolving CONTRADICTED: decide which side is right. If the doc
encoded a real decision the code drifted from, the code has a
bug and the decision deserves an ADR that outlives this doc. If
the code legitimately moved on, the doc dies -- and if the move
itself was a non-obvious decision, that decision gets the ADR.
Either way the doc's version of the claim does not survive as
prose.

## Honesty rules

- The blind reader never sees the doc, a summary of the doc, or
  your expectations. Contamination makes every REDISCOVERED
  verdict worthless.
- Grade against what the doc actually says, not what it
  plausibly meant.
- An agent giving up is not evidence of UNREACHABLE -- only the
  navigation re-check plus your spot-check is.
- Record the verdict sheet (claim, question, answer, citation,
  verdict) next to the pass. It is the evidence the deletion
  survives review with.
