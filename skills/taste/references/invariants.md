# Behavioral invariants

Interaction rules that decide whether the user's mental model
survives a design change. They predate the web, survived every
visual trend since 1984, and apply to native apps, web apps, CLIs,
and agent interfaces alike. Check each: pass / fail / n-a.

Surface trends (saturated fonts, banned gradients) are kiln's
zeitgeist file — temporal, versioned, expiring. These are not that.
If a redesign violates one of these to look better, it is costume
by definition.

## 1. Visible state

The user can always see what exists, what is selected, and what
mode they are in. Landmarks stay put across state changes;
spatial arrangements that carry meaning are preserved.

Why: recognition beats recall. Every landmark that moves or
disappears forces the user to rebuild their map.

Smash when: navigation reshuffles between visits; selection or
focus is ambiguous; the current mode is invisible.

## 2. Disabled, not hidden

Temporarily unavailable commands stay visible and dimmed, with a
discoverable reason. Removing them teaches the user the command
never existed.

Why: the command's visible existence is part of the user's model
of what the system can do. Hiding it deletes learning, not clutter.

Smash when: options vanish based on state; the user must remember
where a command lives instead of seeing it.

## 3. Object first, then action

Show the thing, then offer what can be done to it. Select-then-act;
proposed changes displayed before applied. For agent UIs: show the
file, record, or operation first, then let the user apply a clear
action to that visible object.

Why: acting on an invisible object means acting on a guess.

Smash when: an action fires on something the user never saw; bulk
operations without a visible target set.

## 4. Discoverable first, fast second

Shortcuts, gestures, and command palettes accelerate visible paths;
they never replace them. A double-click, chord, or hidden swipe
must have a see-and-point equivalent.

Why: this dissolves the novice/expert tradeoff — the same command
keeps a discoverable path and a fast path. Efficiency-only design
locks new users out; discoverability-only design caps experts.

Smash when: a capability is reachable only by shortcut, hover, or
tribal knowledge.

## 5. Verbs on buttons

Buttons name the action they perform: Save, Discard, Delete 3
files. Not Yes/No/OK. A destructive button states its consequence
in its own label, and sits spatially apart from the safe default.

Why: the moment of clicking is the worst moment to make the user
re-derive what "Yes" refers to.

Smash when: a confirmation reads "Are you sure? OK/Cancel"; the
destructive and default actions are adjacent twins.

## 6. Undo over confirmation

Prefer reversibility — undo, version history, trash, recoverable
state — over asking permission. Confirm only genuinely costly or
irreversible operations, and say what makes them irreversible.

Why: forgiveness enables exploration; exploration is how users
learn. Frequent confirmations train blind clicking, which then
fails exactly when the dialog finally matters.

Smash when: routine actions demand confirmation; anything
destructive has neither undo nor warning; alert fatigue is treated
as a user problem (frequent alerts are a design bug).

## 7. Modes visible, temporary, escapable

When a mode is unavoidable, show it near the affected object, make
entry and exit obvious, prefer spring-loaded modes (held modifier)
over latched ones. A mode must never block saving or quitting.

Why: modes make the same input mean different things. An invisible
mode converts user intent into system betrayal.

Smash when: the user asks "why did it do that?" and the answer is
a mode they couldn't see; escape/cancel doesn't work somewhere.

## 8. Honest feedback, user's vocabulary

Acknowledge input immediately. Explain delays with progress,
failures with what failed, why, and what to do next — in the
user's words, not the system's internals.

Why: silence after input reads as breakage; jargon after failure
reads as blame.

Smash when: an action gives no acknowledgment; an error names an
internal code with no next step; a spinner hides a known duration.

## 9. Trustworthy representation

What the user sees corresponds to what they get: previews match
results, counts match reality, drafts look like their published
form. The visible state never lies to look tidier.

Why: the first discovered lie poisons every future preview.

Smash when: preview and output diverge; optimistic UI shows
success before it is true without reconciliation.

## 10. Label with the icon

Icons carry recognizable nouns well and abstract actions poorly.
Default to icon plus label; use text alone when text is clearer.
Icon-only earns its place through recognition testing, not through
looking clean.

Why: an unlabeled icon is a mode of remembering. The screenshot
looks tidier; every new user pays for it.

Smash when: navigation or destructive actions are icon-only;
meaning depends on hover.

## 11. Aesthetic integrity — last, and in service

Visual design exists to communicate structure: different kinds of
things look different, decoration never overwhelms meaning. This
invariant is deliberately last — it is real, and it is outranked
by all of the above.

Why: the original sin of costume redesigns is promoting this rule
to first place.

Smash when: decoration answers no comprehension question; two
different things are styled identically for symmetry's sake;
information was removed to make the layout breathe.
