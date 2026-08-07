---
name: handoff
description: >-
  Session baton pass: compress live working state into HANDOFF.md so
  a fresh agent can continue in minutes, and verify-then-resume on
  the receiving side. Fires on two branches: leaving a session with
  work in flight ("handoff", "wrap up for the next agent", "done for
  today", context near its limit, switching agent or machine); and
  picking work back up ("pick up where we left off", "where are we",
  a HANDOFF.md sitting in the repo). Carries live state only -- the
  durable why-chain (decisions, rejected paths, tradeoffs) belongs
  in the devlog; what changed belongs to git.
---

# Handoff -- The Baton Pass

A handoff is the session squeezed to its resumable core: what a
fresh agent needs to continue, and nothing it can get from the repo
itself. Two moves: WRITE when leaving, RESUME when arriving.

The one-line test: a fresh agent reads HANDOFF.md, runs its Verify
block, and is productively working within five minutes -- without
scrolling any transcript.

A handoff is a claim about reality, not reality. The repo may have
moved since the doc was written, so every packet carries the
evidence (branch, commit, dirty count, test results) that lets the
next agent check it. When doc and repo disagree, the repo wins.

## Gate

Size the pass before writing:

| Situation | Do |
|---|---|
| Work committed, next step obvious from git log | No doc -- say so, point at the log |
| Clean tree, one known next step | Mini packet: Goal, Next, Verify only |
| Work in flight -- dirty tree, half-done plan, failing tests, open decision | Full packet |
| A decision worth keeping forever just got made | That part goes to the devlog entry; the handoff references it |

The most valuable output is often "no doc needed": a handoff that
restates git log is noise the next agent has to read past.

## WRITE

### 1. Evidence first

Look, don't remember. Before writing a word:

```bash
git rev-parse --abbrev-ref HEAD && git rev-parse --short HEAD
git status --porcelain        # dirty files, count them
git log --oneline -5          # recent motion
```

Then whatever proves working state: the test command with the tail
of its real output, the failing command verbatim, the build result.
A claim in the packet without a command behind it is a rumor.

Done when branch, commit, dirty count, and test/build state come
from command output, not from memory of the session.

### 2. Write the packet

One file, `HANDOFF.md`, at the repo root (no repo: `./HANDOFF.md`).
Overwrite any previous one -- one live baton, never an archive.

```markdown
# Handoff: <topic in five words>
> 2026-07-28 · feat/auth @ ab12cd3 · 4 dirty files

## Goal
What we are building and why, 1-3 sentences. Link the spec, issue,
or devlog entry that holds the detail -- do not restate it.

## State
Done / in flight / broken, as facts with evidence:
- JWT middleware extracted to src/auth/jwt.ts -- committed ab12cd3
- Refresh-token path half-done: src/auth/refresh.ts writes the
  cookie but nothing reads it yet
- Tests: `npm test` -> 34 pass, 2 fail in test/auth.test.ts
  (expected -- fixing them is step 1)

## Next
1. Make the two failing tests pass: read the refresh cookie in
   src/auth/session.ts:41, mirror what jwt.ts:88 does for access
   tokens
2. Wire /logout to revoke the refresh token
3. Then the plan's phase 3 (docs/plan.md)

## Don't repeat
- Storing refresh tokens in localStorage -- rejected, XSS surface
- express-jwt@8 upgrade -- breaks our custom error handler, pinned at 7

## Read first
1. docs/plan.md            -- the phase list this work follows
2. src/auth/jwt.ts         -- the pattern step 1 mirrors
3. test/auth.test.ts       -- the two failures define done

## Verify
git rev-parse --short HEAD    # expect ab12cd3 -- if not, git log ab12cd3..HEAD
git status --porcelain | wc -l  # expect 4
npm test                      # expect 34 pass / 2 fail in auth.test.ts
```

The example above is the anatomy; adapt sections to the situation,
never pad one that has nothing to say. Rules that hold regardless:

- **Next #1 is executable within a minute of reading** -- a command,
  or a file:line plus the specific edit. "Continue the refactor" is
  not a step; it is the absence of one. This single rule carries
  most of the skill.
- **Reference, don't copy.** Anything already in a spec, plan,
  commit message, diff, or devlog entry appears here only as a path
  or URL. Copies rot; references stay true.
- **Don't repeat earns its keep** -- one line per dead end with why
  it died. This is the section the next agent can get from nowhere
  else; the repo shows what exists, never what was tried and abandoned.
- **Read first is ordered and minimal** -- most important first so a
  tight-context agent can stop early. Everything the session touched
  is not the list; what step 1 needs is.
- **Self-contained.** The next agent has no transcript. Any sentence
  leaning on "as discussed" or "the earlier approach" is broken.
- **Redact.** No keys, tokens, passwords, or PII -- name where a
  secret lives (.env: STRIPE_KEY), never its value.

### 3. Hand over the baton

End your reply with a copy-paste block for the next session -- the
packet has the detail; this is just the entry point:

```
Read HANDOFF.md first, run its Verify block, then continue.
Task: finish the refresh-token path (2 failing tests define done).
Constraint: don't touch the express-jwt version.
```

### Check before finishing

Smash the packet against each; fix, don't ship:

- Next #1 needs interpretation before action -> rewrite until it's
  a command or file:line edit
- A State claim has no command output behind it -> run the command
  or mark the claim `unverified:`
- Any paragraph restates a spec/plan/commit -> replace with the path
- A secret or credential value survives -> redact
- "As discussed" / "as mentioned above" appears -> rewrite self-contained
- Baton block missing from the reply -> add it; the doc without the
  entry point strands the operator

## RESUME

Arriving in a fresh session where HANDOFF.md exists (or the user
points at one):

1. **Read the whole packet.** It is short by construction.
2. **Reality-check it.** Run the Verify block. Compare recorded
   commit against HEAD; recorded dirty count against now. On drift,
   `git log <recorded>..HEAD --oneline` shows what happened since --
   fold that into the picture and trust the repo over the doc.
3. **Orient out loud.** One short paragraph to the user: the goal,
   where things stand, any drift found, and the first move. Not a
   re-litigation of settled decisions -- those live in the devlog
   and the references.
4. **Start on Next #1.** Deviate only when the reality check
   contradicts it, and say so when you do.

Done when the orientation is stated and step 1 is underway -- resume
ends in motion, not in a summary.

## Anti-patterns

Named for diagnosis, not steering:

- **Transcript cosplay** -- the packet narrates the conversation
  instead of the state. The next agent needs what IS, not what was said.
- **Museum baton** -- dated handoff-2026-07-12.md files accumulating
  in the repo. One live file, overwritten; git remembers the rest.
- **Trust-me packet** -- states with no Verify block, claims with no
  commands. Continuity built on rumor breaks at the first drift.
- **Everything bagel** -- ten sections, every file touched, the full
  plan restated. Compression is the job; a handoff longer than a
  screen has failed it.
- **Blind resume** -- picking up Next #1 without the reality check.
  The doc was true once; the repo is true now.

---
